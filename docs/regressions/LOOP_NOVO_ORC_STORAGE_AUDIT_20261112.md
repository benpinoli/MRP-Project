# Novo measurement: ORC storage audit — November 12, 2026

Continuation of [the measurement checkpoint](LOOP_NOVO_MEASUREMENT_CHECKPOINT_20261112.md). This public note contains aggregate findings and delivery receipts only. Licensed rows, identifiers/crosswalks, account observations, detailed storage catalogs and source captures remain private. No regressions, model search, empirical verdict changes or new qualified measurement observations.

## Verification and preservation

- Original pilot ZIP verified against trusted SHA-256 `6e5e2a57a99f22f1c1285152be79f0c25f8bca4a97f8ddc84e277ba6e61b6f91`: **3,792,783 bytes; 118 file entries**. Every entry matched the separate inventory; extracted files were rehashed. CRC, safe-path, duplicate-name and symlink checks passed. Extracted into a new ignored private supplement rather than an existing snapshot.
- All five prior bundle archive hashes, every archived entry and corresponding installed snapshot file verified unchanged. All explicitly reused pilot references resolved and passed size/hash verification. Older bundles and results were not regenerated.
- Current main was merged without overwriting existing modified/untracked work. Applicable repository and ORC guidance was read; aggregated integrity/schema work ran in Slurm.

## Silver Fund storage result

**No usable USD/DKK dataset was identified within the inspected scope.** This is a bounded negative finding, not evidence that no FX exists elsewhere in school storage.

Inspected authorized Silver Fund legacy data and research/production/development/fundamentals catalogs, plus the group's archive/autodelete roots. Recorded **2,117 filenames in 75 immediate nonprivate table directories** and **80 representative Parquet footer schemas**. No FX filename candidate was identified. Schema inspection read metadata, not underlying observation rows; it does not certify schema homogeneity across all years or cover every nested directory. The group archive/autodelete roots were empty at inspection. Private resolved directories and nested fundamentals source extracts were not recursively searched.

Currency-related fields were equity quotation-currency/identifier labels or fundamental fields. Barra equity returns had price, currency, source and date metadata; equity asset tables had daily/rolling spread fields. These do not establish a currency-pair rate or timestamped FX bid/ask. A microsecond timestamp storage type does not establish a source event clock, timezone or actual quote precision. Representative equity date bounds are not USD/DKK coverage.

Selected pipeline documentation identified a separate upstream MSCI Barra archive route. This account lacks permission to that path and is not in its access group; inspection stopped. No credentials were read, no access was inferred from installed libraries, and no restriction was bypassed. Full paths, schemas, native column names, query responses, code-declared products and file metadata are in the private supplement.

Still unresolved for USD/DKK: exact dataset path/table, provider/product/contributor, pair/date coverage, native quotation direction and units, bid/ask versus midpoint/fixing, event and publication clocks, actual timestamp precision, timezone/DST, condition/correction semantics and license. No new Silver Fund intraday or daily FX observations were retained. The previously delivered public raw FX hour remains unqualified.

## Measurement and provenance status

- Twenty frozen dates unchanged: December 3–7, 2007; March 3–7, 2014; November 1–3 and 6–7, 2023; March 3–7, 2025. The delivered `prepared/calendar_selection_frozen.json` remains authoritative and byte-identical. Provider-calendar qualifications, missing original Copenhagen 2007/2023 calendars, known disagreements and historical UTC/DST conventions remain explicit.
- All **60 primary component slots** remain present, with **zero qualified event-aligned observations**. Quote ages and eligibility remain unknown without actual auction events and validated quote clocks. Forty inherited daily comparator inputs remain explicitly asynchronous. No missing date, receipt listing, daily fixing or later US close was substituted.
- WRDS Daily `taqm_common` and Monthly `taq_common` forms explicitly denied BYU subscription; no new TAQ query attempted. Nasdaq archive and LSEG Tick History entitlement/coverage remain unverified. December 2007 requires pre-INET Copenhagen records; 2014 and later periods need their applicable historical schemas.
- Independently reread targeted SEC 2007/2014 split notices through the public web reader. The December 2007 asynchronous local/ADR trading basis and announced depositary conversion suspension remain material gates. Candidate unit alignment is not certified legal conversion. Issuer distribution versus vendor payment-date disagreement remains preserved. Ordinary direct downloads returned 403 and index lookups failed; no original filing bytes or verified first-publication/acceptance clock were newly acquired.
- All five pre-2005 provenance intervals remain held. The 2000 demerger and 2001 basis transition stay separate. Current listing codes do not establish historical quote venue/feed provenance.

## Private supplement receipt

Stored under ignored `data/acquisition/2026-11-12/` on ORC:

- `novo_measurement_orc_supplement_2026-11-12_v1.zip`: **3,916,817 bytes; 164 file entries**.
- SHA-256: **`706babe8f04abc3a1c42a815dbdb0f816e9f7b65817529d15f362fe6f9bd23ab`**.
- Separate `.inventory.json`, `.delivery.json` and `.sha256` files. Inventory SHA-256: `cfda4fd04d18552466c0262da10f0647f5fbb9531af45ec9a73f715377f91006`.
- Every supplement archive entry hash and CRC verified. Root `novo_measurement_orc_supplement_v1/` contains the verified received pilot, raw source/documentation and denial evidence, exact queries, source inventory, schema/coverage/quote-age audits, interval decisions, README and work log.

These private files have **not** been transferred to the acquisition laptop by publishing this note. If needed locally, transfer ZIP and sidecars through an approved private channel, verify them, and extract into a new ignored directory. Existing local pilot/five-bundle evidence can be reused without waiting for another copy. Do not publish licensed data or UI captures.

The next local collection instructions are in [LOOP_NOVO_LOCAL_COLLECTION_PROMPT_20261112.md](LOOP_NOVO_LOCAL_COLLECTION_PROMPT_20261112.md).
