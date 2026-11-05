"""Samsung forecast research; BYU_ORC_AGENTS.md governs compute and data use."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, shutil
from pathlib import Path
import numpy as np
import pandas as pd
from samsung_research.regressions import dated_csv, digest, outcomes

ROOT = Path(os.environ.get('SAMSUNG_REPO', Path(__file__).resolve().parents[2])).resolve()

def load(config):
    ep = ROOT / config['ep01']
    manifest = json.loads((ep/'manifest.json').read_text())
    expected = {x['path']: x['sha256'] for x in manifest['outputs']}
    for name in ('tables/measures_main.csv', 'tables/measures_sensitivity.csv', 'provenance/source_inventory.json'):
        if digest(ep/name) != expected[name]: raise ValueError('EP01 hash mismatch: '+name)
    if digest(ROOT/config['raw']) != config['raw_sha256'] or any(manifest[k] != config['raw_sha256'] for k in ('input_sha256_before','input_sha256_after')):
        raise ValueError('raw hash mismatch')
    f = dated_csv(ep/'tables/measures_main.csv')
    sensitivity = dated_csv(ep/'tables/measures_sensitivity.csv')
    if not f.date.equals(sensitivity.date): raise ValueError('variant grid mismatch')
    f = f.loc[f.observed_session.astype(str).str.lower().eq('true')].reset_index(drop=True)
    outcomes(f)  # independently verify discount arithmetic
    return f

def features(f):
    q = pd.to_numeric(f.discount_pct, errors='raise')
    result = pd.DataFrame({'q':q})
    for h in (1,5,20):
        complete = q.notna().rolling(h+1, min_periods=h+1).sum().eq(h+1)
        result[f'd{h}'] = (q - q.shift(h)).where(complete)
    result['vol20'] = q.diff().rolling(20, min_periods=20).std(ddof=1)
    v = pd.to_numeric(f.volume_ratio, errors='raise')
    result['activity'] = np.log(v.where(v > 0))
    return result

def fit_predict(x, y, xpred, alpha, audit=False):
    if alpha is None:
        design = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(design, y, rcond=None)[0]
        pred = np.column_stack([np.ones(len(xpred)), xpred]) @ beta
        return (pred, {'intercept':float(beta[0]), 'coefficients':beta[1:].tolist(), 'mean':None, 'scale':None}) if audit else pred
    mean = x.mean(axis=0); scale = x.std(axis=0, ddof=0)
    scale = np.where(scale > 0, scale, 1.0)
    z = (x-mean)/scale; zp = (xpred-mean)/scale
    ym = y.mean()
    beta = np.linalg.solve(z.T@z + alpha*np.eye(z.shape[1]), z.T@(y-ym))
    pred = ym + zp@beta
    return (pred, {'intercept':float(ym), 'coefficients':beta.tolist(), 'mean':mean.tolist(), 'scale':scale.tolist()}) if audit else pred

def generate(f, config, mode, locked=None):
    x = features(f); q = x.q; dates = pd.to_datetime(f.date)
    if mode == 'validation':
        masks = [(dates >= a)&(dates <= b) for a,b in config['validation_folds']]
    else: masks = [dates >= config['test_start']]
    allrows = []; audits = []
    for h in config['horizons']:
        end = dates.shift(-h); y = q.shift(-h)-q
        strict = (q.notna() & ~f.flagged.astype(bool)).rolling(h+1, min_periods=h+1).sum().shift(-h).eq(h+1)
        for fold, mask in enumerate(masks, 1):
            for family, cols in config['families'].items():
                if mode == 'test' and family not in {'Z0','A0',locked[str(h)]['family']}: continue
                alphas = config['alphas'] if family in ('H1','V1') else [None]
                if mode == 'test' and family in ('H1','V1'):
                    alphas = [locked[str(h)]['alpha']] if family == locked[str(h)]['family'] else []
                validx = x[cols].notna().all(axis=1) if cols else pd.Series(True,index=x.index)
                eligible = mask & q.notna() & y.notna() & validx
                if mode == 'validation': eligible &= end <= pd.Timestamp(config['validation_folds'][fold-1][1])
                for month in dates[eligible].dt.to_period('M').unique():
                    idx = np.flatnonzero(eligible & dates.dt.to_period('M').eq(month))
                    origin = dates.iloc[idx[0]]
                    train = (end < origin) & y.notna() & validx
                    if family != 'Z0' and train.sum() < max(config['minimum_training'], 20*(len(cols)+1)): continue
                    for alpha in alphas:
                        if family == 'Z0': pred = np.zeros(len(idx))
                        else:
                            pred, details = fit_predict(x.loc[train,cols].to_numpy(), y[train].to_numpy(), x.iloc[idx][cols].to_numpy(), alpha, audit=True)
                            audits.append(dict(h=h, fold=fold, family=family, alpha=alpha, refit_origin=origin.strftime('%Y-%m-%d'), train_n=int(train.sum()), train_label_end=end[train].max().strftime('%Y-%m-%d'), features=cols, **details))
                        for j,p in zip(idx,pred):
                            allrows.append({'h':h,'fold':fold,'family':family,'alpha':alpha,'origin':f.date.iloc[j], 'target_date':end.iloc[j].strftime('%Y-%m-%d'), 'actual':y.iloc[j], 'prediction':p,'q':q.iloc[j], 'implied_level':q.iloc[j]+p, 'actual_level':q.iloc[j]+y.iloc[j], 'strict_interval':bool(strict.iloc[j]),'flagged':bool(f.flagged.iloc[j]),'train_n':int(train.sum()) if family != 'Z0' else 0,'train_label_end':end[train].max().strftime('%Y-%m-%d') if family != 'Z0' else ''})
    return pd.DataFrame(allrows), audits

def metrics(p):
    rows=[]
    for (h,fold,family,alpha), g in p.groupby(['h','fold','family','alpha'], dropna=False):
        z=p[(p.h==h)&(p.fold==fold)&(p.family=='Z0')][['origin','actual']]
        m=g.merge(z,on='origin',suffixes=('','_z'),validate='one_to_one')
        err=m.actual-m.prediction; sse=(m.actual**2).sum()
        a0=p[(p.h==h)&(p.fold==fold)&(p.family=='A0')][['origin','prediction']].rename(columns={'prediction':'a0_prediction'})
        matched=m.merge(a0,on='origin',validate='one_to_one')
        rows.append(dict(h=h,fold=fold,family=family,alpha=alpha,n=len(m),mae=abs(err).mean(),rmse=np.sqrt((err**2).mean()),zero_mae=abs(m.actual).mean(),zero_rmse=np.sqrt(sse/len(m)),r2_oos=1-(err**2).sum()/sse if sse else np.nan,a0_matched_n=len(matched),matched_model_mae=abs(matched.actual-matched.prediction).mean(),matched_a0_mae=abs(matched.actual-matched.a0_prediction).mean(),matched_model_rmse=np.sqrt(((matched.actual-matched.prediction)**2).mean()),matched_a0_rmse=np.sqrt(((matched.actual-matched.a0_prediction)**2).mean()),matched_r2_vs_a0=1-((matched.actual-matched.prediction)**2).sum()/((matched.actual-matched.a0_prediction)**2).sum() if ((matched.actual-matched.a0_prediction)**2).sum() else np.nan))
    return pd.DataFrame(rows)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--config',default='configs/prediction/samsung_v1.json'); ap.add_argument('--run',required=True); ap.add_argument('--mode',choices=['validation','test'],required=True); ap.add_argument('--lock'); a=ap.parse_args()
    config=json.loads(Path(a.config).read_text()); run=Path(a.run); run.mkdir(parents=True,exist_ok=False)
    shutil.copy2(a.config,run/'config.json'); shutil.copy2(__file__,run/'prediction.py')
    locked=json.loads(Path(a.lock).read_text()) if a.mode=='test' and a.lock else None
    if a.mode=='test' and not locked: raise ValueError('test requires lock')
    if locked and (locked.get('code_sha256') != digest(__file__) or locked.get('config_sha256') != digest(a.config)): raise ValueError('lock code/config mismatch')
    if locked: locked = locked['selection']
    if pd.Timestamp(config['initial_train_end']) >= pd.Timestamp(config['validation_folds'][0][0]): raise ValueError('initial training end overlaps validation')
    if pd.Timestamp(config['initial_train_end']) != pd.Timestamp(config['validation_folds'][0][0])-pd.Timedelta(days=1): raise ValueError('initial boundary must abut first fold')
    f=load(config); p,audits=generate(f,config,a.mode,locked); (run/'refits.json').write_text(json.dumps(audits,indent=2)+'\n'); p.to_csv(run/'predictions.csv',index=False); metrics(p).to_csv(run/'metrics.csv',index=False); metrics(p[p.strict_interval]).to_csv(run/'metrics_strict.csv',index=False)
    load(config)  # recheck immutable input hashes after fitting
    (run/'provenance.json').write_text(json.dumps({'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'code_sha256':digest(__file__),'config_sha256':digest(a.config),'rows':len(f),'date_min':f.date.min(),'date_max':f.date.max(),'missing_discount_dates':f.loc[f.discount_pct.isna(),'date'].tolist(),'invalid_volume_dates':f.loc[~(pd.to_numeric(f.volume_ratio,errors='coerce')>0),'date'].tolist()},indent=2)+'\n')
if __name__=='__main__': main()
