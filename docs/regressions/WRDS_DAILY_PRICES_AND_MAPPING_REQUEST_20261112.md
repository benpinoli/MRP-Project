# Exact request: daily prices and historical security mappings

This clarifies the next acquisition after the November 11 descriptor package. The original ZIP remains immutable. Read this document from current Git alongside that ZIP's collection guide and private identity review. No full daily pull is released merely by this request: release verified securities and date intervals after the corresponding identity review.

## Confirmed access versus unresolved access

The user's BYU web session successfully queried Compustat Global `g_security`, `g_sec_history`, `r_ex_codes`, and `g_sec_dprc`, plus CRSP monthly-edition names and distributions. The Global daily-price form exposes close/high/low/open, currency, quotation unit, adjustment, volume and shares fields. The metadata-only November 6 snapshot demonstrates that the daily-price table contains records for the issuers; it does not establish each issue's full requested daily coverage.

The collected `g_sec_history` result contains EPF, MKTLIST and PRIHISTROW items only. Do not describe that result as complete historical ISIN/ticker coverage, or infer that historical identifiers do not exist elsewhere.

WRDS separately documents **`sec_idhist`**, covering historical security identifiers, alongside `sec_history`. Its worked example/support link concerns North America, so it is a discovery lead rather than proof that a table literally called `comp_global_daily.g_sec_idhist` exists or is available to BYU. S&P also documents its 2025 migration to modular identifier history/current-span packages and the `SEC_IDHIST`/`SEC_IDCURRENT` delivery structures, including international ISIN and SEDOL history. Actual WRDS schemas, table aliases, populated items and BYU entitlements must be inspected.

Sources checked November 12, 2026:

