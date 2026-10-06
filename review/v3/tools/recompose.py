"""Recompose a decomposed software module: presence per bin, parameter gaps, rules, consistency chains,
anchor agreement and the independent-pass diff. Produces report/report.html, report.json and gaps.json.

Chain ids follow standards-axis/CONSISTENCY-CHAINS.md. Only the mechanical parts are computed here; a
judgment element is reported as a candidate for the reviewer, never as a conclusion.
"""
from __future__ import annotations

import html
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

SEV_RANK = {"S3": 3, "S2": 2, "S1": 1, "info": 0}
CHAIN_TITLES = {
    "CC-01": "Requirement → test case → passing result at the proposed build",
    "CC-02": "Hazard → risk control → implementation → effectiveness",
    "CC-03": "SOUP → version → anomaly-list review → risk",
    "CC-04": "Threat → security control → security test → finding disposition",
    "CC-05": "Single version identity across the module",
    "CC-06": "Anomaly list = release candidate; anomaly sets agree",
    "CC-07": "Declaration of conformity edition, recognition and extent",
    "CC-11": "SBOM ↔ SOUP ↔ configuration ↔ tested OTS versions",
    "CC-12": "Date ordering",
    "CC-13": "Known vulnerabilities ↔ SBOM ↔ KEV ↔ disposition",
    "CC-22": "Report counts reconcile with records",
    "CC-23": "Tester independence for decisive evidence (candidates)",
    "CC-26": "Security acceptance threshold vs residual scores",
    "CC-27": "Unresolved anomaly to risk file closure",
    "CC-28": "Software safety class vs Documentation Level",
}
NOT_IMPLEMENTED = ["CC-08", "CC-09", "CC-10", "CC-14", "CC-15", "CC-16", "CC-17", "CC-18", "CC-19", "CC-20", "CC-21", "CC-24", "CC-25", "CC-12 rows h/i/m/n/o/t/v"]


# ----------------------------------------------------------------------------- helpers

def vnorm(v) -> str:
    s = str(v or "").strip().lower()
    s = re.sub(r"^(v|version|ver\.?)\s*", "", s)
    s = re.sub(r"\b(lts|csv|edition|ed\.?)\b", "", s)
    return re.sub(r"[\s()]+", "", s)


def idnorm(v) -> str:
    return re.sub(r"\s+", " ", str(v or "")).strip().lower()


def to_date(v):
    if not v:
        return None
    s = str(v).strip()
    m = re.match(r"(\d{4})-(\d{2})(?:-(\d{2}))?", s)
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3) or 1))
    except ValueError:
        return None


def aslist(v):
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    return [x.strip() for x in re.split(r"[;,]\s*", str(v)) if x.strip()]


def ints_in(s):
    return [int(x) for x in re.findall(r"\d+", str(s or ""))]


class Ctx:
    def __init__(self, prof, reg):
        self.prof, self.reg = prof, reg
        self.l2map = {x["id"]: x for b in prof["bins"] for x in b["l2"]}
        self.l1_of = {x["id"]: b["id"] for b in prof["bins"] for x in b["l2"]}
        self.l1map = {b["id"]: b for b in prof["bins"]}
        self.ents = list(reg["entities"].values())
        self.by_l2 = defaultdict(list)
        for e in self.ents:
            for l2 in e["l2"]:
                self.by_l2[l2].append(e)
        self.by_type_id = {(e["entity_type"], idnorm(e["id"])): e for e in self.ents}
        self.by_id = defaultdict(list)
        for e in self.ents:
            self.by_id[idnorm(e["id"])].append(e)
            for a in e.get("alias_ids", []):
                if idnorm(a) != idnorm(e["id"]):
                    self.by_id[idnorm(a)].append(e)
        self.findings = []
        self.candidate_items = 0
        self.chain_stats = defaultdict(lambda: {"checks": 0, "breaks": 0, "unknown": 0})
        self._n = 0

    # anchors
    def anchor(self, name, field=None):
        """Resolved anchor value. Structured anchors return a dict (or one field when `field` is given);
        list anchors return the union list; scalars return the string."""
        a = self.reg["anchors"].get(name) or {}
        v = a.get("value")
        if field is not None:
            return v.get(field) if isinstance(v, dict) else None
        return v

    def anchor_date(self, name, field=None):
        return to_date(self.anchor(name, field))

    # entities
    def l2(self, l2id):
        return self.by_l2.get(l2id, [])

    def find(self, id_, entity_type=None):
        key = idnorm(id_)
        if entity_type and (entity_type, key) in self.by_type_id:
            return self.by_type_id[(entity_type, key)]
        cands = self.by_id.get(key, [])
        return cands[0] if cands else None

    def find_in_l2(self, l2id, param, value):
        for e in self.l2(l2id):
            if idnorm(e["params"].get(param)) == idnorm(value) or idnorm(e["id"]) == idnorm(value):
                return e
        return None

    def find_hazard(self, id_):
        key = idnorm(id_)
        for h in self.l2("L2-04.03"):
            if key in (idnorm(h["id"]), idnorm(self.p(h, "hazard_id")), idnorm(self.p(h, "hazardous_situation_id"))):
                return h
        return None

    def p(self, e, name, default=None):
        return (e or {}).get("params", {}).get(name, default)

    def ev(self, e, limit=1):
        if not e:
            return []
        return [{"entity": e["key"], "doc_id": q["doc_id"], "page": q.get("page"), "quote": q["quote"][:300]} for q in e["quotes"][:limit]]

    def add(self, kind, ref, severity, message, l2=(), evidence=None, status="break", chain=None):
        self._n += 1
        f = {"id": f"F-{self._n:04d}", "kind": kind, "ref": ref, "severity": severity, "status": status, "message": message,
             "l2": sorted(set(l2)), "l1": sorted({self.l1_of.get(x, "?") for x in l2}), "evidence": evidence or []}
        self.findings.append(f)
        if chain:
            self.chain_stats[chain]["breaks" if status == "break" else "unknown"] += 1
        return f

    def check(self, chain):
        self.chain_stats[chain]["checks"] += 1

    def bridged_versions(self):
        out = set()
        for x in self.l2("L2-10.04"):
            if aslist(self.p(x, "differences_listed")):
                out.add(vnorm(self.p(x, "last_fully_tested_version")))
        for x in self.l2("L2-09.06"):
            if self.p(x, "regression_analysis_id"):
                out.add(vnorm(self.p(x, "fixed_in_version")))
        return {v for v in out if v}

    def bridged_builds(self):
        bv = self.bridged_versions()
        out = set()
        for x in self.l2("L2-10.01"):
            if vnorm(self.p(x, "version")) in bv and self.p(x, "build_id"):
                out.add(idnorm(self.p(x, "build_id")))
        return out

    def build_ok(self, build, version=None):
        """True if build equals the release build, or the build/version is bridged."""
        rb = idnorm(self.anchor("A.release_build_id"))
        if build and rb and idnorm(build) == rb:
            return True
        if build and idnorm(build) in self.bridged_builds():
            return True
        if version and vnorm(version) in self.bridged_versions():
            return True
        if not build and version and vnorm(version) == vnorm(self.anchor("A.proposed_version")):
            return True
        return False


# ----------------------------------------------------------------------------- presence and parameters

def presence(ctx: Ctx):
    rows = {}
    docs_by_l1 = defaultdict(list)
    for d in ctx.reg["documents"].values():
        for l1 in d["l1"]:
            docs_by_l1[l1].append(d["doc_id"])
    for b in ctx.prof["bins"]:
        for x in b["l2"]:
            ents = ctx.l2(x["id"])
            req_sub = [p["name"] for p in x["parameters"] if p["scope"] == "submission" and p.get("required_enhanced")]
            req_dhf = [p["name"] for p in x["parameters"] if p["scope"] != "submission"]
            filled = missing = 0
            miss_counter, dhf_missing = Counter(), Counter()
            for e in ents:
                for name in req_sub:
                    if e["params"].get(name) in (None, "", []):
                        missing += 1; miss_counter[name] += 1
                    else:
                        filled += 1
                for name in req_dhf:
                    if e["params"].get(name) in (None, "", []):
                        dhf_missing[name] += 1
            fill = filled / (filled + missing) if (filled + missing) else (1.0 if ents else 0.0)
            has_doc = bool(docs_by_l1.get(b["id"]))
            cov = ctx.reg.get("coverage", {}).get(x["id"], {})
            searched = sorted(cov)
            searched_not_found = sorted(d for d, c in cov.items() if c.get("searched") and not c.get("found"))
            if ents:
                status = "complete" if fill >= 0.9 else "partial"
            elif has_doc:
                status = "unclear"
            else:
                status = "absent"
            support = 0 if not ents and not has_doc else 1 if (not ents or fill < 0.5) else 2 if fill < 0.9 else 3
            conf = Counter(e.get("confidence_level", "single") for e in ents)
            rows[x["id"]] = {"l2": x["id"], "l1": b["id"], "title": x["title"], "importance": x["importance"], "entities": len(ents),
                             "fill_rate": round(fill, 2), "status": status, "support": support, "docs": sorted({d for e in ents for d in e["docs"]}),
                             "confidence": dict(conf), "searched_docs": searched, "searched_not_found": searched_not_found,
                             "absence_basis": ("searched" if (not ents and searched_not_found) else "no document routed" if not ents else ""),
                             "missing_submission_params": dict(miss_counter.most_common()), "missing_dhf_params": dict(dhf_missing.most_common()),
                             "findings": [], "priority": None}
            if ents and miss_counter:
                top = ", ".join(f"{k} ({v}/{len(ents)})" for k, v in miss_counter.most_common(4))
                sev = "S2" if any(k in {"build_id_under_test", "software_version_under_test", "execution_end_date", "execution_start_date", "result",
                                        "described_build_id", "sbom_generation_date", "build_tested", "test_date_range", "list_build_id",
                                        "fda_recognition_number", "standard_designation_and_edition", "version_patch_designation", "component_version"}
                                  for k in miss_counter) else "S1"
                ctx.add("param", x["id"], sev, f"{x['id']}: submission-scope parameters not stated for some entities: {top}", [x["id"]],
                        ctx.ev(ents[0]))
    return rows


