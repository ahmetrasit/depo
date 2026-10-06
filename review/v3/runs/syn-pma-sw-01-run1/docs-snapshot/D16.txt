# Threat Model

**Document ID:** D16-Threat-Model  
**Document version:** 2.1  
**Approval date:** 2026-01-30  
**Approved by:** E. Varga, Product Security Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Identity
Threat model TM-ARR Rev 2.1 dated **2026-01-30**; methodology STRIDE per element with attack trees for T-01 and T-04 (MITRE playbook); configuration covered: **3.2.0** (release candidate scope as designed in D05 Rev 2.2).

## 2. System decomposition
Assets: ECG samples, episode store, clinician credentials, audit log, update packages. Trust boundaries: BLE link (IF-01), portal link (IF-02), USB service port (IF-03). Processes: U-01 to U-09. Data stores: episode store, audit log, settings.

## 3. Assumptions
Hub is installed in a clinic or patient home; physical access by patient assumed; portal is a trusted but separately secured system; BLE pairing is performed by clinic staff.

## 4. Threats
| Threat | Attack vector | Targeted elements | Mitigating controls | Threat-mitigation tests |
|---|---|---|---|---|
| T-01 | Malicious update package installed via USB service port | IF-03 | SC-01 | ST-02 |
| T-02 | Credential stuffing against clinician login | IF-04 | SC-02 | ST-03 |
| T-03 | Theft of hub; extraction of episode store | IF-05 | SC-03 | ST-04 |
| T-04 | Man-in-the-middle on portal synchronisation | IF-02 | SC-04, SC-06 | ST-05 |
| T-05 | Tampering with audit log to hide threshold changes | IF-05 | SC-05 | ST-06 |
| T-06 | Replay of BLE sensor frames to inject false ECG | IF-01 | SC-07 | ST-07 |
| T-07 | Denial of service on cloud sync listener | IF-02 | SC-08 | ST-07 |
| T-08 | Unauthorised remote service session | IF-02 | SC-10 | ST-05 |

## 5. Lifecycle and supply chain
Build pipeline signing keys in HSM; SOUP intake review per D14; vulnerability monitoring per D21.
