# Software Risk Management File and Report

**Document ID:** D07-Risk-File  
**Document version:** 3.1  
**Approval date:** 2026-04-12  
**Approved by:** S. Brandt, Risk Manager; Dr. L. Meyer, Clinical  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Risk management plan
Plan RMP-ARR-03 approved 2025-09-01 (S. Brandt). Acceptability criteria: severity × probability matrix (Annex A); for software failures the probability of occurrence of harm is set to 1 before controls (IEC/TR 80002-1 approach). Cybersecurity risks are assessed on exploitability in D17 and transferred here where they have a safety impact (D17 section 6).

## 2. Hazards and hazardous situations
| Hazard | Hazardous situation | Description | Harm | Severity | Contributing requirements | Security origin |
|---|---|---|---|---|---|---|
| H-01 | HS-01 | Missed atrial fibrillation episode | Delayed anticoagulation decision; stroke | serious | SRS-002, SRS-004 | no |
| H-02 | HS-02 | False atrial fibrillation episode | Unnecessary anticoagulation; bleeding | serious | SRS-004, SRS-012 | no |
| H-03 | HS-03 | Missed pause | Syncope, fall | serious | SRS-005 | no |
| H-04 | HS-04 | Classification during lead-off treated as valid | Wrong rhythm reported | moderate | SRS-008 | no |
| H-05 | HS-05 | Unauthorised software/firmware installed | Any of the above | serious | SRS-010 | yes |
| H-06 | HS-06 | User sets threshold outside validated range | Missed or false episode | serious | SRS-019 | no |
| H-07 | HS-07 | Processing overload drops samples silently | Missed episode | serious | SRS-024 | no |
| H-08 | HS-08 | Episode store corrupted during portal sync | Loss of 30-day record | moderate | SRS-007, SRS-009 | no |

Initial evaluation (2025-09-15): HS-01, HS-02, HS-03, HS-05, HS-06, HS-07 unacceptable before controls; HS-04, HS-08 ALARP review required.

## 3. Risk control measures and verification
| Control | Hazard | Measure | Implementing requirements | Design units | Implementation verification tests | Effectiveness verification |
|---|---|---|---|---|---|---|
| RC-01 | H-01 | Validated QRS detector with reference-set acceptance | SRS-002 | U-02 | TC-002, TC-032 | Performance study CS-PS-02 report (bench, 2026-04-06) |
| RC-02 | H-01 | 30 s sustained-irregularity rule | SRS-004 | U-03 | TC-004, TC-027 | Performance study CS-PS-02 report |
| RC-03 | H-03 | Pause alert at 3.0 s | SRS-005 | U-03 | TC-005 | Simulated-use validation SUV-03 (2026-04-07) |
| RC-04 | H-04 | Lead-off and quality gating | SRS-008 | U-01 | TC-008, TC-025 | Performance study CS-PS-02 report, section 6 |
| RC-05 | H-05 | Signed package verification | SRS-010, SEC-001 | U-07 | TC-010, TC-036 | Security test ST-01 (threat mitigation) |
| RC-06 | H-06 | Bounded threshold entry (Table 4) | SRS-019 | U-05 | TC-016 | Summative usability evaluation HFV-02 task T4 |
| RC-07 | H-07 | Load shedding to single channel with notice | SRS-024 | U-04 | TC-021, TC-034 | — |

## 4. Residual risk
After controls, all hazardous situations are acceptable per the matrix except HS-07, which is ALARP with ANM-104 open (latency 2.4 s under maximum load); benefit-risk rationale in Annex C. HS-08 (store corruption during sync) was evaluated as acceptable without a dedicated control on the basis of SQLite journaling; see Annex D.

## 5. Overall residual risk and disclosure
Overall residual risk acceptable. Disclosed in labeling: pause alert limits, lead-off suppression behaviour, latency under load (ANM-104 workaround: reduce concurrent portal sync).

## 6. Risk management report
Report RMR-ARR-3.2 Rev 3.1 dated **2026-04-12**, software version covered **3.2.0**, reviewed by S. Brandt (Risk), Dr. L. Meyer (Clinical) and M. Okafor (Systems). Post-production information: complaint and vigilance review per SOP-PMS-002, quarterly.
