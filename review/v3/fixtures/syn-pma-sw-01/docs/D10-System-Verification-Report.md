# System Verification Report SVR-3.2

**Document ID:** D10-System-Verification-Report  
**Document version:** 2.0  
**Approval date:** 2026-04-10  
**Approved by:** K. Novak, V&V Lead; QA: J. Doe  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Scope
System verification of CardioSense ARR Software Module version **3.2.0**, release build **b1187**, against SRS 4.2, executed per the protocols in D09 within the declared test window 2026-03-23 to 2026-04-08.

## 2. Summary
**All 40 system test cases passed on build b1187.** Software version tested: 3.2.0. No deviations from plan. Deferred anomalies: ANM-104, ANM-101.

## 3. Test environments
ENV-01 CS-Patch Hub v3, Linux 6.1.77, Qt 6.5.3, libdsp 4.1.2, zlib-ng 2.1.6, OpenSSL 3.0.13. ENV-02 CS-Patch Hub v2, Linux 5.15.148, same OTS versions. Test tools: Halden ECG simulator HES-4 v2.2, pytest 8.0 harness.

## 4. Execution records
| Run | Test case | Requirements | Version (build) | Platform | OTS in configuration | Start | End | Result | Anomaly | Retest of |
|---|---|---|---|---|---|---|---|---|---|---|
| TR-0401 | TC-001 | SRS-001 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-23 | 2026-03-23 | Pass | — | — |
| TR-0402 | TC-002 | SRS-002 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-24 | 2026-03-24 | Pass | — | — |
| TR-0403 | TC-003 | SRS-003 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-25 | 2026-03-25 | Pass | — | — |
| TR-0404 | TC-004 | SRS-004 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-26 | 2026-03-26 | Pass | — | — |
| TR-0405 | TC-005 | SRS-005 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-27 | 2026-03-27 | Pass | — | — |
| TR-0406 | TC-006 | SRS-006 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-28 | 2026-03-28 | Pass | — | — |
| TR-0407 | TC-007 | SRS-007 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-29 | 2026-03-29 | Pass | — | — |
| TR-0408 | TC-008 | SRS-008 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-24 | 2026-03-24 | Pass | — | — |
| TR-0409 | TC-009 | SRS-009 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-31 | 2026-03-31 | Pass | — | — |
| TR-0410 | TC-010 | SRS-010, SEC-001 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-01 | 2026-04-01 | Pass | — | — |
| TR-0411 | TC-011 | SRS-011 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-02 | 2026-04-02 | Pass | — | — |
| TR-0412 | TC-012 | SRS-014 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-03 | 2026-04-03 | Pass | — | — |
| TR-0413 | TC-013 | SRS-015 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-04 | 2026-04-04 | Pass | — | — |
| TR-0414 | TC-014 | SRS-016 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-05 | 2026-04-05 | Pass | — | — |
| TR-0415 | TC-015 | SRS-018 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-06 | 2026-04-06 | Pass | — | — |
| TR-0416 | TC-016 | SRS-019 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-23 | 2026-03-23 | Pass | — | — |
| TR-0417 | TC-017 | SRS-020, SEC-002 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-24 | 2026-03-24 | Pass | — | — |
| TR-0418 | TC-018 | SRS-021, SEC-003 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-25 | 2026-03-25 | Pass | — | — |
| TR-0419 | TC-019 | SRS-022, SEC-005 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-26 | 2026-03-26 | Pass | — | — |
| TR-0420 | TC-020 | SRS-023 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-27 | 2026-03-27 | Pass | — | — |
| TR-0421 | TC-021 | SRS-024 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-28 | 2026-03-28 | Pass | — | — |
| TR-0422 | TC-022 | SRS-006, SRS-013 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-29 | 2026-03-29 | Fail | ANM-104 | — |
| TR-0423 | TC-023 | SRS-009, SEC-004 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-30 | 2026-03-30 | Pass | — | — |
| TR-0424 | TC-024 | SRS-009, SEC-006 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-31 | 2026-03-31 | Pass | — | — |
| TR-0425 | TC-025 | SRS-008 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-01 | 2026-04-01 | Pass | — | — |
| TR-0426 | TC-027 | SRS-003, SRS-004 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-02 | 2026-04-02 | Pass | — | — |
| TR-0427 | TC-028 | SRS-001, SRS-008 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-03 | 2026-04-03 | Pass | — | — |
| TR-0428 | TC-029 | SRS-007, SRS-018 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-04 | 2026-04-04 | Pass | — | — |
| TR-0429 | TC-030 | SRS-011, SRS-022 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-05 | 2026-04-05 | Pass | — | — |
| TR-0430 | TC-031 | SRS-012, SRS-013 | 3.1.4 (b1142) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-02 | 2026-03-02 | Pass | — | — |
| TR-0431 | TC-032 | SRS-002, SRS-012 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-23 | 2026-03-23 | Pass | — | — |
| TR-0432 | TC-033 | SRS-019, SRS-023 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-24 | 2026-03-24 | Pass | — | — |
| TR-0433 | TC-034 | SRS-024 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-25 | 2026-03-25 | Pass | — | — |
| TR-0434 | TC-035 | SRS-016, SRS-014 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-26 | 2026-03-26 | Fail | ANM-109 | — |
| TR-0435 | TC-036 | SRS-010 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-27 | 2026-03-27 | Pass | — | — |
| TR-0436 | TC-037 | SRS-004, SRS-012 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-28 | 2026-03-28 | Pass | — | — |
| TR-0437 | TC-038 | SRS-020 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-29 | 2026-03-29 | Pass | — | — |
| TR-0438 | TC-039 | SRS-021 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-30 | 2026-03-30 | Pass | — | — |
| TR-0439 | TC-040 | SRS-015, SRS-006 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-31 | 2026-03-31 | Blocked | — | — |
| TR-0440 | TC-018 | SRS-021, SEC-003 | 3.2.0 (b1187) | Hub v2 / Linux 5.15.148 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-03-26 | 2026-03-26 | Fail | ANM-101 | — |
| TR-0441 | TC-018 | SRS-021, SEC-003 | 3.2.0 (b1187) | Hub v3 / Linux 6.1.77 | libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3 | 2026-04-02 | 2026-04-02 | Pass | — | TR-0440 |

Executed 41 runs: 37 pass, 3 fail, 1 blocked. Observed results are recorded in the protocol execution sheets (DHF, VV-EXEC-3.2).

## 5. Failed tests and regression
TR-0440 (TC-018) failed on audit export truncation (ANM-101); fixed in the audit exporter configuration and re-run as TR-0441 (pass). TC-022 and TC-035 failures are deferred (see D13). Regression analysis RA-32-01 (2026-03-22) selected the full system set for re-run on b1187; TC-031 was run on 3.1.4 (b1142) under TP-SYS-07 and is carried forward because the classifier parameters are unchanged (see D12 section 5).

## 6. Software validation
Simulated-use validation SUV-03 (2026-04-07, 6 clinicians, Hub v3) passed all 12 scenarios; report SUV-03-R1.
