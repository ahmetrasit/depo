# Standards register: PMA software module (standards axis)

- **Status:** research draft for building the review profile. It is not a list of mandatory deliverables.
- **Scope:** a modular PMA with the software module submitted first. The module covers device software functions, cybersecurity, risk management, the usability interface and SOUP/OTS software. Documentation Level is Enhanced.
- **Recognition checked:** 2026-10-01, against the live FDA Recognized Consensus Standards database (`accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards`, results and detail pages; the site shows "Page Last Updated: 09/28/2026").
- **Library snapshot:** `/Volumes/OZTURK/_projects/standards`, re-listed at 15:40 EDT on 2026-10-01. Files were being added to the library while this work was in progress. Filenames below are exact.

## How to read this register

- **ID:** the key used in `BIN-HIERARCHY.json`. Prefixes:
  - `AUTH-`: a regulation, statute or FDA guidance. These are authorities, not consensus standards.
  - `STD-`: a consensus standard or technical report.
  - `REF-`: a non-consensus reference named by FDA guidance.
- **FDA recognition:** values are as read from the database detail page (Supplementary Information Sheet, SIS) on 2026-10-01.
  - "Recognized" means a current recognition number exists for the edition stated.
  - "Recognized (other edition)" means FDA recognizes an edition different from the library copy.
  - "Not recognized" means a designation-number search returned no record. These searches are substring searches; the same method found every standard known to be recognized.
  - "UNVERIFIED" is used where the database did not settle the question. The text says what was tried.
- **Class** (for a PMA software module at Enhanced level):
  - `expected`: FDA reviewers normally expect conformity or equivalent evidence.
  - `conditional`: depends on a device fact. The trigger is stated.
  - `context`: informative only.
- **Reviewer checks:** what to verify when a sponsor declares conformity or relies on the document. The general DoC checks in the "Declaration of Conformity checks" section apply to every row in addition.

Count: 92 rows. 20 `AUTH-` rows, 63 `STD-` rows (several group a series, so about 95 designations are covered) and 9 `REF-` rows.

---

## A. Regulations, statute and FDA guidances (authorities)

| ID | Title, issue date and status | Library file | Role for the software module | Opened in this pass |
|---|---|---|---|---|
| AUTH-REG-814.20 | 21 CFR 814.20 PMA application. Current eCFR text fetched for 2026-09-01. | `cfr/21CFR-Part814-PMA-2025.pdf` | (b)(4) device description; (b)(5) reference to voluntary standards and (b)(5)(ii) "explain any deviation from a voluntary standard"; (b)(6)(i) nonclinical studies; (b)(10) proposed labeling | Yes (eCFR API and library PDF) |
| AUTH-LAW-524B | FD&C Act 524B (21 USC 360n-2), cyber devices | `cfr/21USC-360n-2-Section524B-2024.html` | (a) covered submissions; (b)(1) plan including coordinated vulnerability disclosure (CVD); (b)(2) processes and updates; (b)(3) SBOM; (c) definition | Via FDA-CY VII only. The HTML was not opened. |
| AUTH-REG-820 | 21 CFR 820 QMSR, effective 2026-02-02. Incorporates ISO 13485:2016 by reference. | `cfr/21CFR-Part820-QMSR-2025.pdf` | QMS obligations behind design records. Not itself a submission-content rule. | No |
| AUTH-FDA-SW | Content of Premarket Submissions for Device Software Functions. Final, June 14 2023. | `fda/Premarket-Software-Functions-Guidance.pdf` | Spine for L1-01 to L1-11: V, VI.A–J and Table 1 (Enhanced column) | Yes, in full |
| AUTH-FDA-CY | Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions. Final, Feb 3 2026; supersedes June 27 2025. | `fda/FDA-Cybersecurity-QMS-Premarket-2026.pdf` (added during this run; SHA-256 prefix d046fa836048933e, identical to the fda.gov media/119933 download) | Spine for L1-13 to L1-26: IV.B–D, V.A.1–6, V.B.1–2, V.C, VI.A–B, VII.A–E, Appendices 1, 2 and 4 | Yes, IV–VII and Appendices 1 (headings), 2, 3 and 4 |
| AUTH-FDA-OTS | Off-The-Shelf Software Use in Medical Devices. Final, Aug 11 2023. | `fda/Off-The-Shelf-Guidance_0.pdf` | L1-12: III.A.1–6, III.B, III.C, III.D.1–2, IV.D, IV.E | Yes, III–IV |
| AUTH-FDA-STD | Appropriate Use of Voluntary Consensus Standards in Premarket Submissions for Medical Devices. Final, Sept 18 2018. | `fda/FDA-Appropriate-Use-Voluntary-Consensus-Standards-2018.pdf` | L1-28: IV.A(1) DoC elements a–h; IV.A(2) supplemental documentation; IV.A(3) review a–g; Table 1; IV.B general use; V transition; VI promissory statements; VIII withdrawn standards | Yes, IV–VIII |
| AUTH-FDA-RECWD | Recognition and Withdrawal of Voluntary Consensus Standards. Final, Sept 15 2020. | `fda/FDA-Recognition-Withdrawal-Voluntary-Consensus-Standards.pdf` | Recognition mechanics; SIS meaning | Extracted only |
| AUTH-FDA-HFC26 | Content of Human Factors Information in Medical Device Marketing Submissions. Final, May 29 2026 (draft was Dec 9 2022). | `fda/FDA-Content-Human-Factors-Information-Marketing-Submissions.pdf` | L1-27: IV (HF Submission Category, decision points A–D), Table 1, V Sections 1–8, Tables 2–3 (URRA) | Yes, III–V |
| AUTH-FDA-HF16 | Applying Human Factors and Usability Engineering to Medical Devices. Reissued Aug 3 2026; originally Feb 3 2016. | `fda/FDA-Applying-Human-Factors-Usability-Engineering-2026.pdf` (SHA-256 prefix 9b49b108) | L1-27: 6.1–6.4 critical tasks; 8 and 8.1.x validation on final design; 8.2 modified devices | TOC and section 8 |
| AUTH-FDA-PMCY | Postmarket Management of Cybersecurity in Medical Devices, 2016 | `fda/FDA-Postmarket-Management-Cybersecurity-2016.pdf` | Controlled/uncontrolled risk concepts behind 524B(b)(2) | Extracted only |
| AUTH-FDA-MODPMA | Premarket Approval Application and Humanitarian Device Exemption Modular Review. Jan 13 2025; originally Nov 3 2003. | `fda/FDA-PMA-Modular-Review.pdf` | L1-00: VI.B shell; VI.C(1) module contents; VI.C(4) reopening a closed module; VI.C(5) final module; Appendix II "Declaration of Conformance to Standards for Module" and "Software Validation and Verification Information" | Yes |
| AUTH-FDA-PMAFILE | Acceptance and Filing Reviews for PMAs. Dec 16 2019. | `fda/FDA-PMA-Acceptance-Filing-Review.pdf` | Acceptance checklist item 12.a: DoC or general-use basis for recognized standards; basis and data for non-recognized standards | Item 12 |
| AUTH-FDA-ESTAR | eSTAR Program page (content current as of 09/21/2026; nIVD/IVD v7.1). Draft guidance "Electronic Submission Template for PMAs", Sept 18 2026. | `fda/FDA-eSTAR-Program-page.html`; `fda/FDA-eSTAR-PMA-Template-Draft-2026.pdf` | PMA eSTAR sections are named in draft Table 1. Draft III scope **excludes PMA Modules and Modular Shells**. The program page states the DoC is built into the template. | Draft III and Table 1; program page via WebFetch |
| AUTH-FDA-GPSV | General Principles of Software Validation, Jan 2002 | `fda/FDA-General-Principles-Software-Validation-2002.pdf` | Referenced by FDA-SW VI.D, VI.F and VI.H for content detail | No |
| AUTH-FDA-INTEROP | Design Considerations and Premarket Submission Recommendations for Interoperable Medical Devices, Sept 2017 | `fda/FDA-Interoperable-Medical-Devices-2017.pdf` | Interfaces (L2-02.04) | No |
| AUTH-FDA-MFDP | Multiple Function Device Products: Policy and Considerations, July 2020 | `fda/FDA-Multiple-Function-Device-Products-2020.pdf` | "Other functions" | No |
| AUTH-FDA-AI | AI-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations. **Draft**, Jan 7 2025. FDA media/184856 still serves the draft on 2026-10-01. | `fda/guidance-ai-enabled-device-software-functions.pdf`; `fda/FDA-AI-Enabled-Device-Software-Functions-2025.pdf` | L1-30 (conditional) | Header only |
| AUTH-FDA-PCCP | Marketing Submission Recommendations for a PCCP for AI-Enabled Device Software Functions. Final, Aug 18 2025; originally Dec 4 2024. | `fda/Guidance-Predetermined-Change-Control-AI.pdf` | L2-30.07 | Header only |
| AUTH-FDA-CSA | Computer Software Assurance for Production and QMS Software. Final, **Feb 3 2026** (FDA page date 02/03/2026, media/188844). | Library copy `fda/guidance-computer-software-assurance-production-quality-system.pdf` is the **Sept 24 2025 edition, which has been superseded** | Context: production and QMS software. Not device software. | Header only |

