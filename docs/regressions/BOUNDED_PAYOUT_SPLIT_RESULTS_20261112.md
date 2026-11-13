# Two bounded studies: payout delivery and the 2007 Novo unit mismatch

Completed November 12, 2026 under the [fixed descriptive protocol](BOUNDED_PAYOUT_SPLIT_PROTOCOL_20261112.md). These studies check delivered cash and measurement arithmetic. They do not estimate a price effect, establish a causal mechanism or change any canonical hypothesis verdict. No regressions, model search or new forecast was run.

## 1. Samsung: reported dividends are consistent with the specific cash commitments

We reviewed seven identified pages from the already acquired FY2015–FY2021 business reports, transcribed six fiscal-year outcomes, and checked ten later-report comparisons. The source PDF hashes match their existing acquisition receipts. No generic annual report was newly collected. Native amounts and later restatements remain separate in the private evidence.

| Fiscal year | Reported total cash dividend, KRW trillion | Common annual DPS, KRW per post-split-equivalent share | Preferred annual DPS, same basis |
| --- | ---: | ---: | ---: |
| 2015 | 3.068737 | 420 | 421 |
| 2016 | 3.991892 | 570 | 571 |
| 2017 | 5.826302 | 850 | 851 |
| 2018 | 9.619243 | 1,416 | 1,417 |
| 2019 | 9.619243 | 1,416 | 1,417 |
| 2020 | 20.338075 | 2,994 | 2,995 |

Pre-2018 DPS is divided by the documented 50-for-1 split **only for comparison**. Original native figures are retained. Totals are fiscal-year reported allocations, not amounts paid on December 31 or a payment-date series. FY2020 includes a special dividend; its own report still required AGM approval. The later FY2021 report confirms that the regular and special amounts were paid, without supplying account-level receipt evidence here.

**The important commitment checks:**

