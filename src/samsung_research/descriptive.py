"""EP01: descriptive Samsung figures, explicit session grids, and sensitivity."""
from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
import math
import shutil
import subprocess
import sys
import traceback
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import numpy as np

from .e01 import (ROOT, audit, git, load_and_validate, match_pair, number,
                  positive, read_json, sha256, validate_registry, write_csv, write_json)

STEMS = ["01_discount_history", "02_annual_distributions", "03_daily_discount_changes",
         "04_raw_closes_since_2019", "05_trading_activity", "06_rolling_discount_volatility"]
TITLES = ["Observed preferred-share discount", "Annual preferred-discount distributions",
          "Daily discount changes", "Common and preferred raw closes since 2019",
          "Trading activity by share class", "20-session discount-change volatility"]


def difference(values):
    a = np.asarray(values, dtype=float)
    return np.r_[np.nan, np.diff(a)]


def rolling_std(values, window=20):
    a = np.asarray(values, dtype=float)
    out = np.full(len(a), np.nan)
    for i in range(window-1, len(a)):
        block = a[i-window+1:i+1]
        if np.isfinite(block).all():
            out[i] = np.std(block, ddof=1)
    return out


def volume_ratio(preferred, common):
    p, c = number(preferred), number(common)
    return p/c if p is not None and p >= 0 and c is not None and c > 0 else np.nan


def finite_or_nan(value):
    return float(value) if value is not None else np.nan


def build_measures(normalized, paired, diagnostics, absent, config):
    byclass = {j: {r["datadate"]: r for r in normalized if r["class_name"] == j} for j in ("common","preferred")}
    bydate = {r["datadate"]: r for r in paired}
    flags = defaultdict(set)
    for r in diagnostics:
        flags[r["date"]].update(r["review_flags"].split(";"))
    for r in normalized:
        if r["prcstd"] == "5" and positive(r["cshtrd"]):
            flags[r["datadate"]].add("carried_with_positive_volume")
    for t in bydate:
        if any(t not in byclass[j] for j in byclass):
            flags[t].add("asymmetric_source_rows")
    for r in absent:
        flags[r["date"]].add("absent_both_weekday_unclassified")
    grid = sorted(set(bydate) | set(flags))
    sessions = [t for t in grid if any(byclass[j].get(t,{}).get("price_eligible",False) for j in byclass)]
    results = {}
    annual = []
    for variant in ("main","sensitivity"):
        session_levels = np.array([finite_or_nan(bydate[t]["discount_pct"]) if not (variant=="sensitivity" and t in flags) else np.nan for t in sessions])
        changes = difference(session_levels)
        volatility = rolling_std(changes,config["window_sessions"])
        session_map = {t:(changes[i],volatility[i]) for i,t in enumerate(sessions)}
        records = []
        for t in grid:
            masked = variant=="sensitivity" and t in flags
            record = dict(date=t, observed_session=t in session_map, flagged=t in flags,
                          flag_reasons=";".join(sorted(flags.get(t,[]))), sensitivity_masked=masked,
                          discount_pct=finite_or_nan(bydate.get(t,{}).get("discount_pct")) if not masked else np.nan,
                          discount_change_pp=session_map.get(t,(np.nan,np.nan))[0],
                          rolling_change_std_pp=session_map.get(t,(np.nan,np.nan))[1])
            for j in byclass:
                r = byclass[j].get(t)
                eligible = r is not None and r["price_eligible"] and not masked
                record[j+"_raw_close"] = float(r["prccd"]) if eligible else np.nan
                v = number(r["cshtrd"]) if eligible else None
                record[j+"_volume"] = v if v is not None and v>=0 else np.nan
            record["volume_ratio"] = volume_ratio(record["preferred_volume"],record["common_volume"])
            records.append(record)
        results[variant] = records
        for year in sorted({t[:4] for t in grid}):
            values = [r["discount_pct"] for r in records if r["date"].startswith(year) and math.isfinite(r["discount_pct"])]
            if values:
                q1, med, q3 = np.quantile(values,[.25,.5,.75],method="linear")
                annual.append(dict(variant=variant, year=int(year), observations=len(values),
                                   minimum=min(values), q1=float(q1), median=float(med), q3=float(q3), maximum=max(values),
                                   partial_endpoint_year=year==grid[-1][:4] and grid[-1][5:]!="12-31"))
    return results, dict(flags), annual


