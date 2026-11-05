# Samsung discount prediction: adaptive implementation plan

**Scope update, November 5, 2026:** Follow [CONTINUE_REMOTE_RESEARCH.md](CONTINUE_REMOTE_RESEARCH.md). Completing the shortlist below is a checkpoint, not completion of the broader program. Inspect the outcomes, update the hypothesis tree, acquire additional accessible data when justified, and execute the next evidence-based batch. Keep previously viewed holdouts labeled as viewed and distinguish exploratory follow-up from genuinely new validation.

Date: 2026-11-05 UTC. Owner: research HEAD; implementation: coder; independent review: inspector. Status: first remote execution checkpoint complete; locked shortlist evaluated and independently reviewed with no reliable primary forecasting gain. That result is retained as provenance while the broader research loop continues under the scope update above.

## Scope and precedence

The current user priority is useful prediction of the Samsung common/preferred discount. Mechanisms organize feature choices and rival explanations; their causal plausibility and their forecast value are separate judgments. All real-data research, fitting and evaluation run on authorized school compute through SSH. Local work is limited to planning and, when implementation resumes, staging code and synthetic engineering checks. No paid services, external messages or credentials in tracked files.

For this workflow this plan supersedes the extensive influence/date-investigation sequence in `COEFFICIENT_STABILITY_AGENT_PLAN.md`. Do not execute that older program before forecasting. Preserve existing user work and immutable raw inputs. A few questionable observations receive a simple documented treatment and work continues; systematic mapping, units, timing or leakage defects stop the affected branch.

Read the companion `PREDICTION_HYPOTHESIS_LEDGER.json` and `B04_CAUSAL_MECHANISM_CANDIDATES.md`. Existing B04 coefficients are retrospective associations. They neither rank forecasting models nor represent Samsung's own leverage/dividends. Share-volume ratios measure activity, not spreads, flows or investor identity.

## Ranked research order and hypothesis tree

1. **Past discount and price discovery (P01):** persistence, short-run reversal, trend and volatility are the smallest data path and essential competitors to every mechanism. Reversal can arise from stale prices or asynchronous trading, rather than tradeable convergence. Audit quote validity and test whether any improvement survives longer horizons and flag sensitivity.
2. **Class demand / trading conditions (P02):** add available relative volume; prioritize actual class turnover, investor flows, spreads and borrow conditions only if accessible with dates and availability. Demand concentrated in common can widen the discount; constrained arbitrage can prolong it. No universal stress sign is imposed. Activity adds predictive value only if it improves validation on the same origins.
3. **Dividend / corporate-action arithmetic (P03):** add only calendars known at the forecast origin. Equal cash dividends mechanically change the percentage discount; Samsung's preferred dividend premium is 1% of par annually, not 1% of the common dividend. Distinguish anticipated calendar effects from surprise policy news and unverified adjusted-return series.
4. **Global risk, FX and chip state (P04):** test a small verified-available lagged block, conditional on P01/P02. Economic news needs a class-specific transmission channel to explain a relative price. US style returns are external states, not Samsung accounting variables. Historical availability/vintage restrictions outrank convenient coverage.
5. **Governance / class-specific supply (P05):** use verified dated repurchase, cancellation, issuance, float or voting events when enough independent observations exist. Separate authorization, execution and cancellation. Sparse events support case studies or diagnostics, not a high-dimensional daily model.

Nearest rivals remain ex-dividend arithmetic, stale quotes, timing mismatch, structural change and chance selection. A forecast win alone does not identify its mechanism. A coherent mechanism without an out-of-sample gain does not improve the predictor.

## Remote resume and data inventory: batch A

Authentication status at planning: an escalated network check reached `ssh.rc.byu.edu`; noninteractive authentication returned `Permission denied (keyboard-interactive)`. The user subsequently confirmed an authenticated VS Code SSH session, visible as `MRP-Project [SSH: ssh.rc.byu.edu]`; this local Codex session cannot inherit it through available access. The user will start remote Codex. No remote repo absolute path or data inventory has been confirmed by this team, and no new empirical job has run. Use the supervisor's `REMOTE_PREDICTION_HANDOFF.md` in that remote session; do not retry aliases, seek credentials or bypass session access controls.

