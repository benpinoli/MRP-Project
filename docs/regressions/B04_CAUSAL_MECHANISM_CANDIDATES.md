# Samsung B04: competing causal mechanisms

Research discussion: November 4, 2026. Status: hypothesis organization only. No feasibility assessment, data acquisition, or new estimation performed.

## Interpretation that must precede the mechanisms

The outcome is the **daily change** in the preferred discount, in percentage points: `q = 100(1-P/C)`, `dd_pp = q_t-q_(t-1)`. A positive coefficient means widening on days when a factor return is positive, conditional on the other regressors. It does not establish an effect on the long-run discount level.

B04 includes US Barra **factor returns**, lagged discount, and lagged log(preferred/common share volume). `BETA` is a style factor, distinct from `COUNTRY`, not simply the US equity market or US GDP. `LEVERAGE` is not Samsung's debt/equity ratio. `DIVYILD` is not Samsung's dividend payment or dividend increase. Exact descriptor construction and factor orientation require the model documentation. Working economic readings below assume positive factors reward higher beta, leverage, and dividend yield, respectively.

The relevant empirical question is why the same firm’s two share classes respond differently. Approximately, using comparable price returns, `dd_pp ≈ 100(P/C)_(t-1)(r_C-r_P)`. More exactly, the right side is divided by `(1+r_C)`. Better Samsung earnings alone do not explain common outperforming preferred.

Samsung's 2024 business report describes the outstanding preferred shares as non-voting and non-cumulative, with an additional annual dividend of 1% of par value. This is not a 1% premium on the common dividend. The February 2025 GDR prospectus says the underlying non-voting preferred shares rank equally with common in liquidation. Its discussion distinguishes older shares from provisions for newly issued preferred shares and describes contingent voting rights following dividend nonpayment. Thus generic US fixed-dividend, senior preferred-stock intuition is inappropriate; historical issue terms must govern each event.

