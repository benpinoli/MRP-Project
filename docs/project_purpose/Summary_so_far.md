Continue my MRP research project on mispricing between related securities. This is a handoff from another ChatGPT account. Preserve the decisions below, distinguish completed work from proposed work, and help me advance the project in concrete steps.

**Project objective**

Estimate how the fair discount between related securities changes over time. Test whether deviations from that estimated discount generate profitable relative-value signals, outperforming a rolling historical median baseline.

The eventual investment decision is which security to own outright. Long-short portfolios are tools for evaluating the model.

The original deliverable is a concise technical memo covering:

- Discount history, fair-value model, and backtest for each core pair.
- Sharpe ratio, drawdown, turnover, and performance after costs.
- A dated view on which security is preferable and why.
- Cross-pair comovement: global versus regional drivers.
- Whether a common framework generalizes or requires company-specific components.

Core pairs:
1. Prosus / Tencent.
2. SK Square / SK Hynix.
3. Samsung Electronics common / preferred.
4. Samsung Fire & Marine / Samsung Electronics common.
5. TSMC local / ADR.

**Current scope and immediate objective**

We subsequently decided to focus on Prosus/Tencent first.

Start by constructing and plotting the historical discount. Initially use a transparent NAV calculation; add estimates of overhead, taxes, and other economic costs afterward. Do not start with a complicated predictive model before validating the underlying series.

I need machine-readable data in CSV form. Annual reports are hundreds of pages long; help locate downloadable tables or extract the relevant inputs into a reproducible dataset.

**Materials**

The candidate spreadsheet is “LOOP Exceptions - Companies vF.xlsx”:
https://docs.google.com/spreadsheets/d/1ViKw39EVKBV7CrVpmtxfnI4pRGv6VasV/edit

It contains 27 candidate pairs:
- 10 holding-company/held-company pairs.
- 5 common/preferred pairs.
- 5 dual-share-class pairs.
- 2 A/H-share pairs.
- 5 primary-listing/ADR pairs.

The project brief is titled “Mispricing Between Related Securities: Holdco discounts and other law-of-one-price (LOOP) exceptions.”

Its anchor is Prosus/Tencent. Approximate ownership percentages and discount figures in the brief are background estimates, not validated historical inputs.

**Data access**

I have access through Silver Fund to:
- SF-quant.
- CRSP stock data.
- Barra data.

I also obtained Compustat Global Securities data covering global securities from 2005 onward. Inspect the actual export and field definitions before assuming it includes all required prices, share counts, currencies, or fundamentals.

The global dataset’s start date does not imply Prosus has a trading history from 2005. Prior work noted its listing began in September 2019; verify the precise usable start date.

CRSP can help with US-listed securities and eligible ADRs, but foreign local legs require other coverage. SF-quant and Barra coverage for the relevant markets remains to be checked.

**Completed work**

1. Reviewed the candidate spreadsheet and project brief.
2. Conducted an initial literature sweep.
3. Discussed the literature’s agreements, disagreements, and economic mental models.
4. Narrowed the immediate project to Prosus/Tencent.
5. Identified historical NAV construction as the first empirical task.
6. Created an existing file named `prosus_buybacks_daily.csv`.

The previous session reported that the buyback CSV contained 1,086 observations covering June 2022–October 2026 and that daily share counts reconciled to weekly totals. Treat those as prior-session validation claims to verify against the attached file.

The saved CSV’s inspected columns include:
- trade_date
- shares_repurchased_as_reported
- average_purchase_price_eur_as_reported
- gross_consideration_eur_as_reported
- usd_per_eur_fix
- total_amount_usd_as_reported
- purchase_currency
- source_url
- source_sheet
- source_row
- retrieved_date
- publication_date

Its source is Prosus’s downloadable buyback workbook:
https://www.prosus.com/~/media/Files/P/prosus-corp-v2/share-buyback-programmes/prosus-share-buyback.xlsx

The inspected early rows have blank publication dates. Those need attention before using buyback information in a point-in-time backtest.

Do not assume buybacks equal immediate share cancellations, or reconstruct historical shares outstanding solely by subtracting repurchases.

There is no confirmed completed historical NAV/discount dataset, fitted fair-value model, or investment backtest in this handoff.

**Literature synthesis**

Our organizing questions are:
1. What cash flows and rights does each security provide?
2. Which investors trade each security, and what restrictions do they face?
3. What mechanism can enforce convergence?

Broad findings:
- Large gaps can persist.
- Financing, short-sale constraints, and uncertain convergence limit arbitrage.
- Taxes, overhead, governance, liquidity, and access can justify price differences.
- Investor demand and trading location can affect relative prices.
- Corporate events and conversion mechanisms matter.

Unresolved:
- The share attributable to economic costs versus sentiment.
- The dominant explanation for each pair.
- The correct discount at a particular date.
- Whether statistical predictability survives implementation costs.

Do not label every unexplained residual “sentiment” or “mispricing.”

