# Agent execution brief: coefficient stability and mechanism research

## Objective and scope

Determine which apparent changes in Samsung common/preferred discount coefficients exceed estimation noise, whether a few observations drive them, and which observable states might explain them. Produce a bounded, reproducible investigation, not an open-ended historical narrative. Prioritize useful evidence over model count.

This is an instruction to execute the available work, not merely propose it. Do not run this entire research program if inputs are missing: finish independent work, implement and validate blocked extensions with synthetic data where useful, and give an exact dependency handoff. Do not fabricate results or treat blocked models as null findings.

Read applicable AGENTS.md instructions. Read once: configs/samsung_regressions.json, docs/regressions/{METHODOLOGY,DATA,FACTORS,CLUSTER}.md, src/samsung_research/regressions.py, and scripts/run_samsung_regressions.py. Reuse existing functions. Inspect git status and preserve unrelated work. No new framework, dashboard, database, or wholesale pipeline rewrite.

The supplied table is docs/regressions/B01_B04_RETROSPECTIVE_COEFFICIENT_TABLES.md. It is a user-provided summary, not a reproducible run record. Repository hub/runbook statements that no empirical run has occurred may be stale. Verify current artifacts before repeating them. Empirical fitting belongs on authorized school compute nodes under the existing workflow; local checks use synthetic data unless the user has authorized otherwise. Never invent cluster access or configuration.

## Execution order and work limits

1. Inventory and exact sample reconciliation.
2. One automated influence screen, one fixed episode audit, one bounded sensitivity batch.
3. B00/common-sample comparisons and formal period-stability tests.
4. M01/M02 mechanism blocks, followed by M03/M04 when data exist.
5. A small set of registered state interactions.
6. A separately specified forecasting evaluation when timing and inputs qualify.

Do not wait for missing mechanisms to finish steps 1–3. Do not run every model/window/bandwidth combination just because the default grid exists. Central inference is HAC 20; use HAC 5/60 as robustness for shortlisted results. Reuse OLS estimates across bandwidths when the design and sample are unchanged. Cache prepared designs and hashes.

Keep a machine-readable ledger with item, status, evidence path/hash, decision, blocker, and next action. Read compact summaries into the conversation, not raw tables or logs. Give brief progress updates about decisions and blockers. Do not request confirmation for routine reversible work already authorized here.

## 1. Locate evidence once and freeze the run

Perform one scoped inventory of configured input paths and runs/samsung/RG (or the current run location). Identify source REPORT.md, coefficients.csv, task/sample/residual files, frozen code/config, factor alignment report, flags, and EP01 inputs. If the cluster code differs from local code, use the frozen implementation to interpret the supplied results; document the difference. Do not silently reinterpret a retrospective preceding-US-session join using a different local join rule.

Write inventory.json recording what is present, missing, and reproducible. Identify one primary source run rather than merging arbitrary runs. Verify source hashes and exact sample dates. Create a new exclusive run directory; preserve previous runs and raw inputs.

If only the pasted table is available, save a table-level assessment and exact artifact request; do not claim an influence audit is possible from coefficients alone. Continue engineering work that does not need licensed data. Ask for the source run bundle once, with a consolidated missing-file list. Do not repeatedly search the filesystem for the same unavailable input.

Reconcile the 5,195 versus 5,189 full-sample observations and every period's main/sensitivity date difference. Six fewer regression rows need not mean six independent events. Distinguish original flagged price dates from rows lost to differences, lags, or missing controls. Preserve the full session grid; do not difference or lag after deleting dates.

## 2. Influential-date investigation: fixed scope, hard stopping rules

### 2A. Produce one machine-readable screen

Use the existing source designs or reconstruct them exactly. Screen B01 and B03, main, in the three prespecified periods. These cover factor-only and discount-adjustment behavior without multiplying work across near-duplicate B02/B04 variants. Add a B04 check only if it changes the conclusion.

For each screen fit, export date, session index, eligibility/flag reason, outcome, fitted value, residual, leverage, internally studentized residual, Cook's distance, and signed DFBETAS. Focus the compact display on lag_discount where present and BETA, MOMENTUM, LEVERAGE; save all coefficient diagnostics to disk. Define each formula and scaling in the methodology. Use QR/linear solves, not unstable explicit matrix inversion.