# ----------------------------------------------------------------------------- rules from profile

def run_rules(ctx: Ctx):
    for r in ctx.prof.get("rules", []):
        l2, param, op = r["l2"], r["param"], r["op"]
        for e in ctx.l2(l2):
            v = ctx.p(e, param)
            sev = r.get("severity", "S2")
            msg = None
            if op == "nonempty" and v in (None, "", []):
                msg = f"{param} not stated"
            elif op == "eq_anchor" and v not in (None, "") and ctx.anchor(r["anchor"]) and (vnorm(v) != vnorm(ctx.anchor(r["anchor"])) and idnorm(v) != idnorm(ctx.anchor(r["anchor"]))):
                if not (r.get("allow_bridged") and ctx.build_ok(v, v)):
                    msg = f"{param}={v!r} differs from {r['anchor']}={ctx.anchor(r['anchor'])!r}"
            elif op in ("before_anchor", "after_anchor") and v:
                d, a = to_date(v), ctx.anchor_date(r["anchor"])
                if d and a and ((op == "before_anchor" and d > a) or (op == "after_anchor" and d < a)):
                    msg = f"{param}={v} is not {op.replace('_', ' ')} {r['anchor']}={a}"
            elif op == "enum_in" and v not in (None, "") and str(v).lower() not in [s.lower() for s in r["values"]]:
                msg = f"{param}={v!r} not in {r['values']}"
            elif op == "exists_in" and v not in (None, "", []):
                missing = [i for i in aslist(v) if not ctx.find_in_l2(r["target_l2"], r["target_param"], i) and not ctx.find(i)]
                if missing:
                    msg = f"{param} references ids not found in {r['target_l2']}: {missing}"
            if msg:
                ctx.add("rule", r["id"], sev, f"{r['id']} {e['entity_type']} {e['id']}: {msg}. {r.get('why','')}".strip(), [l2], ctx.ev(e))


# ----------------------------------------------------------------------------- chains

def latest_runs(ctx: Ctx):
    """Map test_case_id -> list of run entities (L2-09.05 + L2-09.03) sorted by end date (unknown first)."""
    runs = defaultdict(list)
    for l2 in ("L2-09.05", "L2-09.03"):
        for r in ctx.l2(l2):
            tc = ctx.p(r, "test_case_id")
            if tc:
                runs[idnorm(tc)].append(r)
    for k in runs:
        runs[k].sort(key=lambda r: (to_date(ctx.p(r, "execution_end_date")) or date.min, r["id"]))
    return runs


def cc01(ctx: Ctx):
    C = "CC-01"
    runs = latest_runs(ctx)
    tcs = ctx.l2("L2-09.02")
    tc_by_req = defaultdict(list)
    for tc in tcs:
        for rid in aslist(ctx.p(tc, "requirement_or_design_ids")):
            tc_by_req[idnorm(rid)].append(tc)
    for req in ctx.l2("L2-05.02"):
        rid = idnorm(ctx.p(req, "requirement_id") or req["id"])
        method = str(ctx.p(req, "verification_method") or "test").lower()
        if method not in ("test", "testing", "verification test", "unknown", ""):
            continue
        critical = bool(ctx.p(req, "criticality_flag")) or bool(ctx.p(req, "safety_or_security_related"))
        sev = "S3" if critical else "S2"
        ctx.check(C)
        cases = list(tc_by_req.get(rid, [])) + [ctx.find(t, "test_case") for t in aslist(ctx.p(req, "verifying_test_ids")) if ctx.find(t, "test_case")]
        cases = {c["key"]: c for c in cases if c}.values()
        if not cases:
            ctx.add("chain", C, sev, f"CC-01 requirement {req['id']} has no test case (verification_method={method})", ["L2-05.02", "L2-09.02"], ctx.ev(req), chain=C)
            continue
        passing_on_release = False
        reasons = []
        for tc in cases:
            tcid = idnorm(ctx.p(tc, "test_case_id") or tc["id"])
            rs = runs.get(tcid, [])
            if not rs:
                reasons.append(f"{tc['id']}: no executed run"); continue
            last = rs[-1]
            res = str(ctx.p(last, "result") or "").lower()
            if res != "pass":
                reasons.append(f"{tc['id']}: latest run {last['id']} result={res or 'unstated'}"); continue
            b, v = ctx.p(last, "build_id_under_test"), ctx.p(last, "software_version_under_test")
            if not ctx.build_ok(b, v):
                reasons.append(f"{tc['id']}: passing run {last['id']} on build {b or '?'} / version {v or '?'} not the release build {ctx.anchor('A.release_build_id')} and not bridged"); continue
            chg = to_date(ctx.p(req, "requirement_version_or_change_date")); end = to_date(ctx.p(last, "execution_end_date"))
            if chg and end and end < chg:
                reasons.append(f"{tc['id']}: run {last['id']} ended {end} before requirement change {chg}"); continue
            passing_on_release = True
        if not passing_on_release:
            ctx.add("chain", C, sev, f"CC-01 requirement {req['id']}: no passing run at the proposed build. " + "; ".join(reasons), ["L2-05.02", "L2-09.05"], ctx.ev(req), chain=C)


def cc02(ctx: Ctx):
    C = "CC-02"
    runs = latest_runs(ctx)
    controls = ctx.l2("L2-04.05")
    hazards = ctx.l2("L2-04.03")
    covered_hazards = set()
    for c in controls:
        ctx.check(C)
        cid = ctx.p(c, "risk_control_id") or c["id"]
        for h in aslist(ctx.p(c, "hazard_ids")) + aslist(ctx.p(c, "hazardous_situation_ids")):
            covered_hazards.add(idnorm(h))
        reqs = aslist(ctx.p(c, "implementing_requirement_ids"))
        if not reqs:
            ctx.add("chain", C, "S2", f"CC-02 risk control {cid} traces to no SRS requirement", ["L2-04.05", "L2-05.02"], ctx.ev(c), chain=C)
        else:
            missing = [r for r in reqs if not ctx.find(r, "requirement")]
            if missing:
                ctx.add("chain", C, "S2", f"CC-02 risk control {cid} cites requirements not found in the SRS: {missing}", ["L2-04.05", "L2-05.02"], ctx.ev(c), chain=C)
        tests = aslist(ctx.p(c, "implementation_verification_test_ids"))
        if not tests:
            ctx.add("chain", C, "S3", f"CC-02 risk control {cid} has no implementation verification test", ["L2-04.05", "L2-09.02"], ctx.ev(c), chain=C)
        else:
            bad = []
            for t in tests:
                rs = runs.get(idnorm(t), [])
                last = rs[-1] if rs else None
                if not last:
                    bad.append(f"{t}: no run")
                elif str(ctx.p(last, "result") or "").lower() != "pass":
                    bad.append(f"{t}: latest result {ctx.p(last, 'result')}")
                elif not ctx.build_ok(ctx.p(last, "build_id_under_test"), ctx.p(last, "software_version_under_test")):
                    bad.append(f"{t}: passed on build {ctx.p(last, 'build_id_under_test')} not the release build")
            if bad:
                ctx.add("chain", C, "S3", f"CC-02 risk control {cid}: implementation tests without a passing run at the proposed build: " + "; ".join(bad), ["L2-04.05", "L2-09.05"], ctx.ev(c), chain=C)
        eff = ctx.p(c, "effectiveness_verification_ref")
        if not eff:
            ctx.add("chain", C, "S3", f"CC-02 risk control {cid} has no effectiveness verification evidence (ISO 14971 7.2 distinguishes implementation from effectiveness)", ["L2-04.05"], ctx.ev(c), chain=C)
        elif any(idnorm(eff) == idnorm(t) for t in tests):
            ctx.add("chain", C, "S2", f"CC-02 risk control {cid}: effectiveness evidence is the same record as the implementation test ({eff}); 14971 7.2 Note 3 rationale needed", ["L2-04.05"], ctx.ev(c), status="candidate", chain=C)
        if str(ctx.p(c, "control_type") or "").lower().startswith("information") and not ctx.p(c, "information_for_safety_label_ref"):
            ctx.add("chain", C, "S2", f"CC-02 information-for-safety control {cid} has no labeling reference", ["L2-04.05", "L2-29.04"], ctx.ev(c), chain=C)
    for h in hazards:
        hid = idnorm(ctx.p(h, "hazardous_situation_id") or ctx.p(h, "hazard_id") or h["id"])
        hid2 = idnorm(ctx.p(h, "hazard_id") or "")
        ctx.check(C)
        if hid not in covered_hazards and hid2 not in covered_hazards and not any(idnorm(x) in covered_hazards for x in [h["id"]]):
            ctx.add("chain", C, "S2", f"CC-02 hazard/hazardous situation {h['id']} has no risk control traced to it", ["L2-04.03", "L2-04.05"], ctx.ev(h), status="candidate", chain=C)


def name_match(a, b) -> bool:
    a, b = idnorm(a), idnorm(b)
    if not a or not b:
        return False
    a1, b1 = re.sub(r"[^a-z0-9]", "", a), re.sub(r"[^a-z0-9]", "", b)
    return a1 == b1 or a1 in b1 or b1 in a1


def sbom_entry_for(ctx: Ctx, name):
    if not name:
        return None
    n = idnorm(name)
    for s in ctx.l2("L2-16.02"):
        if n in {idnorm(x) for x in s.get("alias_ids", [])} or n == idnorm(ctx.p(s, "unique_identifier")):
            return s
    for s in ctx.l2("L2-16.02"):
        if name_match(ctx.p(s, "component_name") or s["id"], name) or name_match(s["id"], name):
            return s
    return None


