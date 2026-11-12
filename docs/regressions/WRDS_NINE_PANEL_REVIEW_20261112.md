# ORC receipt and nine-comparison review — November 12, 2026

**Subsequent authorized research:** the user later authorized pragmatic cleaning
and hypothesis-guided long-horizon regressions. The [completed LOOP research batch](LOOP_LONG_HORIZON_RESULTS_20261112.md)
records the resulting exploratory fits and forecasts. The receipt-stage gates
below remain the historical review decision; they do not override that later
scoped authorization or imply that no subsequent regressions have run.

Receipt verification and the requested panel review are complete. The private
outputs define fourteen class-specific candidate samples across nine comparisons.
They approve acquisition identities within the delivered dated intervals, subject
to the explicit mapping exceptions; they do **not** approve new regressions.
No regression, FX conversion, return splice, or restart of paused work occurred.
Existing independently authorized regressions retain their existing authorization.

## Receipt and reproducibility

Current `origin/main` was fetched and merged with `--ff-only`; the checkout was
already current and retained its two local commits and the earlier untracked
`scripts/build_loop_review_panels.py`. No reset or overwrite was used.

The supplied ZIP has SHA-256
`a65bfef416b82720c6c8200a64905e6d8fbfdb08d1515d8225ee955cd681bf97`
and size 23,824,061 bytes. All 46 ZIP entries passed absolute/Windows-drive,
traversal, duplicate, inventory, symlink, size and hash checks. Entries have no
outer folder. All 46 existing extracted files matched the delivery inventory and
all 45 internal-manifest files matched their hashes and sizes. The matching
snapshot was reused without extraction. The November 11 manifest files were
also verified before and after review. Neither delivered snapshot was modified.

`audit_acquisition.py` ran from an isolated private working directory, using
links to the immutable raw input and a copy of the required prepared seed.
Its aggregate JSON is semantically identical to the delivered JSON. The twelve
other reproduced prepared files, including the copied seed, are byte-identical;
the summary JSON differs only in serialization. Original prepared files were
never regenerated in place.

Verified controls:

| Control | Result |
| --- | ---: |
| Historical identifier rows | 461 |
| Global raw / requested / excluded rows | 351,747 / 88,055 / 263,692 |
| Requested local stable keys | 17 |
| Unmatched / ambiguous local mappings | 15 / 0 |
| Duplicate local security/date keys | 0 |
| Missing local closes | 2 |
| CRSP raw / unique daily records | 23,461 / 23,458 |
| Duplicated CRSP dates / conflicting daily payloads | 3 / 0 |
| US extension candidates / exact NYSE rows | 550 / 276 |
| Overlap closes agreeing within one cent | 168 / 168 |

Exact SQL remains supplied for the three Compustat jobs. The CRSP submitted form
and returned parameters remain the provenance for that job; no SQL was invented.
The unique CRSP daily file omits distribution columns. The review preserves all
225 populated distribution rows separately, including distinct distributions
on duplicated dates; immutable raw rows and November 11 actions remain available.

Final private directory:
`data/acquisition/2026-11-12/orc_completed_review_20261112_final/`.
Its `review_manifest.json` records output hashes, reviewer/rules hashes, Python
3.12.2 and Slurm job 15292707. That job completed with exit code zero in 33
seconds, using approximately 816 MiB maximum resident memory. An initial attempt
failed on CRSP's unpunctuated `RDSA`/`RDSB` symbols; the corrected intermediate
review succeeded, then was superseded by the final review with the additional
BYD window. Earlier outputs were retained separately.

## Observation and identity decisions

All fifteen unmatched observations remain quarantined: twelve early Shell B
rows through August 4, 2005; the BYD A listing-day row on June 30, 2011; and two
Hyundai third-preferred records on December 28, 2005 and May 15, 2006. The latter
December record has no close. Do not backdate vendor identifier intervals to
absorb these observations. The first supported mapped BYD A row is July 1,
2011; its first screened common A/H date is July 4. The first positive Hyundai
third-preferred quote is May 15, 2006, but the screened mapped sample starts
May 16. The other missing local close is Ping An A on July 13, 2010.

