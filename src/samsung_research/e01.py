"""Samsung E01. Run through scripts/run_samsung_e01.py; never modifies raw data."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import math
import platform
import subprocess
import sys
import traceback
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def write_csv(path, rows, fields=None):
    rows = list(rows)
    fields = fields or (list(rows[0]) if rows else ["no_records"])
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def number(value):
    try:
        n = float(value)
        return n if math.isfinite(n) else None
    except (ValueError, TypeError):
        return None


def positive(value):
    n = number(value)
    return n is not None and n > 0


def discount(preferred, common):
    if not positive(preferred) or not positive(common):
        return None
    return 100 * (1 - float(preferred) / float(common))


def adjusted_price(row):
    raise ValueError("Adjustment formula unresolved; split-adjusted calculations deferred")


def eligibility(row, config):
    """Overlapping reason flags; no fill, no automatic deletion based on returns."""
    flags = []
    if not positive(row.get("prccd")):
        flags.append("invalid_close")
    if number(row.get("qunit")) != config["required_quotation_unit"]:
        flags.append("unsupported_quotation_unit")
    if row.get("prcstd") not in config["accepted_price_status"]:
        flags.append("carried_price" if row.get("prcstd") in config["carried_price_status"] else "unaccepted_status")
    # Vendor status 10 can be valid without volume when the price changes.
    # Volume is audited separately, not an additional eligibility requirement.
    if date.fromisoformat(row["datadate"]).weekday() >= 5:
        flags.append("weekend")
    close, low, high = (number(row.get(f)) for f in ("prccd", "prcld", "prchd"))
    if low is not None and high is not None and (low <= 0 or high < low or (close is not None and not low <= close <= high)):
        flags.append("inconsistent_high_low_close")
    return flags


def load_and_validate(path, config):
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, list(reader)
    required = {"gvkey", "iid", "datadate", "isin", "exchg", "tpci", "curcdd", "prccd", "qunit", "prcstd", "ajexdi", "cshtrd", "split", "prchd", "prcld"}
    if not required.issubset(fields):
        raise ValueError(f"Missing fields: {required - set(fields)}")
    keys = [(r["gvkey"], r["iid"], r["datadate"]) for r in rows]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate gvkey/iid/date keys: resolve upstream; never deduplicate silently")
    selected = {}
    normalized = []
    for label, mapping in config["classes"].items():
        candidates = [r for r in rows if r["gvkey"] == config["gvkey"] and r["iid"] == mapping["iid"]]
        if not candidates:
            raise ValueError(f"No rows for {label}")
        candidates.sort(key=lambda r: r["datadate"])
        previous = None
        for r in candidates:
            date.fromisoformat(r["datadate"])
            expected = {"isin": mapping["isin"], "tpci": mapping["tpci"], "curcdd": config["currency"], "exchg": config["exchange"]}
            if any(r[k] != v for k, v in expected.items()):
                raise ValueError(f"Identity mismatch: {label} {r['datadate']}")
            flags = eligibility(r, config)
            norm = dict(r, class_name=label, source_id=config["source_id"],
                        price_eligible=not flags, exclusion_reasons=";".join(flags),
                        index_eligible=False,
                        unchanged_close=previous is not None and r["prccd"] == previous["prccd"],
                        availability_date="", split_adjusted_close=None,
                        volume_review=not positive(r.get("cshtrd")))
            normalized.append(norm)
            previous = r
        selected[label] = candidates
    return fields, rows, selected, normalized


def match_pair(normalized, config):
    by_class = {j: {r["datadate"]: r for r in normalized if r["class_name"] == j} for j in config["classes"]}
    dates = sorted(set().union(*(set(v) for v in by_class.values())))
    paired, base = [], None
    for t in dates:
        p, c = by_class["preferred"].get(t), by_class["common"].get(t)
        valid = p is not None and c is not None and p["price_eligible"] and c["price_eligible"]
        index_valid = valid and p["index_eligible"] and c["index_eligible"]
        if index_valid and base is None:
            base = (t, p["split_adjusted_close"], c["split_adjusted_close"])
        reasons = []
        for label, row in (("preferred", p), ("common", c)):
            if row is None:
                reasons.append(label + ":absent_row")
            elif not row["price_eligible"]:
                reasons.append(label + ":" + row["exclusion_reasons"])
        paired.append({"datadate": t, "pair_price_eligible": bool(valid), "pair_index_eligible": bool(index_valid),
                       "exclusion_reasons": "|".join(reasons),
                       "preferred_raw_close": number(p["prccd"]) if p else None,
                       "common_raw_close": number(c["prccd"]) if c else None,
                       "discount_pct": discount(p["prccd"], c["prccd"]) if valid else None,
                       "preferred_adjusted_close": p["split_adjusted_close"] if index_valid else None,
                       "common_adjusted_close": c["split_adjusted_close"] if index_valid else None,
                       "preferred_index": 100 * p["split_adjusted_close"] / base[1] if index_valid else None,
                       "common_index": 100 * c["split_adjusted_close"] / base[2] if index_valid else None})
    if base is None:
        valid_dates = [r["datadate"] for r in paired if r["pair_price_eligible"]]
        if not valid_dates:
            raise ValueError("No matched price-eligible observations")
        return paired, valid_dates[0]
    return paired, base[0]


def audit(fields, rows, selected, normalized, paired, config):
    inventory = []
    for key in sorted(set((r["gvkey"], r["iid"]) for r in rows)):
        issue = [r for r in rows if (r["gvkey"], r["iid"]) == key]
        inventory.append({"gvkey": key[0], "iid": key[1], "rows": len(issue),
                          "first": min(r["datadate"] for r in issue), "last": max(r["datadate"] for r in issue),
                          **{f: ";".join(sorted(set(r[f] or "<missing>" for r in issue))) for f in ["isin", "exchg", "curcdd", "tpci"]}})
    coverage, quality, changes, diagnostics = [], {}, [], []
    for label, issue in selected.items():
        nr = [r for r in normalized if r["class_name"] == label]
        for field in fields:
            observed = [r for r in issue if r[field] != ""]
            coverage.append({"class_name": label, "field": field, "rows": len(issue),
                             "missing": len(issue)-len(observed), "nonmissing": len(observed),
                             "first_nonmissing": observed[0]["datadate"] if observed else "",
                             "last_nonmissing": observed[-1]["datadate"] if observed else ""})
        counts = Counter(flag for r in nr for flag in r["exclusion_reasons"].split(";") if flag)
        quality[label] = {"rows": len(issue), "first": issue[0]["datadate"], "last": issue[-1]["datadate"],
                          "price_eligible": sum(r["price_eligible"] for r in nr),
                          "index_eligible": sum(r["index_eligible"] for r in nr),
                          "statuses": dict(Counter(r["prcstd"] for r in issue)),
                          "quotation_units": sorted(set(r["qunit"] for r in issue)),
                          "adjustment_factors": sorted(set(r["ajexdi"] for r in issue)),
                          "exclusion_flags_overlapping": dict(counts),
                          "unchanged_close_valid": sum(r["unchanged_close"] and r["price_eligible"] for r in nr),
                          "carried_with_positive_volume": sum(r["prcstd"] in config["carried_price_status"] and positive(r["cshtrd"]) for r in issue),
                          "missing_close": sum(r["prccd"] == "" for r in issue),
                          "volume_review": sum(r["volume_review"] for r in nr),
                          "status10_without_positive_volume": sum(r["prcstd"] == "10" and not positive(r["cshtrd"]) for r in issue),
                          "invalid_factor": sum(not positive(r["ajexdi"]) for r in issue)}
        prev = None
        for r in issue:
            if r["split"] or (prev and r["ajexdi"] != prev["ajexdi"]):
                changes.append({"class_name": label, "date": r["datadate"], "split": r["split"],
                                "factor_before": prev["ajexdi"] if prev else None, "factor_after": r["ajexdi"],
                                "consistent_factor_ratio": bool(prev and positive(r["split"]) and positive(prev["ajexdi"]) and positive(r["ajexdi"]) and math.isclose(float(prev["ajexdi"])/float(r["ajexdi"]), float(r["split"])))})
            prev = r
    prev = prev_index = None
    for row in paired:
        if row["pair_price_eligible"]:
            delta = row["discount_pct"]-prev["discount_pct"] if prev else None
            days = (date.fromisoformat(row["datadate"])-date.fromisoformat(prev["datadate"])).days if prev else 0
            rp = rc = None
            if row["pair_index_eligible"] and prev_index:
                rp = row["preferred_adjusted_close"]/prev_index["preferred_adjusted_close"]-1
                rc = row["common_adjusted_close"]/prev_index["common_adjusted_close"]-1
            flags = []
            if delta is not None and abs(delta) > config["jump_discount_pp"]:
                flags.append("large_discount_change")
            if config.get("adjusted_prices_enabled", False) and any(v is not None and abs(v)>config["jump_adjusted_return_abs"] for v in (rp, rc)):
                flags.append("large_adjusted_price_change")
            if days > config["long_gap_days"]:
                flags.append("long_gap")
            if flags:
                diagnostics.append({"date": row["datadate"], "previous_date": prev["datadate"] if prev else "", "discount_change_pp": delta,
                                    "preferred_adjusted_change": rp, "common_adjusted_change": rc,
                                    "calendar_days": days, "review_flags": ";".join(flags),
                                    "resolution": "Retained; no price eligibility failure. Adjustment analysis deferred. Independent quote/event reconciliation pending; no causal attribution."})
            prev = row
            if row["pair_index_eligible"]:
                prev_index = row
    valid = [r for r in paired if r["pair_price_eligible"]]
    vals = np.array([r["discount_pct"] for r in valid])
    summary = {"raw_rows": len(rows), "raw_fields": len(fields), "raw_issues": len(inventory),
               "duplicate_key_excess": 0, "selected_rows": len(normalized), "other_issue_rows": len(rows)-len(normalized),
               "union_dates": len(paired), "matched_valid_dates": len(valid), "excluded_union_dates": len(paired)-len(valid),
               "matched_fraction_of_union": len(valid)/len(paired),
               "matched_index_dates": sum(r["pair_index_eligible"] for r in paired),
               "first_valid": valid[0]["datadate"], "last_valid": valid[-1]["datadate"],
               "first_discount_pct": float(vals[0]), "last_discount_pct": float(vals[-1]),
               "median_discount_pct": float(np.median(vals)),
               "minimum": min(valid, key=lambda r:r["discount_pct"]), "maximum": max(valid, key=lambda r:r["discount_pct"]),
               "classes": quality, "factor_events": changes, "discontinuity_flags": len(diagnostics)}
    start, end = date.fromisoformat(paired[0]["datadate"]), date.fromisoformat(paired[-1]["datadate"])
    observed_dates = {r["datadate"] for r in paired}
    absent_weekdays = []
    while start <= end:
        if start.weekday()<5 and start.isoformat() not in observed_dates:
            absent_weekdays.append({"date": start.isoformat(), "classification": "Absent both issues; holiday/session status unverified"})
        start += timedelta(days=1)
    summary["unclassified_absent_weekdays"] = len(absent_weekdays)
    return summary, inventory, coverage, diagnostics, absent_weekdays


def methodology_markdown(registry):
    lines = ["# Samsung E01 methodology", "", f"Methodology version {registry['methodology_version']}. Canonical source: `methodology/methodology.json`.",
             "Generated by `scripts/run_samsung_e01.py --sync-methodology`; edit the JSON, version it, then regenerate this file.", ""]
    for key in ("context", "measures", "models", "figures", "decisions", "change_log"):
        lines.extend([f"## {key.replace('_', ' ').title()}", ""])
        entries = registry[key]
        if isinstance(entries, dict):
            entries = [entries]
        for entry in entries:
            if "id" in entry:
                lines.extend([f"### {entry['id']} {entry.get('name','')}", ""])
            for name, value in entry.items():
                formatted = json.dumps(value, ensure_ascii=False, allow_nan=False) if isinstance(value, (list, dict)) else str(value)
                lines.extend([f"**{name}**: {formatted}", ""])
    return "\n".join(lines)


def validate_registry(registry, schema, markdown):
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(registry)
    ids = [r["id"] for section in ("measures", "figures", "decisions") for r in registry[section]]
    if len(set(ids)) != len(ids):
        raise ValueError("Registry IDs must be unique")
    if markdown != methodology_markdown(registry):
        raise ValueError("Methodology Markdown differs from JSON; regenerate explicitly")
    known = {m["id"] for m in registry["measures"]}
    if any(not set(f["series"]).issubset(known) for f in registry["figures"]):
        raise ValueError("Unknown measure reference")


def plot_figures(paired, base_date, out, run_id, version, config):
    # NaN at every excluded/absent class observation; do not bridge known gaps.
    dates, series = [], {k: [] for k in ("discount_pct", "common_index", "preferred_index")}
    previous = None
    for row in paired:
        t = date.fromisoformat(row["datadate"])
        if previous and (t-previous).days > config["long_gap_days"]:
            dates.append(previous+timedelta(days=1))
            for values in series.values():
                values.append(np.nan)
        dates.append(t)
        for key in series:
            series[key].append(row[key] if row[key] is not None else np.nan)
        previous = t
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "svg.hashsalt": "samsung-e01"})
    for panels, stem in ((1, "discount_history"),):
        fig, axes = plt.subplots(panels, 1, figsize=(13, 5.3 if panels==1 else 8.3), sharex=True, squeeze=False)
        ax = axes[0, 0]
        ax.plot(dates, series["discount_pct"], color="#176678", linewidth=1.05)
        ax.axhline(0, color="#707070", linewidth=.7)
        ax.set_ylabel("Preferred discount (%)")
        values = [v for v in series["discount_pct"] if math.isfinite(v)]
        ax.set_ylim(min(0, min(values))-2, max(values)+3)
        fig.suptitle("Samsung Electronics common and preferred shares", fontsize=17, x=.08, ha="left", y=.97)
        ax.set_title("Observed discount = 100 × (1 − preferred raw close / common raw close)", loc="left", fontsize=11, pad=13)
        if panels == 2:
            lower = axes[1, 0]
            lower.plot(dates, series["common_index"], color="#234e80", label="Common 005930", linewidth=1)
            lower.plot(dates, series["preferred_index"], color="#b15e20", label="Preferred 005935", linewidth=1)
            lower.set_ylabel("Split-adjusted price index")
            lower.set_title(f"Each class = 100 on {base_date} · price only, excludes dividends", loc="left", fontsize=11, pad=10)
            lower.legend(loc="upper left", frameon=False, ncol=2)
        for axis in axes[:, 0]:
            axis.grid(axis="y", alpha=.18)
            axis.axvline(date.fromisoformat(config["split_first_trading_date"]), color="#888888", linestyle="--", linewidth=.8)
            axis.xaxis.set_major_locator(mdates.YearLocator(2))
            axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
            axis.set_xlim(dates[0], dates[-1])
        ax.text(date.fromisoformat(config["split_first_trading_date"]), .98, " 50:1 split · May 2018", transform=ax.get_xaxis_transform(), fontsize=9, va="top", color="#666666")
        axes[-1, 0].set_xlabel("Korean local observation date")
        footer = (f"WRDS Compustat Global · {base_date} to {paired[-1]['datadate']} · same-date valid pairs; excluded rows are gaps\n"
                  f"Status 10; vendor definitions supplied by user · observed gap is not identified vote value\n"
                  f"E01 / {stem} · methodology {version} · run {run_id}")
        fig.text(.08, .018, footer, fontsize=8.2, va="bottom", color="#4a4a4a", linespacing=1.5)
        fig.subplots_adjust(left=.08, right=.98, top=.86 if panels==1 else .89, bottom=.23 if panels==1 else .16, hspace=.28)
        for extension in ("png", "svg"):
            fig.savefig(out/f"{stem}.{extension}", dpi=170, facecolor="white")
        plt.close(fig)


def render_report(summary, coverage, diagnostics, run_id, raw_hash, version):
    s = summary
    lines = ["# Samsung raw-price discount coverage and validation", "",
             f"Run `{run_id}`; methodology {version}. Raw SHA-256 `{raw_hash}` verified unchanged.", "",
             f"Actual matched coverage: **{s['first_valid']} to {s['last_valid']}**. {s['raw_rows']:,} raw rows, {s['raw_fields']} fields, {s['raw_issues']} issues; {s['selected_rows']:,} local-class rows. Other listings excluded: {s['other_issue_rows']:,} rows.",
             f"Zero duplicate keys. {s['union_dates']:,} union dates, **{s['matched_valid_dates']:,} matched valid price dates**, {s['excluded_union_dates']} excluded union dates. No adjusted-price/index observations calculated.", "",
             "## Class coverage", "", "| Class | Rows | Valid prices | Status 10 | Carried status 5 | Missing closes | Volume review flags |", "|---|---:|---:|---:|---:|---:|---:|"]
    for label, q in s["classes"].items():
        lines.append(f"| {label} | {q['rows']} | {q['price_eligible']} | {q['statuses'].get('10',0)} | {q['statuses'].get('5',0)} | {q['missing_close']} | {q['volume_review']} |")
    lines += ["", "## Definitions and filters", "",
              "User supplied vendor PRCSTD, CSHTRD and QUNIT documentation, saved in `docs/reference/data/WRDS_VENDOR_DEFINITIONS.md` and source inventory. This is documentation supplied in chat, not a vendor page independently retrieved. All selected rows are gvkey 104604, preferred 01W/KR7005931001/type 1 and common 02W/KR7005930003/type 0, exchange 248, KRW; descriptors match the existing issuer mapping.",
              "QUNIT=1 verified across every selected row; raw PRCCD is KRW per share. General per-share conversion is PRCCD/QUNIT. Missing/nonpositive/unsupported units are rejected, not filled. Discount = 100*(1-preferred_raw_close/common_raw_close) on the same valid local date.",
              "Accept finite positive raw close, status 10, QUNIT=1, weekday and consistent available low/high. Status 5 means carried forward and is excluded. Other status codes are not automatically accepted for this pair. Non-US CSHTRD is actual shares at individual-exchange issue level. Missing volume is a review flag, NOT an eligibility exclusion: vendor status 10 can arise from a changed price without volume. Unchanged status-10 quotes are retained; unchanged is not automatically stale.",
              "Full field-level missingness and nonmissing coverage: `field_coverage.csv`. Every selected source row and flag: `normalized_market.csv`. Date alignment and gaps: `paired_daily.csv`. No price filling, winsorization, smoothing, dividend adjustment or calendar inference.", "",
              "## Remaining measurement flags", "",
              f"{s['unclassified_absent_weekdays']} weekdays are absent from both classes; see `unclassified_absent_weekdays.csv`. These are not asserted missing exchange sessions. An independent KRX calendar is still needed. Union-date exclusions and intervals over 10 calendar days are chart gaps.",
              "The common 2012-10-03 code-5 row has reported volume/high/low; the supplied vendor definition makes this an internal data inconsistency to reconcile, not permission to ignore the carried flag. It remains excluded.",
              f"{s['discontinuity_flags']} review dates exceed 5 percentage-point discount change or 10 calendar-day interval. See `discontinuity_review.csv`. These observations are retained; independent quote/event/calendar reconciliation is pending. No adjusted-return review was performed.",
              "AJEXDI values and split markers are inventoried in `factor_events.json` and `split_window.csv`. The supplied AJEXDI text refers to an underlying company-factor definition not provided. **Adjustment formula unresolved; split-adjusted panel, price indexes, adjusted returns and total-return wealth deferred.** The existence of a split marker does not settle the complete adjustment rule. Archived v1 panels are superseded for current use.", "",
              "## Descriptive results", "",
              f"First discount {s['first_discount_pct']:.2f}%; endpoint {s['last_discount_pct']:.2f}%; equal-observation median {s['median_discount_pct']:.2f}%. Minimum {s['minimum']['discount_pct']:.2f}% on {s['minimum']['datadate']}; maximum {s['maximum']['discount_pct']:.2f}% on {s['maximum']['datadate']}.",
              "Observed price gaps are not identified causal values of votes. Cash-flow rights, liquidity, flows, supply and arbitrage constraints remain competing explanations. No predictive model, regression, significance test or backtest was run.", "",
              "## Reproducibility and source comparison", "",
              "`discount_history.png` and `.svg` are the only figures in this run. Reproduce with `.venv/Scripts/python.exe scripts/run_samsung_e01.py`. Input hashes, exact code/environment, schema-validated methodology, supplied definitions and passing validation log are archived in this unique ignored run directory. Raw and derived licensed data remain untracked; no publication is authorized.",
              "`overlap_revision_summary.json` compares the old and extended extracts field by field. The old file and prior run directories are preserved. Observation dates are not availability dates; export retrieval, query settings and revision vintage remain unspecified.", "",
              "## Remaining data needs and future factors", "",
              "Independent KRX sessions/suspensions and raw price checks on extrema/jump dates; explanation of the contradictory code-5 row; exchange/type reference tables and export metadata; complete rights/actions and underlying company adjustment-factor formula. PRCSTD, CSHTRD and QUNIT meanings are now supplied and need not be requested again.",
              "Barra and Fama-French loaders were inspected locally; future regressions are recorded in `docs/FACTOR_RESEARCH_NOTES.md`. Their model geography, units, factor dates and Korean-close alignment need verification before use. No factor-data pull or regression was run."]
    return "\n".join(lines)+"\n"


def git(*args):
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.stdout.strip() if p.returncode == 0 else "unavailable: " + p.stderr.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/samsung_e01.json")
    parser.add_argument("--raw")
    parser.add_argument("--output-root")
    parser.add_argument("--sync-methodology", action="store_true")
    args = parser.parse_args()
    config = read_json(ROOT/args.config)
    registry = read_json(ROOT/config["methodology_path"])
    schema = read_json(ROOT/"methodology/schema.json")
    md_path = ROOT/"docs/METHODOLOGY.md"
    if args.sync_methodology:
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(registry)
        md_path.write_text(methodology_markdown(registry), encoding="utf-8")
        print("Synchronized methodology Markdown from canonical JSON")
        return
    validate_registry(registry, schema, md_path.read_text(encoding="utf-8"))
    raw = (ROOT/(args.raw or config["raw_path"])).resolve()
    outroot = (ROOT/(args.output_root or config["output_root"])).resolve()
    run_id = datetime.now(timezone.utc).strftime("samsung_E01_%Y%m%dT%H%M%S_%fZ")
    out = outroot/run_id
    out.mkdir(parents=True, exist_ok=False)
    input_hash = sha256(raw)
    manifest = {"run_id": run_id, "started_at_utc": datetime.now(timezone.utc).isoformat(), "status": "running",
                "experiment": "E01", "config_version": config["version"], "methodology_version": registry["methodology_version"],
                "input_path": str(raw), "input_sha256_before": input_hash, "source_ids": registry["context"]["dataset_ids"],
                "git_commit": git("rev-parse", "HEAD"), "dirty_status": git("status", "--short"),
                "entry_point": "scripts/run_samsung_e01.py", "command": sys.argv, "seed": None,
                "warnings": registry["context"]["limitations"], "patch_reference": "worktree.patch plus code_snapshot/", "outputs": []}
    try:
        source = read_json(ROOT/"research/source_inventory.json")
        source_entry = next(s for s in source["sources"] if s["id"] == config["source_id"])
        expected_hash = source_entry["sha256"]
        manifest["registered_input_hash_matches"] = input_hash == expected_hash
        if raw == (ROOT/config["raw_path"]).resolve() and input_hash != expected_hash:
            raise ValueError("Configured raw source differs from registered immutable hash")
        write_json(out/"config.json", config)
        write_json(out/"methodology.json", registry)
        write_json(out/"methodology_schema.json", schema)
        write_json(out/"source_inventory.json", source)
        (out/"METHODOLOGY.md").write_text(md_path.read_text(encoding="utf-8"), encoding="utf-8")
        (out/"worktree.patch").write_text(git("diff", "--binary", "HEAD"), encoding="utf-8")
        # Include untracked research implementation in snapshots: git diff alone omits it.
        snapshots = [*sorted((ROOT/"src/samsung_research").glob("*.py")), *sorted((ROOT/"tests").glob("check_*.py")), ROOT/"scripts/run_samsung_e01.py", ROOT/"uv.lock", ROOT/"pyproject.toml", ROOT/"research/requirements.txt", ROOT/"research/requirements.lock"]
        manifest["code_and_environment_hashes"] = {}
        for path in snapshots:
            relative = path.relative_to(ROOT)
            target = out/"code_snapshot"/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
            manifest["code_and_environment_hashes"][relative.as_posix()] = sha256(path)
        environment = {"python": sys.version, "platform": platform.platform(),
                       "packages": dict(sorted((d.metadata["Name"], d.version) for d in importlib.metadata.distributions() if d.metadata["Name"]))}
        write_json(out/"environment.json", environment)
        checks = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "check_*.py"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (out/"validation.txt").write_text(checks.stdout+checks.stderr, encoding="utf-8")
        manifest["validation"] = {"command": "python -m unittest discover -s tests -p check_*.py", "exit_code": checks.returncode}
        if checks.returncode:
            raise RuntimeError("Research validation checks failed; see validation.txt")
        fields, rows, selected, normalized = load_and_validate(raw, config)
        old_path = ROOT/config["previous_raw_path"]
        old_hash_before = sha256(old_path)
        with old_path.open(newline="", encoding="utf-8-sig") as f:
            old_rows = list(csv.DictReader(f))
        key = lambda r: (r["gvkey"], r["iid"], r["datadate"])
        old_map, new_map = ({key(r): r for r in rs} for rs in (old_rows, rows))
        overlap = old_map.keys() & new_map.keys()
        revisions = [{"key": list(k), "fields": [f for f in fields if old_map[k].get(f) != new_map[k].get(f)]}
                     for k in sorted(overlap) if old_map[k] != new_map[k]]
        write_json(out/"overlap_revision_summary.json", {"old_path": str(old_path), "old_sha256_before": old_hash_before,
                   "old_sha256_after": sha256(old_path), "overlap_rows": len(overlap), "revised_rows": len(revisions),
                   "old_keys_absent_new": len(old_map.keys()-new_map.keys()), "new_keys_added": len(new_map.keys()-old_map.keys()), "revisions": revisions})
        if sha256(old_path) != old_hash_before:
            raise RuntimeError("Old raw input changed")
        (out/"WRDS_VENDOR_DEFINITIONS.md").write_bytes((ROOT/"docs/reference/data/WRDS_VENDOR_DEFINITIONS.md").read_bytes())
        paired, base_date = match_pair(normalized, config)
        summary, inventory, coverage, diagnostics, absent = audit(fields, rows, selected, normalized, paired, config)
        write_json(out/"summary.json", summary)
        write_json(out/"factor_events.json", summary["factor_events"])
        write_csv(out/"issue_inventory.csv", inventory)
        write_csv(out/"field_coverage.csv", coverage)
        write_csv(out/"normalized_market.csv", normalized)
        write_csv(out/"paired_daily.csv", paired)
        write_csv(out/"discontinuity_review.csv", diagnostics)
        write_csv(out/"unclassified_absent_weekdays.csv", absent)
        write_csv(out/"split_window.csv", [r for r in normalized if "2018-04-25"<=r["datadate"]<="2018-05-08"])
        plot_figures(paired, base_date, out, run_id, registry["methodology_version"], config)
        after = sha256(raw)
        if after != input_hash:
            raise RuntimeError("Raw input bytes changed during analysis")
        manifest["input_sha256_after"] = after
        manifest["base_date"] = base_date
        manifest["coverage"] = summary
        (out/"DATA_QUALITY_REPORT.md").write_text(render_report(summary, coverage, diagnostics, run_id, input_hash, registry["methodology_version"]), encoding="utf-8")
        manifest["status"] = "completed_with_documented_validation_limitations"
    except Exception:
        manifest["status"] = "failed"
        (out/"failure.txt").write_text(traceback.format_exc(), encoding="utf-8")
        raise
    finally:
        manifest["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        manifest["outputs"] = [{"path": p.relative_to(out).as_posix(), "sha256": sha256(p)} for p in sorted(out.rglob("*")) if p.is_file() and p.name != "manifest.json"]
        write_json(out/"manifest.json", manifest)
        print(str(out))


if __name__ == "__main__":
    main()
