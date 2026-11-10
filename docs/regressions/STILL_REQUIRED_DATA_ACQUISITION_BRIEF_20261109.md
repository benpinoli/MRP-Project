# Still-required data acquisition brief

Checkpoint date: November 9, 2026  
Project: LOOP exceptions and core-pair regressions  
Purpose: obtain the smallest auditable inputs needed to move currently blocked hypotheses into estimable tests.

## Acquisition priorities

1. Build dated Korean ownership and NAV histories for SK Square/SK Hynix and Samsung Fire/Samsung Electronics.
2. Obtain exact local legs and identifier histories for the blocked primary/ADR, A/H, and local-class comparisons.
3. Build point-in-time NAV histories for Exor/Ferrari and Industrivarden/Volvo.
4. Recover the original WRDS queries and export metadata for already-delivered core files.
5. Obtain execution and borrowing data before promoting any price signal to a trading result.

Raw vendor exports must remain byte-for-byte unchanged and outside Git. Derived panels may be regenerated, but never overwrite the delivered raw file.

## 1. Korean ownership and NAV histories

### Required pairs

| Holdco/security | Economic holding | Frozen identifiers |
| --- | --- | --- |
| SK Square | SK Hynix | SK Square Global GVKEY/IID 350948/01W; SK Hynix 204049/01W |
| Samsung Fire & Marine | Samsung Electronics common | Samsung Fire 208765/01W; Samsung Electronics common 104604/02W |

### Ownership history required

Obtain a dated observation for every fiscal quarter when available, or at minimum every fiscal year, from the first usable price date through November 6, 2026. Each row must contain:

- Holder entity and held security, including class.
- Effective or measurement date.
- Number of held shares and ownership percentage.
- Held-company shares outstanding used for the percentage.
- Direct versus indirect ownership and the controlled affiliate, if applicable.
- Treasury shares and cross-holdings separately identified.
- Filing/publication date and time, including timezone when available.
- Filing type, source URL or vendor document ID, page/table reference, and whether the value is original, amended, or restated.
- Unit and split basis. Record the corporate action used to restate historical shares; do not silently restate the raw filing.

The filings and ownership CSV already present, including commit `3666efa`, are individual observations. They should be retained as rows in this history, not treated as a complete series.

### NAV components required

For each holdco observation date, collect the values publicly knowable at that date:

- Market value inputs for the named holding: owned shares multiplied by the eligible held-security price.
- Other listed investments, with security identifiers and quantities.
- Unlisted investments at reported carrying value, with valuation date and method.
- Parent-only cash and cash equivalents.
- Parent-only debt and other net liabilities.
- Pension, provisions, minority interests, preferred claims, and material off-balance-sheet obligations.
- Tax or disposal-cost assumption, reported separately rather than netted invisibly.
- Holdco treasury shares and diluted economic shares outstanding.
- Publication date/time and revision vintage for every accounting value.

Consolidated statements must not be used as parent-only NAV inputs unless intercompany and held-company consolidation effects are explicitly removed. Forward-fill is allowed only in a declared point-in-time test after the value's public availability date.

### Preferred delivery shape

Deliver one long CSV per pair with stable columns such as:

`pair_id, observation_date, public_at, holder_gvkey, held_gvkey, held_iid, owned_shares_raw, owned_shares_split_adjusted, ownership_pct, held_shares_outstanding, parent_cash, parent_debt, other_liabilities, other_listed_assets, unlisted_assets, tax_assumption, holdco_shares_outstanding, currency, source_file, source_page, revision_status`

Also deliver every original filing or vendor export referenced by the CSV.

## 2. Exact local-security exports

### Comparisons still needed

