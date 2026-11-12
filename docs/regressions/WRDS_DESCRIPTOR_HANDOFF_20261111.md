# WRDS descriptor collection and SSH handoff

The November 11 BYU/WRDS screen-control pass collected six source CSVs (805 rows), their exact generated SQL, a source manifest, and review evidence. This public repository contains the verification code and public search seeds. The licensed CSVs, row-level crosswalk and UI evidence travel separately to authorized BYU storage; they are not Git content.

For the next acquisition, read the [November 12 exact daily-price and historical-mapping request](WRDS_DAILY_PRICES_AND_MAPPING_REQUEST_20261112.md). It adds the `sec_idhist`/identifier-package discovery step; the limited `g_sec_history` result does not establish that identifier histories are unavailable elsewhere. The original ZIP and its checksum remain unchanged.

## Collection directory and guide

Canonical repository-relative directory after transfer:

`data/acquisition/2026-11-11/wrds_descriptor_review/`

On the originating Windows workstation this directory is under `C:/Users/pinol/Documents/.FALL 2026/MRP/MRP-Project/`. `README.md` explains every raw and prepared file. `WORK_LOG.md` records acquisition actions, job IDs, filename changes and limitations. `COLLECTION_AND_REVIEW.md` summarizes the completed identity review. `manifest.json` records exact SQL paths, source tables, execution clocks, counts and SHA-256 hashes. Job-page timestamps have no stated timezone; do not relabel them Mountain Time.

| Descriptive filename in raw/ | Rows | Contents |
| --- | ---: | --- |
| compustat_global_security_master_9_issuers.csv | 144 | Current/inactive security descriptors across nine issuers and their other listings/classes |
| compustat_global_listing_and_participation_history.csv | 44 | Effective-dated listing, participation and primary-issue items; not ISIN/ticker histories |
| crsp_us_receipt_name_history.csv | 45 | Security-information histories for the requested US receipt families |
| compustat_exchange_code_dictionary.csv | 231 | Exchange-code descriptions |
| crsp_us_receipt_corporate_actions_2005_2026.csv | 225 | Distribution/split event records, with separate ex, record and payment dates |
| compustat_quote_currency_units_snapshot_2026-11-06.csv | 116 | One-date company/issue/currency/unit metadata; no price, volume or return columns |

The source CSV bytes are unchanged; random WRDS names map to descriptive names in the manifest. The source snapshot requests 2005-01-01 through 2026-11-06, limited to live issues. CRSP's available edition ends 2026-09-30. The one-date currency snapshot does not establish historical units.

## What crosswalk review established

A crosswalk maps public security identifiers to vendor security records while checking class, exchange, currency and effective dates. An issuer match or ticker alone is insufficient.

The completed local review verifies all acquisition-manifest hashes, unique company/issue keys, exact local ISIN and venue matches, preferred/common class descriptions, snapshot currency/positive quote units, and US historical CUSIP/PERMNO/NYSE/depositary-class matches within the requested period. It accepts 16 current local identities, one inactive local identity, and six US receipt identities. One Alibaba record is a historical receipt-ratio basis rather than another security. Seven historical local identifier records remain unresolved.

Identity acceptance is not evidence that a full historical panel is ready. The review therefore does not release the held full daily pull or approve new nine-pair regressions. It saves separate decisions in `identity_review/`, preserving the original acquisition manifest and raw bytes.

Material remaining checks:

1. Establish historical local ISIN/ticker validity and issue continuity, especially HDFC, Novo, old Shell A and Roche's nonvoting exchange. Do not guess old IIDs from current identifiers.
2. Establish historical quote units, currencies and live coverage. Shell's current GBP/QUNIT snapshot does not certify old pence/pounds scaling.
3. Close the US October-November 2026 coverage gap with an entitled source if those dates are required. Global receipt records listed in London/Germany are not NYSE substitutes.
4. Preserve Shell's conditional when-issued day separately from regular-way trading. Reconcile the Shell A vendor-series start discrepancy rather than inserting observations.
5. Retain source-specific Novo 2007 payment/distribution dates. Trading/ex dates have been checked separately.
6. Review receipt ratios on matched share bases and exclude asynchronous split windows until their conversion/share basis is validated.