def cc03(ctx: Ctx):
    C = "CC-03"
    for soup in ctx.l2("L2-12.01"):
        if not ctx.p(soup, "version_patch_designation") and not ctx.p(soup, "soup_id"):
            continue  # a component mention without the SOUP-list parameters is not a SOUP-list row
        ctx.check(C)
        sid = ctx.p(soup, "soup_id") or soup["id"]
        name = ctx.p(soup, "title") or sid
        ver = ctx.p(soup, "version_patch_designation")
        soup_label = f" ({name})" if idnorm(name) != idnorm(sid) else ""
        s = sbom_entry_for(ctx, name) or sbom_entry_for(ctx, sid)
        if s and ver and vnorm(ctx.p(s, "component_version")) != vnorm(ver):
            ctx.add("chain", C, "S3", f"CC-03 SOUP {sid}{soup_label} version {ver} but SBOM lists {ctx.p(s,'component_version')}", ["L2-12.01", "L2-16.02"], ctx.ev(soup) + ctx.ev(s), chain=C)
        cfg = next((c for c in ctx.l2("L2-03.03") if name_match(ctx.p(c, "configuration_item_id") or c["id"], name) or name_match(c["id"], sid)), None)
        if cfg and ver and ctx.p(cfg, "item_version") and vnorm(ctx.p(cfg, "item_version")) != vnorm(ver):
            ctx.add("chain", C, "S3", f"CC-03 SOUP {sid}{soup_label} version {ver} but configuration item lists {ctx.p(cfg,'item_version')}", ["L2-12.01", "L2-03.03"], ctx.ev(soup) + ctx.ev(cfg), chain=C)
        alias = {idnorm(x) for x in soup.get("alias_ids", [])} | {idnorm(sid), idnorm(name), idnorm(soup["id"])}
        reviews = [r for r in ctx.l2("L2-12.04") if idnorm(ctx.p(r, "soup_id") or r["id"]) in alias or idnorm(r["id"]) in alias or name_match(ctx.p(r, "soup_id") or r["id"], name)]
        if soup.get("_cc03_done"):
            continue
        soup["_cc03_done"] = True
        if not reviews:
            ctx.add("chain", C, "S3", f"CC-03 SOUP {sid}{soup_label}: no published-anomaly-list review (IEC 62304 7.1.3)", ["L2-12.01", "L2-12.04"], ctx.ev(soup), chain=C)
        for r in reviews:
            scope = ctx.p(r, "anomaly_list_version_scope")
            if scope and ver and vnorm(scope) != vnorm(ver):
                ctx.add("chain", C, "S3", f"CC-03 SOUP {sid}{soup_label}: anomaly review covers version {scope}, SOUP in use is {ver}", ["L2-12.04"], ctx.ev(r), chain=C)
            rd, rel = to_date(ctx.p(r, "review_date")), to_date(ctx.p(soup, "release_date"))
            if rd and rel and rd < rel:
                ctx.add("chain", "CC-12", "S1", f"CC-12p SOUP {sid}: anomaly review dated {rd} precedes the SOUP version release/adoption {rel}; IEC 62304 7.1.3 requires version relevance, so this is an age note only", ["L2-12.04"], ctx.ev(r), chain="CC-12")
            for a in aslist(ctx.p(r, "hazard_relevant_anomalies")):
                pass
        for link in [x for x in ctx.l2("L2-12.05") if idnorm(ctx.p(x, "soup_id") or x["id"]) == idnorm(sid)]:
            missing = [h for h in aslist(ctx.p(link, "linked_hazard_ids")) if not ctx.find_hazard(h)]
            if missing:
                ctx.add("chain", C, "S2", f"CC-03 SOUP {sid}{soup_label} risk link cites hazards not in the risk file: {missing}", ["L2-12.05", "L2-04.03"], ctx.ev(link), chain=C)


def security_controls(ctx: Ctx):
    out = {}
    for l2 in ctx.l2map:
        if l2.startswith("L2-21."):
            for c in ctx.l2(l2):
                cid = ctx.p(c, "control_id") or c["id"]
                if c["entity_type"] != "security_control" or "+" in str(cid) or re.match(r"^SEC-", str(cid), re.I):
                    continue
                out[idnorm(cid)] = c
    return out


def security_tests(ctx: Ctx):
    out = {}
    for l2 in ("L2-23.01", "L2-23.02", "L2-23.03", "L2-23.04"):
        for t in ctx.l2(l2):
            out[idnorm(ctx.p(t, "test_activity_id") or t["id"])] = (l2, t)
    return out


def cc04(ctx: Ctx):
    C = "CC-04"
    controls = security_controls(ctx)
    tests = security_tests(ctx)
    findings = {idnorm(ctx.p(f, "finding_id") or f["id"]): f for f in ctx.l2("L2-23.06")}
    for th in ctx.l2("L2-14.04"):
        ctx.check(C)
        tid = ctx.p(th, "threat_id") or th["id"]
        mits = aslist(ctx.p(th, "mitigating_control_ids"))
        if not mits:
            ctx.add("chain", C, "S3", f"CC-04 threat {tid} has no mitigating control and no accepted rationale recorded", ["L2-14.04", "L2-21.01"], ctx.ev(th), chain=C)
        missing = [m for m in mits if idnorm(m) not in controls and not ctx.find(m)]
        if missing:
            ctx.add("chain", C, "S3", f"CC-04 threat {tid} cites controls not found in the security architecture: {missing}", ["L2-14.04", "L2-21.01"], ctx.ev(th), chain=C)
        mt = aslist(ctx.p(th, "threat_mitigation_test_ids"))
        if not mt:
            ctx.add("chain", C, "S2", f"CC-04 threat {tid} has no threat-mitigation (effectiveness) test", ["L2-14.04", "L2-23.02"], ctx.ev(th), chain=C)
    for cid, c in controls.items():
        ctx.check(C)
        vt = aslist(ctx.p(c, "verification_test_ids"))
        if not vt and not ctx.p(c, "not_applicable_rationale"):
            ctx.add("chain", C, "S3", f"CC-04 security control {c['id']} has no verification test", [c["l2"][0], "L2-23.01"], ctx.ev(c), chain=C)
        for t in vt:
            if idnorm(t) not in tests and not ctx.find(t):
                ctx.add("chain", C, "S2", f"CC-04 security control {c['id']} cites test {t} not found among security test activities", [c["l2"][0], "L2-23.01"], ctx.ev(c), chain=C)
    for key, (l2, t) in tests.items():
        ctx.check(C)
        b, v = ctx.p(t, "build_tested"), ctx.p(t, "software_version_tested")
        if (b or v) and not ctx.build_ok(b, v):
            ctx.add("chain", C, "S3", f"CC-04/CC-12f security test {t['id']} ({l2}) ran on build {b or '?'} / version {v or '?'}, not the release build {ctx.anchor('A.release_build_id')} and not bridged", [l2, "L2-10.04"], ctx.ev(t), chain=C)
        for f in aslist(ctx.p(t, "findings_ids")):
            fe = findings.get(idnorm(f))
            if not fe:
                ctx.add("chain", C, "S2", f"CC-04 finding {f} from {t['id']} has no disposition record", [l2, "L2-23.06"], ctx.ev(t), chain=C)
            elif str(ctx.p(fe, "disposition") or "").lower() == "fixed" and not ctx.p(fe, "fixed_in_build"):
                ctx.add("chain", C, "S2", f"CC-04 finding {f} marked fixed without fixed_in_build / retest", ["L2-23.06"], ctx.ev(fe), chain=C)


def cc05(ctx: Ctx):
    C = "CC-05"
    pv, rb = ctx.anchor("A.proposed_version"), ctx.anchor("A.release_build_id")
    for name, a in ctx.reg["anchors"].items():
        if a.get("conflict"):
            ctx.check(C)
            ctx.add("anchor", C, "S3" if name in ("A.proposed_version", "A.release_build_id", "A.sbom_build", "A.labeled_version") else "S2",
                    f"CC-05 anchor {name} stated inconsistently: {a['value']!r} vs {a['alternatives']}", [], [{"entity": name, "doc_id": c["doc_id"], "quote": c["quote"][:200]} for c in a["claims"][:6]], chain=C)
    # anchors that must agree with the proposed version / release build: (anchor, field or None, kind, severity)
    for name, field, kind, sev in (("A.labeled_version", None, "version", "S3"), ("A.sbom_build", "build", "build", "S3"),
                                   ("A.sbom_build", "version", "version", "S3"), ("A.configuration_set", "build", "build", "S2"),
                                   ("A.risk_file_version", "covers", "version", "S2"), ("A.threat_model_version", "covers", "version", "S2")):
        v = ctx.anchor(name, field)
        if v in (None, ""):
            continue
        ctx.check(C)
        ok = (vnorm(v) == vnorm(pv)) if kind == "version" else (idnorm(v) == idnorm(rb))
        if not ok and not ctx.build_ok(v if kind == "build" else None, v if kind == "version" else None):
            label = name + (f".{field}" if field else "")
            ctx.add("anchor", C, sev, f"CC-05 anchor {label}={v!r} differs from {'A.proposed_version='+repr(pv) if kind=='version' else 'A.release_build_id='+repr(rb)}", [],
                    [{"entity": name, "doc_id": c["doc_id"], "quote": c["quote"][:200]} for c in (ctx.reg["anchors"].get(name) or {}).get("claims", [])
                     if not isinstance(c["value"], dict) or field is None or c["value"].get(field) not in (None, "")][:3], chain=C)
    checks = [("L2-02.03", "final_release_version_stated", "version", "S2"), ("L2-10.04", "final_entry_version", "version", "S2"),
              ("L2-09.08", "summary_software_version_tested", "version", "S3"), ("L2-09.07", "report_software_version", "version", "S3"),
              ("L2-16.01", "described_software_version", "version", "S3"), ("L2-16.01", "described_build_id", "build", "S3"),
              ("L2-24.05", "labeled_sbom_version", "version", "S3"), ("L2-29.01", "labeled_version", "version", "S3"),
              ("L2-11.03", "list_software_version", "version", "S3"), ("L2-11.03", "list_build_id", "build", "S3"),
              ("L2-04.08", "software_version_covered", "version", "S3"), ("L2-13.02", "software_version_covered", "version", "S3"),
              ("L2-14.01", "configuration_covered", "version", "S2"), ("L2-28.04", "software_version_covered_by_doc", "version", "S2")]
    for l2, param, kind, sev in checks:
        for e in ctx.l2(l2):
            v = ctx.p(e, param)
            if v in (None, ""):
                continue
            ctx.check(C)
            ok = (vnorm(v) == vnorm(pv)) if kind == "version" else (idnorm(v) == idnorm(rb))
            if not ok and not ctx.build_ok(v if kind == "build" else None, v if kind == "version" else None):
                ctx.add("chain", C, sev, f"CC-05 {l2} {e['entity_type']} {e['id']}: {param}={v!r} differs from {'A.proposed_version='+repr(pv) if kind=='version' else 'A.release_build_id='+repr(rb)} and is not bridged in L2-10.04", [l2, "L2-03.01"], ctx.ev(e), chain=C)
    for d in ctx.reg["documents"].values():
        v = d["params"].get("software_version_covered")
        if v and pv and vnorm(v) != vnorm(pv):
            ctx.check(C)
            ctx.add("chain", C, "S2", f"CC-05 document {d['doc_id']} states software_version_covered={v!r}, proposed is {pv!r}", d["l1"] and [x["id"] for b in ctx.prof["bins"] if b["id"] in d["l1"] for x in b["l2"][:1]] or [], [{"entity": d["doc_id"], "doc_id": d["doc_id"], "quote": (d["quotes"] or [""])[0][:200]}], chain=C)


