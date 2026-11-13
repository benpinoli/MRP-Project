"""Independent saved-output arithmetic and covariance review. See BYU_ORC_AGENTS.md."""
import argparse,hashlib,json,datetime
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
ROOT=Path(__file__).resolve().parents[1]
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('--run',type=Path,required=True);args=parser.parse_args();out=args.run.resolve();assert out.is_relative_to(ROOT/'runs')
prov=json.loads((out/'provenance.json').read_text());manifest=json.loads((out/'output_manifest.json').read_text())
for name,sha in manifest.items():assert digest(out/name)==sha,name
for name,sha in prov['protected_sources'].items():assert digest(Path(name))==sha,name
assert digest(out/'executed_source.py')==prov['code_sha256']
cfg=json.loads((out/'frozen_config.json').read_text());monthly=pd.read_csv(ROOT/cfg['baseline_run']/'monthly.csv');lookup=dict(tuple(monthly.groupby(['sample','variant'])))
f=pd.read_csv(out/'terminal_forecasts.csv');maxanchor=0.;reconstructed=0
modelmap={m['id']:m['columns'] for m in json.loads((ROOT/cfg['baseline_run']/'provenance.json').read_text())['config']['models']}
for keys,rows in f.groupby(['sample','variant','model','horizon_months']):
    sample,variant,model,h=keys;panel=lookup[sample,variant].reset_index(drop=True);q=panel.discount_pp.to_numpy();g=np.arange(len(q));target=panel.discount_pp.shift(-int(h)).to_numpy();valid=panel[modelmap[model]].notna().all(axis=1).to_numpy()&np.isfinite(target-q)
    for (origin,window),sub in rows.groupby(['origin_grid','window']):
        origin=int(origin);mask=valid&(g<origin)&(g+h<=origin)
        if window=='rolling120':mask&=g>=origin-120
        # Independent anchor identity using saved historical-change mean + mean origin state.
        expected=float(sub.mean_change.iloc[0]+q[mask].mean()-q[origin]);error=float(np.max(abs(sub.terminal_anchor-expected)));maxanchor=max(maxanchor,error);assert error<1e-9
        assert int(mask.sum())==int(sub.training_n.iloc[0]);assert all(sub.latest_training_label_end_grid<=origin);reconstructed+=len(sub)
group=['sample','variant','model','horizon_months','window','method'];scores=pd.read_csv(out/'terminal_scores.csv');scorelookup={tuple(r[k] for k in group):r for _,r in scores.iterrows()}
for keys,sub in f.groupby(group):
    expected=scorelookup[keys];actual=sub.actual_change_pp.to_numpy();loss=float(np.average((actual-sub.prediction_change_pp)**2));anchorloss=float(np.average((actual-sub.terminal_anchor)**2))
    assert np.isclose(loss,expected.mse_pp2,rtol=1e-10,atol=1e-12)
    assert np.isclose(1-loss/anchorloss,expected.r2_vs_terminal_anchor,rtol=1e-9,atol=1e-10)

# Independent annual QR fit, direct pairwise calendar-kernel covariance, t inference.
a=pd.read_csv(out/'annual_analysis_panel.csv');coefs=pd.read_csv(out/'annual_regression_coefficients.csv');maxse=0.
design={'supply_only':['dsupply'],'payout_only':['cash_growth'],'joint_aggregate':['cash_growth','dsupply'],'joint_DPS':['DPS_growth','dsupply']}
for (model,sample),reported in coefs.groupby(['model','sample']):
    p=a if sample=='full' else a[~a.year.isin([2020,2021])];x=np.column_stack([np.ones(len(p)),p[design[model]].values]);y=p.dq.values;n,k=x.shape;Q,R=np.linalg.qr(x);b=np.linalg.solve(R,Q.T@y);u=y-x@b;bread=np.linalg.solve(x.T@x,np.eye(k))
    for cov in ['HC1','HAC1']:
        meat=np.zeros((k,k))
        for i in range(n):
            for j in range(n):
                distance=abs(int(p.year.iloc[i])-int(p.year.iloc[j]));weight=float(i==j) if cov=='HC1' else (1 if distance==0 else (.5 if distance==1 else 0))
                meat+=weight*u[i]*u[j]*np.outer(x[i],x[j])
        ses=np.sqrt(np.diag((n/(n-k))*bread@meat@bread))
        for index,term in enumerate(['intercept']+design[model]):
            r=reported[(reported.covariance==cov)&(reported.term==term)].iloc[0];assert np.isclose(b[index],r.coefficient,rtol=1e-8,atol=1e-8)
            error=abs(ses[index]-r.standard_error);maxse=max(maxse,error);assert np.isclose(ses[index],r.standard_error,rtol=1e-8,atol=1e-8)
            assert np.isclose(2*t.sf(abs(b[index]/ses[index]),n-k),r.p_nominal,rtol=1e-8,atol=1e-10)
            assert np.isclose(b[index]-t.ppf(.975,n-k)*ses[index],r.CI95_low,rtol=1e-8,atol=1e-8)
source=json.loads((ROOT/'data/acquisition/2026-11-12/productive_tree_regressions_v1/source_inventory.json').read_text())
for r in source['source_pages']:assert digest(ROOT/r['path'])==r['sha256']
report={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'passed','terminal_cases_independently_checked':reconstructed,'max_terminal_anchor_identity_error':maxanchor,'aggregate_score_rows_checked':len(scores),'annual_coefficient_rows_checked':len(coefs),'max_independent_covariance_SE_error':maxse,'saved_source_code_and_input_hashes_unchanged':True,'annual_original_report_hashes_rechecked':len(source['source_pages']),'provenance_scope_clarification':'no_new_intervals_or_features in original provenance refers to monthly forecasting designs; annual retrospective payout covariates are new and explicitly authorized by the protocol','no_new_data_or_model_choices_from_verification':True}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
