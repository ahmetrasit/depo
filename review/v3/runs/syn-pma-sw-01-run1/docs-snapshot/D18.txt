# Security Architecture: Controls and Views

**Document ID:** D18-Security-Architecture  
**Document version:** 2.0  
**Approval date:** 2026-02-20  
**Approved by:** E. Varga, Product Security Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Security controls by category
| Control | Category | Security requirements | Implementation | Verification tests |
|---|---|---|---|---|
| SC-01 | Code, Data, and Execution Integrity | SEC-001 | Bootloader and updater verify ECDSA P-256 signature | ST-02 |
| SC-02 | Authentication | SEC-002 | Password policy and lockout in auth service | ST-03 |
| SC-03 | Confidentiality | SEC-003 | AES-256-GCM store encryption, key in SE050 | ST-04 |
| SC-04 | Cryptography | SEC-004 | TLS 1.2+ with pinned portal certificate | ST-05 |
| SC-05 | Event Detection and Logging | SEC-005 | Hash-chained audit log | ST-06 |
| SC-06 | Authentication | SEC-006 | Mutual TLS on sync listener (new in 3.2.0) | ST-05 |
| SC-07 | Code, Data, and Execution Integrity | SRS-001 | BLE frame counter and session nonce | ST-07 |
| SC-08 | Resiliency and Recovery | SRS-024 | Connection rate limiting; monitoring continues when sync unavailable | ST-07 |
| SC-09 | Event Detection and Logging | SEC-005 | Security event forwarding to portal | — |
| SC-10 | Authorization | SEC-002 | Role-based access: clinician, admin, service | ST-03 |

## 2. Views
Global system view, multi-patient harm view (portal fleet update), updatability/patchability view (signed images via IF-03 and IF-02) and security use-case views are in Annex A (diagrams SA-01 to SA-04).

## 3. Communication paths
| Path | Interface | Protocol / ports | Direction | Protection |
|---|---|---|---|---|
| P-01 | IF-01 | BLE 5.0 GATT, LE Secure Connections | sensor ↔ hub | encrypted, authenticated pairing |
| P-02 | IF-02 | HTTPS, TLS 1.2/1.3, port 443 outbound, mutual TLS | hub → portal | pinned certificate |
| P-03 | IF-03 | USB CDC, service protocol v2 | service tool → hub | signed packages only |
| P-04 | IF-02 | Sync listener, TCP 8443 inbound (LAN only), mutual TLS | portal → hub (new in 3.2.0) | rate limited |
