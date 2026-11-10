"""Calendar-grid descriptive discount history; see BYU_ORC_AGENTS.md."""
import argparse,hashlib,json,os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def monthly_grid(frame,minimum=10,fraction=.8,last_complete='2026-09'):
    f=frame[frame.observed_session.astype(str).str.lower().eq('true')].copy();f['date']=pd.to_datetime(f.date);f['q']=pd.to_numeric(f.discount_pct,errors='coerce');f['flag']=f.flagged.astype(str).str.lower().eq('true');f['month']=f.date.dt.to_period('M')
    valid=f.q.notna();f['valid_date']=f.date.where(valid);f['within_month_pos']=f.groupby('month').cumcount()+1;f['valid_pos']=f.within_month_pos.where(valid);calc=100*(1-pd.to_numeric(f.preferred_raw_close,errors='coerce')/pd.to_numeric(f.common_raw_close,errors='coerce'))
    if not np.allclose(f.q[valid],calc[valid],atol=1e-9):raise ValueError('discount arithmetic mismatch')
    g=f.groupby('month');m=g.agg(proxy_sessions=('q','size'),valid_q=('q','count'),flagged_sessions=('flag','sum'),mean_q_all_valid=('q','mean'),last_valid_q=('q','last'),first_proxy=('date','min'),last_proxy=('date','max'),last_valid_date=('valid_date','max'),last_valid_pos=('valid_pos','max'))
    m=m.reindex(pd.period_range(f.month.min(),f.month.max(),freq='M'));m.index.name='month'
    for col in ('proxy_sessions','valid_q','flagged_sessions'):m[col]=m[col].fillna(0).astype(int)
    m['valid_fraction']=m.valid_q/m.proxy_sessions.replace(0,np.nan);m['complete_month']=m.index<=pd.Period(last_complete,'M');m['qualified']=(m.proxy_sessions>0)&(m.valid_q>=minimum)&(m.valid_fraction>=fraction)&m.complete_month
    m['last_valid_staleness_proxy_rows']=m.proxy_sessions-m.last_valid_pos;m['mean_q']=m.mean_q_all_valid.where(m.qualified);m['end_q_last_valid']=m.last_valid_q.where(m.qualified)
    return m

def quarterly_grid(m):
    q=m.copy();q['quarter']=q.index.asfreq('Q');g=q.groupby('quarter');out=g.agg(qualified_months=('qualified','sum'),observed_months=('proxy_sessions',lambda x:(x>0).sum()),quarter_mean=('mean_q','mean'))
    out['quarter_mean']=out.quarter_mean.where(out.qualified_months.eq(3));ends=q[q.index.month.isin([3,6,9,12])].set_index('quarter').end_q_last_valid
    out['quarter_end_last_valid_q']=ends.reindex(out.index).where(out.qualified_months.eq(3));last_month=q[q.index.month.isin([3,6,9,12])].set_index('quarter');out['quarter_end_last_valid_date']=last_month.last_valid_date.reindex(out.index).where(out.qualified_months.eq(3));out['quarter_end_staleness_proxy_rows']=last_month.last_valid_staleness_proxy_rows.reindex(out.index).where(out.qualified_months.eq(3));return out

def changes(m,horizons):
    rows=[];anchor=next((i for i,v in enumerate(m.qualified) if v),None)
    for h in horizons:
        for i in range(h,len(m)):
            a=m.iloc[i-h];b=m.iloc[i];window=m.iloc[i-h:i+1];ok=bool(a.qualified and b.qualified)
            rows.append(dict(h_months=h,start_month=str(m.index[i-h]),end_month=str(m.index[i]),start_q=float(a.mean_q) if a.qualified else np.nan,end_q=float(b.mean_q) if b.qualified else np.nan,change_pp=float(b.mean_q-a.mean_q) if ok else np.nan,window_months=h+1,qualified_window_months=int(window.qualified.sum()),missing_or_unqualified_window_months=int((~window.qualified).sum()),mean_qualified_monthly_q_inclusive=float(window.mean_q.mean()) if window.qualified.any() else np.nan,strict_complete=bool(window.qualified.all()),nonoverlap_anchor=bool(anchor is not None and i-h>=anchor and (i-h-anchor)%h==0)))
    return pd.DataFrame(rows)

