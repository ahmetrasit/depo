# Software Version and Configuration Identification

**Document ID:** D03-Version-Configuration  
**Document version:** 2.0  
**Approval date:** 2026-04-16  
**Approved by:** P. Haas, Configuration Manager  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Proposed release version
Proposed version: **3.2.0**. Versioning rule: MAJOR.MINOR.PATCH per Halden SOP-SW-004; a build identifier `bNNNN` is assigned by the CI pipeline. The version, build identifier and build date are shown on the About screen (SRS-015) and in the device UDI-DI production identifier.

## 2. Release build record
- Release build identifier: **b1187**
- Build date: 2026-03-21
- Build environment: Yocto Kirkstone, GCC 11.4, CI runner image halden-ci:2026.03; reproducible-build hash 9f3c…e21a (full hash in DHF record CM-BLD-1187)
- Archive: DHF vault, record CM-BLD-1187

## 3. Configuration item list (release baseline b1187)
| Item | Name | Type | Version | In release baseline | Changed since 3.1.4 |
|---|---|---|---|---|---|
| CI-01 | ARR application | software item | 3.2.0 | yes | yes |
| CI-02 | Classification model parameters | model/reference data | 3.2.0-p4 | yes | no |
| CI-03 | libdsp | SOUP | 4.1.2 | yes | yes |
| CI-04 | zlib-ng | SOUP | 2.1.6 | yes | yes |
| CI-05 | OpenSSL | SOUP | 3.0.13 | yes | no |
| CI-06 | SQLite | SOUP | 3.45.1 | yes | no |
| CI-07 | Qt | SOUP | 6.5.3 | yes | no |
| CI-08 | Linux kernel Hub v3 BSP | OS | 6.1.77 | yes | no |
| CI-09 | Linux kernel Hub v2 BSP | OS | 5.15.148 | yes | no |
| CI-10 | Bootloader (mbedtls) | software item | 1.9.0 / mbedtls 3.5.2 | yes | no |

## 4. Software safety classification
The software system is classified **IEC 62304 Class C**: a failure of the classification function can contribute to a hazardous situation (HS-01, HS-03) that may result in death or serious injury, and no external risk control measure reduces the probability to acceptable. Software items U-01 to U-05 are Class C; U-06 (UI theming) and U-08 (battery statistics) are segregated as Class A per the architecture (D05 section 3) with the segregation rationale in D06 section 2.

## 5. Baseline dates
- Code freeze: **2026-03-20** (last change request implemented: CH-32)
- Verification complete attestation: 2026-04-08
- Release approval date: **2026-04-15**