def cc06(ctx: Ctx):
    C = "CC-06"
    list_docs = {d for lst in ctx.l2("L2-11.03") for d in lst["docs"]}
    anomalies = {idnorm(ctx.p(a, "anomaly_id") or a["id"]): a for a in ctx.l2("L2-11.01") if not list_docs or set(a["docs"]) & list_docs}
    rb = ctx.anchor("A.release_build_id")
    runs = latest_runs(ctx)
    all_runs = [r for rs in runs.values() for r in rs]
    last_run_end = max([to_date(ctx.p(r, "execution_end_date")) for r in all_runs if to_date(ctx.p(r, "execution_end_date"))] or [None])
    for lst in ctx.l2("L2-11.03"):
        ctx.check(C)
        lb = ctx.p(lst, "list_build_id")
        if lb and rb and idnorm(lb) != idnorm(rb):
            ctx.add("chain", C, "S3", f"CC-06 unresolved-anomaly list describes build {lb}, release build is {rb}", ["L2-11.03", "L2-03.02"], ctx.ev(lst), chain=C)
        xd = to_date(ctx.p(lst, "extraction_date"))
        if xd and last_run_end and xd < last_run_end:
            ctx.add("chain", C, "S2", f"CC-06 anomaly list extracted {xd}, before the last test run ended {last_run_end}", ["L2-11.03", "L2-09.05"], ctx.ev(lst), chain=C)
        sd = ctx.anchor_date("A.module_submission_date")
        if xd and sd and xd > sd:
            ctx.add("chain", C, "S2", f"CC-06 anomaly list extracted {xd}, after the module submission date {sd}", ["L2-11.03"], ctx.ev(lst), chain=C)
        stated = sum(ints_in(ctx.p(lst, "open_count_by_severity")))
        if stated and anomalies and stated != len(anomalies):
            ctx.add("chain", "CC-22", "S2", f"CC-22 anomaly list states {stated} open anomalies; {len(anomalies)} anomaly records were extracted", ["L2-11.03", "L2-11.01"], ctx.ev(lst), chain="CC-22")
    for rep in ctx.l2("L2-09.07"):
        for d in aslist(ctx.p(rep, "deferred_anomaly_ids")):
            ctx.check(C)
            if idnorm(d) not in anomalies:
                ctx.add("chain", C, "S3", f"CC-06 test report {rep['id']} defers anomaly {d} which is not on the unresolved-anomaly list", ["L2-09.07", "L2-11.01"], ctx.ev(rep), chain=C)
    retested = {idnorm(ctx.p(r, "retest_of_run_id")) for r in all_runs if ctx.p(r, "retest_of_run_id") and str(ctx.p(r, "result") or "").lower() == "pass"}
    for r in all_runs:
        if str(ctx.p(r, "result") or "").lower() in ("fail", "failed"):
            ctx.check(C)
            raised = aslist(ctx.p(r, "anomaly_ids_raised"))
            if idnorm(r["id"]) in retested:
                continue
            if not raised:
                ctx.add("chain", C, "S3", f"CC-06 failed run {r['id']} raised no anomaly and has no passing retest", ["L2-09.05", "L2-11.01"], ctx.ev(r), chain=C)
            else:
                missing = [a for a in raised if idnorm(a) not in anomalies]
                if missing:
                    ctx.add("chain", C, "S3", f"CC-06 failed run {r['id']} raised {missing}, not on the unresolved list and no passing retest", ["L2-09.05", "L2-11.01"], ctx.ev(r), chain=C)
    sec = {idnorm(ctx.p(a, "anomaly_id") or a["id"]) for a in ctx.l2("L2-18.01")}
    if sec or ctx.l2("L2-18.01"):
        ctx.check(C)
        left = sorted(set(anomalies) - sec)
        if left:
            ctx.add("chain", C, "S3", f"CC-06 unresolved anomalies without a security assessment (FDA-CY V.A.5 applies to the whole list): {left}", ["L2-11.01", "L2-18.01"], [], chain=C)
    else:
        for a in anomalies.values():
            if ctx.p(a, "security_impact_assessed") is False:
                ctx.check(C)
                ctx.add("chain", C, "S2", f"CC-06 anomaly {a['id']}: security impact not assessed", ["L2-11.01"], ctx.ev(a), chain=C)


def cc07(ctx: Ctx):
    C = "CC-07"
    snap = ctx.prof.get("recognition", [])
    sd = ctx.anchor_date("A.module_submission_date")
    for d in ctx.l2("L2-28.01"):
        ctx.check(C)
        desig = str(ctx.p(d, "standard_designation_and_edition") or d["id"])
        rn = str(ctx.p(d, "fda_recognition_number") or "").strip()
        match = None
        for s in snap:
            if re.search(s["pattern"], desig, re.I):
                match = s; break
        if not match:
            ctx.add("chain", C, "S2", f"CC-07 declaration {d['id']}: standard {desig!r} not in the recognition snapshot; verify recognition manually", ["L2-28.01", "L2-28.02"], ctx.ev(d), status="unknown", chain=C)
            continue
        if not rn:
            ctx.add("chain", C, "S2", f"CC-07 declaration {d['id']} ({desig}) states no FDA recognition number", ["L2-28.01"], ctx.ev(d), chain=C)
        elif match.get("recognition_number") and rn.replace(" ", "") != match["recognition_number"].replace(" ", ""):
            ctx.add("chain", C, "S3", f"CC-07 declaration {d['id']} cites recognition {rn}; database lists {match['recognition_number']} for {match['standard']}", ["L2-28.01", "L2-28.02"], ctx.ev(d), chain=C)
        if match.get("edition_pattern") and not re.search(match["edition_pattern"], desig, re.I):
            ctx.add("chain", C, "S3", f"CC-07 declaration {d['id']}: edition in {desig!r} is not the recognized edition ({match['recognized_edition']}); the DoC can only be treated as general use", ["L2-28.01", "L2-28.02"], ctx.ev(d), chain=C)
        if match.get("not_recognized"):
            ctx.add("chain", C, "S3", f"CC-07 declaration {d['id']}: {match['standard']} is not FDA-recognized; a DoC cannot replace data", ["L2-28.01"], ctx.ev(d), chain=C)
        exp = to_date(match.get("transition_expiry"))
        if exp and sd and sd > exp:
            ctx.add("chain", C, "S3", f"CC-07 declaration {d['id']}: transition period for {match['standard']} ended {exp}, submission dated {sd}", ["L2-28.01"], ctx.ev(d), chain=C)
        di = to_date(ctx.p(d, "date_of_issue"))
        if di and sd and di > sd:
            ctx.add("chain", "CC-12", "S3", f"CC-12k declaration {d['id']} issued {di}, after the module submission date {sd}", ["L2-28.01"], ctx.ev(d), chain="CC-12")
        for scope in ctx.l2("L2-28.03"):
            if idnorm(scope["id"]) != idnorm(d["id"]) and idnorm(ctx.p(scope, "declaration_id") or "") != idnorm(d["id"]):
                continue
            dev = ctx.p(scope, "deviations_declared")
            if dev and str(dev).lower() not in ("none", "no", "n/a"):
                ctx.add("chain", C, "S2", f"CC-07 declaration {d['id']} declares deviations: {str(dev)[:120]}", ["L2-28.03"], ctx.ev(scope), chain=C)
            if match.get("required_clauses"):
                claimed = " ".join(aslist(ctx.p(scope, "clauses_claimed")))
                missing = [c for c in match["required_clauses"] if not re.search(rf"(^|\D){re.escape(c)}(\D|$)", claimed)]
                if claimed and missing:
                    ctx.add("chain", C, "S3", f"CC-07 declaration {d['id']} to {match['standard']}: claimed clauses omit {missing}, required for the Enhanced DoC route", ["L2-28.03"], ctx.ev(scope), chain=C)


