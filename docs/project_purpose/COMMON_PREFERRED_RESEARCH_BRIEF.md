# Korean Common/Preferred Equity Research Laboratory

## Instructions to the AI working in this repository

Act as a mathematical equities researcher and research engineer. Read this brief and the repository's existing instructions before changing anything. Inspect existing code and data without overwriting user work. First create a concrete, dependency-ordered infrastructure and experiment plan; then implement the minimum infrastructure needed and execute the experiments as data becomes available. Do not stop at writing a plan when execution is possible. Do not build a large platform before producing the first validated figure.

Work in this order: inspect repository and data → document assumptions and coverage → validate one pair → produce descriptive figures → test hypotheses → expand across pairs → predictive evaluation. Infrastructure serves those steps. If a source requires a human export, specify exactly what to export, document the dependency, and continue independent work. Never invent data or imply that unavailable experiments have run.

This file is the project specification, not evidence that any dataset, figure, infrastructure, or experiment already exists. No empirical results are established here. The immediate deliverable is a reproducible Samsung figure pack and a clear account of what the observations support, contradict, or leave unresolved.

## 1. Objective and scope

Study why Korean preferred/nonvoting equity trades at different prices from common/voting equity in the same company. Build intuition through readable graphs before fitting complex models. Determine which mechanisms explain the level, changes, and persistence of the gap; later assess whether the gap predicts the relative benefit of owning one class.

Begin with Samsung Electronics' Korean local common and preferred listings (KRX codes 005930 and 005935; independently verify security identifiers and mappings). Aim for daily history from 2005 onward where available, with later starts for datasets with shorter coverage. Add other Korean pairs after the first pipeline works. Keep delisted classes when designing a broader historical sample to reduce survivorship bias.

This branch excludes holding-company NAV research, including Prosus/Tencent. Do not generalize US fixed-income-like preferred-stock assumptions to Korean preferred equities. Read each issue's actual terms.

Use “preferred-share discount” for the observed price ratio. “Voting-rights discount” or “vote value” describes an explanation to investigate, not the entire observed gap by assumption. A single company's time series cannot identify the causal value of votes independently of all other class differences.

## 2. Initial hypothesis tree

Maintain stable IDs even when labels or views change. Distinguish mechanisms creating a gap from constraints allowing it to persist. Interactions are permitted; the tree is an organizing device, not an additive accounting identity.

| ID | Branch / hypothesis | Initial observable implication | Important competing explanation |
| --- | --- | --- | --- |
| H0 | Measurement artifacts | Apparent jumps disappear after correcting splits, stale prices, timestamps, or dividends | Real class-specific repricing |
| H1 | Votes and control | Gap changes when minority votes become pivotal: contested votes, activism, changing ownership blocks | News changes expected cash flows or investor demand |
| H2 | Different cash-flow and legal rights | Relative pricing responds to incremental dividends, priority, conversion, redemption, or contingent voting terms | Ex-dividend mechanics and liquidity |
| H3 | Relative liquidity | Preferred discount tends to increase when preferred trading costs worsen relative to common | Discount changes themselves affect trading activity |
| H4 | Investor clientele and flows | Relative net buying, index demand, and ownership shifts accompany class-relative repricing | Investors respond to a gap rather than cause it |
| H5 | Limited arbitrage | Gaps persist longer when the expensive class is costly or impossible to short | Borrow demand and fees rise in response to the same gap |
| H6 | Class-specific corporate actions and supply | Repurchases, cancellations, issuance, and free-float changes affect relative pricing | Management targets an already large discount |
| H7 | Market state and shared demand | Discounts move with market stress, firm valuation, volatility, or a Korean share-class factor | Mechanical common-price input or shared firm fundamentals |

Possible interactions: H3 × H5 (illiquidity and constrained arbitrage), H4 × H5 (flows with limited correction), H6 × H3 (repurchases reduce float and liquidity), H1 × H4 (governance news attracts investors). Better shareholder protection need not have a universally signed effect on the gap: it may reduce private control benefits while increasing minority voting effectiveness.

## 3. Non-negotiable methodology documentation

Create and maintain BOTH `docs/METHODOLOGY.md` and `methodology/methodology.json`. They must explain exactly how every published number and figure was produced. Documentation is part of completing an experiment, never deferred cleanup. A result is incomplete if its calculation cannot be reconstructed from the documentation, code, inputs, and run record.

