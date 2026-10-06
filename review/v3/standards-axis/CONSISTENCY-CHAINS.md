# Consistency chains for the software-module recomposition

Status: research draft, 2026-10-01. Parameter names refer to `BIN-HIERARCHY.json` as `<L2 id>.<parameter>`. Anchors (`A.*`) are defined in that file's `anchors` block, and each one is resolved once per case from its source L2.

## How to read this file

Each chain lists:

- **Joins:** the entities and parameters it connects.
- **Condition:** what must be true.
- **Break means:** what a failed condition says about the evidence. It never states a regulatory conclusion.
- **Severity:** uses the scale below.
- **Type:** whether the join can be computed or needs a reviewer.

Severity scale (maps onto `review/SCORING.md`):

| Severity | Meaning | Effect on the affected items |
|---|---|---|
| S3 | Decision-critical link broken: the evidence may not apply to the proposed device | The affected importance-3 items cannot be `complete`, so they become P1 |
| S2 | Material gap or inconsistency that needs a reviewer question | The items become `partial` or `unclear`, so they become P2 |
| S1 | Supporting inconsistency, such as navigation, labels or counts with no decision effect | Recorded as a qualifier and lowers evidence-match confidence |

Type:

- **Mechanical:** a deterministic join on ids, version strings, dates, enum values or set membership. The recomposition can compute it and report it without judgment.
- **Judgment:** the join is computed only to collect candidates. A reviewer decides whether the condition holds.
- **Mixed:** the link existence is mechanical and its adequacy is judgment.

Normalization rules for mechanical joins:

- Version strings are compared after case-folding and removing a leading "v" or "version". Build ids are compared exactly.
- A version difference counts as "bridged" only if the two versions appear as consecutive or ordered entries in `L2-10.01`, and either `L2-10.04.differences_listed` or a `L2-09.06` regression analysis covers the change.
- Dates are ISO dates. A missing date fails any ordering check (`unknown`, not `pass`).
- Set comparisons report three lists: left-only, right-only and both. Any non-empty left-only or right-only list is a finding until a reviewer marks it justified.

---

## CC-01 Requirement → test case → passing result at the proposed build

- **Joins:**
  - `L2-05.02.requirement_id`, `verification_method`, `verifying_test_ids`, `criticality_flag`, `requirement_version_or_change_date`
  - `L2-09.02.test_case_id`, `requirement_or_design_ids`
  - `L2-09.05` and `L2-09.03` runs: `test_case_id`, `requirement_ids_covered`, `software_version_under_test`, `build_id_under_test`, `result`, `execution_end_date`
  - `L2-03.01.proposed_version` and `L2-03.02.release_build_id`
- **Condition:**
  - Every requirement with `verification_method=test` has at least one test case.
  - Each of those test cases has a latest run with `result=pass`. That run used either `build_id_under_test = A.release_build_id` or a bridged build (see normalization).
  - The run ended after the requirement's last change (`execution_end_date > requirement_version_or_change_date`).
  - Critical requirements have at least one passing system-level run.
  - Enhanced: unit and integration runs exist for design elements (`L2-07.01`) that implement safety-related requirements.
- **Break means:** the requirement may be untested, tested only on a superseded build, or tested before it last changed.
- **Severity:** S3 for safety, security or critical requirements; S2 otherwise.
- **Type:** Mechanical. Whether a bridge is adequate is judgment, and that judgment belongs to CC-09.

## CC-02 Hazard → risk control → verification of implementation → verification of effectiveness

- **Joins:**
  - `L2-04.03.hazard_id` and `hazardous_situation_id`
  - `L2-04.05.risk_control_id`, `implementing_requirement_ids`, `implementing_design_ids`, `implementation_verification_test_ids`, `effectiveness_verification_ref`, `control_type`
  - `L2-04.06.residual_acceptability`
  - Run records from CC-01
  - `L2-27.08` for use-related controls
- **Condition:**
  - Every hazardous situation that is unacceptable at initial evaluation has at least one control.
  - Every control traces to at least one SRS requirement and, at Enhanced, at least one SDS element.
  - Each implementation test has a passing run at the proposed or bridged build (reuse CC-01).
  - Every control has effectiveness evidence that is a different record from the implementation test. If it is the same record, ISO 14971 7.2 Note 3 must be argued.
  - Information-for-safety controls point to a labeling section and to a summative evaluation of that information.
  - `residual_acceptability` recomputed from the plan matrix equals the stated value.