def cc11(ctx: Ctx):
    C = "CC-11"
    sbom = ctx.l2("L2-16.02")
    if not sbom:
        return
    sbom_versions = {(idnorm(ctx.p(s, "component_name") or s["id"]), vnorm(ctx.p(s, "component_version"))) for s in sbom}
    for c in ctx.l2("L2-03.03"):
        t = str(ctx.p(c, "item_type") or "").lower()
        if t and ("soup" in t or "ots" in t or "os" == t or "third" in t):
            ctx.check(C)
            if not (sbom_entry_for(ctx, c["id"]) or sbom_entry_for(ctx, ctx.p(c, "configuration_item_id") or "") or sbom_entry_for(ctx, ctx.p(c, "name") or "")):
                ctx.add("chain", C, "S3", f"CC-11 configuration item {c['id']} ({t}) does not appear in the SBOM", ["L2-03.03", "L2-16.02"], ctx.ev(c), chain=C)
    # reverse direction: every third-party SBOM component needs a SOUP/OTS list row (IEC 62304 7.1 evaluation, 7.1.3 anomaly review)
    soup_rows = [x for x in ctx.l2("L2-12.01") if ctx.p(x, "version_patch_designation") or ctx.p(x, "soup_id")]
    root = next((x for x in sbom if str(ctx.p(x, "dependency_relationship") or "").lower() in ("root", "describes", "primary")), None)
    sponsor = idnorm(ctx.p(root, "supplier_name")) if root else ""

    def soup_row_for(name, uid):
        n, u = idnorm(name), idnorm(uid)
        for x in soup_rows:
            ids = {idnorm(a) for a in x.get("alias_ids", [])} | {idnorm(x["id"]), idnorm(ctx.p(x, "soup_id") or ""), idnorm(ctx.p(x, "title") or "")}
            if (n and n in ids) or (u and u in ids):
                return x
        for x in soup_rows:
            if name_match(ctx.p(x, "title") or x["id"], name) or name_match(x["id"], name):
                return x
        return None
    if soup_rows:
        for x in sbom:
            if x is root:
                continue
            name = ctx.p(x, "component_name") or x["id"]
            if sponsor and idnorm(ctx.p(x, "supplier_name")) == sponsor:
                continue  # the sponsor's own components are not SOUP
            ctx.check(C)
            if not soup_row_for(name, ctx.p(x, "unique_identifier") or ""):
                ctx.add("chain", C, "S2", f"CC-11 SBOM component {name} {ctx.p(x, 'component_version') or ''} has no SOUP/OTS list row: no IEC 62304 7.1 evaluation or 7.1.3 anomaly-list review is shown for it",
                        ["L2-16.02", "L2-12.01"], ctx.ev(x), chain=C)
    agg = defaultdict(list)
    for r in ctx.l2("L2-09.05") + ctx.l2("L2-09.03"):
        for item in aslist(ctx.p(r, "ots_soup_versions_in_test_config")):
            agg[item].append(r)
    for item, rs in agg.items():
        ctx.check(C)
        m = re.match(r"(.+?)\s+v?([\d][\w.\-+]*)$", item)
        name, ver = (m.group(1), m.group(2)) if m else (item, "")
        s = sbom_entry_for(ctx, name)
        if not s:
            ctx.add("chain", C, "S2", f"CC-11 {len(rs)} test run(s) used {item!r}, which is not in the SBOM (e.g. {rs[0]['id']})", ["L2-09.05", "L2-16.02"], ctx.ev(rs[0]), chain=C)
        elif ver and vnorm(ctx.p(s, "component_version")) != vnorm(ver):
            ctx.add("chain", C, "S3", f"CC-11 {len(rs)} test run(s) used {item!r}; the SBOM ships {ctx.p(s,'component_name')} {ctx.p(s,'component_version')} (e.g. {rs[0]['id']})", ["L2-09.05", "L2-16.02"], ctx.ev(rs[0]) + ctx.ev(s), chain=C)


def cc12(ctx: Ctx):
    C = "CC-12"
    cf, rel, sub = ctx.anchor_date("A.code_freeze_date"), ctx.anchor_date("A.release_date"), ctx.anchor_date("A.module_submission_date")
    rb = idnorm(ctx.anchor("A.release_build_id"))
    tcs = {idnorm(ctx.p(t, "test_case_id") or t["id"]): t for t in ctx.l2("L2-09.02")}
    for r in ctx.l2("L2-09.05") + ctx.l2("L2-09.03"):
        st, en = to_date(ctx.p(r, "execution_start_date")), to_date(ctx.p(r, "execution_end_date"))
        tc = tcs.get(idnorm(ctx.p(r, "test_case_id")))
        pa = to_date(ctx.p(tc, "protocol_approval_date")) if tc else None
        ctx.check(C)
        if pa and st and st < pa:
            ctx.add("chain", C, "S2", f"CC-12b run {r['id']} started {st} before its protocol {tc['id']} was approved {pa}", ["L2-09.05", "L2-09.02"], ctx.ev(r) + ctx.ev(tc), chain=C)
        if cf and st and rb and idnorm(ctx.p(r, "build_id_under_test")) == rb and st < cf:
            ctx.add("chain", C, "S3", f"CC-12c release-candidate run {r['id']} started {st} before code freeze {cf}", ["L2-09.05", "L2-03.04"], ctx.ev(r), chain=C)
        if rel and en and en > rel:
            ctx.add("chain", C, "S2", f"CC-12l run {r['id']} ended {en} after the release date {rel} (IEC 62304 5.8.1)", ["L2-09.05", "L2-03.04"], ctx.ev(r), chain=C)
        if sub and en and en > sub:
            ctx.add("chain", C, "S3", f"CC-12k run {r['id']} ended {en} after the module submission date {sub}", ["L2-09.05"], ctx.ev(r), chain=C)
    for s in ctx.l2("L2-16.01"):
        gd = to_date(ctx.p(s, "sbom_generation_date"))
        ctx.check(C)
        if cf and gd and gd < cf:
            ctx.add("chain", C, "S2", f"CC-12c SBOM generated {gd} before code freeze {cf}; it may not describe the frozen baseline (content mismatch is checked by CC-11)", ["L2-16.01", "L2-03.04"], ctx.ev(s), chain=C)
    for b in ctx.l2("L2-03.02"):
        bd = to_date(ctx.p(b, "build_date"))
        if cf and bd and bd < cf:
            ctx.check(C)
            ctx.add("chain", C, "S3", f"CC-12c release build {b['id']} dated {bd} before code freeze {cf}", ["L2-03.02", "L2-03.04"], ctx.ev(b), chain=C)
    pen_end = None
    for t in ctx.l2("L2-23.04"):
        rng = str(ctx.p(t, "test_date_range") or "")
        ds = [to_date(x) for x in re.findall(r"\d{4}-\d{2}(?:-\d{2})?", rng)]
        ds = [d for d in ds if d]
        if ds:
            pen_end = max(ds) if pen_end is None else max(pen_end, max(ds))
            ctx.check(C)
            if cf and idnorm(ctx.p(t, "build_tested")) == rb and max(ds) < cf:
                ctx.add("chain", C, "S3", f"CC-12c penetration test {t['id']} on the release build ended {max(ds)} before code freeze {cf}", ["L2-23.04"], ctx.ev(t), chain=C)
            if sub and max(ds) > sub:
                ctx.add("chain", C, "S3", f"CC-12k penetration test {t['id']} ended {max(ds)} after the submission date {sub}", ["L2-23.04"], ctx.ev(t), chain=C)
    if pen_end:
        for rep in ctx.l2("L2-13.02"):
            rd = to_date(ctx.p(rep, "report_date"))
            ctx.check(C)
            if rd and rd < pen_end:
                ctx.add("chain", C, "S2", f"CC-12e security risk report dated {rd} predates the last penetration test {pen_end}", ["L2-13.02", "L2-23.04"], ctx.ev(rep), chain=C)
    last_disp = [to_date(ctx.p(a, "disposition_date")) for a in ctx.l2("L2-11.01") + ctx.l2("L2-23.06")]
    last_disp = max([d for d in last_disp if d] or [None])
    for rep in ctx.l2("L2-04.08"):
        rd = to_date(ctx.p(rep, "report_date"))
        ctx.check(C)
        if rd and last_disp and rd < last_disp:
            ctx.add("chain", C, "S2", f"CC-12g risk management report dated {rd} predates the last anomaly/finding disposition {last_disp} (ISO 14971 8-9)", ["L2-04.08", "L2-11.01"], ctx.ev(rep), chain=C)
    for d in ctx.l2("L2-28.04"):
        ec, di = to_date(ctx.p(d, "evidence_completion_date")), None
        decl = ctx.find(d["id"], "declaration")
        di = to_date(ctx.p(decl, "date_of_issue")) if decl else None
        if ec and di and di < ec:
            ctx.check(C)
            ctx.add("chain", C, "S2", f"CC-12j declaration {d['id']} issued {di} before its evidence was complete {ec}", ["L2-28.01", "L2-28.04"], ctx.ev(d), chain=C)
    # r: threat model after last security-relevant change
    tm_dates = [to_date(ctx.p(t, "threat_model_date")) for t in ctx.l2("L2-14.01")]
    tm_dates = [d for d in tm_dates if d]
    if tm_dates:
        vdates = {vnorm(ctx.p(v, "version")): to_date(ctx.p(v, "version_date")) for v in ctx.l2("L2-10.01")}
        sec_changes = [(c, vdates.get(vnorm(ctx.p(c, "to_version")))) for c in ctx.l2("L2-10.02") if ctx.p(c, "safety_security_relevant") in (True, "true", "True", "yes")]
        sec_changes = [(c, d) for c, d in sec_changes if d]
        if sec_changes:
            c, d = max(sec_changes, key=lambda x: x[1])
            ctx.check(C)
            if max(tm_dates) < d:
                ctx.add("chain", C, "S2", f"CC-12r threat model dated {max(tm_dates)} predates security-relevant change {c['id']} introduced in version {ctx.p(c,'to_version')} ({d})", ["L2-14.01", "L2-10.02"], ctx.ev(c), chain=C)
    # s: SBOM generated before the vulnerability scan that used it
    sbom_dates = [to_date(ctx.p(x, "sbom_generation_date")) for x in ctx.l2("L2-16.01")]
    sbom_dates = [d for d in sbom_dates if d]
    for v in ctx.l2("L2-17.01"):
        q = str(ctx.p(v, "vulnerability_source_db_and_query_date") or "")
        qd = [to_date(x) for x in re.findall(r"\d{4}-\d{2}(?:-\d{2})?", q)]
        qd = [d for d in qd if d]
        if sbom_dates and qd and max(sbom_dates) > min(qd):
            ctx.check(C)
            ctx.add("chain", C, "S2", f"CC-12s vulnerability scan for {v['id']} dated {min(qd)} predates the SBOM generation {max(sbom_dates)} (FDA-CY V.A.4(b))", ["L2-17.01", "L2-16.01"], ctx.ev(v), chain=C)
            break
    # u: regression analysis after the change analysed and before the regression runs
    vdates_u = {vnorm(ctx.p(v, "version")): to_date(ctx.p(v, "version_date")) for v in ctx.l2("L2-10.01")}
    for ra in ctx.l2("L2-09.06"):
        rad = to_date(ctx.p(ra, "regression_analysis_date"))
        fv = vdates_u.get(vnorm(ctx.p(ra, "fixed_in_version")))
        if rad and fv and rad < fv:
            ctx.check(C)
            ctx.add("chain", C, "S2", f"CC-12u regression analysis {ra['id']} dated {rad} precedes the version it analyses ({ctx.p(ra,'fixed_in_version')}, {fv})", ["L2-09.06", "L2-10.01"], ctx.ev(ra), chain=C)
    # w: anomaly dispositions not later than the list extraction
    for lst in ctx.l2("L2-11.03"):
        xd = to_date(ctx.p(lst, "extraction_date"))
        for a in ctx.l2("L2-11.01"):
            dd = to_date(ctx.p(a, "disposition_date"))
            if xd and dd and dd > xd:
                ctx.check(C)
                ctx.add("chain", C, "S1", f"CC-12w anomaly {a['id']} disposition dated {dd} is later than the list extraction {xd}", ["L2-11.01", "L2-11.03"], ctx.ev(a), chain=C)
    # k: every doc approval before submission
    for d in ctx.reg["documents"].values():
        ad = to_date(d["params"].get("approval_date"))
        if ad and sub and ad > sub:
            ctx.check(C)
            ctx.add("chain", C, "S3", f"CC-12k document {d['doc_id']} approved {ad}, after the module submission date {sub}", [], [{"entity": d["doc_id"], "doc_id": d["doc_id"], "quote": (d["quotes"] or [""])[0][:200]}], chain=C)


