# Literature replication ledger

Checked 2026-10-26. Readable source evidence is separated from equations requiring licensed/full-text retrieval. No published table has been recreated yet. Samsung-only daily adaptations cannot reproduce original cross-sectional estimates.

## CK99 — ownership, control and voting shares

Chung and Kim (1999), *Corporate ownership and the value of a vote in an emerging market*, Journal of Corporate Finance 5, 35–54. [Author-hosted full paper](https://www.acsu.buffalo.edu/~keechung/JCF.PDF).

Table 3 / equation (10): log(VP) on intercept, log(minority-shareholder power ratio), log(voting-share fraction), and log(equity value net of private benefits). VP adds capitalized preferential dividends to `(C-P)/P`, unlike our `(C-P)/C`. Table 4 / equation (11): VP on power ratio/voting fraction, without intercept. Footnote 18 offers a linear price-ratio alternative.

CK99-R: obtain original 1992/1993 multi-firm data, ownership blocks and class terms. Verify power-ratio construction, dividend capitalization, monthly/annual aggregation and filters before reproducing Tables 3/4. Historical assumptions cannot be transferred automatically to Samsung.

CK99-A: proposed monthly Samsung rights-adjusted premium versus control power, voting fraction, capitalization and liquidity, with stationarity diagnostics. Not scheduled: needs ownership/cash-flow data and a persistent-level estimator. Repeated annual ownership is not independent daily information; nearly constant voting fraction offers little identification.

## PC19 — retail participation / noise-trader risk

Park, Choi and Choi (2019), *Is individual trading priced in the preferred stock discount?*, Emerging Markets Review 38, 326–346. [Publisher record, abstract and introduction](https://www.sciencedirect.com/science/article/abs/pii/S1566014117302315), DOI 10.1016/j.ememar.2018.03.006.

The accessible publisher text motivates relative individual trading weight conditional on conventional class differences, and reports factor-orthogonal co-movement. The search-accessible introduction describes 185 old-type pairs, 2000–October 2014. Full regression tables, exact ITW denominator, lag structure, sample exclusions and covariance estimator have NOT been verified. Obtain full text/appendix before claiming replication. No equation number or exact original controls is invented here.

Replication PC19-R: recreate the paper's preferred-discount/relative-ITW specifications and residual co-movement/PCA on its original pair sample after transcription; preserve negative/near-zero discounts under its actual rules. Record table, column and every deviation in a new config.

Adaptation PC19-A (`L01`): daily discount changes on lagged preferred-minus-common retail trading weight, lagged relative turnover and cash-flow entitlement proxy, plus Barra controls and lagged discount. This is a change-regression mechanism test, NOT the paper's original specification. Requires investor-category trading volume by class with matching venue scope; purchases+sales must use the same counting convention in numerator and denominator. Incremental dividend proxy must use declared amounts and announcement timing, not a yield mechanically driven by P/C.

## AM86 — transaction costs and pricing

Amihud and Mendelson (1986), *Asset pricing and the bid-ask spread*, Journal of Financial Economics 17, 223–249. [Full paper hosted by university faculty](https://www.acsu.buffalo.edu/~keechung/MGF743/Readings/M1%20Amihud%20Mendelson%201986%20JFE%20Asset%20pricing.pdf).

Use as economic motivation: trading costs can require price compensation. `M01` tests relative spreads/turnover conditional on risk factors. This is a Korean share-class adaptation, not a reproduction of the paper's original expected-return tests. Do not call volume a bid-ask spread or infer executable costs from an Amihud proxy.

## Barra framework and numerical methods

[MSCI equity factor models](https://www.msci.com/data-and-analytics/factor-investing/equity-factor-models) lists Korea, regional and global models; access to a US dataset does not establish those models are available in this database. [MSCI market-neutral factor methodology](https://www.msci.com/eqb/methodology/meth_docs/MSCI_Market_Neutral_Factor_Indices_Methodology.pdf) describes targeting exposures while controlling other factors; this does not promise temporal orthogonality of all regressors.

[Slurm job arrays](https://slurm.schedmd.com/job_array.html) and [sbatch dependencies](https://slurm.schedmd.com/sbatch.html) support the prepared pipeline. The original empirical regression engine uses NumPy least squares and an explicitly implemented grid-aware HAC estimator; no shared portfolio-return helper is reused.

## Reproduction checklist for each future published table

Save citation and permitted source reference, table/column, exact equation, outcome denominator, units, sampling frequency, universe, rights definition, estimation dates, filters, timing, weights, fixed effects and inference. Then add original-equation config, data dependencies, expected qualitative comparisons, deviations and validation. Multi-pair reproductions require firm/date dependence handling; those estimators are not implemented by the current single-pair OLS runner. Novel interactions below are proposals; no claim of literature novelty has been established.
