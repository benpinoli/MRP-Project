# WRDS prices and historical mappings received — November 12, 2026

The new private snapshot is `data/acquisition/2026-11-12/wrds_daily_and_mapping`. It supplements the immutable November 11 descriptor ZIP. Licensed observations and vendor crosswalk rows remain outside public Git. The user transfers the new ZIP and delivery JSON privately to BYU ORC. The public repository contains this receipt and instructions only.

## What was collected

All four extracts came from screen control of the authenticated BYU WRDS browser. Exact downloaded SQL accompanies the three Compustat extracts. The CRSP job exposed only its CSV and input parameters; both the submitted form and returned parameters were recorded instead of inventing SQL.

| Extract | WRDS job | Raw rows | Purpose |
| --- | --- | ---: | --- |
| `comp_na_daily_all.sec_idhist` | 11902806 | 461 | Dated ISIN, SEDOL, CUSIP, ticker and exchange history for the nine issuers |
| Compustat Global merged Security Daily | 11902862 | 351,747 | 2005-01-01 through 2026-11-06, nine issuers and Global W-suffix issues |
| CRSP CIZ monthly-edition Daily Stock File | 11902889 | 23,461 | Five verified US receipt PERMNOs through 2026-09-30 |
| Compustat North America merged Security Daily | 11902992 | 550 | Four active US receipt issuers, 2026-08-01 through 2026-11-06, including overlap |

The North America identifier-history product actually supplies international issue ISIN/SEDOL histories for these issuers. All seven old local ISIN records missing from the original current-master review are present. Global W-suffix histories in this result contain ISIN/SEDOL, with no dated EXCHG/TIC records. Preserve the prior venue/class evidence and that limitation. Do not infer a listing start from a nominal identifier start or from the 2900-01-01 open-ended sentinel.

## Validation completed

- Extracted 88,055 local observations for the 17 requested stable issue keys. All 17 have data, with actual series starts/ends in the private coverage audit. The additional 263,692 observations remain in raw only and are excluded by stable keys.
- Joined historical identifiers using stable keys and effective dates. Fifteen local observations have no matching interval and are explicitly retained in an exception file. There are no ambiguous interval matches or duplicate local security/date keys. Two requested local rows have missing closes. Nonblank currencies agree with the requested markets; all populated quotation-unit fields equal one. This does not certify historical quote scale.
- The three duplicate CRSP dates differ only in distribution fields. Prices, returns and the other daily payload agree. The original 23,461 rows remain unchanged. A separate unique daily file has 23,458 rows, without distribution columns; corporate-action detail stays in raw and in the prior descriptor extract.
- Identified the four exact active NYSE receipts in the extension by stable key, dated ISIN and exchange history, current ticker, venue and USD currency. Retained 276 observations and excluded 274 other listing observations. Each receipt has 42 August–September overlap dates and 27 October–November observations, ending November 6. All 168 overlap closes agree with CRSP within one cent.

## Required next work on ORC

Read the site `AGENTS.md` and referenced ORC instructions first. Receive and verify the ZIP and delivery manifest privately, extract into the named new directory without overwriting a different snapshot, then verify the internal manifest. Reject unsafe archive paths and symlinks. Keep licensed rows out of public commits. Pull current public `main` for this instruction, the November 11 handoff, and the [exact acquisition request](WRDS_DAILY_PRICES_AND_MAPPING_REQUEST_20261112.md).

Run the private snapshot's portable `audit_acquisition.py` to regenerate its prepared files and compare the audit totals. Review the new identifier histories alongside the November 11 public transition evidence and ratio intervals. This audit does not grant blanket analysis readiness.

Resolve or bound the following before the affected regressions:

1. Investigate the 15 mapping exceptions: early Shell B, the first BYD A observation, and early Hyundai third-preferred records. Do not silently drop them or invent validity dates. Keep raw rows and explain any sample restriction.
2. Inspect actual first positive price dates and gaps. Hyundai's third preferred series has its first positive close in May 2006. Ping An A begins in this export in March 2007 after the public listing start. Some series have long gaps; distinguish missing coverage, suspensions and exchange holidays. Local price-status codes 5/10, nontrading/stale quotes, missing/zero volume and official calendars need explicit interpretation.
3. Establish Shell's historical pound/pence scale against prices and FX. Preserve QUNIT as vendor evidence, not proof of the conversion. Validate split-factor direction and independently dated local/ADS ratio changes, including asynchronous local/US split windows and Shell/Roche transitions.
4. CRSP RDS.B includes a final post-trading metadata row with a missing price. CRSP RDS.A starts later than the public listing date. Preserve those coverage limits. Treat conditional SHELWI separately from regular-way SHEL.
5. Reconcile adjustment, dividend and return definitions over the US-provider overlap before extending a return series beyond September 30. The extension has Compustat prices/actions, not CRSP-specific return/quote flags. No return splicing has been performed.
6. Preserve exchange-close time zones and point-in-time FX availability. Daily prices alone do not establish executable arbitrage, borrow availability or NAV coverage.

The Global form did not expose daily open price or ADR ratio fields. Do not manufacture these fields. They are not required for every close-based specification, but any specification that needs them must identify another documented source.

## Research scope

The collected prices and historical identifiers support building the nine requested comparison panels: Alibaba, HDFC Bank, Shell, Novo Nordisk, BYD A/H, Ping An A/H, Hyundai common/preferred classes, Roche voting/nonvoting/participation, and Volkswagen ordinary/preferred. Release each security/date interval after its remaining checks. The prior validated regressions can proceed independently; ownership/NAV and intraday execution inputs remain separate requirements. Do not restart paused research jobs merely because this receipt exists.
