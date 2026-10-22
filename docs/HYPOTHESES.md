# Samsung hypothesis tree and evidence

[Full research log and every filename](RESEARCH_LOG.md) · [Canonical hypothesis JSON](../research/hypotheses.json) · [Methodology](METHODOLOGY.md) · [Runs](../runs/README.md)

Observed preferred discounts are not identified vote values. All economic mechanisms below remain hypotheses; plotting trading activity is not a liquidity test. No factor regression or return analysis has run.

## H0 Measurement artifacts can produce apparent discount changes

Status: **testing**. Vendor meanings supplied; row-level conflict/calendar/quotes unresolved; adjustment formula deferred. No causal inference.

Mechanism: Carried quotes, mismatched classes, splits and event treatment distort ratios

Competing/identification concerns: Vendor flags can conflict with volume; Correct arithmetic cannot validate vendor quotes.

- EP01_F01: [main 01_discount_history.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/01_discount_history.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/01_discount_history.png)
- EP01_F02: [main 02_annual_distributions.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/02_annual_distributions.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/02_annual_distributions.png)
- EP01_F03: [main 03_daily_discount_changes.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/03_daily_discount_changes.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/03_daily_discount_changes.png)
- EP01_F04: [main 04_raw_closes_since_2019.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/04_raw_closes_since_2019.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/04_raw_closes_since_2019.png)
- EP01_F05: [main 05_trading_activity.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/05_trading_activity.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/05_trading_activity.png)
- EP01_F06: [main 06_rolling_discount_volatility.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/06_rolling_discount_volatility.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/06_rolling_discount_volatility.png)
- [EP01_F07 local flagged windows](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/flagged_discount_windows.png) · [inspection report](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/episodes/REVIEW.md)

Evidence records: [O002](RESEARCH_LOG.md#o002), [O003](RESEARCH_LOG.md#o003), [O005](RESEARCH_LOG.md#o005), [O006](RESEARCH_LOG.md#o006), [O007](RESEARCH_LOG.md#o007), [O_EP01_20261022T070352_803683Z](RESEARCH_LOG.md#o_ep01_20261022t070352_803683z), [O_EP01_20261022T070352_803683Z_FLAGS](RESEARCH_LOG.md#o_ep01_20261022t070352_803683z_flags), [O_EP01_20261022T070701_403388Z](RESEARCH_LOG.md#o_ep01_20261022t070701_403388z), [O_EP01_20261022T070701_403388Z_FLAGS](RESEARCH_LOG.md#o_ep01_20261022t070701_403388z_flags)

Next: Independent price/calendar reconciliation; adjustments remain deferred.

## H1 Votes and control affect class-relative prices

Status: **proposed**. Not tested by E01; price gap alone cannot identify voting value

Mechanism: Minority votes may become pivotal

Competing/identification concerns: Simultaneous cash-flow and demand news.

No empirical evidence logged for this branch yet.

Next: Acquire required inputs and specify the smallest descriptive test before estimation.

## H2 Cash-flow and legal rights contribute to relative pricing

Status: **proposed**. Issuer split disclosure describes rights differences; no effect tested

Mechanism: Different dividend and contingent rights change economic payoffs

Competing/identification concerns: Ex-dividend mechanics; Liquidity.

Evidence records: [O003](RESEARCH_LOG.md#o003)

Next: Acquire required inputs and specify the smallest descriptive test before estimation.

## H3 Worse relative preferred liquidity can accompany larger discounts

Status: **proposed**. Trading activity plotted only; volume ratio does not establish relative liquidity; liquidity hypothesis untested

Mechanism: Higher trading costs reduce demand for preferred shares

Competing/identification concerns: Discount affects trading activity; Proxies differ from execution costs.

- EP01_F05: [main 05_trading_activity.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/05_trading_activity.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/05_trading_activity.png)

Evidence records: [O_EP01_20261022T070352_803683Z](RESEARCH_LOG.md#o_ep01_20261022t070352_803683z), [O_EP01_20261022T070701_403388Z](RESEARCH_LOG.md#o_ep01_20261022t070701_403388z)

Next: Acquire required inputs and specify the smallest descriptive test before estimation.

## H4 Investor clientele and flows influence class-relative pricing

Status: **proposed**. Not tested

Mechanism: Different demand and access across classes

Competing/identification concerns: Investors react to discount changes.

No empirical evidence logged for this branch yet.

Next: Acquire required inputs and specify the smallest descriptive test before estimation.

## H5 Limited arbitrage allows class-price gaps to persist

Status: **proposed**. Not tested; no lending analysis executed

Mechanism: Borrow costs, inventory and legal short constraints limit correction

Competing/identification concerns: Fees react to demand; Absent fee is not free borrow.

No empirical evidence logged for this branch yet.

Next: Acquire required inputs and specify the smallest descriptive test before estimation.

## H6 Class-specific corporate actions and supply influence pricing

Status: **proposed**. Not tested; split validation is a measurement check

Mechanism: Repurchase, cancellation and float changes affect demand and liquidity

Competing/identification concerns: Management responds to an existing gap; Buybacks do not imply cancellation.

No empirical evidence logged for this branch yet.

Next: Acquire required inputs and specify the smallest descriptive test before estimation.

## H7 Market state and shared demand affect discounts

Status: **proposed**. Annual distributions and discount-change instability described; no market/factor driver or cause estimated

Mechanism: Valuation, stress and common class demand change relative pricing

Competing/identification concerns: Common price mechanically enters discount and valuation; Persistent levels correlate spuriously.

- EP01_F01: [main 01_discount_history.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/01_discount_history.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/01_discount_history.png)
- EP01_F02: [main 02_annual_distributions.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/02_annual_distributions.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/02_annual_distributions.png)
- EP01_F03: [main 03_daily_discount_changes.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/03_daily_discount_changes.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/03_daily_discount_changes.png)
- EP01_F04: [main 04_raw_closes_since_2019.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/04_raw_closes_since_2019.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/04_raw_closes_since_2019.png)
- EP01_F06: [main 06_rolling_discount_volatility.png](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/main/06_rolling_discount_volatility.png) · [sensitivity](../runs/samsung/EP01_descriptive/20261022T070701_403388Z/figures/sensitivity/06_rolling_discount_volatility.png)

Evidence records: [O004](RESEARCH_LOG.md#o004), [O007](RESEARCH_LOG.md#o007), [O008](RESEARCH_LOG.md#o008), [O_EP01_20261022T070352_803683Z](RESEARCH_LOG.md#o_ep01_20261022t070352_803683z), [O_EP01_20261022T070701_403388Z](RESEARCH_LOG.md#o_ep01_20261022t070701_403388z)

Next: Acquire required inputs and specify the smallest descriptive test before estimation.

## Next-layer data needs

| Overlay | Missing inputs |
|---|---|
| Valuation | Quarterly fundamentals, publication dates, class share counts |
| Buybacks | Actual executions by class; announcements/cancellations separate |
| Liquidity | Bid/ask quotes, historical float, verified returns before price-impact measures |
| Shorting constraints | Borrow fees, lendable inventory, utilization, class restrictions |

[Acquisition details](DATA_ACQUISITION.md) · [Deferred factor direction](FACTOR_RESEARCH_NOTES.md)
