# Software Development, Configuration Management and Maintenance Plan Summary

**Document ID:** D08-Lifecycle-Plans  
**Document version:** 1.4  
**Approval date:** 2026-01-15  
**Approved by:** P. Haas, Configuration Manager  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Development plan
Software development plan SDP-ARR-02 (approved 2025-04-10) follows IEC 62304 Ed 1.1 with a staged V-model; agile sprints are used within implementation (AAMI TIR45:2023 referenced for sprint-level documentation). The DoC route to IEC 62304 (D22, DoC-1) covers clauses 5.1, 6 and 8 in addition to 5.2–5.8, 7 and 9.

## 2. Configuration management
CM plan CMP-ARR-02 (approved 2025-04-10): Git with signed tags, CI build identifiers bNNNN, baselines per release, change requests CR-nnnn with impact analysis; configuration items listed in D03.

## 3. Maintenance and problem resolution
Maintenance plan MP-ARR-01 (approved 2025-04-10): problem reports PR-nnnn triaged weekly; anomalies classified per ANSI/AAMI SW91; security vulnerabilities routed to the product security process (D21).

## 4. Tools and coding standards
C++17 with MISRA C++:2023 subset; static analysis (Coverity 2024.3) at every merge; unit test framework GoogleTest 1.14.
