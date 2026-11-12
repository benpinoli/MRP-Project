# Long-history acquisition handoff — November 12, 2026

Independent work on the existing validated samples can proceed now. Do not wait for the structural supplement to audit the new histories or perform the protocol-authorized coefficient-drift, fixed train-only regularization, and nonoverlapping-period checks. Follow site instructions and the existing research protocol; do not restart a paused job solely because this receipt exists. Acquisition alone does not change any hypothesis verdict.

## Private transfer

The user supplies these archives and their separate delivery JSON files through an approved private path. They are not in Git. Preserve existing snapshots and verify archive size/SHA-256 and every entry hash before use; reject unsafe paths and symlinks.

| Snapshot | Archive | SHA-256 |
| --- | --- | --- |
| November 11 descriptors | `wrds_descriptor_review_2026-11-11.zip` | `d8ab4624c9536d9d8789e091886f43b3de8b83bf436d98f50c8412289e4b1748` |
| November 12 daily/mapping | `wrds_daily_and_mapping_2026-11-12.zip` | `a65bfef416b82720c6c8200a64905e6d8fbfdb08d1515d8225ee955cd681bf97` |
| Long-history follow-up v1 | `loop_long_horizon_followup_2026-11-12_v1.zip` | `35a754dd094f50d611c0c95f4a5077a3aa45b43bb3917b9f3c84b950e8f8ae0a` |

Local source directories are under `data/acquisition/2026-11-11/wrds_descriptor_review/`, `data/acquisition/2026-11-12/wrds_daily_and_mapping/`, and `data/acquisition/2026-11-12/loop_long_horizon_followup/`. Recreate those paths privately if required by the portable audits. Read each README, private `REMOTE_AGENT_HANDOFF.md`, coverage matrix, source inventory and prerequisite hash references. The v1 long-history archive is 648,953,971 bytes and contains 273 entries.

## Start here on the supercomputer

Read `AGENTS.md`, `docs/regressions/LOOP_LONG_HORIZON_PROTOCOL_20261112.md`, `LOOP_LONG_HORIZON_RESULTS_20261112.md`, `LOOP_NEXT_DATA_REQUEST_20261112.md`, and the November 11 descriptor / November 12 prices-and-mapping handoffs. Preserve local work while synchronizing main. Use a new versioned data/specification branch and output directory. Retain the original results as the baseline.

The incremental raw pre-2005 exports contain 56,634 Global daily rows and 6,843 CRSP rows. Raw distribution duplicates stay intact. Review `prepared/daily_coverage_audit.csv`, `source_coverage_matrix.csv`, `dated_identifier_history_selected.csv`, and `crsp_duplicate_date_audit.csv` before constructing samples. No estimation sample or adjusted/spliced return series has been certified by acquisition.

Release security/date intervals only after stable-identity, currency/quote-unit, split/receipt-ratio, status/missing-price, corporate-transition and venue checks. Quarantine pre-Xetra Volkswagen; Global quote provenance is not established by a present-day exchange code. Keep early Novo predecessor/de-merger and Nasdaq observations separate from the exact NYSE receipt. Hyundai third preferred has no positive pre-2005 price. Preserve dated identifiers and local/US split-clock differences. Determine 24/60/120-month eligibility from actual qualified history and matured labels, not the requested export start.

Price-based qualification can proceed independently of annual ownership or fee additions. If an exact-venue specification cannot be qualified, document that exclusion and continue independent existing-sample checks. Do not silently relax the venue definition to obtain a longer series. Structural features with unknown first-publication dates remain retrospective evidence and cannot be backfilled into historical forecast origins.

## Final supplement receipt

The separate private snapshot `data/acquisition/2026-11-12/loop_gap_closure_supplement/` is packaged as `loop_gap_closure_supplement_2026-11-12_v1.zip`, **267,222,781 bytes**, **138 entries**, SHA-256 **`a7ad04c4143bf5a7c4b99fe712daedd45d604eead99f5ea817e07a6e5809a5dc`**. Its separate `.delivery.json` contains the full entry inventory and hashes. All entry hashes, CRC and the three earlier archive hashes were verified. The user must still transfer this private archive and JSON; a public receipt does not mean the files have reached ORC.

It contains unchanged 378-row annual issue supply and 402-row annual descriptor exports, their downloaded SQL, additional issuer reports and final depositary cash notices. All378supply rows uniquely match the annual currency/adjustment descriptors on full security/date/format/fiscal-month keys;24descriptor-only rows remain in raw. Actual annual coverage begins1981for Hyundai common and1989for other classes, with material missing preferred/treasury values.

