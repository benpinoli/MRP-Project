# Narrow acquisition request: Novo measurement and older exact-venue coverage

This request follows M01–M05/X01–X03/B02 and the analyst's next-experiment review.
Its purpose is to discriminate economic segmentation/correction from quote, FX,
share-basis and timing artifacts. It is not a request for more generic annual
ownership rows, fee notices, substitute listings or another bulk price export.
Partial, documented negative results are useful. Existing price work proceeds
independently. Use only entitled provider access or public sources; do not bypass
access controls or assume that an ORC account grants a vendor entitlement.

## A. Qualify existing 1995–2004 candidate rows

Use the previously delivered exact Copenhagen Novo B and NYSE NVO identity chain
and private stable keys. Inspect entitlement/catalog coverage before querying.
Reuse the delivered raw price and identifier files; do not export them again
unless a documented missing field actually requires it.

For 1995-01-01 through 2004-12-31 obtain evidence linked to those exact rows for:

- Historical **quote-source venue**, and its date intervals, market identifier,
  source feed/table and definition. Distinguish a specific venue's close from a
  consolidated/composite quote or today's primary listing. A present-day
  exchange code is not sufficient.
- Stable dated security/class identifiers and identity continuity. Keep the
  2000 demerger and 2001 nominal-share/receipt-basis change as separate gates;
  document what can and cannot be treated as the same economic claim.
- Historical currency and price quotation units, raw versus adjusted basis,
  vendor price-status/missing/nontransaction definitions and dated changes.
- Independently dated ordinary/local-shares-per-ADS ratios and local/US split
  trading clocks. Distinguish trading/ex, record, distribution and payment dates
  and preserve disagreements. Do not apply today's share unit backwards.

Return an interval decision table with evidence and released/held/excluded
status. Preserve exact queries/forms, provider edition and retrieval time.
If source provenance cannot be established, retain the interval as held; another
unqualified price CSV does not close the gate. Do not promise ten-year validation
from a requested start date: eligibility depends on actual qualified history,
matured labels and independent holding spans.

## B. Twenty-date synchronized-quote feasibility pilot

Before a larger intraday acquisition, request the **first five verified common
trading sessions** in each of December 2007, March 2014, November 2023 and
March 2025. Use official/provider session calendars to determine these twenty
dates; save that calendar evidence before inspecting quote values. Do not select
dates by observed discount, forecast error or quote availability. Missing quotes
on a selected date stay missing rather than replacing it with a sixth session.

For each selected date request:

1. Exact Copenhagen B official closing-auction price, currency/unit and source
   venue; auction event timestamp and first publication timestamp, with native
   timezone and documented UTC/DST conversion.
2. Exact NYSE receipt bid/ask and, if available, trade/official close metadata.
   The primary comparison uses the last eligible NYSE quote **at or before the
   Copenhagen auction event time**, with maximum age **60 seconds**. Retain
   quote/venue/condition flags, event and dissemination clocks and source edition.
3. USD-per-DKK spot bid/ask at or before that same event, maximum age **60 seconds**,
   raw quotation convention, timestamp/source and conversion method. If the
   source uses DKK per USD, preserve it and invert bid/ask correctly.
4. Dated receipt/local share basis, split/action flags, local/US ex/record/pay
   clocks and any price correction/revision identifiers for these observations.

Save raw timestamps and records; never silently substitute the later NYSE daily
close, same-date ECB reference FX, an OTC receipt or stale prices. If an entitled
source cannot supply the requested clock/venue/age, record the exact gap.
The event-time ratio is a measurement comparison, not an executable strategy:
auction publication can follow the trade event, and fees, financing and tax are
separate. Bid/ask intervals remain visible rather than being collapsed into a
claimed arbitrage profit.

Compare the pilot ratios with the existing asynchronous daily definition on
these same dates, preserving ratio orientation and scale. No regression, threshold
optimization or forecast selection is part of acquisition. Twenty observations
test feasibility and measurement magnitude; they cannot certify a multidecade
synchronized panel or establish predictive skill. Seek a larger scoped pull only
after this pilot identifies a usable source and the next specification is frozen.

## Delivery and decisions

Use a new ignored private acquisition snapshot. Include immutable raw sources,
query/form specifications, selected-date/session manifest, interval decisions,
quote-age/coverage audit, source inventory, hashes/sizes, README and append-only
work log. Every extracted fact needs observation/effective/publication-or-unknown/
retrieval clocks, source and locator, unit, class and revision qualification.
Retain source contradictions and failed routes. Keep licensed rows, private keys,
crosswalks and UI captures out of public Git.

Acceptance requires source-linked exact identity/venue/units/clock evidence,
not a convenient model result. Unknowns stay unknown. Any new admitted interval
or measurement series enters a separate versioned specification, preserving
the current baseline and its exclusions.
