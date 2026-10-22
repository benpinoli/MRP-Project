"""Independent saved-output checks; no vendor data upload or modification."""
import argparse
import csv
import hashlib
import json
import math
import re
import statistics
import sys
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))


def check_equal(actual, expected):
    if expected is None:
        assert actual=="", (actual,expected)
    else:
        assert actual and math.isclose(float(actual),expected,rel_tol=1e-10,abs_tol=1e-10),(actual,expected)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("run_path")
    parser.add_argument("--record-review",action="store_true",help="Record after separate human/agent visual inspection")
    args=parser.parse_args()
    run=(ROOT/args.run_path).resolve()
    m=json.loads((run/"manifest.json").read_text(encoding="utf-8"))
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    assert m["status"].startswith("completed")
    assert digest(Path(m["input_path"]))==m["input_sha256_before"]==m["input_sha256_after"]
    assert all(digest(run/o["path"])==o["sha256"] for o in m["outputs"])
    assert m["validation_exit_code"]==0
    raw=list(csv.DictReader(Path(m["input_path"]).open(encoding="utf-8-sig")))
    source={(r["iid"],r["datadate"]):r for r in raw if r["gvkey"]=="104604" and r["iid"] in ("01W","02W")}
    outputs={v:list(csv.DictReader((run/f"tables/measures_{v}.csv").open(encoding="utf-8"))) for v in ("main","sensitivity")}
    assert [r["date"] for r in outputs["main"]]==[r["date"] for r in outputs["sensitivity"]]
    for variant,rows in outputs.items():
        sessions=[r for r in rows if r["observed_session"]=="True"]
        changes=[]
        for i,r in enumerate(sessions):
            current=float(r["discount_pct"]) if r["discount_pct"] else None
            prior=float(sessions[i-1]["discount_pct"]) if i and sessions[i-1]["discount_pct"] else None
            delta=current-prior if current is not None and prior is not None else None
            changes.append(delta)
            check_equal(r["discount_change_pp"],delta)
            block=changes[-20:]
            expected=statistics.stdev(block) if len(block)==20 and all(v is not None for v in block) else None
            check_equal(r["rolling_change_std_pp"],expected)
        for r in rows:
            if variant=="sensitivity" and r["flagged"]=="True":
                assert all(r[key]=="" for key in ("discount_pct","common_raw_close","preferred_raw_close","common_volume","preferred_volume","volume_ratio"))
            if r["discount_pct"]:
                p,c=source["01W",r["date"]],source["02W",r["date"]]
                assert p["prcstd"]==c["prcstd"]=="10"
                expected=float(Decimal(100)*(1-Decimal(p["prccd"])/Decimal(c["prccd"])))
                check_equal(r["discount_pct"],expected)
            for label,iid in (("common","02W"),("preferred","01W")):
                if r[label+"_raw_close"]:
                    sr=source[iid,r["date"]]
                    check_equal(r[label+"_raw_close"],float(sr["prccd"]))
                if r[label+"_volume"]:
                    check_equal(r[label+"_volume"],float(source[iid,r["date"]]["cshtrd"]))
            expected=float(r["preferred_volume"])/float(r["common_volume"]) if r["preferred_volume"] and r["common_volume"] and float(r["common_volume"])>0 else None
            check_equal(r["volume_ratio"],expected)
    annual=list(csv.DictReader((run/"tables/annual_distributions.csv").open(encoding="utf-8")))
    for r in annual:
        values=[float(x["discount_pct"]) for x in outputs[r["variant"]] if x["date"].startswith(r["year"]) and x["discount_pct"]]
        assert len(values)==int(r["observations"])
        check_equal(r["median"],statistics.median(values))
    pngs=list(run.rglob("*.png"))
    svgs=list(run.rglob("*.svg"))
    assert len(pngs)==len(svgs)==13
    paths=[ROOT/"docs/HYPOTHESES.md",ROOT/"docs/RESEARCH_LOG.md",ROOT/"runs/README.md",run/"README.md",run/"episodes/REVIEW.md"]
    link_count=0
    for path in paths:
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)",path.read_text(encoding="utf-8")):
            if "://" in target:
                continue
            filename=target.split("#")[0].strip("<>")
            if filename:
                assert (path.parent/filename).resolve().exists(),(path,target)
                link_count+=1
    raw_old=ROOT/"docs/reference/data/samsung_data/samsung_05-26.csv"
    assert digest(raw_old)=="bee836dd98b021ce17e3692e71cb72eba1565de6abc59b56274d2697cc9d2924"
    catalog=json.loads((ROOT/"research/artifacts.json").read_text(encoding="utf-8"))
    assert all((ROOT/a["path"]).is_file() for a in catalog["artifacts"])
    print(f"Verified every saved discount/change/rolling std/volume ratio, annual medians, 13 PNG + 13 SVG files, all output hashes, both immutable raw inputs, and {link_count} local links.")
    if args.record_review:
        from samsung_research.e01 import read_json,write_json
        from samsung_research.navigation import append_unique,generate_indexes
        reviews=read_json(ROOT/"research/run_reviews.json")
        reviews[m["run_id"]]=dict(status="verified",note="All six main/sensitivity layouts inspected; corrected episode plot inspected. Independent saved-output arithmetic and local links verified; raw unchanged. Remaining quote/calendar flags are not resolved.",verified_at=datetime.now(timezone.utc).isoformat())
        write_json(ROOT/"research/run_reviews.json",reviews)
        append_unique(ROOT/"research/observations.jsonl",[dict(id=f"O_EP01_{m['run_id']}_QA",timestamp=datetime.now(timezone.utc).isoformat(),author_type="ai",author="Codex",pair="samsung_local_common_preferred",kind="validation",impact="measurement concern",hypothesis_ids=["H0"],run_ids=[m["run_id"]],figure_ids=m["figure_ids"],claim=reviews[m["run_id"]]["note"],data_references=[str(run.relative_to(ROOT)/"manifest.json"),"research/run_reviews.json"],competing_explanations=["Independent vendor prices/calendar remain unchecked"],next_experiment="Resolve flags with independent evidence; keep economic hypotheses provisional",prespecified=True)])
        generate_indexes()


if __name__=="__main__":
    main()
