# Remote Samsung prediction research handoff

In the **remote** VS Code SSH workspace, pull the latest `main` without discarding existing work:

```bash
git status --short
git pull --ff-only origin main
```

If Git reports conflicting local changes or diverged history, preserve those changes and reconcile them; do not reset or overwrite them. Then give remote Codex this instruction:

> Read `docs/regressions/REMOTE_PREDICTION_HANDOFF.md` and execute its research handoff, including the companion plan, hypothesis ledger, mechanism notes, and retrospective coefficient table listed below.

The following documents are included together in the repository:

- [Implementation plan](PREDICTION_IMPLEMENTATION_PLAN.md): ranked experiments, batch handoffs, validation, and stopping rules.
- [Hypothesis and decision ledger](PREDICTION_HYPOTHESIS_LEDGER.json): initial hypotheses, priorities, evidence, and next actions.
- [Causal mechanism candidates](B04_CAUSAL_MECHANISM_CANDIDATES.md): economic interpretations, competing explanations, and distinguishing predictions.
- [Retrospective coefficient table](B01_B04_RETROSPECTIVE_COEFFICIENT_TABLES.md): the available B01–B04 summary; verify against remote source runs.

The execution prompt below is self-contained. Read the companion documents before research and update their decisions and status as evidence arrives. Any statements that local planning awaited SSH authentication describe the originating laptop session; assess the current remote session directly.

---

Work in this SSH-connected MRP-Project repository on the BYU research environment. I authorize sustained research, code changes, environment setup, inspection of accessible licensed datasets, public-data acquisition, and submission of appropriately sized CPU jobs under site policy. Start the work; do not stop at proposing a plan. Preserve existing changes and raw data. Do not publish, push, contact others, buy data, or disclose credentials.

## Team

Use exactly three research agents:

- Head: GPT 6.1 Sol, medium reasoning (`gpt-6.1-sol`). Own the hypothesis tree, research priorities, decisions, and adaptable plan.
- Coder: GPT 6.1 Terra, medium (`gpt-6.1-terra`). Implement, run, and summarize experiments. Do NOT stall on a few days of bad data: apply a simple documented patch and continue.
- Inspector: separate GPT 6.1 Terra, medium. Independently inspect each batch's coefficients, forecasts, metrics, and code outputs against primary literature and economic reasoning. Alert the head to anomalies; message the coder directly about suspected implementation/output errors. Reinspect corrected batches.

If the parent is not Sol medium, delegate the research head to Sol medium and let it spawn the two Terra agents; the parent only coordinates. Use `fork_turns="none"` with explicit model overrides and supply full task context. Verify actual model selections; do not silently substitute if unavailable. Coordinate file ownership and communicate directly. Inspection must recur after each substantive batch, not only at the end.

## First actions and current evidence

Verify hostname, remote repository path, git status, accessible data, Python environment, scheduler/site policy, and applicable AGENTS.md. Record the actual paths. No new prediction jobs have been started by the laptop team. The existing remote REPORT.md and runs may contain completed retrospective regressions: inspect them rather than relying on stale documentation saying nothing ran.

Read docs/regressions/{PREDICTION_IMPLEMENTATION_PLAN.md,PREDICTION_HYPOTHESIS_LEDGER.json,B04_CAUSAL_MECHANISM_CANDIDATES.md,B01_B04_RETROSPECTIVE_COEFFICIENT_TABLES.md,METHODOLOGY.md,DATA.md,FACTORS.md,CLUSTER.md,LITERATURE.md}, configs/samsung_regressions.json, src/samsung_research/regressions.py, and scripts/run_samsung_regressions.py. Existing expected EP01 path is runs/samsung/EP01_descriptive/20261022T070701_403388Z; verify it, do not assume it exists. Inspect existing remote runs before acquiring or reproducing data. Reuse existing pipeline components without a wholesale rewrite.

The discount is q=100(1-P/C), where P and C are comparable preferred/common prices. Positive change means widening. B04 is retrospective daily discount-change regression with Barra factor returns, lagged discount, and lagged log(preferred/common share volume). US BETA is a style factor, distinct from COUNTRY; LEVERAGE and DIVYILD are factor returns, not Samsung's leverage and dividends. Exact factor orientation requires documentation. Relative volume is an activity proxy, not observed liquidity or signed flow.

The laptop table's B04 main full-sample BETA is +13.15 (p=.015; BH q=.150), DIVYILD +25.65 (p=.025; q=.189), LEVERAGE -17.26 (p=.175). Post-2020 MOMENTUM is +13.69 (p=.003; q=.055). Dividend yield persists after adding activity in that table, contrary to informal notes. Reconcile with the actual source run. These are exploratory associations, not causal findings or proof of prediction.

