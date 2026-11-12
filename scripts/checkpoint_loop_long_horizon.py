"""Update the canonical research tree and durable ledgers without losing history."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT/'docs/regressions'
PROTOCOL = 'docs/regressions/LOOP_LONG_HORIZON_PROTOCOL_20261112.md'


def save(path, value):
    temporary = Path(str(path)+'.pending')
    temporary.write_text(json.dumps(value, indent=2)+'\n')
    temporary.replace(path)


def render(tree):
    lines = ['# LOOP discount hypothesis tree for two to ten years', '',
        tree['active_objective'], '',
        '[Canonical JSON](PREDICTION_MECHANISM_TREE.json) · '
        '[Active protocol](LOOP_LONG_HORIZON_PROTOCOL_20261112.md) · '
        '[Prior structural plan](LONG_HORIZON_RESEARCH_PLAN.md)', '',
        'Historical Samsung/daily verdicts retain their original scope. New LOOP '
        'assessments are recorded separately; an activity proxy is not a causal '
        'liquidity test, and exposed-history backtests are not prospective validation.', '',
        'Current execution: '+tree['execution_status'], '']
    for track in tree['research_tracks']:
        lines.extend(['## '+track['id']+' '+track['title'], '', track['question'], ''])
        for node_id in track['nodes']:
            n = next(n for n in tree['nodes'] if n['id'] == node_id)
            lines.extend(['### '+n['id']+' '+n['title'], '',
                '**Historical status:** '+n['status']+'. '+n['status_scope'], '',
                '**Samsung long-horizon status:** '+n['long_horizon_status'], '',
                'Mechanism: '+n['mechanism_chain'], '', 'Nearest rival: '+n['nearest_rival'], '',
                'Next discriminating test: '+n['next_discriminating_test'], ''])
            for assessment in n.get('loop_long_horizon_assessments', []):
                lines.extend(['**LOOP '+assessment['batch_id']+':** '+assessment['status']+'. '+assessment['scope'], '',
                    'Evidence: '+', '.join(assessment['evidence_paths']), ''])
    lines.extend(['## Research discipline', ''])
    lines.extend('- '+r for r in tree['search_rules'])
    (DOCS/'PREDICTION_MECHANISM_TREE.md').write_text('\n'.join(lines)+'\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--status', choices=['registered', 'submitted', 'completed', 'failed'], required=True)
    parser.add_argument('--job-id')
    parser.add_argument('--run')
    args = parser.parse_args()
    now = datetime.now(timezone.utc).isoformat()
    tree_path = DOCS/'PREDICTION_MECHANISM_TREE.json'
    tree = json.loads(tree_path.read_text())
    old_ids = [n['id'] for n in tree['nodes']]
    tree.setdefault('objective_history', []).append({'objective': tree['active_objective'],
        'recorded_utc': now}) if tree['active_plan'] != PROTOCOL else None
    tree['active_objective'] = 'Develop and test hypothesis-guided linear predictions of LOOP class-price discounts over 2, 5 and 10 years; preserve all prior scoped findings'
    tree['active_plan'] = PROTOCOL
    tree['updated_utc'] = now
    batch = {'id': 'LOOP-LH1', 'status': args.status, 'updated_utc': now,
             'config': 'configs/loop_long_horizon_v1.json', 'protocol': PROTOCOL,
             'purpose': 'Monthly 24/60/120-month linear discount predictions with matured-label training and pragmatic cleaning',
             'tree_nodes': ['M01', 'M02', 'B01', 'B02', 'L01'],
             'review': 'Synthetic calendar/aggregation/leakage checks; no independent-agent review claimed',
             'authorization': 'User November 12 go instruction; isolated bad days may be excluded; no paused job restart',
             'validated_predictive_model': False}
    if args.job_id:
        batch['job_id'] = args.job_id
    if args.run:
        batch['run'] = args.run
    if args.status == 'completed':
        run = ROOT/args.run
        progress = json.loads((run/'progress.json').read_text())
        if progress['status'] != 'completed':
            raise ValueError('Cannot mark an incomplete run completed')
        batch['results'] = progress
        batch['report'] = 'docs/regressions/LOOP_LONG_HORIZON_RESULTS_20261112.md'
    tree['execution_status'] = 'LOOP-LH1 '+args.status+'; '+('job '+args.job_id if args.job_id else 'configuration registered before estimation')
    tree['loop_long_horizon_batch'] = batch
    evidence = [PROTOCOL] + ([args.run] if args.run else [])
    if args.status == 'completed':
        evidence.append(batch['report'])
    scopes = {
        'M01': 'Exploratory monthly samples exclude isolated bad rows; 50% observed-weekday coverage main and 80% sensitivity. No full calendar certification or future-price filling.',
        'M02': 'Preserve dated split exclusions, Shell class boundaries and Roche conversion. Cross-market matched-basis ratios and Shell quote scale remain explicit assumptions.',
        'B01': 'Persistence benchmark is mandatory at 24/60/120 calendar months; daily benchmark findings are not promoted to multi-year truth.',
        'B02': 'Nested linear discount-state models use only matured labels at each expanding origin; historical outcomes are exposed, ten-year evaluation may be infeasible.',
        'L01': 'Incremental relative-volume activity prediction is tested against a state model on identical origins. It does not establish causal liquidity costs.'}
    for node in tree['nodes']:
        if node['id'] in scopes:
            assessment = {'batch_id': 'LOOP-LH1', 'status': args.status, 'scope': scopes[node['id']],
                          'evidence_paths': evidence, 'updated_utc': now}
            previous = node.setdefault('loop_long_horizon_assessments', [])
            previous[:] = [a for a in previous if a['batch_id'] != 'LOOP-LH1']+[assessment]
    assert old_ids == [n['id'] for n in tree['nodes']]
    save(tree_path, tree)
    render(tree)
    path = DOCS/'LONG_HORIZON_EXECUTION_LEDGER.json'
    ledger = json.loads(path.read_text())
    ledger['active_objective'] = tree['active_objective']
    ledger['updated_utc'] = now
    ledger['batches'] = [b for b in ledger['batches'] if b['id'] != 'LOOP-LH1']+[batch]
    ledger.setdefault('decisions', [])
    if not any(d['id'] == 'LH-D04' for d in ledger['decisions']):
        ledger['decisions'].append({'id': 'LH-D04', 'decision': 'Prioritize results by excluding isolated invalid observations; no future backfill, no global block from local gaps; scope every prediction to its horizon and assumptions', 'status': 'authorized_2026-11-12'})
    save(path, ledger)
    evidence_path = DOCS/'LOOP_RESEARCH_EVIDENCE_LEDGER.json'
    history = json.loads(evidence_path.read_text()) if evidence_path.exists() else {'schema_version': 1, 'events': []}
    history['events'].append({'batch_id': 'LOOP-LH1', 'timestamp_utc': now, 'status': args.status,
        'job_id': args.job_id, 'run': args.run, 'supported': ['Verified receipt controls; exact candidate date membership'],
        'not_established': ['Required-return discount rates', 'Causal liquidity mechanism', 'Validated 2/5/10-year predictive model', 'Executable arbitrage'],
        'preserved_prior_findings': 'Existing Samsung, core-pair, and US proxy results retain their original samples/horizons',
        'next_test': 'Same-origin OOS benchmark and activity increments, coverage sensitivity, nonoverlapping information counts'})
    save(evidence_path, history)
    print('Tree, readable companion, execution ledger and append-only evidence history updated:', args.status)


if __name__ == '__main__':
    main()
