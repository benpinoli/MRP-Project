"""Fixed terminal-anchor and retrospective payout tests. Follow BYU_ORC_AGENTS.md; run in Slurm."""
import argparse,csv,datetime,hashlib,json,os,subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
ROOT=Path(__file__).resolve().parents[1]
def digest(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v),allow_nan=False)+'\n')
def ridge(x,y,penalty):
    mu=x.mean(0);sd=x.std(0);assert np.all(sd>0)
    z=(x-mu)/sd;s=np.linalg.solve(z.T@z+len(y)*penalty*np.eye(x.shape[1]),z.T@(y-y.mean()))/sd
    return np.r_[y.mean()-mu@s,s]
def metric(f):
    y=f.actual_change_pp.to_numpy();loss=float(np.mean((y-f.prediction_change_pp.to_numpy())**2));r={'forecast_n':len(f),'mse_pp2':loss,'rmse_pp':float(np.sqrt(loss))}
    for label,col in [('persistence','zero'),('mean_change','mean_change'),('terminal_anchor','terminal_anchor')]:
        b=float(np.mean((y-f[col].to_numpy())**2));r[label+'_mse_pp2']=b;r['r2_vs_'+label]=1-loss/b if b>0 else None
    return r

def terminal(cfg,out,protected):
    baseline=ROOT/cfg['baseline_run'];ref=ROOT/cfg['reference_run']
    audit=json.loads((baseline/'verification/AUDIT.json').read_text())['original_output_sha256']
    assert digest(baseline/'monthly.csv')==audit['monthly.csv'];protected[str(baseline/'monthly.csv')]=audit['monthly.csv']
    monthly=pd.read_csv(baseline/'monthly.csv');lookup=dict(tuple(monthly.groupby(['sample','variant'])))
    prov=json.loads((baseline/'provenance.json').read_text());models={m['id']:m['columns'] for m in prov['config']['models']}
    hashes=json.loads((ref/'output_manifest.json').read_text());allrows=[];coef=[];maxdiff=0.;maxmean=0.;files=0
    for path in sorted(ref.glob('*_forecasts.csv')):
        old=pd.read_csv(path)
        if not len(old) or old.model.iloc[0] not in cfg['models'] or int(old.horizon_months.iloc[0]) not in cfg['horizons_months']:continue
        assert digest(path)==hashes[path.name];protected[str(path)]=hashes[path.name];files+=1
        sample,variant,model=old.loc[0,['sample','variant','model']];h=int(old.horizon_months.iloc[0]);panel=lookup[sample,variant].reset_index(drop=True)
        dates=pd.PeriodIndex(panel.month,freq='M');assert dates.equals(pd.period_range(dates.min(),dates.max(),freq='M'))
        q=panel.discount_pp.to_numpy(float);g=panel.grid.to_numpy(int);assert np.array_equal(g,np.arange(len(q)))
        target=panel.discount_pp.shift(-h).to_numpy(float);y=target-q;cols=models[model];x=panel[cols].to_numpy(float)
        valid=np.isfinite(x).all(1)&np.isfinite(y);groupbase={'sample':sample,'variant':variant,'model':model,'horizon_months':h}
        for (origin,window),group in old.groupby(['origin_grid','window']):
            origin=int(origin);mask=valid&(g<origin)&(g+h<=origin)
            if window=='rolling120':mask&=g>=origin-cfg['rolling_training_origin_months']
            else:assert window=='expanding'
            n=int(mask.sum());assert n>=max(cfg['minimum_training_observations'],cfg['observations_per_parameter']*(len(cols)+1))
            assert all(group.training_n==n) and all(g[mask]+h<=origin)
            tx=x[mask];ty=y[mask];X=np.c_[np.ones(n),tx];ols=np.linalg.lstsq(X,ty,rcond=None)[0];rb=ridge(tx,ty,cfg['ridge_penalty'])
            mean_change=float(ty.mean());anchor=float(target[mask].mean()-q[origin]);actual=float(y[origin])
            for method,beta in [('OLS',ols),('RIDGE',rb)]:
                saved=group[group.method==method];assert len(saved)==1;saved=saved.iloc[0]
                pred=float(np.r_[1.,x[origin]]@beta);error=abs(pred-float(saved.prediction_change_pp));maxdiff=max(maxdiff,error);maxmean=max(maxmean,abs(mean_change-float(saved.training_mean_prediction)))
                assert error<1e-7 and np.isclose(mean_change,saved.training_mean_prediction,rtol=0,atol=1e-9) and np.isclose(actual,saved.actual_change_pp,rtol=0,atol=1e-9)
                base={**groupbase,'method':method,'window':window,'origin_grid':origin,'origin_month':str(dates[origin]),'target_month':str(dates[origin]+h),'training_n':n,'latest_training_label_end_grid':int(g[mask].max())+h}
                allrows.append({**base,'actual_change_pp':actual,'prediction_change_pp':pred,'origin_discount_pp':float(q[origin]),'predicted_terminal_q':float(q[origin]+pred),'zero':0.,'mean_change':mean_change,'terminal_anchor':anchor})
                for term,b in zip(['intercept']+cols,beta):coef.append({**base,'term':term,'coefficient':float(b)})
        save(out/'progress.json',{'status':'terminal_refits','completed_source_files':files})
    f=pd.DataFrame(allrows);assert len(f)>0;f.to_csv(out/'terminal_forecasts.csv',index=False);pd.DataFrame(coef).to_csv(out/'terminal_coefficients.csv',index=False)
    grouping=['sample','variant','model','horizon_months','window','method'];scores=[];phases=[];periods=[]
    for keys,frame in f.groupby(grouping):
        base=dict(zip(grouping,keys));scores.append({**base,**metric(frame)})
        for phase,sub in frame.groupby(frame.origin_grid%int(base['horizon_months'])):phases.append({**base,'phase':int(phase),**metric(sub)})
        years=pd.PeriodIndex(frame.origin_month,freq='M').year
        for label,lo,hi in cfg['calendar_periods']:
            sub=frame[(years>=lo)&(years<=hi)]
            if len(sub):periods.append({**base,'period':label,**metric(sub)})
    for name,rows in [('terminal_scores',scores),('terminal_nonoverlap_phases',phases),('terminal_calendar_periods',periods)]:pd.DataFrame(rows).to_csv(out/(name+'.csv'),index=False)
    nested=[];join=['sample','variant','horizon_months','window','method','origin_grid']
    for small,big in [('LH-LEVEL','LH-STATE'),('LH-STATE','LH-ACTIVITY')]:
        joined=f[f.model==small].merge(f[f.model==big],on=join,suffixes=('_small','_big'),validate='one_to_one')
        for keys,sub in joined.groupby(join[:-1]):
            a=np.mean((sub.actual_change_pp_small-sub.prediction_change_pp_small)**2);b=np.mean((sub.actual_change_pp_big-sub.prediction_change_pp_big)**2)
            nested.append({**dict(zip(join[:-1],keys)),'smaller':small,'larger':big,'matched_origins':len(sub),'incremental_r2':float(1-b/a) if a else None})
    pd.DataFrame(nested).to_csv(out/'matched_feature_increments.csv',index=False)
    failed=ref/'failed_origins.csv';assert digest(failed)==hashes[failed.name];protected[str(failed)]=hashes[failed.name]
    (out/'inherited_failed_origins.csv').write_bytes(failed.read_bytes())
    return {'source_groups':files,'refitted_forecast_cases':len(f),'score_rows':len(scores),'max_saved_prediction_abs_error':maxdiff,'max_saved_mean_change_abs_error':maxmean,'terminal_support_breaches':int((f.predicted_terminal_q>=100).sum()),'inherited_failed_rolling_origins':len(pd.read_csv(failed)),'samples':int(f['sample'].nunique())}