def state_runs(m):
    labels=['below_10','10_to_20','20_to_30','at_least_30'];state=pd.cut(m.mean_q,[-np.inf,10,20,30,np.inf],right=False,labels=labels)
    runs=[];start=None;previous=None
    for month,value in state.items():
        s=None if pd.isna(value) else str(value)
        if s!=previous:
            if previous is not None:runs.append(dict(state=previous,start_month=str(start),end_month=str(month-1),months=int(month.ordinal-start.ordinal)))
            start=month if s is not None else None;previous=s
    if previous is not None:runs.append(dict(state=previous,start_month=str(start),end_month=str(state.index[-1]),months=int(state.index[-1].ordinal-start.ordinal+1)))
    return pd.DataFrame(runs,columns=['state','start_month','end_month','months'])

def main():
    a=argparse.ArgumentParser();a.add_argument('--config',required=True);a.add_argument('--run',required=True);args=a.parse_args();cfg=json.loads(Path(args.config).read_text())
    for name,item in cfg['inputs'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('hash mismatch '+name)
    f=pd.read_csv(ROOT/cfg['inputs']['grid']['path']);m=monthly_grid(f,cfg['minimum_valid_sessions'],cfg['minimum_valid_fraction'],cfg['last_complete_month']);q=quarterly_grid(m);c=changes(m,cfg['horizons_months']);runs=state_runs(m)
    annual=m.assign(year=m.index.year).groupby('year').agg(qualified_months=('qualified','sum'),mean_monthly_q=('mean_q','mean'),minimum_monthly_q=('mean_q','min'),maximum_monthly_q=('mean_q','max'),flagged_sessions=('flagged_sessions','sum'));annual.loc[annual.qualified_months<12,['mean_monthly_q','minimum_monthly_q','maximum_monthly_q']]=np.nan
    run=Path(args.run);run.mkdir(parents=True,exist_ok=False);m.to_csv(run/'monthly.csv');q.to_csv(run/'quarterly.csv');c.to_csv(run/'long_changes.csv',index=False);runs.to_csv(run/'state_runs.csv',index=False);annual.to_csv(run/'annual.csv')
    comparison=[]
    for h,g in c.groupby('h_months'):
        for label,mask in [('endpoint',g.change_pp.notna()),('strict_complete',g.change_pp.notna()&g.strict_complete),('anchored_nonoverlap',g.change_pp.notna()&g.nonoverlap_anchor),('anchored_nonoverlap_strict',g.change_pp.notna()&g.nonoverlap_anchor&g.strict_complete)]:
            z=g[mask];comparison.append(dict(h_months=int(h),sample=label,n=len(z),mean_change_pp=z.change_pp.mean(),median_change_pp=z.change_pp.median(),minimum_change_pp=z.change_pp.min(),maximum_change_pp=z.change_pp.max()))
    pd.DataFrame(comparison).to_csv(run/'change_summary.csv',index=False)
    fig,ax=plt.subplots(figsize=(12,5));ax.plot(m.index.to_timestamp(),m.mean_q,label='Qualified monthly mean q');ax.plot(q.index.to_timestamp(how='end'),q.quarter_mean,label='Complete-quarter mean',alpha=.65);ax.set(xlabel='Date',ylabel='Discount (percentage points)',title='Samsung common/preferred discount — proxy-session sample');ax.legend();fig.tight_layout();fig.savefig(run/'discount_history.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(12,5))
    for h,g in c.groupby('h_months'):ax.plot(pd.to_datetime(g.end_month),g.change_pp,label=f'{h//12} years')
    ax.axhline(0,color='black',lw=.6);ax.set(xlabel='Ending month',ylabel='Change in monthly mean discount (pp)',title='Overlapping calendar-horizon changes');ax.legend();fig.tight_layout();fig.savefig(run/'long_changes.png',dpi=160);plt.close(fig)
    for name,item in cfg['inputs'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('input changed '+name)
    (run/'provenance.json').write_text(json.dumps({'inputs':cfg['inputs'],'code_sha256':digest(__file__),'config_sha256':digest(args.config),'grid':cfg['grid'],'rule':cfg['quarter_rule'],'last_complete_month':cfg['last_complete_month'],'notes':cfg['notes']},indent=2)+'\n')
if __name__=='__main__':main()
