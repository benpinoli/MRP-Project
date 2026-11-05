"""Two bounded historical forecast adaptations; BYU_ORC_AGENTS.md applies."""
import argparse, hashlib, json, os
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def train_indices(q, feature, refit_pos, h, span=None):
    indices=np.arange(len(q)); lower=max(0,refit_pos-span) if span else 0
    y=q.shift(-h)-q
    return (indices>=lower)&(indices+h<refit_pos)&q.notna().to_numpy()&y.notna().to_numpy()&feature.notna().to_numpy()

def fit(q, feature, refit_pos, h, span=None, minimum=252):
    train=train_indices(q,feature,refit_pos,h,span); y=q.shift(-h)-q
    if train.sum()<minimum: return None
    design=np.column_stack([np.ones(train.sum()),feature[train].to_numpy()]); beta=np.linalg.lstsq(design,y[train].to_numpy(),rcond=None)[0]
    return beta,train

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);a=ap.parse_args()
    cfg=json.loads(Path(a.config).read_text()); inp=cfg['inputs']
    for name,(path,sha) in inp.items():
        if digest(ROOT/path)!=sha: raise ValueError('input mismatch '+name)
    grid=pd.read_csv(ROOT/inp['grid'][0]);grid=grid[grid.observed_session.astype(str).str.lower().eq('true')].reset_index(drop=True);q=pd.to_numeric(grid.discount_pct); features={'D1':q.diff(),'R756':q}
    indices={v:i for i,v in enumerate(grid.date)}; forecasts=[]; audits=[]
    for source in ('validation','final'):
        p=pd.read_csv(ROOT/inp[source+'_predictions'][0]); refs=json.loads((ROOT/inp[source+'_refits'][0]).read_text()); refs=[r for r in refs if r['family']=='H1' and r['alpha']==100]
        for h in cfg['horizons']:
            x=p[(p.h==h)&(p.family=='H1')&(p.alpha==100)].copy()
            for baseline in ('Z0','A0'):
                base=p[(p.h==h)&(p.family==baseline)][['origin','prediction']].rename(columns={'prediction':baseline});x=x.merge(base,on='origin',validate='one_to_one')
            ref=pd.DataFrame([r for r in refs if r['h']==h]);ref['month']=ref.refit_origin.str[:7]
            x['month']=x.origin.str[:7];x=x.merge(ref[['fold','month','refit_origin']],on=['fold','month'],validate='many_to_one')
            for (fold,origin),group in x.groupby(['fold','refit_origin']):
                pos=indices[origin]
                for model,feature in features.items():
                    span=cfg['window_proxy_origins'] if model=='R756' else None
                    fitted=fit(q,feature,pos,h,span,cfg['minimum_training'])
                    if fitted is None: continue
                    beta,train=fitted;group=group.copy(); group['model']=model;group['prediction_new']=beta[0]+beta[1]*feature.iloc[[indices[v] for v in group.origin]].to_numpy();group['source']=source
                    if not np.isfinite(group.prediction_new).all(): raise ValueError('nonfinite forecast')
                    forecasts.append(group);ix=np.flatnonzero(train)
                    audits.append(dict(source=source,h=h,fold=fold,model=model,refit_origin=origin,training_n=len(ix),training_first_origin=grid.date.iloc[ix[0]],training_last_origin=grid.date.iloc[ix[-1]],training_last_label_end=grid.date.iloc[ix[-1]+h],window_start=grid.date.iloc[max(0,pos-span)] if span else grid.date.iloc[0],intercept=beta[0],coefficient=beta[1]))
    if not forecasts: raise ValueError('no forecasts')
    result=pd.concat(forecasts,ignore_index=True); rows=[]
    uncertainty=[]
    for keys,full in result.groupby(['source','h','fold','model']):
        for variant in ('main','strict'):
            g=full if variant=='main' else full[full.strict_interval]
            if g.empty: continue
            zero_sse=(g.actual**2).sum()
            for name,field in [('candidate','prediction_new'),('Z0','Z0'),('A0','A0'),('H1','prediction')]:
                e=g.actual-g[field];rows.append(dict(source=keys[0],h=keys[1],fold=keys[2],model=keys[3],variant=variant,benchmark=name,n=len(g),mae=abs(e).mean(),rmse=np.sqrt((e**2).mean()),bias=e.mean(),r2_oos=1-(e**2).sum()/zero_sse if zero_sse else np.nan))
    # Paired fixed-forecast losses, contiguous proxy-grid blocks, no resampling of model fits.
    for keys,full in result.groupby(['source','h','model']):
        dates=grid.loc[(grid.date>=full.origin.min())&(grid.date<=full.origin.max()),'date'].reset_index(drop=True)
        for variant in ('main','strict'):
            g=full if variant=='main' else full[full.strict_interval]
            for bench in ('Z0','A0','prediction'):
                loss=abs(g.actual-g[bench])-abs(g.actual-g.prediction_new)
                values=dates.map(pd.Series(loss.to_numpy(),index=g.origin)).to_numpy()
                for block in sorted(set([max(20,2*keys[1]),60])):
                    rng=np.random.default_rng(20261105); means=[]
                    for _ in range(2000):
                        start=rng.integers(0,len(values)-block+1,size=int(np.ceil(len(values)/block)))
                        sample=values[(start[:,None]+np.arange(block)).ravel()[:len(values)]]
                        if not np.isfinite(sample).any(): raise ValueError('empty bootstrap draw')
                        means.append(np.nanmean(sample))
                    uncertainty.append(dict(source=keys[0],h=keys[1],model=keys[2],variant=variant,benchmark='H1' if bench=='prediction' else bench,block=block,draws=2000,seed=20261105,n=len(g),mean_gain=loss.mean(),ci025=np.quantile(means,.025),ci975=np.quantile(means,.975)))
    stability=[]
    for keys,g in result[result.source=='final'].groupby(['h','model',result.origin.str[:4]]):
        for variant in ('main','strict'):
            z=g if variant=='main' else g[g.strict_interval]
            if z.empty: continue
            for name,field in [('candidate','prediction_new'),('Z0','Z0'),('A0','A0'),('H1','prediction')]:
                e=z.actual-z[field]; stability.append(dict(h=keys[0],model=keys[1],year=keys[2],variant=variant,benchmark=name,n=len(z),mae=abs(e).mean(),rmse=np.sqrt((e**2).mean())))
    run=Path(a.run);run.mkdir(parents=True,exist_ok=False);result.to_csv(run/'forecasts.csv',index=False);pd.DataFrame(audits).to_csv(run/'refits.csv',index=False);pd.DataFrame(rows).to_csv(run/'metrics.csv',index=False);pd.DataFrame(uncertainty).to_csv(run/'uncertainty.csv',index=False);pd.DataFrame(stability).to_csv(run/'stability.csv',index=False)
    for name,(path,sha) in inp.items():
        if digest(ROOT/path)!=sha: raise ValueError('input changed '+name)
    (run/'provenance.json').write_text(json.dumps({'scope':cfg['scope'],'code_sha256':digest(__file__),'config_sha256':digest(a.config),'inputs':inp},indent=2)+'\n')
if __name__=='__main__': main()