Read its README, REMOTE_AGENT_HANDOFF.md, prepared/source_inventory.csv, source_coverage_matrix.csv, vendor_basis_exceptions.csv, annual_vendor_coverage.csv, annual_extraction_checks.csv, and delivery_validation.json. The supplement preserves915selected source facts (828structural/payout/event plus87fee/clock/contract) and1,512vendor long-form field observations including missing values. Report-vintage repeats are evidence from separate documents, not independent observations. Prerequisite source hash references retain links to originals in the previous snapshot.

Vendor share basis sometimes disagrees with issuer issued/net-outstanding definitions; preserve the exceptions. First-publication dates of annual facts are mostly unknown. Roche's announced/approved/completed repurchase and later cancellation/register/Gazette clocks are distinct. Novo final notices bracket a changed observed charge between March and August2021; they do not establish a general fee-regime effective day. Contractual maxima, annual disclosure snapshots and event-specific charges remain distinct.

Exact historical local quote-source venue remains unresolved. Screen-control checks explicitly showed no institutional entitlement to Datastream Equities or LSEG Global Ownership; those routes were not bypassed. Annual class/owner/payout/rights histories remain partial and must not be represented as a complete point-in-time panel. The coverage matrix names the missing fields. Use independently qualified price samples now, and admit structural features only after their definition and release-time requirements are satisfied.

## Further public-report additions

The next separate snapshot is `data/acquisition/2026-11-12/loop_public_report_additions/`. Archive `loop_public_report_additions_2026-11-12_v1.zip` is **341,618 bytes**, **48 entries**, SHA-256 **`6f5a6b67c131e69b0388d1dbfc2a6a8b7b4130e0afe45149f64031dbd9425a71`**. Its separate `.delivery.json` supplies every entry hash. All entry hashes/CRC and the four prior ZIP hashes passed verification. The user transfers the archive and JSON privately; public Git holds this receipt only. Keep all four prerequisite bundles.

Read the new README and REMOTE_AGENT_HANDOFF.md, then `prepared/report_additional_facts.csv`, `novo_report_availability_clocks.csv`, `coverage_matrix.csv`, `revision_and_source_alerts.csv`, `source_inventory.csv`, and `validation.json`. The snapshot contains616additional facts (VW257,Novo201,Hyundai158), four Novo report-availability clocks, and eight new public issuer HTML originals.59same-source/class/date/field/value transcriptions already delivered were excluded. Different report-vintage observations remain distinct evidence.59cited source files comprise51reused report originals plus8new documents; `inputs/reused_source_references.json` retains paths/hashes. The compact archive intentionally does not duplicate the earlier report PDFs.

New material includes VW class fiscal-dividend histories, Qatar voting blocks and residual ordinary holdings; Novo treasury flows with split-restated nominal units, latest issued/treasury/outstanding distinctions and class payout components; Hyundai class treasury, explicit completed retirement/issuance dates, preferred-rights snapshots and interim/final payouts. Preserve the2019VWinitial dividend proposal and later reduction as separate vintages/statuses. Older residual other shareholders are not automatically public float. Novo2013and2023comparatives use later split bases. Hyundai final DPS is separate from interim DPS, and dividend-eligible stocks are not year-end supply.

Novo2022..2025report-availability announcements preserve displayed dates/timestamps, but do not prove earliest dissemination or identical first-publication PDF bytes. Keep these availability bounds separate from unknown first-publication fields. Hyundai's file labelled2009has interior2010AnnualReportheaders while financial notes explicitly cover2009/2008; retain the alert and use the explicit observation period. The2021PDF splits a proposed-final year token; the extraction validates the nearest fiscal heading rather than inheriting interim status.

Venue, general fee-effective/holder-notice dates, complete publication vintages and some annual ownership/table transcriptions remain unresolved. This addition does not turn the evidence into a certified point-in-time estimation panel. Continue independently qualified price work under the protocol; gate structural integration on definitions and release timing in a new versioned specification. No new WRDS query, local regression, verdict edit or SSH action occurred in this additions snapshot.

No licensed rows, crosswalk records, private UI captures or credentials may enter public Git. The acquiring agent did not run regressions, alter empirical verdicts, or connect to SSH/ORC.
