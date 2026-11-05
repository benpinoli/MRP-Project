"""Sparse, descriptive issuer disclosures; BYU_ORC_AGENTS.md governs execution."""
import argparse,hashlib,json,os
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(os.environ['SAMSUNG_REPO'])

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def cash_discount_delta(common,preferred,common_cash,preferred_cash):
    if not (common>common_cash>=0 and preferred>preferred_cash>=0):raise ValueError('invalid synthetic prices/cash')
    return 100*(common*preferred_cash-preferred*common_cash)/(common*(common-common_cash))

def event_windows(grid,event,horizons=(1,5,20)):
    date=event['publication_date'];n=len(grid);dates=grid.date.to_numpy();pos=int(np.searchsorted(dates,date,side='right'));exact=int(np.searchsorted(dates,date,side='left'))
    bases=[('publication_date',exact if exact<n and dates[exact]==date else None),('next_proxy_session',pos if pos<n else None)]
    records=[]
    for kind,i in bases:
        for h in horizons:
            row={'event_id':event['id'],'cluster':event['cluster'],'kind':event['kind'],'publication_date':date,'base_rule':kind,'h':h,'base_date':None,'target_date':None,'base_q':None,'target_q':None,'change_pp':None,'strict_interval':False,'status':'base_missing'}
            if i is not None:
                row['base_date']=dates[i]
                if i+h>=n:row['status']='target_out_of_range'
                else:
                    row['target_date']=dates[i+h];a=grid.discount_pct.iloc[i];b=grid.discount_pct.iloc[i+h]
                    if not np.isfinite(a) or not np.isfinite(b):row['status']='invalid_endpoint'
                    else:
                        row.update(base_q=float(a),target_q=float(b),change_pp=float(b-a),status='ok')
                        interval=grid.iloc[i:i+h+1];row['strict_interval']=bool(interval.discount_pct.notna().all() and not interval.flagged.any())
            records.append(row)
    return records

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);ap.add_argument('--run',required=True);a=ap.parse_args();cfg=json.loads(Path(a.config).read_text())
    for item in cfg['inputs'].values():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('input hash mismatch')
    manifest=json.loads((ROOT/cfg['inputs']['events']['path']).read_text());sources=ROOT/cfg['source_directory']
    for name,sha in manifest['sources'].items():
        if digest(sources/(name+'.html'))!=sha:raise ValueError('source hash mismatch '+name)
    grid=pd.read_csv(ROOT/cfg['inputs']['grid']['path']);grid=grid[grid.observed_session.astype(str).str.lower().eq('true')].reset_index(drop=True);grid['discount_pct']=pd.to_numeric(grid.discount_pct,errors='coerce');grid['flagged']=grid.flagged.astype(str).str.lower().eq('true')
    windows=[];dose=[]
    for e in manifest['events']:
        if e.get('denominator_publication_date') and e['denominator_publication_date']>e['publication_date']:raise ValueError('future denominator')
        windows.extend(event_windows(grid,e,cfg['horizons']))
        if e['common_quantity'] is not None:
            c=100*e['common_quantity']/e['common_issued'];p=100*e['preferred_quantity']/e['preferred_issued']
            dose.append({'event_id':e['id'],'kind':e['kind'],'cluster':e['cluster'],'publication_date':e['publication_date'],'common_pct_issued':c,'preferred_pct_issued':p,'preferred_minus_common_pp':p-c,'quantity_status':e['quantity_status'],'denominator_status':e['denominator_status'],'denominator_publication_date':e['denominator_publication_date']})
    # Illustrative mechanics only; not an inferred actual ex-date reaction.
    common,preferred,dc,dp=10000.,8000.,363.,364.;synthetic={'common_before':common,'preferred_before':preferred,'common_cash':dc,'preferred_cash':dp,'discount_change_pp':cash_discount_delta(common,preferred,dc,dp),'note':'synthetic example only, no market date or ex-date inferred'}
    run=Path(a.run);run.mkdir(parents=True,exist_ok=False);pd.DataFrame(windows).to_csv(run/'event_windows.csv',index=False);pd.DataFrame(dose).to_csv(run/'dose_arithmetic.csv',index=False);(run/'cash_identity.json').write_text(json.dumps(synthetic,indent=2)+'\n')
    for item in cfg['inputs'].values():
        if digest(ROOT/item['path'])!=item['sha256']:raise ValueError('input changed')
    for name,sha in manifest['sources'].items():
        if digest(sources/(name+'.html'))!=sha:raise ValueError('source changed '+name)
    (run/'provenance.json').write_text(json.dumps({'scope':manifest['scope'],'timing':manifest['timing'],'source_hashes':manifest['sources'],'input_hashes':cfg['inputs'],'code_sha256':digest(__file__),'config_sha256':digest(a.config),'event_count':len(manifest['events'])},indent=2)+'\n')
if __name__=='__main__':main()
