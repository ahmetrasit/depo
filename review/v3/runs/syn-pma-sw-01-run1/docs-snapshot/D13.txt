# Unresolved Software Anomalies

**Document ID:** D13-Unresolved-Anomalies  
**Document version:** 1.2  
**Approval date:** 2026-04-11  
**Approved by:** K. Novak, V&V Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Scope
Unresolved anomalies for the release candidate, build **b1180**, software version 3.2.0, extracted from the problem tracker (Jira project ARR, filter "Open AND fixVersion != 3.2.0") on **2026-04-05**.

**Open anomalies: 5** (0 critical, 1 major, 4 minor).

## 2. Anomaly records
| Anomaly | Description | Discovery | Affected versions | Class (SW91) | Disposition | Risk file link | Security impact assessed |
|---|---|---|---|---|---|---|---|
| ANM-101 | Audit export truncates entries > 4 kB | system test | 3.2.0 | minor | 2026-04-02 fixed in b1187 hotpatch? no: deferred, workaround documented | H-none | yes |
| ANM-102 | About screen shows build date in UTC not local | system test | 3.1.4, 3.2.0 | minor | deferred | — | yes |
| ANM-103 | Episode list scroll jitter on Hub v2 | formative usability | 3.2.0 | minor | deferred | — | yes |
| ANM-104 | Classification latency 2.4 s under max load (requirement 2 s) | system test | 3.2.0 | major | deferred to 3.2.1; risk file H-07 updated | H-07 | yes |
| ANM-105 | Lead-off indicator flickers at low battery | field (prior version) | 3.1.4, 3.2.0 | minor | deferred | H-04 | yes |
| ANM-106 | Portal sync retry counter not reset after success | integration test | 3.2.0 | minor | deferred | — | yes |

## 3. Workarounds communicated
ANM-104: reduce concurrent synchronisation during continuous monitoring (IFU section 9.3). ANM-101: export audit log in 4 kB pages.