Use JSON as the canonical registry for structured calculation specifications and parameters. Generate matching tables/sections in Markdown from that registry where practical; maintain interpretive prose separately in the same Markdown file. Avoid conflicting independent definitions. Add a consistency check between registered IDs/versions and the Markdown. JSON must be valid, schema-validated JSON without comments, NaN, or Infinity.

For EVERY measure, transformation, model, test, and figure, record:

1. Stable ID, name, purpose, hypothesis links, specification version, status, and author.
2. Exact mathematical definition, symbol definitions, units, sign convention, numerator/denominator, economic interpretation, and what it does not measure.
3. Input dataset IDs, vendor and exact field names, security identifiers, source URLs or export references, extraction query/overrides, and source documentation.
4. Frequencies, market timezone, calendar, close/quote timestamps, alignment/join rules, and treatment of nontrading days.
5. Corporate-action and dividend treatment; split factors; raw versus adjusted prices; share-count and free-float conventions; currency and scaling.
6. Exact sample and eligibility filters, exclusions, missing-value rules, stale-price rules, outlier handling, minimum observations, and coverage limitations.
7. Window definition in trading observations versus calendar time, trailing versus centered calculation, lags, minimum periods, weighting, and annualization/day-count conventions.
8. Effective date, publication/availability date, retrieval time, revisions, and point-in-time assumptions. Unknown publication dates must be explicit; a current restated history is not automatically point-in-time data.
9. Code module and function, configuration, meaningful validation checks, tiny hand-calculated example, and known limitations.
10. For statistical tests: estimation target, controls, horizon, inference method, dependence/overlap handling, selection procedure, and whether exploratory or prespecified.
11. For figures: exact series and transformations, scales, smoothing, axes, annotations, event dates, sample, units, and output IDs.
12. For each change: previous version, date, reason, initiating observation/decision, affected experiments, and whether prior outputs need rerunning.

When uncertain, write an explicit unresolved decision with an owner and next action rather than silently choosing. Reasonable implementation choices may proceed if labeled provisional and documented. “Adjusted price,” “liquidity,” “borrow cost,” or “return” without a precise definition is insufficient.

### Required methodology registry shape

The implementing AI should create a JSON Schema and extend this structure. This is a minimal illustrative entry, not the complete registry:

```json
{
  "schema_version": "1.0.0",
  "methodology_version": "0.1.0",
  "updated_at": null,
  "measures": [
    {
      "id": "preferred_discount",
      "version": "1.0.0",
      "status": "specified_not_executed",
      "hypothesis_ids": ["H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7"],
      "formula": "1 - preferred_close / common_close",
      "inputs": ["preferred_close", "common_close"],
      "unit": "fraction",
      "display_unit": "percent",
      "sign_convention": "Positive means preferred is cheaper than common",
      "frequency": "daily",
      "calendar": "verified Korean local exchange calendar",
      "timezone": "Asia/Seoul",
      "join": "Same local trading date; both prices valid and comparable",
      "price_basis": "Contemporaneous prices per comparable economic share; verify corporate actions",
      "missing_policy": "Missing if either required price is missing or nonpositive; no automatic forward fill",
      "input_dataset_ids": [],
      "availability_policy": "Document actual field timing before predictive use",
      "implementation_ref": null,
      "validation_refs": [],
      "limitations": ["Observed class-price gap is not an identified causal value of votes"]
    }
  ],
  "models": [],
  "figures": [],
  "decisions": [],
  "change_log": []
}
```

Null means explicitly unresolved, not an invitation to fabricate a value. Execution must require completion of the fields relevant to the calculation. A run must snapshot the exact methodology registry used, so later edits never change the interpretation of archived results.

## 4. Core measures and calculation requirements

### 4.1 Price gap and relative performance

For comparable common price C_t and preferred price P_t:

