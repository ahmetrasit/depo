# Unit and Integration Test Summary

**Document ID:** D11-Unit-Integration-Summary  
**Document version:** 1.0  
**Approval date:** 2026-04-09  
**Approved by:** K. Novak, V&V Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Unit tests (Enhanced level)
| Run | Unit | Requirements covered | Version (build) | Start | End | Result | Tools / criteria |
|---|---|---|---|---|---|---|---|
| UT-01 | U-01 | SRS-001, SRS-008 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |
| UT-02 | U-02 | SRS-002 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |
| UT-03 | U-03 | SRS-003, SRS-004, SRS-005, SRS-012, SRS-013 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |
| UT-04 | U-04 | SRS-024, SRS-016 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |
| UT-05 | U-05 | SRS-019, SRS-011 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |
| UT-06 | U-06 | SRS-006, SRS-015, SRS-023 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |
| UT-07 | U-07 | SRS-010, SEC-001 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |
| UT-09 | U-09 | SRS-009, SEC-004, SEC-006, SRS-018, SRS-007 | 3.2.0 (b1187) | 2026-03-23 | 2026-03-24 | Pass | GoogleTest 1.14; coverage 94% lines |

## 2. Integration tests
| Run | Interface | Requirements covered | Version (build) | Date | Result |
|---|---|---|---|---|---|
| IT-01 | IF-01 | SRS-001, SRS-008 | 3.2.0 (b1187) | 2026-03-25 | Pass |
| IT-02 | IF-02 | SRS-009, SEC-004, SEC-006 | 3.2.0 (b1187) | 2026-03-26 | Pass |
| IT-03 | IF-03 | SRS-010, SEC-001 | 3.2.0 (b1187) | 2026-03-26 | Pass |
| IT-04 | IF-04 | SRS-020, SEC-002 | 3.2.0 (b1187) | 2026-03-27 | Pass |
| IT-05 | IF-05 | SRS-007, SRS-021, SEC-003 | 3.2.0 (b1187) | 2026-03-27 | Pass |

Unit acceptance criteria: 100% statement coverage of Class C safety functions, 90% overall (achieved 94%). Integration tests executed on ENV-01 and ENV-02.
