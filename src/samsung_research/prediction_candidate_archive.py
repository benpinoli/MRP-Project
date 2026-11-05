"""Archive predeclared D1 fits for prospective evaluation; BYU_ORC_AGENTS.md applies."""
import argparse,hashlib,json,os
from pathlib import Path
import numpy as np
import pandas as pd
from samsung_research.regressions import fit_ols
ROOT=Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def eligible(q,origin,h):
    y=q.shift(-h)-q;d1=q.diff();idx=np.arange(len(q));mask=(idx+h<origin)&q.notna().to_numpy()&y.notna().to_numpy()&d1.notna().to_numpy()
    return y,d1,mask

def main():
    a=argparse.ArgumentParser();a.add_argument('--config',required=True);a.add_argument('--run',required=True);args=a.parse_args();cfg=json.loads(Path(args.config).read_text())
    for k,v in cfg['inputs'].items():
        if digest(ROOT/v['path'])!=v['sha256']:raise ValueError('input mismatch '+k)
    f=pd.read_csv(ROOT/cfg['inputs']['grid']['path']);f=f[(f.observed_session.astype(str).str.lower()=='true')&(f.date<=cfg['cutoff'])].reset_index(drop=True)
    if f.date.iloc[-1]!=cfg['cutoff']:raise ValueError('cutoff not on proxy grid')
    q=pd.to_numeric(f.discount_pct);origin=len(f)-1;fits=[]
    for h in cfg['horizons']:
        y,d1,mask=eligible(q,origin,h);ii=np.flatnonzero(mask);x=np.column_stack([np.ones(len(ii)),d1[mask].to_numpy()]);b,se,p,res,diag=fit_ols(y[mask].to_numpy(),x,ii,bandwidth=20)
        fits.append({'h':h,'features':['intercept','d1'],'coefficients':b.tolist(),'hac20_se':se.tolist(),'hac20_95pct_normal_interval':np.column_stack([b-1.96*se,b+1.96*se]).tolist(),'p_values':p.tolist(),'diagnostics':diag,'training_first_origin':f.date.iloc[ii[0]],'training_last_origin':f.date.iloc[ii[-1]],'training_last_label_end':f.date.iloc[ii[-1]+h],'cutoff':cfg['cutoff'],'cutoff_q':float(q.iloc[-1]),'cutoff_d1':float(d1.iloc[-1])})
    run=Path(args.run);run.mkdir(parents=True,exist_ok=False);(run/'candidate.json').write_text(json.dumps({'scope':cfg['scope'],'prospective_start':cfg['prospective_start'],'protocol':cfg['protocol'],'fits':fits},indent=2,allow_nan=False)+'\n')
    for k,v in cfg['inputs'].items():
        if digest(ROOT/v['path'])!=v['sha256']:raise ValueError('input changed '+k)
    (run/'provenance.json').write_text(json.dumps({'code_sha256':digest(__file__),'config_sha256':digest(args.config),'inputs':cfg['inputs']},indent=2)+'\n')
if __name__=='__main__':main()