Other FDA files in the library that are context only (not opened): `Guidance-Clinical-Decision-Software_5.pdf` (CDS, Jan 2026), `fda/FDA-Q-Submission-Program.pdf`, `fda/FDA-PMA-Supplement-Decision-Making-2008.pdf`, `fda/FDA-Policy-Device-Software-Functions-Mobile-Apps.pdf`, `fda/FDA-Benefit-Risk-PMA-DeNovo-2019.pdf`, `fda/FDA-Uncertainty-Benefit-Risk-PMA-DeNovo-2019.pdf`, `fda/FDA-Good-Machine-Learning-Practice-Principles.pdf`, `fda/FDA-Transparency-ML-Enabled-Devices-Principles.html`.

---

## B. Consensus standards

### B1. Software life cycle and health software product safety

| ID | Standard and title | Library file(s) | FDA recognition (2026-10-01) | Class (trigger) | Reviewer checks when conformity is declared or relied on |
|---|---|---|---|---|---|
| STD-62304 | IEC 62304:2006+AMD1:2015 (Edition 1.1 CSV), Medical device software — Software life cycle processes | `iec62304{ed1.1}b.pdf`; `ANSI+AAMI+IEC+62304-2006.pdf` plus `62304_A1_2016.pdf` | **Recognized 13-79.** IEC 62304 Ed 1.1 2015-06 CSV; identical adoption ANSI/AAMI/IEC 62304:2006/A1:2016. Complete. List 051, entry 2019-01-14. SIS: recognized on merit; lists FDA-SW 2023, FDA-OTS 2023, FDA-CY 2026 and FDA-STD 2018 among relevant guidances. | expected | DoC route for FDA-SW VI.G at Enhanced level must cover **5.1 (5.1.1–5.1.12), clause 6 and clause 8**; a DoC to the complete standard is not needed (FDA-SW VI.G). It is a process standard, so supplemental documentation is required (FDA-STD IV.A(2)): the plans or summaries themselves. The software safety class the sponsor assumes is a 62304 option and does not set the FDA Documentation Level. The 1.1 or 2006/A1:2016 edition must be cited; the 2006 edition alone is not recognized. Evidence parameters come from 5.6.7, 5.7.5 a)–g), 5.8.2–5.8.5, 7.1.3, 8.1.2–8.1.3 and 9.8 (see BIN-HIERARCHY L1-03, L1-09, L1-11, L1-12). |
| STD-82304-1 | IEC 82304-1:2016 Ed 1.0, Health software — Part 1: General requirements for product safety | `iec82304-1{ed1.0}b.pdf` | **Recognized 13-97.** Ed 1.0 2016-10. Complete. List 047, entry 2017-08-21. | conditional: software-only health software product (SaMD) on general-purpose platforms | Product validation plan and report (6.1–6.3) on the released version; identification with a unique version identifier visible to the user (7.1); accompanying documents (7.2.1–7.2.3); post-market (8.1–8.5). Clause 5 invokes 62304. |
| STD-60601-1 | IEC 60601-1:2005+AMD1:2012+AMD2:2020 (Ed 3.2 CSV). Clause 14 programmable electrical medical systems (PEMS); 14.13 IT-network connection. | `iec60601-1{ed3.2}en.pdf` (also `iec60601-1{ed3.1}en.pdf`) | **Recognized 19-49** (IEC Ed 3.2 2020-08, included in ASCA), Complete, List 060, entry 2023-04-03. Also ANSI/AAMI ES60601-1 consolidated text including AMD2:2021, **19-46**, entry 2022-05-30. | conditional: ME equipment containing PEMS | Applicability statement per 14.1. When 14.2–14.13 apply, 62304 4.3, 5, 7, 8 and 9 also apply (14.1). 14.13 technical description: network characteristics, hazardous situations from network failure, instructions to the responsible organization. The edition cited must be 3.2 (or ES60601-1 per 19-46). ASCA test summary where used. Ed 3.1 is in the library but is not a current recognition (not returned by the database). |
| STD-60601-1-6 | IEC 60601-1-6:2010+AMD1:2013+AMD2:2020 (Ed 3.2 CSV), Usability collateral | `iec60601-1-6{ed3.2}b.pdf` | **Recognized 5-132** (Ed 3.2 2020-07, ASCA). Complete. List 055, entry 2020-12-21. | conditional: ME equipment | 4.2 applies the usability engineering process via IEC 62366-1. Check consistency with the 62366-1 DoC. |
| STD-60601-1-8 | IEC 60601-1-8 Ed 2.2 2020-07 CSV, Alarm systems | **NOT IN LIBRARY** | **Recognized 5-131** (ASCA). Complete. Entry 2020-12-21. | conditional: ME equipment whose software generates alarm conditions | Alarm requirements trace to SRS and system tests. |
| STD-TIR45 | AAMI TIR45:2023, Guidance on the use of AGILE practices in the development of medical device software | `AAMI+TIR45-2023.pdf` (added during run) | **Recognized 13-143.** Complete. List 064, entry 2025-05-26. SIS transition: TIR45:2012 (13-36) DoC accepted until **2028-07-02**. | conditional: agile life cycle claimed | It is a TIR, so it gives guidance rather than requirements. Use it to interpret iterative evidence and design history file (DHF) synchronization (FDA-SW III). Check that the edition cited is 2023, or 2012 before the transition date. |
| STD-TR60601-4-5 | IEC TR 60601-4-5:2021, Safety-related technical security specifications for medical devices | **NOT IN LIBRARY** | **Not recognized** (search "60601-4-5": no records) | context | None |