The newly confirmed HDFC 2011 US ex-date is July 25; it differs from the July 14 local ex-date. Full date details and licensed vendor evidence are in the private package, not in public data rows.

## Receive and verify on SSH

The user will upload `wrds_descriptor_review_2026-11-11.zip` and `wrds_descriptor_review_2026-11-11.delivery.json` to an authorized private location on BYU storage. Their presence is separate from a Git pull. The delivery JSON gives the ZIP SHA-256 and an inventory of packaged files.

Read applicable BYU site instructions, preserve existing work, and inspect current Git state. Fetch/pull this handoff without resetting or overwriting local changes. Do not restart paused research jobs solely because this document exists.

Verify the ZIP hash against the separately supplied delivery JSON. The ZIP's entries are relative to the collection directory. Extract into a new `data/acquisition/2026-11-11/wrds_descriptor_review/` directory; do not overlay a differing snapshot. Reject absolute paths, traversal components or archive symlinks. Compare extracted files to the delivery inventory, then verify the original acquisition manifest with the command below. Do not run the old `build_review.py` on SSH: it records workstation-specific original-file paths and is retained as acquisition provenance. Use the portable reviewer instead.

```bash
python scripts/review_wrds_crosswalk.py \
  --bundle data/acquisition/2026-11-11/wrds_descriptor_review
python tests/check_wrds_crosswalk.py
```

Use the existing approved Python environment. These commands use only Python's standard library, perform no network operations, and submit no compute jobs. Hash changes or conflicting records fail validation. Review output stays inside the ignored private bundle.

## Continue research

Regression families supported by the existing validated server inputs are Samsung common/preferred discount and factor models (B01-B04 and their registered sensitivities); SK Square/SK Hynix and Samsung Fire/Samsung Electronics price-return/gap associations; TSMC local/ADS parity and return comparisons; and Prosus/Tencent/Naspers return pass-through and normalized-gap models. Existing US share-class LOOP comparisons can also continue using the shared assets where their configured inputs remain available. These are price/factor associations, not completed NAV or executable-arbitrage tests.

The new exact-local comparisons are Alibaba/HDFC/Shell/Novo primary-versus-receipt, BYD/Ping An A-versus-H, Hyundai common-versus-preferred, Roche voting-versus-nonvoting, and Volkswagen ordinary-versus-preferred. This ZIP improves their identities and transition evidence; their daily panels and remaining historical gates are still needed. Dated ownership and parent-only NAV inputs remain separate requirements for NAV regressions.

Reconcile this package with the [November 9 inventory](../data_acquired/DATA_EXPORT_INVENTORY_20261109.md), the actual shared assets, [LOOP acquisition brief](STILL_REQUIRED_DATA_ACQUISITION_BRIEF_20261109.md), public candidates and transition seeds. Reuse the 17 original core inputs, Samsung export and Prosus bundle in place; do not rerun completed vendor queries.

Existing validated core/Samsung/Prosus regressions are independent of the nine new LOOP descriptor gaps. Continue only currently authorized work, with the established 2/5/10-year structural research scope and normal scheduler rules. For the nine new comparisons, resolve period-specific identity and unit gates, freeze exact verified identifiers, and explicitly record the released acquisition intervals before pulling full daily prices. Do not turn absent data into zero values or count blocked regressions as null findings.

The package recovers saved Global daily query specification 7980223 and an existing TSM query-summary job ID 11890165 without rerunning either. Other original query provenance remains incomplete. Six new descriptor/event/metadata SQL files are not substitutes for missing original core SQL.
