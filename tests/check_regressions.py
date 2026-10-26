"""Synthetic engineering fixtures only; no Samsung empirical regressions."""
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from samsung_research.regressions import (align_factors, collect, digest, fit_ols, fit_task, freeze,
    outcomes, prepare, read_json, tasks, utc_column, write_json)


class RegressionChecks(unittest.TestCase):
    def test_config_names_and_declared_grid(self):
        root = Path(__file__).resolve().parents[1]
        config = read_json(root / "configs/samsung_regressions.json")
        shipped = set(re.findall(r'"(USSLOWL_[A-Z]+)"', (root / "src/sf_quant/data/_factors.py").read_text()))
        self.assertTrue(set(config["factor_names"]).issubset(shipped))
        self.assertEqual(len(tasks(config)), 312)
        self.assertEqual(len({m["id"] for m in config["models"]}), len(config["models"]))

    def test_freeze_excludes_private_profile_and_records_packages(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            for name in ["src/samsung_research", "scripts", "slurm", "docs/regressions", "methodology", "research"]:
                (repo / name).mkdir(parents=True)
            (repo / "slurm/cluster.env.sh").write_text("SYNTHETIC_PRIVATE_VALUE")
            (repo / "slurm/worker.sbatch").write_text("# fixture")
            (repo / "research/regression-requirements.lock").write_text("# fixture")
            write_json(repo / "config.json", {})
            run = repo / "output"
            freeze(repo, run, repo / "config.json")
            self.assertFalse((run / "frozen/slurm/cluster.env.sh").exists())
            self.assertTrue((run / "frozen/slurm/worker.sbatch").exists())
            self.assertTrue(read_json(run / "snapshot.json")["packages"])

    def test_hand_calculated_outcomes_and_gap_masking(self):
        frame = pd.DataFrame(dict(discount_pct=[20, 18, np.nan, 15, 14], common_raw_close=[100]*5,
            preferred_raw_close=[80, 82, np.nan, 85, 86], volume_ratio=[.2, .3, 0, .4, .5]))
        actual = outcomes(frame)
        self.assertAlmostEqual(actual.dd_pp.iloc[1], -2)
        self.assertAlmostEqual(actual.dg.iloc[1], np.log(80/82))
        self.assertTrue(actual.dd_pp.iloc[2:4].isna().all())
        self.assertTrue(np.isnan(actual.lag_activity.iloc[3]))

    def test_timestamp_bins_holiday_and_late_data(self):
        sessions = pd.DataFrame(dict(date=["2020-01-02", "2020-01-06", "2020-01-07"],
            close_utc=["2020-01-02T06:30:00Z", "2020-01-06T06:30:00Z", "2020-01-07T06:30:00Z"]))
        factors = pd.DataFrame(dict(date=["2020-01-02", "2020-01-03", "2020-01-06"], TEST=[1., 2., 3.]))
        timing = pd.DataFrame(dict(date=factors.date,
            period_end_utc=["2020-01-02T21:00:00Z", "2020-01-03T21:00:00Z", "2020-01-06T21:00:00Z"],
            available_at_utc=["2020-01-02T22:00:00Z", "2020-01-03T22:00:00Z", "2020-01-07T09:00:00Z"]))
        a, mapping = align_factors(sessions, factors, timing, ["TEST"], .01)
        self.assertTrue(np.isnan(a.F_TEST.iloc[0]))
        self.assertAlmostEqual(a.F_TEST.iloc[1], .03)
        self.assertTrue(np.isnan(a.F_TEST.iloc[2]))
        self.assertEqual(mapping.status.tolist(), ["available", "available", "late"])
        with self.assertRaises(ValueError):
            utc_column(pd.Series(["2020-01-01T06:00:00"]))
        factors.loc[1, "TEST"] = np.nan
        a, _ = align_factors(sessions, factors, timing, ["TEST"], .01)
        self.assertTrue(np.isnan(a.F_TEST.iloc[1]))

    def test_ols_and_hac_against_independent_score_calculation(self):
        rng = np.random.default_rng(31)
        x = np.column_stack([np.ones(400), rng.normal(size=(400, 2))])
        y = x @ [2, .3, -.2] + rng.normal(size=400)
        b, se, _, e, diag = fit_ols(y, x, np.arange(400), 5)
        expected = np.linalg.solve(x.T @ x, x.T @ y)
        np.testing.assert_allclose(b, expected, atol=1e-12)
        scores = x * (y-x@expected)[:, None]
        meat = scores.T @ scores
        for lag in range(1, 6):
            cross = scores[lag:].T @ scores[:-lag]
            meat += (1-lag/6) * (cross+cross.T)
        bread = np.linalg.inv(x.T@x)
        expected_se = np.sqrt(np.diag(bread @ meat @ bread * 400/397))
        np.testing.assert_allclose(se, expected_se, atol=1e-12)
        self.assertEqual(diag["rank"], 3)
        np.testing.assert_allclose(y-e, x@b)

    def test_hac_does_not_compress_grid_holes(self):
        rng = np.random.default_rng(8)
        x = np.column_stack([np.ones(320), rng.normal(size=320)])
        y = x@[1, 2] + rng.normal(size=320)
        _, full_se, _, _, _ = fit_ols(y, x, np.arange(320), 5)
        _, gap_se, _, _, _ = fit_ols(y, x, np.arange(320)*10, 5)
        self.assertGreater(np.max(abs(full_se-gap_se)), 1e-5)

    def test_rank_constant_and_small_sample_rejection(self):
        rng = np.random.default_rng(2)
        a = rng.normal(size=400)
        for x in [np.column_stack([np.ones(400), a, a]), np.ones((400, 2))]:
            with self.assertRaises(ValueError):
                fit_ols(a, x, np.arange(400), 5)
        with self.assertRaises(ValueError):
            fit_ols(a[:30], np.column_stack([np.ones(30), a[:30]]), np.arange(30), 5)

    def test_synthetic_prepare_fit_collect_and_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pack = root / "pack"
            (pack / "tables").mkdir(parents=True)
            (pack / "provenance").mkdir()
            dates = pd.bdate_range("2020-01-01", periods=330).strftime("%Y-%m-%d")
            rng = np.random.default_rng(21)
            price_p = 80 + np.cumsum(rng.normal(0, .1, len(dates)))
            frame = pd.DataFrame(dict(date=dates, discount_pct=100-price_p, common_raw_close=100,
                preferred_raw_close=price_p, volume_ratio=.2, observed_session=True, flagged=False))
            frame.to_csv(pack / "tables/measures_main.csv", index=False)
            frame.to_csv(pack / "tables/measures_sensitivity.csv", index=False)
            write_json(pack / "provenance/source_inventory.json", {"sources": [{"sha256": "synthetic"}]})
            files = ["tables/measures_main.csv", "tables/measures_sensitivity.csv", "provenance/source_inventory.json"]
            write_json(pack / "manifest.json", {"run_id": "SYNTHETIC", "input_sha256_before": "synthetic",
                "input_sha256_after": "synthetic", "outputs": [{"path": x, "sha256": digest(pack / x)} for x in files]})
            pd.DataFrame(dict(date=dates, TEST=rng.normal(0, 1, len(dates)))).to_csv(root / "factors.csv", index=False)
            pd.DataFrame(dict(date=dates, close_utc=[x+"T06:30:00Z" for x in dates])).to_csv(root / "sessions.csv", index=False)
            pd.DataFrame(dict(date=dates, period_end_utc=[x+"T06:00:00Z" for x in dates],
                available_at_utc=[x+"T06:10:00Z" for x in dates])).to_csv(root / "timing.csv", index=False)
            pd.DataFrame(dict(date=dates)).to_csv(root / "calendar.csv", index=False)
            write_json(root / "barra.json", dict(model_id="SYNTHETIC", geography="Korea", currency="KRW",
                currency_justification="fixture", vintage="fixture", units="percent", timing_source="fixture",
                session_source="fixture", calendar_source="fixture", calendar_start=dates[0], calendar_end=dates[-1], reviewed=True))
            config = dict(inputs=dict(ep01_run="pack", factors="factors.csv", sessions="sessions.csv",
                factor_timing="timing.csv", factor_calendar="calendar.csv", barra_metadata="barra.json",
                mechanisms="absent.csv", mechanisms_metadata="absent.json"), expected_raw_sha256="synthetic",
                factor_names=["TEST"], mechanism_columns=[], min_observations=252,
                observations_per_parameter=20, max_condition=1e8, hac_lags=[5],
                windows=[dict(id="all", start=dates[0], end=dates[-1])],
                models=[dict(id="SYNTHETIC", outcome="dd_pp", columns=[], barra=True)])
            run = root / "run"
            run.mkdir()
            prepare(root, run, config)
            self.assertEqual(len(tasks(config)), 2)
            fit_task(run, 0, config)
            counts = collect(run)
            self.assertEqual(counts["estimated"], 1)
            self.assertEqual(counts["missing"], 1)
            self.assertTrue((run / "REPORT.md").exists())
            with (run / "prepared/panel.csv").open("a") as f:
                f.write("\n")
            with self.assertRaises(RuntimeError):
                fit_task(run, 1, config)
            self.assertEqual(read_json(run / "results/task_00001/result.json")["status"], "failed")


if __name__ == "__main__":
    unittest.main()