- **Break means:** the risk file asserts a control without showing it was built, without showing it works, or on another configuration.
- **Severity:** S3.
- **Type:** Mixed. The links are mechanical. Whether the effectiveness evidence is adequate is judgment.

## CC-03 SOUP → version → anomaly-list review → risk

- **Joins:**
  - `L2-12.01.soup_id`, `version_patch_designation`, `manufacturer_supplier`
  - `L2-12.04.anomaly_list_version_scope`, `review_date`, `hazard_relevant_anomalies`
  - `L2-12.05.linked_hazard_ids`
  - `L2-16.02.component_version`, `supplier_name`
  - `L2-03.03.item_version`
- **Condition:**
  - The SOUP version matches across the SOUP list, the configuration item list and the SBOM entry.
  - The anomaly-list review covers that same version.
  - The review date is after the SOUP version was frozen in configuration, and the review is "current" relative to `A.module_submission_date`. Flag any review older than the latest SOUP version change, and pass the review's age to the reviewer.
  - Each hazard-relevant SOUP anomaly links to a hazard in `L2-04.03`.
- **Break means:** the supplier defect review was done on a different version, or never fed the risk file.
- **Severity:** S3 when the SOUP item contributes to a hazardous situation (IEC 62304 7.1.3 applies); S2 otherwise.
- **Type:** Mechanical. The currency of the review is judgment.

## CC-04 Threat → security control → security test → finding disposition

- **Joins:**
  - `L2-14.04.threat_id`, `mitigating_control_ids`, `threat_mitigation_test_ids`
  - `L2-21.0x.control_id`, `security_requirement_ids`, `verification_test_ids`
  - `L2-05.03.security_requirement_id`
  - `L2-23.01` and `L2-23.02` runs (`build_tested`, `findings_ids`)
  - `L2-23.06.finding_id`, `disposition`, `fixed_in_build`
  - `L2-19.01` trace rows
- **Condition:**
  - Every threat has controls, or an accepted rationale.
  - Every control has a security requirement with an acceptance criterion and has both a requirements test (implementation) and a threat-mitigation test (effectiveness).
  - Tests ran on `A.release_build_id` or a bridged build.
  - Every finding has a disposition. A `fixed` disposition needs `fixed_in_build <= A.release_build_id` and a retest.
  - The trace matrix (`L2-19.01`) agrees with the per-artifact links.
- **Break means:** a claimed security control is unverified, is verified only for implementation, or has unresolved findings.
- **Severity:** S3.
- **Type:** Mechanical. The adequacy of a threat-mitigation test is judgment.

## CC-05 Single version identity across the module

- **Joins:**
  - `L2-03.01.proposed_version` (`A.proposed_version`) and `L2-03.02.release_build_id`
  - `L2-02.03.final_release_version_stated`
  - `L2-10.04.final_entry_version`
  - `L2-09.08.summary_software_version_tested`
  - `L2-09.07.report_software_version`
  - `L2-16.01.described_software_version` and `described_build_id`
  - `L2-24.05.labeled_sbom_version`
  - `L2-29.01.labeled_version`
  - `L2-11.03.list_software_version` and `list_build_id`
  - `L2-04.08.software_version_covered`
  - `L2-13.02.software_version_covered`
  - `L2-14.01.configuration_covered`
  - `L2-28.04.software_version_covered_by_doc`
  - `L2-27.08.ui_software_version_tested`
  - Every L1's `l1_document_parameters.software_version_covered`
- **Condition:** All of these equal `A.proposed_version`, and the build ids equal `A.release_build_id`. Any exception is explicitly bridged in `L2-10.04`.
- **Break means:** at least one evidence set (SBOM, tests, labeling, risk file, threat model or DoC) describes a different software than the one proposed. This is the most common and most decision-relevant mechanical defect.
- **Severity:** S3 for tests, SBOM, labeling and risk report; S2 for descriptive documents.
- **Type:** Mechanical.

## CC-06 Anomaly list = release candidate, and anomaly sets agree

