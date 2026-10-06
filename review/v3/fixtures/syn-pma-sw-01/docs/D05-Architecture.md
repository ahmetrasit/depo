# System and Software Architecture

**Document ID:** D05-Architecture  
**Document version:** 2.3  
**Approval date:** 2026-02-18  
**Approved by:** M. Okafor, Systems Engineering Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Modules and layers
Acquisition (U-01) → Detection (U-02) → Classification (U-03) → Load manager (U-04) → Settings and thresholds (U-05) → UI (U-06) → Update and integrity (U-07) → Battery statistics (U-08, non-device function). Sync service (U-09) handles IF-02.

## 2. Interfaces
| Interface | Protocol | External party | Crosses trust boundary |
|---|---|---|---|
| IF-01 | BLE 5.0 GATT, proprietary sensor profile | CS-Patch sensor | yes |
| IF-02 | HTTPS/TLS 1.2+, mutual TLS, port 443 outbound | Clinician portal | yes |
| IF-03 | USB 2.0 CDC service port | Service tool | yes |
| IF-04 | Touch UI (Qt) | Clinician / patient | no |
| IF-05 | Local file system (encrypted) | Episode store | no |

## 3. SOUP items and segregation
SOUP items are listed in D14. Class A items U-06 and U-08 run in a separate process with a message-queue boundary; a fault in them cannot block the Class C pipeline (watchdog W-1).

## 4. Data flow
Samples → ring buffer → detector → classifier → episode store (AES-256-GCM) → sync queue → portal. Thresholds flow from U-05 to U-03 with range checks (SRS-019).
