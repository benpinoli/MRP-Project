# Prompt for the local acquisition agent

Copy the prompt below into the agent running on the acquisition laptop. Public Git contains aggregate receipts, not the private ZIPs. Existing pilot and five-bundle snapshots on that laptop remain valid inputs. This request authorizes collection through existing entitled access and ordinary public sources; it does not authorize purchases, provider contacts, new paid accounts or restriction bypasses.

---

Pull current main without overwriting local work. Read AGENTS.md and applicable local/site instructions, then:

- `docs/regressions/LOOP_NOVO_MEASUREMENT_CHECKPOINT_20261112.md`
- `docs/regressions/LOOP_NOVO_ORC_STORAGE_AUDIT_20261112.md`
- `docs/regressions/LOOP_NOVO_TARGETED_DATA_REQUEST_20261112.md`
- `docs/regressions/LOOP_NOVO_ACQUISITION_FEASIBILITY_20261112.md`
- `configs/novo_measurement_acquisition_v1.json`

Continue the independent Novo measurement/provenance acquisition. Reuse the original five delivered bundles and finalized pilot snapshot; preserve every existing snapshot and result. Read its README.md, CHECKPOINT_02.md, WORK_LOG.md and prepared/checkpoint_validation.json. Do not rerun its preparation scripts over finalized outputs.

The original `novo_measurement_pilot_2026-11-12_v1.zip` is 3,792,783 bytes, 118 files, SHA-256 `6e5e2a57a99f22f1c1285152be79f0c25f8bca4a97f8ddc84e277ba6e61b6f91`. Verify any received archive and every extracted file against its separate inventory, with safe-path/duplicate/symlink checks; extract into a new ignored private directory. ORC verified this pilot, all five prior archives and installed snapshots, and all reused pilot references unchanged.

If privately transferred, the new ORC supplement is `novo_measurement_orc_supplement_2026-11-12_v1.zip`, 3,916,817 bytes, 164 files, SHA-256 `706babe8f04abc3a1c42a815dbdb0f816e9f7b65817529d15f362fe6f9bd23ab`, with separate inventory/receipts. Read its README, schema findings, route/gap decisions and exact query logs. Do not assume a public Git receipt transferred the private archive. Existing local evidence suffices to begin independent authorized collection if this additional transfer is unavailable.

ORC inspected 2,117 filenames in 75 bounded Silver Fund table directories and 80 representative Parquet schemas. No USD/DKK series was established; observed currency labels and spreads belonged to equity/fundamental tables. The documented separate upstream Barra archive was permission denied; that route stopped. This does not establish global FX absence. Do not repeat broad code searches as a substitute for finding a dataset or infer entitlement from a library, configured path or account affiliation.

Keep these twenty dates unchanged, with `prepared/calendar_selection_frozen.json` authoritative:

```
2007-12-03, 2007-12-04, 2007-12-05, 2007-12-06, 2007-12-07
2014-03-03, 2014-03-04, 2014-03-05, 2014-03-06, 2014-03-07
2023-11-01, 2023-11-02, 2023-11-03, 2023-11-06, 2023-11-07
2025-03-03, 2025-03-04, 2025-03-05, 2025-03-06, 2025-03-07
```

Preserve calendar qualifications and discrepancies. Copenhagen is UTC+1 on the selected dates; New York changes from UTC−4 on November 1–3, 2023 to UTC−5 on November 6–7. Retain historical timezone evidence and native timestamps. Session offsets or current trading hours do not establish actual auction events.

Prioritize collection as follows; proceed independently on available routes and report partial/negative results promptly.