- **Joins:**
  - `L2-11.03.list_build_id`, `extraction_date`, `open_count_by_severity`
  - `L2-11.01.anomaly_id`, `affected_versions`, `disposition_date`, `security_impact_assessed`
  - `L2-18.01.anomaly_id`
  - `L2-09.07.deferred_anomaly_ids`
  - `L2-09.05.anomaly_ids_raised`
  - `L2-23.06` findings with disposition `accepted` or `deferred`
- **Condition:**
  - The list build equals `A.release_build_id`.
  - The extraction date is on or after the last test-run end and on or before the submission date.
  - Recounted entries equal the stated counts.
  - These sets are equal: unresolved list, security-assessed set, and deferred set in the reports.
  - Every failing run's anomaly is either unresolved (on the list) or closed by a fix and passing retest.
  - Accepted or deferred security findings that are software defects appear on the unresolved list or in a documented exclusion.
- **Break means:** known defects may be missing from the list, assessed for a different build, or never assessed for security impact.
- **Severity:** S3.
- **Type:** Mechanical.

## CC-07 Declaration of conformity edition = recognized edition, and extent covers the claimed clauses

- **Joins:**
  - `L2-28.01.standard_designation_and_edition`, `fda_recognition_number`, `date_of_issue`
  - `L2-28.02.recognized_edition_db`, `recognition_number_db`, `extent_of_recognition_db`, `transition_expiry_date`, `withdrawn_flag`
  - `L2-28.03.clauses_claimed`, `deviations_declared`
  - `A.recognition_db_snapshot` (STANDARDS-REGISTER.md)
- **Condition:**
  - The DoC edition string matches the recognized edition for the cited recognition number.
  - The recognition number exists, is not withdrawn, and is within any transition window at `A.module_submission_date`.
  - The claimed clauses avoid unrecognized clauses under partial recognition.
  - No deviations are declared.
  - For IEC 62304 at Enhanced level, the clauses claimed include 5.1 (all subclauses), 6 and 8.
  - Process standards have supplemental documentation (`L2-28.05`).
- **Break means:** the declaration cannot serve as a DoC. It must be treated as general use (FDA-STD IV.B), with underlying data, or it misstates conformity.
- **Severity:** S3 when the DoC replaces documentation (for example the 62304 route for VI.G); S2 otherwise.
- **Type:** Mechanical, except clause-applicability rationales, which are judgment.
- **Known library-driven risk:** the library holds non-recognized editions of several standards that FDA recognizes in another edition. These include ISO/IEC 29147:2018 versus the recognized 2014 edition, ISO/IEC 30111:2019 versus 2013, UL 2900-1:2026 versus 2017, ISO/IEC/IEEE 15026-1:2019 versus 2013, IEC 62443-2-1 edition 2.0 versus edition 1.0, and AAMI TIR34971:2023 versus CR34971:2022. A sponsor citing these editions should produce CC-07 breaks.

## CC-08 Usability: critical tasks → use-related risks → UI controls → summative validation on the final UI

- **Joins:**
  - `L2-27.03.task_id`, `critical_task`, `hazardous_situation_id`, `risk_control_ids`, `severity`
  - `L2-04.03.harm_and_severity`
  - `L2-27.05.ui_requirement_ids`
  - `L2-27.08.critical_tasks_tested`, `ui_software_version_tested`, `labeling_version_used`, `participants_by_group`
  - `L2-27.01.user_groups`
  - `L2-27.04.hf_submission_category`
- **Condition:**
  - Every critical task maps to a hazardous situation in the risk file with the same severity scale.
  - Every UI risk control maps to an SRS requirement.
  - Category 3: every critical task is in the summative scenarios, or a rationale is given.
  - The summative UI version equals `A.proposed_version`, or production equivalence is argued.
  - The labeling version used equals final labeling.
  - Every user group is represented.
  - The category matches the decision-point answers.
- **Break means:** use-related risk controls may be unvalidated, or validated on a superseded UI or labeling.
- **Severity:** S3 for Category 3 or when critical tasks exist; S2 otherwise.
- **Type:** Mixed. Representativeness and production equivalence are judgment.

## CC-09 Change history → regression analysis → re-verification scope

- **Joins:**
  - `L2-10.01.version` and `version_date`
  - `L2-10.02.change_id`, `from_version`, `to_version`, `affected_items`, `safety_security_relevant`
  - `L2-10.05.affected_risk_control_ids`
  - `L2-09.06.regression_analysis_id`, `tests_selected_for_rerun`, `tests_not_rerun_rationale`, `regression_run_ids`
  - `L2-00.03` (module reopening)
  - Run records
