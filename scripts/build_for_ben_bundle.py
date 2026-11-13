"""Build Ben's aggregate research reading pack; no licensed rows. See BYU_ORC_AGENTS.md."""
from pathlib import Path
import csv,datetime,hashlib,json,os,re,shutil
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'FOR_BEN';DOC=ROOT/'docs/regressions'
def read(p):
    source=ROOT/p
    if not source.is_file():
        mapping=json.loads((OUT/'TABLE_INPUTS/SOURCES.json').read_text())
        source=OUT/next(r['bundle_file'] for r in mapping if r['original_path']==p)
    return list(csv.DictReader(source.open(newline='')))
def write_csv(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def metric(x):return '' if x in ('',None) else f'{float(x):+.6f}'
def escape(x):return str(x).replace('|','/').replace('\n',' ')

def situation(sample):
    if sample.startswith('hyundai'):return 'Common/preferred shares — Korea','Hyundai '+sample.rsplit('_',1)[-1]
    if sample=='volkswagen_ordinary_preferred':return 'Common/preferred shares — Germany','Volkswagen ordinary/preferred local'
    if sample.startswith('roche_'):return 'Voting/nonvoting participation rights — Switzerland','Roche voting/Genussschein' if 'Genuss' in sample else 'Roche voting/participation'
    if sample=='byd_A_H':return 'Segmented A/H shares — Mainland/Hong Kong','BYD A/H'
    if sample=='ping_an_A_H':return 'Segmented A/H shares — Mainland/Hong Kong','Ping An A/H'
    if sample=='novo_nordisk_local_ADS':return 'Ordinary share versus US depositary receipt','Novo Copenhagen B / NYSE ADS'
    if sample=='hdfc_local_ADS':return 'Ordinary share versus US depositary receipt','HDFC local / NYSE ADS'
    if sample.startswith('shell_RDS_'):return 'Historical Shell class versus US receipt','Historical Shell '+sample[-1]
    if 'alibaba' in sample:return 'Ordinary share versus US depositary receipt','Alibaba'
    if 'shell' in sample:return 'Unified successor listing','Unified Shell'
    return 'Other scoped comparison',sample
VARIABLES={'LH-LEVEL':'current discount q','LH-STATE':'current q; trailing 12-month change in q','LH-ACTIVITY':'current q; trailing 12-month change in q; relative volume/activity proxy','PPML-MEAN':'log(current positive price ratio); intercept; exponential conditional mean'}

def main():
    if OUT.exists():assert (OUT/'SOURCE_SNAPSHOTS.json').is_file(), 'Refuse to overwrite an unrelated folder'
    else:OUT.mkdir()
    core={'LOOP_HYPOTHESIS_TESTS_PAPER_20261112.md':'PAPER.md','LOOP_SIMPLE_TIMELINE_20261112.md':'TIMELINE.md','PREDICTION_MECHANISM_TREE.md':'HYPOTHESIS_TREE.md','PREDICTION_MECHANISM_TREE.json':'HYPOTHESIS_TREE.json'}
    snapshots=[]
    for name,dest in core.items():
        src=DOC/name
        if src.suffix=='.json':shutil.copyfile(src,OUT/dest)
        else:
            def link(m):
                target=m.group(1)
                if re.match(r'^[a-z]+://',target) or target.startswith(('#','mailto:')):return m.group(0)
                path,mark,anchor=target.partition('#');resolved=(src.parent/path).resolve()
                new=core.get(resolved.name) if resolved.parent==DOC.resolve() else None
                if not new:new=os.path.relpath(resolved,OUT)
                return ']('+new+(mark+anchor if mark else '')+')'
            (OUT/dest).write_text(re.sub(r'\]\(([^)]+)\)',link,src.read_text()))
        snapshots.append({'file':dest,'source':str(src.relative_to(ROOT)),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'note':'Snapshot; Markdown links rebased for repository-root folder. JSON unchanged.'})

    failures=[]
    def add(category,comparison,model,variables,horizon,window,coverage,n,source,fail,notes='',r0='',rm='',rt='',status='forecast benchmark loss'):
        failures.append({'situation_type':category,'comparison':comparison,'model':model,'variables':variables,'horizon':horizon,'training':window,'coverage':coverage,'forecast_n':n,'failure_or_limit':fail,'r2_vs_persistence':r0,'r2_vs_mean_change':rm,'r2_vs_terminal_anchor':rt,'status':status,'qualification':notes,'source':source})
    src='docs/regressions/LOOP_TREE_PRODUCTIVE_BATCH_SCORES_20261112.csv'
    allcurrent=read(src)
    for r in allcurrent:
        failed=[label for label,key in [('persistence','r2_vs_persistence'),('mean change','r2_vs_mean_change'),('matching terminal anchor','r2_vs_terminal_anchor')] if float(r[key])<0]
        if not failed:continue
        cat,name=situation(r['sample'])
        add(cat,name,r['model']+' / '+r['method'],VARIABLES[r['model']],r['horizon_months']+' months',r['window'],r['variant'],r['forecast_n'],src,'Loses to '+', '.join(failed),'Historical matched-origin scores; dependent horizons/variants. A loss to one benchmark does not erase wins against others.',r['r2_vs_persistence'],r['r2_vs_mean_change'],r['r2_vs_terminal_anchor'])
    src='docs/regressions/LOOP_LH5_MEAN_SCORECARD_20261112.csv'
    for r in read(src):
        if r['method']!='PPML-MEAN':continue
        failed=[label for label,key in [('persistence','r2_vs_persistence'),('mean change','r2_vs_mean_change'),('terminal anchor','r2_vs_terminal_mean')] if float(r[key])<0]
        if not failed:continue
        cat,name=situation(r['sample']);add(cat,name,'PPML-MEAN',VARIABLES['PPML-MEAN'],r['horizon_months']+' months','expanding',r['variant'],r['forecast_n'],src,'Loses to '+', '.join(failed),'Positive support repaired; that alone does not improve forecasts. OLS/ridge cases already represented in current matched scorecard.',r['r2_vs_persistence'],r['r2_vs_mean_change'],r['r2_vs_terminal_mean'])

    cat='Common/preferred shares — Korea';name='Samsung Electronics common/preferred'
    for file,variant in [('metrics.csv','main'),('metrics_strict.csv','strict')]:
        for r in read('runs/samsung/prediction_final_15055345/'+file):
            if r['family']!='H1':continue
            problems=[]
            if float(r['mae'])>float(r['zero_mae']):problems.append('MAE worse than persistence')
            if float(r['matched_model_mae'])>float(r['matched_a0_mae']):problems.append('MAE worse than direct AR')
            if r['h']=='1':problems.append('primary gain uncertainty spans zero')
            if problems:add(cat,name,'H1 ridge alpha100','current q; trailing 1/5/20-session changes; 20-session change volatility',r['h']+' sessions','expanding monthly refits',variant,r['n'],'docs/regressions/PREDICTION_RESEARCH_REPORT.md','; '.join(problems),f"Model MAE {float(r['mae']):.6f} pp; persistence {float(r['zero_mae']):.6f}; matched AR {float(r['matched_a0_mae']):.6f}. Positive MSE gain can coexist with worse MAE.",r['r2_oos'],status='forecast loss or unreliable primary improvement')
    designs={'D1':('latest one-session discount change; intercept','expanding OLS'),'R756':('current discount q; intercept','rolling 756 origins OLS'),'F4':('latest change; delayed VIX level; 5-day VIX change; 5-day KRW/USD change; 5-day US10y yield change','ridge100; expanding'),'G2':('latest change; relative activity surprise vs prior60-session average; relative high-low range','ridge100; expanding'),'C2':('latest change; late-quarter indicator; late-year indicator','ridge100; expanding')}
    for stem in ['continuation_e_15055790','continuation_f_15055873','continuation_gh_15055999']:
        rows=read('runs/samsung/'+stem+'/metrics.csv')
        for r in rows:
            if r['source']!='final' or r['benchmark']!='candidate' or r['model'] not in designs:continue
            model=r['model'];group=[x for x in rows if x['source']==r['source'] and x['h']==r['h'] and x['fold']==r['fold'] and x['variant']==r['variant'] and x['model']==model and x.get('block')==r.get('block')]
            losses=[]
            for b,label in [('Z0','persistence'),('A0','direct AR'),('H1','history ridge')]:
                q=[x for x in group if x['benchmark']==b]
                if q and float(r['mae'])>float(q[0]['mae']):losses.append('MAE worse than '+label)
            if model in ['F4','G2','C2']:
                base=[x for x in rows if x['source']==r['source'] and x['h']==r['h'] and x['fold']==r['fold'] and x['variant']==r['variant'] and x['model']=='D1r' and x['benchmark']=='candidate' and x.get('block')==r.get('block')]
                if base and float(r['mae'])>float(base[0]['mae']):losses.append('MAE worse than matched reversal base')
            if model in ['R756','F4','G2','C2'] and r['h']=='1':losses.append('failed stated primary development gate')
            if model=='D1' and r['h']=='1':losses.append('primary improvement interval crosses zero')
            if not losses:continue
            variables,training=designs[model];add(cat,name,model,variables,r['h']+' sessions',training,r['variant'],r['n'],'docs/regressions/PREDICTION_CONTINUATION_REPORT.md','; '.join(losses),'Final history was exposed; development gate failure is not evidence every secondary point estimate loses. D1 five-session improvement is retained in the paper.',r['r2_oos'],status='forecast loss or development gate failure')
    add('Common/preferred shares — Korea',name,'V1 history plus activity','current q; trailing changes and volatility; class activity','1/5/20 sessions','development ridge comparisons','validation folds','varies by fold/horizon','docs/regressions/PREDICTION_RESEARCH_REPORT.md','No material incremental validation improvement; not promoted','Development-only result; not a failed final forecast or a causal liquidity test.',status='development-only non-promotion')
    src='runs/loop_exceptions/15208094/results/walk_forward_forecasts.csv'
    labels={'alphabet_a_c':('US dual-class voting shares','Alphabet A/C'),'news_b_a':('US dual-class voting shares','News B/A'),'fox_b_a':('US dual-class voting shares','Fox B/A'),'petrobras_common_preferred':('Two receipt classes with different underlying rights','Petrobras common/preferred ADR'),'volkswagen_common_preferred':('US receipt proxies for German share classes','Volkswagen ADR proxy')}
    for r in read(src):
        if r['b00_beats_persistence']=='True':continue
        cat,name=labels.get(r['pair'],('US class/receipt comparison',r['pair']))
        add(cat,name,'Expanding B00','lagged log relative-price gap; intercept','next observed session','expanding; minimum252 observations','original scoped panel',r['n'],'docs/regressions/LOOP_EXCEPTION_TEST_RESULTS_20261109.md','RMSE worse than persistence',f"RMSE {float(r['rmse_expanding_b00']):.6f} vs {float(r['rmse_persistence']):.6f}; it still beats the aggressive rolling-median benchmark. No zero fair value assumed.",r0=1-(float(r['rmse_expanding_b00'])/float(r['rmse_persistence']))**2)
    failures.sort(key=lambda r:(r['situation_type'],r['comparison'],r['variables'],r['model'],r['horizon'],r['training'],r['coverage']))
    failures=[{'case_id':f'F{i:04d}',**r} for i,r in enumerate(failures,1)];write_csv('WHAT_DID_NOT_WORK.csv',failures)
    sources={r['source'] for r in failures}
    md=['# What we tried that did not clear its predictive comparison','',f'November 12, 2026 snapshot. **{len(failures)} reported specification cases**; these are not independent trials. Grouped by discount situation, then regression variables. [CSV for sorting/filtering](WHAT_DID_NOT_WORK.csv).','',
        '**Read the failure narrowly.** A row can beat persistence and still lose to the terminal anchor. That is a benchmark-specific failure, not proof of zero predictive content. Negative R² below means higher MSE than the named benchmark; values are forecast-loss ratios, not returns. Daily designs also use MAE and development/uncertainty gates. Positive values and caveats remain visible. No p-values or weak descriptive fits are silently treated as forecast tests.','',
        '**Variables and targets:** every conditional design includes an intercept. The monthly target is the 24-/60-month change in the inherited observed discount; q is the current discount, not a required return. Monthly activity is the mean log relative-volume proxy under each original pair convention, not spread/depth or signed flow. Daily targets use the original session-based discount changes or log relative-price change. All windows, coverage variants and units retain their source definitions.','',
        'The current 524-row matched scorecard is used once; earlier LH1/LH2/LH3 versions of the same predictions are not counted as new independent failures. The positive-mean challenger contributes separate cases. Coverage variants, horizons and windows share observations. Successful Berkshire/Liberty point results, Novo benchmark gains and its narrow activity exception are retained in the paper and omitted here when they clear all listed comparisons.','',
        '## Summary by situation and variable block','', '| Situation | Variables | Listed cases |', '| --- | --- | ---: |']
    counts={}
    for r in failures:counts[(r['situation_type'],r['variables'])]=counts.get((r['situation_type'],r['variables']),0)+1
    md.extend('| '+escape(k[0])+' | '+escape(k[1])+' | '+str(n)+' |' for k,n in sorted(counts.items()))
    current=None
    for r in failures:
        if r['situation_type']!=current:
            current=r['situation_type'];md+=['','## '+current,'','| Case / comparison | Variables; model | Horizon / training / coverage; n | What did not work | R²: persistence / mean change / terminal anchor | Qualification |','| --- | --- | --- | --- | --- | --- |']
        md.append('| '+' | '.join(map(escape,[r['case_id']+' — '+r['comparison'],r['variables']+'; '+r['model'],r['horizon']+' / '+r['training']+' / '+r['coverage']+'; n='+str(r['forecast_n']),r['failure_or_limit'],' / '.join(metric(r[k]) or '—' for k in ['r2_vs_persistence','r2_vs_mean_change','r2_vs_terminal_anchor']),r['qualification']]))+' |')
    md+=['','## Weak explanatory results are a separate category','',
        '| Situation | Variables/design | Result | Why this is not counted as a failed forecast |','| --- | --- | --- | --- |',
        '| Samsung common/preferred | US Barra factors; lagged discount; relative activity | Some nominal main-sample associations weaken after batch adjustment | Retrospective factor/gap regressions are not the locked forecast tests |',
        '| Samsung common/preferred | Annual dividend growth + relative non-treasury supply change | Fourteen changes; joint R²≈0.0202; HC1 payout p≈0.544 | Retrospective same-year association, not origin-available forecasting |',
        '| Samsung common/preferred | Annual supply/activity changes | Weak changes fit despite strong levels association | Descriptive annual mechanism proxy, not a chronological forecast |',
        '| Prosus/Tencent local gap | Factors + lagged gap + relative activity | Adjusted R² below1%; no multiplicity-robust factor result | In-sample normalized price-gap model, not NAV or future prediction |',
        '| US share pairs | Quoted spreads and turnover mismatch | Heterogeneous signs and fits | Explanatory liquidity proxies; no universal predictive test |',
        '| Related-security gaps | Common component/PCA | PC1 explains16.22% in that design | Descriptive factor structure, not a forecast-loss comparison |','',
        '## Blocked and unidentifiable tests are not failures','',
        '| Situation | Unavailable test / limitation | Correct label |','| --- | --- | --- |',
        '| Alibaba, unified Shell, Roche participation | Too few matured labels under the declared two-/five-year design | Not evaluated; unavailable history is not a loss |',
        '| All long-horizon panels | No ten-year forecast evaluation meeting the declared requirements | Not run; descriptive ten-year endpoints are not validation |',
        '| Samsung class cash difference | Post-split-equivalent preferred/common annual difference is constantKRW1 in2010–2024 | Separate effect not identified, not estimated as zero |',
        '| Novo synchronized parity | All60auction/NYSE/FXslots missing;6091FXcandidate rows unqualified | Measurement test not available; no substituting daily quotes |',
        '| Demand, governance, borrowing mechanisms | Qualified investor flow, intervention or lending histories missing | Mechanism not tested; no null verdict |','',
        '## Source reports','']
    for s in sorted(sources):
        if s.startswith('docs/regressions/'):md.append('- ['+Path(s).name+'](../'+s+')')
    md+=['- [Annual payout regressions](../docs/regressions/LOOP_TREE_PRODUCTIVE_BATCH_RESULTS_20261112.md)','- [Full synthesis and retained successes](PAPER.md)','']
    (OUT/'WHAT_DID_NOT_WORK.md').write_text('\n'.join(md))
    (OUT/'SOURCE_SNAPSHOTS.json').write_text(json.dumps({'date_local':'2026-11-12','timezone':'America/Denver','core_snapshots':snapshots,'failure_table_cases':len(failures),'monthly_score_cases_screened':len(allcurrent),'scope':'Aggregate documentation only; no licensed raw rows, private crosswalks or UI captures'},indent=2)+'\n')
    print(json.dumps({'core_files':list(core.values()),'failure_cases':len(failures),'situation_groups':len({r['situation_type'] for r in failures})},indent=2))
if __name__=='__main__':main()