def cc13(ctx: Ctx):
    C = "CC-13"
    sbom = ctx.l2("L2-16.02")
    assessed = {idnorm(ctx.p(a, "vulnerability_id") or a["id"]): a for a in ctx.l2("L2-17.02")}
    listed = {idnorm(ctx.p(v, "vulnerability_id") or v["id"]): v for v in ctx.l2("L2-17.01")}
    for vid, v in listed.items():
        ctx.check(C)
        comp = ctx.p(v, "component_ref")
        if comp:
            m = re.match(r"(.+?)\s+v?(\d[\w.\-+]*)$", str(comp).strip())
            cname, cver = (m.group(1), m.group(2)) if m else (comp, "")
            s = sbom_entry_for(ctx, cname)
            if not s:
                ctx.add("chain", C, "S3", f"CC-13 vulnerability {v['id']} is listed against component {comp!r}, which is not in the SBOM", ["L2-17.01", "L2-16.02"], ctx.ev(v), chain=C)
            elif cver and vnorm(ctx.p(s, "component_version")) != vnorm(cver):
                ctx.add("chain", C, "S3", f"CC-13 vulnerability {v['id']} is assessed against {comp!r}; the SBOM ships {ctx.p(s,'component_name')} {ctx.p(s,'component_version')}. The assessment refers to a component version not in the release", ["L2-17.01", "L2-16.02"], ctx.ev(v) + ctx.ev(s), chain=C)
        if vid not in assessed:
            ctx.add("chain", C, "S3", f"CC-13 vulnerability {v['id']} has no assessment/disposition record", ["L2-17.01", "L2-17.02"], ctx.ev(v), chain=C)
        if ctx.p(v, "in_cisa_kev") in (True, "true", "yes"):
            a = assessed.get(vid)
            if not a or str(ctx.p(a, "disposition") or "").lower() in ("", "open", "deferred"):
                ctx.add("chain", C, "S3", f"CC-13 KEV vulnerability {v['id']} present without a closing disposition", ["L2-17.01", "L2-17.04"], ctx.ev(v), chain=C)
    for s in sbom:
        for k in aslist(ctx.p(s, "known_vulnerability_ids")):
            ctx.check(C)
            if idnorm(k) not in assessed and idnorm(k) not in listed:
                ctx.add("chain", C, "S3", f"CC-13 SBOM component {ctx.p(s,'component_name') or s['id']} lists {k}, which is not in the vulnerability assessment", ["L2-16.02", "L2-17.01"], ctx.ev(s), chain=C)
    for k in ctx.l2("L2-17.04"):
        for vid in aslist(ctx.p(k, "kev_vulnerability_ids_present_in_release")):
            ctx.check(C)
            a = assessed.get(idnorm(vid))
            if not a:
                ctx.add("chain", C, "S3", f"CC-13 KEV vulnerability {vid} present in release without individual justification", ["L2-17.04", "L2-17.02"], ctx.ev(k), chain=C)


def cc22(ctx: Ctx):
    C = "CC-22"
    runs = latest_runs(ctx)
    all_runs = [r for rs in runs.values() for r in rs]
    for rep in ctx.l2("L2-09.07"):
        stated = ctx.p(rep, "counts_executed_passed_failed_blocked")
        if not stated:
            continue
        ctx.check(C)
        nums = ints_in(stated)
        m = re.search(r"(\d+)\s*(?:tests?\s*)?pass", str(stated), re.I)
        stated_pass = int(m.group(1)) if m else (nums[1] if len(nums) > 1 else None)
        latest = [rs[-1] for rs in runs.values()]
        recount_pass = sum(str(ctx.p(r, "result") or "").lower() == "pass" for r in latest)
        recount_fail = sum(str(ctx.p(r, "result") or "").lower() in ("fail", "failed") for r in latest)
        if stated_pass is not None and latest and stated_pass != recount_pass:
            sev = "S2"
            tag = "overstates" if stated_pass > recount_pass else "understates"
            ctx.add("chain", C, sev, f"CC-22 test report {rep['id']} states {stated_pass} passed; recount of latest runs per test case gives {recount_pass} pass / {recount_fail} fail over {len(latest)} cases ({tag}; misleading if the summary is relied on)", ["L2-09.07", "L2-09.05"], ctx.ev(rep), chain=C)
    findings = ctx.l2("L2-23.06")
    for t in ctx.l2("L2-23.04"):
        stated = sum(ints_in(ctx.p(t, "findings_by_severity")))
        mine = [f for f in findings if idnorm(ctx.p(f, "source_test_activity_id")) == idnorm(ctx.p(t, "test_activity_id") or t["id"])]
        if stated and mine and stated != len(mine):
            ctx.check(C)
            ctx.add("chain", C, "S2", f"CC-22 penetration test {t['id']} states {stated} findings; {len(mine)} finding records reference it", ["L2-23.04", "L2-23.06"], ctx.ev(t), chain=C)


def cc23(ctx: Ctx):
    C = "CC-23"
    for t in ctx.l2("L2-23.04"):
        ctx.check(C)
        who = str(ctx.p(t, "tester_org_and_independence") or "")
        if not who:
            ctx.add("chain", C, "S2", f"CC-23 penetration test {t['id']}: tester and independence not stated (FDA-CY V.C)", ["L2-23.04"], ctx.ev(t), chain=C)
        elif re.search(r"\b(internal|in-house|development team|dev team|same team|developer)\b", who, re.I) and not re.search(r"independen", who, re.I):
            ctx.add("chain", C, "S2", f"CC-23 penetration test {t['id']} performed by {who!r}; independence from the development team is not shown", ["L2-23.04"], ctx.ev(t), status="candidate", chain=C)
        if ctx.p(t, "original_third_party_report_provided") is False:
            ctx.add("chain", C, "S2", f"CC-23 penetration test {t['id']}: original third-party report not provided", ["L2-23.04"], ctx.ev(t), chain=C)


def cc26(ctx: Ctx):
    C = "CC-26"
    thr = None
    for m in ctx.l2("L2-15.01"):
        nums = re.findall(r"\d+(?:\.\d+)?", str(ctx.p(m, "acceptance_threshold") or ctx.p(m, "acceptance_criteria") or ""))
        if nums:
            thr = float(nums[0]); break
    if thr is None:
        return
    unacceptable = {idnorm(x) for r in ctx.l2("L2-15.04") for x in aslist(ctx.p(r, "residual_unacceptable_ids"))}
    for e in ctx.l2("L2-15.02"):
        nums = re.findall(r"\d+(?:\.\d+)?", str(ctx.p(e, "post_mitigation_score") or ""))
        if not nums:
            continue
        ctx.check(C)
        if float(nums[0]) > thr and idnorm(ctx.p(e, "vulnerability_id") or e["id"]) not in unacceptable:
            ctx.add("chain", C, "S3", f"CC-26 security risk {e['id']} post-mitigation score {nums[0]} exceeds the acceptance threshold {thr} but is not listed as unacceptable residual risk", ["L2-15.02", "L2-15.04"], ctx.ev(e), chain=C)


def cc27(ctx: Ctx):
    C = "CC-27"
    for a in ctx.l2("L2-11.01"):
        link = ctx.p(a, "risk_file_link")
        if not link or str(link).lower() in ("none", "n/a", "-", "—"):
            continue
        ctx.check(C)
        if not ctx.find_hazard(link):
            ctx.add("chain", C, "S2", f"CC-27 anomaly {a['id']} cites risk file entry {link!r}, which is not a hazard or hazardous situation in L2-04.03", ["L2-11.01", "L2-04.03"], ctx.ev(a), chain=C)


