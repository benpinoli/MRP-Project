#!/usr/bin/env python3
"""Apply reviewed hypothesis-resolution outcomes to the canonical JSON tree and ledger."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TREE = ROOT / "docs/regressions/PREDICTION_MECHANISM_TREE.json"
LEDGER = ROOT / "docs/regressions/LONG_HORIZON_EXECUTION_LEDGER.json"
REPORT = "docs/regressions/HYPOTHESIS_RESOLUTION_RESULTS_20261109.md"
RUN = "runs/hypothesis_resolution/15204916/results"


def add_path(node: dict) -> None:
    paths = node.setdefault("evidence_paths", [])
    for path in (REPORT, RUN):
        if path not in paths:
            paths.append(path)


tree = json.loads(TREE.read_text())
nodes = {node["id"]: node for node in tree["nodes"]}

nodes["S06"].update(
    status="unresolved",
    status_scope="Annual supply levels mark regimes, but time/activity-controlled evidence is weak, first differences are null, and supply-only fails in the stable-count era",
    failure_reason="Only 17 level years; non-treasury is not public float; supply ratio is nearly constant in 2018-2023 while discount spans 9.61 pp",
    next_discriminating_test="Add independently dated ownership/public-float and actual trading-cost histories; do not repeat the annual count ratio across daily rows",
    long_horizon_status="Annual panel tested: simple supply-only explanation insufficient; ownership/liquidity channels unresolved",
)
add_path(nodes["S06"])

nodes["L01"].update(
    status="unresolved",
    status_scope="Annual relative-activity proxy is weak in levels and changes; actual spread/depth mechanism remains untested",
    failure_reason="Volume per year-end non-treasury share is not synchronized spread, depth, signed flow, or execution cost",
    next_discriminating_test="Acquire synchronized class bid/ask and depth or a reviewed cost proxy; retain annual activity result as a proxy null",
    long_horizon_status="Annual activity proxy tested with null change association; true liquidity-cost channel unresolved",
)
add_path(nodes["L01"])

for node_id in ("S01", "S02", "S03"):
    nodes[node_id]["status"] = "unresolved"
    nodes[node_id]["long_horizon_status"] = "Sparse recent issuer case study completed; connected, near-proportional programs do not identify a persistent effect"
    add_path(nodes[node_id])

nodes["S01"]["status_scope"] = "2024/2025 authorization fractions were nearly class-proportional; descriptive event paths mostly widened"
nodes["S02"]["status_scope"] = "Aggregate reports cannot be backdated; 2024 report preceded narrowing while 2025 report preceded widening"
nodes["S03"]["status_scope"] = "Cancellation window was mixed and belongs to the same 2024 program, not an independent purchase"

nodes["P01"].update(
    status="unresolved",
    status_scope="One FY2024 dividend decision produced mixed 1/5/20-session paths; no ex-date or repeated announcement panel",
    long_horizon_status="Single descriptive dividend-decision case completed; payout mechanism unresolved",
)
add_path(nodes["P01"])

nodes["M04"].update(
    status="unresolved",
    status_scope="After a widening, preferred-over-common returns correct positively at 1/5/20 sessions, primarily through preferred catch-up; exact clocks/executable quotes absent",
    failure_reason="Full-sample close-to-close response can include bid-ask bounce or auction effects and is not an untouched forecast",
    next_discriminating_test="Validate on an untouched future cohort with synchronized executable quotes or auction data",
    long_horizon_status="Price-leg decomposition completed: preferred catch-up dominates observed short-horizon correction; mechanism remains noncausal",
)
add_path(nodes["M04"])

nodes["B03"].update(
    status="unresolved",
    status_scope="Full-sample leg decomposition supports preferred catch-up after widening across fixed subperiods; exposed/OOS transfer remains unconfirmed",
)
add_path(nodes["B03"])

tree["updated_utc"] = "2026-11-09"
tree["execution_status"] = "LHA and LHB completed/reviewed; hypothesis-resolution job 15204916 completed; source reconstruction and payout panel remain active"
tree["hypothesis_resolution_batch"] = {
    "status": "completed_reviewed",
    "job_id": 15204916,
    "run": RUN,
    "report": REPORT,
    "questions": {
        "S06_L01": "Supply levels mark regimes, but changes are null and stable-count-era discount variation rejects supply-only sufficiency; activity proxy also weak.",
        "M04_B03": "Observed correction after widening is primarily preferred catch-up; common reversal contributes at five sessions only in the full sample.",
        "S01_S02_S03_P01": "Recent programs are near-proportional and event paths mixed; no causal preferred-support result.",
        "TSMC_X02_X03_M04": "Both later US ADR and next Taiwan local prices move toward parity; spread sensitivity preserves signs."
    },
    "remaining_gates": ["dated Korean ownership/NAV inputs", "reviewed payout-delivery panel", "borrow/short data", "Samsung GDR history", "synchronized Korean quotes/depth"]
}
TREE.write_text(json.dumps(tree, indent=2) + "\n")

ledger = json.loads(LEDGER.read_text())
ledger["updated_utc"] = "2026-11-09"
batches = {batch["id"]: batch for batch in ledger["batches"]}
batches["LHB"] = {
    "id": "LHB", "status": "completed_independently_reviewed", "job_id": 15069061,
    "run": "runs/samsung/long_horizon_b_15069061",
    "purpose": "Annual non-treasury share supply and relative activity panel",
    "review": "17 joint years; non-treasury is not public float; volume proxy is not trading cost"
}
batches["HR1"] = {
    "id": "HR1", "status": "completed_reviewed", "job_id": 15204916,
    "run": RUN, "report": REPORT,
    "purpose": "Resolve currently testable supply/activity, price-leg, issuer-event, and TSMC timing questions"
}
ledger["batches"] = list(batches.values())
LEDGER.write_text(json.dumps(ledger, indent=2) + "\n")
