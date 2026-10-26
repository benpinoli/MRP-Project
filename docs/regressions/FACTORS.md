# Factor and mechanism dictionary

All signs refer to widening of `(1-P/C)`, unless stated otherwise. Ambiguous signs are intentional competing hypotheses. H IDs refer to the [existing hypothesis tree](../HYPOTHESES.md). Optional fields supplied to the engine must already be constructed in these units on the session grid with metadata. It applies the one-session lag itself. Do not pre-lag fields.

| Block / fields | Definition before engine lag | Intuition / expected association | Data needed |
|---|---|---|---|
| Barra core `F_*` (H7) | Vendor daily pure factor return, converted percent→decimal only when metadata declares percent; sum endpoints per Korean interval | Shared style/industry shocks can affect classes differently; no universal sign | Verified model ID, currency, history, timing and vintage |
| Activity `log_volume_ratio` (H3) | log(preferred shares traded/common shares traded), both strictly positive; zero/missing→missing | More preferred activity may accompany narrowing; reverse causality plausible | Already in EP01; not turnover or execution cost |
| Liquidity `spread_diff` (H3) | `(askP-bidP)/midP - (askC-bidC)/midC`, decimal, synchronized valid bid/ask | Worse preferred costs → wider discount (+) | Class quotes and timestamps |
| Liquidity `log_turnover_ratio` (H3) | log[(volP/floatP)/(volC/floatC)], positive values; dated beginning float shares | Relative preferred trading capacity may narrow discount (-) | Class free float and compatible volumes |
| Liquidity extension `amihud_diff` (H3) | 20 consecutive session mean of `abs(verified adjusted return)/(KRW traded value/1e9)` for P minus C, positive traded value, full window | Larger preferred price impact → widening (+); price changes endogenous | Verified returns, traded value; exclude split artifacts |
| Retail `retail_weight_diff` (H4) | Preferred minus common individual-investor share of traded shares, decimal; consistent one-/two-sided counting and venue | Retail clientele/noise risk can sustain divergence; sign tested | Retail and total trading per class |
| Flow `foreign_flow_diff` (H4) | Preferred minus common net foreign KRW buying / previous-session free-float market cap for respective class | Relative preferred demand → narrowing (-) | Class flows and float; not changes in ownership alone |
| Constraint `common_borrow_fee` (H5) | Observed annualized decimal fee on common, fixed documented vendor concept; missing inventory/fee not zero | Costly short common can sustain positive discount (+) | Lending fee and availability by class |
| Supply `buyback_diff` (H6) | Trailing 20-session executed P repurchases / P outstanding at window start minus C equivalent | Relative preferred support may narrow (-), float loss may widen | Executions, counts; authorizations/cancellations separate |
| Rights `incremental_dividend` (H2) | Latest publicly announced next comparable-share preferred-minus-common cash entitlement / contemporaneous preannouncement common price, decimal; do not backfill announcements | Relative preferred cash flows → narrowing (-); yields partly mechanical | Rights, dividend announcements, ex-dates and actions |
| Ownership `control_contestability` (H1) | Paper-specific minority control-power measure or separately named concentration proxy; do not substitute one for the other | More pivotal common votes → widening (+); better governance may offset | Dated blocks, affiliates and voting agreements |
| Macro extension (H7) | KRW FX, Korean rate changes, stress and chip-cycle shocks with actual availability dates | FX/export and duration shocks may transmit differently by clientele | Verified macro publications; avoid redundant market/style proxies |
| Cross-pair extension (H7) | Leave-Samsung-out preferred-discount change factor across verified pairs | Shared clientele/limits-to-arbitrage state | Other pairs, historic listing universe; never include Samsung in its own control |

## Registered exploratory products

`X01`: lagged spread difference × lagged common borrow fee, with both main effects, to test whether costly preferred trading and constrained short-common arbitrage reinforce widening. Joint causality remains unresolved; use actual fee availability, not a ban indicator as a fee.

`X02`: lagged retail weight difference × the aligned semiconductor factor shock, with both main effects. Hypothesis: retail clientele magnifies class-relative response to chip news. Sign is open. This interaction is a proposed extension with intuition, not a claimed unpublished discovery. It is skipped if the configured semiconductor factor is not selected.

Future extensions: incremental preferred buybacks × falling preferred float; index-demand surprises × common borrow scarcity; governance announcements × minority-vote contestability; foreign-flow pressure × KRW shocks; post-announcement dividend equalization × retail participation. For each, preserve main effects, availability timestamps, sufficient independent events and rival explanations. No automatic combinatorial interaction search.

## Initial factor selection

The default config uses the shipped names `USSLOWL_COUNTRY`, `USSLOWL_BETA`, `USSLOWL_VALUE`, `USSLOWL_SIZE`, `USSLOWL_MOMENTUM`, `USSLOWL_LIQUIDTY`, `USSLOWL_RESVOL`, `USSLOWL_LEVERAGE`, `USSLOWL_DIVYILD`, `USSLOWL_PROFIT` and `USSLOWL_SEMICOND`. Inspect the live export schema and coverage too. BETA is a vendor factor name, not permission to label it the Korean market return. Factor selection changes require a new run/config snapshot. An all-available-factor sensitivity should be a separate config and must pass rank, conditioning and n/k gates; use theoretical factor constraints to select a reference, never silently let a pseudoinverse disguise unidentified coefficients.