- The November 2016 enhancement announced approximately KRW4 trillion of FY2016 dividends and common DPS of KRW28,500 on the old share basis. Reported delivery is KRW3.991892 trillion and exactly that native DPS. The small aggregate difference reflects comparison with a rounded announcement, not an established breach. [Dated enhancement](https://news.samsung.com/global/samsung-electronics-announces-comprehensive-roadmap-to-enhance-long-term-shareholder-value-creation).
- The October 2017 policy's FY2018 doubling must use the **announcement-time** FY2017 base. The January 2018 clarification explains that the initially announced FY2017 amount was KRW4.8 trillion, subsequently increased to about KRW5.8 trillion, while the FY2018–FY2020 annual commitment remained about KRW9.6 trillion. Therefore FY2018's approximately **65.1%** increase over the final FY2017 total is not evidence that the original doubling commitment failed. [Policy](https://www.samsung.com/global/ir/reports-disclosures/public-disclosure-view.70985/), [clarification](https://news.samsung.com/global/samsung-electronics-announces-stock-split-and-shareholder-return).
- FY2018 and FY2019 reported totals are identical. The FY2021 report says annual regular dividends for FY2018–FY2020 were about KRW9.6 trillion and a roughly KRW10.7 trillion special dividend accompanied the FY2020 year-end regular payment. Thus FY2020's KRW20.338075 trillion total must not be treated as a new regular annual commitment. The rounded components are not used to invent an exact special-dividend aggregate.

Across FY2015–FY2017, reported dividends sum to **KRW12.886931 trillion**. Across FY2018–FY2020, totals including the special dividend sum to **KRW39.576561 trillion**. Preferred annual cash exceeds common by **KRW1 per post-split-equivalent share** in every selected year. Higher preferred dividend yield therefore does not by itself show a large preferred-specific increase in cash rights; a lower preferred price also raises its yield.

**What remains untested:** the policy's 30–50%/50% free-cash-flow allocation cannot be independently certified from dividends alone. Policy-defined FCF, repurchase cash and cancellation accounting have not been reconciled; the reported net-income payout ratio is not the FCF ratio. Credibility, investor clientele and any causal effect on the class-price discount remain untested. P05 gains a completed cash-delivery audit, not a supported causal verdict. The [2015 commitment](https://news.samsung.com/global/samsung-electronics-announces-shareholder-return-plan) remains distinct from its later enhancements.

**Report-page evidence:** FY2015 p21; FY2016 p21; FY2017 p28; FY2018 p25; FY2019 p24; FY2020 p24; FY2021 p224 (PDF pages, one-based). Original publication timestamps remain unknown. Page-specific layout text was independently extracted and manually reviewed; no raster visual verification is claimed. Direct downloads of four targeted policy pages returned 403; normal public web-reader inspection supplied explicitly paraphrased policy facts, not newly downloaded original HTML.

## 2. Novo: the split-unit mismatch can dominate the apparent daily gap

The five frozen dates **December 3–7, 2007** fall after the local B share started post-split trading on December 3 and before the ADR started post-split trading on December 17. They also lie inside the announced depositary issuance/cancellation suspension, after November 29 close through December 19 close. A candidate scale of two post-split local units per pre-split ADR follows those separate trading clocks; it was not selected from the observed gap. [Retained notice evidence](LOOP_NOVO_LOCAL_COLLECTION_CHECKPOINT_20261112.md), [issuer formal notice](https://www.sec.gov/Archives/edgar/data/353278/000120864607000555/c97594.txt).

We reused the **ten existing daily price records** and ten corresponding USD/EUR and DKK/EUR ECB reference observations. No extra date or event window was added. Let L be raw local DKK close, A raw ADR USD close, and F the daily reference USD-per-DKK cross. The explicitly asynchronous comparator is `A / (k × L × F)`.

| Candidate local units per raw ADR, k | ADR/local-value ratio across the five dates | Discount, 100 × (1 − ratio) |
| --- | ---: | ---: |
| 1, without candidate unit alignment | 1.9933–2.0345 | −103.455 to −99.333 percentage points |
| 2, motivated by the split trading clocks | 0.9967–1.0173 | −1.727 to +0.333 percentage points |

The unit assumption halves the ratio. An apparent roughly two-to-one price relation can consequently become a relation near one. This is a **material measurement effect**, not evidence that the remaining gap is fair value, an arbitrage profit or caused by the conversion suspension. This raw-comparator exercise does not establish that the original forecasting panel used the wrong unit or explain its predictive results.

The local quote venue/feed and exact vendor raw/adjustment semantics remain unqualified. ECB observations are current-vintage daily references; the local and later US closes are asynchronous. No common auction time, bid/ask interval, quote age, cash entitlement, executable conversion ratio or investor return is established. No original price series was rebased, no quote admitted to the synchronized pilot and no forecast result recomputed.

The chronology preserves the issuer's December 20 ADR distribution date and the vendor's December 14 payment-date field as a disagreement. Document dates, displayed archive publication times, record dates, trading dates and announced operational boundaries remain distinct. The current retrospective issuer table cannot override the separate dated trading clocks. Because all five dates share both the split mismatch and suspension, this case cannot isolate a causal suspension effect.

**What remains untested:** X03's causal depositary-friction mechanism and M05's auction/execution mechanism. All twenty frozen dates, sixty missing primary slots, unknown ages/eligibility, five pre-2005 holds, 1997 caution and separate 2000/2001 gates are preserved. WRDS denials and unverified Nasdaq/LSEG access are unchanged. No stopped provider route was retried.

## Evidence and checks

New ignored snapshot: `data/acquisition/2026-11-12/bounded_payout_split_studies_v1/`. It contains native and normalized dividend tables, ten source-vintage checks, commitment decisions, a nine-entry Novo source-clock chronology, original daily rows/flags and daily FX references, comparator arithmetic, explicit gap decisions, source hashes, exact queries, code, protocol, README and work log. Licensed rows and identifiers remain private; the tables above are aggregate/source-derived findings.

Independent checks rehashed the identified Samsung PDFs, reconciled share-basis arithmetic, preserved the ten original Novo rows, recomputed currency conversion through an independent EUR-cross calculation, and asserted the unchanged calendar hash and sixty missing slots. Original sources and results were preserved. The separate ZIP receipt records delivery integrity; these arithmetic checks do not create another economic sample or validate a causal explanation.

Private archive `bounded_payout_split_studies_2026-11-12_v1.zip`: **53,702 bytes; 37 files**; SHA-256 `3b2f8c9d5ea46b50d580b3258b45aeb60cded52b004b7c4091b363f069807e2e`. Separate inventory SHA-256 `bd67e3dcb08491fef509bb476f4436e4d4de658ab4f747e39039dff92bd43727`, delivery JSON and SHA-256 sidecars are under the same ignored acquisition parent. All archive entry sizes/hashes and CRC passed.
