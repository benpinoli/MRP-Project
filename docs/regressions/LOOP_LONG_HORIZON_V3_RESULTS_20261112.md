# LOOP-LH3 verified deliveries, gated evidence and fixed training memory

Both newly transferred private archives are verified and integrated into a new
evidence specification. Exact historical local quote provenance remains
unresolved, so no pre-2005 paired interval has been released. Independent work
on the existing price samples continued: a fixed training-memory sensitivity
does not establish a universal correction model. All LH1/LH2 and earlier
scoped results remain preserved.

## Synchronization and private receipt

Fetched main and fast-forwarded to `6fd695d` without overwriting the uncommitted
v2 work. Local main points at that commit. New work is on
`data/loop-long-horizon-v3-20261112`. The repository AGENTS.md, current ORC
instruction symlink and applicable development, storage, security, software,
Python, Slurm and performance instructions were read. Sustained I/O and
computation ran in Slurm; no paused research job was restarted.

The user supplied both new archives and separate delivery JSONs under
`data/acquisition/2026-11-12_v1/`. Receipt job `15308123` verified published
byte sizes and SHA-256, exact entry inventories, every entry hash and CRC,
path/type/symlink safety, and every internal inventory file. Extraction created
separate canonical private snapshots without overlaying earlier deliveries.

| Snapshot | ZIP bytes | ZIP entries | Internal files | SHA-256 |
| --- | ---: | ---: | ---: | --- |
| Long-history follow-up v1 | 648,953,971 | 273 | 272 | `35a754dd094f50d611c0c95f4a5077a3aa45b43bb3917b9f3c84b950e8f8ae0a` |
| Gap-closure supplement v1 | 267,222,781 | 138 | 137 | `a7ad04c4143bf5a7c4b99fe712daedd45d604eead99f5ea817e07a6e5809a5dc` |

The earlier descriptor and daily/mapping ZIPs, delivery JSONs and snapshot
inventories were reverified too. The new missing-file condition recorded in v2
is now resolved; v2's report remains a historical receipt record. Private receipt:
`runs/loop_long_horizon/v3_receipt_15308123/receipt_verification.json`.

Read both READMEs, `REMOTE_AGENT_HANDOFF.md` files, coverage audits/matrices,
source inventories, identifier and duplicate-date audits, prerequisite hash
references, annual join/coverage/extraction checks and vendor-basis exceptions.
Source checking reproduced 13 daily coverage rows from 56,634 raw Global rows
and 6,843 CRSP rows. It verified 117 prerequisite-reference records, retaining
repeated references rather than calling them distinct sources. The two new
inventories contain 113 and 55 source-attempt records; failed downloads,
extraction failures, mirror qualifications and derived web summaries remain
explicit. Original PDFs remain authoritative where extracted layout is uncertain.

## Interval and feature admission

**No new paired price interval was admitted.** Exact historical local source
venue is not supplied by current exchange attributes, dated ISIN alone, or
issuer listing dates. The private `source_review/interval_decisions.csv` records
all 13 decisions and original coverage qualifications.

| Candidate | Decision retained |
| --- | --- |
| Novo local/NYSE | Local historical quote venue and early identity/ratio continuity remain gated; pre-1989 predecessor and 2000 demerger are separate review intervals. Keep Nasdaq receipt rows separate from NYSE. |
| Roche voting/nonvoting | Early dated-ID gaps and local quote provenance remain gated; no participation prehistory is invented. |
| VW ordinary/preferred | Pre-November 28, 1997 is excluded from Xetra; post-launch quote provenance remains unverified. Preserve DEM/EUR regimes and quote units. |
| Hyundai common/preferred 1/2 | Longer positive-price candidates remain gated by venue, identity, status and unit checks. |
| Hyundai preferred 3 | No positive pre-2005 price; exclude the placeholder from samples. |
| HDFC local/NYSE | Local venue remains gated. Preserve July 20, 2001 first price versus July 23 metadata beginning; no validity date is invented. |

