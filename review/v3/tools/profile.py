"""Build the v3 review profile from the standards-axis hierarchy plus an activation overlay.

The hierarchy (standards-axis/BIN-HIERARCHY.json) is the reference and is never edited.
The overlay (profile/activation.json) selects bins, recalibrates importance, marks parameter
scope (submission vs dhf), merges checklist-style L2s, and adds missing L2s.

Usage:
    python3 review/v3/tools/profile.py build  [--overlay review/v3/profile/activation.json] [--out review/v3/profile/profile.json]
    python3 review/v3/tools/profile.py show   [--out ...]        # print a summary of the built profile
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HIERARCHY = ROOT / "standards-axis" / "BIN-HIERARCHY.json"
DEFAULT_OVERLAY = ROOT / "profile" / "activation.json"
DEFAULT_OUT = ROOT / "profile" / "profile.json"

# Parameters that are conventionally held in the DHF/QMS rather than supplied in the
# submission. The overlay can override any of these per parameter.
DEFAULT_DHF_PARAM_NAMES = {
    "executor_identity", "executor_independence", "test_tools_and_versions",
    "approver_names_roles", "plan_approval_date", "coding_standards", "tools_used",
}


def load(path: Path):
    return json.loads(path.read_text())


def build(overlay_path: Path = DEFAULT_OVERLAY) -> dict:
    hierarchy = load(HIERARCHY)
    overlay = load(overlay_path) if overlay_path.exists() else {}
    active_l1 = set(overlay.get("activate_l1") or [b["id"] for b in hierarchy["bins"]])
    imp_over = overlay.get("importance_overrides", {})
    scope_over = overlay.get("parameter_scope_overrides", {})
    merges = {m["into"]: m for m in overlay.get("l2_merges", [])}
    merged_away = {mid: m["into"] for m in overlay.get("l2_merges", []) for mid in m["merge"]}
    additions = overlay.get("l2_additions", [])
    corrections = overlay.get("l2_corrections", [])
    dormant_l2 = set(overlay.get("deactivate_l2", []))
    param_adds = overlay.get("parameter_additions", {})
    req_over = overlay.get("required_enhanced_overrides", {})

    bins = []
    for b in hierarchy["bins"]:
        if b["id"] not in active_l1:
            continue
        nb = copy.deepcopy(b)
        l2s = []
        for x in nb.get("l2", []):
            if x["id"] in merged_away or x["id"] in dormant_l2:
                continue
            if x["id"] in merges:
                m = merges[x["id"]]
                absorbed = [y for y in nb["l2"] if y["id"] in m["merge"]]
                x["title"] = m.get("title", x["title"])
                x["merged_from"] = [y["id"] for y in absorbed]
                seen = {p["name"] for p in x["parameters"]}
                for y in absorbed:
                    for p in y["parameters"]:
                        if p["name"] not in seen:
                            x["parameters"].append(p); seen.add(p["name"])
                    x["clauses"] = x.get("clauses", []) + y.get("clauses", [])
                if m.get("note"):
                    x["merge_note"] = m["note"]
            if x["id"] in imp_over:
                x["importance_original"] = x["importance"]
                x["importance"] = imp_over[x["id"]]
            for extra in param_adds.get(x["id"], []):
                if extra["name"] not in {p["name"] for p in x["parameters"]}:
                    q = dict(extra); q.setdefault("required_enhanced", False); q.setdefault("check_type", "mechanical"); q["added_by_overlay"] = True
                    x["parameters"].append(q)
            for p in x["parameters"]:
                key = f"{x['id']}.{p['name']}"
                p["scope"] = scope_over.get(key) or ("dhf" if p["name"] in DEFAULT_DHF_PARAM_NAMES else "submission")
                if key in req_over:
                    p["required_enhanced_original"] = p.get("required_enhanced"); p["required_enhanced"] = req_over[key]
            l2s.append(x)
        for add in additions:
            if add["parent_l1"] == nb["id"]:
                a = copy.deepcopy(add); a.pop("parent_l1", None)
                for p in a["parameters"]:
                    p.setdefault("scope", "submission"); p.setdefault("check_type", "mechanical"); p.setdefault("required_enhanced", True)
                a["added_by_overlay"] = True
                l2s.append(a)
        nb["l2"] = l2s
        bins.append(nb)

    # apply corrections (free-text fixes recorded alongside the parameter they touch)
    for c in corrections:
        for b in bins:
            for x in b["l2"]:
                if x["id"] == c["id"]:
                    x.setdefault("corrections", []).append(c)

    l2_count = sum(len(b["l2"]) for b in bins)
    params = [p for b in bins for x in b["l2"] for p in x["parameters"]]
    profile = {
        "version": "3.0",
        "source_hierarchy": str(HIERARCHY),
        "overlay": str(overlay_path.resolve()) if overlay_path.exists() else None,
        "scope": hierarchy["scope"],
        "entity_types": hierarchy["conventions"]["entity_types"],
        "anchors": hierarchy["anchors"],
        "rules": overlay.get("rules", []),
        "recognition": overlay.get("recognition_snapshot", []),
        "conventions": overlay.get("_provenance", {}),
        "counts": {
            "l1": len(bins), "l2": l2_count, "parameters": len(params),
            "submission_scope": sum(p["scope"] == "submission" for p in params),
            "dhf_scope": sum(p["scope"] == "dhf" for p in params),
            "l2_by_importance": {k: sum(x["importance"] == k for b in bins for x in b["l2"]) for k in (1, 2, 3)},
        },
        "bins": bins,
    }
    return profile


def summary(profile: dict) -> str:
    lines = [f"profile v{profile['version']}: {profile['counts']}"]
    for b in profile["bins"]:
        lines.append(f"{b['id']} {b['title']}")
        for x in b["l2"]:
            sub = sum(p["scope"] == "submission" for p in x["parameters"])
            tag = " +added" if x.get("added_by_overlay") else (" merged<-" + ",".join(x["merged_from"]) if x.get("merged_from") else "")
            lines.append(f"   {x['id']} [imp{x['importance']}] {x['title'][:70]} ({sub} submission / {len(x['parameters'])-sub} dhf){tag}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["build", "show"])
    ap.add_argument("--overlay", type=Path, default=DEFAULT_OVERLAY)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    a = ap.parse_args()
    if a.command == "build":
        profile = build(a.overlay)
        a.out.write_text(json.dumps(profile, indent=1, ensure_ascii=False) + "\n")
        print(f"wrote {a.out}: {profile['counts']}")
    else:
        print(summary(load(a.out)))


if __name__ == "__main__":
    main()
