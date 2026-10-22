# WRDS field definitions supplied by the user

Source: user-pasted vendor field documentation in this chat on 2026-10-22.
Vendor page URL, publication/version date and export retrieval date were not
provided. This is supplied documentation, not a page independently fetched by
the agent. It supersedes research-paper inference for the meanings below.

## PRCSTD

Daily scalar code describing the form in which prices are available. Reference
items PRCSTDCD and PRCSTDDESC hold the code/description list.

| Code | Vendor meaning |
|---|---|
| 3 | High, Low and Close |
| 4 | Bid, Ask, Average/Last Volume Close |
| 5 | No prices available; last actual price carried forward |
| 10 | Prices as reported |

The supplied documentation says volume can produce status 10 even when price
is unchanged, and price changes can produce status 10 without volume. Thus
unchanged price is not automatically stale, and missing volume does not by
itself invalidate a reported price. The current Samsung specification accepts
only code 10 for these local issues and excludes 5; codes 3/4 are documented
but not silently admitted to this pair's sample.

The historical bid/ask-to-last-close note concerns US/Canadian issues and is not
applied to Samsung's Korean listings. Code 5 alone does not distinguish a
holiday, suspension, or vendor missingness.

## CSHTRD

Daily actual number of shares traded. For non-US securities, coverage is each
individual exchange at issue level. US volume is composite across exchanges.
The documentation notes missing periods and nontrading observations; it does
not imply that every blank volume must be treated as zero or override PRCSTD.
No volume-derived liquidity statistic is being estimated in this rerun.

## QUNIT

Daily quotation block size. Per-share price is PRCCD/QUNIT; QUNIT=1 is already
per share. Missing, nonfinite, nonpositive or unsupported block sizes need
review. This Samsung specification verifies QUNIT=1 on every selected row;
other block sizes are flagged rather than silently mixed.

## AJEXDI

The supplied description identifies a daily issue-level cumulative adjustment
factor by ex-date, in ratio units, and refers to the company-level adjustment
factor definition. It does not supply that underlying definition or a complete
calculation rule. **The adjustment formula remains unresolved.** Existing
factor values and event changes may be inventoried, but adjusted prices,
adjusted returns and indexed-price panels are deferred. Earlier run panels
remain archived under their original assumptions and are superseded for use.
