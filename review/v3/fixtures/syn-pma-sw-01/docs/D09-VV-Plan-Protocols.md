# Verification and Validation Plan and Protocol Index

**Document ID:** D09-VV-Plan-Protocols  
**Document version:** 2.0  
**Approval date:** 2026-03-12  
**Approved by:** K. Novak, V&V Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Verification strategy
Unit tests (GoogleTest) per Class C unit; integration tests per interface; system tests per requirement on both hub platforms; software validation in simulated clinical use (SUV-03). Regression: full system regression on each release candidate; selective re-run after late changes per regression analysis RA-nnn (D10 section 5).

## 2. Declared test window
System verification of release candidate b1187: **2026-03-23 to 2026-04-08**.

## 3. Test case and protocol index
| Test case | Level | Requirements / design | Risk control verified | Protocol id / version | Protocol approval | Approver |
|---|---|---|---|---|---|---|
| TC-001 | system | SRS-001 | — | TP-SYS-01 v2.0 | 2026-03-12 | K. Novak |
| TC-002 | system | SRS-002 | RC-01 | TP-SYS-01 v2.0 | 2026-03-12 | K. Novak |
| TC-003 | system | SRS-003 | — | TP-SYS-01 v2.0 | 2026-03-12 | K. Novak |
| TC-004 | system | SRS-004 | RC-02 | TP-SYS-02 v2.0 | 2026-03-12 | K. Novak |
| TC-005 | system | SRS-005 | RC-03 | TP-SYS-02 v2.0 | 2026-03-12 | K. Novak |
| TC-006 | system | SRS-006 | — | TP-SYS-02 v2.0 | 2026-03-12 | K. Novak |
| TC-007 | system | SRS-007 | — | TP-SYS-03 v1.1 | 2026-03-12 | K. Novak |
| TC-008 | system | SRS-008 | RC-04 | TP-SYS-03 v1.1 | 2026-03-25 | K. Novak |
| TC-009 | system | SRS-009 | — | TP-SYS-04 v1.0 | 2026-03-12 | K. Novak |
| TC-010 | system | SRS-010, SEC-001 | RC-05 | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-011 | system | SRS-011 | — | TP-SYS-04 v1.0 | 2026-03-12 | K. Novak |
| TC-012 | system | SRS-014 | — | TP-SYS-05 v1.0 | 2026-03-12 | K. Novak |
| TC-013 | system | SRS-015 | — | TP-SYS-05 v1.0 | 2026-03-12 | K. Novak |
| TC-014 | system | SRS-016 | — | TP-SYS-05 v1.0 | 2026-03-12 | K. Novak |
| TC-015 | system | SRS-018 | — | TP-SYS-05 v1.0 | 2026-03-12 | K. Novak |
| TC-016 | system | SRS-019 | RC-06 | TP-SYS-02 v2.0 | 2026-03-12 | K. Novak |
| TC-017 | system | SRS-020, SEC-002 | — | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-018 | system | SRS-021, SEC-003 | — | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-019 | system | SRS-022, SEC-005 | — | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-020 | system | SRS-023 | — | TP-SYS-06 v1.0 | 2026-03-12 | K. Novak |
| TC-021 | system | SRS-024 | RC-07 | TP-SYS-06 v1.0 | 2026-03-12 | K. Novak |
| TC-022 | system | SRS-006, SRS-013 | — | TP-SYS-06 v1.0 | 2026-03-12 | K. Novak |
| TC-023 | system | SRS-009, SEC-004 | — | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-024 | system | SRS-009, SEC-006 | — | TP-SEC-02 v1.0 | 2026-03-14 | K. Novak |
| TC-025 | system | SRS-008 | — | TP-SYS-03 v1.1 | 2026-03-12 | K. Novak |
| TC-027 | system | SRS-003, SRS-004 | — | TP-SYS-01 v2.0 | 2026-03-12 | K. Novak |
| TC-028 | system | SRS-001, SRS-008 | — | TP-SYS-03 v1.1 | 2026-03-12 | K. Novak |
| TC-029 | system | SRS-007, SRS-018 | — | TP-SYS-05 v1.0 | 2026-03-12 | K. Novak |
| TC-030 | system | SRS-011, SRS-022 | — | TP-SYS-04 v1.0 | 2026-03-12 | K. Novak |
| TC-031 | system | SRS-012, SRS-013 | — | TP-SYS-07 v1.0 | 2026-02-20 | K. Novak |
| TC-032 | system | SRS-002, SRS-012 | — | TP-SYS-07 v1.0 | 2026-02-20 | K. Novak |
| TC-033 | system | SRS-019, SRS-023 | — | TP-SYS-06 v1.0 | 2026-03-12 | K. Novak |
| TC-034 | system | SRS-024 | — | TP-SYS-06 v1.0 | 2026-03-12 | K. Novak |
| TC-035 | system | SRS-016, SRS-014 | — | TP-SYS-05 v1.0 | 2026-03-12 | K. Novak |
| TC-036 | system | SRS-010 | — | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-037 | system | SRS-004, SRS-012 | — | TP-SYS-07 v1.0 | 2026-02-20 | K. Novak |
| TC-038 | system | SRS-020 | — | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-039 | system | SRS-021 | — | TP-SEC-01 v1.0 | 2026-03-12 | K. Novak |
| TC-040 | system | SRS-015, SRS-006 | — | TP-SYS-05 v1.0 | 2026-03-12 | K. Novak |