def ols_stats(frame,columns):
    X=np.c_[np.ones(len(frame)),frame[columns].to_numpy(float)];y=frame.dq.to_numpy(float);n,k=X.shape
    assert n>k and np.linalg.matrix_rank(X)==k
    b=np.linalg.lstsq(X,y,rcond=None)[0];res=y-X@b;bread=np.linalg.inv(X.T@X);score=X*res[:,None]
    # Independent QR estimates and alternative HC1 diagonal construction.
    Q,R=np.linalg.qr(X,mode='reduced');assert np.allclose(b,np.linalg.solve(R,Q.T@y),rtol=1e-8,atol=1e-8)
    meat=score.T@score;hc1=bread@meat@bread*n/(n-k)
    check=bread@X.T@np.diag(res**2)@X@bread*n/(n-k);assert np.allclose(hc1,check,rtol=1e-8,atol=1e-9)
    hacmeat=meat.copy();years=frame.year.to_numpy(int)
    for j in range(1,n):
        if years[j]-years[j-1]==1:hacmeat+=.5*(np.outer(score[j],score[j-1])+np.outer(score[j-1],score[j]))
    covs={'HC1':hc1,'HAC1':bread@hacmeat@bread*n/(n-k)};rows=[];tcrit=stats.t.ppf(.975,n-k)
    fit_r2=1-float(res@res)/float((y-y.mean())@(y-y.mean()))
    for covlabel,cov in covs.items():
        se=np.sqrt(np.maximum(np.diag(cov),0))
        for term,value,sd in zip(['intercept']+columns,b,se):
            p=float(2*stats.t.sf(abs(value/sd),n-k)) if sd>0 else None
            rows.append({'term':term,'coefficient':float(value),'standard_error':float(sd),'CI95_low':float(value-tcrit*sd),'CI95_high':float(value+tcrit*sd),'p_nominal':p,'covariance':covlabel,'n':n,'df_residual':n-k,'fit_r2':fit_r2,'supply_effect_per_0_01_ratio_change':float(value*.01) if term=='dsupply' else None})
    return rows,b

