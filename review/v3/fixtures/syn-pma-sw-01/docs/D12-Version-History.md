# Software Version History

**Document ID:** D12-Version-History  
**Document version:** 1.6  
**Approval date:** 2026-04-16  
**Approved by:** P. Haas, Configuration Manager  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Tested versions since design-control start
| Version | Build | Date | Testing / notes | Used in bench or clinical study |
|---|---|---|---|---|
| 3.0.0 | b0912 | 2025-03-14 | Initial design-controlled release candidate; bench study CS-PS-01 | CS-PS-01 |
| 3.1.0 | b1098 | 2025-10-20 | Portal sync, clinician login; penetration test PT-01 | — |
| 3.1.4 | b1142 | 2026-02-27 | Age-band recompute (SRS-013), false-positive tuning (SRS-012); full system regression | CS-PS-02 |
| 3.2.0 | b1187 | 2026-03-21 | Mutual-TLS sync listener (CH-31), load shedding notice text, About screen build id; release candidate | — |

## 2. Changes between tested versions
| Change | From | To | Affected items | Safety/security relevant |
|---|---|---|---|---|
| CH-29 | 3.1.0 | 3.1.4 | SRS-012, SRS-013, U-03 | no |
| CH-30 | 3.1.4 | 3.2.0 | SRS-024, U-04, notice text | no |
| CH-31 | 3.1.4 | 3.2.0 | SRS-009, SEC-006, SC-06, IF-02, sync listener | yes |
| CH-32 | 3.1.4 | 3.2.0 | SRS-015, About screen | no |

## 3. Previously authorized versions
None; this is the initial PMA.

## 4. Final entry: tested versus released
Last fully tested version: **3.2.0** (b1187); version to be released: **3.2.0** (b1187). No differences.

## 5. Study version bridge
Bench study CS-PS-02 used 3.1.4 (b1142). Differences to 3.2.0: CH-30 (load manager notice), CH-31 (sync listener), CH-32 (About screen). None affects the detector or classifier parameters (CI-02 unchanged); assessment in D07 Annex E. Test TC-031 (TP-SYS-07) executed on 3.1.4 is therefore carried forward without re-execution.