- [WRDS: Using Compustat Historical Identifiers](https://wrds-www.wharton.upenn.edu/pages/wrds-research/database-linking-matrix/using-compustat-historical-identifier-notebook/)
- [S&P: Compustat Security Identifier Package Change Migration](https://www.support.marketplace.spglobal.com/content/dam/spglobal/mi/en/documents/marketplace/datasets/compustat/naandglobal/cusip-migration-notice.pdf)
- [WRDS: CRSP data coverage overview](https://wrds-www.wharton.upenn.edu/demo/crsp/form/)

The earlier BYU proxy web session does not grant or demonstrate separate WRDS PostgreSQL/SSH credentials. A supercomputer SSH login is not itself a WRDS database login. Use an existing entitled session; if only the user's browser session can access a source, prepare exact query specifications for that browser session.

## 1. Discover and export the correct mapping history

Use the nine comparisons and public seeds in `configs/loop_security_descriptor_candidates.csv`, together with the private reviewed current identities. Preserve all historical seed rows. Do not substitute another company's similarly named ticker, another preferred class, an OTC line or a London/German receipt listing for NYSE.

First inspect the data dictionary/catalog for identifier history and current-span tables across the entitled Compustat Global/security-identifier products. Search for `sec_idhist`, `sec_idcurrent`, ISIN history and SEDOL history, including product-specific equivalents. Do not guess a schema/table prefix or declare a subscription absent from one table's results.

If an already authorized PostgreSQL connection is available, this is a read-only metadata discovery query, not an instruction to establish new authentication:

```sql
SELECT table_schema, table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema ILIKE 'comp%'
  AND (table_name ILIKE '%idhist%'
       OR table_name ILIKE '%idcurrent%'
       OR table_name ILIKE '%sec_history%')
ORDER BY table_schema, table_name, ordinal_position;
```

Also inspect relevant non-`comp%` identifier products if the dictionary shows them. For each candidate table, record schema/columns and, within the nine-issuer scope, populated item types, counts, earliest/latest effective dates, and access errors. A missing table, denied query, empty result and missing identifier item are different outcomes. Record them separately.

Export historical records for exact GVKEY/IID or equivalent stable keys, identifier type/value, effective-from/effective-through, name/ticker, class, venue, primary-line and security-status history where available. Discover actual column names; do not assume `efffrom` and `effthru` match a different table's `effdate`/`thrudate`. Keep current identifiers separate from historical intervals. Preserve open/sentinel endpoints explicitly; they are not independently verified listing starts or every-day trading coverage.

Prioritize the seven unresolved old local identifier records: two HDFC, three Novo, old Shell A, and old Roche nonvoting. Distinguish issuer economic continuity from continuity of the vendor issue record. Use issuer/exchange/depositary evidence to corroborate splits and conversions, not to invent vendor validity intervals. If the entitled identifier feed cannot supply a needed history, document that exact limitation and use a separately evidenced mapping; keep the affected period blocked until review.

For US receipts, reuse the delivered CRSP name history and PERMNO evidence. Prefer direct PERMNO-scoped history once verified; a header-CUSIP filter alone can miss a retired CUSIP. Require historical CUSIP, ticker/trading symbol, class, venue, trading status, name-info intervals and security-data start/end. Keep SHELWI distinct from regular-way SHEL and separate pre-unification A/B records.

## 2. Daily local price request

For each released local security/date interval, request January 1, 2005 through November 6, 2026, bounded by live coverage. Use Compustat Global `g_secd` or its documented underlying daily-price/action tables. **Filter on stable issue keys, not only today's ISIN or ticker.** Reuse existing core/Samsung/Prosus exports; this request targets missing nine-comparison legs.

Required fields, using documented available names:

- `gvkey`, `iid`, `datadate` and independently dated identity/venue/class mappings; preserve any returned ISIN, CUSIP, SEDOL and company-name fields with their actual current-versus-historical semantics.
- `prccd`, `prchd`, `prcld` and `prcod` where available; `prcstd`, `curcdd`, `qunit`, `cshtrd`, `cshoc`.
- `ajexdi`, `trfd`, `split`, `splitf`; dividend amounts/types/currencies, declaration/ex/record/payment dates, and any delisting/suspension/conversion flags available in the product.
- ADR ratio `adrrc` where exposed, as vendor evidence requiring comparison with issuer/depositary terms; it does not replace the independently dated ratio record.

Do not require unsupported columns from a merged form: inspect the schema first, split into documented tables/exports when needed, and record missing fields. Do not infer historical ISIN validity because a daily merged file repeats the current master identifier.

Validate local H shares in HKD, A shares in CNY, Korean classes in KRW, the NSE bank line in INR, Novo B in DKK, Swiss classes in CHF and German local classes in EUR. For Shell separately establish vendor currency/quotation scale against issuer/exchange quotes. A face-value description is not quote currency. Check adjustment-factor direction against independently documented splits before constructing adjusted prices.

## 3. Daily US receipt request

Use CRSP CIZ daily data for the verified PERMNOs, with dated names/distributions as separate exports where appropriate. The existing core export demonstrates fields named `DlyCalDt`, `DlyPrc`, `DlyRet`, `DlyRetx`, `DlyVol`, `DlyBid`, `DlyAsk`, `DlyClose`, `DlyOpen`, `DlyLow`, `DlyHigh`, `DlyPrcFlg`, `DlyRetMissFlg`, `DlyDelFlg`, `DlyCumFacPr`, `DlyCumFacShr`, and `ShrOut`. Inspect the current SQL schema for lowercase/table aliases rather than assuming exported headings are SQL identifiers. Include corporate-action, shares and delisting metadata supported by that edition.

The accessed monthly CRSP edition ended September 30, 2026. Verify its actual latest date before querying. For October 1-November 6, inspect another already entitled exact-US source, such as Compustat North America, and independently match the NYSE receipt; the existing TSM extension is evidence of that route for TSM only, not proof of coverage for these six receipt families. If using a second provider, retain both sources, compare an overlapping interval and report absent CRSP-specific fields. Otherwise end the affected comparison at the supported common date and state the gap.

Daily bid/ask values are not synchronized intraday executable quotes or borrow data. Do not label their presence an implementable arbitrage test.

## 4. Validation and delivery

Freeze one reviewed row per exact security and valid date interval before the corresponding full pull. Record separate approvals for acquisition identity and analysis readiness; resolve only the affected period when evidence is partial. Do not blanket-approve all nine histories.

Retain immutable raw bytes, exact SQL/form specifications, actual provider/table and retrieval/edition clocks. Hash each file and report counts, actual first/last observations per issue, duplicate security/date keys, currency/unit changes, gaps and unmatched mappings. Historical joins must use stable keys **and** effective dates, avoid duplicate overlapping matches, and retain unmatched observations in a quarantine/audit output rather than silently dropping them.

Keep the independently verified local/US split-trading clocks separate from record/payment/settlement dates. Keep asynchronous transition windows flagged. Reconcile unexpected jumps against actions before interpreting them; do not automatically delete unusual valid prices. Preserve exchange calendars, local close/timezone and FX fixing/availability clocks. Daily fixings alone do not establish synchronized or point-in-time comparisons.

Save new licensed data in a new ignored snapshot on authorized storage and report aggregate readiness by comparison. Existing validated regressions can continue independently. New nine-pair regressions require their actual daily panels plus the applicable identity, unit, ratio and timing checks; the descriptor ZIP alone does not supply them.