- Fractional discount: d_t = 1 − P_t/C_t. Display 100d_t percent; changes in this display are percentage points.
- Absolute gap: G_t = C_t − P_t, in KRW per comparable share.
- Common premium relative to preferred, if used: v_t = C_t/P_t − 1 = d_t/(1−d_t). Do not confuse the different denominators.
- Log gap: g_t = log(C_t/P_t) = −log(1−d_t).
- Exact identity: Δg_t = Δlog(C_t) − Δlog(P_t), using consistently adjusted price returns across corporate actions. This explains which class moved; it is not causal evidence.
- Separately plot indexed price performance and dividend-reinvested total-return wealth. Normalize each wealth series to 100 at the same valid initial date.
- Relative cumulative wealth: W_P,t / W_C,t − 1, where each W begins at 1. This is a relative wealth ratio, not the return of a self-financing long-short strategy.
- Future ownership comparison: total return of preferred over horizon minus total return of common over the same horizon. Define dividend reinvestment and horizons exactly.

Use contemporary, economically comparable share prices for the price ratio. Do not substitute independently dividend-adjusted historical prices into a historical spot-discount calculation. Keep raw prices and adjustment factors. Detect changes in per-share economic entitlements from splits, mergers, or conversions. Do not forward-fill absent trades without a separately documented sensitivity analysis.

### 4.2 Valuation and business conditions

Plot the discount against firm valuation, earnings yield, book equity, profitability, leverage, and operating results where useful. Document how issuer-level earnings/equity are allocated across classes before computing per-share multiples or aggregate market capitalization. Preferred/common multiples cannot be compared naively when vendor allocation conventions differ. Handle negative earnings explicitly rather than presenting a nonsensical P/E.

Common price is in both d_t and many valuation multiples; common rising while preferred is unchanged can mechanically raise both the discount and common valuation. Show which class moved and include operating fundamentals that do not use the same daily price. Use both levels and changes with their different interpretations. Avoid interpreting a correlation in persistent levels as identification.

### 4.3 Liquidity

- Relative quoted spread per class: (ask − bid)/((ask + bid)/2). Require valid synchronized quotes; document quote time and whether the observation is a closing snapshot or intraday average.
- Turnover per class: shares traded/free-float shares. If only shares outstanding are available, label that alternative denominator explicitly.
- Amihud proxy per class: trailing mean of |daily return|/daily traded value. State the return definition, KRW scaling, window, and positive-volume requirement. Zero-volume observations require a separate rule, not division by zero.
- Nontrading-day rate, zero-return rate, and stale-close indicators. These are related but different concepts.
- Compare levels for each class and preferred-minus-common differences or ratios. For log ratios, require strictly positive inputs and document how zero observations are handled.

Start with a documented trailing 20-trading-observation window where appropriate; show unsmoothed data or alternate windows as sensitivity checks. Amihud is a price-impact proxy and not an observed execution cost. Volume, free float, spread, and turnover are not interchangeable.

### 4.4 Borrowing and short-sale constraints

Obtain for BOTH classes: annualized borrow fee and its precise vendor definition, lendable inventory, shares on loan, utilization, and security-level short-sale eligibility. Record whether fees are lender-side averages, new-loan fees, indicative benchmarks, or investor-facing costs. Do not silently splice different fee concepts.

When preferred is cheap, the usual relative trade buys preferred and shorts common. Common borrow conditions therefore constrain this direction. If preferred is expensive, reverse the relevant short leg. Absence of a loan observation does not mean zero fee or unlimited borrowability. A legal ban is not just a high fee.

Utilization must follow the vendor's exact inventory definition; document whether units are shares or market value and the sampling population. Shares on loan, reported short positions, and executed short-sale volume measure different things. None substitutes for an observed borrowing fee.

For a simplified constant-rate illustration, borrow expense ≈ short notional × annualized fee × elapsed days/day-count basis. Actual evaluation accrues on the specified daily short market value and fee path, includes dividend compensation and financing where appropriate, and handles unavailable inventory and restrictions. A price discount cannot be directly reduced by an annualized fee without a horizon and portfolio definition. Zero discount is not an assumed terminal fair value.

Build a historical class-specific policy/eligibility table including bans, partial resumptions, membership changes, exceptions, announcement dates, and effective dates. Verify exact rules from official sources; do not apply one country-wide indicator to all classes indiscriminately.

### 4.5 Buybacks, supply, dividends, and flows

