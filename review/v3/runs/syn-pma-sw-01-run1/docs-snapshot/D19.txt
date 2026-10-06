# Cybersecurity Testing Report

**Document ID:** D19-Security-Testing  
**Document version:** 1.1  
**Approval date:** 2026-04-08  
**Approved by:** E. Varga, Product Security Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Security requirements, threat-mitigation and vulnerability testing
| Activity | Type | Version (build) | Dates | Tester | Controls covered | Threats covered | Findings |
|---|---|---|---|---|---|---|---|
| ST-01 | threat mitigation test | 3.2.0 (b1187) | 2026-03-30 to 2026-03-31 | Halden product security team (separate from development) | SC-01 | T-01 | none |
| ST-02 | security requirements test | 3.2.0 (b1187) | 2026-03-30 to 2026-03-31 | Halden product security team (separate from development) | SC-01 | — | none |
| ST-03 | security requirements test | 3.2.0 (b1187) | 2026-04-01 to 2026-04-01 | Halden product security team (separate from development) | SC-02, SC-10 | — | none |
| ST-04 | security requirements test | 3.2.0 (b1187) | 2026-04-01 to 2026-04-02 | Halden product security team (separate from development) | SC-03 | — | none |
| ST-05 | threat mitigation test | 3.2.0 (b1187) | 2026-04-02 to 2026-04-03 | Halden product security team (separate from development) | SC-04, SC-06, SC-10 | T-04, T-08 | none |
| ST-06 | security requirements test | 3.2.0 (b1187) | 2026-04-03 to 2026-04-03 | Halden product security team (separate from development) | SC-05 | — | none |
| ST-07 | vulnerability/fuzz test | 3.2.0 (b1187) | 2026-04-04 to 2026-04-06 | Halden product security team (separate from development) | SC-07, SC-08 | T-06, T-07 | none |

Tools: OWASP ZAP 2.14, boofuzz 0.4.2, Grype 0.74, Halden BLE fuzzer v0.4. Scope: IF-01 to IF-05. No findings; boundary assumptions in Annex B.

## 2. Penetration testing
Penetration test **PT-01** on version **3.1.0** (build **b1098**), **2025-11-03 to 2025-11-14**, performed by Halden internal development team (two engineers from the ARR software team). Tools: nmap 7.94, Burp Suite Pro 2025.9, custom BLE fuzzer v0.3. Scope: IF-01, IF-02, IF-03, IF-04. Methodology: OWASP MASVS/ASVS checklist plus manual exploitation. Duration: 10 person-days. Result: **3 findings (0 critical, 1 high, 2 medium)**. Original report PT-01-R1 is attached (Annex C).

| Finding | Severity | Description | Disposition | Fixed in build | Disposition date |
|---|---|---|---|---|---|
| PF-01 | high | Session token not invalidated at logout | fixed | b1120 | 2025-12-15 |
| PF-02 | medium | Verbose TLS error reveals library version | fixed | b1120 | 2025-12-15 |

No retest was performed; both findings were verified closed by code review. No penetration test has been performed on 3.2.0; the attack surface change of CH-31 (new inbound sync listener) was covered by threat-mitigation test ST-05.

## 3. Findings assessment and deferrals
No deferred security findings. Future-release plan: none required.