These are classical OLS influence rankings, not HAC significance tests, data-error probabilities, or grounds for automatic deletion. Classical cutoffs are screening aids only. Rank within each fit before combining candidates so shorter periods and different units are comparable.

Build a fixed candidate set:

- Include every source flagged episode that generates a main/sensitivity sample difference.
- Add at most six previously unflagged episodes from the union of the top-three Cook's-distance and top-three absolute targeted-DFBETAS rankings per fit. Deduplicate and rank that union using best within-fit percentile; use a fixed date tie-breaker.
- Group candidate dates within two original Korean sessions into one episode. Show at most two surrounding sessions on each side in the audit packet.
- Investigate at most twelve episodes in total. Existing flagged episodes take precedence; if there are more than twelve, audit the twelve with highest model influence and list the remainder as unresolved. Save the full screen without manually investigating the tail.
- Freeze the candidate list before external searching. No recursive expansion based on an interesting news story.

An episode is a review unit, not an automatic exclusion window.

### 2B. Assemble one compact evidence packet per episode

Generate packets programmatically. Include both classes' raw closes, available verified adjusted prices/action factors, quote/status flags, volumes, discount/log gap, daily changes, actual interval length, aligned US factor dates and returns, source row IDs, and available corporate-action/dividend records. Show only existing fields; mark unavailable fields explicitly. Look for unit/split mismatches, stale/carried prices, holiday gaps, unusually large factor observations, factor percent/decimal errors, and wrong interval joins.

Use one overview figure with the selected episodes and one compact appendix; do not create a new chart for each date unless the packet cannot resolve a material discrepancy. Never dump the full price panel or all diagnostics into chat.

### 2C. Triage before historical research

Assign one status and evidence confidence per episode:

1. Confirmed measurement/alignment error: documented evidence and exact correction.
2. Genuine observed market move: internal price/action checks pass; an economic explanation may remain unknown.
3. Registered eligibility exclusion: supported by the pre-existing sample rule; not necessarily a proven bad quote.
4. Unresolved: data insufficient.

Internal consistency alone does not prove a quote correct, and a news headline does not validate a quote. Record any proposed driver as a hypothesis unless supported by direct evidence.

External research is restricted to unresolved issues that could materially affect the result. First use existing vendor/action/issuer records. If still useful, allow at most two targeted searches and two directly relevant source opens per episode, capped at twenty searches and twenty source opens across this audit. Prefer issuer, exchange, or vendor evidence; record URLs and dates. Do not search news for every large residual. Do not paywall-hop or broaden the history endlessly. At the cap, label unresolved, give the missing evidence, and continue. Missing external access is not a reason to repeat tool attempts.

### 2D. One bounded sensitivity batch

Estimate, using the same model definitions and session-grid HAC:

- Source main and registered sensitivity samples.
- Main with each frozen candidate episode's affected regression rows omitted individually, at most twelve episode omissions per screen fit, only where the episode is in that fit.
- One combined omission of all selected episodes as a deliberately extreme influence diagnostic, not a preferred estimate.
- If errors are confirmed, one separately versioned corrected-data run with a correction ledger. Do not apply this branch to merely unexplained observations.

Distinguish regression-row omission from invalidating an underlying price: invalid prices must propagate through every affected difference and lag according to the registered rule. Do not bridge missing sessions. Refit HAC after omissions. Save exact omitted rows and reasons.

Report signed coefficient changes, sign changes, and changes divided by the original fit's HAC SE. Avoid percentage changes when the reference coefficient is near zero. Show fit changes and whether the substantive conclusion survives; a p-value crossing 0.05 is not the conclusion. Deletion comparisons are descriptive and selected after observing influence, not new confirmatory tests.

Stopping rule: after this batch, close the audit with one of: robust to reviewed episodes; sensitive to a few observations; demonstrable data error; or unresolved source dependence. Do not launch another date hunt because coefficients remain unstable. Broader review requires a concrete newly established systematic error or a separate user request.

## 3. Establish the baseline and test actual instability

