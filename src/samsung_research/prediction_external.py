"""Delayed-current-vintage external state joins and fixed candidate; BYU_ORC_AGENTS.md applies."""
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

def prepare_source(frame,date_col,value_col,minimum,maximum,kind):
    f=frame[[date_col,value_col]].copy();f.columns=['source_date','value'];f.source_date=pd.to_datetime(f.source_date);f['value']=pd.to_numeric(f.value,errors='coerce');f=f[(f.source_date>=minimum)&(f.source_date<=maximum)&f.value.notna()].sort_values('source_date').reset_index(drop=True)
    if f.source_date.duplicated().any():raise ValueError('duplicate source dates')
    if kind in ('vix','fx') and (f.value<=0).any(): raise ValueError('nonpositive index/exchange rate')
    f['baseline_date']=f.source_date.shift(5);old=f.value.shift(5)
    f['change5']=np.log(f.value/old) if kind in ('vix','fx') else f.value-old
    if kind=='vix':f['level']=np.log(f.value)
    return f

def align_source(origins,source,kind,delay,max_age):
    left=pd.DataFrame({'origin':pd.to_datetime(origins)});left['cutoff']=left.origin-pd.to_timedelta(delay,unit='D')
    joined=pd.merge_asof(left.sort_values('cutoff'),source,left_on='cutoff',right_on='source_date',direction='backward');joined['age']=(joined.origin-joined.source_date).dt.days
    cols=['source_date','baseline_date','age','change5']+(['level'] if kind=='vix' else [])
    invalid=joined.age>max_age
    joined.loc[invalid,cols]=np.nan
    return joined[cols].rename(columns={c:kind+'_'+c for c in cols})

def ridge(x,y,xpred,alpha):
    mean=x.mean(axis=0);scale=x.std(axis=0);scale=np.where(scale>0,scale,1.0);z=(x-mean)/scale;yp=y.mean();beta=np.linalg.solve(z.T@z+alpha*np.eye(z.shape[1]),z.T@(y-yp))
    return yp+(xpred-mean)/scale@beta,dict(mean=mean.tolist(),scale=scale.tolist(),intercept=float(yp),coefficients=beta.tolist())

