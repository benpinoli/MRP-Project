> November5 continuation: this first locked evaluation is a checkpoint. Successive diagnostics and new-data/proxy tests are reported in [PREDICTION_CONTINUATION_REPORT.md](PREDICTION_CONTINUATION_REPORT.md). The current autonomous cycle ended after independent ranked exhaustion review; the research program remains open.

# Samsung discount forecasting: completed locked evaluation

The registered compact history model did **not establish a useful out-of-sample improvement**. Its one-session error reduction versus persistence is about 0.11%, uncertainty spans zero, and direct AR has a better point estimate. Five-session MAE worsens and twenty-session performance deteriorates materially. Retain persistence as the operational research benchmark; do not promote a forecasting or trading claim. This is a completed negative/inconclusive result, not a failure to execute.

## Execution and reproducibility

Research ran in `/home/bpinoli/MRP/MRP-Project` on BYU ORC, verified login03. Git revision `5c6f79091c00204da5f86b87a69648b4cdd67fe0`; `git pull --ff-only origin main` was already up to date and all existing staged/untracked work was preserved. Site instructions and seven applicable reference guides were read. Top-level `BYU_ORC_AGENTS.md` is the authoritative `/apps` symlink. No restricted-data indicators arose in this financial research inventory. No push, publication, external contact, paid acquisition or credential disclosure occurred.

Exactly three research roles were requested successfully: Head `gpt-6.1-sol` medium, separate Coder and Inspector each `gpt-6.1-terra` medium, explicit overrides with `fork_turns=none`. Model verification is at successful request level; runtime agent state exposes names/status but not actual model/reasoning introspection. The coordinating parent is separate from the three research roles.

Actual EP01 input is `runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z` (the laptop path is absent). Source raw `src/sf_quant/data/samsung_2005-20261020.csv`, SHA256 `c64a9cdbba02ee7d70cd3fa4b0af14e0540d0beab70d3d55132f333fb11ba8bb`. Independent source/mapping/hash/units inspection passed conditionally: preferred 005935/KR7005931001, common 005930/KR7005930003, KRW, QUNIT=1. Existing retrospective B01–B04 run `runs/samsung/RG/20261103T010848_30613` matches the companion coefficient table, including persistent DIVYILD association after activity; it is not predictive or causal evidence. Existing coefficient-stability work was reused rather than restarting isolated episode investigations.

Jobs used configured account bhb35, existing `.venv-rg/bin/python` (Python3.11), one node/core,4GB, no partition, bounded BLAS threads; no installations. Module inventory found Python3.11/3.12. All jobs completed exit0:

| Job | Purpose | Elapsed | Peak batch RSS | Artifacts |
|---|---|---:|---:|---|
|15055217|Exploratory validation|55s|273460K|`runs/samsung/prediction_v1_15055217`|
|15055275|Corrected validation / refit audit|58s|291264K|`runs/samsung/prediction_v2_15055275`|
|15055345|Single locked final evaluation|29s|199976K|`runs/samsung/prediction_final_15055345`|

The first run's end digest was unreliable because source was edited while running; it is preserved as exploration. The second run's numerical source/config were unchanged, but an unused summary module and manifest entries were added during execution; this limitation is retained in its log. The final run used a separate immutable snapshot with verified before/after source/config/tests/regression/summary manifest and lock. No test-driven rerun occurred.

Final snapshot `runs/samsung/prediction_final_freeze`; manifest SHA256 `cbac3801f3f1cce5a3d60a2f49eb9dba6bc2d02ff98ddbe230d050522599d9af`. Final lock `runs/samsung/prediction_final_lock.json`, SHA256 `d41f724a64bcc893621cfa97c6d74e2c2bc3d458a1c8140c9d444a682782a26f`. Numerical source SHA256 `3cf7e85c70c4285ab35f12882cbe0528a532815ea1324c2e99d2df9b50f0b7d8`; config `69213601efde85111227effa130f8b1cfa9b6efa3e5ddcb03bbbd4b2499c5cfa`. Final run saves copied lock, snapshot checksums, predictions including implied levels, refit coefficients/scalers/training endpoints, metrics, strict metrics, bootstrap uncertainty, fixed-year stability and input/code/environment provenance.

## Protocol and selection

Target is q(t+h)−q(t), q=100(1−preferred/common), in percentage points, at horizons1/5/20 observed proxy sessions. Origin is after Korean close and vendor field finalization, whose historical clock is unverified. Initial train through2014; validation2015–17/2018–20/2021–23; final origins2024 onward. Monthly expanding refits use only labels ending strictly before the refit origin; ridge scaling uses training only. Validation labels are capped at fold end, never crossing into2024. Existing historical descriptions and retrospective coefficients had been viewed, so the test is not historically unseen.

Z0 persistence, A0 direct AR, A1 AR plus latest change, H1 history ridge and V1 history plus class activity were registered before fitting; ridge alphas .1/1/10/100. H1 contains current q,1/5/20-session trailing changes and20-session change volatility. Candidate training requires max(252,20k). Equal-fold paired MAE gains, the registered0.5%-baseline simplicity tolerance and stability gate selected H1 alpha100 at each horizon. Exact alpha tie ordering was clarified after exploratory validation and is disclosed as validation adaptivity. Inspector independently reproduced selection, metrics and sampled refits before Head created the lock. Activity yielded no material incremental validation improvement; it was not promoted to the final shortlist.

