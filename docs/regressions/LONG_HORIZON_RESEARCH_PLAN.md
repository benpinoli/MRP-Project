# Active plan: Samsung preferred discount over 2, 5 and 10 years

User direction, November 5, 2026. This supersedes next-session forecast selection and daily-reversal work as the active research objective. Existing results, IDs, configurations and frozen runs remain historical evidence. No new empirical study has been executed as part of this reorganization. Agents are on user-requested hold pending review; do not restart agents or submit jobs merely because this plan exists.

Read [the literature synthesis](LONG_HORIZON_LITERATURE.md) and [the reorganized tree](PREDICTION_MECHANISM_TREE.md). The filename retains its historical `PREDICTION_` prefix for compatibility; its active scope is now long-horizon explanation.

## Question and outputs

Explain why Samsung preferred shares trade at persistently different discounts across multi-year periods and what documented structural changes could sustain narrowing or widening over 2, 5 and 10 years. Do not force an exact price target or a positive forecasting result.

Deliver: (1) an honest history of persistent discount states and their duration; (2) dated histories of the leading economic mechanisms; (3) a table of what each mechanism explains, fails to explain, or cannot yet be tested; (4) conditional 2/5/10-year scenarios with observable signposts and reasons to reject them. A scenario is an economic argument conditional on a change, not a fitted 10-year forecast with artificial precision.

## Reordered tree and economic priority

Priority is a research judgment from economic fit and literature, not a probability that a branch is true. Data accessibility can affect execution sequence without changing scientific priority.

| Priority | Track | Main question and distinguishing evidence |
|---|---|---|
| 1 | LH1: Public share supply and trading capacity | Has preferred supply available to ordinary investors shrunk relative to common over years? Does the discount track worse trading costs/capacity, or does scarcity and buying support dominate? Use shares, holder blocks, treasury, executed class actions and sustained trading measures together. |
| 2 | LH2: Durable investor demand and access | Has the investor base shifted toward common or preferred through foreign/institutional holdings, index treatment, mandates, or retail participation? Track ownership stocks separately from trading flows. Evidence must be class-specific. |
| 3 | LH3: Control and governance | Has the relevance of common votes, control contestability, or protection against unequal treatment changed? Reconstruct controller/affiliate and independent blocks; distinguish protection of cash claims from increased voting power. |
| 4 | LH4: Payout policy and actual cash received | Did sustained payout commitments and their delivery change demand for preferred? Compare announced policy, actual cash per class, coverage and credibility across policy eras; separate price-discount change from the return earned by holding each class. |
| 5 | LH5: Class structure and market integration | Is there a verified path toward broader access, equalized rights, class unification or lower receipt frictions? Distinguish currently effective rules from proposed or hypothetical changes. No assumed Samsung conversion catalyst. |
| Cross-cutting | LH6: Why the gap can persist | Can investors finance and maintain the relevant relative-value positions, borrow common and exit at known terms? Are legal differences and lack of a terminal date enough to defeat a convergence thesis? Establish these conditions before interpreting persistence as irrationality. |
| Conditional | LH7: Company and economic cycles | Do chip cycles, cash generation, rates or exchange rates affect class demand/payout/trading capacity differently? Without an observed class-specific link, better Samsung fundamentals are an explanation for both prices, not their ratio. |

Measurement is a prerequisite. Daily reversal, day-to-day sentiment, closing-price timing and short-window forecast rankings move to an archived/supporting section. A short event window can date a mechanism, but its relevance to this project requires a sustained effect or a structural change.

## Data design

- Keep the paired daily source untouched. Build a monthly mean discount from valid same-day ratios, recording coverage and full/missing-month flags; do not divide separately averaged common/preferred prices. Use quarterly means of available qualified monthly means with an explicit complete-quarter rule and a quarter-end sensitivity. No daily forecast pipeline rewrite is needed.
- Build 24/60/120-calendar-month endpoint changes on qualified monthly endpoints; report available counts, overlapping periods and non-overlapping comparisons. For each horizon distinguish a change in the terminal discount from the average discount along the holding period. Do not silently substitute trading-day counts or invent endpoints.
- Ownership, shares, cash distributions and policy evidence belong at their actual reporting frequency. Save reporting period, effective date, first-publication date, retrieval date, units, class mapping and source. Annual values repeated across 252 days remain one annual observation. Use only known-at-date inputs for prediction; distinguish subsequently reported facts used for historical explanation.
- Publicly tradeable shares are not simply all issued shares. Separate outstanding/issued, treasury, controller/affiliate blocks, lockups, strategic holdings and shares underlying receipts using documented definitions without double subtraction. Separate authorized repurchases, actual executions, treasury cancellation and employee disposals; reconcile class counts around splits.
- Collect policy, ownership and supply history across the longest credible span, ideally 2005 onward. Start with issuer annual/interim and governance reports and dated announcements; the current six disclosures are a seed, not a sufficient longitudinal panel. Use accessible school data for historical class ownership, liquidity and peers where present. Do not mislabel missing holdings as zero or total trading as investor net demand.
- Start with directly observable costs/capacity when available: monthly quoted spreads/depth or compatible effective costs, turnover relative to documented public float, and scaled price impact as a separately named proxy. Market capitalization and dividend yield reuse prices; treat their mechanical relationships with the discount explicitly.

