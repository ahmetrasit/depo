"""Score a recomposition against a fixture's planted-defect answer key.

    python3 review/v3/tools/score.py <workspace> <fixture>/defects.json

A defect matches a finding when the finding's chain/rule/kind reference is one of the defect's
`detect_by` references and every string in `match_any` occurs in the finding message or evidence
(case-insensitive) for at least one of the strings. Findings that match no defect are listed as
candidates for false positives; a human decides whether they are real.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def text_of(f):
    return (f["message"] + " " + " ".join(e.get("entity", "") + " " + e.get("quote", "") for e in f.get("evidence", []))).lower()


def main(ws: Path, key: Path):
    findings = json.loads((ws / "report" / "gaps.json").read_text())
    key_all = json.loads(key.read_text())
    defects = key_all["defects"]
    matched, unmatched_defects, used = [], [], set()
    for d in defects:
        hits = []
        for f in findings:
            if f["ref"] not in d["detect_by"] and f["kind"] not in d["detect_by"]:
                continue
            t = text_of(f)
            if any(s.lower() in t for s in d["match_any"]):
                hits.append(f["id"]); used.add(f["id"])
        (matched if hits else unmatched_defects).append({**d, "findings": hits})
    # inconsistencies the fixture author did not plant but kept (found by run 1); scored separately, never part of recall
    kept = []
    for d in key_all.get("unplanted_kept", []):
        hits = [f["id"] for f in findings if (f["ref"] in d["detect_by"] or f["kind"] in d["detect_by"]) and any(s.lower() in text_of(f) for s in d["match_any"])]
        kept.append({**d, "findings": hits}); used.update(hits)
    fp = [f for f in findings if f["id"] not in used and f["status"] == "break"]
    cand = [f for f in findings if f["id"] not in used and f["status"] != "break"]
    # expected-normal items: only mechanical breaks count; parameter-gap aggregates list entity ids incidentally, candidates are not breaks
    expected_absent = [f for f in findings if f["status"] == "break" and f["kind"] != "param"
                       and any(s.lower() in text_of(f) for d in key_all.get("expected_no_finding", []) for s in d["match_any"])]
    out = {"planted": len(defects), "detected": len(matched), "recall": round(len(matched) / len(defects), 2) if defects else None,
           "matched": matched, "missed": unmatched_defects,
           "unplanted_kept": {"total": len(kept), "detected": sum(bool(k["findings"]) for k in kept), "items": kept},
           "unmatched_breaks": [{"id": f["id"], "ref": f["ref"], "severity": f["severity"], "message": f["message"][:200]} for f in fp],
           "unmatched_candidates": len(cand),
           "false_positive_checks": [{"id": f["id"], "message": f["message"][:200]} for f in expected_absent]}
    (ws / "report" / "score.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"planted {out['planted']} · detected {out['detected']} · recall {out['recall']}")
    for m in matched:
        print(f"  HIT  {m['id']}: {m['title']} <- {m['findings']}")
    for m in unmatched_defects:
        print(f"  MISS {m['id']}: {m['title']} (expected {m['detect_by']})")
    if kept:
        print(f"unplanted kept inconsistencies: {out['unplanted_kept']['detected']}/{len(kept)} detected")
        for k in kept:
            print(f"  {'HIT ' if k['findings'] else 'MISS'} {k['id']}: {k['title'][:90]} {k['findings'][:4]}")
    print(f"unmatched breaks (false-positive candidates): {len(fp)}; reviewer candidates not tied to a defect: {len(cand)}")
    for f in fp[:30]:
        print(f"  ? {f['id']} {f['ref']} {f['severity']}: {f['message'][:160]}")
    if expected_absent:
        print(f"FALSE POSITIVES on expected-normal items: {len(expected_absent)}")
        for f in expected_absent:
            print(f"  ! {f['id']}: {f['message'][:160]}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