Validation H1 meanfold paired MAE gains versus persistence were .015178/.043822/.028659pp at h1/5/20, with wins in all3folds. However h20 fold2 RMSE worsened (1.7184 vs1.6993), an early stability limitation retained in interpretation. No feature/alpha/refit/metric change followed final losses.

## Final results

All models share the same final origins for each horizon; native persistence coverage equals matched coverage. Targets end2026-10-20; origins begin2024-01-02 and end2026-10-19 /10-13 /09-16 for h1/5/20. Errors in implied level forecasts equal change forecast errors algebraically and are not separate evidence.

|h|n|H1 MAE|Persistence MAE|AR MAE|H1 RMSE|Persistence RMSE|AR RMSE|H1 R² OOS vs persistence|
|---|---:|---:|---:|---:|---:|---:|---:|---:|
|1|679|.645551|.646276|.644646|.841796|.843059|.841727|.002994|
|5|675|1.280598|1.275236|1.267534|1.670657|1.683770|1.674587|.015515|
|20|660|2.239976|2.114604|2.084507|2.894129|2.744197|2.709556|−.112257|

Primary paired MAE gain H1 versus persistence is .000725pp, with moving-block95% interval[−.009182,.011332]pp at block20 and[−.008776,.010473] at block60. Against AR the gain is−.000904pp, interval[−.010391,.009482] at block20. Five-session MAE gain versus persistence is−.005362pp, interval[−.074462,.052689] (block20). Twenty-session gain is−.125372pp, interval[−.299206,.039891] (block40). All main/strict paired uncertainty and60-block sensitivities are saved, including AR comparisons; none establish a reliable gain.

Bootstrap uses2,000 draws, seed20261105, noncircular moving blocks over the full ordered proxy grid, preserving missing eligibility. These are conditional loss-difference intervals with fixed fitted forecasts/selection, approximate stationary dependence, no tuning/re-estimation uncertainty or exhaustive search correction.

Primary H1 beats persistence MAE slightly in2024 (.611360 vs.615124) and2025 (.487938 vs.494463), but worsens in2026 (.886404 vs.876015). Twenty-session H1 MAE is worse in every test year. This instability supports the cautious conclusion. Fixed-year comparisons to AR and RMSE are retained in `stability.csv`.

## Cheap data handling and limitations

Raw data and prior runs are unchanged. Six invalid paired-discount/activity dates were kept missing, with affected endpoint labels and trailing features omitted:2007-11-16,2008-04-30,2008-09-22,2009-05-25,2009-08-31,2009-09-25. Seven existing review flags were retained in main when valid; one strict evaluation sensitivity excludes any interval containing missing/flagged proxy observations. This predetermined omission rule kept research moving; no lengthy date hunt, future interpolation, winsorization or deletion of strange valid prices occurred. [Dated patch ledger](PREDICTION_PATCH_LEDGER.json) records methods.

Multi-session main targets require valid endpoints; the strict sensitivity requires a fully observed unflagged proxy interval. Strict masks evaluation only and does not retrain. Final strict and main samples/metrics coincide (679/675/660) because no affected test interval is present; validation strict counts differ and are reported. The 5,373-row grid is EP01's at-least-one-eligible-quote proxy, not an independent KRX calendar. Both-missing/both-carried dates can lie outside it, so no full real-session no-bridge guarantee is claimed. Historical vendor revisions/finalization, full security-master identity and unequal action history remain incompletely verified. This is a conditional pseudo-out-of-sample historical evaluation, not a certified point-in-time replay.

P03 dividend, P04 external factors and P05 supply/governance remain **untested** because qualified historical availability/provenance is absent. The scoped [input audit](PREDICTION_INPUT_AUDIT.md) records existing inputs and a reasonable public issuer route. Current aggregates and finalized amounts are not backdated into predictors: [Samsung's Q1-2024 disclosure](https://www.samsung.com/global/ir/reports-disclosures/public-disclosure-view.84177/) was dated April30 with a March31 record date. Existing US Barra metadata explicitly marks its publication/vintage information unavailable and forecasting validity false. Relative share volume is activity, not observed liquidity or signed demand. No causal or executable trading/cost claim follows these tests.

## Review and resume

Batch A source/retrospective audit and B validation/code inspection were independent and recurring; [inspection report](PREDICTION_INSPECTION.md) contains findings and final C verdict. Head triaged endpoint-valid labels as planned, fixed provenance/audit omissions before final lock, and deferred unavailable optional mechanisms with reasons. Batch C independently passed: metrics, forecast arithmetic, label maturity, four sampled refits, immutable hashes and a representative bootstrap interval were reproduced; no material code defect was found.

[Plan](PREDICTION_IMPLEMENTATION_PLAN.md), [decision ledger](PREDICTION_HYPOTHESIS_LEDGER.json), [input audit](PREDICTION_INPUT_AUDIT.md), [patch ledger](PREDICTION_PATCH_LEDGER.json), and [exact resume instructions](PREDICTION_RESUME.md) are durable. Copy of this report belongs at the final run root after C review. The qualified shortlist is evaluated; no further model search on the exposed final holdout is warranted. Additional research needs genuinely new unexposed dates and a bounded preregistered question, or qualified class spread/flow/borrow and announcement/action inputs. Scheduler jobs persist independently; interactive agent survival across disconnect is not promised.
