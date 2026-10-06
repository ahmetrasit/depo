"""Compose profile/activation.json from the independent review decisions plus the v3 runtime pieces.

    python3 review/v3/profile/build_activation.py

Sources:
- standards-axis/REVIEW-FABLE-DECISIONS.json: activation set, importance, parameter scope, required overrides,
  added sub-elements, merges, corrections (reviewer decisions; the coordinator accepted them in full).
- This file: parameter additions the chains need, rules, recognition snapshot, L2 deactivations.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEC = HERE.parent / "standards-axis" / "REVIEW-FABLE-DECISIONS.json"
PROV = HERE / "activation.provisional.json"
OUT = HERE / "activation.json"

dec = json.loads(DEC.read_text())
prov = json.loads(PROV.read_text())

overlay = {
    "_provenance": {
        "built_from": [str(DEC.name), str(PROV.name)],
        "date": "2026-10-01",
        "note": "Reviewer decisions accepted in full: 18 active L1 (safety risk file active), importance 3 held at 45, 50 parameters moved to design-and-development-file scope, L1-21 collapsed to one L2, three L2 added. Coordinator additions: parameters the chains join on, rules, recognition snapshot, L1-13 limited to its plan and report. After run 1 (2026-10-01): why_appropriate and design_limitations on SOUP rows and device_in_standard_scope on declarations no longer required per row.",
        "build_identity_fallback": dec["scope_rules"][2],
        "dhf_scope_meaning": "design and development file / QMS record (ISO 13485:2016 7.3.10 via 21 CFR 820.10). A missing dhf-scope parameter is reported as 'not in submission; available on request' and lowers confidence, never completeness.",
    },
    "activate_l1": dec["activate_l1"],
    "deactivate_l2": ["L2-13.03", "L2-13.04", "L2-13.05"],
    "importance_overrides": dec["importance_overrides"],
    "parameter_scope_overrides": dec["parameter_scope_overrides"],
    "required_enhanced_overrides": {**dec["required_enhanced_overrides"],
                                    # run-1 tidy-ups: stated once per list or only when a condition holds, never per row
                                    "L2-12.01.why_appropriate": False, "L2-12.01.design_limitations": False,
                                    "L2-28.04.device_in_standard_scope": False},
    "l2_additions": dec["l2_additions"],
    "l2_merges": [dict(m, title="Security controls by FDA-CY category (collapsed for v3)") if m["into"] == "L2-21.01" else m for m in dec["l2_merges"]],
    "l2_corrections": dec["l2_corrections"],
    "chain_corrections": dec["chain_corrections"],
    "chain_additions": dec["chain_additions"],
    "parameter_additions": {
        "L2-04.05": [{"name": "hazard_ids", "type": "list", "required_enhanced": True, "scope": "submission", "check": "each must exist in L2-04.03 (hazard_id or hazardous_situation_id)", "check_type": "mechanical"},
                     {"name": "completeness_review_recorded", "type": "bool", "required_enhanced": False, "scope": "submission", "check": "ISO 14971 7.6 completeness of risk control; may be recorded on L2-04.08 instead", "check_type": "mechanical"}],
        "L2-28.03": [{"name": "declaration_id", "type": "id", "required_enhanced": True, "scope": "submission", "check": "must exist in L2-28.01", "check_type": "mechanical"}],
        "L2-21.01": [{"name": "category", "type": "enum", "required_enhanced": True, "scope": "submission",
                      "check": "Authentication|Authorization|Cryptography|Code, Data, and Execution Integrity|Confidentiality|Event Detection and Logging|Resiliency and Recovery|Updatability and Patchability (Appendix 1: Firmware and Software Updates)", "check_type": "mechanical"}],
        "L2-15.01": [{"name": "acceptance_threshold", "type": "text", "required_enhanced": False, "scope": "submission", "check": "numeric threshold used by CC-26", "check_type": "mechanical"}],
        "L2-15.04": [{"name": "residual_unacceptable_ids", "type": "list", "required_enhanced": False, "scope": "submission", "check": "CC-26: every L2-15.02 entry above the acceptance threshold must be listed here", "check_type": "mechanical"},
                     {"name": "conclusion_date", "type": "date", "required_enhanced": False, "scope": "submission", "check": "CC-12 e: after the last penetration test", "check_type": "mechanical"}],
    },
    "rules": prov["rules"],
    "recognition_snapshot": prov["recognition_snapshot"],
}
OUT.write_text(json.dumps(overlay, indent=1, ensure_ascii=False) + "\n")
print(f"wrote {OUT}: {len(overlay['activate_l1'])} L1 active, {len(overlay['importance_overrides'])} importance overrides, {len(overlay['parameter_scope_overrides'])} scope overrides, {len(overlay['l2_additions'])} additions, {len(overlay['l2_merges'])} merges")
