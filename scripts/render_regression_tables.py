"""Render completed Samsung regression CSVs as readable Markdown tables."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


def number(value, digits=4):
    if pd.isna(value):
        return "—"
    value = float(value)
    if value and abs(value) < 0.0001:
        return f"{value:.2e}"
    return f"{value:.{digits}f}"


def load(run):
    run = Path(run)
    coefficients = pd.read_csv(run / "coefficients.csv")
    statuses = json.loads((run / "status.json").read_text(encoding="utf-8"))
    task = pd.DataFrame({
        "task_index": [x["task_index"] for x in statuses],
        "model_id": [x["model"]["id"] for x in statuses],
        "variant": [x["variant"] for x in statuses],
        "window": [x["window"]["id"] for x in statuses],
        "hac": [x["hac"] for x in statuses],
        "n": [x.get("diagnostics", {}).get("n") for x in statuses],
        "adjusted_r_squared": [x.get("diagnostics", {}).get("adjusted_r_squared") for x in statuses],
        "condition": [x.get("diagnostics", {}).get("standardized_condition") for x in statuses],
    })
    return coefficients.merge(task, on=["task_index", "model_id"], validate="many_to_one"), task


def baseline_table(data, task):
    rows = []
    lag = data.loc[data.term.eq("lag_discount")].sort_values("task_index")
    intercept = data.loc[data.term.eq("intercept"), ["task_index", "coefficient"]].rename(
        columns={"coefficient": "intercept"})
    lag = lag.merge(intercept, on="task_index", validate="one_to_one")
    for _, x in lag.iterrows():
        rows.append(
            f"| {x.variant} | {x.window} | {int(x.hac)} | {number(x.intercept)} | "
            f"{number(x.coefficient)} | {number(x.std_error)} | {number(x.p_value)} | "
            f"{number(x.q_bh_exploratory)} | [{number(x.ci_lower)}, {number(x.ci_upper)}] | "
            f"{int(x.n)} | {number(x.adjusted_r_squared)} |"
        )
    return "\n".join([
        "# B00 discount-only coefficient table", "",
        "Outcome is the daily discount change in percentage points. `lag_discount` is the prior-session discount in percentage points.", "",
        "| Variant | Window | HAC | Intercept | Lag discount | SE | p | BH q | 95% CI | n | Adj. R² |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|", *rows, "",
        "All configured HAC bandwidths are shown. Estimates are exploratory associations.", "",
    ])


def retrospective_tables(data, task, hac):
    selected = data.loc[data.hac.eq(hac)].copy()
    windows = ["full", "2005_2014", "2015_2019", "2020_2026"]
    lines = [
        "# B01–B04 retrospective US-Barra coefficient tables", "",
        f"Central display uses Bartlett HAC bandwidth {hac}. Cells show `coefficient (standard error); p; BH q`. "
        "The source `coefficients.csv` retains HAC 5, 20, and 60 estimates.", "",
        "Factor returns were converted from percent to decimal. Outcomes are `dd_pp` for B01/B03/B04 and `dg` for B02. "
        "These are retrospective explanatory sensitivities, not point-in-time forecasts.", "",
    ]
    for model in ["B01", "B02", "B03", "B04"]:
        for variant in ["main", "sensitivity"]:
            block = selected.loc[selected.model_id.eq(model) & selected.variant.eq(variant)]
            lines += [f"## {model} — {variant}", "",
                      "| Term | Full | 2005–2014 | 2015–2019 | 2020–2026 |",
                      "|---|---:|---:|---:|---:|"]
            terms = block.sort_values("task_index").term.drop_duplicates().tolist()
            for term in terms:
                cells = []
                for window in windows:
                    row = block.loc[block.term.eq(term) & block.window.eq(window)]
                    if row.empty:
                        cells.append("—")
                    else:
                        x = row.iloc[0]
                        q = "—" if term == "intercept" else number(x.q_bh_exploratory)
                        cells.append(f"{number(x.coefficient)} ({number(x.std_error)}); p={number(x.p_value)}; q={q}")
                lines.append("| " + term + " | " + " | ".join(cells) + " |")
            lines.append("")
    lines += ["## Sample and diagnostic summary", "",
              "| Model | Variant | Window | n | Adjusted R² | Standardized condition |",
              "|---|---|---|---:|---:|---:|"]
    diagnostics = task.loc[task.hac.eq(hac)].sort_values(["model_id", "variant", "task_index"])
    for _, x in diagnostics.iterrows():
        lines.append(f"| {x.model_id} | {x.variant} | {x.window} | {int(x.n)} | "
                     f"{number(x.adjusted_r_squared)} | {number(x.condition)} |")
    lines += ["", "Blocked mechanism specifications are not included and are not null findings.", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--hac", type=int, default=20)
    args = parser.parse_args()
    data, task = load(args.run)
    text = baseline_table(data, task) if set(data.model_id) == {"B00"} else retrospective_tables(data, task, args.hac)
    (args.run / "COEFFICIENT_TABLES.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