def cc28(ctx: Ctx):
    C = "CC-28"
    level = str(ctx.anchor("A.documentation_level") or "").lower()
    for e in ctx.l2("L2-01.02"):
        cls = str(ctx.p(e, "safety_class") or "").strip().upper()
        if not cls:
            continue
        ctx.check(C)
        if cls == "A" and level.startswith("enhanced"):
            ctx.add("chain", C, "S2", f"CC-28 software safety class A with Documentation Level Enhanced: class A means no injury possible, Enhanced means serious injury or death possible; query the classification", ["L2-01.02", "L2-01.01"], ctx.ev(e), status="candidate", chain=C)
        for h in aslist(ctx.p(e, "worst_case_hazardous_situation_ids")):
            if not ctx.find_hazard(h):
                ctx.add("chain", C, "S2", f"CC-28 safety classification cites hazardous situation {h}, not found in L2-04.03", ["L2-01.02", "L2-04.03"], ctx.ev(e), chain=C)


# ----------------------------------------------------------------------------- independent diff

CAND_ID_RE = re.compile(r"\b(?:CVE-\d{4}-\d+|[A-Z]{1,6}-\d{2,5}[a-z]?|b\d{3,5}|D\d{2}|\d{4}-\d{2}-\d{2}|\d+\.\d+(?:\.\d+)+)\b")
CAND_STOP = {"that", "this", "with", "from", "which", "have", "been", "were", "only", "also", "than", "then", "into", "their", "there",
             "stated", "states", "state", "document", "documents", "section", "table", "version", "software", "build", "module", "release",
             "submission", "evidence", "found", "searched", "listed", "list", "none", "does", "not", "but", "and", "for", "the", "its",
             "each", "per", "all", "any", "both", "while", "where", "when", "what", "whose", "under", "over", "between", "before", "after"}


def cand_keys(text: str, exclude=()):
    """(object identifiers, content tokens). Document ids, dates and the module's own version/build are not discriminating."""
    ids = {x for x in CAND_ID_RE.findall(text or "") if not re.match(r"^(D\d{2}|\d{4}-\d{2}-\d{2})$", x) and idnorm(x) not in exclude}
    toks = {w for w in re.findall(r"[a-z][a-z0-9]{3,}", (text or "").lower()) if w not in CAND_STOP}
    return ids, toks


def cand_similar(a, b) -> bool:
    ids_a, tok_a = a; ids_b, tok_b = b
    if ids_a and ids_b:
        inter = ids_a & ids_b
        if len(inter) >= 2 and len(inter) / len(ids_a | ids_b) >= 0.5:
            return True
        if len(inter) == 1 and len(ids_a | ids_b) <= 2 and tok_a and tok_b and len(tok_a & tok_b) / len(tok_a | tok_b) >= 0.25:
            return True
    if tok_a and tok_b and len(tok_a & tok_b) >= 4 and len(tok_a & tok_b) / len(tok_a | tok_b) >= 0.5:
        return True
    return False


def independent_diff(ctx: Ctx, ws: Path):
    """Read the original-first returns; group near-duplicate candidates across agents, bins and kinds; mark the groups
    that corroborate a mechanical break. One finding per group, with every member kept under `members`."""
    out, items = [], []
    for f in sorted((ws / "independent").glob("*.json")):
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            ctx.add("independent", f.name, "S2", f"independent return {f.name} is not valid JSON: {e}", [], status="unknown"); continue
        out.append(data)
        job = data.get("job_id", f.stem)
        for b in data.get("bins", []):
            l1 = b.get("l1")
            l2s = [x["id"] for x in ctx.l1map.get(l1, {}).get("l2", [])]
            n_ents = sum(len(ctx.l2(x)) for x in l2s)
            for nf in b.get("not_found", []):
                items.append({"kind": "not found", "job": job, "l1": l1, "l2": l2s[:1], "what": nf.get("what", ""), "detail": nf.get("searched", ""), "doc_ids": []})
            for pc in b.get("parameter_concerns", []):
                items.append({"kind": "parameter concern", "job": job, "l1": l1, "l2": l2s[:1], "what": pc.get("what", ""), "detail": pc.get("locator", ""), "doc_ids": [pc["doc_id"]] if pc.get("doc_id") else []})
            for c in b.get("contradictions", []):
                items.append({"kind": "contradiction", "job": job, "l1": l1, "l2": l2s[:1], "what": c.get("what", ""), "detail": "", "doc_ids": list(c.get("doc_ids", []))})
            if b.get("found") and n_ents == 0:
                ctx.add("independent", l1, "S2", f"Independent pass found evidence for {l1} ({len(b['found'])} items) but extraction produced no entities for it: possible extraction omission", l2s[:1], [{"entity": "", "doc_id": x.get("doc_id", ""), "quote": x.get("what", "")} for x in b["found"][:3]], status="candidate")
        for u in data.get("unexpected_material", []):
            items.append({"kind": "unexpected material", "job": job, "l1": "unexpected", "l2": [], "what": f"{u.get('doc_id','')}: {u.get('what','')}. {u.get('why_it_matters','')}", "detail": "", "doc_ids": [u["doc_id"]] if u.get("doc_id") else []})
    # group near-duplicates against each group's representative (no chaining through intermediates)
    anchor_ids = {idnorm(ctx.anchor("A.proposed_version")), idnorm(ctx.anchor("A.release_build_id"))}
    keys = [cand_keys(it["what"] + " " + it["detail"], anchor_ids) for it in items]
    order = sorted(range(len(items)), key=lambda i: -len(items[i]["what"]))
    groups, rep_of = [], []
    for i in order:
        for gi, g in enumerate(groups):
            if cand_similar(keys[rep_of[gi]], keys[i]):
                g.append(i); break
        else:
            groups.append([i]); rep_of.append(i)
    # identifiers of existing breaks, for corroboration
    breaks = [(f["id"], cand_keys(f["message"] + " " + " ".join(e.get("entity", "") + " " + e.get("quote", "") for e in f["evidence"]), anchor_ids)[0])
              for f in ctx.findings if f["status"] == "break"]
    ctx.candidate_items = len(items)
    for idxs in sorted(groups, key=lambda g: (-len(g), g[0])):
        members = [items[i] for i in idxs]
        rep = items[idxs[0]]
        kinds = Counter(m["kind"] for m in members)
        l1s = sorted({m["l1"] for m in members}); jobs = sorted({m["job"] for m in members})
        l2 = sorted({x for m in members for x in m["l2"]})
        group_ids = set().union(*(keys[i][0] for i in idxs))
        corroborates = [fid for fid, ids in breaks if len(group_ids & ids) >= 1 and (len(group_ids & ids) >= 2 or len(ids) <= 3)]
        sev = "S1" if kinds and set(kinds) == {"unexpected material"} else "S2"
        suffix = ""
        if len(members) > 1:
            suffix = f" [{len(members)} statements: {', '.join(f'{k} x{v}' for k, v in kinds.most_common())}; bins {', '.join(l1s)}; agents {', '.join(jobs)}]"
        if corroborates:
            suffix += f" [corroborates {', '.join(corroborates[:4])}]"
        f = ctx.add("independent", rep["l1"], sev, f"Independent pass, {rep['l1']}: {rep['kind']}: {rep['what']}{suffix}", l2,
                    [{"entity": "", "doc_id": ",".join(m["doc_ids"]), "quote": m["detail"]} for m in members if m["doc_ids"] or m["detail"]][:3], status="candidate")
        f["members"] = [{"kind": m["kind"], "job": m["job"], "l1": m["l1"], "what": m["what"], "doc_ids": m["doc_ids"], "locator": m["detail"]} for m in members]
        f["corroborates"] = corroborates
        f["new_vs_chains"] = not corroborates
    return out


# ----------------------------------------------------------------------------- report

def esc(s):
    return html.escape(str(s if s is not None else ""), quote=True)