Samsung's outstanding preferred shares are non-cumulative with an additional annual dividend of 1% of par value. The 2025 prospectus says they rank equally with common in liquidation. Do not assume US-style fixed-dividend senior preferred securities. Verify relevant historical class terms when needed. Sources: https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2024_4Q_Interim_Report.pdf and https://images.samsung.com/is/content/samsung/assets/global/ir/docs/Samsung_Final_Prospectus_20250210.pdf. Informal 40% Americas revenue and 7.5% US supply claims remain unverified.

## Priority and malleable implementation plan

Optimize genuine out-of-sample prediction of the discount; distinguish predictive usefulness from causal identification. Write a durable ranked plan and hypothesis/decision ledger before fitting, then update them after each batch. For each mechanism record chain, expected sign/timing, distinguishing prediction, rival, evidence, decision, and next experiment.

1. Establish persistence/zero-change and simple AR baselines. Assess discount mean reversion, recent changes/momentum, and volatility as predictive features; these are statistical benchmarks, not automatically causal mechanisms.
2. Prioritize class-relative demand and liquidity: begin with accessible class volumes/activity, then spreads/turnover/flows/borrow where accessible. Risk appetite may direct buying toward common; relative trading costs and constrained arbitrage may sustain the gap.
3. Add lagged global risk/style, FX, rates, and chip-cycle information with genuine forecast-origin availability. Fundamentals affecting both classes require a differential-class channel to explain the discount. Retrospective factor joins are not automatically forecasting inputs.
4. Test dividend clientele and known dividend/corporate-action calendars. Separate announced Samsung payouts from US DIVYILD factor returns. Equal cash dividends can mechanically widen the percentage discount with the absolute price gap unchanged; distinguish mechanical calendar effects from investor responses.
5. Explore class-specific buybacks/issuance/float and governance/voting events when sufficient relevant dated observations exist. Avoid broad event hunts or forcing scarce-event models.

Reorder based on accessible inputs, validated forecast improvements, inspector findings, and expected information value. Missing expensive data must not block independent batches. Record untested mechanisms as untested, not null. Do not prioritize long investigations of a handful of questionable days.

## Forecast protocol

Default origin: after Korean close t, using only information actually available then. Primary target q[t+1]-q[t]; secondary 5- and 20-session changes. Report implied level forecasts against q[t] persistence too. Confirm or revise horizons before validation based on remote inventory.

Freeze chronological train/validation/final-test date ranges and a compact candidate registry before fitting. Use expanding/rolling origin evaluation, training-only imputation/scaling/selection, and strict label-end purging for overlapping horizons. Keep the final holdout sealed until the shortlisted design is frozen; do not repeatedly mine it. Account for information revealed during earlier retrospective research when describing holdout independence. Start with small linear/AR models, then a small regularized extension if justified. Compare on identical forecast origins against zero change/persistence and AR; report MAE, RMSE, out-of-sample R-squared, sample sizes, regime stability, and dependence-aware uncertainty. In-sample significance is not the selection criterion. A no-improvement finding is a valid result.

## Patch and inspection policy

For isolated invalid observations, choose a cheap predetermined handling rule (e.g. mark invalid, omit affected labels, training-only predictor imputation with missingness indicator). Record dates, reasons and method; preserve raw data. No future-value interpolation, backfilled announcements, invented outcomes, or silently bridged missing sessions. If useful, run one cheap sensitivity. Escalate systematic class mapping, units, factor timing, leakage, or widespread corruption to the head; these are material research errors.

After each batch coder provides run path, configuration, sample dates, patches, metrics/coefficient summary, and logs. Inspector checks arithmetic, units, timing, baseline comparisons, leakage, unexpected signs, large improvements, instability, and relevant primary literature. Head triages anomalies as fix-now, bounded follow-up, or deferred with reason. A strange but valid market move alone is not grounds for deletion. Preserve exploration history and reserve new unexposed validation data if a post-test change is pursued.

## Execution and completion

Run empirical research on authorized remote compute, using Slurm where site policy requires. Reuse existing environments and scheduler configuration; do not guess account, partition, or paths. Avoid duplicate jobs. Verify accepted job IDs and scheduler state; report submitted/running/completed accurately. Preserve failures in separate run directories. Meaningful synthetic checks should cover forecast timing, overlap purging and arithmetic.

Save plan, hypothesis tree, decision/patch logs, data inventory, frozen configs/code provenance, predictions, metrics, inspector findings, and a concise final research report in the remote repository/run directory. At each checkpoint summarize findings, changed priorities, and next action. Continue feasible prioritized iterations until the shortlist is evaluated and independently reviewed, or a specific external dependency prevents further useful progress. Do not promise that interactive agents survive disconnects: use scheduler jobs for durable compute and save exact resume instructions.

Begin by verifying the remote environment, creating the team, and writing the prioritized plan, then execute the smallest useful batch with the actual available data.