### B2. Risk management (safety), including software and ML guidance

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-14971 | ISO 14971:2019 (3rd ed.), Medical devices — Application of risk management to medical devices | `ISO+14971-2019.pdf`; `example list of standards for poc/ANSI+AAMI+ISO+14971-2019.pdf` | **Recognized 5-125.** ISO 14971 3rd ed. 2019-12; identical adoption ANSI/AAMI/ISO 14971:2019. Complete. List 053, entry 2019-12-23. **SIS note:** the probability-based definition of risk (3.18) does not apply to cybersecurity, where FDA uses exploitability. | expected | FDA-STD IV.A(2) names ISO 14971 as a standard needing supporting documentation. Check: plan 4.4 a)–g); risk management file traceability 4.5; verification of implementation and effectiveness 7.2; overall residual risk 8; review/report 9 before release; 10 production/post-production. A DoC never replaces the risk file content FDA-SW VI.C asks for. |
| STD-TR24971 | ISO/TR 24971:2020, Guidance on the application of ISO 14971 | `ISO+TR+24971-2020-2.pdf` | **Not recognized** (search "24971" and "TIR24971": no records) | context | Interpretation aid only |
| STD-TR80002-1 | IEC/TR 80002-1:2009 Ed 1.0, Guidance on the application of ISO 14971 to medical device software | `iec80002-1{ed1.0}en.pdf` | **Recognized 13-34** (Ed 1.0 2009-09; identical ANSI/AAMI/IEC TIR80002-1). Complete. List 030, entry 2013-01-15. | context | Technical report, no requirements. Annex B lists examples of software causes that are useful for checking hazard completeness. |
| STD-TIR80002-2 | AAMI/ISO TIR80002-2:2017, Validation of software for medical device quality systems | `AAMI+ISO+TIR80002-2-2017.pdf` | **Not recognized** (search "TIR80002" returned only 13-34) | context: production/QMS tools | None |
| STD-CR34971 | AAMI CR34971:2022, Guidance on the Application of ISO 14971 to AI and ML (recognized). Library holds **AAMI TIR34971:2023**, Application of ISO 14971 to machine learning in AI — Guide. | `AAMI+TIR34971-2023-2.pdf` | **Recognized (other designation/edition) 13-124:** AAMI CR34971:2022, Complete, List 059, entry 2022-12-19. The library edition TIR34971:2023 is **not** the recognized designation. **UNVERIFIED** whether FDA treats TIR34971:2023 as equivalent: the database has no TIR34971 record and the CR34971 SIS does not mention it. | conditional: device has ML-enabled functions | A DoC must cite CR34971:2022 / 13-124. A TIR34971:2023 citation should be handled as general use. Check that ML hazards (data, overfitting, drift, automation bias) appear in the risk file (L2-30.05). |
| STD-TS24971-2 | ISO/TS 24971-2:2026, Guidance on the application of ISO 14971 — Part 2: Machine learning in AI | `ISO+TS+24971-2-2026-3.pdf`, `-4.pdf`, `-5.pdf` (three copies) | **Not recognized** (search "24971": no records) | context, or conditional general use (ML) | General use only |