Transaction closes, bid/ask observations, missing/status flags and all action
rows remain distinct. Local/US split clocks, historical identifiers, quote
scale, receipt ratios and corporate transitions remain binding. No adjusted or
provider-spliced return series was formed. An older requested start cannot
establish actual 24/60/120-month eligibility.

Supplement integration is governed by
[`configs/loop_long_horizon_v3.json`](../../configs/loop_long_horizon_v3.json)
and the [registered v3 protocol](LOOP_LONG_HORIZON_V3_PROTOCOL_20261112.md).
The private evidence registry preserves all 1,375 selected facts: 460 follow-up
facts plus 775 annual structural, 53 additional structural/payout/event and
87 fee/clock/contract facts. Original fact IDs are namespaced by snapshot/table;
all original values, dates, units, source references, report vintages and
qualifications survive. Original snapshot-relative and repository-relative
citation paths remain intact, with a separate resolved-source path for checks.

First-publication dates are unknown for **1,371/1,375 facts**, including all
775 annual structural facts and all 87 fee/clock/contract facts. Four facts
have explicit publication dates, but remain dated evidence rather than new
predictors in this price-only specification. **Zero structural forecast features
were admitted.** Source document, report, authorization, observation, retrieval,
implementation and first-publication dates were not substituted for one another.
No annual forward/backward fill, missing-to-zero conversion or repeated-vintage
collapse was performed.

All 378 annual supply rows uniquely match the 402-row descriptor export on
security/date/format/fiscal-month keys; 24 descriptor-only rows remain in raw.
The 1,512 long-form vendor observations reproduce raw values and descriptor
currency/adjustment context, including **502 missing values**. All four delivered
vendor-basis exceptions remain: CSHOI is not assumed uniformly net outstanding,
aggregate treasury is not allocated to classes, and issued-minus-treasury is
not relabeled public float. Currency context does not certify ICAPI/PV units.

All six final JPM cash notices reconcile gross less stated tax/charges to net
within the delivered tolerance. These are final announcements, not independent
investor settlement confirmation. March/August 2021 observed charges bound a
change between payments; they do not establish a general fee-effective day.
Contractual maxima, annual fee disclosures, preliminary notices and final event
charges remain separate, and embedded FX fees are not deducted twice.
Roche's conditional announcement, approval, completed repurchase, cancellation,
register and Gazette clocks remain distinct; missing originals stay missing.
These checks establish integrity, coverage and arithmetic, not blanket
certification of every transcription against original PDF table layout.

## Existing-sample price check

Main job `15308280` completed the frozen fixed-memory check in
`runs/loop_long_horizon/v3_15308280/`. Training origins must be within the previous
120 calendar months and have outcomes matured by the completed feature month.
OLS and fixed lambda=1 ridge use the same original features, monthly calendar,
coverage variants and target horizons. Training scaling is fit only on rolling
training rows; the intercept is unpenalized. No window or penalty was tuned.

Of 13,695 original candidate origins, 13,687 meet the rolling minimum, producing
27,374 rolling forecasts across two methods. Eight strict Ping An five-year
activity origins have 39 usable rows against the required 40 and remain in
`failed_origins.csv`. Expanding-window comparisons are restricted to exactly
the successful rolling origins; baseline tables are untouched. All nonempty
nonoverlap phases, fixed calendar-period summaries and common-origin nested
comparisons are retained privately. Original blocked model rows are copied too.

Separate verification job `15308326` reconstructed all 27,374 rolling forecasts
using calendar-date masks and independent least-squares/augmented ridge fits;
maximum prediction discrepancy is 9.06e-14 percentage points. It checked all
21,184 overall/phase/calendar score rows and 348 nested comparisons, accounted
for every candidate origin, and confirmed all 1,375 evidence rows preserve their
original fields without feature admission. Baseline/v2 outputs and original
source inputs remain hash-identical. The receipt is
`runs/loop_long_horizon/v3_15308280/verification/AUDIT.json`.
Synthetic checks covered rolling-calendar boundaries, missing values,
publication-date gates, safe extraction, symlink rejection and refusal to
overwrite a differing existing snapshot. No independent-agent review is claimed.