def annual(cfg,out,protected):
    p=ROOT/cfg['annual_source_panel'];protected[str(p)]=digest(p);a=pd.read_csv(p);assert len(a)==15 and a.year.tolist()==list(range(2010,2025))
    a['dq']=a.mean_monthly_q.diff();a['dsupply']=a.preferred_to_common_nontreasury.diff();a['cash_growth']=np.log(a.total_cash_KRW_million/a.total_cash_KRW_million.shift(1));a['DPS_growth']=np.log(a.common_DPS_postsplit/a.common_DPS_postsplit.shift(1))
    f=a.dropna(subset=['dq','dsupply','cash_growth','DPS_growth']).copy();assert len(f)>=cfg['annual_minimum_changes']
    f.to_csv(out/'annual_analysis_panel.csv',index=False);designs={'supply_only':['dsupply'],'payout_only':['cash_growth'],'joint_aggregate':['cash_growth','dsupply'],'joint_DPS':['DPS_growth','dsupply']};rows=[];loo=[]
    for name,cols in designs.items():
        estimates,_=ols_stats(f,cols);rows.extend({'model':name,'sample':'full','first_year':int(f.year.min()),'last_year':int(f.year.max()),**r} for r in estimates)
    sub=f[~f.year.isin(cfg['annual_special_sensitivity_excluded_outcome_years'])];estimates,_=ols_stats(sub,designs['joint_aggregate']);rows.extend({'model':'joint_aggregate','sample':'exclude_2020_2021','first_year':int(sub.year.min()),'last_year':int(sub.year.max()),**r} for r in estimates)
    for year in f.year:
        sub=f[f.year!=year];_,b=ols_stats(sub,designs['joint_aggregate']);loo.append({'omitted_year':int(year),'n':len(sub),'intercept':float(b[0]),'cash_growth_coefficient':float(b[1]),'dsupply_coefficient':float(b[2])})
    primary=[r for r in rows if r['sample']=='full' and r['covariance']=='HC1' and ((r['model']=='joint_aggregate' and r['term']=='cash_growth') or (r['model']=='joint_DPS' and r['term']=='DPS_growth'))];assert len(primary)==2
    order=sorted(primary,key=lambda r:r['p_nominal']);qvals=np.minimum.accumulate(np.array([min(1,r['p_nominal']*2/(i+1)) for i,r in enumerate(order)])[::-1])[::-1]
    qmap={(r['model'],r['term']):float(q) for r,q in zip(order,qvals)}
    for r in rows:r['BH_q_primary_two_test_family']=qmap.get((r['model'],r['term'])) if r['sample']=='full' and r['covariance']=='HC1' else None
    pd.DataFrame(rows).to_csv(out/'annual_regression_coefficients.csv',index=False);pd.DataFrame(loo).to_csv(out/'annual_leave_one_year_out.csv',index=False)
    gap=a.cash_extra_postsplit.to_numpy();assert np.isfinite(gap).all()
    return {'annual_levels':len(a),'annual_changes':len(f),'year_range':[int(f.year.min()),int(f.year.max())],'special_sensitivity_n':int((~f.year.isin(cfg['annual_special_sensitivity_excluded_outcome_years'])).sum()),'preferred_cash_gap_min':float(gap.min()),'preferred_cash_gap_max':float(gap.max()),'class_cash_difference_regression_status':'not_identified_constant_regressor' if np.ptp(gap)==0 else 'not_in_fixed_design','coefficient_rows':len(rows),'covariance_checks':'QR estimates and independent HC1 sandwich passed; HAC1 uses only adjacent calendar years and t intervals','forecast_status':'retrospective annual association only; first-publication dates unknown'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--config',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();cfg=json.loads(args.config.read_text());out=args.output.resolve();assert out.is_relative_to(ROOT/'runs');out.mkdir(parents=True,mode=0o700,exist_ok=False)
    protected={};save(out/'progress.json',{'status':'started'});(out/'frozen_config.json').write_bytes(args.config.read_bytes());(out/'executed_source.py').write_bytes(Path(__file__).read_bytes())
    ta=terminal(cfg,out,protected);save(out/'progress.json',{'status':'annual_started','terminal':ta});aa=annual(cfg,out,protected)
    for path,expected in protected.items():assert digest(Path(path))==expected
    save(out/'provenance.json',{'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'config_sha256':digest(args.config),'code_sha256':digest(Path(__file__)),'protected_sources':protected,'job_id':os.environ.get('SLURM_JOB_ID'),'git_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'numpy':np.__version__,'pandas':pd.__version__,'no_new_intervals_or_features':True})
    summary={'status':'completed','terminal_anchor':ta,'annual_payout':aa,'protected_sources_unchanged':True,'prospectively_validated':False,'canonical_verdicts_changed':False};save(out/'summary.json',summary);save(out/'output_manifest.json',{p.name:digest(p) for p in out.iterdir() if p.is_file() and p.name not in ['output_manifest.json','progress.json']});save(out/'progress.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