There are 3,605 local status-5 rows. Every one repeats the preceding supplied
close and lacks volume. They are excluded from candidate trading observations.
Status-10 rows with unchanged prices are retained when they otherwise pass the
screen: an unchanged traded price alone is not evidence of staleness. There are
also four status-10 rows without volume; these are excluded conservatively.
No local row reports zero volume. The screen requires a positive finite close,
positive finite volume/unit, nonblank currency, and one dated mapping, with
`PRCSTD=10`. This is an explicit screening rule, supported by the observed
payload and a [primary research precedent](https://www.newyorkfed.org/medialibrary/media/research/conference/2022/global-research/presentations/6_Adams_Verdelhan_2022_FRBNY_Global_Research_Forum.pdf?sc_lang=en),
not a replacement for the provider's full price-status dictionary or official
exchange calendars. The delivered catalog identifies `r_prc_stat`, but its
reference rows were not supplied.

CRSP candidates require NYSE, active trading status, regular-way condition,
`DlyPrcFlg=TR`, positive close and positive volume. Price flags are checked
against [CRSP's dictionary](https://www.crsp.org/wp-content/uploads/appendix/FlagType_PC.html).
All source return and duration flags are retained; the
[duration dictionary](https://www.crsp.org/wp-content/uploads/appendix/FlagType_RD.html)
distinguishes a single trading period across weekends/holidays from a multi-period
return. A candidate level row is not automatically a one-session return.

The CRSP RDS.A series starts July 25, 2005, after the public listing date. RDS.B
has a January 31, 2022 post-trading metadata record without a close: its last
valid class-B trading date is January 28. The positive January 31 SHELWI row is
conditional, not regular-way SHEL. Pre-unification A/B and regular-way SHEL are
separate samples. Regular-way SHEL begins February 1.

Roche retains its old and new nonvoting identifiers. The issuer establishes the
last Genussschein session as March 16, 2026 and participation-certificate trading
from March 17, with a 1:1 exchange; March 18 is the record date, not the first
trading date. [Roche notice](https://www.roche.com/investors/updates/inv-update-2026-03-16).
The delivered nonvoting March 17 quote is status 5 without volume, so this
screened participation sample starts March 18. Do not manufacture a March 17
trading close or redefine the public event date.

## Gaps, adjustment direction and share bases

The private gap audit records every supplied-row gap exceeding ten calendar
days. Hyundai preferred classes 1 and 2 have gaps January 22–February 21 and
February 21–April 14, 2008; the common series has no comparable long gap. Ping
An H has a June 30–July 28, 2010 gap. Ping An A's last positive close before
its long gap is June 28 and its next is September 2, 2010; the missing-close
July 13 metadata row does not bridge that 66-day gap. Both BYD classes have a
May 22–June 4, 2015 gap. Hyundai third preferred's December 2005 metadata
record precedes its first positive quote by 138 days; that is an initial
coverage boundary, not proof of a 138-day trading suspension. No gap is filled
or assigned a suspension/holiday cause without exchange evidence. Ping An A
begins in this export on March 5, 2007, after the March 1 listing seed.

WRDS specifies adjusted close as `PRCCD / AJEXDI` and total-return index as
`(PRCCD / AJEXDI) * TRFD`. [WRDS methodology, slides 23 and 25](https://wrds-www.wharton.upenn.edu/documents/1402/Compustat_Global_in_WRDS_the_basics.pptx).
The three documented HDFC and three Novo local splits corroborate division:
the factor changes by the inverse split multiple, and division removes the
mechanical price discontinuity. Multiplication introduces a second discontinuity.
All twelve observed factor changes are saved privately. The Volkswagen 2010
preferred adjustment and BYD's 2008 H adjustment still need event-specific
interpretation before returns spanning those events are released. Ping An's
two 2015 factors change together; this observation alone does not establish
the full action's legal and dividend terms.

The November 11 verified local/US windows remain excluded, with inclusive
start and exclusive end:

- HDFC: July 14–25, 2011; September 19–26, 2019; August 26–September 8, 2025.
- Novo: December 3–17, 2007; January 2–9, 2014; September 13–20, 2023.
- Shell: January 31–February 1, 2022, with SHELWI separately retained in source.

**Additional finding:** BYD's H shares go ex on June 10, 2025, whereas its A
shares go ex on July 29. Each class triples. The H date is confirmed by
[HKEX](https://www.hkex.com.hk/News/Market-Communications/2025/250520news?sc_lang=en);
the A ex-date and new-share trading date are confirmed by
[BYD's implementation announcement](https://epaper.cs.com.cn/zgzqb/html/2025-07/22/nw.D110000zgzqb_20250722_4-B027.htm).
Exclude June 10 through July 28 from a raw-share-basis A/H premium: 34 otherwise
screened common dates. The H payment date must not replace the H ex-date.
The supplementary public rules are stored separately; neither delivered input
transition table was changed.

Preserve the dated ADS ratio evidence: Alibaba's old 1-share basis has no Hong
Kong overlap and its overlap uses the 8-share basis; HDFC uses 3, Novo 1 and
Shell 2 on matched bases. Every delivered long ratio interval explicitly has
`full_interval_certified=NO`. Event corroboration does not silently certify
the entire 2005–2026 ratio history. Novo's 2007 issuer distribution date and
CRSP payment date remain distinct evidence; the trading window uses ex/first
post-split sessions.

Shell's aggregate ADS/two-local-quote magnitude is consistent with vendor
prices being pounds: class medians are approximately 1.55, 1.55 and 1.29.
This is a diagnostic inference, not independent FX validation or certification
of every historical date. Do not divide the vendor prices by 100 just because
LSE displays GBX, or treat `QUNIT=1` as proof. Historical quote scale and dated
FX validation remain gates for the Shell parity samples.

## Provider overlap and clocks

There are 41 comparable adjacent-provider return pairs per current US receipt
in the August–September overlap: 164 comparisons. Both split-adjusted price
returns and total returns agree with CRSP within 0.0000005 in return units,
consistent with CRSP's exported rounding; none differs by one basis point.
Previous provider dates are matched explicitly. The first overlap date cannot
form a two-date Compustat return within the extract and is not counted.

This strengthens the provider consistency evidence beyond the 168 matching
closes. The 27 October–November dates per receipt remain a separate extension:
there is no CRSP flag/return coverage after September 30 and no executed splice.
The proposed receipt samples therefore end September 30. October–November
extension observations are preserved in the delivered prepared file and the
earlier nine review panels, not silently appended to CRSP returns.

Date joins here align calendar labels only. No per-date timezone-aware close
timestamps, historical session exceptions, or point-in-time FX observations
were certified. Any proposed currency conversion must specify USD per local
currency (or the corresponding CNY/HKD convention), the fixing timestamp,
publication/availability lag, and which close preceded it. European daylight
saving and New York daylight saving must be resolved by date. Same-date local
and US returns have different information windows. No synchronized parity,
intraday execution, borrow, transaction-cost, ownership or NAV claim follows.

## Exact proposed samples

These are **screened price-level candidates**, not executed regressions or
approved daily-return counts. Membership is frozen by sample/date in the private
`proposed_sample_membership.csv`, with the exact local/US keys, dated local
identifier, original fields and approval flag zero. `review_summary.json`
records each endpoint, exclusion, blocker, and 2/5/10-year count. Raw rows,
crosswalks and membership records remain ignored by Git.

| Comparison / class | First candidate | Last candidate | Candidate dates | 2 / 5 / 10-year dates |
| --- | --- | --- | ---: | --- |
| Alibaba local/ADS | 2019-11-26 | 2026-09-30 | 1,636 | 479 / 1,192 / 1,636* |
| HDFC local/ADS | 2005-01-03 | 2026-09-30 | 5,189 | 470 / 1,185 / 2,379 |
| Shell A/ADS | 2005-07-25 | 2022-01-28 | 4,086 | 496 / 1,238 / 2,474 |
| Shell B/ADS | 2005-08-05 | 2022-01-28 | 4,077 | 496 / 1,238 / 2,474 |
| Shell unified/ADS | 2022-02-01 | 2026-09-30 | 1,147 | 493 / 1,147* / 1,147* |
| Novo B/ADR | 2005-01-03 | 2026-09-30 | 5,278 | 484 / 1,212 / 2,428 |
| BYD A/H | 2011-07-04 | 2026-11-06 | 3,572 | 438 / 1,142 / 2,323 |
| Ping An A/H | 2007-03-05 | 2026-11-06 | 4,575 | 472 / 1,176 / 2,357 |
| Hyundai common/preferred 1 | 2005-01-03 | 2026-11-06 | 5,324 | 486 / 1,223 / 2,452 |
| Hyundai common/preferred 2 | 2005-01-03 | 2026-11-06 | 5,324 | 486 / 1,223 / 2,452 |
| Hyundai common/preferred 3 | 2006-05-16 | 2026-11-06 | 5,048 | 486 / 1,223 / 2,452 |
| Roche voting/Genussschein | 2005-01-03 | 2026-03-16 | 5,328 | 497 / 1,257 / 2,511 |
| Roche voting/participation | 2026-03-18 | 2026-11-06 | 163 | 163* / 163* / 163* |
| VW ordinary/preferred | 2005-01-03 | 2026-11-06 | 5,553 | 506 / 1,275 / 2,539 |

Each horizon is `(sample end minus N calendar years, sample end]`; retired
classes end on their supported historical endpoint. An asterisk means the
class lacks the full nominal horizon; it must not be described as a completed
five- or ten-year sample. Endpoints and counts do not imply continuous trading
coverage or eligibility of a return immediately following an excluded interval.

For proposed levels, use a class premium/discount within one currency, a
currency-adjusted A/H premium for the Chinese comparisons, or
`log(ADS close / (dated ratio * local close * USD-per-local FX))` for receipts.
These are descriptive price associations with class rights and market
restrictions retained. Return models require positive adjustment/return factors,
valid corporate actions, matching previous trading endpoints, approved calendars,
and separate close-alignment specifications. Do not calculate a daily return
by simply lagging the filtered membership file across a gap, split window,
provider boundary, Shell unification, or Roche conversion.

All nine comparisons retain explicit readiness gates. Same-currency Hyundai,
Roche and VW do not require FX for their class-price comparisons, but still
need calendar/status/venue-history and affected-action checks. Cross-currency
samples additionally need FX/close alignment; receipt samples need certified
dated ratios; Shell additionally needs historical scale verification. The
Global W histories contain no historical venue/ticker records, so exact current
venue evidence is not promoted to an independently observed full venue history.
No approved regression sample is released by this report.

## Run and validation

From the repository root, use a **new** private output directory:

```bash
mkdir -p data/acquisition/2026-11-12/review_logs
sbatch slurm/wrds_daily_mapping_review.sbatch \
  data/acquisition/2026-11-12/another_review_directory
```

The reviewer rejects an existing output directory and validates delivered
hashes before executing the bundled audit. Four new synthetic security/trading
gate checks and the four existing crosswalk checks passed. The batch shell
passed syntax validation. Licensed files and all generated review directories
are ignored by Git. Public changes contain code, public event rules and this
aggregate report only.