def build_states(grid,cfg):
    out=pd.DataFrame({'date':grid.date})
    for kind,source in cfg['external'].items():
        path=ROOT/source['path'];raw=pd.read_csv(path);f=prepare_source(raw,source['date'],source['value'],source['min_date'],cfg['max_source_date'],kind)
        aligned=align_source(grid.date,f,kind,source['delay_days'],source['max_age_days']);out=pd.concat([out,aligned],axis=1)
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);a=ap.parse_args();cfg=json.loads(Path(a.config).read_text())
    for name,item in cfg['inputs'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('hash mismatch '+name)
    for name,item in cfg['external'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('hash mismatch '+name)
    grid=pd.read_csv(ROOT/cfg['inputs']['grid']['path']);grid=grid[grid.observed_session.astype(str).str.lower().eq('true')].reset_index(drop=True);q=pd.to_numeric(grid.discount_pct);features=build_states(grid,cfg);features['d1']=q.diff()
    columns=['d1','vix_level','vix_change5','fx_change5','rate_change5'];complete=features[columns].notna().all(axis=1);ix={d:i for i,d in enumerate(grid.date)};allrows=[];audits=[]
    for source in ('validation','final'):
        p=pd.read_csv(ROOT/cfg['inputs'][source+'_predictions']['path']);refs=json.loads((ROOT/cfg['inputs'][source+'_refits']['path']).read_text());refs=[r for r in refs if r['family']=='H1' and r['alpha']==100]
        e=pd.read_csv(ROOT/cfg['inputs']['e_forecasts']['path']);e=e[(e.source==source)&(e.model=='D1')]
        for h in (1,5,20):
            x=p[(p.h==h)&(p.family=='H1')&(p.alpha==100)].copy()
            for b in ('Z0','A0'):
                base=p[(p.h==h)&(p.family==b)][['origin','prediction']].rename(columns={'prediction':b});x=x.merge(base,on='origin',validate='one_to_one')
            d=e[e.h==h][['origin','prediction_new']].rename(columns={'prediction_new':'D1OLS'});x=x.merge(d,on='origin',validate='one_to_one')
            ref=pd.DataFrame([r for r in refs if r['h']==h]);ref['month']=ref.refit_origin.str[:7];x['month']=x.origin.str[:7];x=x.merge(ref[['fold','month','refit_origin']],on=['fold','month'],validate='many_to_one')
            x=x.merge(features,left_on='origin',right_on='date',validate='many_to_one');x=x[x[columns].notna().all(axis=1)]
            for (fold,origin),g in x.groupby(['fold','refit_origin']):
                pos=ix[origin];train=(np.arange(len(q))+h<pos)&q.notna().to_numpy()&q.shift(-h).notna().to_numpy()&complete.to_numpy();y=(q.shift(-h)-q)[train].to_numpy()
                if train.sum()<252:continue
                for model,cols in [('D1r',['d1']),('F4',columns)]:
                    pred,detail=ridge(features.loc[train,cols].to_numpy(),y,g[cols].to_numpy(),100)
                    if not np.isfinite(pred).all():raise ValueError('nonfinite prediction')
                    r=g.copy();r['model']=model;r['prediction_new']=pred;r['source']=source;allrows.append(r);ti=np.flatnonzero(train)
                    audits.append(dict(source=source,h=h,fold=int(fold),model=model,refit_origin=origin,training_n=len(ti),training_first_origin=grid.date.iloc[ti[0]],training_last_label_end=grid.date.iloc[ti[-1]+h],features=cols,**detail))
    if not allrows:raise ValueError('no forecasts')
    result=pd.concat(allrows,ignore_index=True);run=Path(a.run);run.mkdir(parents=True,exist_ok=False);result.to_csv(run/'forecasts.csv',index=False);features.to_csv(run/'external_alignment.csv',index=False);(run/'refits.json').write_text(json.dumps(audits,indent=2)+'\n')
    stats=[]
    for keys,g in result.groupby(['source','h','fold','model']):
        for variant in ('main','strict'):
            z=g if variant=='main' else g[g.strict_interval]
            if z.empty:continue
            for b,col in [('candidate','prediction_new'),('Z0','Z0'),('A0','A0'),('H1','prediction'),('D1OLS','D1OLS')]:
                e=z.actual-z[col];ss=(z.actual**2).sum();stats.append(dict(source=keys[0],h=keys[1],fold=keys[2],model=keys[3],variant=variant,benchmark=b,n=len(z),mae=abs(e).mean(),rmse=np.sqrt((e**2).mean()),r2_oos=1-(e**2).sum()/ss if ss else np.nan))
    pd.DataFrame(stats).to_csv(run/'metrics.csv',index=False)
    f=result[result.model=='F4'];b=result[result.model=='D1r'][['source','h','origin','prediction_new']].rename(columns={'prediction_new':'D1r'});paired=f.merge(b,on=['source','h','origin'],validate='one_to_one');paired.to_csv(run/'paired_forecasts.csv',index=False)
    uncertainty=[]
    for keys,full in paired.groupby(['source','h']):
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
                    uncertainty.append(dict(source=keys[0],h=keys[1],variant=variant,benchmark='H1' if base=='prediction' else base,block=block,n=len(z),draws=2000,seed=20261105,mean_gain=loss.mean(),ci025=np.quantile(means,.025),ci975=np.quantile(means,.975)))
    pd.DataFrame(uncertainty).to_csv(run/'uncertainty.csv',index=False)

    for name,item in {**cfg['inputs'],**cfg['external']}.items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('input changed '+name)
    (run/'provenance.json').write_text(json.dumps({'scope':cfg['scope'],'code_sha256':digest(__file__),'config_sha256':digest(a.config),'inputs':cfg['inputs'],'external':cfg['external']},indent=2)+'\n')
if __name__=='__main__':main()