After a usable SSH context exists:

1. Read applicable remote AGENTS instructions. Confirm hostname, current directory, repository root, git status, available Python environment and scheduler policy. Record identifiers without secrets. Locate an existing configured `slurm/cluster.env.sh` rather than guessing paths, allocation or partition. Use compute nodes for empirical work.
2. Inspect one bounded inventory of the remote repository, configured EP01/RG paths, frozen code/config and available source runs. The local config expects `runs/samsung/EP01_descriptive/20261022T070701_403388Z`; this is a relative expectation, not a confirmed remote location. Verify remote reality, including more recent runs, before assuming anything is absent.
3. Identify exact raw data, measures, manifests, source inventory, quote flags, class identifiers, currency/units, volumes, session calendar and corporate actions. Check raw hashes against manifests and class mapping against existing source documentation. Keep raw data on authorized school storage; transfer only permitted code/review artifacts.
4. Inventory external factor/FX/chip/event inputs and metadata: units, geography, currency, dates, actual publication/availability timestamps and revisions. Missing optional inputs block their branch only. Do not require a factor export before running qualified history-only models.
5. Create an exclusive remote prediction run directory with source/code/config hashes, environment, inventory, patch ledger and batch status. Record whether any proposed holdout dates have already informed model design. Export compact audit summaries; avoid dumping licensed rows into chat.

Implementation reuse: inspect `e01.load_and_validate` / `match_pair` for class/quote checks and `regressions.dated_csv` / `outcomes` plus manifest validation. Reuse verified pieces, not the whole explanatory preparation requirement: history-only forecasts must not wait on Barra metadata, and existing contemporaneous factor bins must not be rebranded as forecasts.

Inspector reviews batch A before model interpretation: mapping, units, gaps, stale quotes, alignment and availability. Code staging may proceed independently. Stop only affected empirical branches while material defects are corrected.

## Forecast specification and candidate budget: batch B

At forecast origin the Korean session close **t**, predict `y_h(t) = q(t+h)-q(t)`, where `q=100*(1-P/C)` is in percentage points, primary `h=1`, secondary `h=5,20` observed sessions. The implied level forecast is `q(t)+predicted_y_h(t)`. The origin is a research close-to-close information set, not a claim that the same closing auction was executable. If closing prices or volumes finalize later, move the declared decision timestamp accordingly and disclose it. Horizons count the preserved session grid, not surviving eligible rows.

Retain invalid/missing price rows before shifts, rolling calculations and target construction. Never bridge deleted dates. Endpoint discount changes at h>1 are valid when both endpoints are valid; report intervening missing/flagged sessions and a stricter sensitivity requiring all h+1 prices valid. Features requiring consecutive changes/windows require their complete trailing grid. Match the sensitivity sample separately and report its coverage.

Predeclared small candidates, subject to field verification:

| ID | Forecast / features | Purpose |
|---|---|---|
| Z0 | Zero discount change; constant current discount level | Essential persistence benchmark |
| A0 | Direct OLS `y_h ~ intercept + q(t)` | Simple AR/mean-reversion benchmark; no equilibrium claim |
| A1 | A0 + `delta_q(t)` | Distinguish short-term reversal from slow level adjustment |
| H1 | q(t), trailing discount changes over 1/5/20 sessions, trailing 20-session change volatility | Small history model |
| V1 | H1 + log(preferred/common volume) at t | Incremental activity test; finite positive class volumes only |
| E1 | Best validated history/activity set + small qualified external or known-calendar block | Conditional extension, separately registered before fitting |

Use OLS for A0/A1. H1/V1/E1 use train-standardized ridge with alpha in `{0.1,1,10,100}`; intercept unpenalized. No more than these initial families; do not expand a broad nonlinear/search system before a measurable validation gain. No full-sample winsorization, imputations, detrending, feature selection or residualization. Missing optional fields get a separately evaluated complete-case branch; all baseline comparisons use exactly its eligible origins. Native baseline coverage is also reported. If a model cannot support `n >= max(252,20*k)` training rows, skip it with a reason. If code dependencies differ remotely, use the smallest existing numerical stack rather than installing a new framework without need.

