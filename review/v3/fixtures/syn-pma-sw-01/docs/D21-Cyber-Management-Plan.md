# Cybersecurity Management Plan (Postmarket)

**Document ID:** D21-Cyber-Management-Plan  
**Document version:** 1.3  
**Approval date:** 2026-04-01  
**Approved by:** E. Varga, Product Security Lead  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Responsibilities
Product Security Lead (E. Varga) owns monitoring and response; PSIRT mailbox security@halden.example.

## 2. Monitoring
Weekly NVD/KEV/vendor advisory monitoring for all SBOM components; SBOM re-scan at every build and monthly in the field.

## 3. Coordinated vulnerability disclosure
Policy published at halden.example/security; ISO/IEC 29147 and 30111 aligned; acknowledgement within 5 business days.

## 4. Patch timelines
Regular cycle: quarterly maintenance releases. Out-of-cycle: uncontrolled risk patched within 30 days of confirmation, controlled risk within 60 days. Updates delivered as signed images via portal (IF-02) and service port (IF-03).

## 5. Device support
Software support end date: **2032-12-31**, stated in labeling (D23 section 4).
