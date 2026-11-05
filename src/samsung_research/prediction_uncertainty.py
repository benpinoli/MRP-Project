"""Fixed test summaries and paired block bootstrap on the preserved proxy grid."""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from samsung_research.regressions import dated_csv

def bootstrap(pair, grid, block, draws=2000, seed=20261105):
    loss=abs(pair.actual-pair.benchmark)-abs(pair.actual-pair.prediction)
    full=grid.map(pd.Series(loss.to_numpy(),index=pair.origin)).to_numpy(); n=len(full)
    if n < block: raise ValueError('grid shorter than block')
    rng=np.random.default_rng(seed); means=[]
    for _ in range(draws):
        starts=rng.integers(0,n-block+1,size=int(np.ceil(n/block)))
        sample=full[(starts[:,None]+np.arange(block)).ravel()[:n]]
        if np.isfinite(sample).any(): means.append(np.nanmean(sample))
    if len(means)!=draws: raise ValueError('empty bootstrap draw')
    return {'finite_pairs':len(pair),'mean_mae_improvement_pp':loss.mean(),'ci025':np.quantile(means,.025),'ci975':np.quantile(means,.975)}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--run',required=True); ap.add_argument('--lock',required=True); ap.add_argument('--ep01',required=True); a=ap.parse_args()
    lock=json.loads(Path(a.lock).read_text())['selection']; p=pd.read_csv(Path(a.run)/'predictions.csv'); f=dated_csv(Path(a.ep01)/'tables/measures_main.csv')
    f=f[f.observed_session.astype(str).str.lower().eq('true')]; grid=f.loc[(f.date >= p.origin.min()) & (f.date <= p.origin.max()),'date'].reset_index(drop=True)
    uncertainty=[]; stability=[]
    for h in sorted(p.h.unique()):
        c=lock[str(h)]; sub=p[(p.h==h)&(p.family==c['family'])]
        if c.get('alpha') is not None: sub=sub[np.isclose(sub.alpha,c['alpha'])]
        for benchmark in ('Z0','A0'):
            base=p[(p.h==h)&(p.family==benchmark)][['origin','prediction']].rename(columns={'prediction':'benchmark'})
            pair=sub.merge(base,on='origin',validate='one_to_one')
            for variant in ('main','strict'):
                sample = pair if variant=='main' else pair[pair.strict_interval]
                for block in sorted(set([max(20,2*h),60])):
                    uncertainty.append(dict(h=h,family=c['family'],alpha=c.get('alpha'),benchmark=benchmark,variant=variant,block=block,draws=2000,seed=20261105,**bootstrap(sample,grid,block)))
            for year in (2024,2025,2026):
                for variant in ('main','strict'):
                    z=pair[pair.origin.str.startswith(str(year))]; z=z if variant=='main' else z[z.strict_interval]
                    e=z.actual-z.prediction; b=z.actual-z.benchmark
                    stability.append(dict(h=h,family=c['family'],benchmark=benchmark,year=year,variant=variant,n=len(z),model_mae=abs(e).mean(),benchmark_mae=abs(b).mean(),model_rmse=np.sqrt((e**2).mean()),benchmark_rmse=np.sqrt((b**2).mean())))
    pd.DataFrame(uncertainty).to_csv(Path(a.run)/'uncertainty.csv',index=False)
    pd.DataFrame(stability).to_csv(Path(a.run)/'stability.csv',index=False)
if __name__=='__main__': main()
