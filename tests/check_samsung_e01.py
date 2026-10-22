"""Small synthetic fixtures are tests, never empirical chart inputs."""
import copy
import math
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"src"))
from samsung_research.e01 import (ROOT, adjusted_price, discount, eligibility,
    load_and_validate, match_pair, methodology_markdown, read_json,
    validate_registry, write_csv)


class SamsungValidation(unittest.TestCase):
    def setUp(self):
        self.config = read_json(ROOT/"configs/samsung_e01.json")

    def row(self, label="common", t="2018-05-04", price="100", factor="1"):
        mapping = self.config["classes"][label]
        return dict(gvkey="104604", datadate=t, isin=mapping["isin"], iid=mapping["iid"],
                    exchg="248", tpci=mapping["tpci"], curcdd="KRW", prccd=price,
                    qunit="1", prcstd="10", cshtrd="100", ajexdi=factor,
                    split="", prchd="", prcld="")

    def test_discount_denominator_and_invalid_prices(self):
        self.assertAlmostEqual(discount(80,100),20)
        self.assertAlmostEqual(discount(120,100),-20)
        for value in (0, -1, "", "nan", "inf"):
            self.assertIsNone(discount(value,100))
            self.assertIsNone(discount(80,value))

    def test_split_continuity_and_raw_ratio_invariance(self):
        before = self.row(price="2500000", factor="50")
        with self.assertRaisesRegex(ValueError,"unresolved"):
            adjusted_price(before)
        self.assertAlmostEqual(discount(2000000,2500000),discount(40000,50000))

    def test_status_dominates_volume_and_unchanged_not_excluded(self):
        r = self.row()
        self.assertEqual(eligibility(r,self.config),[])
        r["prcstd"] = "5"
        self.assertIn("carried_price",eligibility(r,self.config))
        r["prcstd"] = "10"
        r["cshtrd"] = ""
        self.assertEqual(eligibility(r,self.config),[])

    def test_units_ranges_and_weekend(self):
        r = self.row()
        for unit in ("", "0", "-1", "nan", "inf"):
            r["qunit"] = unit
            self.assertIn("unsupported_quotation_unit",eligibility(r,self.config))
        r["qunit"] = "100"
        self.assertIn("unsupported_quotation_unit",eligibility(r,self.config))
        r.update(qunit="1", prcld="101", prchd="110")
        self.assertIn("inconsistent_high_low_close",eligibility(r,self.config))
        r = self.row(t="2018-05-05")
        self.assertIn("weekend",eligibility(r,self.config))

    def test_class_aware_join_no_filling_and_base_date(self):
        rows = [self.row("common"), self.row("preferred",price="80"), self.row("common",t="2018-05-08",price="110")]
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/"fixture.csv"
            write_csv(p,rows)
            _,_,_,norm = load_and_validate(p,self.config)
            paired,base = match_pair(norm,self.config)
        self.assertEqual(base,"2018-05-04")
        self.assertAlmostEqual(paired[0]["discount_pct"],20)
        self.assertIsNone(paired[0]["common_index"])
        self.assertIsNone(paired[0]["preferred_index"])
        self.assertIsNone(paired[1]["discount_pct"])
        self.assertIn("preferred:absent_row",paired[1]["exclusion_reasons"])

    def test_raw_discount_does_not_require_adjustment_or_volume(self):
        rows = [self.row("common"), self.row("preferred",price="80")]
        for r in rows:
            r.update(ajexdi="", cshtrd="")
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/"fixture.csv"
            write_csv(p,rows)
            _,_,_,norm = load_and_validate(p,self.config)
            paired,_ = match_pair(norm,self.config)
        self.assertAlmostEqual(paired[0]["discount_pct"],20)
        self.assertFalse(paired[0]["pair_index_eligible"])
        self.assertTrue(all(r["volume_review"] for r in norm))

    def test_duplicate_or_wrong_isin_aborts(self):
        common,preferred = self.row(),self.row("preferred")
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/"fixture.csv"
            write_csv(p,[common,preferred,common])
            with self.assertRaisesRegex(ValueError,"Duplicate"):
                load_and_validate(p,self.config)
            common["isin"] = preferred["isin"]
            write_csv(p,[common,preferred])
            with self.assertRaisesRegex(ValueError,"Identity"):
                load_and_validate(p,self.config)

    def test_registry_schema_and_markdown_consistency(self):
        r = read_json(ROOT/"methodology/methodology.json")
        s = read_json(ROOT/"methodology/schema.json")
        md = (ROOT/"docs/METHODOLOGY.md").read_text(encoding="utf-8")
        validate_registry(r,s,md)
        changed = copy.deepcopy(r)
        changed["measures"][0]["formula"] = "incorrect alternative"
        with self.assertRaisesRegex(ValueError,"differs"):
            validate_registry(changed,s,md)


if __name__ == "__main__":
    unittest.main()