def csv_clean(rows):
    return [{k:(None if isinstance(v,(float,np.floating)) and not math.isfinite(v) else v) for k,v in row.items()} for row in rows]


def summary_stats(results, annual):
    out = {}
    for variant, rows in results.items():
        valid = [r for r in rows if math.isfinite(r["discount_pct"])]
        change = [r for r in rows if math.isfinite(r["discount_change_pp"])]
        roll = [r for r in rows if math.isfinite(r["rolling_change_std_pp"])]
        top = sorted(change,key=lambda r:abs(r["discount_change_pp"]),reverse=True)[:10]
        out[variant] = dict(discount_observations=len(valid), change_observations=len(change), rolling_observations=len(roll),
                            median_discount_pct=float(np.median([r["discount_pct"] for r in valid])),
                            largest_changes=[dict(date=r["date"],change_pp=r["discount_change_pp"],flagged=r["flagged"]) for r in top],
                            highest_rolling_std=dict(date=max(roll,key=lambda r:r["rolling_change_std_pp"])["date"],std_pp=max(r["rolling_change_std_pp"] for r in roll)) if roll else None,
                            annual=[r for r in annual if r["variant"]==variant])
    return out


def setup_axes(axes, dates):
    for ax in np.atleast_1d(axes).ravel():
        ax.spines[["top","right"]].set_visible(False)
        ax.grid(axis="y",alpha=.18)
        ax.xaxis.set_major_locator(mdates.YearLocator(2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.set_xlim(dates[0],dates[-1])


def mark_flags(ax, dates, values, rows, rug=False):
    idx = [i for i,r in enumerate(rows) if r["flagged"] and math.isfinite(values[i])]
    if idx:
        ax.scatter([dates[i] for i in idx],[values[i] for i in idx],s=25,color="#ba362c",zorder=5,label="Review flag")
    if rug:
        uncertain = [dates[i] for i,r in enumerate(rows) if r["flagged"] and not math.isfinite(values[i])]
        if uncertain:
            ax.plot(uncertain,[.025]*len(uncertain),"|",transform=ax.get_xaxis_transform(),color="#bf8a32",markersize=5,label="Source/calendar flag")


def save_plot(fig, out, stem, title, variant, run_id, number_id, note):
    fig.suptitle(title+" — "+("main sample" if variant=="main" else "flag-exclusion sensitivity"),x=.08,ha="left",fontsize=15,y=.97)
    version=read_json(ROOT/"methodology/methodology.json")["methodology_version"]
    fig.text(.08,.025,note+f"\nEP01_F{number_id:02d} · method {version} · {run_id}",fontsize=8,color="#555555",va="bottom",linespacing=1.45)
    fig.subplots_adjust(left=.08,right=.98,top=.87,bottom=.20,hspace=.3)
    for ext in ("png","svg"):
        fig.savefig(out/f"{stem}.{ext}",dpi=150,facecolor="white")
    plt.close(fig)


def plot_pack(results, annual, out, run_id, config):
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"svg.hashsalt":"samsung-EP01"})
    main = results["main"]
    all_level = [r["discount_pct"] for r in main if math.isfinite(r["discount_pct"])]
    max_change = max(abs(r["discount_change_pp"]) for r in main if math.isfinite(r["discount_change_pp"]))
    max_vol = max(r["rolling_change_std_pp"] for r in main if math.isfinite(r["rolling_change_std_pp"]))
    for variant, rows in results.items():
        target = out/"figures"/variant
        target.mkdir(parents=True,exist_ok=True)
        dates = [date.fromisoformat(r["date"]) for r in rows]
        y = [r["discount_pct"] for r in rows]
        common_note = f"WRDS Compustat Global · {rows[0]['date']}–{rows[-1]['date']} · observed preferred discount, not identified vote value"
        mask_note = "Flags retained; excluded source observations remain gaps." if variant=="main" else "Flagged dates masked on original grids; no bridging or compressed rolling windows."
        fig,ax = plt.subplots(figsize=(13,5.8))
        ax.plot(dates,y,color="#176678",linewidth=.9,label="Observed discount")
        mark_flags(ax,dates,y,rows,rug=True)
        ax.axvline(date(2018,5,4),linestyle="--",color="#888888",linewidth=.8)
        ax.text(date(2018,5,4),.97," 50:1 split (context)",transform=ax.get_xaxis_transform(),va="top",fontsize=8,color="#666666")
        ax.axhline(0,color="#888888",linewidth=.6)
        ax.set_ylim(-2,max(all_level)+4)
        ax.set_ylabel("Preferred discount (%)")
        setup_axes(ax,dates)
        ax.legend(frameon=False,loc="upper right",fontsize=8)
        save_plot(fig,target,STEMS[0],TITLES[0],variant,run_id,1,common_note+"\n"+mask_note)

        years = sorted({int(r["date"][:4]) for r in rows})
        groups = [[r["discount_pct"] for r in rows if int(r["date"][:4])==year and math.isfinite(r["discount_pct"])] for year in years]
        fig,ax=plt.subplots(figsize=(13,6))
        ax.boxplot(groups,positions=range(len(years)),widths=.6,whis=1.5,patch_artist=True,
                   boxprops=dict(facecolor="#d8e9ec",edgecolor="#176678"),medianprops=dict(color="#176678"),
                   flierprops=dict(marker=".",markersize=2,alpha=.4,markeredgecolor="#6c8d94"))
        ax.plot(range(len(years)),[np.median(v) if v else np.nan for v in groups],"o-",color="#b56522",markersize=3,linewidth=1,label="Annual median")
        ax.set_xticks(range(len(years)),[str(v)+("*" if v==years[-1] else "") for v in years],rotation=45,fontsize=8)
        ax.set_ylabel("Preferred discount (%)")
        ax.set_ylim(-2,max(all_level)+4)
        ax.grid(axis="y",alpha=.18)
        ax.spines[["top","right"]].set_visible(False)
        ax.legend(frameon=False)
        save_plot(fig,target,STEMS[1],TITLES[1],variant,run_id,2,common_note+"\n*Final year partial; 1.5-IQR whiskers and outliers shown. "+mask_note)

        changes=[r["discount_change_pp"] for r in rows]
        fig,ax=plt.subplots(figsize=(13,5.8))
        ax.vlines(dates,0,changes,color="#557c89",linewidth=.55,alpha=.75)
        top=sorted([i for i,v in enumerate(changes) if math.isfinite(v)],key=lambda i:abs(changes[i]),reverse=True)[:config["top_changes"]]
        ax.scatter([dates[i] for i in top],[changes[i] for i in top],s=22,color="#b63d30",zorder=4)
        ax.text(.01,.97,"Largest moves: "+"; ".join(f"{rows[i]['date']} {changes[i]:+.2f}pp" for i in top[:3]),transform=ax.transAxes,va="top",fontsize=8)
        ax.axhline(0,color="#777777",linewidth=.6)
        ax.set_ylim(-max_change*1.18,max_change*1.18)
        ax.set_ylabel("Discount change (percentage points)")
        setup_axes(ax,dates)
        save_plot(fig,target,STEMS[2],TITLES[2],variant,run_id,3,common_note+"\nAdjacent observed-session proxy dates only; red=ten largest absolute changes. "+mask_note)

        recent=[r for r in rows if r["date"]>=config["recent_start"]]
        rd=[date.fromisoformat(r["date"]) for r in recent]
        recent_main=[r for r in main if r["date"]>=config["recent_start"]]
        ceiling=max(r[j+"_raw_close"] for r in recent_main for j in ("common","preferred") if math.isfinite(r[j+"_raw_close"]))
        fig,axes=plt.subplots(2,1,figsize=(13,7.8),sharex=True)
        for ax,j,color in zip(axes,("common","preferred"),("#234e80","#b56522")):
            vals=[r[j+"_raw_close"] for r in recent]
            ax.plot(rd,vals,color=color,linewidth=.9)
            mark_flags(ax,rd,vals,recent)
            ax.set_ylabel(j.title()+" close (KRW)")
            ax.set_ylim(0,ceiling*1.08)
            ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
        setup_axes(axes,rd)
        save_plot(fig,target,STEMS[3],TITLES[3],variant,run_id,4,"Raw per-share quotes; own-class eligibility, shared KRW scale. Not adjusted prices or returns.\n"+mask_note)

        fig,axes=plt.subplots(3,1,figsize=(13,9),sharex=True)
        for ax,j,color in zip(axes[:2],("common","preferred"),("#234e80","#b56522")):
            vals=[r[j+"_volume"]/1e6 for r in rows]
            ax.plot(dates,vals,color=color,linewidth=.6)
            mark_flags(ax,dates,vals,rows)
            ax.set_ylabel(j.title()+" volume\n(million shares)")
            cap=max(r[j+"_volume"] for r in main if math.isfinite(r[j+"_volume"]))/1e6
            ax.set_ylim(0,cap*1.08)
            ax.axvline(date(2018,5,4),color="#888888",linestyle="--",linewidth=.7)
        ratios=[r["volume_ratio"] for r in rows]
        axes[2].plot(dates,ratios,color="#176678",linewidth=.7)
        axes[2].set_ylabel("Preferred/common\nvolume ratio")
        axes[2].set_ylim(0,max(r["volume_ratio"] for r in main if math.isfinite(r["volume_ratio"]))*1.08)
        setup_axes(axes,dates)
        save_plot(fig,target,STEMS[4],TITLES[4],variant,run_id,5,"Raw issue-level shares; dashed line=2018 split. Volume levels across splits require care.\nVolume ratio measures trading activity; it does not establish relative liquidity. "+mask_note)

        vols=[r["rolling_change_std_pp"] for r in rows]
        fig,ax=plt.subplots(figsize=(13,5.8))
        ax.plot(dates,vols,color="#70538a",linewidth=.9)
        mark_flags(ax,dates,vols,rows)
        ax.set_ylabel("20-session sample std (percentage points)")
        ax.set_ylim(0,max_vol*1.12)
        setup_axes(ax,dates)
        save_plot(fig,target,STEMS[5],TITLES[5],variant,run_id,6,"Volatility of discount changes, not security returns; trailing 20 observed-session changes, ddof=1, unannualized.\nRequires 20 finite changes on original grid (21 prices); no fill. "+mask_note)


