"""Exploratory diagnostics on frozen forecasts. See BYU_ORC_AGENTS.md."""
import argparse, hashlib, json, os
from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def corr(a,b):
    x=pd.DataFrame({'a':a,'b':b}).dropna()
    return x.a.corr(x.b) if len(x)>2 and x.a.std()>0 and x.b.std()>0 else np.nan

def training_thresholds(grid, dates, origins, h, window):
    q=grid.q; d1=q.diff(); local=q-q.rolling(window,min_periods=window).mean()
    z=pd.DataFrame({'abs_d1':abs(d1),'abs_local':abs(local),'abs_y':abs(q.shift(-h)-q)})
    records=[]
    for origin in sorted(set(origins)):
        pos=dates.searchsorted(origin); train=z.iloc[:max(0,pos-h)]
        if len(train)<252: raise ValueError('insufficient matured history')
        r={'refit_origin':origin,'h':h,'training_max_label_end':dates.iloc[pos-1]}
        for col in z:
            for pct in (.5,.9,.99): r[f'{col}_p{int(pct*100)}']=train[col].quantile(pct)
        records.append(r)
    return pd.DataFrame(records)

def summary(g):
    e=g.actual-g.prediction; ez=g.actual-g.z0; ea=g.actual-g.a0
    return {'n':len(g),'actual_mean':g.actual.mean(),'prediction_mean':g.prediction.mean(),'bias_actual_minus_pred':e.mean(), 'corr_error_d1':corr(e,g.d1),'corr_error_local':corr(e,g.local),'corr_error_q':corr(e,g.q), 'positive_actual_fraction':(g.actual>0).mean(),'model_mae':abs(e).mean(),'z0_mae':abs(ez).mean(),'a0_mae':abs(ea).mean(),'model_rmse':np.sqrt((e**2).mean()),'z0_rmse':np.sqrt((ez**2).mean()),'a0_rmse':np.sqrt((ea**2).mean()),'model_abs_error_sum':abs(e).sum(),'z0_abs_error_sum':abs(ez).sum(),'a0_abs_error_sum':abs(ea).sum()}

def classify(v,lo,hi):
    return np.where(v.isna()|lo.isna()|hi.isna(),'missing',np.where(v<=lo,'low',np.where(v<=hi,'middle','high')))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--config',required=True); ap.add_argument('--run',required=True); a=ap.parse_args()
    cfg=json.loads(Path(a.config).read_text()); inp=cfg['inputs']
    for name,(path,sha) in inp.items():
        if digest(ROOT/path)!=sha: raise ValueError('input mismatch '+name)
    run=Path(a.run); run.mkdir(parents=True,exist_ok=False)
    grid=pd.read_csv(ROOT/inp['grid'][0]); grid=grid[grid.observed_session.astype(str).str.lower().eq('true')].reset_index(drop=True)
    dates=pd.to_datetime(grid.date); grid['q']=pd.to_numeric(grid.discount_pct); grid['d1']=grid.q.diff(); grid['local']=grid.q-grid.q.rolling(cfg['local_window'],min_periods=cfg['local_window']).mean()
    datasets=[]; threshold_tables=[]; coeff=[]
    for source in ('validation','final'):
        p=pd.read_csv(ROOT/inp[source+'_predictions'][0]); refs=json.loads((ROOT/inp[source+'_refits'][0]).read_text())
        refs=[r for r in refs if r['family']==cfg['model'] and r['alpha']==cfg['alpha']]
        for r in refs:
            for feature,beta,mean,scale in zip(r['features'],r['coefficients'],r['mean'],r['scale']):
                coeff.append({'source':source,'h':r['h'],'fold':r['fold'],'refit_origin':r['refit_origin'],'train_n':r['train_n'],'train_label_end':r['train_label_end'],'feature':feature,'standardized_coefficient':beta,'raw_scale_coefficient':beta/scale if scale else np.nan,'train_mean':mean,'train_scale':scale})
        for h in cfg['horizons']:
            x=p[(p.h==h)&(p.family==cfg['model'])&(p.alpha==cfg['alpha'])].copy()
            for family in ('Z0','A0'):
                base=p[(p.h==h)&(p.family==family)][['origin','prediction']].rename(columns={'prediction':family.lower()})
                x=x.merge(base,on='origin',validate='one_to_one')
            x=x.merge(grid[['date','d1','local']],left_on='origin',right_on='date',validate='many_to_one')
            r=pd.DataFrame([v for v in refs if v['h']==h]); r['month']=r.refit_origin.str[:7]
            if r.duplicated(['fold','month']).any(): raise ValueError('duplicate refit')
            x['month']=x.origin.str[:7]; x=x.merge(r[['fold','month','refit_origin']],on=['fold','month'],validate='many_to_one')
            t=training_thresholds(grid,dates,pd.to_datetime(r.refit_origin),h,cfg['local_window']); t['refit_origin']=pd.to_datetime(t.refit_origin).dt.strftime('%Y-%m-%d'); t['training_max_label_end']=pd.to_datetime(t.training_max_label_end).dt.strftime('%Y-%m-%d'); t['source']=source
            x=x.merge(t.drop(columns=['h','source']),on='refit_origin',validate='many_to_one'); x['source']=source
            x['period']=np.where(source=='validation','fold'+x.fold.astype(str),x.origin.str[:4])
            x['d1_bin']=classify(abs(x.d1),x.abs_d1_p50,x.abs_d1_p90); x['local_bin']=classify(abs(x.local),x.abs_local_p50,x.abs_local_p90)
            x['realized_extreme_vs_training']=np.where(abs(x.actual)>x.abs_y_p99,'above_training_p99','other')
            x['direction']=np.where(x.actual>0,'widen',np.where(x.actual<0,'narrow','unchanged'))
            datasets.append(x); threshold_tables.append(t)
    allx=pd.concat(datasets,ignore_index=True); results=[]
    for keys,g in allx.groupby(['source','h','period'],sort=True):
        source,h,period=keys
        for dimension in ('overall','d1_bin','local_bin','realized_extreme_vs_training','direction','realized_top1pct'):
            if dimension=='overall': groups=[('all',g)]
            elif dimension=='realized_top1pct':
                # Exact top ceiling 1% by realized |change| in this viewed segment; diagnostic, not a forecast feature.
                ranked=g.assign(rank=abs(g.actual).rank(method='first',ascending=False)); k=max(1,int(np.ceil(.01*len(g)))); groups=[('top1pct',ranked[ranked['rank']<=k]),('rest',ranked[ranked['rank']>k])]
            else: groups=list(g.groupby(dimension,dropna=False))
            for level,sub in groups:
                if len(sub): results.append(dict(source=source,h=h,period=period,dimension=dimension,level=level,**summary(sub)))
    allx.to_csv(run/'paired_diagnostics.csv',index=False); pd.DataFrame(results).to_csv(run/'diagnostic_summary.csv',index=False); pd.concat(threshold_tables).to_csv(run/'training_thresholds.csv',index=False); pd.DataFrame(coeff).to_csv(run/'coefficient_paths.csv',index=False)
    for name,(path,sha) in inp.items():
        if digest(ROOT/path)!=sha: raise ValueError('input changed: '+name)
    (run/'provenance.json').write_text(json.dumps({'scope':cfg['scope'],'input_hashes':{k:v[1] for k,v in inp.items()},'code_sha256':digest(__file__),'config_sha256':digest(a.config),'rows':len(allx),'grid_rows':len(grid),'first_date':grid.date.min(),'last_date':grid.date.max()},indent=2)+'\n')
if __name__=='__main__': main()