- **Condition:**
  - Every change between the last fully tested version and `A.proposed_version` has a regression analysis.
  - Every test whose last passing run predates a change touching its requirement or design element was either re-run on a later build or carries a rationale.
  - Safety- or security-relevant changes have risk re-analysis and, if they touch interfaces or architecture, a threat-model date after the change (`L2-14.01`).
  - If `A.proposed_version` changed after FDA accepted the module, an amendment lists the repeated tests.
- **Break means:** older evidence is being carried forward to a changed build without a documented basis.
- **Severity:** S3 when changes touch safety, security or critical requirements; S2 otherwise.
- **Type:** Mixed. Selecting candidates is mechanical. Whether a rationale is adequate is judgment.

## CC-10 Security → safety risk transfer

- **Joins:**
  - `L2-15.05.vulnerability_id`, `safety_impact_flag`, `transferred_hazardous_situation_id`
  - `L2-04.03.security_origin_flag`
  - `L2-17.02` dispositions
- **Condition:**
  - Every vulnerability or security risk with a safety impact has a hazardous situation in the safety risk file flagged as security-origin.
  - Every security-origin hazardous situation points back to a vulnerability.
  - The residual evaluation in the safety risk file reflects the security controls.
- **Break means:** a security risk with patient-safety impact is missing from the safety risk file, or the two files disagree.
- **Severity:** S3.
- **Type:** Mechanical.

## CC-11 SBOM ↔ SOUP list ↔ configuration items ↔ tested OTS versions

- **Joins:**
  - `L2-16.02` entries
  - `L2-12.01` SOUP list
  - `L2-03.03` configuration items where `item_type` is SOUP or OS
  - `L2-09.05.ots_soup_versions_in_test_config`
  - `L2-09.04.ots_versions`
  - `L2-02.03.software_platforms_os_versions`
- **Condition:**
  - The SOUP list is a subset of the SBOM, with equal name, supplier and version.
  - Every SOUP or OS configuration item appears in the SBOM.
  - Test configurations use exactly these versions.
  - Every OTS version the device permits has test evidence (FDA-OTS III.C).
- **Break means:** the tested stack and the shipped or declared stack differ, or the SBOM omits components.
- **Severity:** S3.
- **Type:** Mechanical.

## CC-12 Date ordering

All checks are mechanical. A missing date gives `unknown`.

| # | Earlier | Later | Source rule | Severity |
|---|---|---|---|---|
| a | `L2-04.01.plan_approval_date` | first `L2-04.04.evaluation_date` | FDA-SW VI.C(1): criteria set before initial evaluation | S2 |
| b | `L2-09.02.protocol_approval_date` | each formal run `execution_start_date` | protocol governs execution | S2; S3 for system-level runs relied on in the summary |
| c | `A.code_freeze_date` | release-candidate run `execution_start_date`, `L2-16.01.sbom_generation_date`, `L2-03.02.build_date` | evidence must describe the frozen baseline | S3 |
| d | last change touching the tested item | that test's run date | IEC 62304 5.7.3 retest after change | S3 for safety, security or critical items |
| e | `L2-23.04.test_date_range` end | `L2-13.02.report_date` and `L2-15.04.conclusion_date` | security conclusions must postdate pen test findings | S2 |
| f | pen test `build_tested` | must equal `A.release_build_id` or be a bridged earlier build; if bridged, all security-relevant changes after it need CC-09 coverage | FDA-SW VI.I tested-vs-released assessment; FDA-STD IV.A final finished device | S3 |
| g | last `L2-11.01.disposition_date` and last `L2-23.06.disposition_date` | `L2-04.08.report_date` | ISO 14971 8–9: overall evaluation after all controls verified | S2 |
| h | `L2-05.04.srs_approval_date` | first system-level protocol approval | DHF synchronized; no retrospective documentation (FDA-SW III) | S1 (judgment escalation) |
| i | `L2-07.03.sds_initial_approval_date` | first unit run for the covered units | FDA-SW VI.F prospective SDS | S2 |
| j | underlying evidence completion (`L2-28.04.evidence_completion_date`) | `L2-28.01.date_of_issue` | FDA-STD IV.A: conformance before declaration | S2 |
| k | every execution, report, DoC and list date | `A.module_submission_date` | no promissory evidence (FDA-STD VI) | S3 |
| l | `L2-09.05` run end dates | `A.release_date` | IEC 62304 5.8.1: verification complete before release | S2 |
| m | `L2-27.06.plan_approval_date` | summative execution start | IEC 62366-1 5.7.3 | S2 |
| n | `L2-13.01.plan_approval_date` | first `L2-15.02.evaluation_date` | criteria set before assessment | S2 |
| o | `L2-00.03.module_acceptance_date` | any later `A.proposed_version` change | FDA-MODPMA VI.C(4) | S3 |
| p | `L2-12.04.review_date` | must be on or after the date the SOUP version entered `A.configuration_set` | IEC 62304 7.1.3 | S2 |
| q | `L2-17.01` vulnerability query date | judged against `A.module_submission_date` (age reported, no fixed limit) | FDA-CY V.A.4(b) "all known vulnerabilities" | S2 (judgment) |
| r | `L2-14.01.threat_model_date` | must be after the last security-relevant change in `L2-10.02` | IEC 81001-5-1 7.2 current scope | S2 |