- Buyback intensity B_j,t = trailing-window shares repurchased in class j / class j shares outstanding at the beginning of that window. Plot B_P,t − B_C,t.
- Buying pressure: repurchased shares / total shares traded over the same window; use compatible dates and venues.
- Keep authorizations, announcements, execution, treasury holding, cancellation, and reissuance distinct. A repurchase does not imply immediate cancellation.
- Track outstanding, treasury, free-float, and voting shares separately, each with source-specific definitions. Cancellation can change outstanding shares without removing additional shares from public float at that moment.
- Record actual dividends per comparable share, incremental preferred dividends, ex-dates, record dates, payment dates, and announcement dates. Samsung's incremental entitlement must be checked against its articles; do not interpret a percent of par as a percent of the ordinary dividend.
- Net buying by investor category: document shares versus KRW, class coverage, and normalization by beginning market capitalization/free float or trading value. Plot domestic institutional, retail, and foreign categories separately where coverage exists.
- Dividend-yield differences partly reflect the price ratio itself. They are useful descriptive measures, but not independent explanatory evidence by construction.

## 5. Experiment and figure backlog

Each figure needs an experiment ID, hypothesis links, caption, methodology version, data coverage, and run manifest. Use aligned time panels for overlays; avoid arbitrary dual axes. Add scatterplots/binned averages where they reveal a relationship. Clearly label units, smoothing, missing periods, and events. Never use simulated data in empirical figures; any demonstration with synthetic data must be conspicuously labeled.

| ID | Required output | Core question / implementation detail |
| --- | --- | --- |
| E01 | Discount history; indexed class prices; total-return wealth | Level, persistence, reversals, which class moved; compare daily versus weekly views |
| E02 | Discount with valuation and operating fundamentals | Valuation state versus discount; flag common-price mechanical overlap |
| E03 | Liquidity panels, relative measures, scatter/binned plots | Is widening associated with deteriorating preferred liquidity relative to common? |
| E04 | Borrow fees, inventory, utilization, eligibility by class | Does inability to short the expensive class accompany larger gaps? |
| E05 | Subsequent convergence by borrowing-constraint state | Compare similar initial gaps; distinguish fee changes preceding versus following gap changes |
| E06 | Repurchases by class and relative intensity | Separate announcements from execution; consider management responding to the discount |
| E07 | Treasury shares, cancellation, issuance, and free float | Supply and liquidity consequences; do not double count repurchase/cancellation |
| E08 | Dividends and rights; ex-dividend event panels | Cash-flow differences and mechanical price adjustments |
| E09 | Investor flows and ownership by class | Which investors buy the appreciating class; lead–lag and reverse causality |
| E10 | Index changes and governance/control events | Event-time discount changes; confounding firm news and pre-event trends |
| E11 | Market/firm returns, volatility, stress regimes | Conditional behavior in rallies/selloffs; distinguish price identities from mechanisms |
| E12 | Initial discount versus future relative total returns | 1, 3, 6, 12 calendar-month ownership horizons with explicit trading-date mapping |
| E13 | Multi-pair discount heatmap and change correlations | Common Korean component versus company-specific movement; shared missing-data rules |
| E14 | Feasible long-short evaluation, gross/net, versus baseline | Later stage only; separate prediction from executable returns and outright ownership choice |

First milestone: E01–E04 and E06 where data supports them, plus a coverage report. If lending data is blocked, produce the other figures and clearly separate constraint proxies from actual fee analysis.

For each question follow: descriptive time series → scatter/binned summary → lead–lag comparison → event analysis where defensible → small conditional model. Do not run every combination of every metric and horizon without logging the search. Record null, contradictory, and inconclusive results as carefully as favorable ones.

Quantify effects in interpretable units, such as percentage-point discount differences per stated liquidity deterioration, with confidence intervals. Examine discount levels, changes, and subsequent relative returns as different outcomes. Avoid predicting an outcome with a variable constructed directly from the same prices without acknowledging the mechanical dependence.

For convergence, distinguish movement toward zero, movement toward a rolling historical anchor, and predicted relative returns; none is automatically the same economic target. Estimate a half-life only if the process specification and stability diagnostics justify it. A wider gap need not close.

For formal models: address serial dependence, heteroskedasticity, overlapping forward horizons, persistent regressors, and small samples. Use a justified dependence-aware inference method (for example specified HAC settings or block bootstrap); log its exact settings. Panel inference must account for within-pair and common-time dependence where sample size supports it. Event studies must distinguish announcement/effective dates, identify overlapping news, inspect pretrends, and state when evidence remains descriptive. Regulatory changes alone do not guarantee an exogenous causal experiment.