Earlier source-check job `15308230` stopped before estimation because it initially
resolved all fact citations relative to the repository. The follow-up instead
uses snapshot-relative source paths. The corrected verifier handles the two
documented namespaces explicitly; the failed directory remains preserved.

Public aggregate [scorecard](LOOP_LONG_HORIZON_V3_SCORECARD_20261112.csv):

| LH-LEVEL horizon | Expanding OLS wins | Rolling OLS wins | Expanding ridge wins | Rolling ridge wins |
| --- | ---: | ---: | ---: | ---: |
| 24 months, pragmatic | 4/11 | 3/11 | 6/11 | 5/11 |
| 24 months, strict | 4/11 | 3/11 | 6/11 | 5/11 |
| 60 months, pragmatic | 4/11 | 4/11 | 3/11 | 4/11 |
| 60 months, strict | 4/11 | 4/11 | 3/11 | 5/11 |

Here a win means lower mean squared error than zero-change persistence on
matched origins, not statistical or prospective validation. The rolling state
ridge model beats persistence in 7/11 five-year samples under both coverage
rules; it remains a sensitivity, not a selected deployment model. More favorable
counts in one cell do not support universal correction or a causal mechanism.

Novo remains positive under all four method/window combinations at two and five
years. Pragmatic LH-LEVEL rolling OLS R-squared is 0.396 at 24 months and 0.136
at 60; rolling ridge gives 0.283 and 0.126. Both are below their expanding
counterparts. Two-year rolling ridge nonoverlap phases remain positive under
both coverage rules, but contain only 5–8 forecasts per phase. Five-year phases
contain only 1–2 outcomes and show both gains and losses. Shared data across
phases and nearly zero persistence losses prohibit treating phase counts as
independent validation or reading extreme phase R-squared as precise evidence.

VW remains a counterexample: pragmatic rolling LH-LEVEL R-squared is -7.416
(OLS) / -1.609 (ridge) at two years and -0.097 / -2.401 at five years. No valid
unusual period was dropped to improve these outcomes. Rolling OLS activity
improves only 1/11 two-year state comparisons under either coverage rule; ridge
activity improves 4/11 pragmatic and 5/11 strict comparisons. These specification
sensitivities preserve the original OLS negative activity finding within its scope.

No ten-year forecast is validated. The baseline has insufficient matured-label
evaluation history, and a 120-month training-origin window can furnish at most
one matured ten-year label before missingness. This particular sensitivity
therefore cannot evaluate that horizon even with additional older prices; it
does not show that longer independently qualified histories could never support
an expanding-window ten-year evaluation.

## Evidence and next gates

B01/B02 retain mixed, method/window-dependent retrospective findings. Novo
remains a candidate for ratio/clock, cash-cost and prospective challenges; VW
remains an adverse stability case. L01 remains an activity-proxy design test,
not a liquidity mechanism verdict. M01/M02 retain explicit interval gates.
Supply, ownership, control and payout branches now have a larger cited evidence
registry, with publication, class and denominator limits still binding.

The next backward-sample gate is dated exact local quote-source venue plus the
remaining identity/unit/status/split/transition checks. The next structural
feature gate is definition reconciliation and independently evidenced publication
availability at each forecast origin. Lack of entitlement to the inspected
Datastream/LSEG routes is preserved; no restriction was bypassed. Receipt and
partial annual coverage do not upgrade a hypothesis verdict. Licensed source
files, facts, crosswalks, monthly panels and individual forecasts remain ignored
by Git; public changes contain reusable code and aggregate documentation only.