## CC-13 Known vulnerabilities ↔ SBOM ↔ KEV ↔ disposition

- **Joins:**
  - `L2-17.01.vulnerability_id`, `component_ref`, `in_cisa_kev`, `vulnerability_source_db_and_query_date`
  - `L2-16.02.known_vulnerability_ids`
  - `L2-17.02.disposition`
  - `L2-17.04.kev_vulnerability_ids_present_in_release`
  - `L2-15.02` entries
- **Condition:**
  - Every vulnerability listed against an SBOM component appears in the vulnerability assessment with a disposition.
  - Every vulnerability references an existing SBOM component.
  - KEV vulnerabilities are absent from the release or individually justified.
  - The scan was run against `A.sbom_build`.
- **Break means:** known vulnerabilities are unassessed, or the assessment refers to a different component set.
- **Severity:** S3.
- **Type:** Mechanical. Scan recency is judgment.

## CC-14 Component end of support vs device support horizon

- **Joins:**
  - `L2-16.02.level_of_support` and `end_of_support_date`
  - `A.device_support_end` (`L2-25.07` and `L2-24.10`)
  - `L2-17.03.replacement_or_update_plan`
  - `L2-12.09.support_mechanism`
- **Condition:**
  - Any component whose end of support is earlier than `A.device_support_end`, or whose support level is `no longer maintained`, `abandoned` or `unknown`, has a replacement or update plan, and its disclosure appears in labeling.
  - The device support end date is the same in the management plan and in labeling.
- **Break means:** the device will knowingly ship, or remain in the field, with unsupported components and no plan.
- **Severity:** S2; S3 if the component is internet-facing or security-relevant.
- **Type:** Mechanical. Plan adequacy is judgment.

## CC-15 Interface set agreement

- **Joins:**
  - `L2-02.04.interface_id`
  - `L2-06.03.interface_id` (with `crosses_trust_boundary`)
  - `L2-14.02.element_id` where kind is data flow or trust boundary
  - `L2-22.05.path_id`, `protocol_name_version_ports`, `unused_or_dormant_interfaces`
  - `L2-24.03.port_or_interface`
  - `L2-26.01.connectors_listed`
  - `L2-09.03.integration_interface_ids`
  - `L2-23.0x.scope_components_interfaces`
- **Condition:**
  - The externally exposed interfaces are the same set in the architecture, threat model, security views, labeling port list and 524B connector list.
  - Every interface has integration testing.
  - Every external interface is in the security test scope, or is listed as an exclusion with a rationale.
- **Break means:** an attack surface or a functional dependency is undocumented, untested or undisclosed.
- **Severity:** S3 for external or trust-boundary interfaces; S2 for internal ones.
- **Type:** Mechanical.

## CC-16 Transferred security risk → labeling → human factors task

- **Joins:**
  - `L2-15.06.transferred_risk_id` and `receiving_user_type`
  - `L2-14.03.assumption_verified_or_transferred`
  - `L2-24.0x` labeling items
  - `L2-24.12.hf_task_id`
  - `L2-27.03.task_id`
- **Condition:**
  - Every transferred risk or assumption appears in labeling.
  - Every transferred risk is either an HF task in the URRA or has a rationale for exclusion.
  - Tasks given to lay users are judged feasible.