Prediction comes after descriptive validation. Use chronological training/validation/test splits or walk-forward evaluation, with overlapping-label leakage controlled. Calculate baselines using information available at the decision time. Compare models on the same sample and execution assumptions. Log all tested variants; changes after looking at outcomes are exploratory. Do not reuse a previously examined holdout as untouched evidence.

## 6. Data acquisition and audit

User has BYU access to WRDS (including CRSP, Compustat, Capital IQ, etc.) and Bloomberg. Exact entitlements and coverage remain unverified. Do not assume US CRSP covers Korean local shares, that Compustat means Compustat Global is licensed, or that Capital IQ access includes S&P Securities Finance. Prefer existing usable extracts before requiring duplicate downloads.

| Block | Required inputs | First route | Validation / fallback |
| --- | --- | --- | --- |
| Identity and rights | ISIN/local/vendor IDs; class terms; listings and corporate actions | Company articles, filings, IR | Bloomberg reference data; Korean filings |
| Market history | Raw close, adjustment factors, dividends, total returns, volume, traded value, shares | WRDS Compustat Global Security Daily if entitled | Bloomberg; KRX |
| Liquidity | Bid/ask with timestamps; float; trading activity | Bloomberg historical quote/float coverage audit | KRX; documented daily proxies |
| Lending | Fee definitions, supply, loans, utilization, both classes | WRDS S&P Global/Markit Securities Finance entitlement check | Bloomberg historical entitlement/coverage check |
| Short activity and rules | Short volume/value, reported balances, class eligibility | KRX; Financial Services Commission | Bloomberg |
| Corporate actions | Class-level authorizations, purchases, cancellations, treasury and issuance | Company and Korean regulatory disclosures | Bloomberg event data |
| Fundamentals | Earnings, equity, profitability, leverage and publication dates | Compustat Global; Capital IQ | Company filings; Bloomberg |
| Ownership/flows | Blocks, holdings history, investor-category class flows | KRX flows; Capital IQ/Bloomberg ownership audit | Company disclosures |
| Events/controls | Index history, votes/activism, rates, market returns | Official notices; Bloomberg | KRX; company disclosures |

At Bloomberg use the field search/documentation and a small test export before choosing exact field mnemonics. Verify historical rather than current-only fields, adjustment overrides, units, fee conventions, and export availability. Never invent terminal fields or promise unavailable history. Ask the human for the documented export only when necessary.

Create `docs/DATA_ACQUISITION.md` and a machine-readable source inventory with: source ID; field mapping; security mapping; license/redistribution status; extraction instructions/query; file hash; retrieval date; units; earliest/latest usable date per class; missingness; publication timing; unresolved issues. A vendor product description is evidence of a product's existence, not BYU's access or pair-level coverage.

Acquisition sequence:

1. Inspect existing extracts and entitlements; check lending access early because it is a likely bottleneck.
2. Get a small overlapping sample for both classes; verify identifiers, dates, prices, volume units, and actions against another source.
3. Download the core market history. Preserve source bytes and export settings unchanged.
4. Build class-aware normalized tables; publish a field-level coverage matrix and quality report.
5. Validate historical discount dates and suspicious jumps, including split periods and ex-dividend dates.
6. Add liquidity, lending, class-level buybacks, flows, and events incrementally. Never silently substitute another concept for unavailable data.
7. Extend to additional pairs using explicit historical eligibility and rights rules.

Use stable internal issuer, security, and pair IDs. Maintain dated identifier mappings and separate issuer-level fundamentals from security-level observations. Every observation should carry or resolve to source, effective date, availability date, and ingestion lineage. Never merge common and preferred simply on issuer ID and date if that duplicates or overwrites class records.

## 7. Infrastructure planning requirements

Inspect the actual repository first. Propose the smallest maintainable Python-oriented design compatible with its existing tools; no framework migration or orchestration service without a demonstrated need. Code should be modular, with notebooks used for exploration rather than being the only home of calculations. CSV/manual vendor exports are acceptable first-class ingestion routes. Do not require live vendor credentials for plotting already downloaded data.

Suggested logical outputs (adapt locations to the repository while preserving responsibilities):