Sources: [2024 business report](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/2024_4Q_Interim_Report.pdf); [February 2025 prospectus, pp. 8 and 39](https://images.samsung.com/is/content/samsung/assets/global/ir/docs/Samsung_Final_Prospectus_20250210.pdf).

## What the local coefficient table actually says

Source: `B01_B04_RETROSPECTIVE_COEFFICIENT_TABLES.md`, main specification, HAC 20. This is the available local table, not confirmation that it is the team's latest run.

| Term | Full sample | 2005–2014 | 2015–2019 | 2020–2026 |
|---|---|---|---|---|
| BETA | +13.15; p=.015 | +20.29; p=.148 | -11.67; p=.440 | +12.86; p=.015 |
| LEVERAGE | -17.26; p=.175 | -42.41; p=.064 | +51.26; p=.079 | -17.22; p=.331 |
| DIVYILD | +25.65; p=.025 | +14.23; p=.590 | +9.44; p=.740 | +27.49; p=.035 |
| MOMENTUM | +3.11; p=.508 | -22.00; p=.097 | +3.34; p=.770 | +13.69; p=.003 |

The dividend-yield coefficient does **not** disappear in this B04 table. Full-sample B03 to B04 is +26.58 to +25.65, with p=.020 to .025. Resolve the run/specification discrepancy before describing attenuation as a result. Nested comparisons must use identical observations.

These are exploratory signals: full-sample B04 BETA and DIVYILD have BH q=.150 and .189; post-2020 MOMENTUM has q=.055. None of those pass a 5% BH threshold under the table's correction family. Leverage significance is sensitive to sample exclusions and bandwidth; a decade is not a measured recession state. A coefficient significant in one period and insignificant in another is not itself evidence that the coefficients differ.

A coefficient of 13.69 is not a 13.69% discount increase: with decimal factor returns, a +1 percentage point factor return corresponds to about +0.137 percentage point in the discount change, conditional on the model.

## Ranked mechanism candidates

Ranking reflects economic coherence and fit to the reported patterns, not estimated causal probabilities.

### M1. Risk appetite and common-directed demand

**Chain:** global risk-taking or Samsung optimism → marginal buying concentrates in common → common outperforms preferred → discount widens.

Potential reasons buying concentrates in common include investor mandates, benchmark implementation, trading capacity, or investor attention. Each is a separate claim to verify. Positive BETA and recent MOMENTUM are compatible with this mechanism but do not establish it. A US style return is an indicator of market conditions, not automatically an exogenous sentiment shock.

**Distinctive predictions:** widening accompanies common-relative net buying; common-specific attention or benchmark events have disproportionate effects; the relation varies with investor participation or trading capacity. A temporary attention shock should show some subsequent reversal. Persistent benchmark demand need not reverse quickly.

**Evidence against it:** preferred attracts the incremental buying during widening; the factor relation persists without the proposed flow pattern; only common earnings news, with no class allocation channel, is observed. Flows and prices can be jointly determined, so contemporaneous mediation is suggestive rather than identified.

### M2. Relative liquidity and constrained arbitrage

**Chain:** funding/trading conditions change → preferred becomes relatively expensive or difficult to trade → investors pay more for common's trading capacity → discount widens; costly shorting of common prevents convergence.

This can coexist with M1: preferred demand may fail to keep pace in rallies, and a common liquidity premium may also widen in stress. Do not give this mechanism a universal recession sign. A negative leverage coefficient is compatible with stress-induced widening when the leverage factor falls, assuming the factor orientation is verified. It does not mean Samsung increased its own leverage.

**Distinctive predictions:** preferred-relative spreads or price impact worsen as the discount widens; factor sensitivity is stronger under tight funding or scarce common borrow; divergences last longer when arbitrage is costly.

**Evidence against it:** widening occurs while preferred-relative trading conditions improve, without another constraint. `lag_activity` measures share volume, not liquidity, order direction, or investor identity. Its inclusion cannot alone establish this channel.

### M3. Income clientele and dividend expectations

**Chain A:** increased demand for dividend income → investors favor the cheaper preferred claim with a higher cash yield → preferred outperforms → discount narrows.

**Chain B:** lower concern about dividend cuts → investors shift from an income-oriented preferred clientele toward common → discount widens. This requires actual differences in investor preferences or perceived payout protection; Samsung's non-cumulative terms and shared operating exposure make generic dividend-insurance language too strong.

**Distinctive predictions:** unexpected payout-policy news or changes in payout uncertainty have class-relative effects; income-oriented investors buy preferred disproportionately; the response is tied to actual dividend news, rather than only a US yield-style return.

**Sign challenge:** the simplest income-clientele story predicts a negative relation to a positive high-dividend-yield factor shock. The observed positive coefficient needs an additional allocation channel or an omitted common driver. Do not force it into a dividend-causality interpretation.

If another run really loses DIVYILD significance after `lag_activity`, distinguish coefficient shrinkage from larger standard errors and sample changes. Correlated predictors, an imperfect activity proxy, conditioning on a mediator, or selection effects can all produce this pattern. Losing significance alone does not identify mediation. A lagged activity measure cannot automatically mediate a later same-interval factor shock.

### M4. US demand and semiconductor fundamentals, transmitted through class-specific trading

**Chain:** unexpected US customer demand or chip-cycle news → improved Samsung earnings expectations → both classes benefit → common responds more because of M1, M2, or another class-specific channel → discount widens.

This retains the useful part of the consumer-demand idea while making its missing step explicit. Higher US stock prices are not the same thing as more current consumer income; equity prices also move with discount rates and expected future profits. Samsung exposure extends beyond consumer products to components and business demand.

**Distinctive predictions:** relevant demand/earnings news predicts Samsung's overall value, and the discount response varies with the proposed class-specific channel. Effects should align with economic news dates, not only broad style rotations.

**Evidence against it:** US factor shocks move the discount without relevant earnings revisions or class-specific transmission; pure macro exposure affects both classes similarly.

Do not use the notes' 40% Americas revenue or 7.5% US supply figures as established inputs. Their year, geography, denominator, and underlying source need verification. Americas revenue is not necessarily US final demand. US production exposure can create costs or benefits and has no standalone discount sign.

### M5. Voting and governance value

**Chain:** a governance event increases the expected benefit or pivotality of common voting rights → common rises relative to preferred → discount widens.

**Distinctive predictions:** relative-price movements cluster around control-related announcements and are stronger when minority votes matter. The pattern should be more event-specific than general risk appetite.

**Evidence against it:** no change in voting relevance accompanies the movement, or preferred responds equally. Poor prospects do not mechanically make votes worthless; distress can also increase the value of intervention. The discount is not a direct estimate of voting value because other rights and trading conditions differ.

### M6. Class-specific supply and capital allocation

**Chain:** unequal repurchases, cancellations, issuance, treasury-share sales, or float changes → relative supply/trading conditions change → discount changes.

All else equal, preferred-relative repurchases can narrow the discount; common-relative repurchases can widen it. A lasting loss of preferred float may worsen liquidity and offset initial price support. Authorization, execution, and cancellation are distinct events.

**Distinctive predictions:** movements align with the affected class, announcement surprise, actual execution, and magnitude relative to float.

The adverse-selection idea belongs here only if actual equity issuance is documented. A primary issue raises company capital; a shareholder sale does not. Selling treasury stock, issuing new shares, and retaining earnings have different implications. A lower market-value D/E ratio can result simply from a rising equity price; it does not prove issuance. Management issuing overpriced equity can signal bad news, but the discount sign depends on class-specific dilution, rights, and demand. This is a lower-priority explanation of a daily US leverage-factor coefficient.

## Rival explanations that must remain live

- **Style covariance:** factors may proxy Korean market news, USD/KRW, rates, or the chip cycle. A style coefficient is not a named causal shock.
- **Ex-dividend arithmetic:** with equal cash dividends D and otherwise unchanged prices, `(C-D)-(P-D)=C-P`, but `1-(P-D)/(C-D)` increases when C>P. The percentage discount can widen with no widening of the absolute price gap. Unequal dividends change the calculation further. Compare raw-price outcomes with properly verified cash-inclusive outcomes before attributing this to sentiment.
- **Nonsynchronous trading:** common may incorporate news sooner than preferred; carried/stale quotes or market-close misalignment can create apparent exposures. Short-horizon reversal and aggregation can distinguish this from persistent repricing.
- **Changing sample composition and structural conditions:** pandemic-era investment flows, trading rules, payout policy, and industry changes are candidates, not explanations established by a 2020 split. Verify dates and test coefficient differences directly.
- **Chance and specification search:** repeated factors, windows, variants, and bandwidths can generate isolated significant coefficients. Retain uncertainty and the correction family when selecting follow-up hypotheses.

## Proposed order for the later research cycle

1. Reconcile the exact run, outcome units, factor definitions, dividend result, and common-sample nested comparison.
2. Prioritize M1 and M2, with ex-dividend and timing explanations as competing benchmarks.
3. Separate M3's actual Samsung payout news from the US DIVYILD style return.
4. Investigate M4 only with an explicit explanation of differential class response.
5. Pursue M5/M6 when dated, relevant events motivate them; retain distress insurance and equity issuance as conditional, lower-priority branches.

For each later hypothesis, specify: initiating shock; class-specific transmission; signed outcome; timing; one prediction that distinguishes it from its nearest rival; evidence that would reject or downgrade it; and confounding events. Evaluate feasibility and data availability only after that specification. Factor attenuation after adding an endogenous proxy is not, by itself, a causal test.
