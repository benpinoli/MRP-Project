# Analyst review: regression anomalies, literature tensions and testable opportunities

Reviewed November 12, 2026. This is a separate analyst sweep anchored to
[the hypothesis tree](PREDICTION_MECHANISM_TREE.json). It preserves all existing
specifications, estimates and historical verdicts. No regression was refitted or
strategy optimized for this review. The [review inventory](LOOP_ANALYST_REVIEW_INVENTORY_20261112.csv)
records 61 aggregate tables across 16 completed research families plus two
v4 diagnostic tables, with paths, row counts and file hashes. Superseded/failed validation runs are provenance,
not independent replications. This review covers the registered completed
families and their substantive aggregate results, not a new reproduction of
every individual coefficient, forecast, source transcription or licensed row.

## Assessment

There is one confirmed dimensional reporting problem: the US LOOP strategy
diagnostic labels a cumulative-log drawdown as a percentage wealth drawdown.
There are also several results worth challenging: Berkshire's unusually strong
short-horizon diagnostic, Novo's persistent long-horizon wins, TSMC's large
2015–2019 change in adjustment speed, and News's opposite-signed spread
association. None currently establishes an executable arbitrage.

The sweep does **not** establish that our results overturn the literature.
Several apparent contradictions compare different outcomes: price-discount
changes versus returns, raw activity versus transaction costs, supply stocks
versus public float, and normalized holding-company prices versus NAV.
Separating those objects removes much of the apparent conflict. The strongest
remaining tensions are useful hypotheses for new data, not findings to force
into a preferred economic story.

## Ranked findings and falsification tests

### AR01 — Confirmed drawdown-label problem

**Tree:** M01, M02, B01, L02, L04. **Priority:** repair interpretation before any
trading claim. **Classification:** numerical units/label problem, not evidence
of an extraordinary market opportunity.

In `runs/loop_exceptions/15208094/results/trading_sensitivity.csv`, Volkswagen's
`gross_max_drawdown_pct` is **−238.1755**. The source
`scripts/run_loop_exception_tests.py`, in `walk_forward()`/`metrics()`, constructs
`wealth = series.cumsum()` and returns `100*(wealth-wealth.cummax()).min()`.
Here `series` is a signed difference of security log returns. The resulting
quantity is a drawdown in cumulative log-score units multiplied by 100, not a
proportional wealth loss. A conventional nonnegative wealth index cannot have
a drawdown below −100%.

For a diagnostic geometric index, `100*expm1(log_drawdown)` maps the units to a
proportional index drawdown. That does **not** turn a signed long/short log-return
difference into the log return of a funded, self-financing portfolio. Financing,
leg notionals, rebalancing, collateral and liabilities must be specified before
reporting portfolio wealth. The current high-watermark calculation also omits
the initial zero log-score; an initial-loss convention needs separate checking.

