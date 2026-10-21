# Prosus/Tencent source audit — initial checkpoints

Checked 2026-10-16. This is an input audit, not a completed NAV reconstruction or discount chart.

## Files inspected

- `bjhxhtdt8qi0ylul.csv` is a monthly Compustat Global Securities export. Tencent primary Hong Kong listing is `gvkey=270615`, `iid=01W`, and `curcdm=HKD`. Its `prccm` field is being treated provisionally as the monthly close; the original Compustat data dictionary and adjustment-factor conventions still need verification. The file provides Tencent price observations but not Prosus prices, Tencent shares held by Prosus, Prosus shares outstanding, or portfolio values. A search found Naspers and Tencent but no Prosus security rows.
- `prosus_buybacks_daily.csv` contains trade dates and reported daily repurchases. All 1,086 `publication_date` cells are blank. Trade date is not a safe substitute for information-availability date. Buyback trades must not be treated as immediate share cancellations; Prosus's report says repurchased shares could remain treasury shares pending cancellation.
- Prosus's current shares-in-issue webpage displays historical checkpoints and explains the N/A/B share structure and September 2023 cross-holding removal. The extracted `prosus_share_count_checkpoints.csv` is a transcription of that current page, not yet a point-in-time source. Its historical values need reconciliation to the contemporaneous annual/interim reports before use.
- The current Prosus NAV webpage is a current analyst-consensus summary. Prosus says unlisted-asset values use sell-side analyst estimates, post-money transaction values, and internal valuations, and warns it has not verified the analyst information. It is useful as a current reconciliation reference, not as a historical point-in-time dataset or an observed market price.

## Cross-checked checkpoints

The accompanying `prosus_tencent_verified_checkpoints.csv` records three annual measurement dates. Ownership percentages and publication dates come from Prosus annual reports/results; Tencent prices come from the supplied Compustat export. The FY2023 report independently states the 31 March 2023 Tencent close was HK$385.8 and values Prosus's stake at US$123bn, matching the Compustat `prccm` value for that date. FY2024 and FY2025 Compustat prices are retained as vendor-sourced values and explicitly marked as awaiting an independent quote match. Before valuation, confirm the actual trading-session date represented by each month-end `datadate` and the Compustat price adjustment convention.

These dates are validation checkpoints only. The published ownership percentages do not give an exact number of shares held, and annual checkpoints cannot substitute for the changing Tencent position during intervening periods.

## Source hierarchy and cautions

1. Use Prosus annual/interim reports and dated results materials for reported holdings, share structure, cash, debt, and corporate actions. Record the reporting date and the public release date separately.
2. Use point-in-time listed prices from a source that covers both Prosus and Tencent. The current attached Compustat export covers Tencent but not Prosus. Before use, verify `prccm` as the unadjusted month-end close and `ajexm`/`ajpm` treatment around splits and other corporate actions.
3. Treat Prosus's quarterly NAV disclosures as comparison values only after checking their date, methodology, listed prices, FX, analyst consensus inputs, and share denominator. Do not backfill those current or later inputs into earlier periods.
4. Use buyback trades only after reconstructing publication/availability dates and reconciling purchased, treasury, cancelled, and economically outstanding shares to Prosus's reports and shares-in-issue tables.

Primary source pages used in this audit:

- Prosus results archive: https://www.prosus.com/investors/financial-information/results
- Prosus annual reports: https://www.prosus.com/investors/financial-information/annual-reports
- Prosus shares in issue: https://www.prosus.com/investors/share-information/shares-in-issue
- Prosus current NAV disclosure and its valuation caveats: https://www.prosus.com/investors/investing-in-prosus/net-asset-value
- Prosus buyback disclosure: https://www.prosus.com/investors/share-information/share-buyback-programmes
- FY2023 annual report: https://www.prosus.com/~/media/Files/P/Prosus-CORP/menu-footer-pdf/prosus-annual-report-2023.pdf
- FY2024 annual report: https://www.prosus.com/~/media/Files/P/Prosus-CORP/AR2024/2resultsarchive/01annualreport/fy2024annualreport.pdf
- FY2025 annual report: https://www.prosus.com/~/media/Files/P/prosus-corp-v2/results-reports-and-events-archive/annual-report/2025/fy2025-annual-report.pdf

## Still required before a defensible first chart

- Prosus month-end market price from September 2019 onward, preferably with listing, currency, adjustment, and corporate-action metadata.
- Tencent shares actually owned by Prosus at each effective date, including daily/periodic sales and corporate actions; interpolate only between disclosed changes when justified and flag the method.
- Prosus's effective economic share count over time, including N/A/B share economics, treasury shares, the Naspers cross-holding through September 2023, and subsequent cancellations/buybacks. The current webpage gives historical checkpoints, but those values and the economic denominator must be cross-checked against the original dated reports before use.
- Dated values for other listed and unlisted assets, central cash, debt, and relevant liabilities. Keep listed market value separate from unlisted estimates and report both raw/transparent NAV and sensitivity to uncertain private marks.
- FX rates and timestamps consistent with the chosen monthly close convention.

Until these are assembled and checked, no full-NAV discount should be calculated from the files currently available.
