# Software Requirements Specification

**Document ID:** D04-SRS  
**Document version:** 4.2  
**Approval date:** 2026-02-12  
**Approved by:** M. Okafor, Systems Engineering Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Requirement identification and traceability
Requirements are identified SRS-nnn (functional, performance, interface, platform, security) and SEC-nnn (security requirements derived from the threat model, D16). Each requirement states its verification method; the trace to test cases is held in the V&V protocol index (D09) and the trace matrix export TM-3.2 (DHF). Requirements changed for 3.2.0 carry a change date of 2026-02-10 or later.

## 2. Software requirements
| ID | Requirement | Category | Safety-related | Critical | Verification | Last change |
|---|---|---|---|---|---|---|
| SRS-001 | The module shall acquire single-lead ECG samples at 256 Hz from the patch sensor via the BLE link. | functional | yes | yes | test | 2025-11-20 |
| SRS-002 | The module shall detect QRS complexes with sensitivity >= 99.0% on the MIT-BIH reference set. | performance | yes | yes | test | 2025-11-20 |
| SRS-003 | The module shall classify rhythm episodes into normal, atrial fibrillation, bradycardia, tachycardia and pause. | functional | yes | yes | test | 2025-11-20 |
| SRS-004 | An atrial fibrillation episode shall be reported only after >= 30 s of sustained irregular RR intervals. | functional | yes | yes | test | 2025-11-20 |
| SRS-005 | The module shall raise a pause alert when no QRS is detected for > 3.0 s. | functional | yes | yes | test | 2025-11-20 |
| SRS-006 | The module shall display the current rhythm classification within 2 s of episode end. | performance | yes | no | test | 2025-11-20 |
| SRS-007 | The module shall store episodes locally for 30 days with timestamp and lead quality index. | functional | no | no | test | 2025-11-20 |
| SRS-008 | The module shall flag lead-off and low signal quality and suppress classification during those intervals. | functional | yes | yes | test | 2025-11-20 |
| SRS-009 | The module shall synchronise stored episodes to the clinician portal over TLS 1.2 or higher. | interface | no | no | test | 2025-11-20 |
| SRS-010 | The module shall reject firmware or software packages whose signature does not verify. | security | yes | yes | test | 2025-11-20 |
| SRS-011 | The module shall log all classification threshold changes with user identity and time. | functional | no | no | test | 2025-11-20 |
| SRS-012 | The module shall limit false positive atrial fibrillation episode rate to <= 1 per 24 h on the reference set. | performance | yes | yes | test | 2026-02-10 |
| SRS-013 | The module shall recompute classification when the user corrects the patient age band. | functional | yes | no | test | 2026-02-10 |
| SRS-014 | The module shall run on the CS-Patch Hub v2 (Linux 5.15, ARM64) and the CS-Patch Hub v3 (Linux 6.1, ARM64). | platform | no | yes | test | 2025-11-20 |
| SRS-015 | The module shall display its software version, build identifier and date on the About screen. | functional | no | no | test | 2025-11-20 |
| SRS-016 | The module shall complete a cold start to monitoring state within 20 s. | performance | no | no | test | 2025-11-20 |
| SRS-017 | On loss of the BLE link for > 60 s the module shall alert the user and mark the gap in the episode record. | functional | yes | yes | test | 2025-11-20 |
| SRS-018 | The module shall export episodes in the CS-ECG v1.2 interchange format. | interface | no | no | test | 2025-11-20 |
| SRS-019 | User-configurable thresholds shall be bounded to clinically validated ranges defined in Table 4. | functional | yes | yes | test | 2025-11-20 |
| SRS-020 | The module shall authenticate clinician users with a username and password of >= 12 characters, or SSO. | security | no | yes | test | 2025-11-20 |
| SRS-021 | The module shall encrypt the local episode store with AES-256 using a device-unique key. | security | no | yes | test | 2025-11-20 |
| SRS-022 | The module shall report audit log integrity failures to the clinician portal. | security | no | no | test | 2025-11-20 |
| SRS-023 | The module shall provide a manual rhythm review workflow permitting the clinician to overrule a classification. | functional | yes | no | test | 2025-11-20 |
| SRS-024 | The module shall degrade to single-channel monitoring with an on-screen notice when the processing load exceeds 80%. | functional | yes | yes | test | 2025-11-20 |

## 3. Security requirements
| ID | Requirement | Derived from | Review date |
|---|---|---|---|
| SEC-001 | Signed update packages only; signature algorithm ECDSA P-256; rejection logged. | SRS-010 | 2026-02-11 |
| SEC-002 | Clinician authentication with lockout after 5 failures for 15 min. | SRS-020 | 2026-02-11 |
| SEC-003 | Local episode store encrypted at rest (AES-256-GCM, device-unique key in secure element). | SRS-021 | 2026-02-11 |
| SEC-004 | TLS 1.2+ with certificate pinning for portal synchronisation. | SRS-009 | 2026-02-11 |
| SEC-005 | Audit log protected by hash chain; tamper detection reported. | SRS-022 | 2026-02-11 |
| SEC-006 | Cloud synchronisation listener accepts connections only from the paired portal (mutual TLS). | SRS-009 | 2026-02-11 |

## 4. Approval
SRS 4.2 approved 2026-02-12 by M. Okafor (Systems) and S. Brandt (Risk). Changes since 4.1: SRS-012, SRS-013 (CH-29), SRS-009/SEC-006 (CH-31), SRS-024 (CH-30), SRS-015 (CH-32).