### B3. Security life cycle, security risk management and security testing

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-81001-5-1 | IEC 81001-5-1:2021 Ed 1.0, Health software and health IT systems safety, effectiveness and security — Part 5-1: Security — Activities in the product life cycle. Plus ISH1:2025 interpretation sheet. | `IEC+81001-5-1-2021.pdf`; `IEC+81001-5-1-2021+ISH1-2025.pdf` | **Recognized 13-122.** Ed 1.0 2021-12. Complete. List 059, entry 2022-12-19. **SIS note:** conformance may not satisfy all 524B requirements or the FDA-CY recommendations. ISH1:2025 is **not mentioned** in the SIS (UNVERIFIED whether a DoC must or may cite it). | expected: an SPDF framework, or an equivalent such as 62443-4-1 or JSP2 (FDA-CY V) | Process standard, so supplemental documentation is required. Check scope and tailoring (4.1.3, 5.8.2 b), Annex E). Test activities: 5.7.1 security requirements, 5.7.2 threat mitigation, 5.7.3 vulnerability (known-vulnerability testing based on recent public source contents), 5.7.4 penetration, 5.7.5 objectivity. Release: 5.8.1 findings resolved, 5.8.2 documentation, 5.8.3 file integrity. Threat model per 7.2 a)–l) for the current development scope. Configuration management in clause 8 can reproduce the list of external components. Classification of software items as maintained/supported/required (4.3; ISH1). Annex F covers transitional health software. |
| STD-SW96 | ANSI/AAMI SW96:2023, Security risk management for device manufacturers | `ANSI+AAMI+SW96-2023.pdf` | **Recognized 13-131.** Complete. List 061, entry 2023-10-09. **SIS note:** may not satisfy 524B; exploitability, not ISO 14971 probability, is the basis for security risk estimation. | expected: SW96 or TIR57, or equivalent (FDA-CY V.A names both) | Plan (4.4), file (4.7), supply chain and third parties (4.5–4.6), analysis (5.1–5.5), evaluation including safety impact (6.1–6.2), control (7.1–7.6), overall residual (8), review (9), production/post-production (10). Report attributes from Annex C.2–C.6 (version history, approvals, scope, per-vulnerability attributes with versions). If the scoring method relies on probability of attack, check it against the SIS note. |
| STD-TIR57 | AAMI TIR57:2016 (R2023), Principles for medical device security — Risk management | `AAMI+TIR57-2016+(R2023).pdf` | **Recognized 13-83** (TIR57:2016). Complete. List 043, entry 2016-06-27. SIS notes as SW96. The library copy is the 2023 reaffirmation; **UNVERIFIED** whether the SIS's "TIR57:2016" covers the R2023 printing. Reaffirmation normally carries no technical change, but this was not confirmed. | expected (alternative to SW96) | TIR (guidance) structure 3–9: plan 3.4, threats/vulnerabilities/assets/impacts 4.3.1–4.3.4, risk control 6.1–6.7, report 8. A DoC to a TIR carries limited assurance, so check the report content directly. |
| STD-TIR97 | AAMI TIR97:2019 (R2023), Postmarket risk management for device manufacturers | `AAMI+TIR97-2019+(R2023).pdf` | **Recognized 13-112** (TIR97:2019). Complete. List 053, entry 2019-12-23. **SIS rationale:** guidance for postmarket security risk management; may not satisfy 524B. Same R2023 note as TIR57. | conditional: device with cybersecurity risk; supports the VI.B management plan | Clauses 3–7 and Annex C (CVD) and Annex E (incident handling), against plan elements L2-25.01 to L2-25.09. |
| STD-62443-4-1 | ANSI/ISA-62443-4-1-2018 (recognized) / IEC 62443-4-1:2018 Ed 1.0 (library), Secure product development life-cycle requirements | `iec62443-4-1{ed1.0}b.pdf` | **Recognized 13-119** as **ANSI/ISA 62443-4-1-2018**. Complete. List 056, entry 2021-06-07. SIS: may not satisfy 524B. **UNVERIFIED** whether a DoC citing the IEC designation is accepted under 13-119: the record names only the ANSI/ISA designation. | conditional: SPDF framework used instead of, or in addition to, 81001-5-1 | Practices SM-1 to SM-13, SR-1 to SR-5, SD-1 to SD-4, SI-1 and SI-2, SVV-1 to SVV-5 (9.2–9.6, testing and independence), DM-1 to DM-6, SUM-1 to SUM-5, SG-1 to SG-7. FDA-CY V.C cites 4-1 for vulnerability testing. |
| STD-62443-4-2 | IEC 62443-4-2:2019 Ed 1.0 plus COR1:2022, Technical security requirements for IACS components | `iec62443-4-2{ed1.0}b.pdf`; `iec62443-4-2-cor1{ed1.0}b.pdf` | **Not recognized** (search "62443-4-2": no records) | context | Component requirement catalogue; general use only |
| STD-62443-3-3 | IEC 62443-3-3:2013 Ed 1.0, System security requirements and security levels | `iec62443-3-3{ed1.0}en.pdf` | **Not recognized** | context | None |
| STD-62443-3-2 | IEC 62443-3-2:2020 Ed 1.0, Security risk assessment for system design | `iec62443-3-2{ed1.0}en.pdf` | **Not recognized** (not among the 4 records returned for "62443") | context | None |
| STD-62443-2-1 | IEC 62443-2-1. Library: Ed 2.0. Recognized: Ed 1.0 2010. | `iec62443-2-1{ed2.0}b.pdf`; `iec62443-2-4{ed2.0}b.zip` (not opened) | **Recognized (other edition) 13-61:** IEC 62443-2-1 Ed 1.0 2010-11, entry 2013-08-06. Also recognized and not in library: IEC TS 62443-1-1:2009 (13-60) and IEC TR 62443-3-1:2009 (13-62). | context: asset-owner programme | Ed 2.0 cannot support a DoC |
| STD-UL2900-1 | ANSI/UL 2900-1, Software Cybersecurity for Network-Connectable Products, Part 1: General Requirements | `ANSI+UL+2900-1-2026+(2026).pdf`: ANSI/CAN/UL 2900-1:2026, **Second Edition** dated Dec 13 2023, revisions through June 29 2026 (read with pymupdf after pypdf failed) | **Recognized (other edition) 13-96:** UL/ANSI 2900-1 **First Edition 2017**. Complete. List 047, entry 2017-08-21. SIS: may not satisfy 524B; cites 524B. | conditional: sponsor uses UL 2900 for security testing (FDA-CY fn 48: may partially meet testing recommendations) | A DoC to the 2nd edition cannot use 13-96, so it is general use. Clause structure of the 2nd edition: 4–6 documentation, 7–11 risk controls, 12 vendor risk management, 13 software composition analysis, 14 malware, 15 malformed input, 16 structured penetration testing, 17 weakness analysis, 18 static binary analysis. Check test lab identity and accreditation. |
| STD-UL2900-2-1 | UL 2900-2-1, Part 2-1: Particular requirements for network connectable components of healthcare and wellness systems | `s2900-2-1_1.pdf`: ANSI/CAN/UL 2900-2-1 **First Edition** (Sept 1 2017), **revision dated Sept 21 2023** (read with pymupdf) | **Recognized 13-104:** UL/ANSI 2900-2-1 First Edition 2017. Complete. List 049, entry 2018-06-07. SIS: may not satisfy 524B. Same edition as the library copy, but **UNVERIFIED** whether the recognition covers the 2023 revision text (the SIS does not mention revisions). | conditional: as UL 2900-1 | Healthcare-specific: safety-related security risk management (12.x), documentation for product use (6.1–6.2). Check which revision the lab tested to. |
| STD-IEEE2621 | IEEE/UL 2621.2-2022, Wireless diabetes device security | **NOT IN LIBRARY** | **Recognized 13-128.** Complete. Entry 2022-12-19. | conditional: connected diabetes device | None |
| STD-11073-40101 | IEEE Std 11073-40101-2020, Cybersecurity: processes for vulnerability assessment | **NOT IN LIBRARY** | **Recognized, partial, 13-117.** **Subclause 8.6 (Iteration) is not recognized**: it conflicts with the postmarket cybersecurity guidance VII.B, TIR57 6.6 and ISO 14971 7.3/7.5. Entry 2021-06-07. | conditional: 11073 interoperability claimed | A DoC must not claim 8.6 |
| STD-11073-40102 | IEEE Std 11073-40102:2020, Cybersecurity: capabilities for mitigation. Library holds ISO/IEEE 11073-40102:2022. | `ISO+IEEE+11073-40102-2022.pdf` | **Recognized 13-118** (IEEE 2020). Complete. Entry 2021-06-07. SIS: may not satisfy 524B. **UNVERIFIED** whether the ISO/IEEE 2022 adoption is accepted under 13-118 (not listed in the record). | conditional: as above | Check the designation cited |
| STD-CR515 | AAMI CR515:2025, Cybersecurity considerations unique to ML-enabled medical devices | `AAMI+CR515-2025-2.pdf` | **Recognized 13-153.** Complete. List 065, entry 2025-12-22. SIS: may not satisfy 524B. | conditional: ML-enabled and connected | Clauses 4 (threat modeling for ML-enabled devices), 5 (ML life cycle), 6 (threats, vulnerabilities, mitigations). Check that ML threats appear in the threat model (L2-30.06). |

### B4. Vulnerability disclosure, handling and scoring

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-29147 | ISO/IEC 29147, Vulnerability disclosure | `ISO+IEC+29147-2018.pdf`; `INCITS+ISO+IEC+29147+2018+(R2024).pdf` (both 2nd ed. 2018) | **Recognized (other edition) 13-77:** ISO/IEC 29147 **First edition 2014-02-15**. Complete. List 040, entry 2015-08-14. SIS: may not satisfy 524B. | conditional: device with cybersecurity risk. The CVD process is recommended (FDA-CY VI.B) and is statutory for cyber devices (524B(b)(1)); conformity to this standard is one route. | A DoC to the 2018 edition cannot use 13-77, so it is general use. Check the policy elements (9.2–9.4), report receipt (6.2.x) and advisory elements (7.4.1–7.4.17) against plan item L2-25.04. |
| STD-30111 | ISO/IEC 30111, Vulnerability handling processes | `ISO+IEC+30111-2019.pdf`; `INCITS+ISO+IEC+30111+2019+(2024)-3.pdf` (2nd ed. 2019) | **Recognized (other edition) 13-78:** INCITS/ISO/IEC 30111 **First edition 2013-11-01 (R2019)**. Complete. List 040, entry 2015-08-14. SIS: may not satisfy 524B. | conditional: as above | Handling phases 7.1.2–7.1.7, monitoring 7.2, supply chain 8, against L2-25.08. |
| STD-CVSS | FIRST Common Vulnerability Scoring System | **NOT IN LIBRARY** (free FIRST specification) | **Recognized:** v4.0 **13-140** (List 066, entry 2026-05-25); v3.1 **13-142** (List 064, entry 2025-05-26; SIS transition: DoC to v3.1 accepted until **2028-07-02**); v3.0 **13-116** (SIS transition: DoC accepted until **2026-12-20**; the v3.0 SIS ties it to the FDA-qualified MITRE rubric as a Medical Device Development Tool, MDDT). | conditional: sponsor scores vulnerabilities with CVSS | Version stated; environmental score and rubric use; reproducibility of pre- and post-mitigation scores (L2-15.01). |
| STD-HN1 | ANSI/NEMA HN 1-2019, Manufacturer Disclosure Statement for Medical Device Security (MDS2) | **NOT IN LIBRARY** | **Recognized 13-123.** Complete. Entry 2022-12-19. SIS: may not satisfy 524B. | conditional: MDS2 used as labeling vehicle (FDA-CY VI.A) | MDS2 revision and software version match the proposed release |

