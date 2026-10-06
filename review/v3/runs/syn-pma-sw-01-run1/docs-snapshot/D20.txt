# Vulnerability Assessment

**Document ID:** D20-Vulnerability-Assessment  
**Document version:** 1.0  
**Approval date:** 2026-03-19  
**Approved by:** E. Varga, Product Security Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Known vulnerabilities
Source: SBOM scan with Grype 0.74 against NVD and the CISA KEV catalogue on 2026-03-19 (KEV check date 2026-03-19). Scan target: SBOM for build b1150.

| Vulnerability | Component | Discovery | In CISA KEV | Assessment | Disposition |
|---|---|---|---|---|---|
| CVE-2024-0727 | OpenSSL 3.0.13 | SBOM scan (Grype 0.74, 2026-03-19) | no | not applicable: PKCS12 parsing not used; compensating control none required | not_affected |
| CVE-2023-46218 | libcurl 8.5.0 | SBOM scan (Grype 0.74, 2026-03-19) | no | cookie handling not used; portal client uses pinned TLS only | not_affected |
| CVE-2024-2511 | OpenSSL 1.1.1w | SBOM scan (Grype 0.74, 2026-03-19) | no | unbounded session cache growth; mitigated by rate limiting SC-08 | mitigated |

## 2. KEV
No KEV-listed vulnerabilities are present in the release.

## 3. Component support horizon
OpenSSL 3.0 LTS end of support 2026-09-07: migration to 3.3 LTS planned for release 3.3.0 (Q4 2026). Qt 6.5 LTS end 2026-05-26: commercial extended support contract in place to 2028.