Retrieve B00 if already fitted. Otherwise fit its registered discount-only equation. Compare on exact shared date masks:

- B00 versus B03: incremental explanatory value of the factor block.
- B01 versus B03: incremental value of the lagged discount.
- B03 versus B04: incremental value of trading activity.

For each comparison save n, date-mask hash, R²/adjusted R², partial R² = (restricted SSR - unrestricted SSR)/restricted SSR, and a HAC-robust Wald test for added terms. Do not use an iid partial-F p-value as the primary inference. Show native coverage separately. B02 is an outcome-transformation robustness check, not independent replication.

Fit one pooled period-interaction model for B03, allowing intercept, lag-discount coefficient, and all factor coefficients to differ across the fixed 2005–2014, 2015–2019, and 2020–2026 periods. Include period intercept shifts so a changed average relationship is not forced into changed slopes. Use the original-grid multivariate HAC score covariance, retaining cross-period boundary contributions.

Primary tests: joint equality of the factor slopes across periods; joint equality of lag-discount coefficients across periods. Secondary: a small declared set of individual slopes and pairwise contrasts. Predeclare the successful-test multiplicity family and distinguish it from the old submission's BH family. Do not combine old and new q-values silently. Report effect sizes and confidence intervals as well as p/q values. Failure to reject is not proof of stability.

Separate descriptive adjustment from claims of stable equilibrium: inspect discount persistence and run documented ADF/KPSS trend/lag sensitivities before interpreting half-lives. A significant lag coefficient alone does not establish a stationary equilibrium. No exhaustive break-date search. The supplied periods are the primary stability design. Any additional break analysis is a separately labeled extension.

Optional display only: trailing 756-session B03 estimates at quarter-end, at most four target coefficients, with uncertainty and sample counts. Overlapping windows are not independent tests. Skip if it adds no decision value; do not let a rolling dashboard delay mechanism work.

## 4. Mechanism work, ordered by information gained

Create one coverage/provenance table for M01–M04 and L01: field definition, class identifiers, units, start/end, missingness, availability lag, revision status, independent release/event count, and licensing/source. Report why each blocked field matters. Existing volume ratios are activity, not spreads or float-adjusted turnover. Missing borrow fees are not zero.

Prioritize M01 (relative spreads and turnover) and M02 (retail participation and foreign flows). Use the registered equations and definitions in FACTORS.md. Fit each block separately first, comparing B03 and the augmented model on identical rows. Show how much baseline coefficients change merely from using the mechanism's shorter sample before attributing changes to the added controls. A complete block runs under its existing ID; a partial block receives a new explicitly restricted ID, never the original model label.

Then M03 (common borrow fees) and M04 (relative repurchases/dividend entitlement) as coverage permits. Sparse announcements, policy changes, or annual ownership updates require event/monthly designs and independent-event counts; do not replicate a slow series across daily rows and claim thousands of independent observations. A ban dummy is not a borrow fee. Separate buyback announcements, executions, and cancellations.

L01 can follow once its fields exist. J01 and the registered X01/X02 interactions are later checks, not prerequisites. Do not force all mechanisms onto one tiny common sample for the entire project. Add verified Korea/global controls if available as a separately versioned robustness block; the US controls remain explicitly US controls. Broader ownership/panel research should not block this single-pair stage.

## 5. Explain changing coefficients with a small state-dependent design

Adding a mechanism in levels does not by itself test why a coefficient changes. Register a separate extension before estimating it. Use no more than two initial state variables, chosen by economic rationale, data quality, and coverage rather than smallest observed p-value. Start with relative spread and common borrow fee if qualified data exist; if not, use the best qualified M01/M02 state and document the choice.

For outcome y_t = dd_pp_t and discount q_(t-1), fit:

    y_t = alpha + beta'F_t + rho*q_(t-1)
          + gamma*Z_(t-1) + theta*q_(t-1)*Z_(t-1) + error_t.

Retain both main effects. Report conditional adjustment rho + theta*z at representative supported state values, confidence intervals using the full covariance, and whether the data support those values in multiple periods. Center/scale explicitly; full-sample scaling is descriptive only. Do not equate conditional adjustment with a causal arbitrage channel. Check whether Z largely proxies period membership; include period intercept/main-slope robustness where identified, and report poor within-period variation or collinearity.