### B5. Usability

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-62366-1 | IEC 62366-1:2015+AMD1:2020 (Ed 1.1 CSV), Application of usability engineering to medical devices | `iec62366-1{ed1.1}b.pdf`; `ANSI+AAMI+IEC+62366-1-2015+(R2021)+AMD1-2020-2.pdf` (also `iec62366-1{ed1.0}b.pdf`, older edition) | **Recognized 5-129.** Ed 1.1 2020-06 CSV; identical ANSI/AAMI IEC 62366-1:2015+AMD1:2020. Complete. List 054, entry 2020-07-06. Ed 1.0 alone was not returned by the database. | expected: usability engineering file interface | Process standard, so supplemental documentation is required (the usability engineering file summary or HFE/UE report). Check: 5.1 use specification; 5.2–5.4 use errors and hazard-related use scenarios; 5.5 summative selection and rationale; 5.6 UI specification; 5.7.3 a)–e) summative planning; **5.9 summative on the final or production-equivalent UI**. The FDA HF Submission Category (FDA-HFC26) decides what content is submitted. |
| STD-62366-2 | IEC TR 62366-2:2016 Ed 1.0, Guidance on usability engineering | `iec62366-2{ed1.0}en.pdf` | **Not recognized** (the "62366" search returned only 5-129) | context | None |
| STD-HE75 | ANSI/AAMI HE75, Human factors engineering — Design of medical devices | `ANSI+AAMI+HE75-2025.pdf` (2025 edition, added during run) | **Recognized (other edition), partial, 5-57:** ANSI/AAMI HE75:2009/(R)2018, List 043, entry 2016-06-27. **Section 9 (Usability testing) is not recognized**: it conflicts with HF guidance section 8. | context | A DoC to the 2025 edition cannot use 5-57. Never accept HE75 section 9 in place of FDA HF validation. |

### B6. Testing, defects and process documentation

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-SW91 | ANSI/AAMI SW91:2018, Classification of defects in health software | `ANSI+AAMI+SW91-2018.pdf` | **Recognized 13-105.** Complete. List 051, entry 2019-01-14. SIS: may not satisfy 524B. | expected: a defect taxonomy is recommended (FDA-SW VI.J); SW91 or an equivalent | Defect codes (4) and taxonomy (5) applied per anomaly. CWE mapping (Annex D) supports FDA-CY V.A.5. Severity is assessed separately from the code. |
| STD-29119-1 | ISO/IEC/IEEE 29119-1:2022, Software testing — Part 1: General concepts | `ISO+IEC+IEEE+29119-1-2022.pdf` | **Recognized 13-129** (2nd ed. 2022-01). Complete. List 061, entry 2023-10-09. The 1st edition 2013 (**13-115**, entry 2020-07-06) is **also still listed with no transition statement** (ambiguous). | context: vocabulary | None |
| STD-29119-2 | ISO/IEC/IEEE 29119-2:2021, Test processes | `ISO+IEC+IEEE+29119-2-2021.pdf` | **Not recognized** (the "29119" search returned only 13-115 and 13-129) | context | Source for test-process L3 parameters |
| STD-29119-3 | ISO/IEC/IEEE 29119-3:2021, Test documentation | `ISO+IEC+IEEE+29119-3-2021.pdf` | **Not recognized** | context | Source for L3 parameters: 7.2 test plan, 7.3 status, 7.4 completion report, 8.3 test case specification, 8.4 procedure, 8.6 and 8.8 environment, 8.9 results, 8.10 execution log, 8.11 incident report |
| STD-29119-4 | ISO/IEC/IEEE 29119-4:2021, Test techniques | `ISO+IEC+IEEE+29119-4-2021.pdf` | **Not recognized** | context | None |
| STD-29119-5 | ISO/IEC/IEEE 29119-5:2024, Keyword-driven testing | `ISO+IEC+IEEE+29119-5-2024.pdf` | **Not recognized** | context | None |
| STD-TR29119-11 | ISO/IEC TR 29119-11:2020, Testing of AI-based systems; also INCITS/ISO/IEC TR 29119-6:2021 (agile) | `ISO+IEC+TR+29119-11-2020.pdf`; `INCITS+ISO+IEC+TR+29119-6+2021+(2023).pdf` | **Not recognized** | context (ML or agile) | None |
| STD-15289 | ISO/IEC/IEEE 15289:2019 (content of life-cycle information items). Context group: ISO/IEC/IEEE 14764:2022, 24748-x, 24765:2017, 90003:2018, 16326:2019, 21839:2019, 26511/26515:2018, ISO/IEC 33063:2015. | the files with those names | **Not recognized:** 15289, 14764, 90003, 24748 and 33063 searched, no records. 24765, 16326, 21839, 26511 and 26515 were not searched (UNVERIFIED). | context | None |
| STD-TIR36 | AAMI TIR36:2007, Validation of software for regulated processes | **NOT IN LIBRARY** | **Recognized 13-33.** Complete. Entry 2013-01-15. | context: production/QMS software | None |

### B7. AI/ML (beyond B2 and B3)

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-23053 | ISO/IEC 23053:2022, Framework for AI systems using ML | `ISO+IEC+23053-2022.pdf` | **Not recognized** | context (ML) | None |
| STD-TR24027 | ISO/IEC TR 24027:2021, Bias in AI systems | `ISO+IEC+TR+24027-2021.pdf` | **Not recognized** | context (ML) | Bias methods (L2-30.04) |
| STD-TR24028 | ISO/IEC TR 24028:2020, Trustworthiness in AI | `ISO+IEC+TR+24028-2020.pdf` | **Not recognized** | context | None |
| STD-TR24372 | ISO/IEC TR 24372:2021, Computational approaches for AI systems | `ISO+IEC+TR+24372-2021.pdf` | **Not recognized** (search "24372": no records) | context | None |
| STD-VV40 | ASME V&V 40-2018, Credibility of computational modeling | **NOT IN LIBRARY** | **Recognized 5-122.** Complete. Entry 2019-01-14. | conditional: computational model used as evidence | None |

