# Local agent acquisition prompt for long horizon LOOP research

Copy the prompt below to the local agent after synchronizing the public repository.
Licensed exports travel separately from Git. Partial, well-documented acquisitions
are useful; an unavailable source must not block independent priorities.

```text
We are researching predictive linear models of observed LOOP class-price discounts
at 24, 60 and 120 calendar months. This is not an estimate of a required return or
valuation discount rate, a NAV model, or an executable-arbitrage claim.

Read repository AGENTS.md and applicable site instructions, then pull current main
without overwriting local work. Read:
- docs/regressions/PREDICTION_MECHANISM_TREE.json and its readable companion
- docs/regressions/LOOP_LONG_HORIZON_PROTOCOL_20261112.md
- docs/regressions/LOOP_LONG_HORIZON_RESULTS_20261112.md
- docs/regressions/WRDS_DESCRIPTOR_HANDOFF_20261111.md
- docs/regressions/WRDS_PRICES_AND_MAPPING_HANDOFF_20261112.md
- configs/loop_security_descriptor_candidates.csv
Use the existing privately held November 11/12 bundles for vendor stable keys;
do not substitute today's ticker for historical identity.

Context: the first batch built 14 class-specific samples across nine comparisons.
The basic model beat persistence in 4/11 evaluable samples at each of two/five
years. Novo was strongest across both horizons. Relative volume worsened all 11
two-year same-origin state-model comparisons. No ten-year forecast could meet
the matured-label training/evaluation requirements with the 2005-onward history.
These are exposed-history exploratory results, not prospective validation.

Your task is acquisition and source qualification, not model tuning or fitting.
Use the internet, issuer/exchange/depositary sources, and the user's existing
entitled WRDS access where available. Do not assume a computer login grants WRDS
database credentials. Do not bypass authentication, MFA, paywalls or permissions.

PRIORITY 1: Extend the exact securities backward, without repeating delivered data.
Inspect entitled daily-price and identifier-history coverage before requesting
bulk data. Target 1990-01-01 through 2004-12-31, and earlier where the exact
instruments existed and coverage is readily available. A 30-40-year history is
more useful for long-horizon evaluation than filling isolated days after 2005.
Start with Novo B/NYSE NVO, Roche voting/nonvoting, VW Xetra ordinary/preferred,
and Hyundai common/each of its three preferred classes; then HDFC local/NYSE HDB.
Do not invent older Alibaba, Ping An A, BYD A, unified Shell or Roche participation
histories. Treat predecessors and retired Shell classes as separate securities.

Export immutable raw closes, currencies, quote units, price-status flags, volume,
adjustment/return factors, supported distributions/actions, stable identifiers
and dated identifier/venue/class history. Include provider-specific daily return
and duration/trading flags where available. Retain full corporate-action records
when multiple events share a daily price. Request documented available fields;
record missing fields rather than inventing columns. Preserve SQL where supplied,
otherwise actual query forms/parameters, provider edition and retrieved coverage.
Confirm the exact local venue and exact NYSE receipt. Do not silently substitute
OTC receipts, other markets or another preferred class. Return actual coverage,
not a claim that the requested start date was available.

PRIORITY 2: Challenge Novo's promising result with measurement and cash-cost evidence.
Collect independently dated ADS-to-local ratios and changes, depositary fees and
effective dates, dividends with currency and gross/net/tax basis where supported,
local/US ex/trading/record/payment dates, and splits/identifier transitions.
Keep trading/ex dates separate from later payments. Preserve known 2007/2014/2023
split-clock differences and any issuer/provider date disagreement. Obtain official
close/auction timezone conventions and meaningful historical changes. These inputs
will test whether the apparent forecast signal is FX/close timing, dividend/fee
mechanics, or a persistent economic gap. They do not themselves prove a mechanism.

PRIORITY 3: Build dated structural feature histories linked to the tree.
Start with Novo, Roche, Hyundai and VW, using annual/interim and dated issuer
reports back to 2005 (earlier if readily accessible). Collect class-specific:
- issued, outstanding and treasury shares, keeping definitions distinct;
- actual repurchases/cancellations/issuance and their effective/report dates,
  separately from announced authorizations;
- controlling/strategic/large-owner blocks and foreign/institutional holdings
  where genuinely available; distinguish ownership stocks from trading flows;
- cash distributions, payout commitments and delivery by class;
- implemented rights, conversion/access, index-eligibility or governance changes.
Do not call issued-minus-treasury public float without documenting strategic
blocks and definitions. Do not infer class-specific shares/holdings from an
issuer-wide aggregate. Keep unavailable observations missing rather than zero.

Every extracted fact needs issuer/security/class, observation/effective date,
first public-release date (or explicitly unknown), retrieval date, value/unit,
source URL/file, page/table locator, and revision/vintage qualification. Retain
reported historical facts separately from those actually known at a past forecast
origin. A current website table is not evidence it was public in an earlier year.
No future backfill and no repeated annual values presented as daily observations.

DELIVERY AND CONTINUITY:
Use a new ignored acquisition directory such as
data/acquisition/2026-11-12/loop_long_horizon_followup/; never overwrite earlier
snapshots. Save raw sources, exact queries/form specifications, a tidy dated
evidence table, a source/coverage matrix, acquisition manifest (SHA-256 and size),
README, and an append-only work log. Preserve partial progress by priority/issuer.
State which tree branches each source can and cannot test; retain contradictory
evidence and failed routes. Do not upgrade a hypothesis because data were found.
Do not change empirical tree verdicts or run/restart regressions on the local side.

Package licensed files in a ZIP whose entries are relative to the new snapshot
directory, with no outer directory, absolute paths, traversal components or
symlinks. Supply a separate delivery JSON with ZIP SHA-256, byte size and full
entry inventory/hashes. Provide actual row counts and dates. Keep licensed rows,
crosswalks, private UI captures and credentials out of public Git. Public commits
may contain only reusable code, public-source rules and aggregate documentation.
Report the archive path and completed/blocked items; do not silently drop a
priority because one other source is unavailable. No connection to ORC is needed
for collection; the user will transfer private artifacts through an approved path.
```

Meanwhile, ORC work can proceed without another acquisition: inspect coefficient
drift by training vintage, compare fixed train-only regularization on identical
origins, verify apparent gains with nonoverlapping-period summaries, and preserve
all outcomes in the tree. New histories and structural features enter only a new
versioned specification, retaining the first batch as evidence.