- **Break means:** risk is shifted to users who are not told about it or cannot act on it (FDA-CY V.A and VI.A).
- **Severity:** S2; S3 when the receiving user is a patient or caregiver.
- **Type:** Mixed.

## CC-17 Documentation Level ↔ risk severity ↔ Enhanced deliverables

- **Joins:**
  - `L2-01.01.documentation_level` and `pre_control_worst_hazardous_situation_ids`
  - `L2-04.03.harm_and_severity`
  - Presence of L1-07 (SDS), `L2-09.03` (unit and integration), and `L2-08.02`/`L2-08.03` full plans or a 62304 DoC with clauses 5.1, 6 and 8
- **Condition:**
  - If any pre-control hazardous situation reaches death or serious injury, the level is Enhanced.
  - If the level is Enhanced, every Enhanced-only deliverable is present.
  - A Class III device claiming Basic carries a rationale.
- **Break means:** the claimed level understates risk, or required Enhanced content is missing.
- **Severity:** S3.
- **Type:** Mechanical. Severity classification is judgment.

## CC-18 Supported platform coverage

- **Joins:**
  - `L2-02.03.hardware_platforms` and `software_platforms_os_versions` (`A.supported_platforms`)
  - `L2-09.04.environment_id`, `hardware_model`, `os_and_patch_level`
  - `L2-09.05.hardware_os_platform_config`
  - `L2-29.02.user_selectable_ots_versions`
- **Condition:**
  - Every supported platform has an environment.
  - Every platform has at least one passing run of the critical and system test set.
  - Every user-selectable OTS version is validated.
- **Break means:** labeling or the description claims platforms that were not tested.
- **Severity:** S3 for platforms affecting safety or effectiveness; S2 otherwise.
- **Type:** Mechanical. A "representative platform" argument is judgment.

## CC-19 Residual risk and workaround disclosure

- **Joins:**
  - `L2-04.07.disclosed_residual_risks`
  - `L2-11.04.anomaly_ids_covered`
  - `L2-29.03.disclosed_items`
  - `L2-15.04.residual_unacceptable_ids`
  - `L2-24.10` (end of support)
- **Condition:** Every significant residual risk and every user workaround appears in labeling.
- **Break means:** users are not told about known residual risk.
- **Severity:** S2.
- **Type:** Mechanical.

## CC-20 Deferred security findings → future release plan → management plan timelines

- **Joins:**
  - `L2-23.06.disposition=deferred`, `deferral_plan_release_and_timeline`, `interim_devices_receive_update`
  - `L2-25.05.regular_cycle_length_and_justification`
  - `L2-25.06.patching_capability_rate`
- **Condition:**
  - Every deferred finding has a release plan whose timeline fits the plan's regular or out-of-cycle commitments.
  - Every deferred finding states whether interim devices will receive the update.
- **Break means:** shipped vulnerabilities have no credible remediation path.
- **Severity:** S2; S3 when the post-mitigation score fails the acceptance threshold.
- **Type:** Mixed.

## CC-21 Cross-module software version join (modular PMA)

- **Joins:**
  - `L2-10.01.used_in_clinical_or_bench_study` and `version`
  - Software versions stated in other modules (bench, analytical, clinical and the final-module labeling)
  - `L2-00.03.changed_version_after_acceptance`
- **Condition:**
  - Every software version named as studied in another module appears in the version history.
  - Differences between the studied version and `A.proposed_version` are assessed in `L2-10.04`.
  - Any change after module acceptance has an amendment.
- **Break means:** clinical or bench evidence was generated on software whose relationship to the proposed release is undocumented.
- **Severity:** S3.
- **Type:** Mechanical for presence. Whether a difference is significant is judgment.

## CC-22 Report counts reconcile with records

- **Joins:**
  - `L2-09.07.counts_executed_passed_failed_blocked` against recounted runs
  - `L2-23.04.findings_by_severity` against the `L2-23.06` finding list
  - `L2-11.03.open_count_by_severity` against `L2-11.01` entries
- **Condition:** The stated counts equal the recounts.
- **Break means:** the summary does not reflect the records, either through an extraction gap or a misleading summary.
- **Severity:** S2. If the summary overstates the pass rate, status becomes `misleading` under SCORING.md.
- **Type:** Mechanical.

