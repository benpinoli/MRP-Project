"""Annual share supply and activity description; see BYU_ORC_AGENTS.md."""
import argparse,hashlib,json,os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from samsung_research.e01 import load_and_validate
ROOT=Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def annual_volume(normalized,grid_dates,split_date='2018-05-04',factor=50):
    dates=pd.Series(pd.to_datetime(grid_dates));year=dates.dt.year;data=[]
    index={name:{r['datadate']:r for r in normalized if r['class_name']==name} for name in ('preferred','common')}
    for y in sorted(year.unique()):
        days=dates[year==y].dt.strftime('%Y-%m-%d').tolist();row={'year':int(y),'proxy_sessions':len(days)}
        for name in ('preferred','common'):
            valid=0;positive=0;missing=0;ineligible=0;total=0.0
            for d in days:
                r=index[name].get(d)
                if r is None or not r['price_eligible']:ineligible+=1;continue
                try:v=float(r['cshtrd'])
                except (TypeError,ValueError):missing+=1;continue
                if not np.isfinite(v) or v<0:missing+=1;continue
                valid+=1;positive+=v>0;total+=v*(factor if d<split_date else 1)
            row.update({name+'_valid_volume_rows':valid,name+'_positive_volume_rows':positive,name+'_missing_invalid_volume_rows':missing,name+'_ineligible_price_rows':ineligible,name+'_volume_coverage':valid/len(days),name+'_observed_volume_incomplete':valid<len(days),name+'_annual_volume_postsplit_shares':total})
        data.append(row)
    return pd.DataFrame(data)

def normalize_counts(issuer,factor=50):
    rows=[]
    for r in issuer['rows']:
        year=int(r['period_end'][:4]);z={'year':year,'source_url':r['source_url'],'source_page':r['source_page'],'count_status':r['status'],'conflict_flags':'; '.join(r['conflict_flags']),'publication_status':r['publication_status'],'share_basis':r['share_basis']}
        for cls in ('common','preferred'):
            for typ in ('issued','treasury','non_treasury'):
                value=r[typ+'_'+cls];z[typ+'_'+cls+'_postsplit']=value*(factor if year<2018 else 1) if value is not None else np.nan
            if r['issued_'+cls] is not None and r['treasury_'+cls] is not None and r['non_treasury_'+cls] is not None and r['issued_'+cls]-r['treasury_'+cls]!=r['non_treasury_'+cls]:raise ValueError('issuer count mismatch '+str(year)+' '+cls)
        rows.append(z)
    if len({r['year'] for r in rows})!=len(rows):raise ValueError('duplicate issuer year')
    return pd.DataFrame(rows)

def combine(vol,counts,annual_q,coverage=.8,last_complete=2025):
    years=pd.DataFrame({'year':range(int(vol.year.min()),int(vol.year.max())+1)});z=years.merge(vol,on='year',how='left',validate='one_to_one').merge(counts,on='year',how='left',validate='one_to_one').merge(annual_q,on='year',how='left',validate='one_to_one')
    z['complete_year']=z.year<=last_complete
    for cls in ('common','preferred'):
        z[cls+'_activity_per_yearend_nontreasury']=(z[cls+'_annual_volume_postsplit_shares']/z['non_treasury_'+cls+'_postsplit']).where(z.complete_year&(z[cls+'_volume_coverage']>=coverage)&(z['non_treasury_'+cls+'_postsplit']>0))
    z['preferred_to_common_nontreasury']=z.non_treasury_preferred_postsplit/z.non_treasury_common_postsplit
    z['preferred_to_common_activity']=z.preferred_activity_per_yearend_nontreasury/z.common_activity_per_yearend_nontreasury
    z['joint_eligible']=z.complete_year&(z.qualified_months==12)&z.preferred_to_common_activity.notna()&z.preferred_to_common_nontreasury.notna()
    for col in ('mean_monthly_q','preferred_to_common_nontreasury','preferred_to_common_activity'):
        z['change_'+col]=z[col]-z[col].shift(1)
    return z

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);a=ap.parse_args();cfg=json.loads(Path(a.config).read_text())
    for name,item in cfg['inputs'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('input mismatch '+name)
    pair=json.loads((ROOT/cfg['inputs']['pair']['path']).read_text());_,_,_,norm=load_and_validate(ROOT/cfg['inputs']['raw']['path'],pair);grid=pd.read_csv(ROOT/cfg['inputs']['grid']['path']);grid=grid[grid.observed_session.astype(str).str.lower().eq('true')]
    vol=annual_volume(norm,grid.date,cfg['split_first_trading_date'],cfg['split_factor']);issuer=json.loads((ROOT/cfg['inputs']['issuer']['path']).read_text());counts=normalize_counts(issuer,cfg['split_factor']);annual=pd.read_csv(ROOT/cfg['inputs']['annual_q']['path']);z=combine(vol,counts,annual,cfg['minimum_proxy_volume_coverage'],cfg['last_complete_year'])
    run=Path(a.run);run.mkdir(parents=True,exist_ok=False);z.to_csv(run/'annual_supply_activity.csv',index=False)
    eras=[('pre_policy',2005,2014),('2015_policy',2015,2016),('2017_policy',2017,2017),('stable_counts_2018_2023',2018,2023),('recent',2024,2025)];out=[]
    for label,start,end in eras:
        g=z[(z.year>=start)&(z.year<=end)&z.joint_eligible];out.append(dict(era=label,start=start,end=end,joint_years=len(g),mean_discount_pp=g.mean_monthly_q.mean(),mean_preferred_to_common_nontreasury=g.preferred_to_common_nontreasury.mean(),mean_preferred_to_common_activity=g.preferred_to_common_activity.mean()))
    pd.DataFrame(out).to_csv(run/'era_summary.csv',index=False)
    fig,axes=plt.subplots(2,1,figsize=(12,8),sharex=True);axes[0].plot(z.year,z.mean_monthly_q,label='Annual mean discount (pp)',color='black');axes[0].set_ylabel('Discount (pp)');ax=axes[0].twinx();ax.plot(z.year,z.preferred_to_common_nontreasury,label='P/C non-treasury count',color='tab:blue');ax.set_ylabel('P/C non-treasury count');axes[1].plot(z.year,z.preferred_to_common_activity,color='tab:orange');axes[1].set(xlabel='Year',ylabel='P/C activity per year-end non-treasury share');fig.suptitle('Annual supply and activity proxies — gaps retained');fig.tight_layout();fig.savefig(run/'annual_supply_activity.png',dpi=160);plt.close(fig)
    for name,item in cfg['inputs'].items():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('input changed '+name)
    (run/'provenance.json').write_text(json.dumps({'scope':cfg['scope'],'inputs':cfg['inputs'],'code_sha256':digest(__file__),'config_sha256':digest(a.config),'split_normalization':'pre-2018-05-04 shares x50; earlier year-end share counts x50','calendar':'observed-session proxy; 2026 partial retained, excluded from annual activity','volume_coverage_note':'Nonnegative volumes on eligible price rows only; incomplete coverage is an observed-volume lower bound, not extrapolated; year-end non-treasury denominator is not average float.'},indent=2)+'\n')
if __name__=='__main__':main()