| Relationship | Exact securities required | Do not substitute |
| --- | --- | --- |
| Alibaba primary/ADR | Hong Kong primary ordinary and US ADR | OTC proxy or current ticker-only match |
| HDFC primary/ADR | Indian primary and the historically corresponding US ADR for its live period | A post-merger identifier applied backward |
| Shell primary/ADR | Exact primary ordinary line and US ADR/ADS for each historical structure | Unverified OTC cross-listing |
| Novo Nordisk primary/ADR | Danish primary and US ADR | OTC ordinary proxy |
| BYD A/H | Exact Shenzhen A share and Hong Kong H share | US OTC receipts |
| Ping An A/H | Exact Shanghai A share and Hong Kong H share | US OTC receipts |
| Hyundai common/preferred | Korean common and exact preferred class or classes declared in the hypothesis | US OTC ordinary proxy |
| Roche voting/nonvoting | Swiss bearer/voting and participation/nonvoting lines with the March 17, 2026 ROG-to-ROP history | US unsponsored receipts |
| Volkswagen common/preferred | German ordinary and preferred shares | VWAGY/VWAPY proxy as the final test |

Target daily coverage is January 1, 2005 through November 6, 2026, or the complete live history when a security starts later or terminates earlier.

### Required daily fields

- Stable vendor security identifiers: GVKEY/IID or equivalent, ISIN, SEDOL, CUSIP where applicable, exchange code, and local ticker.
- Effective-dated name, ticker, identifier, exchange, status, and primary-security history.
- Trading date and local exchange calendar.
- Raw close, close-status code, currency, quote unit, volume, and shares outstanding.
- Split/adjustment factor, dividend/total-return factor, split fields, cash dividends, ex-date, and distribution type.
- Bid, ask, quoted spread, and preferably depth when licensed and available.
- Delisting, suspension, merger, conversion, class-unification, and identifier-change events.
- Exchange close timestamp and timezone, including historical daylight-saving handling.

For ADRs/ADSs also obtain:

- PERMNO or another stable US security identifier and effective-dated name history.
- Depositary bank, ordinary shares per ADS, ratio effective dates, fees, and creation/cancellation eligibility.
- ADR dividends and withholding treatment sufficient to reconcile cash rights.
- CRSP-style price, return, volume, bid, ask, cumulative price factor, cumulative share factor, and delisting return where available.

### FX and market-clock data

Obtain the applicable foreign-units-per-USD series with source, observation time, timezone, vintage/retrieval date, and holiday policy. A daily fixing after the local close may be used only for a retrospective comparison and must not be labeled point-in-time. For executable timing tests, obtain synchronized or bounded intraday FX quotes spanning both market closes.

### Identifier-resolution export first

Before requesting the full daily extract, obtain a compact descriptor/history export for every candidate. Confirm exact economic class, exchange, country, currency, active dates, and receipt ratio. Freeze the verified identifiers in configuration before building prices. Conflicting histories should block the pair rather than be manually guessed.

## 3. Holdco NAV histories beyond Korea

### Exor/Ferrari and Industrivarden/Volvo

For each published NAV date, obtain:

- Exact shares owned and ownership percentage in the named listed holding.
- All other material listed positions and quantities.
- Unlisted asset valuations and valuation dates.
- Parent-only cash, debt, liabilities, tax assumptions, and diluted holdco shares.
- Published NAV, if supplied, with the issuer's definition and reconciliation.
- Publication timestamp and original report/presentation.
- Corporate actions affecting the holdco or holding, including distributions, spin-offs, tender offers, and share cancellations.

Monthly published NAV observations are preferred. Quarterly observations are acceptable if monthly history is unavailable. Do not infer historical holdings from a current portfolio page.

The same structure can later be extended to Prosus/Tencent, Naspers/Prosus, Liberty Broadband/Charter, BN/BAM, SoftBank/Arm, and Investor AB/Atlas when the objective moves from return pass-through to NAV-discount explanation.

## 4. Missing WRDS query provenance

The price baselines are complete, but the following original executable queries or query specifications are missing:

- Compustat Global daily-security export.
- Compustat Global annual fundamentals export.
- CRSP TSM daily export for 2005–2025.
- CRSP TSM daily export for 2026.
- CRSP TSM name history.
- Compustat Global company, security, and security-history descriptors.

For each export, provide:

- Exact WRDS library and table names.
- SQL or saved-query text with every selected field, filter, join, and sort key.
- Requested start/end dates and identifier filters.
- WRDS execution/export timestamp and timezone.
- Output format and delimiter options.
- WRDS dataset vintage or last-update date when exposed.
- Row count, file size, and SHA-256 of the delivered export.
- Any manual post-export action. Prefer none; if unavoidable, retain both the untouched export and the transformation code.

The existing quarterly-fundamentals SQL and Compustat North America ADR SQL should be used as examples. A query-summary PDF is supporting metadata, not a substitute for executable SQL.

## 5. Fundamentals and publication clocks

For every slow-moving accounting or ownership field used in a predictive or event-time design, obtain:

- Fiscal period end.
- First public announcement/filing timestamp.
- Vendor availability timestamp, if different.
- Original value and every revision/restatement with its date.
- Currency, units, consolidation scope, accounting standard, and fiscal-year convention.

Vendor `fdate` or `pdate` fields alone are not proof of the original public-release clock. Preserve the vendor fields, then independently document the filing or announcement clock when the test requires point-in-time validity.

## 6. Borrowing and execution inputs

These are required before any z-score or mean-reversion diagnostic becomes a portfolio claim:

- Daily lendable quantity and utilization for each leg.
- Indicative and realized borrow fee, rebate, and recall events.
- Locate success/failure and hard-to-borrow status.
- Applicable short-sale restrictions, uptick rules, foreign-ownership limits, and market bans with effective dates.
- Executable bid/ask quotes, depth, auction status, and trading halts.
- Commissions, exchange fees, stamp taxes, ADR/depositary fees, FX costs, withholding taxes, and conversion/creation fees.
- Dividend and manufactured-dividend cash flows by leg.
- Settlement calendar, settlement currency, and failures/recalls.

Minimum useful frequency is daily. Intraday quotes are preferred for cross-market price-discovery tests. Missing borrow must remain missing; it must not be interpreted as zero cost or full availability.

## 7. FRED and external-series provenance

For DEXKOUS, DEXTAUS, and any later FX/rate series, retain:

- Raw downloaded file without edits.
- Series ID, source URL/API endpoint, retrieval timestamp, and timezone.
- Units and fixing/observation time.
- Vintage or realtime start/end parameters if available.
- Missing-value code and holiday treatment.
- SHA-256 and a short retrieval script or command.

## 8. Delivery and acceptance checklist

A delivery is ready for panel construction only when all applicable checks pass:

- Raw files are stored below a Git-ignored `data/acquisition/YYYY-MM-DD/<bundle>_raw/` directory.
- Raw filenames are stable, descriptive, and never reused for transformed files.
- A manifest records byte size and SHA-256 before any parsing.
- Executable query/retrieval code is delivered beside, but separate from, raw output.
- Identifier and descriptor exports establish the exact securities and effective dates.
- Duplicate keys are classified as exact duplicates or conflicts; conflicts block construction.
- Currency, quote units, adjustment factors, corporate actions, and receipt ratios reconcile.
- Missing fields are counted by security and period; unavailable fields remain missing.
- Market-close and FX observation times are documented.
- Publication timestamps and revision vintages are present for point-in-time fields.
- Licensed raw data and derived row-level licensed panels remain outside Git.
- A small README states what was requested, what was delivered, coverage, known gaps, and contact/date.

## Suggested bundle layout

```text
data/acquisition/YYYY-MM-DD/<bundle>_raw/
  README.md
  manifest.json
  queries/
    <export_name>.sql
  descriptors/
    company.csv
    security.csv
    security_history.csv
  daily/
    <exact_vendor_export>.csv
  fundamentals/
    annual.csv
    quarterly.csv
  ownership/
    ownership_history.csv
  filings/
    <original_documents>
  fx/
    <raw_series>.csv
    retrieval_metadata.json
```

Do not place licensed raw rows, filings with redistribution restrictions, or derived licensed row-level panels in tracked documentation. Tracked reports should contain only permitted aggregates, hashes, methodology, and results.
