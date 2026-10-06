# Software Bill of Materials

**Document ID:** D15-SBOM  
**Document version:** 3.2.0-sbom-1  
**Approval date:** 2026-03-18  
**Approved by:** DevSecOps pipeline (automated); reviewed P. Haas  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. SBOM identity
Format: CycloneDX 1.5 (JSON; this document is the human-readable rendering). Generated **2026-03-18** by the DevSecOps pipeline (syft 0.105) for build **b1150**, software version 3.2.0. Transitive dependencies included. Covers the ARR application, bootloader and Hub v3 BSP; the Hub v2 BSP SBOM is a separate file (SBOM-HUBV2-5.15).

## 2. Components
| Component | Supplier | Version | Identifier | Relationship | Level of support | End of support | Known vulnerabilities |
|---|---|---|---|---|---|---|---|
| CardioSense ARR Module | Halden Cardiac Systems GmbH (fictional) | 3.2.0 | pkg:generic/cardiosense-arr@3.2.0 | root | active | 2032-12-31 | — |
| libdsp | Signalworks AG | 4.1.0 | pkg:generic/libdsp@4.1.0 | depends-on | active | 2028-06-30 | — |
| zlib-ng | zlib-ng project | 2.1.6 | pkg:github/zlib-ng/zlib-ng@2.1.6 | depends-on | active | — | — |
| OpenSSL | OpenSSL Software Foundation | 3.0.13 | pkg:generic/openssl@3.0.13 | depends-on | active (LTS) | 2026-09-07 | CVE-2024-0727 |
| SQLite | SQLite Consortium | 3.45.1 | pkg:generic/sqlite@3.45.1 | depends-on | active | — | — |
| Qt | The Qt Company | 6.5.3 | pkg:generic/qt@6.5.3 | depends-on | active (LTS) | 2026-05-26 | — |
| Linux kernel | kernel.org / Halden BSP | 6.1.77 | pkg:generic/linux@6.1.77 | depends-on | active (LTS) | 2026-12-31 | — |
| BlueZ | bluez.org | 5.66 | pkg:generic/bluez@5.66 | depends-on | active | — | — |
| libcurl | curl project | 8.5.0 | pkg:generic/curl@8.5.0 | depends-on | active | — | CVE-2023-46218 |
| protobuf | Google | 25.2 | pkg:generic/protobuf@25.2 | depends-on | active | — | — |
| glibc | GNU | 2.36 | pkg:generic/glibc@2.36 | depends-on | active (Debian LTS) | 2026-06-30 | — |
| busybox | busybox.net | 1.36.1 | pkg:generic/busybox@1.36.1 | depends-on | active | — | — |
| mbedtls (bootloader) | Arm | 3.5.2 | pkg:generic/mbedtls@3.5.2 | depends-on | active | — | — |
| CS-Patch firmware interface lib | Halden Cardiac Systems GmbH (fictional) | 2.4.0 | pkg:generic/cspatch-if@2.4.0 | depends-on | active | 2032-12-31 | — |