| Path | Responsibility |
| --- | --- |
| `docs/RESEARCH_PLAN.md` | Dependency-ordered milestones, acceptance criteria, blockers, next actions |
| `docs/METHODOLOGY.md` | Complete human-readable calculations and analytical decisions |
| `methodology/methodology.json` and schema | Structured, versioned calculation/model/figure registry |
| `docs/HYPOTHESES.md` and `research/hypotheses.json` | Current tree, predictions, evidence links, uncertainty, revisions |
| `research/observations.jsonl` | Append-only human/AI observation ledger |
| `research/decisions.jsonl` | Decisions, rationale, alternatives, and superseded choices |
| `research/experiments/` | Versioned experiment configurations and outcome summaries |
| `docs/DATA_ACQUISITION.md` | Vendor export instructions, verified coverage, missing requests |
| `data/` or external configurable data root | Immutable raw extracts and derived tables, excluded from public Git where licensed |
| `src/` | Ingestion, validation, transformations, experiments, plotting |
| `configs/` | Pair definitions, paths, settings, model and figure parameters |
| `tests/` | Meaningful arithmetic, corporate-action, temporal-integrity, schema and integration checks |
| `runs/` | Immutable manifests, methodology snapshots, result tables, figures and summaries |

These are required responsibilities, not a requirement to create empty folders or duplicate documents. Avoid infrastructure that does not contribute to the first milestone.

Implement reproducible environment/dependency locking, configurable local data paths, and simple documented commands to validate inputs, build measures, run named experiments, and regenerate figures. First make a one-pair path work end to end. Use lightweight CI to validate code, JSON schemas, metadata consistency, and small synthetic fixtures without vendor access. Synthetic fixtures are for tests only, not empirical findings.

Minimum meaningful checks: hand-calculated discount/premium/log-gap identities; split/corporate-action comparability; total-return arithmetic; class-aware joins; no duplicate security/date rows; nonpositive/invalid prices; return/traded-value units; missing versus zero fees; no future observations in trailing windows; availability-date leakage; simple daily borrow accrual; methodology/config registry consistency. Do not add redundant tests that merely repeat implementation code.

Every run manifest must include run ID/time, experiment/config version and hash, Git commit and dirty-state/patch reference where relevant, environment/lockfile reference, input file hashes and source IDs, methodology snapshot/hash, sample/filters, random seed if used, warnings/coverage, code entry point, outputs, and execution status. Reuse cached outputs only when dependencies match. Retain failed-run diagnostics. Use immutable run directories rather than overwriting prior evidence.

Keep licensed data and restricted exports outside public Git; configure ignores before ingestion. Verify applicable licenses before distributing derived data or charts. Never commit credentials. Do not publish a repository or transmit data to another service without authorization. Local implementation and local experiments are authorized by this brief.

## 8. Living hypothesis and methodology workflow

Human observations and AI observations must enter the same traceable process. Do not treat either as established fact without supporting evidence.

For every meaningful observation:

1. Append an observation with stable ID, timestamp, author type/name, exact claim, pair/date window, figure/run IDs, data references, supporting detail, and whether it is visual, statistical, institutional, or speculative.
2. Link affected hypothesis IDs. Record competing explanations and what new evidence would distinguish them.
3. Classify impact as motivation, supportive association, contradictory association, measurement concern, or credible causal evidence. Avoid upgrading correlation into causation.
4. Propose the smallest next experiment. Record whether it was specified before looking at its outcome.
5. Update the tree's current summary and evidence links. Add/split/merge branches when necessary, preserve original IDs or explicit supersession links, and never silently delete failed hypotheses.
6. If calculations change, update BOTH methodology representations, increment the affected specification version, record why, identify affected runs, and regenerate outputs under a new run ID. Keep the old result and mark it superseded where appropriate.
7. After execution, append results including nulls, limitations, and updated confidence. Add the current best next step to the research plan.

Each hypothesis record needs: ID, parent, claim, mechanism, expected sign or reason the sign is ambiguous, measurable predictions, required data, identification risks, evidence and observation IDs, experiment IDs, status, qualitative confidence with justification, created/updated times, and supersession history. Useful statuses: proposed, specified, data-blocked, testing, evidence-supports, evidence-conflicts, inconclusive, superseded. “Supports” never means proven.

Each methodology change needs a decision record. Separate (a) correcting an error, (b) changing a scientific assumption, and (c) adding an exploratory alternative. Record the before/after formula or parameter, reason, observation/issue that triggered it, and impact on prior conclusions. Never choose the preferred specification solely because it improves significance or returns. Report material sensitivity across defensible alternatives.

