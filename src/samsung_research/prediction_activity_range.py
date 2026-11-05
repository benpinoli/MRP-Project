"""Paired class activity/range proxies and fixed candidate; BYU_ORC_AGENTS.md applies."""
import argparse, hashlib, json, os
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def ridge(x,y,xpred,alpha):
    mean=x.mean(axis=0);scale=x.std(axis=0);scale=np.where(scale>0,scale,1.0);z=(x-mean)/scale;yp=y.mean();beta=np.linalg.solve(z.T@z+alpha*np.eye(z.shape[1]),z.T@(y-yp))
    return yp+(xpred-mean)/scale@beta,dict(mean=mean.tolist(),scale=scale.tolist(),intercept=float(yp),coefficients=beta.tolist())

def activity_and_ranges(grid, normalized):
    ratio=pd.to_numeric(grid.volume_ratio,errors='coerce');activity=np.log(ratio.where(ratio>0))
    previous=activity.shift(1).rolling(60,min_periods=60).mean();out=pd.DataFrame({'date':grid.date,'activity_surprise':activity-previous})
    by_class={}
    for name in ('preferred','common'):
        records=[]
        for r in normalized:
            if r['class_name']!=name:continue
            try: lo=float(r['prcld']);hi=float(r['prchd']);close=float(r['prccd'])
            except (ValueError,TypeError):continue
            if r['price_eligible'] and np.isfinite([lo,hi,close]).all() and lo>0 and hi>=lo and lo<=close<=hi:
                records.append((r['datadate'],np.log(hi/lo)))
        by_class[name]=pd.Series(dict(records),dtype=float)
    out['relative_range']=out.date.map(by_class['preferred'])-out.date.map(by_class['common'])
    d=pd.to_datetime(out.date);out['QE']=((d.dt.month.isin([3,6,9,12]))&(d.dt.day>=25)).astype(int);out['YE']=((d.dt.month==12)&(d.dt.day>=25)).astype(int)
    return out