def run(ws: Path):
    ws = Path(ws)
    prof = json.loads((ws / "profile.json").read_text())
    reg = json.loads((ws / "registry.json").read_text())
    ctx = Ctx(prof, reg)
    rows = presence(ctx)
    run_rules(ctx)
    for fn in (cc01, cc02, cc03, cc04, cc05, cc06, cc07, cc11, cc12, cc13, cc22, cc23, cc26, cc27, cc28):
        fn(ctx)
    independent = independent_diff(ctx, ws)
    # attach findings and priority
    for f in ctx.findings:
        for l2 in f["l2"]:
            if l2 in rows:
                rows[l2]["findings"].append(f["id"])
    sev_by_l2 = defaultdict(int)
    for f in ctx.findings:
        if f["status"] == "break":
            for l2 in f["l2"]:
                sev_by_l2[l2] = max(sev_by_l2[l2], SEV_RANK[f["severity"]])
    for r in rows.values():
        if r["status"] == "complete" and sev_by_l2[r["l2"]] >= 3:
            r["status"] = "partial"; r["support"] = min(r["support"], 2)
        if (r["importance"] == 3 and r["status"] != "complete") or sev_by_l2[r["l2"]] >= 3:
            r["priority"] = "P1"
        elif r["status"] != "complete" or sev_by_l2[r["l2"]] >= 2:
            r["priority"] = "P2"
        else:
            r["priority"] = "P3"
    l1rows = []
    for b in prof["bins"]:
        sub = [rows[x["id"]] for x in b["l2"]]
        l1rows.append({"l1": b["id"], "title": b["title"], "l2": len(sub), "entities": sum(r["entities"] for r in sub),
                       "absent": sum(r["status"] == "absent" for r in sub), "partial": sum(r["status"] == "partial" for r in sub), "complete": sum(r["status"] == "complete" for r in sub),
                       "priority": min((r["priority"] for r in sub), default="P3"), "findings": sum(len(r["findings"]) for r in sub)})
    counts = Counter(f["severity"] for f in ctx.findings if f["status"] == "break")
    report = {"workspace": str(ws), "profile_counts": prof["counts"], "anchors": reg["anchors"], "l1": l1rows, "l2": list(rows.values()),
              "findings": ctx.findings, "chains": {k: dict(v, title=CHAIN_TITLES.get(k, "")) for k, v in sorted(ctx.chain_stats.items())},
              "chains_not_implemented": NOT_IMPLEMENTED, "unbinned": reg["unbinned"], "notes": reg["notes"], "independent": independent,
              "documents": reg["documents"], "summary": {"findings_break": dict(counts), "findings_candidate": sum(f["status"] == "candidate" for f in ctx.findings),
                          "candidate_statements": ctx.candidate_items, "candidates_new_vs_chains": sum(1 for f in ctx.findings if f["status"] == "candidate" and f.get("new_vs_chains")),
                          "confidence_levels": reg.get("counts", {}).get("confidence_levels", {}), "replicated_docs": reg.get("counts", {}).get("replicated_docs", 0),
                          "l2_absent_searched": sum(1 for r in rows.values() if r["status"] == "absent" and r.get("absence_basis") == "searched"),
                          "candidates_corroborating": sum(1 for f in ctx.findings if f["status"] == "candidate" and f.get("corroborates")),
                                                          "l2_absent": sum(r["status"] == "absent" for r in rows.values()), "l2_partial": sum(r["status"] == "partial" for r in rows.values()),
                                                          "l2_complete": sum(r["status"] == "complete" for r in rows.values()), "P1": sum(r["priority"] == "P1" for r in rows.values())}}
    out = ws / "report"; out.mkdir(exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    (out / "gaps.json").write_text(json.dumps(ctx.findings, indent=1, ensure_ascii=False))
    (out / "report.html").write_text(render_html(report, prof))
    print(f"recomposed: {report['summary']} -> {out/'report.html'}")
    return report


def render_html(rep, prof):
    css = """body{font:15px system-ui;margin:1.5rem auto;max-width:1300px;padding:0 1rem;color:#1b2430;background:#fafbfc}table{border-collapse:collapse;width:100%;margin:.5rem 0 1rem}td,th{border:1px solid #d6dbe1;padding:.4rem .5rem;text-align:left;vertical-align:top}th{background:#eef1f4}
    .S3{border-left:5px solid #b91c1c}.S2{border-left:5px solid #b45309}.S1{border-left:5px solid #64748b}.P1{background:#fde8e8}.P2{background:#fff4e0}.P3{background:#e9f7ee}
    blockquote{margin:.3rem 0 .3rem 1rem;color:#475569;font-size:.9em}details{margin:.4rem 0}summary{cursor:pointer}code{background:#eef1f4;padding:0 .2rem}.cand{opacity:.8}small{color:#64748b}"""
    h = [f"<!doctype html><html lang='en'><meta charset='utf-8'><title>v3 recomposition</title><style>{css}</style><h1>Software module recomposition (v3)</h1>"]
    s = rep["summary"]
    h.append(f"<p>{esc(rep['workspace'])} · profile {rep['profile_counts']['l1']} L1 / {rep['profile_counts']['l2']} L2 · findings: {esc(s['findings_break'])} breaks, {s['findings_candidate']} reviewer candidates (grouped from {s.get('candidate_statements', 0)} statements; {s.get('candidates_corroborating', 0)} corroborate a break, {s.get('candidates_new_vs_chains', 0)} are new) · L2 absent {s['l2_absent']} (of which searched and not found: {s.get('l2_absent_searched', 0)}) / partial {s['l2_partial']} / complete {s['l2_complete']} · P1 bins {s['P1']} · entity confidence {esc(s.get('confidence_levels', {}))} over {s.get('replicated_docs', 0)} replicated documents</p>")
    h.append("<p><small>Statuses and scores are ordinal review aids. A break is a mechanical inconsistency in what the sponsor supplied; it is not a regulatory conclusion. Candidates need reviewer judgment.</small></p>")
    h.append("<h2>Anchors</h2><table><tr><th>Anchor</th><th>Resolved value</th><th>Claims</th><th>Conflict</th></tr>")
    def fmt_anchor(v):
        if isinstance(v, dict):
            return "; ".join(f"{k}={x}" for k, x in v.items())
        if isinstance(v, list):
            return "; ".join(str(x) for x in v)
        return str(v)
    for k, a in rep["anchors"].items():
        claims = "<br>".join(f"{esc(fmt_anchor(c['value']))} <small>({esc(c['doc_id'])})</small>" for c in a.get("claims", [])[:8])
        h.append(f"<tr class='{'S3' if a.get('conflict') else ''}'><td><code>{esc(k)}</code><br><small>{esc(a.get('shape',''))}</small></td><td>{esc(fmt_anchor(a.get('value'))) if a.get('value') not in (None, '', {}, []) else '<i>unresolved: not stated, or its source bin is dormant</i>'}</td><td>{claims}</td><td>{'YES: '+esc('; '.join(map(str, a.get('alternatives', [])))) if a.get('conflict') else ''}</td></tr>")
    h.append("</table><h2>Bins</h2><table><tr><th>L1</th><th>L2</th><th>Entities</th><th>Absent / partial / complete</th><th>Findings</th><th>Priority</th></tr>")
    for r in rep["l1"]:
        h.append(f"<tr class='{r['priority']}'><td><a href='#{esc(r['l1'])}'>{esc(r['l1'])}</a> {esc(r['title'])}</td><td>{r['l2']}</td><td>{r['entities']}</td><td>{r['absent']} / {r['partial']} / {r['complete']}</td><td>{r['findings']}</td><td>{r['priority']}</td></tr>")
    h.append("</table><h2>Consistency chains</h2><table><tr><th>Chain</th><th>Checks</th><th>Breaks</th><th>Unknown / candidates</th></tr>")
    for k, v in rep["chains"].items():
        h.append(f"<tr><td>{esc(k)} {esc(v['title'])}</td><td>{v['checks']}</td><td>{v['breaks']}</td><td>{v['unknown']}</td></tr>")
    h.append(f"</table><p><small>Not computed in v3: {', '.join(rep['chains_not_implemented'])}.</small></p>")
    h.append("<h2>Findings</h2>")
    for sev in ("S3", "S2", "S1", "info"):
        fs = [f for f in rep["findings"] if f["severity"] == sev]
        if not fs:
            continue
        h.append(f"<h3>{sev} ({len(fs)})</h3>")
        for f in sorted(fs, key=lambda f: (f["status"] != "break", f["ref"])):
            ev = "".join(f"<blockquote>{esc(e['doc_id'])}{' p'+esc(e['page']) if e.get('page') else ''} {esc(e['entity'])}: {esc(e['quote'])}</blockquote>" for e in f["evidence"][:3])
            mem = ""
            if len(f.get("members", [])) > 1:
                mem = "<details><summary><small>statements in this group</small></summary>" + "".join(f"<p><small><b>{esc(m['kind'])}</b> {esc(m['l1'])} {esc(m['job'])} {esc(','.join(m['doc_ids']))}: {esc(m['what'])}</small></p>" for m in f["members"]) + "</details>"
            h.append(f"<div class='{sev} {'cand' if f['status']!='break' else ''}' style='padding:.3rem .6rem;margin:.4rem 0;background:#fff'><b>{esc(f['id'])}</b> <code>{esc(f['ref'])}</code> <small>{esc(f['status'])} · {esc(', '.join(f['l2']))}</small><br>{esc(f['message'])}{ev}{mem}</div>")
    h.append("<h2>Bin detail</h2>")
    cur = None
    for r in rep["l2"]:
        if r["l1"] != cur:
            cur = r["l1"]; title = next(b["title"] for b in prof["bins"] if b["id"] == cur)
            h.append(f"<h3 id='{esc(cur)}'>{esc(cur)} {esc(title)}</h3>")
        miss = ", ".join(f"{k} ({v})" for k, v in list(r["missing_submission_params"].items())[:6])
        dhf = ", ".join(f"{k} ({v})" for k, v in list(r["missing_dhf_params"].items())[:6])
        h.append(f"<details class='{r['priority']}'><summary><b>{esc(r['l2'])}</b> {esc(r['title'])} · imp {r['importance']} · {esc(r['status'])} · support {r['support']}/3 · {r['entities']} entities · {r['priority']}</summary>"
                 f"<p>Docs: {esc(', '.join(r['docs']))}<br>Entity confidence: {esc(r.get('confidence') or {}) if r['entities'] else '—'}"
                 f"<br>Searched by extractors in: {esc(', '.join(r.get('searched_docs', []))) or 'no coverage statements'}; searched and not found in: {esc(', '.join(r.get('searched_not_found', []))) or '—'}"
                 f"{'<br><b>Absence basis: ' + esc(r['absence_basis']) + '</b>' if r.get('absence_basis') else ''}"
                 f"<br>Submission-scope parameters not stated: {esc(miss) or 'none'}<br><small>DHF-scope not in submission (normal): {esc(dhf) or 'none'}</small><br>Findings: {esc(', '.join(r['findings'])) or 'none'}</p></details>")
    h.append(f"<h2>Unbinned material ({len(rep['unbinned'])})</h2>")
    for u in rep["unbinned"]:
        h.append(f"<blockquote>{esc(u.get('doc_id'))}: {esc(u.get('quote',''))[:400]}<br><small>{esc(u.get('reason',''))}</small></blockquote>")
    h.append(f"<h2>Agent notes ({len(rep['notes'])})</h2>" + "".join(f"<p><small>{esc(n.get('doc_id'))}: {esc(n.get('text'))}</small></p>" for n in rep["notes"]))
    h.append("<h2>Independent pass</h2>")
    for data in rep["independent"]:
        h.append(f"<details><summary>{esc(data.get('job_id'))} · read {len(data.get('documents_read',[]))} documents · {len(data.get('bins',[]))} bins</summary><pre>{esc(json.dumps(data, indent=1, ensure_ascii=False))[:20000]}</pre></details>")
    h.append("<h2>Documents</h2><table><tr><th>Doc</th><th>L1</th><th>Version</th><th>Approved</th><th>Covers</th></tr>")
    for d in rep["documents"].values():
        p = d["params"]
        h.append(f"<tr><td>{esc(d['doc_id'])} {esc(p.get('document_title',''))}</td><td>{esc(', '.join(d['l1']))}</td><td>{esc(p.get('document_version',''))}</td><td>{esc(p.get('approval_date',''))}</td><td>{esc(p.get('software_version_covered',''))} {esc(p.get('build_id_covered',''))}</td></tr>")
    h.append("</table></html>")
    return "".join(h)
