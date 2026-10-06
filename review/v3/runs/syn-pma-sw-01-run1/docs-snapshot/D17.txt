# Cybersecurity Risk Assessment and Report

**Document ID:** D17-Security-Risk-Assessment  
**Document version:** 2.0  
**Approval date:** 2026-04-09  
**Approved by:** E. Varga, Product Security Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Method
Security risk management plan SRMP-ARR-01 (approved 2025-06-20) per ANSI/AAMI SW96:2023; scoring with CVSS v3.1 base and the MITRE medical device rubric for exploitability; acceptance threshold: post-mitigation exploitability ≤ 3.0 and no unmitigated high.

## 2. Security risk entries
| Risk | Threat | Vulnerability / weakness | Controls | Pre-mitigation | Post-mitigation | Status | Evaluation date |
|---|---|---|---|---|---|---|---|
| SR-01 | T-01 | CWE-347 improper signature verification | SC-01 | 7.8 (CVSS 3.1 base) / exploitability high | 2.1 | controlled | 2026-04-08 |
| SR-02 | T-02 | CWE-307 excessive auth attempts | SC-02, SC-10 | 6.5 / medium | 2.0 | controlled | 2026-04-08 |
| SR-03 | T-03 | CWE-311 missing encryption | SC-03 | 6.1 / medium | 1.5 | controlled | 2026-04-08 |
| SR-04 | T-04 | CWE-295 improper certificate validation | SC-04, SC-06 | 8.1 / high | 2.2 | controlled | 2026-04-08 |
| SR-05 | T-05 | CWE-117 log tampering | SC-05, SC-09 | 5.3 / medium | 2.0 | controlled | 2026-04-08 |
| SR-06 | T-06 | CWE-294 replay | SC-07 | 7.1 / high | 2.5 | controlled; safety transfer to HS-02 | 2026-04-08 |
| SR-07 | T-07 | CWE-400 resource exhaustion | SC-08 | 5.9 / medium | 2.0 | controlled; safety transfer to HS-07 | 2026-04-08 |
| SR-08 | T-08 | CWE-287 improper authentication | SC-10, SC-06 | 7.5 / high | 2.0 | controlled | 2026-04-08 |

## 3. Residual security risk
All entries below threshold. Overall residual security risk acceptable (E. Varga, 2026-04-09).

## 4. Risks arising from controls
Lockout (SC-02) can delay clinician access: transferred to usability task T7 (D07 Annex F).

## 5. Report
Security risk management report SRMR-ARR-3.2 Rev 2.0 dated **2026-04-09**, software version covered **3.2.0**; traceability in section 7; version history: Rev 1.0 (3.1.0), Rev 2.0 (3.2.0).

## 6. Transfer to safety risk management
SR-06 → HS-02 (false episode from injected frames; security origin). SR-07 → HS-07 (overload). Both recorded in D07 section 2.

## 7. Traceability
Threat → risk → control → requirement → test: T-01/SR-01/SC-01/SEC-001/ST-01, ST-02; T-02/SR-02/SC-02,SC-10/SEC-002/ST-03; T-03/SR-03/SC-03/SEC-003/ST-04; T-04/SR-04/SC-04,SC-06/SEC-004,SEC-006/ST-05; T-05/SR-05/SC-05,SC-09/SEC-005/ST-06; T-06/SR-06/SC-07/SRS-001/ST-07; T-07/SR-07/SC-08/SRS-024/ST-07; T-08/SR-08/SC-10,SC-06/SEC-002,SEC-006/ST-05. Export date 2026-04-09.