1. **USD/DKK FX.** Inventory existing authorized local files, school-provided exports, provider catalogs and documentation. Establish exact dataset path/table or instrument identifier; provider/product/contributor; actual historical coverage; schema and units; native direction; bid/ask versus midpoint/fixing; timestamp precision; event/publication semantics; timezone/DST; quote conditions/corrections; and license/source edition. Save exact queries and responses, including denials. LSEG Tick History remains unverified: check only a legitimate existing entitled interface if available. Public product documentation is not access evidence.

   Reuse the delivered Dukascopy raw March 3, 2025 16 UTC hour. It decompresses structurally but lacks a validated decoder, scale, direction and clock. Qualify it using provider documentation and an independently checkable native export, preserving original bytes and distinguishing third-party decoding assumptions. If an ordinary public export works, acquire only the fixed-date native bid/ask slices. Do not repeat stopped 503/timeout routes in a retry loop or work around restrictions. A failed delivery does not prove historical absence.

   If usable intraday FX exists, retain source-native observations for all available fixed dates and document gaps without replacement dates. Preserve sufficient native history to identify the last eligible quote before each actual auction once that clock is known; freeze the narrow acquisition window from documented clock evidence rather than observed values. Eligibility requires the last eligible observation at or before the auction event, maximum age 60 seconds. Until both event and quote clocks are established, keep ages and eligibility unknown. Preserve raw DKK per USD if supplied; converting to USD per DKK requires bid=1/raw ask and ask=1/raw bid, with valid positive quotes. Daily FX can be retained only as an explicitly labeled asynchronous comparator.

2. **Copenhagen closing auctions.** Through an already authorized archive or public exact-event source, establish the historical exact Novo B instrument/order-book/venue mapping, official closing-cross price, currency/scale, native event and first-publication timestamps, historical format, condition/correction/broken-trade identifiers and archive edition on those same dates. December 2007 predates the 2010 INET rollout and needs pre-INET records. The 2014 format also cannot be inferred from post-2015 UTC nanosecond schemas. Retain any missing distinction between event and dissemination clocks. Nasdaq historical archive access remains unverified, not demonstrated denied.

3. **Exact NYSE receipt quotes.** BYU WRDS Daily (`taqm_common`) and Monthly (`taq_common`) forms explicitly say Not Subscribed; do not submit or keep retrying those routes. An alternative already entitled source may be checked, but no purchase/new account is authorized. Obtain dated exact NVO identity/master evidence, NYSE-issued participant bid/ask and sizes, native event/SIP/publication clocks as available in each historical format, conditions/corrections and source edition. Do not substitute NBBO, an OTC/predecessor listing, today's primary exchange code or the later US close. Do not synthesize participant timestamps absent in 2007/2014. Apply the same at-or-before/60-second rule only once clocks and eligibility conditions are established.

4. **Separate basis/provenance gates.** Qualify existing 1995–2004 rows rather than reexporting unneeded prices. Seek date-linked source feed/table/venue, stable historical identity, raw/adjusted price basis, currency/unit/status definitions and independently dated ordinary-shares-per-ADS history. Keep all unresolved intervals held; current listing codes do not prove historical provenance. Preserve the 2000 demerger and 2001 basis transition as separate gates. All December 2007 pilot dates lie between local December 3 and ADR December 17 split trading dates and inside the announced depositary issuance/cancellation suspension through December 19 close. Candidate factor two is unit alignment, not verified legal conversion. Preserve issuer December 20 distribution versus vendor December 14 pay-date as a disagreement. Keep document, effective/ex, record, distribution/pay, first-publication-or-unknown and retrieval clocks distinct.

Save additions in a **new ignored versioned private supplement**, with immutable raw sources, publication dates or explicit unknowns, exact queries/forms and failure responses, dated source inventory, frozen date manifest, full coverage/quote-age audit retaining all sixty primary slots, interval decisions, README and append-only work log. Include a separate full per-file inventory and SHA-256 ZIP receipt; verify the resulting archive and every entry. Link reused originals by path/hash without modifying them. Keep licensed rows, stable identifiers/crosswalks, credentials and private UI captures out of public Git.

Report FX schema/access/coverage results early, then deliver all available evidence with precise remaining gaps. Zero qualified observations remains a valid outcome when documented. Do not run regressions, search new models, optimize thresholds, change empirical hypothesis verdicts, purchase data, contact providers, bypass restrictions, collect generic annual reports, or replace missing selected observations.