At each working-session start, read the brief, research plan, current hypothesis tree, methodology version, and recent ledger entries. At each session end, update completed work, reproducible run references, unresolved blockers, and the next action. This enables a new AI or human to continue without relying on conversation memory.

## 9. Milestones and acceptance criteria

### M0 — Repository audit and plan

Deliver a concrete infrastructure/experiment plan identifying what already exists, minimal changes, data dependencies, commands, and acceptance criteria. Initialize the documentation/registries with the hypotheses and calculations in this brief. Mark unresolved source details explicitly. Do not represent planning as empirical progress.

### M1 — Validated core pair

Deliver security/rights mapping, source inventory, class-level coverage report, normalized market history, and E01. Reconcile selected observations against independent source evidence. Explain every material discontinuity investigated; preserve unresolved flags. One command should regenerate the figure from configured local extracts.

### M2 — First hypothesis figure pack

Deliver E02–E04 and E06 where inputs exist; supply explicit blockers for missing series. Every figure has labeled units, period, definitions, hypothesis references, methodology and run IDs, a short observation, alternative explanations, and a proposed next test. Include the relative liquidity measures and actual borrowing-fee analysis when available. Do not stop other experiments because one vendor dataset is unavailable.

### M3 — Quantified exploratory evidence

Run selected binned comparisons, lead–lag tests and carefully chosen event studies; then small conditional models. Save estimate tables, uncertainty, sensitivity, all attempted specifications and updates to the tree. Prioritize the strongest observations rather than exhaustive model mining.

### M4 — Generalization and prediction

Expand across documented Korean pairs; study common discount changes and firm-specific behavior. Evaluate chronological predictions against a rolling historical baseline, then feasible gross/net relative trading outcomes if data supports execution assumptions. Keep forecast accuracy, explanatory fit, outright ownership returns, and long-short returns separate.

## 10. Evidence and source starting points

These are leads from the prior literature review, not independent confirmation of any effect in our sample. Verify paper details and methodology before adopting a result. Record whether full text or only an abstract was inspected. Add exact supporting passages/page references to the literature notes when available; do not overstate consensus.

- Chung & Kim (1999), *Corporate Ownership and the Value of a Vote in an Emerging Market*: ownership/control branch. https://www.sciencedirect.com/science/article/abs/pii/S0929119998000145
- Chay & Moon (2005), *Discount Pricing of Preferred Stocks to Common Stocks: The Role of Liquidity Premiums*: relative-liquidity branch. https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART001103943
- Yang & Ryu (2021), *Investor Sentiment and Price Discrepancies between Common and Preferred Stocks in Korea*: demand/sentiment branch. https://www.mdpi.com/2071-1050/13/10/5539
- Amihud (2002), *Illiquidity and Stock Returns: Cross-Section and Time-Series Effects*: daily illiquidity proxy. https://www.sciencedirect.com/science/article/pii/S1386418101000246
- Samsung investor relations: https://www.samsung.com/global/ir/
- Samsung shareholder returns: https://www.samsung.com/global/ir/stock-information/shareholder-return/
- WRDS Compustat Global overview: https://wrds-www.wharton.upenn.edu/pages/grid-items/compustat-global-wrds-basics/
- WRDS former Markit routing: https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/markit/
- S&P Securities Finance product: https://www.spglobal.com/market-intelligence/en/solutions/products/securities-finance
- KRX Data Marketplace: https://data.krx.co.kr/contents/MDC/MAIN/main/index.cmd
- FSC 2021 partial resumption announcement: https://www.fsc.go.kr/eng/pr010101/75835
- FSC March 2025 resumption information: https://www.fsc.go.kr/eng/pr010101/84220

Do not restart a broad literature review before producing the first figure. Consult focused sources when needed to resolve a calculation, class term, data definition, or identification question.

## 11. First action after reading this file

Inspect the repository and any existing datasets, then write the M0 plan. Identify the smallest missing export needed for E01 and check lending access in parallel with other independent preparation. Implement the minimal one-pair ingestion/validation/plotting path. Keep the methodology, hypothesis tree, and observation ledger current from the first calculation onward. Finish with a concise report of files changed, experiments actually run, figure/run references, findings with uncertainty, and the next concrete action.