def build_states(grid,cfg):
    from samsung_research.e01 import load_and_validate
    pair=json.loads((ROOT/cfg['inputs']['pair_config']['path']).read_text())
    _,_,_,normalized=load_and_validate(ROOT/cfg['inputs']['raw']['path'],pair)
    return activity_and_ranges(grid,normalized)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);a=ap.parse_args();cfg=json.loads(Path(a.config).read_text())
    for name,item in cfg['inputs'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('hash mismatch '+name)
    grid=pd.read_csv(ROOT/cfg['inputs']['grid']['path']);grid=grid[grid.observed_session.astype(str).str.lower().eq('true')].reset_index(drop=True);q=pd.to_numeric(grid.discount_pct);features=build_states(grid,cfg);features['d1']=q.diff()
    blocks={'G2':['d1','activity_surprise','relative_range'],'C2':['d1','QE','YE']};ix={d:i for i,d in enumerate(grid.date)};allrows=[];audits=[]
    for source in ('validation','final'):
        p=pd.read_csv(ROOT/cfg['inputs'][source+'_predictions']['path']);refs=json.loads((ROOT/cfg['inputs'][source+'_refits']['path']).read_text());refs=[r for r in refs if r['family']=='H1' and r['alpha']==100]
        e=pd.read_csv(ROOT/cfg['inputs']['e_forecasts']['path']);e=e[(e.source==source)&(e.model=='D1')]
        for h in (1,5,20):
            x=p[(p.h==h)&(p.family=='H1')&(p.alpha==100)].copy()
            for b in ('Z0','A0'):
                base=p[(p.h==h)&(p.family==b)][['origin','prediction']].rename(columns={'prediction':b});x=x.merge(base,on='origin',validate='one_to_one')
            d=e[e.h==h][['origin','prediction_new']].rename(columns={'prediction_new':'D1OLS'});x=x.merge(d,on='origin',validate='one_to_one')
            ref=pd.DataFrame([r for r in refs if r['h']==h]);ref['month']=ref.refit_origin.str[:7];x['month']=x.origin.str[:7];x=x.merge(ref[['fold','month','refit_origin']],on=['fold','month'],validate='many_to_one')
            x=x.merge(features,left_on='origin',right_on='date',validate='many_to_one')
            for block,columns in blocks.items():
                complete=features[columns].notna().all(axis=1); eligible=x[x[columns].notna().all(axis=1)]
                for (fold,origin),g in eligible.groupby(['fold','refit_origin']):
                    pos=ix[origin];train=(np.arange(len(q))+h<pos)&q.notna().to_numpy()&q.shift(-h).notna().to_numpy()&complete.to_numpy();y=(q.shift(-h)-q)[train].to_numpy()
                    if train.sum()<252:continue
                    for model,cols in [('D1r',['d1']),(block,columns)]:
                        pred,detail=ridge(features.loc[train,cols].to_numpy(),y,g[cols].to_numpy(),100)
                        if not np.isfinite(pred).all():raise ValueError('nonfinite prediction')
                        r=g.copy();r['block']=block;r['model']=model;r['prediction_new']=pred;r['source']=source;allrows.append(r);ti=np.flatnonzero(train)
                        audits.append(dict(source=source,h=h,fold=int(fold),block=block,model=model,refit_origin=origin,training_n=len(ti),training_first_origin=grid.date.iloc[ti[0]],training_last_label_end=grid.date.iloc[ti[-1]+h],features=cols,**detail))
    if not allrows:raise ValueError('no forecasts')
    result=pd.concat(allrows,ignore_index=True);run=Path(a.run);run.mkdir(parents=True,exist_ok=False);result.to_csv(run/'forecasts.csv',index=False);features.to_csv(run/'activity_range_alignment.csv',index=False);(run/'refits.json').write_text(json.dumps(audits,indent=2)+'\n')
    stats=[]
    for keys,g in result.groupby(['source','h','fold','block','model']):
        for variant in ('main','strict'):
            z=g if variant=='main' else g[g.strict_interval]
            if z.empty:continue
            for b,col in [('candidate','prediction_new'),('Z0','Z0'),('A0','A0'),('H1','prediction'),('D1OLS','D1OLS')]:
                e=z.actual-z[col];ss=(z.actual**2).sum();stats.append(dict(source=keys[0],h=keys[1],fold=keys[2],block=keys[3],model=keys[4],variant=variant,benchmark=b,n=len(z),mae=abs(e).mean(),rmse=np.sqrt((e**2).mean()),r2_oos=1-(e**2).sum()/ss if ss else np.nan))
    pd.DataFrame(stats).to_csv(run/'metrics.csv',index=False)
    f=result[result.model.isin(['G2','C2'])];b=result[result.model=='D1r'][['source','h','block','origin','prediction_new']].rename(columns={'prediction_new':'D1r'});paired=f.merge(b,on=['source','h','block','origin'],validate='one_to_one');paired.to_csv(run/'paired_forecasts.csv',index=False)
    uncertainty=[]
    for keys,full in paired.groupby(['source','h','block']):
        dates=grid.loc[(grid.date>=full.origin.min())&(grid.date<=full.origin.max()),'date'].reset_index(drop=True)
        for variant in ('main','strict'):
            z=full if variant=='main' else full[full.strict_interval]
            for base in ('D1r','D1OLS','Z0','A0','prediction'):
                loss=abs(z.actual-z[base])-abs(z.actual-z.prediction_new);values=dates.map(pd.Series(loss.to_numpy(),index=z.origin)).to_numpy()
                for block in sorted(set([max(20,2*keys[1]),60])):
                    rng=np.random.default_rng(20261105);means=[]
                    for _ in range(2000):
                        starts=rng.integers(0,len(values)-block+1,size=int(np.ceil(len(values)/block)));sample=values[(starts[:,None]+np.arange(block)).ravel()[:len(values)]]
                        if not np.isfinite(sample).any():raise ValueError('empty bootstrap draw')
                        means.append(np.nanmean(sample))
                    uncertainty.append(dict(source=keys[0],h=keys[1],block=keys[2],variant=variant,benchmark='H1' if base=='prediction' else base,block_length=block,n=len(z),draws=2000,seed=20261105,mean_gain=loss.mean(),ci025=np.quantile(means,.025),ci975=np.quantile(means,.975)))
    pd.DataFrame(uncertainty).to_csv(run/'uncertainty.csv',index=False)
    coverage=[]
    for keys,g in paired.groupby(['source','h','block']):
        for field in ('QE','YE'):
            selected=g[g[field]==1];d=pd.to_datetime(selected.origin);windows=(d.dt.year.astype(str)+'Q'+d.dt.quarter.astype(str)).nunique()
            coverage.append(dict(source=keys[0],h=keys[1],block=keys[2],feature=field,origins=len(g),active_rows=len(selected),distinct_quarter_windows=windows))
    pd.DataFrame(coverage).to_csv(run/'calendar_coverage.csv',index=False)
    stability=[]
    for keys,g in paired[paired.source=='final'].groupby(['h','block',paired.origin.str[:4]]):
        for base in ('D1r','D1OLS','Z0','A0','prediction'):
            stability.append(dict(h=keys[0],block=keys[1],year=keys[2],baseline=base,n=len(g),candidate_mae=abs(g.actual-g.prediction_new).mean(),baseline_mae=abs(g.actual-g[base]).mean()))
    pd.DataFrame(stability).to_csv(run/'stability.csv',index=False)

    for name,item in cfg['inputs'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('input changed '+name)
    (run/'provenance.json').write_text(json.dumps({'scope':cfg['scope'],'code_sha256':digest(__file__),'config_sha256':digest(a.config),'inputs':cfg['inputs']},indent=2)+'\n')
if __name__=='__main__':main()