**Next test:** preserve the original field; publish a separately versioned
log-score drawdown and compounded-log-index interpretation, then construct a
fully specified marked-to-market long/short account before any portfolio-risk
claim. Root is preparing the separate v4 metric diagnostic; this review does
not replace the historical output. Funding-induced divergence is economically
compatible with [Shleifer and Vishny's limits of arbitrage](https://www.nber.org/papers/w5167),
which emphasizes capital requirements and risk rather than guaranteed convergence.

### AR02 — Berkshire is the strongest short-horizon implementation candidate, with an asymmetric anchor

**Tree:** S07, X01, L01–L04, M04–M06, B02/B03. **Classification:** conditional
opportunity candidate; executable profitability unverified.

The US LOOP aggregate files report Berkshire B00 RMSE **0.2600** versus
persistence **0.2692**, roughly a 3.4% reduction. Its z-score diagnostic has
gross Sharpe **3.31** and quoted-spread-net Sharpe **1.58**, with annualized
log-score means 9.97% and 4.70%. The gross and quote-net samples differ
(4,043 versus 3,829 observations), so their difference is not a matched-sample
estimate of the spread cost alone. These quantities are unusually favorable
relative to the other pairs and merit first implementation scrutiny.

The [issuer's comparative-rights memo](https://www.berkshirehathaway.com/brkshareholderinfo/compab.pdf)
establishes **one-way** A-to-1,500-B conversion, not the reverse. A B premium
above conversion value and a B discount therefore have different economic
anchors. A symmetric z-score signal around a rolling mean can mix an anchored
conversion direction with an unanchored relative-value direction.

The diagnostic uses the current closing ratio to set a position applied to the
next close-to-close log-return difference, and charges half the same-date
combined spread when positions change. It does not establish that the signal
could be computed and both legs filled at that closing price. Borrow, funding,
impact, dividends, taxes, conversion timing and live quote availability are
omitted. [Roll (1984)](https://onlinelibrary.wiley.com/doi/full/10.1111/j.1540-6261.1984.tb03897.x)
shows that transaction costs alone can create negative serial dependence in
observed prices; reversal in transaction closes is not by itself excess return.

**Next test:** freeze separate conversion-direction and reverse-direction
rules, use synchronized executable bid/ask quotes and next available fills,
compare identical quote-covered dates, include both legs' financing/borrow,
and reserve an untouched prospective cohort. Do not optimize the z-score
threshold or select the profitable side after inspecting its returns.

### AR03 — Novo is the most consistent new long-horizon candidate, but its economic interpretation is not identified

**Tree:** B01/B02, X01–X03, M02–M05, P01/P03. **Classification:** repeatable
retrospective forecasting association, not a realized cash or arbitrage result.

Novo is the only v3 comparison positive against both benchmarks under every
tested model/method/horizon/coverage combination. Pragmatic level-only rolling
OLS R-squared versus persistence is **0.396** at 24 months and **0.136** at
60 months; fixed ridge gives **0.283/0.126**. Expanding specifications are also
positive. This warrants prioritization over a broad new predictor search.

The horizon outcome is a change in a monthly mean **price discount**. Same-date
reference FX and local/US closes are asynchronous; receipt ratios, split
windows, cash deductions and source quote provenance are separate measurement
questions. [Gagnon and Karolyi (2010)](https://www.sciencedirect.com/science/article/pii/S0304405X10000486)
measure synchronous currency-adjusted ADR/home-market price deviations and
relate them to holding costs. Their design is not directly replicated by our
monthly asynchronous-close series. Their average deviation of 4.9 basis points
cannot be compared directly with our forecast R-squared or discount-change RMSE.

Five-year nonoverlapping phases contain only one or two outcomes; phases
reuse the same underlying history. Broad consistency across correlated model
variants is stronger descriptive evidence than a single win, but not several
independent confirmations.

**Next test:** predeclare a ratio/clock and cash-basis reconciliation on exact
qualified intervals, compare synchronous or explicitly lagged quotes when
available, retain all phases and losses, and reserve prospective origins.
Final dividend notices can test event-specific deductions; they cannot date a
general fee regime or supply historical net cash for every investor.

### AR04 — Volkswagen defeats simple convergence; the loss is not a reason to remove the squeeze period

**Tree:** B02, L02/L04, G01, S06, M01/M02. **Classification:** adverse stability
case and candidate funding/short-supply mechanism, not a validated short trade.

LH1's pragmatic two-year level model has persistence R-squared **−7.208**.
Its expanding slope moves from **+1.287** to **−0.819**, reaching **−2.559**.
V3 rolling level OLS/ridge remain negative at two years (**−7.416/−1.609**)
and five years (**−0.097/−2.401**). Fixed shrinkage and a shorter training memory
do not remove the problem.

The original [Godfrey study of the 2008 Volkswagen squeeze](https://www.sciencedirect.com/science/article/pii/S0927538X16300075)
documents a severe short-squeeze setting. This makes constrained convergence a
plausible rival to constant-parameter equilibrium adjustment. It does not prove
that the squeeze alone causes our forecast losses, and the US ADR proxy and
exact German local-class results must not be merged.

**Next test:** attribute existing forecast squared errors to predeclared
calendar episodes and training-origin support; flag rather than delete
extrapolations. Report the full sample first, followed by a clearly labeled
episode diagnostic. Add dated lendable supply, control blocks and borrow costs
before proposing an implementable convergence position. Pre-Xetra observations
remain excluded from an exact-Xetra history.

### AR05 — TSMC adjustment is unusually stronger in 2015–2019

**Tree:** X02/X03, M01/M02/M04/M05. **Classification:** meaningful timing/regime
anomaly needing discrimination, not a proven error or literature contradiction.

In `tsmc_price_discovery.csv`, full-sample Taiwan-to-US and US-to-next-Taiwan
coefficients are **−0.0451/+0.0612**. In 2015–2019 they are
**−0.3712/+0.3901**, with adjusted R-squared **15.95%/21.32%**. This is much
stronger than the full sample. Both signs survive the declared ADR-spread
sensitivity, but that alone does not certify executable prices or isolate price
discovery from shared endpoints.

The Taiwan-close predictor includes the prior ADR close, and the later ADR
return uses that same prior close with opposite sign. The US-close predictor
includes the Taiwan close in its denominator, and the next local return also
uses that local close as a denominator. With efficient latent prices and
transitory quote noise, these shared endpoints can induce corrective signs.
That is an algebraic rival, not a demonstrated bias estimate in these data.

[The original 2021 price-delay study](https://www.sciencedirect.com/science/article/pii/S1544612320300295)
finds predictability associated with ADR/underlying information transmission
and idiosyncratic-risk impediments. Our signs are compatible with that line of
research. The unusually large regime difference is the question to explain.

**Next test:** audit fixed-window gap/return scales, quote flags, split bases,
FX units and timestamp age; then predeclare midpoint/auction and executable
next-fill sensitivities with identical dates. The existing full-sample 90th
percentile spread cutoff is descriptive, not an origin-known trading filter.

### AR06 — News's negative spread coefficient challenges a universal liquidity story

**Tree:** L01, G01/G02, D02/D03, M04/M05. **Classification:** sign tension,
with different-estimand and measurement explanations still open.

The US LOOP News regression has combined-spread coefficient **−0.00643**,
p approximately **3.45e−9**, whereas Berkshire and Petrobras have positive
coefficients. The dependent variable is the **absolute deviation from a prior
rolling median log ratio**, and the regressor is the **sum** of the two relative
spreads. It is not the preferred-class discount level on relative illiquidity.
One cannot infer that illiquidity makes nonvoting claims more valuable from
this negative coefficient.

[Amihud and Mendelson (1986)](https://www.sciencedirect.com/science/article/abs/pii/0304405X86900656)
study trading costs and asset pricing; that mechanism does not impose a universal
sign on this absolute-deviation regression. More recently,
[de La Bruslerie (2025)](https://www.sciencedirect.com/science/article/pii/S0144818825000262?dgcid=author)
reports unstable dual-class voting premiums and does not confirm a relative
illiquidity explanation in its US/Canada sample. That paper instead emphasizes
control-related news and other conditioning variables. Our heterogeneity is
therefore not uniformly out of harmony with current literature.

**Next test:** freeze separate class-relative spread and signed premium measures,
audit stale/closing quotes, and condition on independently dated control/access
events. Do not pool News with common/preferred or receipt pairs under an assumed
common liquidity sign, and do not reinterpret the tiny p-value as causal proof.

### AR07 — Some winners exploit a weak benchmark rather than strong prediction

**Tree:** B01/B02. **Classification:** benchmark interpretation problem,
not a new market anomaly.

All seven US B00 models beat the forecast that moves next session's level all
the way to a rolling median, but only Berkshire and narrowly Liberty beat
zero-change persistence. The full median correction is mechanically aggressive
for a one-session target. In v3, Volkswagen can beat its rolling historical
mean while every tested rolling method loses to persistence. Both benchmarks
must remain visible.

For a single standardized predictor, v2/v3 lambda=1 ridge halves the OLS slope
and blends its prediction equally with the training mean. A ridge win can thus
reflect reduced estimation variance and conservative calibration rather than
stronger economic information. The fixed penalty remains a valid prespecified
sensitivity; its win does not identify a mechanism.

[Campbell and Thompson (2008)](https://academic.oup.com/rfs/article-abstract/21/4/1509/1567518)
study prediction against a historical-average benchmark for excess stock
returns. Our zero-mean discount-change benchmark and rolling matured-label mean
are different targets. Apply their discipline of explicit benchmarks, not a
claim that our results replicate their equity-premium findings.

**Next test:** report native and identical-origin benchmark losses, absolute RMSE,
loss ratios and independent-span counts together. Never choose the easier
benchmark after observing which one a model beats.

### AR08 — Samsung has correction signs without a reliable primary forecast

**Tree:** B02/B03, M04/M05, L01. **Classification:** candidate microstructure or
short-run response, not a contradiction of the forecasting null.

The locked Samsung history model reduces one-session MAE versus persistence
by only **0.000725 percentage points**, with a block interval crossing zero;
the direct AR point estimate is better. Continuation D1's exploratory five-session
MAE gain **0.016738 points** has a positive conditional block interval, but
was adaptively motivated on viewed data and is a secondary-horizon result.
The leg decomposition finds preferred-over-common correction of roughly
**0.14%/0.38%/0.53%** after a one-point widening at 1/5/20 sessions.

Those statements can coexist: in-sample corrective covariance does not guarantee
stable out-of-sample forecasts after estimation, nor executable return after
spread and delay. Observed closes can contain bounce, as in Roll's mechanism.
The external-state, activity/range and generic calendar challengers failed
their registered incremental gates and should remain negative evidence for
those particular designs.

**Next test:** follow the existing untouched-future protocol, preserving primary
and secondary horizons, and compare actual executable price responses. Do not
reopen a lag/window search on the exposed 2024–2026 outcomes.

### AR09 — The Samsung supply association is a regime description, not a universal supply law

**Tree:** S06, S01–S05, L01, D01–D03, G01/G02. **Classification:** meaningful
within-firm boundary on a simple explanation; broader mechanisms unresolved.

Supply-only annual levels have R-squared **0.6984** in 17 observations, while
the joint first-difference model has R-squared **0.0006** in 15 changes. The
non-treasury share ratio is effectively constant in 2018–2023 while the discount
spans **9.61 points**. A coefficient near 1,047 on the raw supply ratio is not
automatically absurd: a 0.001 ratio change corresponds to about 1.05 discount
points. Scale and causality are separate questions.

[Chay and Moon (2005), indexed bilingual abstract](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART001103943)
links Korean relative preferred supply and liquidity to price differences in
1990–2003. Their cross-sectional liquidity mechanism is not refuted by our
single-issuer, non-treasury-count/activity change null. We did not retrieve and
replicate their full empirical tables.

[Chung and Kim (1999), original paper](https://www.acsu.buffalo.edu/~keechung/JCF.PDF)
emphasizes ownership structure and pivotal minority votes. Non-treasury shares
do not measure strategic blocks, public float, minority control power or
transaction costs. Recent almost-proportional buyback programs and connected
announcement/execution/cancellation dates supply little clean relative dose.

**Next test:** reconcile class definitions and public-release dates; then study
actual float/owner and spread changes jointly, preserving policy endogeneity.
Do not backfill the newly received annual evidence at old forecast origins.

### AR10 — Prosus, Naspers and other holdco betas are exposures, not NAV convergence

**Tree:** S06, G01/G02, D02/D03, R01–R04, B02. **Classification:** strong
contemporaneous association with an untested valuation mechanism.

Exact-interval Prosus/Tencent price-return beta falls from **0.736** in the
stock-only specification to **0.637** with regional controls; Naspers/Prosus
is **0.971** stock-only. Holdco proxy up betas range from about **0.246** for
Investor/Atlas to **1.006** for Naspers/Prosus. These differences are not an
automatic violation of one-for-one asset ownership: cash, other holdings,
leverage, liabilities, changing ownership, share counts and market covariance
all affect equity-return elasticity.

The local normalized Prosus/Tencent gap model has adjusted R-squared only
**0.48%–0.71%**; its nominal B03 gap p-value **0.0183** has BH q approximately
**0.634**. Stock exposure and useful discount prediction are different results.
Tencent's in-specie distributions and the Prosus/Naspers reorganization also
make price-return and total-return bases material.

[Froot and Dabora's twin-share study](https://www.nber.org/papers/w6572)
finds relative valuation related to trading/ownership habitat even for linked
cash flows. Our holding companies are not its identical cash-flow twins; a
normalized first-price ratio cannot measure NAV or identify a cheap claim.

**Next test:** build dated holdings, asset/liability/tax and share-count NAV with
publication-vintage controls, then ask whether deviations predict cash-inclusive
relative outcomes. Preserve the current descriptive betas and their action-window
sensitivities rather than relabeling them as NAV evidence.

### AR11 — Dividend-factor associations do not establish a class payout mechanism

**Tree:** P01–P05, R01/R04, M03, B01. **Classification:** nominal explanatory
association with multiplicity, source-timing and estimand limits.

The Samsung full-sample B04 US-Barra DIVYILD coefficient is **25.646** with
p **0.0249**, but BH q **0.1888**; lagged activity has p **0.0183**, q **0.1643**.
The factor is a US factor-return series, not Samsung's historical class cash
dividend or an announced payout feature. A positive loading therefore cannot
show that an independently dated Samsung dividend raises or closes the class gap.
Factor publication/revision timing is also unverified. The source report already
scopes these as retrospective associations; this review preserves that scope.

**Next test:** use actual class cash rights, announcements, ex/trading and payment
clocks and a qualified release-time history. Remove the arithmetic linkage
between price and dividend yield before calling yield an independent cause.
Retain family-wise/multiplicity qualifications across tested factors and windows.

### AR12 — Long horizons, clean arithmetic and many variants do not create independent evidence

**Tree:** B01/B02, M01–M03, S06. **Classification:** inference and generalization
limit affecting the entire result inventory.

Samsung's descriptive ten-year map has 141 overlapping endpoints but only two
anchored nonoverlapping intervals. The newer LOOP five-year phases often have
one or two outcomes. LH1/v2/v3 arithmetic reconstructions are valuable software
checks, not fresh economic samples. Strict/pragmatic coverage, multiple phases,
OLS/ridge and nested feature models remain strongly dependent.

[Boudoukh, Richardson and Whitelaw (2008)](https://www.nber.org/papers/w11841)
show how persistent regressors and overlapping outcomes can produce closely
related estimates and apparently stronger long-horizon patterns under a null.
Their stock-return setting is not identical to our discount changes, but their
dependence warning applies directly to claims based on a large endpoint count.

The US cross-pair PC1 explains **16.22%** of standardized changes, only modestly
above the equal-eigenvalue reference **1/7 = 14.29%**. This argues against a
dominant daily factor in that complete-case sample; it does not disprove common
stress, regional, legal-rights or multi-year channels. Different economic rights
and asynchronous closes make a universal factor an especially strong claim.

**Next test:** reserve genuinely new origins and predeclare loss comparisons and
economic measurement challenges. Report the full candidate universe and blocked
fits alongside winners, without interpreting multiple correlated designs as
independent replications or selecting a favorable nonoverlap anchor.

## V4 diagnostic addendum

### AR13 — V4 audit identifies impossible price-ratio forecasts and weak-benchmark wins

**Tree:** M01/M02, B01/B02, L02/L04. **Classification:** diagnosed model-support
failure and benchmark/risk-unit diagnostics; no refit, new exclusion or
implementation claim. **Validation status:** separate verification job
`15308863` passed, checking 524 score diagnostics, 54,748 origin diagnostics,
14 drawdown translations and preservation of 1,991 evidence rows. Its receipt
is `runs/loop_long_horizon/v4_15308800/verification_v2/AUDIT.json`.
Earlier verified v3 estimates and original inputs/outputs remain unchanged.
This is validation of diagnostic arithmetic, not a new economic sample.

The separately versioned outputs are
`runs/loop_long_horizon/v4_15308800/forecast_diagnostics.csv` and
`drawdown_units_review.csv`. The former summarizes all 524 v3 score rows; it
does not select a new model. It flags **316 forecast-variant cases** with implied
terminal discount at or above 100, all from OLS. For the defined
`q=100*(1-positive_price_ratio)`, a discount at or above 100 implies a nonpositive
price ratio. This is incompatible with two positive qualified price legs and
reveals failure of the unconstrained linear forecast outside its admissible
economic support. It is not an unusually profitable signal. Counts repeat
under related models, windows and coverage rules; they are not 316 independent
market episodes.

Violations concentrate in VW two-year and Hyundai preferred-3 two-/five-year
comparisons, with additional Hyundai preferred-2 five-year rolling cases.
No ridge violations were found in these inspected saved cases. That contrast
is diagnostic evidence about the already fixed methods, not authorization to
select ridge from the observed losses, censor OLS predictions, or rerun a
bounded model on exposed evaluation data.

The same audit finds **161/524 score rows** that beat their training-mean
benchmark but lose to persistence. For pragmatic VW LH-LEVEL at five years,
expanding OLS has R-squared **−0.0759** versus persistence but **+0.8692** versus
the training mean; the mean benchmark's MSE is approximately **8.226 times**
persistence MSE. The rolling ratio is about **7.636**. The apparent very large
historical-mean win therefore does not establish useful prediction against
the harder zero-change benchmark.

Calendar attribution also corrects a tempting story: VW's pragmatic two-year
level loss has its largest origin-year contribution in **2011**, accounting
for about **40.84%** of squared error. This does not establish that 2008 has no
influence through training or target endpoints, but it prevents attributing
all losses to the squeeze without an origin/training/target decomposition.
Novo's largest origin-year contributions occur in 2024 at two years
(approximately 22–25% across the stated method/window comparisons) and 2021
at five years (approximately 28–33%). Those concentrations and the very small
nonoverlapping phase counts remain material to its apparent robustness.

The legacy VW **−238.1755 log-point** drawdown translates to approximately
**−90.7612%** for a geometric log-score index using the **same legacy peak
convention**. Missing quote-net values remain missing. Neither the initial-zero
high-watermark convention nor actual funded portfolio wealth has been
reconstructed by this unit translation. It must not be reported as a financed
strategy's verified wealth drawdown.

The first verification attempt `15308814` checked forecast diagnostics before
rejecting the unavailable VW quote-net drawdown. The successful audit explicitly
preserves that missing value as missing rather than zero. Completed scientific
outputs were not recomputed after the main run's console-only JSON type failure.

**Next test:** retain the independently checked diagnoses alongside the original
outputs. A model respecting the positive-ratio
support needs a separately registered transformation/estimation protocol and
new evaluation evidence. Do not clip impossible forecasts or remove their
origins after inspecting losses. The literature warnings about overlap,
estimation instability and funding constraints cited above remain relevant;
these dimensional and support checks do not themselves overturn a literature
result.

## Completed-family coverage

| Completed family | Evidence reviewed | Analyst conclusion |
| --- | --- | --- |
| Samsung retrospective B01–B04 | 1,224 coefficient rows, task definitions, HAC/BH tables | Lag-state associations stronger than deployable prediction; nominal factor/activity findings need BH and timing qualifications. |
| Samsung locked forecasting | Matched metrics, strict metrics, stability and uncertainty | Primary gain tiny/uncertain; 20-session deterioration retained. |
| Continuation D/E/F/G–H/I | Diagnostic and threshold summaries; D1/R756 and external/activity/calendar metrics; final coefficient archive/report | D1 secondary candidate only; no primary predictor validated; other fixed blocks failed their gates. |
| Samsung long-horizon A/B | Change/era summaries and prior independent inspection | Persistent states and source-definition traps matter; counts and overlap prevent inference from descriptive means. |
| Hypothesis resolution | Supply/rank, class-leg, issuer-dose/event and TSMC timing tables | Supply-only insufficient, preferred catch-up descriptive, connected events noncausal, TSMC regime anomaly unresolved. |
| Three core-pair baselines | Coefficients, status/coverage/fundamentals audits | SK Square/TSMC in-sample adjustment; Samsung Fire weak; no Korean NAV claim. |
| Prosus/Tencent/Naspers returns | Primary/action/lag coefficient and rolling summaries | Strong exposure, weak lag signal; return bases and NAV still gated. |
| Local Prosus/Tencent gap factors | Coefficients and model-status tables | Negligible fit and no multiplicity-robust factor finding. |
| US LOOP exceptions | B00, walk-forward, liquidity, legs, trading, holdco, PCA/correlation and coverage tables | Berkshire candidate; News sign tension; strategy drawdown units need correction; heterogeneity retained. |
| LOOP LH1 | Scores, coefficients, coverage, blocked status and nested comparisons | Four of eleven level wins at each of two/five years; volume does not universally help. |
| LOOP LH2 | Fixed ridge, drift, all phases and fixed-period summaries | Shrinkage sensitivity, VW instability, Novo repeat candidate; no penalty selected. |
| LOOP LH3 | Rolling/expanding matched scores, phases, calendar periods, nested comparisons and failed origins | Novo robust within exposed history; eight strict Ping An activity origins blocked; no new exact-venue interval or structural feature admitted. |
| LOOP v4 existing-output diagnostics | 524-row forecast audit and 14-row drawdown-units review | Implied impossible OLS ratios, benchmark difficulty and loss concentration diagnosed without refit; independently verified arithmetic, not a new economic sample. |

The original 61-table inventory, extended by two v4 diagnostic tables, retains
hashes of the actual aggregate artifacts rather
than counting the narrative reports as independent analyses. Prior verification
and failed-run histories were read for scope; this analyst did not independently
replay all historical jobs. No licensed row, crosswalk, raw export or individual
forecast origin is included in this public review.

## Research order

1. Correct the drawdown units in a separate diagnostic and require a funded
   portfolio definition before comparing trading risk.
2. Challenge Berkshire's conversion directions and execution assumptions, and
   Novo's ratio/clock/cash basis, before claiming exploitability.
3. Attribute VW losses and TSMC's regime contrast without deleting adverse
   episodes or searching for favorable break dates.
4. Test News's signed premium and class-relative liquidity with dated control
   information; treat 2025 evidence as a rival to a universal liquidity claim.
5. Qualify structural definitions, exact venues and publication timing; preserve
   source revisions, unknown dates, missing fields and dividend statuses.
6. Freeze the resulting hypotheses before new prospective outcomes are opened.

No economic anomaly is presently certified as exploitable. Berkshire and Novo
deserve the first mechanism/implementation challenges; the rest supply useful
negative controls, rival explanations and measurement tests. Lack of a proven
trade does not negate the descriptive results, and descriptive success does
not establish a trade.

## Literature access record

Primary author/issuer, original-paper and publisher sources were searched on
November 12, 2026. The source claims above are paraphrased. Full original
Chung–Kim and Berkshire documents and the KCI indexed abstract were readable.
Publisher/search excerpts supplied the cited Gagnon–Karolyi, 2021 price-delay,
de La Bruslerie, Godfrey, Amihud–Mendelson and Campbell–Thompson claims; some
direct publisher/SSRN requests returned 403. Their full tables were not newly
replicated, and no access restriction was bypassed. NBER abstracts supported
the Froot–Dabora, Shleifer–Vishny and Boudoukh–Richardson–Whitelaw summaries.
This is a targeted comparison to the original literature, including a 2025
study; it is not a claim of an exhaustive systematic literature review.