def inspect_episodes(normalized, results, diagnostics, flags, out, run_id, config):
    target=out/"episodes"
    target.mkdir(exist_ok=True)
    main=results["main"]
    sessions=[r for r in main if r["observed_session"]]
    indexes={r["date"]:i for i,r in enumerate(sessions)}
    fig,axes=plt.subplots(2,2,figsize=(13,8))
    review=[]
    for ax,event in zip(axes.ravel(),diagnostics):
        i=indexes[event["date"]]
        w=sessions[max(0,i-config["episode_radius_sessions"]):i+config["episode_radius_sessions"]+1]
        # Bound by observed sessions, but retain every missing vendor/calendar
        # date inside the envelope so the close-up cannot bridge a known gap.
        w=[r for r in main if w[0]["date"]<=r["date"]<=w[-1]["date"]]
        dates=[date.fromisoformat(r["date"]) for r in w]
        ax.plot(dates,[r["discount_pct"] for r in w],color="#176678",marker=".",markersize=3,linewidth=1)
        center=sessions[i]
        ax.scatter([date.fromisoformat(center["date"])],[center["discount_pct"]],color="#ba362c",s=35,zorder=4)
        ax.set_title(event["date"]+" · "+event["review_flags"].replace("_"," "),fontsize=10)
        ax.set_ylabel("Discount (%)")
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3,maxticks=4))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.grid(alpha=.15)
        prior=sessions[i-1] if i else center
        review.append(dict(date=event["date"],previous_date=prior["date"],discount_before=prior["discount_pct"],discount_after=center["discount_pct"],change_pp=event["discount_change_pp"],
                           common_before=prior["common_raw_close"],common_after=center["common_raw_close"],preferred_before=prior["preferred_raw_close"],preferred_after=center["preferred_raw_close"],
                           calendar_days=event["calendar_days"],resolution="Both matched closes pass local status/unit/range checks. Independent prices/calendar/news not reconciled; no causal attribution."))
    fig.suptitle("Flagged discount episodes — local data inspection",x=.08,ha="left",fontsize=15)
    version=read_json(ROOT/"methodology/methodology.json")["methodology_version"]
    fig.text(.08,.025,"Red=review date; ±10 observed sessions, internal gaps retained. Local consistency is not independent verification.\nEP01_F07 · method "+version+" · "+run_id,fontsize=8,color="#555555")
    fig.subplots_adjust(left=.08,right=.98,top=.89,bottom=.14,wspace=.23,hspace=.35)
    for ext in ("png","svg"):
        fig.savefig(target/f"flagged_discount_windows.{ext}",dpi=150,facecolor="white")
    plt.close(fig)
    write_csv(target/"flagged_episode_comparison.csv",review)
    review_dates={r["date"] for r in diagnostics}|{r["datadate"] for r in normalized if r["prcstd"]=="5" and positive(r["cshtrd"])}
    selected=[]
    for event in sorted(review_dates):
        et=date.fromisoformat(event)
        selected.extend(dict(r,episode_date=event) for r in normalized if abs((date.fromisoformat(r["datadate"])-et).days)<=20)
    write_csv(target/"source_rows_around_flags.csv",selected)
    lines=["# Flagged episode inspection","","Local quote/status checks only; no independent price, exchange-calendar or news explanation asserted.","",
           "| Date | Prior date | Discount before → after | Change (pp) | Common raw close | Preferred raw close |","|---|---|---|---:|---|---|"]
    for r in review:
        lines.append(f"| {r['date']} | {r['previous_date']} | {r['discount_before']:.2f}% → {r['discount_after']:.2f}% | {r['change_pp']:+.2f} | {r['common_before']:,.0f} → {r['common_after']:,.0f} | {r['preferred_before']:,.0f} → {r['preferred_after']:,.0f} |")
    lines += ["","The 2008 widening/narrowing sequence is present in valid-status raw quotes; the rapid reversal remains an unresolved quote/event question. The 2015 move is also visible in both eligible class quotes. The 2017 interval spans 11 calendar days; no claim is made that it spans 11 trading sessions.","",
              "The 2012-10-03 common quote is code 5 despite positive volume/high/low. Both classes' ineligible quotes remain excluded; volume cannot override the status code. See exact raw rows in [source_rows_around_flags.csv](source_rows_around_flags.csv).", "",
              "All asymmetric-row dates and absent-both weekdays are in [flagged_dates.csv](../tables/flagged_dates.csv), including flags that affect no valid discount observation. Ordinary carried rows are exclusions, not automatically suspicious economic events.","",
              "Sensitivity removes review dates without closing the grid; changes using either endpoint and all affected 20-change windows become missing. This does not establish that the removed quotes are erroneous.","",
              "[Episode figure](flagged_discount_windows.png) · [Exact comparison table](flagged_episode_comparison.csv) · [Back to run](../README.md)"]
    (target/"REVIEW.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return review


def run_readme(out, run_id, stats, flags, annual, summary):
    a,b=stats["main"],stats["sensitivity"]
    version=read_json(ROOT/"methodology/methodology.json")["methodology_version"]
    lines=["# Samsung descriptive figure pack", "",f"Run `{run_id}` · methodology {version} · input through {summary['last_valid']}","",
           "Observed preferred discount, not estimated voting-right value. No return graphs, regressions or backtests.","",
           "## Figures","","| ID | Figure | Main | Flag-exclusion sensitivity |","|---|---|---|---|"]
    for i,(stem,title) in enumerate(zip(STEMS,TITLES),1):
        lines.append(f"| EP01_F{i:02d} | {title} | [PNG](figures/main/{stem}.png) · [SVG](figures/main/{stem}.svg) | [PNG](figures/sensitivity/{stem}.png) · [SVG](figures/sensitivity/{stem}.svg) |")
    lines += ["","## Coverage and sensitivity","",
              f"Main: {a['discount_observations']:,} matched discount observations; sensitivity: {b['discount_observations']:,}. Removed valid flagged observations: {a['discount_observations']-b['discount_observations']}. {len(flags)} distinct dates have a source/calendar/review flag, many already ineligible.",
              f"Daily-change observations: {a['change_observations']:,} main vs {b['change_observations']:,} sensitivity. Rolling-volatility observations: {a['rolling_observations']:,} vs {b['rolling_observations']:,}. Grids are identical; masking never bridges a removed date.",
              f"Full-sample medians: {a['median_discount_pct']:.4f}% main, {b['median_discount_pct']:.4f}% sensitivity. Annual boxplots use each year's finite observations; 2026 is partial. These are descriptive summaries, not fair-value estimates.","",
              "Twenty-session volatility means sample standard deviation of 20 discount changes, in percentage points, requiring 21 consecutive valid prices. Observed sessions are a proxy until an independent KRX calendar is supplied. Volume ratio measures activity, not liquidity. Full-history raw volume spans the split and is not split-adjusted.","",
              "## Inspection and exact tables","",
              "- [Flagged episode review](episodes/REVIEW.md) and [four local episode windows](episodes/flagged_discount_windows.png)",
              "- [Annual distributions](tables/annual_distributions.csv), [all flagged dates](tables/flagged_dates.csv), [largest changes](tables/largest_changes.csv)",
              "- [Main measures](tables/measures_main.csv), [sensitivity measures](tables/measures_sensitivity.csv), [numerical summary](tables/summary.json)",
              "- [Field coverage](tables/field_coverage.csv), [source-row inventory](tables/issue_inventory.csv), [raw-quality summary](tables/raw_quality.json)",
              "- [Manifest](manifest.json), [methodology](provenance/METHODOLOGY.md), [source inventory](provenance/source_inventory.json), [validation](provenance/validation.txt)","",
              "## Remaining inputs","",
              "Valuation: quarterly fundamentals, publication dates and class share counts. Buybacks: actual executions by class, announcements/cancellations separate. Liquidity: bid/ask, float and verified returns before price-impact measures. Shorting: fees, lendable inventory, utilization and class restrictions.",
              "Independent quotes/calendar, the contradictory carried row and the adjustment formula remain unresolved. Flags mark concerns, not established errors or causes. Raw files and older run directories are unchanged.","",
              "Reproduce from repository root: `.venv/Scripts/python.exe scripts/run_samsung_descriptive.py`. New runs are grouped under `runs/samsung/EP01_descriptive/`.","",
              "[Research log](../../../../docs/RESEARCH_LOG.md) · [Hypothesis tree](../../../../docs/HYPOTHESES.md) · [Runs index](../../../README.md)"]
    (out/"README.md").write_text("\n".join(lines)+"\n",encoding="utf-8")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--config",default="configs/samsung_descriptive.json")
    args=parser.parse_args()
    config=read_json(ROOT/args.config)
    pair_config=read_json(ROOT/config["pair_config"])
    registry=read_json(ROOT/"methodology/methodology.json")
    validate_registry(registry,read_json(ROOT/"methodology/schema.json"),(ROOT/"docs/METHODOLOGY.md").read_text(encoding="utf-8"))
    run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    out=ROOT/config["output_root"]/run_id
    out.mkdir(parents=True,exist_ok=False)
    for folder in ("tables","provenance","episodes"):
        (out/folder).mkdir()
    raw=ROOT/pair_config["raw_path"]
    before=sha256(raw)
    manifest=dict(run_id=run_id,experiment_id="EP01",started_at_utc=datetime.now(timezone.utc).isoformat(),status="running",
                  input_path=str(raw),input_sha256_before=before,methodology_version=registry["methodology_version"],
                  config_version=config["version"],git_commit=git("rev-parse","HEAD"),dirty_status=git("status","--short"),
                  entry_point="scripts/run_samsung_descriptive.py",command=sys.argv,seed=None,warnings=registry["context"]["limitations"])
    try:
        sources=read_json(ROOT/"research/source_inventory.json")
        source=next(s for s in sources["sources"] if s["id"]==pair_config["source_id"])
        if before!=source["sha256"]:
            raise ValueError("Raw source hash differs from registered immutable input")
        snapshots=[ROOT/args.config,ROOT/config["pair_config"],ROOT/"methodology/methodology.json",ROOT/"methodology/schema.json",ROOT/"docs/METHODOLOGY.md",ROOT/"research/source_inventory.json",ROOT/"research/requirements.lock",ROOT/"pyproject.toml",ROOT/"uv.lock",ROOT/"scripts/run_samsung_descriptive.py",*sorted((ROOT/"src/samsung_research").glob("*.py")),*sorted((ROOT/"tests").glob("check_*.py"))]
        for path in snapshots:
            target=out/"provenance"/"snapshot"/path.relative_to(ROOT)
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,target)
        shutil.copyfile(ROOT/"docs/METHODOLOGY.md",out/"provenance/METHODOLOGY.md")
        shutil.copyfile(ROOT/"research/source_inventory.json",out/"provenance/source_inventory.json")
        write_json(out/"provenance/environment.json",dict(python=sys.version,packages={d.metadata["Name"]:d.version for d in importlib.metadata.distributions() if d.metadata["Name"]}))
        (out/"provenance/worktree.patch").write_text(git("diff","--binary","HEAD"),encoding="utf-8")
        checks=subprocess.run([sys.executable,"-m","unittest","discover","-s","tests","-p","check_*.py"],cwd=ROOT,capture_output=True,text=True,encoding="utf-8",errors="replace")
        (out/"provenance/validation.txt").write_text(checks.stdout+checks.stderr,encoding="utf-8")
        if checks.returncode:
            raise RuntimeError("Validation failed; see provenance/validation.txt")
        manifest["validation_exit_code"]=checks.returncode
        fields,raw_rows,selected,normalized=load_and_validate(raw,pair_config)
        paired,_=match_pair(normalized,pair_config)
        quality,inventory,coverage,diagnostics,absent=audit(fields,raw_rows,selected,normalized,paired,pair_config)
        results,flags,annual=build_measures(normalized,paired,diagnostics,absent,config)
        stats=summary_stats(results,annual)
        write_json(out/"tables/raw_quality.json",quality)
        write_json(out/"tables/summary.json",stats)
        write_csv(out/"tables/annual_distributions.csv",annual)
        write_csv(out/"tables/field_coverage.csv",coverage)
        write_csv(out/"tables/issue_inventory.csv",inventory)
        write_csv(out/"tables/flagged_dates.csv",[dict(date=t,reasons=";".join(sorted(reasons)),main_discount_valid=any(r["date"]==t and math.isfinite(r["discount_pct"]) for r in results["main"])) for t,reasons in sorted(flags.items())])
        for variant,rows in results.items():
            write_csv(out/f"tables/measures_{variant}.csv",csv_clean(rows))
        write_csv(out/"tables/largest_changes.csv",[dict(variant=v,rank=i+1,**r) for v,s in stats.items() for i,r in enumerate(s["largest_changes"])])
        plot_pack(results,annual,out,run_id,config)
        inspect_episodes(normalized,results,diagnostics,flags,out,run_id,config)
        run_readme(out,run_id,stats,flags,annual,quality)
        after=sha256(raw)
        if before!=after:
            raise RuntimeError("Raw bytes changed")
        manifest.update(input_sha256_after=after,status="completed_with_documented_validation_limitations",summary=stats,
                        figure_ids=[f"EP01_F{i:02d}" for i in range(1,8)],figure_count=26)
    except Exception:
        manifest["status"]="failed"
        (out/"provenance/failure.txt").write_text(traceback.format_exc(),encoding="utf-8")
        raise
    finally:
        manifest["finished_at_utc"]=datetime.now(timezone.utc).isoformat()
        manifest["outputs"]=[dict(path=p.relative_to(out).as_posix(),sha256=sha256(p)) for p in sorted(out.rglob("*")) if p.is_file() and p.name!="manifest.json"]
        write_json(out/"manifest.json",manifest)
        print(out)
    from .navigation import record_run
    record_run(out)


if __name__=="__main__":
    main()