## Chronological selection, lock and test

Before fitting or inspecting target-performance summaries, freeze actual boundaries from the remote coverage audit. Default for verified 2005–2026 coverage: initial training through 2014, validation folds 2015–2017 / 2018–2020 / 2021–2023, final test from 2024 through the last available verified session. If dates/coverage require another split, HEAD records it before validation. Existing descriptive history and retrospective coefficients have already been viewed: even an unused forecasting holdout is not historically unseen, and this limitation must be explicit.

Use expanding training; within each validation fold, start from its prior observations and refit monthly using only labels that have fully matured before that origin. Scaling and any tuning use only that training history. For h-step targets enforce `training_label_end < evaluation_origin` at every refit, and purge boundary origins accordingly. No random splits. No overlapping test targets in training, including at monthly updates. Refit policy is fixed before holdout. An expanding test may absorb matured past test labels by the same registered rule; no model or hyperparameter changes are allowed from test performance.

Select one challenger per horizon using mean fold MAE improvement versus persistence on identical origins, with fold RMSE/stability as safeguards; retain simpler model when MAE differences are less than 0.5% of baseline MAE. Prefer baseline if the best challenger does not beat it in at least two validation folds or materially worsens the remaining fold (>5% MAE). Record all candidates attempted, not only winners. Horizon 1 is the primary decision; horizons 5/20 are exploratory secondary decisions, not extra chances to declare primary success.

Inspector reviews batch B code, synthetic alignment/maturity fixtures, origin masks and validation summary. HEAD then freezes selected family, features, alpha per horizon, refit policy, split boundaries and metric code in a lock artifact with hashes. No final holdout pass until this review and lock. Any holdout-driven redesign starts a clearly exploratory follow-up; it cannot reuse the original confirmatory label.

## Evaluation and uncertainty: batch C

Run the locked evaluation once and preserve every forecast, actual, origin/target date, model version, eligibility mask and training endpoint on remote storage. Report MAE, RMSE and `R2_OOS = 1-SSE_model/SSE_zero`, plus relative errors versus A0 and Z0. Report change and implied level forecasts explicitly; their errors are algebraically identical when both use the same q(t), so do not count them as separate evidence. Directional accuracy and turnover are secondary. Do not claim trading returns without an executable-price/cost model.

Quantify paired forecast-loss differences using a moving-block bootstrap with 2,000 draws and fixed seed 20261105, block length max(20,2h); show 60-session-block sensitivity. Resample contiguous session blocks with original eligibility preserved and report finite-pair counts. This is approximate dependence-aware uncertainty, not proof of independent observations or exhaustive multiple-search correction. Show fixed calendar subperiod/fold stability and concentration in flagged dates. No bootstrap-based retraining/search on the holdout.

Inspector reviews batch C independently against baseline mechanics, data defects, timing and economic plausibility; messages coder directly about likely code defects and HEAD about unexplained or suspicious results. HEAD resolves defects and records whether a corrected rerun compromises the lock. A surprising win is audited before interpreted; a null result is a completed result.

## Patch policy, handoffs and changing priorities

For isolated malformed/missing quotes or zero-volume logs, preserve raw inputs, apply an explicit validity mask or narrowly documented verified correction in derived data, record affected rows/units/reason and continue. An unexplained large move is not automatically an error and is not deleted for improving performance. Run one compact sensitivity if it can change conclusions. No recursive historical date hunt. Propagate invalid values through affected lags/windows; never fill missing prices, volume or events with zero.

Stop the affected branch for systemic class swaps, factor percent/decimal errors, unequal actions, missing-source calendar defects, or future-information leakage. Coder sends inspector exact reproduction/artifact; inspector sends a direct defect report back; HEAD decides repair, branch exclusion or limitation. Each batch ledger records status, artifacts/hashes, review verdict, action and next dependency. Handoffs occur at A/B/C and after every material correction, not only at the end. Supervisor receives compact substantive progress; no unchanged polling.

