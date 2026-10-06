# Software Description

**Document ID:** D02-Software-Description  
**Document version:** 3.0  
**Approval date:** 2026-04-20  
**Approved by:** M. Okafor, Systems Engineering Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Software operation
The ARR module receives ECG samples from the CS-Patch sensor over Bluetooth Low Energy, detects QRS complexes, classifies rhythm episodes (normal, atrial fibrillation, bradycardia, tachycardia, pause) and presents them on the CS-Patch Hub display and, after synchronisation, on the clinician portal. Intended users are cardiologists and cardiac nurses; patients wear the patch and see only lead-quality and alert indications.

## 2. Inputs and outputs
Inputs: ECG samples (256 Hz, 24-bit), lead impedance, patient age band (clinician entry), configurable thresholds (Table 4 of D04). Outputs: episode records (CS-ECG v1.2), alerts (pause, BLE link loss), audit log, synchronisation to portal.

## 3. Software specifics
- Final release version stated: **3.2.0**, build b1187.
- Hardware platforms: CS-Patch Hub v2 (i.MX8M, ARM64) and CS-Patch Hub v3 (i.MX93, ARM64).
- Software platforms / OS: Linux 5.15.y (Hub v2), Linux 6.1.77 Halden BSP (Hub v3). Qt 6.5.3 LTS UI framework.
- Hosting: on-device; portal synchronisation to Halden Cloud (AWS eu-central-1) over TLS. The portal is a separate device software function covered in module M4.
- OTS software is used: see D14 and D15.

## 4. Interfaces and other functions
IF-01 BLE sensor link; IF-02 portal synchronisation (HTTPS, mutual TLS from 3.2.0); IF-03 USB service port (updates, logs); IF-04 clinician login UI; IF-05 local encrypted store. A non-device function (battery statistics export) shares the hub and was assessed per the Multiple Function guidance (D07 Annex B).
