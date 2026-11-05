"""Retain historical evidence while reorganizing the Samsung tree for years."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "regressions"

TRACKS = [
    dict(id="LH1", rank=1, title="Public share supply and sustained trading capacity",
         nodes=["S06", "S01", "S02", "S03", "S04", "S05", "L01"],
         question="Do years of relative supply and trading capacity explain persistent discount changes?",
         data="Quarterly class share counts, treasury/strategic holdings, executed actions, documented public float, and monthly trading costs/capacity.",
         test="Reconstruct supply and cost histories jointly; distinguish scarcity/support from deteriorating ability to trade and management responding to the gap."),
    dict(id="LH2", rank=2, title="Durable investor base, institutional demand and access",
         nodes=["D01", "D02", "D03", "D05", "D04"],
         question="Who holds each class over years, and do changes in that investor base persistently reprice the classes?",
         data="Class-level quarterly/annual foreign and institutional holdings, holder concentration, retail participation, index/mandate histories and dated eligibility rules.",
         test="Separate ownership stocks from trading flows; compare durable class-relative ownership/access changes with discount regimes and comparable peers."),
    dict(id="LH3", rank=3, title="Control, minority rights and governance regimes",
         nodes=["G01", "G02", "G04", "G03"],
         question="Does a sustained change in control or shareholder protection alter what common votes are worth?",
         data="Dated controller/affiliate blocks, independent blocks, agreements, succession/control events and effective legal/charter rules.",
         test="Distinguish lower unequal-treatment risk from more effective minority votes; test the two potentially opposing channels with actual ownership states."),
    dict(id="LH4", rank=4, title="Multi-year payout policy, cash rights and income investors",
         nodes=["P05", "P01", "P02", "P04", "P03"],
         question="Do credible sustained cash-return policies change relative demand and the holding outcome of the two classes?",
         data="Dated policy commitments and changes, actual class cash payments, earnings/free cash flow, payout coverage and investor composition.",
         test="Compare policy eras and delivery over quarters/years; separate cash received from terminal discount and remove mechanical yield/price-ratio explanations."),
    dict(id="LH5", rank=5, title="Class structure, investor access and market integration",
         nodes=["S07", "X01", "X02", "X03"],
         question="What verified structural change could permanently reduce segmentation or equalize class rights?",
         data="Historical class terms, conversion/unification proposals or implementation if any, receipt ratios/venues, access and ownership restrictions.",
         test="Audit a credible legal/economic convergence route before assigning it value; distinguish an actual change from a hypothetical scenario."),
    dict(id="LH6", rank=None, title="Cross-cutting constraints that allow a gap to last",
         nodes=["L02", "L03", "L04", "L05"],
         question="Why can investors not cheaply maintain a position that closes the gap over years?",
         data="Lending/borrow availability and fees, applicable short-sale rules, funding conditions, holding costs and the existence or absence of a terminal event.",
         test="Evaluate persistence and the cost/risk of corrective positions alongside each leading mechanism; a short-sale ban alone is not a measured borrowing cost."),
    dict(id="LH7", rank=None, title="Company and economic cycles through a class-specific channel",
         nodes=["R01", "R02", "R03", "R04", "R05"],
         question="Do multi-year company or macro cycles alter class demand, payout credibility or trading capacity differently?",
         data="Quarterly cash generation/capital spending, industry state, rates/FX, and observed class-specific transmission variables.",
         test="Require a differential-class channel; compare complete economic cycles and peers rather than re-labeling US style returns as Samsung fundamentals."),
    dict(id="FOUNDATION", rank=None, title="Measurement and legal foundations",
         nodes=["M01", "M02", "M03", "M04", "M05", "M06"],
         question="Are the long-run price ratios, class rights and cash outcomes comparable?",
         data="Class identifiers, historical units/actions, independent calendar, entitlements and publication dates.",
         test="Validate monthly/quarterly aggregation and historical rights; use daily timing or ex-date tests only to resolve a material long-run ambiguity."),
    dict(id="ARCHIVE", rank=None, title="Archived daily forecasting questions",
         nodes=["B01", "B02", "B03", "B04"],
         question="What was learned in the earlier daily forecasting program?",
         data="Preserved historical forecasts, reviews and run records.",
         test="Do not resume daily reversal/model selection under the active long-horizon objective. Preserve findings within their original scope."),
]

NEW_NODES = [
    dict(id="S06", parent="SUPPLY", title="Cumulative public-share supply and liquidity feedback",
         mechanism_chain="Years of class-specific issuance, repurchases, treasury holdings and strategic ownership change the shares available to investors and the capacity to trade them",
         expected_sign="Preferred scarcity/support may narrow; impaired preferred trading capacity may widen. Measure both, not a universal sign.",
         data_fields=["class issued/outstanding shares", "treasury shares", "strategic and locked holdings", "documented public float", "actual cumulative class actions", "relative trading costs/capacity"],
         distinguishing_prediction="Persistent discount changes align with documented relative public supply and cost/capacity changes, beyond issuer share-count headlines",
         nearest_rival="Management targets an existing discount; ownership shifts rather than supply cause the repricing",
         evidence_source_ids=["long_cm05", "long_samsung15"],
         next_discriminating_test="Build a quarterly 2005-onward class supply/ownership bridge, split-adjusted, and compare supply and trading-capacity paths before fitting"),
    dict(id="P05", parent="PAYOUT", title="Credibility and delivery of multi-year payout policy",
         mechanism_chain="A durable, implemented cash-return commitment changes expected cash availability and the investor base of the classes",
         expected_sign="Preferred income demand may narrow; direction is conditional on actual allocation and rights, not shared earnings alone",
         data_fields=["policy announcement and effective dates", "promised cash-return framework", "actual class cash distributions", "cash generation and coverage", "policy revisions", "class holder composition"],
         distinguishing_prediction="A sustained discount regime shift accompanies a credible policy and its delivery after separating common cash news and price-ratio arithmetic",
         nearest_rival="Concurrent buybacks/control changes or a policy announced in response to existing undervaluation",
         evidence_source_ids=["long_bc11", "long_samsung15", "long_samsung17"],
         next_discriminating_test="Reconstruct dated payout regimes and delivery over years; compare with relative share supply, ownership and peer changes"),
    dict(id="G04", parent="GOV", title="Governance reform: cash protection versus effective minority votes",
         mechanism_chain="Changes in rules/enforcement can reduce unequal treatment while separately changing whether common votes matter",
         expected_sign="Better protection of nonvoting cash claims can narrow; greater common voting effectiveness can widen. Net sign is an empirical question.",
         data_fields=["dated legal/charter implementation", "actual ownership blocks", "minority voting relevance", "credible enforcement/governance evidence", "class rights"],
         distinguishing_prediction="Persistent relative repricing differs by actual exposure to cash protection and control contestability rather than every governance headline having the same sign",
         nearest_rival="Reforms improve total firm value equally, or investor access/payout changes coincide",
         evidence_source_ids=["long_ck99", "long_od07", "long_pj05"],
         next_discriminating_test="Qualify relevant historical changes and reconstruct controller/independent blocks; distinguish firm-wide valuation from class-relative effects"),
    dict(id="S07", parent="SUPPLY", title="Credible class unification or rights equalization over years",
         mechanism_chain="An implemented or credible future change in class structure alters expected terminal rights and the buyer base",
         expected_sign="Toward the value of actual post-change entitlements; no automatic one-for-one conversion or zero discount assumption",
         data_fields=["issue-specific rights", "actual proposals/announcements if present", "approval incentives and control blocks", "exchange terms", "effective dates"],
         distinguishing_prediction="Relative valuation changes with verifiable prospects and terms of equalization, rather than time passing alone",
         nearest_rival="Speculation about a transaction that has no legal or economic path, or simultaneous firm-wide governance news",
         evidence_source_ids=["long_pj05", "long_ck99"],
         next_discriminating_test="Audit actual Samsung class terms and any documented structural proposal; absent evidence keep as a conditional 5/10-year scenario"),
]

SOURCES = {
    "long_cm05": ("https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART001103943", "Chay and Moon 2005: journal record/abstract, not verified full tables"),
    "long_ck99": ("https://www.acsu.buffalo.edu/~keechung/JCF.PDF", "Chung and Kim 1999: author-hosted full paper"),
    "long_od07": ("https://ba-odegaard.no/publications/abf/index.html", "Odegaard 2007: author summary and linked supplementary results"),
    "long_pc19": ("https://www.sciencedirect.com/science/article/abs/pii/S1566014117302315", "Park et al. 2019: abstract/previous transcription; current full-text retrieval denied"),
    "long_sv97": ("https://web.stanford.edu/~piazzesi/Reading/ShleiferVishny1997.pdf", "Shleifer and Vishny 1997: full original paper"),
    "long_fd99": ("https://www.nber.org/papers/w6572", "Froot and Dabora: original abstract via search; direct page retrieval denied"),
    "long_bc11": ("https://www.ecgi.global/sites/default/files/working_papers/documents/SSRN-id1881657.pdf", "Bigelli and Croci 2011 working version, not final 2013 numerical estimates"),
    "long_pj05": ("https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp465.pdf", "Pajuste 2005: full ECB working paper"),
    "long_samsung15": ("https://news.samsung.com/global/samsung-electronics-announces-shareholder-return-plan", "Dated October 29 2015 issuer policy announcement, not proof of its price effects"),
    "long_samsung17": ("https://www.samsung.com/global/ir/reports-disclosures/public-disclosure-view.70985/", "Dated October 31 2017 issuer policy announcement, not proof of its price effects"),
}


def reorganize():
    path = DOCS / "PREDICTION_MECHANISM_TREE.json"
    tree = json.loads(path.read_text(encoding="utf-8"))
    old_ids = {n["id"] for n in tree["nodes"]}
    for node in NEW_NODES:
        if node["id"] not in old_ids:
            tree["nodes"].append(dict(node, timing="Quarters and years; 2/5/10-year scenarios",
                data_availability="Source route identified; longitudinal Samsung panel not yet reconstructed",
                status="untested", status_scope="Long-horizon mechanism not empirically tested",
                evidence_paths=["docs/regressions/LONG_HORIZON_LITERATURE.md"],
                failure_reason="No new empirical test in this reorganization", priority="long_horizon",
                causal_status="Hypothesis, not an identified Samsung effect"))
    assert len(tree["nodes"]) == 44
    membership = {key: t for t in TRACKS for key in t["nodes"]}
    assert sum(len(t["nodes"]) for t in TRACKS) == len(membership)
    assert set(membership) == {n["id"] for n in tree["nodes"]}
    tree.update(schema_version="2.0.0", updated_utc="2026-11-05",
        active_objective="Explain persistent Samsung preferred-discount levels and structural changes over 2, 5 and 10 years",
        active_plan="docs/regressions/LONG_HORIZON_RESEARCH_PLAN.md",
        literature_review="docs/regressions/LONG_HORIZON_LITERATURE.md",
        base_tree_commit="26e8957", horizon_years=[2, 5, 10],
        observation_frequency="Monthly prices, quarterly mechanisms, annual checks; preserve actual publication frequency",
        execution_status="Agents on user-requested hold; planning/reorganization only; no new empirical results",
        purpose="Rank slow structural mechanisms and distinguish what sets the gap, moves it, and allows it to persist",
        status_rule="Historical status and scope are preserved. Use long_horizon_status for the active question; daily forecasting failures do not refute long-run mechanisms.",
        research_tracks=TRACKS,
        current_information_priority=[f"{t['id']}: {t['title']}" for t in TRACKS[:7]])
    for key, (url, access) in SOURCES.items():
        tree["sources"][key] = dict(url=url, availability=access,
            reviewed_date="2026-11-05", synthesis="docs/regressions/LONG_HORIZON_LITERATURE.md")
    for node in tree["nodes"]:
        t = membership[node["id"]]
        node.setdefault("historical_priority", node["priority"])
        node["priority"] = t["id"]
        node["research_track"] = t["id"]
        node["long_horizon_status"] = (
            "documented foundation; historical completeness still scoped" if node["id"] in {"M02", "M03", "M06"}
            else "supporting measurement question" if t["id"] == "FOUNDATION"
            else "archived short-horizon finding; no long-run inference" if t["id"] == "ARCHIVE"
            else "untested for persistent 2/5/10-year Samsung effects")
        node["long_horizon_next_action"] = t["test"]
        node["long_horizon_data"] = t["data"]
    order = {n: i for i, n in enumerate(k for t in TRACKS for k in t["nodes"])}
    tree["nodes"].sort(key=lambda n: order[n["id"]])
    tree["search_rules"] = [
        "Active scope is persistent discount level and structural change over 2/5/10 years, not next-session forecast error",
        "Preserve stable IDs, historical evidence, negative findings and the scope of each finding",
        "Measure at monthly/quarterly/annual frequencies appropriate to actual independent information",
        "Count independent years, policy changes and ownership observations; overlapping endpoints are not independent experiments",
        "Separate causes of a gap, triggers that change it, and constraints that sustain it",
        "Test scarcity versus trading-capacity effects and cash-protection versus voting-effectiveness channels separately",
        "No forced fixed equilibrium, zero terminal discount, assumed conversion or firm-wide cash-news explanation without a class channel",
        "Reconstruct multi-year supply/ownership/payout histories rather than treating six recent disclosures as a complete study",
        "Peer evidence must match class rights and distinguish company-specific from common market changes",
        "Accessible-data proxies are labeled; a proxy null does not reject its parent mechanism",
        "Preserve simple logged patches and recurring independent inspection; no new local empirical work or agent restart in this planning turn",
    ]
    path.write_text(json.dumps(tree, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    render(tree)
    ledger_path = DOCS / "PREDICTION_HYPOTHESIS_LEDGER.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger.update(updated_utc="2026-11-05", status="long_horizon_reorganization_on_user_hold",
        active_plan=tree["active_plan"], active_research=dict(
            objective=tree["active_objective"], horizon_years=[2, 5, 10],
            literature_review=tree["literature_review"],
            research_tracks=[t["id"] for t in TRACKS],
            empirical_status="No new long-horizon tests; historical daily results retained with original scope",
            next_action="After user resumption: monthly/quarterly discount map and longitudinal supply/ownership/cost/payout/control coverage matrix"),
        historical_hypotheses_scope="Existing P01-P07 entries record prior daily forecasting work, not current long-horizon mechanism verdicts",
        mechanism_tree_branch_count=44)
    ledger["forecast"]["active"] = False
    ledger["forecast"]["scope"] = "Archived 1/5/20-session protocol; not the active user objective"
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Reorganized 44 stable branches in 7 active tracks plus foundations and archive; no empirical status promoted.")


def render(tree):
    lines = ["# Samsung discount hypothesis tree: 2, 5 and 10 years", "",
        "Active objective: understand persistent discount levels and structural change over years. Daily forecasting is archived.", "",
        "[Active research plan](LONG_HORIZON_RESEARCH_PLAN.md) · [Literature synthesis](LONG_HORIZON_LITERATURE.md) · [Canonical JSON](PREDICTION_MECHANISM_TREE.json)", "",
        "All original 40 IDs and scoped findings are retained. Four distinct long-run branches are added: cumulative public supply (S06), payout credibility (P05), opposing governance channels (G04), and credible class equalization (S07). No new empirical results are claimed. Agents remain on user-requested hold.", "",
        "Historical evidence and current long-horizon status are different fields. A daily proxy/model failure is not a verdict on a structural mechanism. Supported arithmetic or documented rights are not proven causes of Samsung's long-run discount.", "",
        "## Research order", "", "| Order | Track | Question |", "|---|---|---|"]
    for t in tree["research_tracks"]:
        rank = str(t["rank"]) if t["rank"] else {"LH6": "Cross-cutting", "LH7": "Conditional", "FOUNDATION": "Prerequisite", "ARCHIVE": "Archived"}[t["id"]]
        lines.append(f"| {rank} | {t['id']} — {t['title']} | {t['question']} |")
    nodes = {n["id"]: n for n in tree["nodes"]}
    for t in tree["research_tracks"]:
        lines += ["", f"## {t['id']} — {t['title']}", "", t["question"], "", f"Data across time: {t['data']}", "", f"Next active task: {t['test']}"]
        for key in t["nodes"]:
            n = nodes[key]
            lines += ["", f"### {key} — {n['title']}", "",
                f"**Current long-horizon status:** {n['long_horizon_status']}.", "",
                f"Economic chain: {n['mechanism_chain']}. Expected direction: {n['expected_sign']}.", "",
                f"Distinguishing observation: {n['distinguishing_prediction']}. Nearest rival: {n['nearest_rival']}.", "",
                f"Historical or foundational evidence: **{n['status']}** — {n['status_scope']}. Original timeframe: {n['timing']}.", "",
                f"Existing data status: {n['data_availability']}. Limitation: {n['failure_reason']}.", "",
                f"Original next-test note (subject to the active long-horizon task above): {n['next_discriminating_test']}.", "",
                f"Evidence/source keys: {', '.join(n['evidence_source_ids'])}; exact paths and access qualifications remain in the canonical JSON."]
    lines += ["", "## Research discipline", ""] + [f"- {s}" for s in tree["search_rules"]]
    (DOCS / "PREDICTION_MECHANISM_TREE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    reorganize()
