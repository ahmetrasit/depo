"""Oracle extraction for SYN-PMA-SW-01: a perfect-extractor return built from the generator's data.

Used to verify the recomposition chains independently of any model. The oracle states what the
documents say, including the planted defects, exactly as an ideal extractor would.

    python3 review/v3/fixtures/oracle_syn01.py <out.jsonl>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_syn01 as g  # noqa: E402

R = []


def ent(doc, l2, etype, id_, params, quote=None, status="executed", conf=3):
    R.append({"type": "entity", "entity_type": etype, "id": id_, "l2": l2, "doc_id": doc, "params": {k: v for k, v in params.items() if v not in (None, "", [])},
              "quote": quote or id_, "status": status, "confidence": conf})


def anchor(doc, name, value, quote=None):
    R.append({"type": "anchor", "name": name, "value": value, "doc_id": doc, "quote": quote or str(value), "confidence": 3})


def docrec(doc, l1, title, version, approved, approver, covers, build=None):
    R.append({"type": "doc", "doc_id": doc, "l1": l1, "params": {"document_title": title, "document_version": version, "approval_date": approved, "approver_names_roles": approver, "software_version_covered": covers, "build_id_covered": build}, "quote": title})


def main(out: Path):
    # documents
    l1_of = {"D01": ["L1-00", "L1-03"], "D02": ["L1-02"], "D03": ["L1-03", "L1-01"], "D04": ["L1-05"], "D05": ["L1-06"], "D06": ["L1-07"], "D07": ["L1-04"], "D08": ["L1-08"],
             "D09": ["L1-09"], "D10": ["L1-09"], "D11": ["L1-09"], "D12": ["L1-10"], "D13": ["L1-11"], "D14": ["L1-12"], "D15": ["L1-16"], "D16": ["L1-14"], "D17": ["L1-13", "L1-15"],
             "D18": ["L1-21", "L1-22"], "D19": ["L1-23"], "D20": ["L1-17"], "D21": ["L1-25"], "D22": ["L1-28"], "D23": ["L1-29", "L1-24"]}
    for name, title, ver, appr, who in g.DOCS_DEFS:
        d = name[:3]
        docrec(d, l1_of[d], title, ver, appr, who, g.PV, g.RB if d in ("D10", "D11") else None)
    # anchors
    anchor("D01", "A.proposed_version", g.PV, "Software version proposed for approval: 3.2.0"); anchor("D01", "A.release_build_id", g.RB, "Release build identifier: b1187")
    anchor("D01", "A.module_submission_date", g.SUBMIT, "Module submission date: 2026-05-04"); anchor("D01", "A.documentation_level", "Enhanced", "Documentation Level: Enhanced")
    anchor("D03", "A.proposed_version", g.PV, "Proposed version: **3.2.0**"); anchor("D03", "A.release_build_id", g.RB, "Release build identifier: **b1187**")
    anchor("D03", "A.code_freeze_date", g.CODE_FREEZE, "Code freeze: **2026-03-20**"); anchor("D03", "A.release_date", g.RELEASE, "Release approval date: **2026-04-15**")
    anchor("D02", "A.proposed_version", g.PV, "Final release version stated: **3.2.0**"); anchor("D02", "A.supported_platforms", ["CS-Patch Hub v2 (Linux 5.15.y)", "CS-Patch Hub v3 (Linux 6.1.77)"], "Hardware platforms: CS-Patch Hub v2")
    anchor("D09", "A.test_window", {"start": g.TEST_START, "end": g.TEST_END}, "2026-03-23 to 2026-04-08"); anchor("D10", "A.release_build_id", g.RB, "release build **b1187**"); anchor("D10", "A.proposed_version", g.PV, "version **3.2.0**")
    anchor("D13", "A.release_build_id", "b1180", "release candidate, build **b1180**"); anchor("D15", "A.sbom_build", {"build": "b1150", "version": g.PV}, "for build **b1150**"); anchor("D15", "A.proposed_version", g.PV, "software version 3.2.0")
    anchor("D23", "A.labeled_version", "3.2.1", "software version **3.2.1**"); anchor("D21", "A.device_support_end", "2032-12-31", "Software support end date: **2032-12-31**")
    anchor("D07", "A.risk_file_version", {"id": "RMR-ARR-3.2", "version": "Rev 3.1", "date": "2026-04-12", "covers": g.PV}, "Report RMR-ARR-3.2 Rev 3.1 dated **2026-04-12**"); anchor("D16", "A.threat_model_version", {"id": "TM-ARR", "version": "Rev 2.1", "date": "2026-01-30", "covers": g.PV}, "TM-ARR Rev 2.1 dated **2026-01-30**")
    anchor("D12", "A.design_control_start_version", "3.0.0", "3.0.0 | b0912"); anchor("D22", "A.proposed_version", g.PV, "software version **3.2.0**")
    # L1-03
    ent("D03", "L2-03.01", "software_version", g.PV, {"proposed_version": g.PV, "version_naming_rule": "MAJOR.MINOR.PATCH per Halden SOP-SW-004; build bNNNN", "user_accessible_identification": "About screen"}, "Proposed version: **3.2.0**")
    ent("D03", "L2-03.02", "software_version", g.RB, {"release_build_id": g.RB, "build_date": g.BUILD_DATE, "build_environment_toolchain_versions": "Yocto Kirkstone, GCC 11.4, halden-ci:2026.03", "archive_location_ref": "CM-BLD-1187"}, "Release build identifier: **b1187**")
    ent("D03", "L2-03.04", "date", "baseline-dates", {"code_freeze_date": g.CODE_FREEZE, "release_date": g.RELEASE, "last_change_request_implemented_id": "CH-32", "verification_complete_attestation_date": g.TEST_END}, "Code freeze: **2026-03-20**")
    cfg = [("CI-01", "ARR application", "software item", g.PV), ("CI-02", "Classification model parameters", "model/reference data", "3.2.0-p4"), ("CI-03", "libdsp", "SOUP", "4.1.2"), ("CI-04", "zlib-ng", "SOUP", "2.1.6"),
           ("CI-05", "OpenSSL", "SOUP", "3.0.13"), ("CI-06", "SQLite", "SOUP", "3.45.1"), ("CI-07", "Qt", "SOUP", "6.5.3"), ("CI-08", "Linux kernel Hub v3 BSP", "OS", "6.1.77"), ("CI-09", "Linux kernel Hub v2 BSP", "OS", "5.15.148"), ("CI-10", "Bootloader (mbedtls)", "software item", "1.9.0 / mbedtls 3.5.2")]
    for cid, nm, t, v in cfg:
        ent("D03", "L2-03.03", "design_component" if t != "SOUP" else "soup_component", nm, {"configuration_item_id": cid, "item_type": t, "item_version": v, "in_release_baseline": True}, f"| {cid} | {nm} |")
    ent("D03", "L2-01.02", "software_version", "ARR software system", {"software_system_id": "CI-01", "safety_class": "C", "worst_case_hazardous_situation_ids": ["HS-01", "HS-03"], "item_level_classes_and_segregation": ["U-06 Class A", "U-08 Class A"], "classification_rationale_ref": "D03 section 4"}, "classified **IEC 62304 Class C**")
    ent("D03", "L2-01.01", "document", "doc-level", {"documentation_level": "Enhanced", "pre_control_worst_hazardous_situation_ids": ["HS-01", "HS-03"]}, "Documentation Level")
    ent("D02", "L2-02.03", "software_version", g.PV, {"final_release_version_stated": g.PV, "hardware_platforms": ["CS-Patch Hub v2", "CS-Patch Hub v3"], "software_platforms_os_versions": ["Linux 5.15.y", "Linux 6.1.77", "Qt 6.5.3 LTS"], "ots_used": True}, "Final release version stated: **3.2.0**")
    # L1-05
    for r in g.REQS:
        tcs = [t["id"] for t in g.TCS if r["id"] in t["reqs"]]
        ent("D04", "L2-05.02", "requirement", r["id"], {"requirement_id": r["id"], "requirement_text": r["text"], "category": r["cat"], "safety_or_security_related": r["safety"], "criticality_flag": r["crit"], "verification_method": r["method"], "requirement_version_or_change_date": r["changed"]}, f"| {r['id']} |")
    for sid, txt, src in g.SEC_REQS:
        ent("D04", "L2-05.03", "requirement", sid, {"security_requirement_id": sid, "acceptance_criterion": txt, "security_requirements_review_date": "2026-02-11"}, f"| {sid} |")
    # L1-09
    for t in g.TCS:
        ent("D09", "L2-09.02", "test_case", t["id"], {"test_case_id": t["id"], "test_level": t["level"], "requirement_or_design_ids": t["reqs"], "risk_control_ids_verified": [t["rc"]] if t["rc"] else [], "protocol_id_and_version": t["proto"], "protocol_approval_date": t["approved"], "protocol_approver": "K. Novak"}, f"| {t['id']} |")
    for r in g.RUNS:
        ent("D10", "L2-09.05", "test_run", r["id"], {"test_run_id": r["id"], "test_case_id": r["tc"], "requirement_ids_covered": r["reqs"], "software_version_under_test": r["ver"], "build_id_under_test": r["build"],
                                                 "hardware_os_platform_config": "Hub v3 / Linux 6.1.77" if int(r["id"][3:]) % 2 else "Hub v2 / Linux 5.15.148", "ots_soup_versions_in_test_config": ["libdsp 4.1.2", "zlib-ng 2.1.6", "OpenSSL 3.0.13", "Qt 6.5.3"],
                                                 "execution_start_date": r["start"], "execution_end_date": r["end"], "result": r["result"].lower(), "anomaly_ids_raised": [r["anom"]] if r["anom"] else [], "retest_of_run_id": r["retest"], "actual_result_recorded": True}, f"| {r['id']} |")
    ent("D10", "L2-09.07", "test_report", "SVR-3.2", {"report_id": "SVR-3.2", "report_software_version": g.PV, "report_date": "2026-04-10", "counts_executed_passed_failed_blocked": "40 executed, 40 passed, 0 failed, 0 blocked", "deferred_anomaly_ids": ["ANM-104", "ANM-101"], "report_conclusion": "All 40 system test cases passed on build b1187."}, "All 40 system test cases passed on build b1187")
    ent("D10", "L2-09.08", "test_report", "SVR-3.2-summary", {"summary_software_version_tested": g.PV, "declared_test_window_start": g.TEST_START, "declared_test_window_end": g.TEST_END}, "within the declared test window")
    ent("D10", "L2-09.06", "document", "RA-32-01", {"regression_analysis_id": "RA-32-01", "regression_analysis_date": "2026-03-22", "tests_selected_for_rerun": ["full system set"], "tests_not_rerun_rationale": "TC-031, TC-032, TC-037 run on 3.1.4 (b1142) carried forward because classifier parameters unchanged"}, "Regression analysis RA-32-01")
    units = [("U-01", ["SRS-001", "SRS-008"]), ("U-02", ["SRS-002"]), ("U-03", ["SRS-003", "SRS-004", "SRS-005", "SRS-012", "SRS-013"]), ("U-04", ["SRS-024", "SRS-016"]), ("U-05", ["SRS-019", "SRS-011"]), ("U-06", ["SRS-006", "SRS-015", "SRS-023"]), ("U-07", ["SRS-010", "SEC-001"]), ("U-09", ["SRS-009", "SEC-004", "SEC-006", "SRS-018", "SRS-007"])]
    for u, reqs in units:
        ent("D11", "L2-09.03", "test_run", f"UT-{u[2:]}", {"test_run_id": f"UT-{u[2:]}", "test_case_id": f"UT-{u[2:]}", "requirement_ids_covered": reqs, "software_version_under_test": g.PV, "build_id_under_test": g.RB, "execution_start_date": "2026-03-23", "execution_end_date": "2026-03-24", "result": "pass", "test_tools_and_versions": ["GoogleTest 1.14"]}, f"| UT-{u[2:]} |")
    # L1-10
    for v, b, d, note, study in g.VERSIONS:
        ent("D12", "L2-10.01", "software_version", v, {"version": v, "build_id": b, "version_date": d, "test_activities_on_version": [note], "used_in_clinical_or_bench_study": [study] if study else []}, f"| {v} | {b} |")
    for cid, f, t, items, sec in g.CHANGES:
        ent("D12", "L2-10.02", "software_version", cid, {"change_id": cid, "from_version": f, "to_version": t, "affected_items": items, "safety_security_relevant": sec}, f"| {cid} |")
    ent("D12", "L2-10.04", "software_version", "final-entry", {"final_entry_version": g.PV, "last_fully_tested_version": g.PV, "differences_listed": [], "safety_effectiveness_assessment": "No differences."}, "No differences.")
    # L1-11
    for a in g.ANOMS:
        ent("D13", "L2-11.01", "anomaly", a[0], {"anomaly_id": a[0], "description": a[1], "discovery_method": a[2], "affected_versions": a[3], "defect_class_code": a[4], "safety_effectiveness_impact": a[5], "risk_file_link": a[6] if a[6] and a[6] != "H-none" else "", "security_impact_assessed": True}, f"| {a[0]} |")
    ent("D13", "L2-11.03", "anomaly", "ANM-list-3.2.0", {"list_build_id": "b1180", "list_software_version": g.PV, "extraction_date": "2026-04-05", "source_system_and_query": "Jira ARR, Open AND fixVersion != 3.2.0", "open_count_by_severity": "5 (0 critical, 1 major, 4 minor)"}, "Open anomalies: 5")
    # L1-12
    for sid, title, sup, ver, rel, fn in g.SOUP:
        ent("D14", "L2-12.01", "soup_component", sid, {"soup_id": sid, "title": title, "manufacturer_supplier": sup, "version_patch_designation": ver, "release_date": rel, "why_appropriate": fn}, f"| {sid} |")
    for sid, src, scope, rd, haz, sec in g.SOUP_REVIEW:
        ent("D14", "L2-12.04", "soup_component", sid, {"soup_id": sid, "anomaly_list_source": src, "anomaly_list_version_scope": scope, "review_date": rd, "hazard_relevant_anomalies": [haz] if haz else [], "security_vulnerabilities_cross_checked": sec}, f"| {sid} |")
    ent("D14", "L2-12.05", "soup_component", "SOUP-01", {"soup_id": "SOUP-01", "linked_hazard_ids": ["HS-01", "HS-03"]}, "SOUP-01 (libdsp) contributes to HS-01 and HS-03")
    ent("D14", "L2-12.05", "soup_component", "SOUP-02", {"soup_id": "SOUP-02", "linked_hazard_ids": ["HS-08"]}, "SOUP-02 to HS-08")
    # L1-16 / 17
    ent("D15", "L2-16.01", "document", "SBOM-3.2.0", {"sbom_format_and_spec_version": "CycloneDX 1.5", "sbom_generation_date": "2026-03-18", "generation_tool_and_version": "syft 0.105", "described_software_version": g.PV, "described_build_id": "b1150", "includes_transitive_dependencies": True}, "Generated **2026-03-18**")
    for nm, sup, ver, purl, rel, lvl, eos, vul in g.SBOM:
        ent("D15", "L2-16.02", "sbom_entry", nm, {"component_name": nm, "supplier_name": sup, "component_version": ver, "unique_identifier": purl, "dependency_relationship": rel, "level_of_support": lvl, "end_of_support_date": eos, "known_vulnerability_ids": [vul] if vul else []}, f"| {nm} |")
    for cve, comp, disc, kev, assess, disp in g.VULNS:
        ent("D20", "L2-17.01", "vulnerability", cve, {"vulnerability_id": cve, "component_ref": comp, "discovery_method": "SBOM scan", "vulnerability_source_db_and_query_date": disc, "in_cisa_kev": kev, "kev_check_date": "2026-03-19"}, f"| {cve} |")
        ent("D20", "L2-17.02", "vulnerability", cve, {"vulnerability_id": cve, "exploitability_assessment": assess, "disposition": disp}, f"| {cve} |")
    ent("D20", "L2-17.04", "vulnerability", "KEV-check", {"kev_vulnerability_ids_present_in_release": []}, "No KEV-listed vulnerabilities")
    # L1-14 / 15
    ent("D16", "L2-14.01", "document", "TM-ARR-2.1", {"threat_model_version": "2.1", "threat_model_date": "2026-01-30", "configuration_covered": g.PV, "methodology": "STRIDE"}, "TM-ARR Rev 2.1 dated **2026-01-30**")
    for tid, vec, tgt, ctl, tst in g.THREATS:
        ent("D16", "L2-14.04", "threat", tid, {"threat_id": tid, "attack_vector": vec, "targeted_element_ids": tgt, "mitigating_control_ids": ctl, "threat_mitigation_test_ids": tst}, f"| {tid} |")
    for sr, th, cwe, ctl, pre, post, st, dt in [("SR-01", "T-01", "CWE-347", "SC-01", "7.8", "2.1", "controlled", "2026-04-08"), ("SR-04", "T-04", "CWE-295", "SC-04, SC-06", "8.1", "2.2", "controlled", "2026-04-08"), ("SR-06", "T-06", "CWE-294", "SC-07", "7.1", "2.5", "controlled", "2026-04-08"), ("SR-07", "T-07", "CWE-400", "SC-08", "5.9", "2.0", "controlled", "2026-04-08")]:
        ent("D17", "L2-15.02", "vulnerability", sr, {"vulnerability_id": sr, "cwe_or_root_vulnerability": cwe, "threat_ids": [th], "control_ids": ctl.split(", "), "pre_mitigation_score": pre, "post_mitigation_score": post, "evaluation_date": dt}, f"| {sr} |")
    ent("D17", "L2-15.05", "vulnerability", "SR-06", {"vulnerability_id": "SR-06", "safety_impact_flag": True, "transferred_hazardous_situation_id": "HS-02"}, "SR-06 → HS-02")
    ent("D17", "L2-15.05", "vulnerability", "SR-07", {"vulnerability_id": "SR-07", "safety_impact_flag": True, "transferred_hazardous_situation_id": "HS-07"}, "SR-07 → HS-07")
    ent("D17", "L2-13.02", "document", "SRMR-ARR-3.2", {"report_version": "2.0", "report_date": "2026-04-09", "software_version_covered": g.PV, "residual_security_risk_conclusion": "acceptable", "traceability_section_present": True}, "SRMR-ARR-3.2 Rev 2.0 dated **2026-04-09**")
    # L1-21 / 23
    for sc, cat, reqs, impl, tests, l2 in g.SCS:
        ent("D18", "L2-21.01", "security_control", sc, {"control_id": sc, "category": cat, "security_requirement_ids": reqs, "implementation_ref": impl, "verification_test_ids": tests}, f"| {sc} |")
    for st, l2, b, v, rng, who, ctls, ths in g.STS:
        p = {"test_activity_id": st, "build_tested": b, "software_version_tested": v, "test_date_range": rng, "tester_org_and_independence": who, "scope_components_interfaces": ["IF-01", "IF-02", "IF-03", "IF-04", "IF-05"], "findings_ids": []}
        if l2 == "L2-23.02": p["threat_ids_covered"] = ths
        if l2 == "L2-23.01": p["security_requirement_ids_covered"] = [r for c in g.SCS if c[0] in ctls for r in c[2]]
        ent("D19", l2, "test_case", st, p, f"| {st} |")
    P = g.PEN
    ent("D19", "L2-23.04", "test_report", P["id"], {"test_activity_id": P["id"], "build_tested": P["build"], "software_version_tested": P["ver"], "test_date_range": P["range"], "tester_org_and_independence": P["tester"], "tools_versions_settings": P["tools"], "scope_components_interfaces": P["scope"], "findings_ids": [f[0] for f in P["findings"]], "duration_effort": "10 person-days", "methodology": "OWASP MASVS/ASVS plus manual exploitation", "findings_by_severity": P["findings_stmt"], "retest_date_and_build": "", "original_third_party_report_provided": True}, "Penetration test **PT-01**")
    for fid, sev, desc, disp, fb, dd in P["findings"]:
        ent("D19", "L2-23.06", "vulnerability", fid, {"finding_id": fid, "source_test_activity_id": P["id"], "severity_score": sev, "disposition": disp, "fixed_in_build": fb, "disposition_date": dd}, f"| {fid} |")
    # L1-04
    for h in g.HAZ:
        ent("D07", "L2-04.03", "hazard", h[0], {"hazard_id": h[0], "hazardous_situation_id": h[1], "cause_description": h[2], "harm_and_severity": h[4], "contributing_software_item_ids": h[5], "security_origin_flag": h[6]}, f"| {h[0]} |")
    for c in g.RCS:
        ent("D07", "L2-04.05", "risk_control", c[0], {"risk_control_id": c[0], "hazard_ids": [c[1]], "control_type": "design", "implementing_requirement_ids": c[3], "implementing_design_ids": c[4], "implementation_verification_test_ids": c[5], "effectiveness_verification_ref": c[6]}, f"| {c[0]} |")
    ent("D07", "L2-04.08", "document", "RMR-ARR-3.2", {"report_version_date": "3.1", "report_date": "2026-04-12", "software_version_covered": g.PV, "reviewers_and_authority": "S. Brandt; Dr. L. Meyer; M. Okafor"}, "RMR-ARR-3.2 Rev 3.1 dated **2026-04-12**")
    # L1-28
    for did, std, rn, cl, dev, dt in [("DoC-1", "IEC 62304:2006 + AMD1:2015 (Edition 1.1)", "13-79", "5.1 (all), 5.2–5.8, 6, 7, 8, 9", "none", "2026-04-20"), ("DoC-2", "ISO 14971:2019 (third edition)", "5-125", "4–10", "none", "2026-04-20"),
                                      ("DoC-3", "ANSI/UL 2900-1, Second Edition (2023)", "13-96", "all", "none", "2026-04-20"), ("DoC-4", "IEC 62366-1:2015 + AMD1:2020 (Edition 1.1)", "5-129", "all", "none", "2026-04-20"), ("DoC-5", "IEC 81001-5-1:2021 (Edition 1.0)", "13-122", "4–9 (Annex A not claimed)", "none", "2026-04-20")]:
        ent("D22", "L2-28.01", "declaration", did, {"doc_id": did, "applicant_name_address": "Halden Cardiac Systems GmbH, Hannover", "product_identification": f"CardioSense ARR Software Module {g.PV} {g.RB}", "statement_of_conformity": "conforms to the standards listed", "standard_designation_and_edition": std, "fda_recognition_number": rn, "date_of_issue": dt, "place_of_issue": "Hannover", "signatory_name_function": "R. Lindqvist, Regulatory Affairs Director", "limitations_on_validity": f"applies to {g.PV}; activities completed by 2026-04-12"}, f"| {did} |")
        ent("D22", "L2-28.03", "declaration", did, {"declaration_id": did, "clauses_claimed": [cl], "deviations_declared": dev}, f"| {did} |")
    # labeling
    ent("D23", "L2-29.01", "software_version", "3.2.1", {"labeled_version": "3.2.1", "labeling_document_version_date": "IFU-ARR-07 2026-04-22", "on_screen_identification_location": "Settings → About"}, "software version **3.2.1**")
    ent("D23", "L2-24.05", "document", "IFU-SBOM", {"sbom_delivery_method": "Halden customer portal", "labeled_sbom_version": "3.2.0"}, "The SBOM for version 3.2.0 is available")
    R.append({"type": "unbinned", "doc_id": "D02", "quote": "A non-device function (battery statistics export) shares the hub", "reason": "Multiple-function assessment reference; no bin active for it in this profile"})
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in R) + "\n")
    print(f"oracle: {len(R)} records -> {out}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
