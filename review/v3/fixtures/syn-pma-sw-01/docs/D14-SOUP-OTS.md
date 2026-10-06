# SOUP and Off-the-Shelf Software List and Anomaly Review

**Document ID:** D14-SOUP-OTS  
**Document version:** 2.2  
**Approval date:** 2026-03-12  
**Approved by:** A. Reyes, Software Architect  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. SOUP / OTS identification
| SOUP id | Title | Manufacturer / supplier | Version | Release / adoption date | Function in device |
|---|---|---|---|---|---|
| SOUP-01 | libdsp | Signalworks AG | 4.1.2 | 2025-12-01 | QRS filtering and resampling |
| SOUP-02 | zlib-ng | zlib-ng project | 2.1.6 | 2026-01-10 | Episode record compression |
| SOUP-03 | OpenSSL | OpenSSL Software Foundation | 3.0.13 | 2024-01-30 | TLS, signature verification |
| SOUP-04 | SQLite | SQLite Consortium | 3.45.1 | 2024-01-30 | Episode store |
| SOUP-05 | Qt | The Qt Company | 6.5.3 LTS | 2023-10-10 | User interface |
| SOUP-06 | Linux kernel (Hub BSP) | Halden BSP team / kernel.org | 6.1.77 | 2024-02-01 | Operating system |

Required hardware/software: see D02 section 3. Each SOUP item has functional and performance requirements in the SOUP requirements sheet SR-ARR-02 (DHF).

## 2. Published anomaly list review (IEC 62304 7.1.3)
| SOUP id | Anomaly list source | List version scope | Review date | Hazard-relevant anomalies | Security vulnerabilities cross-checked |
|---|---|---|---|---|---|
| SOUP-01 | https://signalworks.example/libdsp/errata | 4.1.2 | 2026-02-02 | none hazard-relevant | yes |
| SOUP-02 | https://github.com/zlib-ng/zlib-ng/issues | 2.1.3 | 2025-10-02 | none hazard-relevant | yes |
| SOUP-03 | https://openssl.org/news/vulnerabilities.html | 3.0.13 | 2026-03-10 | CVE-2024-0727 (not applicable: PKCS12 not used) | yes |
| SOUP-04 | https://sqlite.org/cves.html | 3.45.1 | 2026-03-10 | none hazard-relevant | yes |
| SOUP-05 | https://bugreports.qt.io | 6.5.3 | 2026-03-11 | QTBUG-118 rendering glitch; H-04 not affected (display only) | yes |
| SOUP-06 | https://kernel.org / Debian security tracker | 6.1.77 | 2026-03-12 | none hazard-relevant | yes |

## 3. Risk assessment of SOUP
SOUP-01 (libdsp) contributes to HS-01 and HS-03 (detector filtering); SOUP-02 to HS-08; others have no hazard contribution. Residual risk: see D07.

## 4. OTS verification
All SOUP items are exercised in the system tests of D10 at the versions listed in section 1 and in D15. Qt rendering glitch QTBUG-118 was evaluated against H-04 and found not applicable.

## 5. Control of versions in the field
Software is delivered as a signed monolithic image; users cannot install or update OTS components (SEC-001).
