# Novo measurement acquisition checkpoint — November 12, 2026

Implements the acquisition order in `LOOP_NOVO_TARGETED_DATA_REQUEST_20261112.md`, `LOOP_NOVO_ACQUISITION_FEASIBILITY_20261112.md` and `configs/novo_measurement_acquisition_v1.json` from commit 151d701. This is partial measurement evidence, not a completed synchronized pilot. No regressions, model searches or empirical verdict changes. Original snapshots and five delivered bundles remain unchanged.

## Private delivery

Transfer these files from `data/acquisition/2026-11-12/` on the acquisition laptop:

- `novo_measurement_pilot_2026-11-12_v1.zip` — 3,792,783 bytes, 118 entries.
- `novo_measurement_pilot_2026-11-12_v1.inventory.json` — separate full per-file SHA-256 inventory.
- `novo_measurement_pilot_2026-11-12_v1.sha256` and `.delivery.json` — archive receipts.

Archive SHA-256: `6e5e2a57a99f22f1c1285152be79f0c25f8bca4a97f8ddc84e277ba6e61b6f91`.

Extracts to `novo_measurement_pilot_v1/`. Read `README.md`, `CHECKPOINT_02.md`, `WORK_LOG.md` and `prepared/checkpoint_validation.json` first. Keep all acquisition files private and ignored. Reused files are referenced by path/hash in `inputs/`; this supplement requires the original five bundles (or their existing combined transfer). The archive and every archived entry were verified after writing; reused references were independently rehashed. Do not regenerate the old bundles.

## Findings and limits

1. Calendar selection completed and frozen before quote values: December 3–7, 2007; March 3–7, 2014; November 1–3 and 6–7, 2023; March 3–7, 2025. Provider exchange calendars and official corroboration are saved with known discrepancies. Historic original Copenhagen 2007/2023 exchange calendars were not recovered; provider verification is explicitly qualified. No auction clocks inferred from today's hours. Historical DST retained, including New York's November 2023 change.
2. Actual BYU WRDS exact consolidated quote forms explicitly show **Not Subscribed** for Daily (`taqm_common`) and Monthly (`taq_common`) after maintenance recovery. Both submissions disabled; no query submitted. Nasdaq historical archive and LSEG Tick History entitlement/coverage remain **unverified**, not demonstrated denied. Public product descriptions are not entitlement proof. December 2007 needs pre-INET records; period-appropriate quote schemas remain necessary.
3. Zero qualified synchronized observations. All sixty component slots (twenty dates × three components) remain present, with missing observations and unknown quote ages. A nonempty public USD/DKK raw hour was retained but lacks validated decoder/scale and auction alignment. Repeated service failures stopped the wider route; a normal public export UI attempt did not deliver a CSV. No daily fixing, later US close, alternate receipt or replacement date admitted.
4. Forty original daily comparator records reused with hashes/record locators, explicitly labeled asynchronous. New dated split evidence identifies all December 2007 pilot dates as between local/ADR split dates and inside a depositary conversion suspension. Candidate unit alignment is separate from legal delivery/conversion. Source conflicts and unknown publication clocks remain explicit.
5. All pre-2005 provenance intervals remain held pending exact historical quote-source venue/feed, identity, units and receipt basis. The 2000 demerger and 2001 basis transition remain separate gates. Current listing codes do not resolve historical provenance.

## Prompt for the supercomputer agent

> Pull current main while preserving local work. Read AGENTS.md and applicable site instructions, then this checkpoint, the two focused Novo request documents and frozen config. Verify the separately transferred ZIP against its SHA-256 and full inventory; extract privately to a new ignored directory and reuse the original five acquisition bundles. Read its README, CHECKPOINT_02 and validation receipt. Preserve the twenty dates in prepared/calendar_selection_frozen.json and all existing snapshots/results. Do not run regressions, search models, change empirical verdicts or replace missing pilot observations.
>
> The user recalls FX in Silver Fund src/research or school-backed storage but is unsure of the path. Local/current sf-quant code inspection found no FX loader/table, which does not establish storage absence. Inventory authorized local/shared FX datasets and documentation: exact path/table, provider/product/contributor, USD/DKK direction, bid/ask versus midpoint/fixing, native event/publication clocks and timezone/DST, frequency, historical coverage, conditions/corrections and license. Do not print credentials or infer access from library installation. If suitable intraday FX exists, retain source rows for the fixed twenty dates with full provenance; do not assert <=60-second eligibility until actual Copenhagen auction events exist. If only daily FX exists, label it a daily comparator and leave primary pilot slots missing. Report schema and coverage evidence promptly. No purchase, restriction bypass or new acquisition through an unauthorized service.
>
> Respect the observed WRDS Daily/Monthly TAQ denial and unresolved Nasdaq/LSEG access. Continue independent dated basis/provenance evidence where authorized; preserve the separate 2000/2001 gates and December 2007 asynchronous split/conversion constraint. Save additions in a new versioned private supplement with source evidence, exact queries, coverage/quote-age audits, inventory and SHA-256. Public Git receives aggregate handoff notes only, never licensed rows or crosswalks.