## Research sequence after the user resumes agents

**A. Construct the long-run map.** Reuse existing paired prices to plot monthly/quarterly discount level and show 2/5/10-year movements with sparse-data warnings. Reconcile the recent reversal findings as a different timescale. Add dated structural facts selected independently of price jumps. Use stated policy dates and data-driven break descriptions separately; neither proves a cause.

**B. Build the joint supply–ownership–trading history.** This is the primary acquisition and interpretation task. For each class assemble quarterly/annual share counts, public-share estimates, key owner blocks, relevant institutional/foreign participation and available cost/capacity measures. Plot them alongside the discount, with gaps visible. Do not let one unavailable flow API block public multi-year supply and ownership reconstruction.

**C. Reconstruct payout and governance regimes in parallel.** Begin the policy chronology with dated 2015 and 2017 source announcements already identified in the literature memo; add earlier/later periods and implementation from primary reports. Management explicitly responded to the discount in 2015, so later narrowing cannot be treated as the effect of an independent random policy shock. Track control/affiliate changes and relevant legal implementation dates only after verifying historical terms.

**D. Run mechanism-specific tests.** Choose a small question before estimating: e.g. does sustained relative trading deterioration accompany a wider discount after accounting for public supply, or does a durable investor-base shift coincide with a persistent repricing? Compare effects at quarterly/yearly scale and alternative multi-year periods. Prefer one informative observable channel to a large combination of correlated ratios. Analyze policy episodes for effects over subsequent quarters/years with anticipation, concurrent news and management response documented.

**E. Use peer pairs when identification needs them.** Add a manageable set of Korean common/preferred pairs with verified rights and adequate history. Compare Samsung with peers or changes across more/less exposed firms; report persistent firm differences and shared date effects separately. Include delisted classes when feasible and disclose selection. Common national reforms can affect both classes and the whole market; they are not automatically causes of Samsung's relative gap. A peer control must not include Samsung in its own aggregate. Broad common time effects also absorb common macro variables, so any remaining macro claim needs its identifying variation stated.

**F. Turn results into horizon-specific scenarios.** For two years emphasize existing policy implementation, investor allocation and current trading capacity. At five years emphasize cumulative class supply, payout credibility, ownership and institutional participation. At ten years emphasize durable governance, class rights, market integration and credible structural change. For each: widening/narrowing/no-change case, assumptions, discriminating signposts, what would invalidate it, and uncertainty. Do not assign probabilities or a numeric terminal discount without an estimable and disclosed basis.

## Estimation and interpretation safeguards

Persistent series can appear related just because both trend. Plot levels and changes, inspect broad periods, compare transformations and assess whether any claimed stable relationship survives regime changes. A model that adjusts toward a long-run relation is appropriate only if that relation is independently supported; the failed daily fixed-anchor design neither proves nor disproves it. Do not regress a long list of trending levels and declare causality from conventional significance.

Use quarterly/annual information for a small model only after counting independent changes and checking the measured channel. With approximately two decades of one firm's data there are roughly two non-overlapping ten-year stretches. Monthly overlapping long-horizon outcomes are highly dependent; narrower intervals from pretending otherwise are false precision. Peer comparisons can add information but require comparable rights and source definitions. State when results are descriptive associations rather than identified causal effects.

Do not use the common/preferred yield difference computed from the same cash amounts/prices as if it independently explained the discount. Do not treat changes in market-value leverage as independent balance-sheet shocks. Shared earnings or firm value must enter through an explicit differential-class channel. Cash-inclusive relative performance and terminal discount are distinct outcomes; verify adjustment and reinvestment conventions before calculating the former.

## Roles, progress and stopping

After resumption retain Head Sol medium, Coder Terra medium, separate Inspector Terra medium. Head maintains scientific rank and decides which observation could change a branch. Coder implements frequency-aware data tables and small tests, cheaply logs isolated bad rows and keeps going. Inspector checks primary-source interpretation, share/count arithmetic, sparse independent episodes, trends, reverse causation and the difference between both-price effects and class-relative effects. Review every substantive batch and communicate suspected code errors directly to coder.

Update the canonical tree after each batch. Preserve the original 40 stable IDs and all historical evidence; four added branches describe genuine missing long-run mechanisms, not arbitrary feature variants. Keep long-horizon status separate from old daily-test status. Stop a branch only with scoped evidence or a specific dependency; continue independent priority work. No requirement to find significance or an exact forecast.

The next reviewable deliverable is the long-run map plus a source/coverage matrix for supply, ownership, trading capacity, payout and control across years—not another one-day regression, a new short-reversal holdout, or the six-event short-window study alone.
