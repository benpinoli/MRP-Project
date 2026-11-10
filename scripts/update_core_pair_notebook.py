#!/usr/bin/env python3
"""Idempotently add the completed core-pair checkpoint to the submission notebook."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "docs/MRP_Initial_Submission_Final.ipynb"
MARKER = "## 8. Remaining core-pair price baselines"
LOOP_MARKER = "## 9. LOOP-exception generalization"

MARKDOWN = """## 8. Remaining core-pair price baselines

The three remaining price-only panels are now complete through November 6, 2026. They use adjusted reported closes, exact-date joins, fixed windows, the existing B00 equation `Δq = α + ρq₋₁ + ε`, and Newey–West inference. SK Square/SK Hynix and Samsung Fire/Samsung Electronics are normalized price ratios, **not NAV discounts**. TSMC uses five Taiwan common shares per ADS and DEXTAUS in TWD per USD.

| Pair | Actual sample | n | ρ (HAC 20 SE) | p | Adjusted R² |
|---|---:|---:|---:|---:|---:|
| SK Square / SK Hynix | 2021-11-30–2026-11-06 | 1,149 | −0.01153 (0.00438) | 0.0084 | 0.56% |
| Samsung Fire / Samsung Electronics | 2005-01-04–2026-11-06 | 5,203 | −0.00148 (0.00098) | 0.130 | 0.06% |
| TSMC local / ADR | 2005-01-04–2026-11-06 | 4,737 | −0.06905 (0.00752) | 4.15×10⁻²⁰ | 3.42% |

The TSM ADR uses CRSP through September 30, 2026 and Compustat North America from October 1 through November 6; all five overlapping September closes matched exactly and rows are source-tagged. Same-date FRED FX is a noon New York fixing after the Taiwan close, making the baseline retrospective; a prior-fixing sensitivity is retained in the panel. Korean NAV models remain pending because isolated filings do not supply dated ownership histories. See `docs/regressions/CORE_PAIR_BASELINE_RESULTS.md` for coverage, join losses, adjustments, fundamentals, and provenance gaps.
"""

CODE = """core_pair_baselines = pd.DataFrame([
    {"Pair": "SK Square / SK Hynix", "n": 1149, "rho": -0.011528, "HAC20_SE": 0.004377, "p": 0.008439, "Adjusted_R2": 0.005612},
    {"Pair": "Samsung Fire / Samsung Electronics", "n": 5203, "rho": -0.001484, "HAC20_SE": 0.000980, "p": 0.129881, "Adjusted_R2": 0.000605},
    {"Pair": "TSMC local / ADR", "n": 4737, "rho": -0.069053, "HAC20_SE": 0.007519, "p": 4.146079e-20, "Adjusted_R2": 0.034184},
])
core_pair_baselines
"""

LOOP_MARKDOWN = """## 9. LOOP-exception generalization

The LOOP Exceptions workbook is now tested beyond Samsung wherever exact US-listed class pairs or clearly labeled US proxies are locally available. Five of seven share-class/preferred pairs have a negative full-sample B00 coefficient at conventional significance levels, but expanding forecasts beat zero-change persistence only for Berkshire A/B and Liberty Broadband A/C. All seven beat a prior-252-session rolling-median forecast, showing that persistence is the more demanding benchmark.

| Question | Outcome |
|---|---|
| Does mean reversion generalize? | Yes descriptively in 5/7 pairs; fit is usually tiny, except Berkshire (9.8% adjusted R²). |
| Does it forecast? | Berkshire improves RMSE about 3.4% vs persistence; Liberty about 0.2%; the other five do not. |
| Is liquidity a common explanation? | No. Spread signs and significance differ by pair; Volkswagen quotes are unavailable. |
| Is there one global gap factor? | No strong one: PC1 explains 16.22% of seven US differential changes. |
| Do held-company returns pass through? | Often, but betas range from 0.25 to about 1.00; only Liberty/Charter and SoftBank/Arm show clear downside asymmetry. |

Quoted-spread strategy sensitivities are diagnostics only: borrow, dividends, taxes, locates, impact, and conversion costs are missing. Holdco regressions are return pass-through tests, not NAV discounts. See `docs/regressions/LOOP_EXCEPTION_TEST_RESULTS_20261109.md` for hypotheses, samples, regressions, results, and blocked exact-local tests.

The staged Prosus/Tencent local-security B01–B04 sensitivity is also complete: full-window n=1,611, adjusted R² 0.48%–0.71%, and no factor survives BH adjustment. B03's lagged gap is nominally negative (p=0.018) but q=0.634; activity is null. It remains a normalized price ratio, not NAV.
"""

LOOP_CODE = """loop_exception_summary = pd.DataFrame([
    {"Pair": "Alphabet A/C", "n": 2988, "B00_rho": -0.001379, "p": 0.4522, "B00_beats_persistence": False},
    {"Pair": "Berkshire A/B", "n": 4043, "B00_rho": -0.195744, "p": 1.1228e-6, "B00_beats_persistence": True},
    {"Pair": "News B/A", "n": 3184, "B00_rho": -0.004970, "p": 0.01196, "B00_beats_persistence": False},
    {"Pair": "Fox B/A", "n": 1741, "B00_rho": -0.004427, "p": 0.01580, "B00_beats_persistence": False},
    {"Pair": "Liberty Broadband A/C", "n": 2779, "B00_rho": -0.028091, "p": 6.4656e-10, "B00_beats_persistence": True},
    {"Pair": "Petrobras common/preferred", "n": 6257, "B00_rho": -0.006034, "p": 0.0002304, "B00_beats_persistence": False},
    {"Pair": "Volkswagen ADR proxies", "n": 5679, "B00_rho": -0.002652, "p": 0.2370, "B00_beats_persistence": False},
])
loop_exception_summary
"""


def cell(kind: str, source: str) -> dict:
    out = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        out.update({"execution_count": None, "outputs": []})
    return out


notebook = json.loads(PATH.read_text(encoding="utf-8"))
notebook["cells"] = [
    c for c in notebook["cells"]
    if MARKER not in "".join(c.get("source", []))
    and "core_pair_baselines = pd.DataFrame" not in "".join(c.get("source", []))
    and LOOP_MARKER not in "".join(c.get("source", []))
    and "loop_exception_summary = pd.DataFrame" not in "".join(c.get("source", []))
]
notebook["cells"].extend([
    cell("markdown", MARKDOWN), cell("code", CODE),
    cell("markdown", LOOP_MARKDOWN), cell("code", LOOP_CODE),
])
PATH.write_text(json.dumps(notebook) + "\n", encoding="utf-8")
