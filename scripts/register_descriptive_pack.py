"""Register the user-authorized descriptive pack before executing it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
from samsung_research.e01 import ROOT, read_json, write_json, methodology_markdown


def main():
    m = read_json(ROOT/"methodology/methodology.json")
    if m["methodology_version"].startswith("3."):
        print("Descriptive pack already registered")
        return
    if m["methodology_version"] != "2.0.0":
        raise ValueError("Review migration against current methodology before proceeding")
    m["methodology_version"] = "3.0.0"
    c = m["context"]
    c["purpose"] = "EP01 six-figure descriptive pack with flagged episodes and exclusion sensitivity; E01 ingestion reused. No returns, regressions or backtests."
    c["configuration"] = "configs/samsung_descriptive.json plus configs/samsung_e01.json"
    c["calendar"] = "Session proxy: union of dates with at least one eligible local quote. Missing pairs retained on this grid. Both-carried/absent-both dates are not assumed sessions. Independent KRX calendar unavailable. Full vendor union dates and absent-both weekdays used to break plotted lines."
    c["sample"] = "Full available 2005-2026 sample; raw-price panels since 2019-01-01. Main retains eligible flagged observations; sensitivity masks all flagged dates before summary, differences and rolling calculations, without dropping grid rows. No price or volume fill."
    c["windows"] = "Adjacent observed-session discount differences. Trailing 20 session-endpoint changes, sample standard deviation ddof=1, minimum 20 finite changes, no annualization. Thus requires 21 valid consecutive price observations. No lookahead or centered window. Yearly equal-observation boxplots; 2026 partial through input end."
    for decision in m["decisions"]:
        if decision["id"] in ("D001", "D002"):
            decision["status"] = "superseded"
            decision["decision"] += " Superseded by D005/D006; retained only as decision history."
    specs = [
        ("discount_change", "Daily observed-session discount change", "delta_d(t)=d(t)-d(t-1) on original observed-session proxy grid; missing if either endpoint missing or masked", "d=preferred discount in percent; t-1=adjacent proxy session, not previous surviving row", "percentage points", ["preferred_discount"], "20% to 21.5% gives +1.5pp, not a 7.5% return.", ["Not a security return", "Calendar gaps may span holidays or unobserved sessions"]),
        ("annual_distribution", "Annual discount distribution", "Group finite unmasked d(t) by local calendar year. Median and Q1/Q3 use numpy linear quantiles; Tukey whiskers are most extreme observed values inside Q1-1.5*IQR and Q3+1.5*IQR, outliers shown individually. Equal observation weights.", "IQR=Q3-Q1; year from local datadate", "percent; count in observations", ["preferred_discount"], "[10,20,30] has median 20, Q1=15 and Q3=25.", ["Unequal annual coverage; last year partial", "Serial observations are not independent evidence"]),
        ("raw_close_panels", "Contemporaneous raw closing quotes", "C(t)=PRCCD_common/QUNIT_common; P(t)=PRCCD_preferred/QUNIT_preferred; require QUNIT=1 here. Plot separately since 2019-01-01 using each class's own eligibility, shared date axis.", "C/P are raw per-share KRW closes, not returns or adjusted indexes", "KRW per share", ["prccd", "qunit", "prcstd"], "PRCCD=50000 and QUNIT=1 means KRW50000 per share.", ["Not total-return performance", "History before raw-panel start not displayed"]),
        ("volume_activity", "Class trading volumes and volume ratio", "V_j(t)=CSHTRD_j(t) for eligible own-class quote and finite nonnegative volume. Ratio=V_preferred/V_common only if both volumes finite, preferred>=0 and common>0. Missing and flagged dates never filled. Raw volumes plotted in millions of shares over full history.", "j=common or preferred; non-US vendor issue/exchange-level actual shares", "millions of shares; dimensionless ratio", ["cshtrd", "prcstd", "datadate"], "Preferred volume=200 and common=1000 gives ratio 0.2. Common=0 makes ratio missing.", ["Trading activity does not establish relative liquidity", "Raw share counts change with splits; pre/post split volume levels not directly comparable", "No turnover or free-float normalization"]),
        ("rolling_discount_volatility", "20-session discount-change volatility", "sigma(t)=sqrt(sum((delta_d(s)-mean(delta_d))^2)/19) for s=t-19,...,t on original session grid; require all 20 changes finite. Unannualized, trailing, no grid compression.", "delta_d in percentage points; 20 change endpoints need 21 prices", "percentage points", ["discount_change"], "Twenty alternating changes +1,-1 have sample std sqrt(20/19). A missing change anywhere makes the window missing.", ["Instability of the gap, not stock-return volatility", "Observed session proxy pending calendar validation"]),
        ("flag_sensitivity", "Flag-exclusion sensitivity", "Mask dates flagged by >5pp audit change, >10-calendar-day adjacent valid gap, carried status with positive volume, asymmetric source rows, or absent-both weekdays. Keep same original session and plot grids. Recalculate annual summaries/differences/windows after masking. Context split marker and top-ten display highlights are not exclusions.", "Flags from unchanged E01 audit plus explicit source-row/calendar concerns; baseline includes otherwise valid flagged observations", "date masks; no numeric scale", ["quality_audit", "preferred_discount"], "For [10,11,12] with middle price flagged, sensitivity changes at second AND third endpoints are missing; never compute 12-10 as one daily change.", ["Outcome-based review thresholds make this a diagnostic sensitivity, not proof that excluded values are wrong", "Many flagged dates are already ineligible, so exclusions may not affect annual counts"]),
        ("episode_review", "Local inspection of flagged dates", "For each audit flag, inspect 10 observed sessions before/after and export original class rows in a +/-20-calendar-day envelope; show four eligible flagged-date discount windows. List code/volume conflicts, asymmetric rows and absent-both dates separately. No causal event attribution.", "Window bounds clipped to actual data; no interpolation", "percent, KRW and shares as labeled", ["quality_audit", "prccd", "prcstd", "cshtrd"], "A code-5 close with positive volume stays excluded and is documented as an unresolved vendor inconsistency.", ["Local consistency is not independent price verification", "No event-date explanation inferred from nearby movement"]),
    ]
    for mid, name, formula, symbols, unit, inputs, example, limitations in specs:
        m["measures"].append(dict(id=mid,name=name,version="1.0.0",status="implemented",author="Codex",hypothesis_ids=["H0","H3","H7"] if mid=="volume_activity" else ["H0","H7"],formula=formula,symbols=symbols,unit=unit,sign_convention="As defined in formula; positive discount change means widening",inputs=inputs,example=example,limitations=limitations,implementation_ref="src/samsung_research/descriptive.py:build_measures"))
    plots = [
        ("EP01_F01","Discount history with flags","01_discount_history",["preferred_discount","flag_sensitivity"],"Daily unsmoothed discount, red markers on eligible analytical-review dates; amber rug for source/calendar flags; split context dashed. Same sample and limits for main/sensitivity."),
        ("EP01_F02","Annual discount distributions","02_annual_distributions",["annual_distribution"],"Annual Tukey boxplots, visible outliers, orange median overlay; partial endpoint year marked *. Show per-year counts in table. Same y limits across variants."),
        ("EP01_F03","Daily discount changes","03_daily_discount_changes",["discount_change","flag_sensitivity"],"Vertical stems around zero; red markers on ten largest absolute finite changes ranked per variant, annotations for three largest. Missing changes remain absent. Units percentage points."),
        ("EP01_F04","Recent common and preferred raw closes","04_raw_closes_since_2019",["raw_close_panels","flag_sensitivity"],"Two aligned own-class price panels since 2019, same KRW y scale, no ratios/indexes/return interpretation; flagged valid quotes red."),
        ("EP01_F05","Class trading activity","05_trading_activity",["volume_activity","flag_sensitivity"],"Three aligned panels: common and preferred raw shares in millions, ratio preferred/common on its own linear axis. Split context. Label explicitly as activity, not liquidity."),
        ("EP01_F06","Rolling discount-change volatility","06_rolling_discount_volatility",["rolling_discount_volatility","flag_sensitivity"],"Trailing 20 observed-session sample standard deviation of daily discount changes, unannualized pp, no centered windows; gaps visible including sensitivity-window loss."),
        ("EP01_F07","Flagged episode windows","flagged_discount_windows",["episode_review"],"2x2 local discount windows around the four audit dates; no causal labels. Other source/calendar flags documented in tables and review report.")]
    for fid,name,stem,series,spec in plots:
        outputs = [f"figures/{variant}/{stem}.{ext}" for variant in ("main","sensitivity") for ext in ("png","svg")] if fid!="EP01_F07" else [f"episodes/{stem}.{ext}" for ext in ("png","svg")]
        m["figures"].append(dict(id=fid,name=name,version="1.0.0",status="implemented",author="Codex",hypothesis_ids=["H0","H3","H7"] if fid=="EP01_F05" else ["H0","H7"],series=series,specification=spec,output_ids=outputs,implementation_ref="src/samsung_research/descriptive.py:plot_pack"))
    m["decisions"].append(dict(id="D007",owner="Codex",status="adopted",decision="User authorizes six descriptive graphs plus flagged-date sensitivity and episode inspection. Use session proxy, pp changes and unannualized trailing change volatility; log all files and group new runs. Earlier run paths stay immutable; no factors/returns."))
    m["change_log"].append(dict(version="3.0.0",previous_version="2.0.0",date="2026-10-22",reason="User requests descriptive figure pack, flagged-date sensitivity and navigable output log",initiating_decision="D007",affected_experiments=["EP01"],prior_outputs_need_rerun=False))
    write_json(ROOT/"methodology/methodology.json",m)
    (ROOT/"docs/METHODOLOGY.md").write_text(methodology_markdown(m),encoding="utf-8")
    print("Registered methodology 3.0.0 and generated matching Markdown")

if __name__ == "__main__":
    main()