Reprioritize only with a recorded trigger: verified accessible mechanism data can advance its block; demonstrated data/timing defects can demote it; weak incremental validation can close it; sparse events downgrade causal claims; unstable gains favor simpler baselines. Broader model search requires a concrete validation failure hypothesis and a bounded amended candidate budget **before** final holdout. No hypothesis is promoted because of an attractive full-sample p-value.

## Completion and stopping criteria

Finish when the smallest qualified history/activity experiment, feasible prioritized input blocks, locked evaluation and independent inspection are complete, including a legitimate baseline victory. Deliver reproducible remote run paths/job IDs, hashes, tested code, split/feature availability audit, forecast metrics/uncertainty, exclusion/patch ledger, inspector verdict and concrete remaining data needs. Do not call prediction successful unless the locked primary challenger improves baseline errors with uncertainty and stability disclosed.

Close an unavailable branch after one scoped inventory and one reasonable authorized acquisition route identify a concrete dependency; name the missing source, field, availability metadata or access step. SSH authentication currently blocks empirical work but does not turn missing results into nulls. Do not repeat failed authentication, invent paths, or substitute local empirical execution. Resume at batch A when authenticated access is available.


## Remote execution checkpoint — 2026-11-05 UTC

Head verified login03, repository `/home/bpinoli/MRP/MRP-Project`, revision `5c6f79091c00204da5f86b87a69648b4cdd67fe0`. `git status --short` recorded existing staged/untracked work; `git pull --ff-only origin main` succeeded (already up to date). Work is preserved. The top-level site file is the required symlink to `/apps/instructions_for_ai_agents/BYU_ORC_AGENTS.md`; all seven applicable reference guides read. No restricted-data indicators appeared in this financial research inventory.

Team requests: Head `/root/research_head` requested `gpt-6.1-sol`, medium; Coder `/root/research_head/coder` and independent Inspector `/root/research_head/inspector` each requested `gpt-6.1-terra`, medium, fork_turns=none. These are verified from successful spawn requests. Runtime agent state reports roles/status only and does not expose model/reasoning metadata; do not claim stronger runtime verification. No further research agents permitted. Coder owns new forecast code/config/tests/jobs/runs; Inspector owns inspection artifacts; Head owns this plan, ledger, decisions and final report.

The expected EP01 path is absent. Actual reusable pack: `runs/samsung/RG/20261026T131821Z_setup/EP01/20261026T131848_234484Z`; raw source `src/sf_quant/data/samsung_2005-20261020.csv`, registered SHA256 `c64a9cdbba02ee7d70cd3fa4b0af14e0540d0beab70d3d55132f333fb11ba8bb`. Existing completed retrospective run: `runs/samsung/RG/20261103T010848_30613`, with prepared source hashes and frozen configuration. Other bounded inventory: `20261103T010838_25471`, `20261103T021451Z_coefficient_stability`, setup run. Inspector independently reconciles these, not stale CLUSTER.md claims of no runs.

Available module choices include python/3.11 and python/3.12. Existing configured Python `/home/bpinoli/MRP/MRP-Project/.venv-rg/bin/python`; configured account `bhb35`; no partition requested. Forecast jobs use one CPU, one node, 4GB, 30 minutes maximum and bounded threads. Head centrally checks scheduler at least 60 seconds apart. Initial user queue was empty. Default sandbox initialization fails before shell execution (`bwrap` temporary directory); approved escalation is used for narrow authorized commands.

**Before fitting, Head freezes** train through 2014-12-31, validation folds 2015–2017 / 2018–2020 / 2021–2023, final test from 2024-01-01 through verified coverage. Candidate families and alphas remain the table above, horizons 1/5/20, monthly expanding refits, strict matured labels. Session counts refer to preserved EP01 observed-session proxy, not independently verified exchange sessions. Prior full-history descriptive/retrospective access means final test is not historically unseen. Closing price/volume finalization clocks and historical vendor vintages remain unverified; origin is after Korean close and completion of vendor fields, not same-auction execution.