Different categories require different economic models:
- Holdcos: indirect ownership, management discretion, other assets, liabilities, and costs of delivering value to shareholders.
- Share classes: differences in voting, dividends, liquidity, and investor demand.
- ADRs and segmented listings: conversion ratios, currencies, trading times, access restrictions, and conversion capacity.
- Operating companies holding stakes: separately value the operating business. Samsung Fire & Marine is an insurer, not a pure Samsung Electronics wrapper.

Relevant readings already identified:
- Lamont & Thaler, “Can the Market Add and Subtract?” (2001 working paper; 2003 publication): https://www.nber.org/papers/w8302
- Mitchell, Pulvino & Stafford (2002), “Limited Arbitrage in Equity Markets.”
- Shleifer & Vishny (1997), “The Limits of Arbitrage”: https://www.nber.org/papers/w5167
- Lee, Shleifer & Thaler (1991), “Investor Sentiment and the Closed-End Fund Puzzle”: https://www.nber.org/papers/w3465
- Brennan & Jain, “Capital Gains Taxes, Agency Costs, and Closed-End Fund Discounts” (2007 working-paper version): https://www.anderson.ucla.edu/documents/areas/fac/finance/brennan_capital.pdf
- Holmén & Högfeldt (2009), “Pyramidal Discounts: Tunneling or Overinvestment?”
- Froot & Dabora (1999), “How Are Stock Prices Affected by the Location of Trade?”: https://www.nber.org/papers/w6572
- Chay & Moon (2005), Korean preferred-share liquidity premiums.
- Yang & Ryu (2021), Korean common/preferred sentiment: https://doi.org/10.3390/su13105539
- Li, Teruya & Tsai (2006), Taiwanese depositary-receipt restrictions, supply, and sentiment.
- “An Empirical Analysis on the Persistent Premium of TSMC ADRs over Domestic Listings in Taiwan Stock Market” (2025): https://doi.org/10.1080/13504851.2025.2571074
- Schultz & Shive (2010), “Mispricing of Dual-Class Shares.”
- Gatev, Goetzmann & Rouwenhorst (2006), “Pairs Trading”: https://www.nber.org/papers/w7032

This was an initial literature review, not a full replication or exhaustive assessment of every paper.

**Prosus discount definitions**

Use a common currency and consistent economic ownership/share-count conventions:

NAV_t =
Tencent shares owned_t × Tencent price_t
+ other listed stakes_t
+ estimated unlisted asset values_t
+ holdco cash_t
− holdco debt_t
− other relevant liabilities_t.

Discount_t = 1 − Prosus economic market capitalization_t / NAV_t.

Also retain the absolute difference, NAV minus market capitalization.

Use parent-level liabilities appropriately; avoid subtracting subsidiary debt again when it is already reflected in subsidiary equity values.

A stake-only comparison can be useful as an explicitly labeled approximation. It is not the full NAV discount.

Distinguish:
- Discount to gross look-through NAV.
- Discount to an economically adjusted NAV after estimated additional costs.

Do not deduct the same tax or overhead assumption twice.

**Missing historical inputs**

We still need:
- Tencent shares actually owned by Prosus over time.
- Other portfolio assets and their valuation dates/methods.
- Holdco cash and debt.
- Prosus economic shares, treasury shares, splits, and the former Naspers crossholding structure.
- Price, dividend, currency, and corporate-action data.
- Publication dates showing when information became available.

Useful official sources:
https://www.prosus.com/investors/investing-in-prosus/net-asset-value
https://www.prosus.com/investors/share-information/share-buyback-programmes
https://www.prosus.com/investors/financial-information/annual-reports

Current NAV pages cannot automatically supply historical point-in-time information.

**Next steps**

1. Inspect the attached data and buyback CSV. Establish identifiers, units, currency conventions, corporate actions, and coverage.
2. Build a source inventory for missing NAV components, prioritizing downloadable spreadsheets and tables.
3. Create a tidy historical NAV-input CSV retaining effective dates, publication dates, sources, and valuation methods.
4. Construct both the transparent stake-only approximation and full NAV discount where data supports it.
5. Validate selected dates against published Prosus NAV disclosures. Explain discrepancies.
6. Plot the discount and flag genuine structural changes. Handle different market closing times carefully.
7. Establish a rolling-median baseline using only information available at each date.
8. Test simple conditional models using underlying returns/volatility, buybacks, liquidity, governance events, and other justified drivers.
9. Evaluate forecasts and long-short returns separately, using consistent execution rules, hedge ratios, financing, dividends, FX, borrowing costs, and turnover.
10. Expand to other pairs after the Prosus pipeline works.

A proposed framework—not a completed model—is:

observed discount = changing conditional/economic anchor + residual deviation.

Estimate the anchor and test residual convergence separately. A historically normal discount is not necessarily an economically fair discount.

For later cross-pair analysis, control for shared securities and common factor exposures before interpreting correlation as sentiment. Several core pairs involve Samsung.

**How to work with me**

Be concise, define symbols and spell out acronyms. Work through one concrete step at a time. Clearly distinguish verified data, approximations, proposed methods, and completed results.

Begin by assessing the attached files and identifying the smallest missing dataset needed to produce our first defensible Prosus/Tencent discount chart. Do not restart the broad literature review.