## CC-23 Independence of testers for decisive evidence

- **Joins:**
  - `L2-09.05.executor_independence`
  - `L2-23.05.independence_level`
  - `L2-23.04.tester_org_and_independence`
  - `L2-28.06.lab_name` and `accreditation_body_and_scope`
- **Condition:**
  - Pen testing and the other activities listed in IEC 81001-5-1 5.7.5 document how objectivity was ensured.
  - Third-party reports are originals.
  - Lab accreditation scope covers the method relied on.
- **Break means:** evidence-match and assessment confidence fall. This is not by itself a completeness gap.
- **Severity:** S2.
- **Type:** Judgment.

## CC-24 Standards cited vs declared vs expected

- **Joins:**
  - `L2-28.09.standards_cited_in_module` and `standards_listed_in_section`
  - `L2-28.10.expected_standard_id` and `addressed_by`
  - Register relevance class
- **Condition:**
  - Every cited standard is listed with a use type.
  - Every register-`expected` standard is addressed by a DoC, by general use, or by equivalent evidence.
- **Break means:** standards appear as unsupported assertions, or an expected standard (for example IEC 62304, ISO 14971, IEC 81001-5-1, SW96/TIR57 or IEC 62366-1) is silently absent.
- **Severity:** S2.
- **Type:** Mechanical. Whether evidence is equivalent is judgment.

## CC-25 ML model version binding (conditional on L1-30)

- **Joins:**
  - `L2-30.02.model_version`, `model_artifact_hash`, `model_version_tested`
  - `L2-03.03` configuration items (`item_type=model`)
  - `L2-09.04.test_data_set_ids_versions`
  - `L2-30.03.partition_role`
- **Condition:**
  - The model version is in the release configuration and equals the tested model version.
  - Test data sets are versioned and include an independent partition.
- **Break means:** the same application version may carry a different model than the one evaluated.
- **Severity:** S3.
- **Type:** Mechanical. Data independence is judgment.

---

## Chain summary

| Chain | Name | Type | Max severity |
|---|---|---|---|
| CC-01 | Requirement → test → result at build | Mechanical | S3 |
| CC-02 | Hazard → control → implementation and effectiveness | Mixed | S3 |
| CC-03 | SOUP → version → anomaly review → risk | Mechanical (+ judgment on currency) | S3 |
| CC-04 | Threat → control → security test → disposition | Mechanical | S3 |
| CC-05 | Single version identity | Mechanical | S3 |
| CC-06 | Anomaly list = release candidate | Mechanical | S3 |
| CC-07 | DoC edition, recognition and extent | Mechanical | S3 |
| CC-08 | Critical tasks → URRA → summative on final UI | Mixed | S3 |
| CC-09 | Change → regression → re-verification | Mixed | S3 |
| CC-10 | Security → safety risk transfer | Mechanical | S3 |
| CC-11 | SBOM ↔ SOUP ↔ configuration ↔ tested OTS | Mechanical | S3 |
| CC-12 | Date ordering (a–r) | Mechanical | S3 |
| CC-13 | Vulnerabilities ↔ SBOM ↔ KEV | Mechanical | S3 |
| CC-14 | Component end of support vs device support | Mechanical (+ judgment) | S3 |
| CC-15 | Interface set agreement | Mechanical | S3 |
| CC-16 | Transferred risk → labeling → HF | Mixed | S3 |
| CC-17 | Documentation Level ↔ deliverables | Mechanical | S3 |
| CC-18 | Platform coverage | Mechanical | S3 |
| CC-19 | Residual risk disclosure | Mechanical | S2 |
| CC-20 | Deferred findings → plans | Mixed | S3 |
| CC-21 | Cross-module version join | Mechanical | S3 |
| CC-22 | Count reconciliation | Mechanical | S2 |
| CC-23 | Tester independence | Judgment | S2 |
| CC-24 | Standards cited vs declared vs expected | Mechanical | S2 |
| CC-25 | ML model binding (conditional) | Mechanical | S3 |

Totals: 25 chains. 19 are mechanical; two of them (CC-03 and CC-14) also carry a judgment element on currency or plan adequacy. 5 are mixed (CC-02, CC-08, CC-09, CC-16, CC-20). 1 is judgment only (CC-23). CC-12 has 18 ordering checks (a–r).
