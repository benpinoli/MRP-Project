# Repository and data review — 2026-10-26

The repository combines the `sf-quant` 0.2.7 source library and a separate Samsung research layer. The working tree was clean at review start. No applicable AGENTS.md was found in the repo inventory or checked ancestors. Existing raw files, research registries, output runs and `uv.lock` are preserved.

## Existing evidence

The latest [EP01 run](../../runs/samsung/EP01_descriptive/20261022T070701_403388Z/README.md) uses the immutable WRDS export `samsung_2005-20261020.csv` (SHA-256 `c64a9cdbba02ee7d70cd3fa4b0af14e0540d0beab70d3d55132f333fb11ba8bb`). The selected pair is gvkey 104604, common iid 02W / KR7005930003 and preferred iid 01W / KR7005931001, KRW, exchange 248. There are 5,367 matched dates from 2005-01-03 to 2026-10-20; flag sensitivity has 5,363. These are local listings, not overseas receipts.

The descriptive tables already contain prices, volumes, the spot discount, daily discount changes, review flags and a session proxy. They contain no economic explanation, model estimates, verified returns, borrow fees, investor-category flows or class-level historical Barra mappings. A volume ratio alone is not a liquidity measure. The [source inventory](../../research/source_inventory.json) contains versioned historical definitions; use the current v2 and [vendor definitions](../reference/data/WRDS_VENDOR_DEFINITIONS.md), not superseded v1 assumptions.

## Findings affecting implementation

| Finding | Consequence |
|---|---|
| `load_factors` supplies wide factor returns documented in percent | Explicit metadata and conversion required; never scale exposures as returns |
| Static names use `USSLOWL_`, including style and semiconductor factors | This is not proof of Korean risk coverage. Prefer verified Korea/global model; US-only use is a sensitivity |
| `load_exposures` uses security `barrid` and dated rows | Both Korean class mappings must be obtained before vendor exposure attribution |
| `run_ff_regression` shifts ascending factor dates by -1 | It brings future rows backward. New pipeline does not call it; shared library left unchanged |
| AJEXDI definition and full action taxonomy unresolved | No class price returns or total returns are manufactured from raw prices; ratio changes remain gap changes |
| PRCSTD=5 means carried; status 10 need not have positive volume | Reuse audited eligibility; do not restore a positive-volume price gate |
| Independent KRX sessions/quotes incomplete | Preserve proxy-grid gaps; flag known episodes; obtain a calendar before stronger claims |
| Previous methodology schema prohibited all models | Registry now admits versioned model references; archived run snapshots retain their old meaning |
| Packaging defaults concern `sf_quant` | Cluster scripts explicitly set `PYTHONPATH=src`; do not rely on Samsung being installed by the library wheel |

## Remaining risks and concrete next inputs

Reconcile the flagged episodes listed in EP01, especially the 2012 carried/status conflict and unusually large moves. Obtain exact historical KRX close times (including special sessions), vendor return period ends/availability and both share classes' corporate actions. Same-date joins across US and Korean markets can use information that arrives after Seoul closes. Do not assume a constant close timestamp throughout a twenty-year history without source verification.

An observed reversal can reflect changing liquidity, retail participation, supply, index clientele, control rights, expected cash flows or measurement. Test these as competing mechanisms. Neither the descriptive trend nor a factor-adjusted residual alone identifies private control benefits or a required-return shock.
