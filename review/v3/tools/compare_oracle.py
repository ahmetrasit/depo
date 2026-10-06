"""Compare a model extraction run against the oracle run for the same fixture.

    python3 review/v3/tools/compare_oracle.py <run_ws> <oracle_ws>

Reports entity recall by L2 (oracle entity keys found in the run), parameter fill against the oracle's
parameters on shared entities, anchor agreement, extra entities the run produced that the oracle did not,
and the finding-level difference (defects detected by each, from score.json if present).
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def norm(v):
    return re.sub(r"\s+", " ", str(v or "")).strip().lower()


def load(ws):
    reg = json.loads((Path(ws) / "registry.json").read_text())
    ents = {}
    for e in reg["entities"].values():
        ents[(norm(e["entity_type"]), norm(e["id"]))] = e
    return reg, ents


def main(run, oracle):
    rreg, rents = load(run)
    oreg, oents = load(oracle)
    # entity recall by L2, matching on id only when type differs (agents may choose another entity_type)
    by_id_run = defaultdict(list)
    for (t, i), e in rents.items():
        by_id_run[i].append(e)
        for a in e.get("alias_ids", []):
            if norm(a) != i:
                by_id_run[norm(a)].append(e)
    per_l2 = defaultdict(lambda: {"oracle": 0, "found": 0, "params_oracle": 0, "params_found": 0, "params_agree": 0})
    missing = []
    for (t, i), oe in oents.items():
        cands = by_id_run.get(i, [])
        hit = next((c for c in cands if norm(c["entity_type"]) == t), None) or (cands[0] if cands else None)
        for l2 in oe["l2"]:
            per_l2[l2]["oracle"] += 1
            if hit and l2 in hit["l2"]:
                per_l2[l2]["found"] += 1
            for k, v in oe["params"].items():
                per_l2[l2]["params_oracle"] += 1
                if hit and k in hit["params"] and hit["params"][k] not in (None, "", []):
                    per_l2[l2]["params_found"] += 1
                    a, b = hit["params"][k], v
                    if isinstance(b, list):
                        agree = set(map(norm, a if isinstance(a, list) else [a])) >= set(map(norm, b))
                    elif isinstance(b, bool):
                        agree = (a is b) or norm(a) in ({"true", "yes"} if b else {"false", "no"})
                    else:
                        agree = norm(a) == norm(b) or norm(b) in norm(a) or norm(a) in norm(b)
                    per_l2[l2]["params_agree"] += int(agree)
        if not hit:
            missing.append(f"{t}:{i} ({', '.join(oe['l2'])})")
    extra = [f"{e['entity_type']}:{e['id']} ({', '.join(e['l2'])})" for (t, i), e in rents.items() if i not in {k[1] for k in oents}]
    tot_o = sum(v["oracle"] for v in per_l2.values()); tot_f = sum(v["found"] for v in per_l2.values())
    po = sum(v["params_oracle"] for v in per_l2.values()); pf = sum(v["params_found"] for v in per_l2.values()); pa = sum(v["params_agree"] for v in per_l2.values())
    anchors = {}
    for k, a in oreg["anchors"].items():
        r = rreg["anchors"].get(k, {})
        anchors[k] = {"oracle": a.get("value"), "run": r.get("value"), "agree": norm(a.get("value")) == norm(r.get("value")) if a.get("value") else None, "run_conflict": r.get("conflict")}
    out = {"entity_recall": round(tot_f / tot_o, 3) if tot_o else None, "entities_oracle": tot_o, "entities_found": tot_f,
           "param_fill_vs_oracle": round(pf / po, 3) if po else None, "param_agreement_when_filled": round(pa / pf, 3) if pf else None,
           "per_l2": {k: dict(v, recall=round(v["found"] / v["oracle"], 2) if v["oracle"] else None) for k, v in sorted(per_l2.items())},
           "missing_entities": missing, "extra_entities_count": len(extra), "extra_entities_sample": extra[:40], "anchors": anchors}
    for ws in (run,):
        s = Path(ws) / "report" / "score.json"
        if s.exists():
            sc = json.loads(s.read_text()); out["run_score"] = {"recall": sc["recall"], "detected": sc["detected"], "planted": sc["planted"], "missed": [m["id"] for m in sc["missed"]], "unmatched_breaks": len(sc["unmatched_breaks"])}
    (Path(run) / "report" / "compare_oracle.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"entity recall {out['entity_recall']} ({tot_f}/{tot_o}) · param fill {out['param_fill_vs_oracle']} · agreement when filled {out['param_agreement_when_filled']} · extra entities {len(extra)}")
    for k, v in out["per_l2"].items():
        if v["recall"] is not None and v["recall"] < 1:
            print(f"  {k}: recall {v['recall']} ({v['found']}/{v['oracle']})")
    for k, a in anchors.items():
        if a["agree"] is False or a["run_conflict"]:
            print(f"  anchor {k}: oracle={a['oracle']!r} run={a['run']!r} conflict={a['run_conflict']}")
    if "run_score" in out:
        print("score:", out["run_score"])


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
