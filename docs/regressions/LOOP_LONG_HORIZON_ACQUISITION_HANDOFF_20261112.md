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

## Supplement in preparation

`data/acquisition/2026-11-12/loop_gap_closure_supplement/` is still being finalized locally and is not yet a delivered dataset. It includes a 378-row annual issue-level WRDS export, additional issuer annual reports, dated Roche corporate events and Novo final cash notices. Vendor share basis sometimes disagrees with issued/net-outstanding definitions in issuer reports; these exceptions travel with the supplement. Exact quote-source venue and a general fee-schedule effective day remain unresolved where the sources do not establish them. Use the supplement only after its separate final delivery receipt is published and its private archive is received and verified.

No licensed rows, crosswalk records, private UI captures or credentials may enter public Git. The acquiring agent did not run regressions, alter empirical verdicts, or connect to SSH/ORC.
