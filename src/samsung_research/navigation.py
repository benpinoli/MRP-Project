"""Append research records and rebuild clickable indexes from immutable manifests."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .e01 import ROOT, read_json, write_json
from .descriptive import STEMS, TITLES


def append_unique(path, entries):
    existing = {json.loads(line)["id"] for line in path.read_text(encoding="utf-8").splitlines() if line} if path.exists() else set()
    with path.open("a",encoding="utf-8") as f:
        for entry in entries:
            if entry["id"] not in existing:
                f.write(json.dumps(entry,allow_nan=False)+"\n")


def record_run(out):
    manifest=read_json(out/"manifest.json")
    stats=read_json(out/"tables/summary.json")
    run_id=manifest["run_id"]
    rel=out.relative_to(ROOT).as_posix()
    now=datetime.now(timezone.utc).isoformat()
    oid=f"O_EP01_{run_id}"
    observation=dict(id=oid,timestamp=now,author_type="ai",author="Codex",pair="samsung_local_common_preferred",
                     window=["2005-01-03","2026-10-20"],kind="visual/statistical",impact="motivation",
                     hypothesis_ids=["H0","H3","H7"],run_ids=[run_id],figure_ids=[f"EP01_F{i:02d}" for i in range(1,8)],
                     claim=f"Descriptive pack produced: six main and six flag-exclusion figures plus local episode windows. Main {stats['main']['discount_observations']} discount observations vs {stats['sensitivity']['discount_observations']} sensitivity; rolling windows {stats['main']['rolling_observations']} vs {stats['sensitivity']['rolling_observations']}. No causal or liquidity conclusion.",
                     data_references=[f"{rel}/README.md",f"{rel}/episodes/REVIEW.md",f"{rel}/tables/summary.json"]+[f"{rel}/figures/{v}/{stem}.png" for v in ("main","sensitivity") for stem in STEMS],
                     competing_explanations=["Voting/control","Cash-flow rights","Investor demand","Liquidity/supply","Measurement artifacts"],
                     next_experiment="Independent quotes/calendar for flagged episodes; choose next descriptive overlay once inputs arrive. No factors or returns yet.",prespecified=True)
    episode=dict(observation,id=oid+"_FLAGS",kind="measurement",impact="measurement concern",hypothesis_ids=["H0"],figure_ids=["EP01_F07"],
                 claim="Four eligible review dates inspected locally; three >5pp moves and one 11-calendar-day interval. Code-5/volume conflict remains excluded. Local price/status consistency does not verify independent quotes or identify news causes.",
                 data_references=[f"{rel}/episodes/REVIEW.md",f"{rel}/episodes/flagged_episode_comparison.csv",f"{rel}/episodes/source_rows_around_flags.csv",f"{rel}/tables/flagged_dates.csv"])
    append_unique(ROOT/"research/observations.jsonl",[observation,episode])
    append_unique(ROOT/"research/decisions.jsonl",[dict(id="D007",timestamp=now,author="User/Codex",type="exploratory extension",previous="Single raw-discount chart",new="Six descriptive graphs, flagged-date sensitivity, local episode inspection and grouped clickable run log",reason="Explicit user request",observation_ids=[oid],methodology_version="3.0.0",affected_experiments=["EP01"],status="adopted",prior_results_impact="Old runs untouched; new grouped output only",alternatives=["Compress flagged dates before rolling, rejected because it bridges gaps"],owner="Codex",next_action="Inspect plots and record remaining data needs")])
    h=read_json(ROOT/"research/hypotheses.json")
    h.update(version="3.0.0",scope="Samsung descriptive pack; no causal vote valuation or factor regressions")
    for item in h["hypotheses"]:
        if item["id"] in ("H0","H3","H7"):
            if oid not in item["evidence_ids"]:
                item["evidence_ids"].append(oid)
            if "EP01" not in item["experiment_ids"]:
                item["experiment_ids"].append("EP01")
            item["artifact_refs"]=[dict(run_id=run_id,path=f"{rel}/README.md",purpose="descriptive motivation; not a causal test")]
        if item["id"]=="H0" and episode["id"] not in item["evidence_ids"]:
            item["evidence_ids"].append(episode["id"])
        if item["id"]=="H3":
            item["confidence"]="Trading activity plotted only; volume ratio does not establish relative liquidity; liquidity hypothesis untested"
        if item["id"]=="H7":
            item["confidence"]="Annual distributions and discount-change instability described; no market/factor driver or cause estimated"
    write_json(ROOT/"research/hypotheses.json",h)
    write_json(ROOT/"research/experiments/EP01.json",dict(id="EP01",version="1.0.1",methodology_version=manifest["methodology_version"],run_id=run_id,run_path=rel,status="executed_with_validation_limitations",exploratory=True,configuration="configs/samsung_descriptive.json",hypothesis_ids=["H0","H3","H7"],observations=[oid,episode["id"]],figure_ids=manifest["figure_ids"],outputs=[o["path"] for o in manifest["outputs"]],models_or_backtests_run=False,next_action=observation["next_experiment"]))
    generate_indexes()
    plan=ROOT/"docs/RESEARCH_PLAN.md"
    with plan.open("a",encoding="utf-8") as f:
        f.write(f"\n\n## Descriptive pack {run_id}\n\nCompleted [EP01 figure pack](../{rel}/README.md): six main/sensitivity graph pairs, flagged-episode inspection and exact tables. [Research log](RESEARCH_LOG.md) and [hypothesis tree](HYPOTHESES.md) link files. All return-based work and factors deferred. Raw source unchanged. Independent quotes/calendar and next-layer inputs remain open.\n")


def generate_indexes():
    reviews=read_json(ROOT/"research/run_reviews.json") if (ROOT/"research/run_reviews.json").exists() else {}
    manifests=sorted((ROOT/"runs").glob("samsung_E01_*/manifest.json"))+sorted((ROOT/"runs/samsung/EP01_descriptive").glob("*/manifest.json"))
    catalog=[]
    research=["# Samsung research log and artifact index","","This is the clickable record of experiments and files. Canonical file catalog: [research/artifacts.json](../research/artifacts.json). Append-only [observations](../research/observations.jsonl) and [decisions](../research/decisions.jsonl) preserve prior claims and revisions. Raw and derived licensed artifacts remain local and Git-ignored.","","[Hypothesis tree](HYPOTHESES.md) · [Methodology](METHODOLOGY.md) · [Run folders](../runs/README.md)","","## Current descriptive packs",""]
    folders=["# Samsung run navigation","","New runs are grouped by pair and experiment. Old immutable run directories remain in place so existing links continue to work.","","## Samsung descriptive packs",""]
    current=[]
    legacy=[]
    for path in manifests:
        m=read_json(path)
        run=path.parent
        rel=run.relative_to(ROOT).as_posix()
        is_pack=m.get("experiment_id")=="EP01"
        entries=[dict(run_id=m["run_id"],experiment_id="EP01" if is_pack else "E01",path=f"{rel}/{o['path']}",sha256=o["sha256"],category="figure" if o["path"].endswith((".png",".svg")) else "table" if o["path"].endswith(".csv") else "documentation/provenance",status=m["status"]) for o in m["outputs"]]
        entries.append(dict(run_id=m["run_id"],experiment_id="EP01" if is_pack else "E01",path=f"{rel}/manifest.json",category="manifest",status=m["status"]))
        catalog.extend(entries)
        if is_pack:
            current.append((rel,m))
            folders.append(f"- [{m['run_id']}](samsung/EP01_descriptive/{run.name}/README.md) — [manifest](samsung/EP01_descriptive/{run.name}/manifest.json)")
            review=reviews.get(m["run_id"],{})
            research += [f"### {m['run_id']}","",f"Review status: {review.get('status','awaiting final visual verification')}. {review.get('note','')}","",f"[Run overview](../{rel}/README.md) · [episode review](../{rel}/episodes/REVIEW.md) · [manifest](../{rel}/manifest.json)","","| ID | Filename | Main | Sensitivity |","|---|---|---|---|"]
            for i,stem in enumerate(STEMS,1):
                research.append(f"| EP01_F{i:02d} | `{stem}.png` / `.svg` | [PNG](../{rel}/figures/main/{stem}.png) · [SVG](../{rel}/figures/main/{stem}.svg) | [PNG](../{rel}/figures/sensitivity/{stem}.png) · [SVG](../{rel}/figures/sensitivity/{stem}.svg) |")
            research += [f"| EP01_F07 | `flagged_discount_windows.png` / `.svg` | [PNG](../{rel}/episodes/flagged_discount_windows.png) · [SVG](../{rel}/episodes/flagged_discount_windows.svg) | Local inspection |","","Exact non-figure files:",""]
            for o in m["outputs"]:
                if not o["path"].startswith("provenance/snapshot/") and not o["path"].endswith((".png",".svg")):
                    research.append(f"- [{o['path']}](../{rel}/{o['path']})")
            research += ["","Every snapshot/support file and hash is retained in the manifest and artifact catalog.",""]
        else:
            legacy.append((rel,m))
    research += ["## Research code and registries","", "- [Descriptive entry point](../scripts/run_samsung_descriptive.py)", "- [Independent saved-output verifier](../scripts/verify_samsung_pack.py)", "- [Plot and calculation module](../src/samsung_research/descriptive.py)", "- [Index and log generation](../src/samsung_research/navigation.py)", "- [Existing source validation](../src/samsung_research/e01.py)", "- [Pack configuration](../configs/samsung_descriptive.json)", "- [Canonical methodology JSON](../methodology/methodology.json) and [schema](../methodology/schema.json)", "- [Source inventory](../research/source_inventory.json), [experiment record](../research/experiments/EP01.json), [run reviews](../research/run_reviews.json)", "- [Descriptive checks](../tests/check_descriptive.py) and [source checks](../tests/check_samsung_e01.py)", "", "## Archived input-validation runs","","Prior adjusted-price panels under methodology 1.0.0 are superseded/deferred, not current evidence. Older raw-discount results remain dated observations. No old directory was moved.",""]
    folders += ["","## Archived input-validation runs",""]
    for rel,m in legacy:
        folders.append(f"- [{m['run_id']}]({Path(rel).name}/manifest.json) — methodology {m['methodology_version']}")
        research += [f"### {m['run_id']}","",f"Methodology {m['methodology_version']} · [manifest](../{rel}/manifest.json)",""]
        for o in m["outputs"]:
            if o["path"].endswith((".png",".svg")) or o["path"] in ("DATA_QUALITY_REPORT.md","summary.json","field_coverage.csv","discontinuity_review.csv","paired_daily.csv"):
                label=" — superseded adjusted-price panel" if "indexed_prices" in o["path"] else ""
                research.append(f"- [{o['path']}](../{rel}/{o['path']}){label}")
        research.append("")
    research += ["## Observation ledger",""]
    for line in (ROOT/"research/observations.jsonl").read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        o=json.loads(line)
        research += [f"### {o['id']}","",f"{o['timestamp']} · {o.get('impact','unclassified')} · hypotheses: {', '.join(o.get('hypothesis_ids',[]))}","",o["claim"],""]
        for ref in o.get("data_references",[]):
            if (ROOT/ref).is_file():
                research.append(f"- [{ref}](../{ref})")
        research += ["",f"Next: {o.get('next_experiment','See ledger')}",""]
    (ROOT/"docs/RESEARCH_LOG.md").write_text("\n".join(research)+"\n",encoding="utf-8")
    (ROOT/"runs/README.md").write_text("\n".join(folders)+"\n",encoding="utf-8")
    write_json(ROOT/"research/artifacts.json",dict(version="1.0.0",generated_at=datetime.now(timezone.utc).isoformat(),artifacts=catalog))
    tree=["# Samsung hypothesis tree and evidence","","[Full research log and every filename](RESEARCH_LOG.md) · [Canonical hypothesis JSON](../research/hypotheses.json) · [Methodology](METHODOLOGY.md) · [Runs](../runs/README.md)","","Observed preferred discounts are not identified vote values. All economic mechanisms below remain hypotheses; plotting trading activity is not a liquidity test. No factor regression or return analysis has run.",""]
    h=read_json(ROOT/"research/hypotheses.json")
    latest=current[-1][0] if current else None
    for item in h["hypotheses"]:
        tree += [f"## {item['id']} {item['claim']}","",f"Status: **{item['status']}**. {item['confidence']}","",f"Mechanism: {item['mechanism']}","",f"Competing/identification concerns: {'; '.join(item['identification_risks'])}.",""]
        if latest and item["id"] in ("H0","H3","H7"):
            ids=[0,1,2,3,5] if item["id"]=="H7" else [4] if item["id"]=="H3" else list(range(6))
            for i in ids:
                tree.append(f"- EP01_F{i+1:02d}: [main {STEMS[i]}.png](../{latest}/figures/main/{STEMS[i]}.png) · [sensitivity](../{latest}/figures/sensitivity/{STEMS[i]}.png)")
            if item["id"]=="H0":
                tree.append(f"- [EP01_F07 local flagged windows](../{latest}/episodes/flagged_discount_windows.png) · [inspection report](../{latest}/episodes/REVIEW.md)")
            tree.append("")
        tree.append("Evidence records: "+", ".join(f"[{oid}](RESEARCH_LOG.md#{oid.lower()})" for oid in item["evidence_ids"]) if item["evidence_ids"] else "No empirical evidence logged for this branch yet.")
        tree += ["", "Next: "+("Independent price/calendar reconciliation; adjustments remain deferred." if item["id"]=="H0" else "Acquire required inputs and specify the smallest descriptive test before estimation."),""]
    tree += ["## Next-layer data needs","","| Overlay | Missing inputs |","|---|---|","| Valuation | Quarterly fundamentals, publication dates, class share counts |","| Buybacks | Actual executions by class; announcements/cancellations separate |","| Liquidity | Bid/ask quotes, historical float, verified returns before price-impact measures |","| Shorting constraints | Borrow fees, lendable inventory, utilization, class restrictions |","","[Acquisition details](DATA_ACQUISITION.md) · [Deferred factor direction](FACTOR_RESEARCH_NOTES.md)"]
    (ROOT/"docs/HYPOTHESES.md").write_text("\n".join(tree)+"\n",encoding="utf-8")
