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

## BYU receipt and validation — November 12, 2026

The private transfer was received and verified at `data/acquisition/2026-11-11/wrds_descriptor_review/`. The separately delivered ZIP SHA-256 matched its delivery JSON, all 95 archive entries passed path/symlink safety checks, and every extracted file matched the delivered byte count and SHA-256. The separate workstation-named snapshot was preserved rather than overlaid. A private aggregate receipt and dated per-comparison decisions are stored inside the ignored bundle; no licensed row was added to Git.

The portable review verified all six original export hashes and 805 raw rows before writing review output. Four synthetic checks passed. The reproduced aggregate decisions are 16 current local identities accepted, one inactive local identity accepted, six US receipts accepted, one historical ratio-basis record, and seven unresolved historical local records. No full historical panel is approved and no daily pull is released.

The required default reviewer command exposed a packaging interaction: it rewrites two generated files under `identity_review/` that are also members of the immutable delivery inventory. The source/raw hashes passed first and no raw or prepared source changed. The two generated delivery files were restored byte-for-byte from the verified ZIP, the delivery inventory returned to zero mismatches, and the reviewer was rerun successfully with a separate ignored output directory, `ssh_identity_review_20261112/`. Future receipt validation should use a separate `--output` directory when the delivered review files are part of the package manifest.

Existing server inputs were reconciled without reacquisition: all 17 November 9 core files match their baseline manifest, the Samsung source matches its registry hash, and the Prosus archive matches its checksum. Thirty-one of the 32 shared annual asset files still match the prior LOOP run by size. The shared `assets_2026.parquet` has been refreshed since that run; the old result remains tied to its immutable manifest, while any future run must freeze the new source metadata. No scheduler job was active or submitted during receipt validation.

### Comparison-level acquisition decisions

| Comparison | What can proceed | Remaining gate and next exact step |
| --- | --- | --- |
| Alibaba | Exact current Hong Kong and US receipt identities can enter a bounded identifier/ratio review. | Discover entitled historical identifier/current-span records and certify the dated matched-share ADS basis before releasing prices. |
| HDFC | Reuse the accepted receipt history and documented split clocks. | Resolve two old local identifiers and the effective issue chain; preserve the July 14 local versus July 25 US 2011 ex-date separation. |
| Shell | Reuse accepted receipt histories, inactive Shell B identity and the separate SHELWI transition record. | Resolve old Shell A, historical GBP/GBX scale and the July 20-versus-25 vendor start discrepancy; keep conditional January 31 trading separate. |
| Novo Nordisk | Reuse the accepted receipt identity and verified split-trading clocks. | Resolve three old local identifiers and retain the 2007 vendor payment, ex-trading and issuer distribution dates as separate clocks. |
| BYD | Freeze the current Shenzhen A and Hong Kong H identities; exclude the RMB counter. | Obtain effective-dated identifier, currency/unit and live-coverage history before a bounded A/H pull. |
| Ping An | Freeze the current Shanghai A and Hong Kong H identities; exclude the RMB counter. | Obtain effective-dated identifier, currency/unit and live-coverage history before a bounded A/H pull. |
| Hyundai | Freeze current common and three preferred identities for class-by-class review. | Verify historical class continuity, rights, metadata and the exact preferred comparison before prices or regressions. |
| Roche | Reuse current voting/nonvoting identities and public March 2026 transition evidence. | Resolve the old ROG record and freeze separate pre/post ROP intervals before a daily pull. |
| Volkswagen | Freeze the two current Xetra class identities; exclude Frankfurt/OTC substitutes. | Obtain effective-dated Xetra identifier, currency/unit and live-coverage history before prices. |

The next common query is read-only catalog discovery for the entitled `SEC_IDHIST`/`SEC_IDCURRENT`-equivalent product described in `WRDS_DAILY_PRICES_AND_MAPPING_REQUEST_20261112.md`, followed by one separately reviewed issue/date interval at a time. Current-master acceptance alone does not authorize any of the nine daily panels.

Independent completed regressions remain usable: Samsung B01–B04 and registered sensitivities, the three core-pair price/gap suites, Prosus/Tencent/Naspers return and normalized-gap models, and existing US share-class LOOP tests tied to their frozen inputs. The active structural interpretation remains the 2/5/10-year scope. Daily forecast selection and previously paused programs were not restarted.
