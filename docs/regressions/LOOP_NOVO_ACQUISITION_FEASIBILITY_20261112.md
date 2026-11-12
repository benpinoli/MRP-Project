# Novo targeted acquisition: primary-source feasibility check

Reviewed November 12, 2026, for NEXT-02 in the
[active plan](LOOP_ACTIVE_RESEARCH_PLAN_20261112.md) and the
[fixed acquisition request](LOOP_NOVO_TARGETED_DATA_REQUEST_20261112.md).
This was a public documentation lookup only. No institutional entitlement,
credential, paid order, provider contact or data query was attempted. No new
price record, sample interval, regression or empirical verdict is produced.

The coordinating agent froze `configs/novo_measurement_acquisition_v1.json`:
four months times five common sessions, 60-second quote-age limits, with exact
dates pending independent official session-calendar verification. A filtered
research-membership file must not determine the selected session dates.

## Decision

**The synchronized pilot has identifiable commercial/exchange product routes,
but actual access and date/instrument coverage remain unverified.** Official
documentation describes venue-tagged US quotes, Nordic order/trade logs and
timestamped FX quote extraction. It does not yet certify that the required
twenty observations can be delivered, or resolve the original Compustat local
quote source in 1995–2004. Keep those gates held.

The fixed pilot remains the first five verified common trading sessions in
December 2007, March 2014, November 2023 and March 2025. Save calendar evidence
before inspecting quotes. Do not replace unavailable selected dates or substitute
NBBO, another listing, daily reference FX or the later US close for the specified
venue/clock observations.

## Documented routes and limits

| Needed component | Primary route with documented capability | Still needs authorized confirmation |
| --- | --- | --- |
| NYSE NVO quotes at Copenhagen close | NYSE Daily TAQ quote records with issuing exchange, SIP time, bid/offer, sizes and conditions | Entitlement; actual dated NVO identity and quote coverage; period-specific timestamp schema; last eligible NYSE-issued quote within 60 seconds |
| Copenhagen official closing cross and identity | Nasdaq Nordic HistoricalView order/trade logs; Nordic TotalView-ITCH closing-cross messages | Actual archived dates, venue/order-book mapping, raw price basis and historical format; distinct event/publication clocks; especially pre-INET 2007 |
| USD/DKK spot bid/ask within 60 seconds | LSEG Tick History Time and Sales quote extraction and UTC timestamp options | Separate Tick History entitlement; historical instrument/contributor and USD/DKK coverage; indicative versus executable quote meaning and clock precision |
| Source provenance for existing 1995–2004 local prices | Date-linked vendor/exchange evidence requested for the existing raw records | No public document found in this scoped check that maps those particular old Compustat observations to an exact historical quote venue |

### NYSE quotes: capability documented, access not established