### B8. Networked IT risk, interoperability, assurance cases and organizational security

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-80001-1 | IEC 80001-1, Application of risk management for IT-networks incorporating medical devices | `IEC+80001-1-2021.pdf` (2021, "Part 1: Safety, effectiveness and security…"); `ANSI+AAMI+IEC+80001-1-2010.pdf` | **Recognized (2010 edition only) 13-38:** IEC 80001-1 Ed 1.0 2010-10 (identical ANSI/AAMI/IEC 80001-1:2010), Complete, entry 2013-08-06. The **2021 edition is not recognized** (only the 2010 record was returned). | context: health delivery organization (HDO) duties. The 2021 Annex B informs accompanying information. | A sponsor DoC is unusual. Use Annex B (2021) as a check-list for network information in labeling. |
| STD-TR80001-2 | IEC TR 80001-2-1 to 2-9 series | **NOT IN LIBRARY** | **Recognized:** 2-1 **13-40**; 2-2 **13-42**; 2-3 **13-44**; 2-4 **13-63**; 2-5 **13-70**; ANSI/AAMI/ISO TIR80001-2-6:2014 **13-82**; 2-8 **13-102**; 2-9 **13-103**. All Complete. | context. FDA-CY VI.A fn 52 cites 2-2, 2-8 and 2-9 for security labeling content. | None |
| STD-UL2800 | ANSI/AAMI/UL 2800-1:2022 interoperability series | **NOT IN LIBRARY** | **Recognized:** 2800-1 **13-121**; 2800-1-1 **13-125**; 2800-1-2 **13-126**; 2800-1-3 **13-127** (all entry 2022-12-19) | conditional: interoperable medical product claims | None |
| STD-AUTO11 | CLSI AUTO11-A2, IT security of in vitro diagnostic instruments and software systems; also CLSI AUTO09-A (remote access) | **NOT IN LIBRARY** | **Recognized:** AUTO11-A2 **7-344** (List 064, entry 2025-05-26); AUTO09-A **7-339** (entry 2025-05-26) | conditional: IVD instrument or software (relevant to this book's NGS and digital pathology cases) | Security controls and labeling for laboratory IT integration |
| STD-81001-1 | ISO 81001-1:2021, Health software and health IT systems — Principles and concepts | `ISO+81001-1-2021-2.pdf` | **Not recognized** (the "81001" search returned only 13-122) | context | None |
| STD-TS81001-2-1 | ISO/TS 81001-2-1:2025, Assurance cases for safety and security | `ISO+TS+81001-2-1-2025.pdf` | **Not recognized** | context | None |
| STD-15026 | ISO/IEC 15026 systems and software assurance | `ISO+IEC+IEEE+15026-1-2019.pdf` | **Recognized (other edition):** ISO/IEC 15026-1 **2013** (**13-86**); 15026-2:2011 (**13-87**); record 13-59 now shows ISO/IEC/IEEE 15026-4 First ed. 2021-10-01 (its date of entry still reads 2013-08-06). The library 15026-1:2019 is not a recognized edition. | context | None |
| STD-27001 | ISO/IEC 27001 (ISMS); also 27002 | **NOT IN LIBRARY** | **Not recognized** (searches "27001" and "27002": no records) | context: manufacturer or cloud-provider organizational security, and third-party service organizations (SW96 Annex E) | A certificate does not substitute for device security evidence |
| STD-TS27100 (incl. STD-TS27110) | ISO/IEC TS 27100:2020 (cybersecurity concepts); ISO/IEC TS 27110:2021 (framework development) | `ISO+IEC+TS+27100-2020.pdf`; `ISO+IEC+TS+27110-2021.pdf` | **Not recognized** (both searched) | context | None |

### B9. Labeling, QMS and conformity assessment

| ID | Standard and title | Library file(s) | FDA recognition | Class | Reviewer checks |
|---|---|---|---|---|---|
| STD-13485 | ISO 13485:2016, QMS | `ISO+13485-2016.pdf`; `ANSI+AAMI+ISO+13485-2016+(R2019).pdf` | **No database record** (search "13485": no records). It is incorporated by reference into 21 CFR 820 (QMSR), so it is a legal obligation, not a voluntary-recognition item. | context for the module | Not a DoC item. FDA-CY cites 7.3, 7.4, 7.5, 8.4 and 8.5 as homes for security processes. |
| STD-20417 | ISO 20417:2026 (2nd ed.), Information to be supplied by the manufacturer | `ISO+20417-2026.pdf` | **Recognized 5-149.** Complete. List 066, entry 2026-05-25. SIS transition: the 2021 edition (5-135) DoC is accepted until **2029-07-01**. | context for the software module (labeling filed in the final module) | Edition and transition |
| STD-15223-1 | ISO 15223-1:2021+AMD1:2025, Symbols | **NOT IN LIBRARY** (library has ISO 15223-2:2010 in `example list of standards for poc/`) | **Recognized 5-148.** Transition: the 2021 edition (5-134) DoC is accepted until **2028-12-17**. | context | None |
| STD-17025 | ISO/IEC 17025:2017, Competence of testing and calibration laboratories | `ISO+IEC+17025-2017.pdf` | **Not recognized** (search "17025": no records) | conditional: third-party test lab accreditation cited | Accreditation body and scope cover the method relied on (FDA-STD IV.A) |
| STD-17050 | ISO/IEC 17050-1 and -2, Supplier's declaration of conformity | **NOT IN LIBRARY** | **Not recognized** (search "17050": no records; not a device standard) | context: DoC format referenced by FDA-STD IV.A(1) and (2) | Format, plus 17050-2 supporting documentation |

---

## C. Non-consensus references named by FDA guidance

| ID | Reference | Library file | Named in | Use |
|---|---|---|---|---|
| REF-NTIA-SBOM | NTIA "The Minimum Elements for a Software Bill of Materials" (July 2021). FDA-CY cites the Oct 2021 NTIA "Framing Software Component Transparency" baseline attributes. | `other/NTIA-SBOM-Minimum-Elements-2021.pdf` (Framing document **not in library**) | FDA-CY V.A.4(b) | Data fields: Supplier, Component Name, Version, Other Unique Identifiers, Dependency Relationship, Author of SBOM Data, Timestamp (opened). FDA adds level of support and end-of-support date. |
| REF-CISA-KEV | CISA Known Exploited Vulnerabilities Catalog | online | FDA-CY V.A.2, V.A.4(b), VI.B | Should be designed out of the device; must be monitored |
| REF-CWE | MITRE Common Weakness Enumeration | online | FDA-CY V.A.5; SW91 Annex D | Anomaly security assessment |
| REF-MITRE-RUBRIC | MITRE rubric for applying CVSS to medical devices (FDA-qualified MDDT) | not in library | SIS 13-116; SW96 C.3 | Scoring |
| REF-PLAYBOOK | MITRE/MDIC Playbook for Threat Modeling Medical Devices (Nov 30 2021) | `Playbook-for-Threat-Modeling-Medical-Devices.pdf` (added during run) | FDA-CY V.A.1 fn 34 | Methodology reference |
| REF-JSP2 | Medical Device and Health IT Joint Security Plan v2 | not in library | FDA-CY V; VI.A (customer security documentation) | Alternative SPDF framework |
| REF-NIST-CSF | NIST Cybersecurity Framework 2.0 (CSWP 29, 2024) | `other/NIST-CSF-2.0-CSWP29-2024.pdf` | FDA-CY V (HDO frameworks) | Context |
| REF-NIST-800-30 | NIST SP 800-30 Rev. 1 (2012) | `other/NIST-SP800-30r1-Risk-Assessment-2012.pdf` | SW96 C.5 (control strength, Table D-3) | Context |
| REF-NIST-800-160 | NIST SP 800-160 Vol. 1 Rev. 1 | not in library | FDA-CY V.B fn 42 | Context |

---

## Library gaps

These standards are `expected` or `conditional` for the software module, or were specifically asked about, and are missing from the library or present only in an edition FDA does not recognize. The library was re-listed at 15:40 EDT on 2026-10-01. Items added during this run are **not** reported as missing.

### Absent from the library

| Item | Class | FDA status | Note |
|---|---|---|---|
| IEC 60601-1-8 Ed 2.2 (alarms) | conditional | Recognized 5-131 | Needed only if ME equipment raises alarms |
| IEEE 11073-40101-2020 | conditional | Recognized, partial, 13-117 | Library has 40102 only |
| ANSI/NEMA HN 1-2019 (MDS2) | conditional | Recognized 13-123 | Labeling vehicle |
| FIRST CVSS v3.1 / v4.0 specifications | conditional | 13-142 / 13-140 | Freely available; not stored |
| IEC TR 80001-2-2, -2-8, -2-9 (and the rest of the series) | context | Recognized 13-42, 13-102, 13-103 | Cited by FDA-CY VI.A fn 52 |
| ANSI/AAMI/UL 2800-1 series | conditional | 13-121, 13-125 to 13-127 | Interoperability claims |
| IEEE/UL 2621.2-2022 | conditional | 13-128 | Diabetes devices only |
| CLSI AUTO11-A2 and AUTO09-A | conditional (IVD) | 7-344, 7-339 | Relevant to the IVD cases in this project |
| ASME V&V 40-2018 | conditional | 5-122 | Computational models |
| AAMI TIR36:2007 | context | 13-33 | Production software |
| ISO/IEC 17050-1 and -2 | context (DoC format) | not a recognized device standard | Referenced by FDA-STD |
| ISO/IEC 27001 / 27002 | context | Not recognized | The task asked whether this family is relevant. It is relevant only to organizational and cloud security, not to a device DoC. |
| IEC TR 60601-4-5:2021 | context | Not recognized | Absent, as the coordinator noted |
| NTIA "Framing Software Component Transparency" (Oct 2021) | expected content reference | n/a | The document FDA-CY actually cites. Minimum Elements (July 2021) is present instead. |
| FDA "Cybersecurity for Networked Medical Devices Containing OTS Software" (2005) | context | guidance; current status not checked | Still cited by FDA-SW II. A mislabeled copy (`fda/FDA-Cybersecurity-Networked-Devices-OTS-2005.pdf`) briefly held the bytes of the 2026 guidance (same SHA-256) and was later removed. |
| Current CSA guidance (Feb 3 2026) | context | final guidance | The library copy is the superseded Sept 24 2025 edition |

### Present but not the FDA-recognized edition or designation

A DoC to the library edition is not possible; only general use with underlying data is.

| Library edition | Recognized edition |
|---|---|
| ISO/IEC 29147:2018 (two copies) | 2014, 13-77 |
| ISO/IEC 30111:2019 (two copies) | 2013 (R2019), 13-78 |
| ANSI/CAN/UL 2900-1:2026 (2nd ed.) | 1st ed. 2017, 13-96 |
| AAMI TIR34971:2023 | AAMI CR34971:2022, 13-124 (equivalence UNVERIFIED) |
| ANSI/AAMI HE75:2025 | HE75:2009/(R)2018, partial, 5-57 |
| IEC 62443-2-1 Ed 2.0 | Ed 1.0 2010, 13-61 |
| ISO/IEC/IEEE 15026-1:2019 | ISO/IEC 15026-1:2013, 13-86 |
| IEC 80001-1:2021 | 2010, 13-38 |
| IEC 60601-1 Ed 3.1 | Ed 3.2 is recognized and is also in the library |

### Present, with acceptance under the recognition UNVERIFIED

| Library edition | Recognition record | Open question |
|---|---|---|
| IEC 62443-4-1:2018 | ANSI/ISA-62443-4-1-2018, 13-119 | The record names only the ANSI/ISA designation |
| ISO/IEEE 11073-40102:2022 | IEEE 2020, 13-118 | The ISO/IEEE adoption is not listed |
| UL 2900-2-1 First Edition with the 2023 revision | 13-104, "First Edition 2017" | The SIS does not mention revisions |
| AAMI TIR57 (R2023) and TIR97 (R2023) | 13-83 (TIR57:2016) and 13-112 (TIR97:2019) | Whether the reaffirmed printings are covered |
| IEC 81001-5-1 ISH1:2025 | 13-122 | Not mentioned in the SIS |

### Unreadable library files

- `30416038.pdf` and `30416046.pdf`: DRM-encrypted. pypdf reports a non-standard security handler, and both PDFKit and pymupdf failed to open them. Their identity is unknown, so they may be relevant BSI documents.
- `iec62443-2-4{ed2.0}b.zip`: not opened.

### Specific items the task asked about

| Item | Status |
|---|---|
| UL 2900-1 | Present, but only the 2nd edition (recognized edition is the 1st) |
| UL 2900-2-1 | Present (1st edition, 2023 revision) |
| IEC 60601-1 clause 14 | Present (Ed 3.2 and Ed 3.1) |
| AAMI TIR45 | Present (2023, the recognized edition) |
| 2026 FDA cybersecurity guidance PDF | Present (added during the run) |
| FDA human factors guidances | Both present (2026 content guidance; 2016 guidance as reissued Aug 2026) |
| ISO/IEC 27001 family | Absent; context only |

---

## Declaration of Conformity checks

These checks apply to **every** declaration in the module. Each item cites its source and the BIN-HIERARCHY parameter where the value is captured.

| # | Parameter to verify | What the review compares | Source | BIN-HIERARCHY |
|---|---|---|---|---|
| 1 | Standard identifier (organization, designation) | Matches a database record. An identical adoption (for example ANSI/AAMI) must be the one named in the SIS. | FDA-STD IV.A(1) d; IV.A(3) b; eSTAR Consensus Standards fields "Organization", "Designation Number and Edition/Date", "Title" (field names from an earlier template transcript; the v7.1 and draft PMA eSTAR sub-fields were not opened) | L2-28.01.standard_designation_and_edition |
| 2 | Edition, amendment or date | String-equal to the recognized edition, or to an outgoing edition still inside its SIS transition window at the submission date. Withdrawn editions are rejected. | FDA-STD IV fn 8; V; VIII | L2-28.02.recognized_edition_db, transition_expiry_date, withdrawn_flag |
| 3 | FDA recognition number | Present and corresponds to the cited edition (for example 62304 → 13-79; 14971 → 5-125; 62366-1 → 5-129; 81001-5-1 → 13-122; SW96 → 13-131). A DoC may only refer to standards with a recognition number. | FDA-STD IV (para. 2); IV.A(1) e; IV.A(3) b; eSTAR "Recognition#" | L2-28.01.fda_recognition_number |
| 4 | Extent of recognition and clauses claimed | Claimed clauses avoid any part FDA does not recognize (for example 11073-40101 8.6; HE75 section 9). For IEC 62304 at Enhanced level the clauses must include **5.1, 6 and 8** (FDA-SW VI.G(2)). | FDA-STD IV fn 8; FDA-SW VI.G; database SIS "Extent of Recognition" | L2-28.02.extent_of_recognition_db; L2-28.03.clauses_claimed |
| 5 | Options selected | Stated wherever the standard offers choices (for example 62304 safety class, test methods), with an explanation of each choice | FDA-STD IV.A(1) d; IV.A(3) bullet 3 | L2-28.01.options_selected; L2-28.05.choices_explained |
| 6 | Exclusions and deviations | No deviation from the normative part. Any deviation turns the declaration into general use, which needs 814.20(b)(5)(ii) "explain any deviation". | FDA-STD IV (no deviation in a DoC); IV.A(3) c; IV.B; 21 CFR 814.20(b)(5)(ii) | L2-28.03.deviations_declared |
| 7 | Statement of conformity, and no promissory statement | Conformance is complete at submission. No "will conform" language. | FDA-STD IV.A (testing completed before submission); VI; IV.A(3) g | L2-28.01.statement_of_conformity; L2-28.07 |
| 8 | Date and place of issue | Issued on or before the module submission date, and after the completion date of the evidence relied on | FDA-STD IV.A(1) f | L2-28.01.date_of_issue; CC-12 j/k |
| 9 | Product identification and applicability to the proposed build or configuration | Device name, model and software version equal the proposed version. The standard's scope covers the device, or an explanation is given. Tests were on the final finished device, or differences are justified. | FDA-STD IV.A(1) b; IV.A (scope; final finished device); IV.A(3) d | L2-28.01.product_identification; L2-28.04 |
| 10 | Signatory | Printed name, function and signature of the person responsible | FDA-STD IV.A(1) g | L2-28.01.signatory_name_function |
| 11 | Limitations on validity | What was tested, validity period, concessions; "none" stated explicitly | FDA-STD IV.A(1) h | L2-28.01.limitations_on_validity |
| 12 | Applicant | Name and address equal the module applicant | FDA-STD IV.A(1) a | L2-28.01.applicant_name_address |
| 13 | Test laboratory or certification body and accreditation | Name, address and accreditation references for each third party. The accreditation scope covers the method. ASCA participation where claimed. | FDA-STD IV.A (third-party paragraph); eSTAR option "DoC with ASCA" | L2-28.06 |
| 14 | Supplemental documentation | For process or horizontal standards and standards with choices or no acceptance criteria (ISO 14971, IEC 62304, IEC 62366-1, IEC 81001-5-1, SW96): a summary report or the underlying plans and records, per ISO/IEC 17050-2 and FDA-STD Table 1 | FDA-STD IV.A(2); IV.A(3) e–f; Table 1 | L2-28.05 |
| 15 | SIS cautions | For cybersecurity standards, the SIS states that conformance may not satisfy 524B or FDA-CY recommendations. A DoC never closes L1-13 to L1-26 by itself. | Database SIS for 13-122, 13-131, 13-83, 13-112, 13-119, 13-96, 13-104, 13-77, 13-78, 13-105, 13-153, 13-123 | L2-28.02.sis_notes |
| 16 | Module placement | Each module carries its own "Declaration of Conformance to Standards for Module". The PMA filing checklist item 12.a asks for a DoC or general-use basis for every cited standard. | FDA-MODPMA Appendix II; FDA-PMAFILE item 12.a.i–ii | L2-28.09 |
| 17 | Records retained | The sponsor maintains the data behind the DoC. FDA may request it at any time (FD&C Act 514(c)(3)(B), as cited by FDA-STD). | FDA-STD IV.A | L2-28.04.underlying_evidence_ids |

Regulatory hooks for the checks above:

- **21 CFR 814.20(b)(5):** reference voluntary standards known, or reasonably known, to the applicant, and explain deviations. CC-24 makes this check mechanical against the `expected` rows above.
- **FD&C Act 514(c):** basis of DoC as cited by FDA-STD. The Act itself was not opened.
- **PMA eSTAR:** the draft guidance (Sept 18 2026) lists a "Consensus Standards" section mapped to 814.20(b)(5). The eSTAR program page says the DoC is built into the template. Modular modules are excluded from PMA eSTAR, so for a software module the DoC is a standalone document checked against items 1–17.

## Recognition lookup log

- **Method.** HTTPS GET of `results.cfm` with `referencenumber=<designation>` and `pagenum=500`, followed by `detail.cfm?standard__identification_no=<id>` for each hit. Fields were parsed from the SIS (Part B): FR Recognition List Number, Date of Entry, FR Recognition Number, Standard, Extent of Recognition, Rationale, Transition Period. Raw pages are saved in the session scratchpad and are not part of the deliverable.
- **Designation searches run.** 62304, 82304, 81001, 14971, 24971, TIR24971, 34971, 62366, 62366-1, 62366-2, 60601-1, 60601-1-6, 60601-4-5, SW96, TIR57, TIR97, SW91, 80001, 62443, 62443-4-2, 62443-3-3, 29147, 30111, 29119, 2900, 2900-1, 2900-2-1, 80002, TIR80002, 13485, 20417, 27001, 27002, 27100, 27110, 15026, 23053, 24027, 24028, 24372, TIR45, TIR105, 17025, 17050, 11073-40101, 2621, SW87, 15223, CR515, CR510, 42001, 23894, TIR32, TIR36, SW68, 25010, 20243, 1012, 1633, HE75, 5338, 24029, TIR101, V&V 40, 16085, 12207, 15288, 81001-1, TIR86, SW101, TIR102, TIR109, TIR113, 2700, HN 1, CVSS, TS 5615, 15289, 90003, 14764, 33063, 24748.
- **Title or keyword searches** (used to find records only): cybersecurity, security, software, artificial intelligence, machine learning, usability, human factors, risk management.
- **Counts.**
  - Detail records read: 121.
  - Recognition facts stated as verified in this register: **60** recognition numbers, each read from its SIS detail page. This includes outgoing editions inside a transition window: 13-36, 13-116, 5-134 and 5-135.
  - **Not recognized, by negative search:** 23 register rows covering about 35 designations. Not recognized is also recorded for non-recognized editions of recognized standards. The search behaviour was confirmed by positive control: every known-recognized designation returned its record.
  - **UNVERIFIED:** 8 recognition questions. Six are listed under "Present, with acceptance under the recognition UNVERIFIED" (62443-4-1 IEC vs ANSI/ISA; ISO/IEEE 11073-40102:2022; the UL 2900-2-1 2023 revision; the TIR57 R2023 printing; the TIR97 R2023 printing; 81001-5-1 ISH1). The other two are the CR34971/TIR34971 designation and the 29119-1 status (two editions listed, no transition). In addition, five context designations were not searched: 24765, 16326, 21839, 26511 and 26515.
- **No recognition number in this register was taken from memory.**
