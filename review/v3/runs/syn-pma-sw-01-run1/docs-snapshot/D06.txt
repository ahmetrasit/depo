# Software Design Specification

**Document ID:** D06-SDS  
**Document version:** 2.1  
**Approval date:** 2026-02-25  
**Approved by:** A. Reyes, Software Architect  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Detailed design per unit
| Unit | Responsibility | Implements requirements |
|---|---|---|
| U-01 | Acquisition and lead quality | SRS-001, SRS-008 |
| U-02 | QRS detector | SRS-002 |
| U-03 | Rhythm classifier | SRS-003, SRS-004, SRS-005, SRS-012, SRS-013 |
| U-04 | Load manager | SRS-024, SRS-016 |
| U-05 | Settings | SRS-019, SRS-011 |
| U-06 | UI | SRS-006, SRS-015, SRS-023 |
| U-07 | Update and integrity | SRS-010, SEC-001 |
| U-08 | Battery statistics (non-device) | — |
| U-09 | Sync service | SRS-009, SEC-004, SEC-006, SRS-018, SRS-007 |

## 2. Segregation
U-06 and U-08 are Class A per D03 section 4; IPC boundary via ZeroMQ with bounded queues; watchdog W-1 restarts UI without affecting classification.

## 3. Design evidence dates
SDS 2.0 approved 2025-11-28 before unit testing started (2025-12-02); SDS 2.1 (this version) approved 2026-02-25 after CH-30/CH-31 design changes; unit tests for U-04 and U-09 were re-run (D11).