The [NYSE Daily TAQ product page](https://www.nyse.com/data-products/catalog/daily-taq/)
describes US consolidated trades/quotes and historical coverage from 1993.
The [official client specification v4.1](https://www.nyse.com/publicdocs/nyse/data/Daily_TAQ_Client_Spec_v4.1.pdf)
documents quote-file `Time` as SIP publication time, `Exchange` as issuing
exchange, symbol, bid/offer prices and sizes, and quote condition; participant
ID `N` is NYSE. It distinguishes participant timestamps from SIP time and
documents historical timestamp/schema changes. Historical access is licensed.

Use the **individual participant quote records**, not an unexamined consolidated
NBBO substituted for a NYSE-only observation. The document's present field list
does not prove all fields exist in 2007. A date-specific master/name match and
the correct historical schema must accompany each selected quote. The clock
field used for the at-or-before rule must be explicit; publication and matching-
engine clocks are not interchangeable.

The [official WRDS TAQ description](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/nyse-trade-and-quote-taq/)
lists Daily TAQ from September 2003 and the Monthly product for 1993–2014.
This identifies a possible institutional delivery route for the pilot. It does
**not** establish BYU subscription/access, permission to use this particular
dataset, or that the account used for earlier Compustat/CRSP exports has TAQ.
No full-market daily-file download is needed to establish entitlement or request
twenty narrow instrument/time slices.

### Nordic closing cross: useful product, material historical-format gate

[Nasdaq HistoricalView](https://www.nasdaq.com/products/data/nordic-baltic/historicalview)
describes full order/trade daily files, with HistoricalView-ITCH based on Nordic
TotalView-ITCH logs. Current daily delivery is T+1; files older than the online
retention window may be requested through the provider's authorized process.
That is product-level capability, not confirmation of the first available
archive date or NVO/Novo-specific availability for our selected dates.

The [current official Nordic ITCH specification](https://www.nasdaq.com/docs/2026/10/28/Nordic-Equity-TotalView-ITCH-3.04.7.pdf)
contains closing-cross type `C`, order-book identifier, cross price, quantity,
match number and feed timestamp. Its revision history records the 2015 UTC
nanosecond-timestamp change. The fetched document body identifies revision
3.04.8 dated November 5, 2026, although the URL filename contains 3.04.7:
save the actual fetched version/hash, not the filename as the version.

These fields can identify a recorded closing-cross message; they do not by
themselves establish two separately measured auction-event and first-publication
times. Require that distinction or explicitly record its absence. Zero-size
crosses, broken trades, price scales, venue mapping and dissemination semantics
must be interpreted using the **applicable historical** specification.

Nasdaq's [dated February 8, 2010 launch notice](https://ir.nasdaq.com/news-releases/news-release-details/nasdaq-omx-launches-inet-trading-system-across-its-seven-markets)
states that Copenhagen was included in the Nordic/Baltic INET rollout. Therefore
December 2007 predates that rollout. Inferring a 2007 INET archive/schema from
today's HistoricalView-ITCH description would be invalid. Request the pre-INET
archive and format explicitly; if unavailable, retain the five selected 2007
dates as unavailable rather than moving them into a convenient modern period.

### FX ticks: documented extraction route, currency-pair coverage unverified

The [LSEG Tick History factsheet](https://www.lseg.com.cn/content/dam/data-analytics/en_us/documents/fact-sheets/lseg-tick-history-factsheet.pdf)
describes historical trade/quote messages since 1996 across asset classes,
including foreign exchange. This is a broad archive statement; it does not
prove USD/DKK, a particular contributor, the twenty timestamps or 1995 coverage.

The [provider's Time and Sales tutorial](https://developers.lseg.com/en/article-catalog/article/request-tick-history-time-and-sales-data-using-python)
documents authenticated on-demand instrument/date-range extraction and bid/ask
output. A [provider extraction example](https://developers.lseg.com/en/article-catalog/article/tick-history-request-parallel)
explicitly requests bid/ask price/size fields and sets message timestamps to
GMT/UTC. These examples identify an API/query route; no example instrument is
asserted to be the right historical USD/DKK source. Confirm available field names,
historical instrument mapping, contributor/venue semantics, correction handling
and actual coverage through an authorized catalog/query first.

Tick History is a separate product. The previously documented lack of Datastream
Equities/Global Ownership entitlement neither proves Tick History is available
nor establishes its absence. Do not reuse or infer credentials. Retain the
provider's native quotation direction and invert bid/ask correctly if needed.
An indicative contributor quote is not automatically an executable FX fill.
The maximum-age rule remains 60 seconds; a daily ECB fixing cannot satisfy it.

## Immediate authorized acquisition sequence

The coordinating agent also checked the available plugin directory. An exact
WRDS search found no matching plugin, and broader historical-quote searches
did not identify a relevant provider connector. The available Finances plugin
describes personal-account insights, not demonstrated TAQ/Nordic/FX archives.
This limits the present connected-tool route; it is **not** evidence that no
provider, institutional entitlement or future connector exists. No plugin was
installed, account connected, purchase made or outside message sent.

1. In the existing entitled environment, establish the three **specific product**
   permissions and actual archive/instrument coverage. Record unavailable access
   or dates. Public documentation is sufficient to prepare this check but is
   not entitlement evidence.
2. Ask first for a provider field/schema/coverage response and the fixed narrow
   slices, not entire-market tick files. Establish historical Copenhagen/NVO
   identities and official session dates, then obtain applicable native/UTC/DST
   and event-versus-publication definitions.
3. Preserve each original record, source edition, extraction parameters,
   condition/correction flags and received hash. Apply the existing date, venue
   and at-or-before/60-second rules without replacements or interpolation.
4. Treat 1995–2004 provenance as a **separate gate**: a newly obtained exchange
   series can support a new exact-venue specification but does not retroactively
   certify which venue supplied an old Compustat price. If the old source cannot
   be linked, keep it held and retain any alternative series as a separate source.
5. Stop the affected route on unavailable entitlement or unresolved provenance;
   retain the negative result. No purchase, outside message or provider connection
   is authorized merely by this memo. No existing qualified sample is globally
   blocked by a failed pilot component.

## What this advances scientifically

This lookup advances the acquisition request from an abstract need to specific
provider products, fields and historical-schema checks. It supplies **zero new
qualified price observations**. The next concrete evidence is an authorized
coverage/entitlement response and, where available, the fixed twenty-date
price/quote/FX slices—not another regression or a claim that the measured
terminal gap has already been explained.