Then, only for factor slopes with credible stability evidence and a specified transmission story, allow up to two targeted F_t × Z_(t-1) products with main effects. Distinguish factor sensitivity from discount adjustment. Do not search all factor/state combinations. X02 is an existing semiconductor/retail candidate, not a mandate to fit it without its data.

Use HAC inference plus a prespecified 20/60-session contiguous-block bootstrap for the small final interaction set when estimable. Document how blocks preserve joint rows, missing-grid positions, and lagged design values; do not stitch raw price levels and create artificial boundary changes. Record seed, replications, failures, and estimator. A bootstrap is a sensitivity, not a fix for weak identification or nonstationarity.

## 6. Prediction is a separate evaluation, not a reinterpretation of explanatory fits

Specify forecast origin, horizon, target, and input availability first. A prior-US-session shock may occur after the previous Korean close; being known by the outcome close does not make it available at the forecast origin. Build origin-safe joins using actual availability and vintage information. If vintage timing is unknown, label a retrospective pseudo-out-of-sample exercise or block the forecasting claim.

Because these full-history summaries have already been viewed, no historical period is genuinely untouched by research judgment. Freeze a chronological evaluation protocol now; call the historical final segment a reserved evaluation segment with acknowledged prior exposure, and reserve genuinely new future data for prospective confirmation.

Minimal candidates: zero change, historical-mean change, B00-style AR adjustment, origin-safe constant factor model, one selected state-dependent model. Use expanding annual evaluation folds, an initial training history of at least five years, and identical scored dates per comparison; report coverage separately. Any tuning, scaling, feature selection, or nuisance residualization occurs within training only. Use boundary purging/embargo when labels overlap; do not impose arbitrary gaps on nonoverlapping one-session labels.

Primary metric: out-of-sample MSE and improvement versus zero change and AR, with dependence-aware uncertainty. Secondary: MAE and period breakdown. No trading profitability claim without verified total returns and execution/borrow costs. Do not promote a model because its in-sample coefficients are significant. Record failure to improve as a valid result and stop expanding the candidate set.

## 7. Deliverables, validation, and final stopping rule

Minimum artifacts in the new run:

- inventory.json and status/dependency ledger.
- sample_reconciliation.csv, influence_screen.csv, frozen episode_candidates.csv.
- One episode_audit.md table with source references, status/confidence, and unresolved evidence.
- influence_sensitivity.csv with exact omission masks.
- common_sample_comparisons.csv and stability_tests.csv.
- mechanism_coverage.csv and results for eligible prioritized models.
- Versioned interaction/prediction specifications and results only where actually executed.
- A concise REPORT.md linking artifacts and distinguishing completed, blocked, and deferred work.

Record hashes, source/frozen code differences, equations, windows, timing, inference families, and any corrections in the existing methodology registry/docs; preserve prior versions. No published calculation without reconstruction instructions. Test new engineering with meaningful synthetic fixtures: influence against direct deletion, multirow episode deletion, invalid-price lag propagation, common masks, HAC Wald restrictions, interaction main effects/conditional uncertainty, and origin-safe timing where implemented. Run relevant existing tests. Do not rerun unchanged test suites indefinitely.

The existing entry point is scripts/run_samsung_regressions.py with readiness, freeze, prepare, fit, collect, and count stages. Inspect current CLI/config and frozen-run behavior before composing exact commands. Use the existing Slurm wrapper on school compute for empirical fits; a readiness check is not substantive data validation. Do not launch the entire default task grid when a focused configuration suffices.

Final response: at most about 800 words, with links to detailed artifacts. Answer: (1) which apparent changes are supported; (2) which depend on a few observations; (3) what mechanisms have actually been tested; (4) whether any state explains adjustment/sensitivity; (5) whether prediction improves, if evaluated; and (6) exact blockers and highest-value next action. Stop after the fixed batch and planned comparisons. Unresolved dates, null results, and unavailable mechanisms are acceptable explicit outcomes; endless investigation is not.
