"""Reviewed annual cash source panel, retrospective only. See BYU_ORC_AGENTS.md."""
from pathlib import Path
import csv,datetime,hashlib,json,re
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/acquisition/2026-11-12/productive_tree_regressions_v1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((ROOT/'data/regression/raw/long_horizon_issuer_20261105/download_manifest.json').read_text())
sources={r['reporting_year']:r for r in manifest['sources'] if r.get('status')=='downloaded'}
# Fiscal year, source report year/page, reviewed aggregate KRW million, native common/preferred DPS.
values=[(2010,2011,11,1496540,10000,10050),(2011,2011,11,827196,5500,5550),(2012,2012,12,1206562,8000,8050),(2013,2014,19,2156969,14300,14350),(2014,2014,19,2999972,20000,20050),(2015,2015,21,3068737,21000,21050),(2016,2016,21,3991892,28500,28550),(2017,2017,28,5826302,42500,42550),(2018,2018,25,9619243,1416,1417),(2019,2019,24,9619243,1416,1417),(2020,2020,24,20338075,2994,2995),(2021,2021,224,9809438,1444,1445),(2022,2022,223,9809438,1444,1445),(2023,2023,209,9809438,1444,1445),(2024,2024,241,9810767,1446,1447)]
old=list(csv.DictReader((ROOT/'runs/samsung/long_horizon_b_15069061/annual_supply_activity.csv').open(newline='')))
annual={int(r['year']):r for r in old}
extracts={};refs=[];rows=[]
for year,vintage,page,total,common,pref in values:
    key=(vintage,page);source=sources[vintage];p=ROOT/source['local_path']
    if key not in extracts:
        assert digest(p)==source['sha256']
        text=PdfReader(str(p)).pages[page-1].extract_text(extraction_mode='layout')
        out=OUT/'source_pages'/f'issuer_{vintage}_PDFpage{page}.txt';assert not out.exists();out.write_text(text)
        extracts[key]=text;refs.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':source['sha256'],'url':source['url'],'PDF_page':page,'extracted_path':str(out.relative_to(OUT)),'extracted_sha256':digest(out),'retrieved_utc':source['retrieved_utc'],'first_publication_utc':'unknown','review':'independent page-specific layout text extraction, manually reviewed; not raster visual verification'})
    normalized=re.sub(r'(?<=,)\s+(?=\d)','',extracts[key])
    assert all(f'{v:,}' in normalized for v in [total,common,pref]),year
    a=annual[year];assert a['complete_year']=='True' and int(a['qualified_months'])==12
    divisor=50 if year<2018 else 1
    rows.append({'year':year,'total_cash_KRW_million':total,'common_DPS_native':common,'preferred_DPS_native':pref,'DPS_divisor':divisor,'common_DPS_postsplit':common/divisor,'preferred_DPS_postsplit':pref/divisor,'cash_extra_postsplit':(pref-common)/divisor,'mean_monthly_q':a['mean_monthly_q'],'preferred_to_common_nontreasury':a['preferred_to_common_nontreasury'],'source_report_year':vintage,'PDF_page':page,'source_path':str(p.relative_to(ROOT)),'source_sha256':source['sha256'],'first_publication_utc':'unknown; retrospective only','qualification':'Fiscal dividend allocation, including special payouts; own-report final payment may await AGM. Source2011 comparative used for2010; source2014 for2013. No calendar-year payment or FCF compliance claim.'})
assert len(rows)==15 and all(r['preferred_to_common_nontreasury'] for r in rows)
target=OUT/'prepared/samsung_annual_delivery_panel.csv';assert not target.exists()
with target.open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(OUT/'source_inventory.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_pages':refs,'source_annual_q_and_supply':{'path':'runs/samsung/long_horizon_b_15069061/annual_supply_activity.csv','sha256':digest(ROOT/'runs/samsung/long_horizon_b_15069061/annual_supply_activity.csv')},'fiscal_years':15,'unknown_publication':'All annual facts are retrospective, not forecasting inputs'},indent=2)+'\n')
print('Prepared15fiscal years from',len(refs),'verified source pages; no outcomes fitted')