Next checkpoint: Inspector batch A mapping/hash/calendar verdict; Coder synthetic fixtures and validation in Slurm; Inspector batch B; Head lock; one final evaluation; Inspector batch C. Holdout target-performance summaries remain sealed until the lock.

### Validation selection convention clarified before corrected validation / final test

The first exploratory validation job `15055217` completed in 55 seconds, peak batch RSS 273460K. Preserve it, but do not use its end-of-run source digest as proof of executed source: the module was edited while it ran. This is a reproducibility defect, not evidence of forecast leakage. A corrected immutable snapshot must be reviewed and rerun. No final test performance was inspected.

Apply the already registered equal-fold MAE criterion concretely: compute each fold's paired MAE(Z0) minus MAE(candidate) on exactly the candidate origins, then average the three fold differences. The 0.5% tie tolerance uses the correspondingly paired mean fold baseline MAE. Eligibility requires beating persistence in at least two folds and no >5% MAE deterioration in the remaining fold. Prefer the simplest eligible family within tolerance of the best: Z0, A0, A1, H1, V1, in this order. A0 remains the direct-AR comparator even if it is not selected. Within a ridge family, prefer alpha=100 over 10 over 1 over 0.1 when differences are within tolerance; this is a parsimony convention, not a significance statement or proof that 100 is best. The exact alpha tie ordering is clarified after exploratory validation; disclose this validation adaptivity. The final target-loss holdout remains sealed and no hyperparameters will change based on it.

Inspector batch A accepted conditionally. Endpoint-valid multi-session cumulative labels remain main per predeclared plan; strict sensitivity excludes any missing/flagged proxy observation over the entire interval and reports matched baselines. Unknown exchange sessions remain a limitation of both. No episode deletion is chosen to improve validation.

### Batch B decision and final lock

Corrected validation job `15055275` completed exit 0 in 58 seconds, peak batch RSS 291264K. Independent Inspector reproduced selected metrics to 3.1e-16 and four sampled ridge refits/scalers to 1.2e-16, with all training endpoints strictly before refit origins and validation labels ending by 2023-12-28. D10 selects H1 alpha=100 for all three horizons, with equal-fold paired MAE gains 0.015178 / 0.043822 / 0.028659 percentage points versus persistence. Activity V1 has no material incremental validation improvement. Horizon-20 fold 2 worsens RMSE (1.7184 versus 1.6993) despite MAE gain; this limits stability, rather than justifying post-hoc redesign.

V2 numerical source/config remained unchanged, but an unused summary module and checksum manifest entries were added during execution; preserve the before/after log and disclose this provenance limitation. Final execution uses a separate immutable directory `runs/samsung/prediction_final_freeze`, manifest SHA256 `cbac3801f3f1cce5a3d60a2f49eb9dba6bc2d02ff98ddbe230d050522599d9af`. Head created exclusive lock `runs/samsung/prediction_final_lock.json`, SHA256 `d41f724a64bcc893621cfa97c6d74e2c2bc3d458a1c8140c9d444a682782a26f`, after Inspector B signoff and before final-test target losses. One final evaluation authorized; features, alpha, refit policy and bootstrap remain fixed.

Moving-block confidence intervals use the full ordered proxy grid with missing eligibility, 2,000 draws, seed 20261105, block max(20,2h) and 60, without circular wrapping. They condition on already estimated forecasts and selected models, omit tuning/estimation uncertainty, and rely on approximate stationarity. Strict sensitivity masks evaluation intervals only and does not retrain on masked historical flags. Stronger real-time and tradability claims remain unsupported.


### Completion checkpoint

Final job15055345 completed exit0 in29s, peak batch RSS199976K. InspectorC independently verified metrics/arithmetic/maturity/refits/hashes and bootstrap. Primary gain .000725pp vs persistence has95%block20 interval[−.009182,.011332], below AR point estimate;20-session worsens materially. No further fitting or holdout reuse. Final report PREDICTION_RESEARCH_REPORT.md and exact resume PREDICTION_RESUME.md; all A/B/C complete. Optional provenance-dependent mechanism branches remain untested, not null.
