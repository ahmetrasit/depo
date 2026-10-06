"""Generate the synthetic PMA software module fixture SYN-PMA-SW-01 with planted defects.

Everything here is fictional. Device, company, standards citations and findings are stipulated test
material for exercising review/v3; they are not claims about any real product.

    python3 review/v3/fixtures/gen_syn01.py        -> fixtures/syn-pma-sw-01/docs/*.md + defects.json
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "syn-pma-sw-01"
DOCS = OUT / "docs"

# ------------------------------------------------------------------ anchors (truth)
PV, RB = "3.2.0", "b1187"
PREV_V, PREV_B = "3.1.4", "b1142"
CODE_FREEZE, BUILD_DATE, RELEASE, SUBMIT = "2026-03-20", "2026-03-21", "2026-04-15", "2026-05-04"
TEST_START, TEST_END = "2026-03-23", "2026-04-08"
COMPANY = "Halden Cardiac Systems GmbH (fictional)"
DEVICE = "CardioSense ARR Software Module"


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def doc(name, title, version, approved, approver, body, covers=PV):
    head = f"# {title}\n\n**Document ID:** {name}  \n**Document version:** {version}  \n**Approval date:** {approved}  \n**Approved by:** {approver}  \n**Software version covered:** {covers}  \n**Applicant:** {COMPANY}  \n**Device:** {DEVICE}\n\n"
    (DOCS / f"{name}.md").write_text(head + body.strip() + "\n")


# ------------------------------------------------------------------ requirements
REQS = []
def req(i, text, cat, safety, crit, method="test", changed="2025-11-20"):
    REQS.append({"id": f"SRS-{i:03d}", "text": text, "cat": cat, "safety": safety, "crit": crit, "method": method, "changed": changed})

req(1, "The module shall acquire single-lead ECG samples at 256 Hz from the patch sensor via the BLE link.", "functional", True, True)
req(2, "The module shall detect QRS complexes with sensitivity >= 99.0% on the MIT-BIH reference set.", "performance", True, True)
req(3, "The module shall classify rhythm episodes into normal, atrial fibrillation, bradycardia, tachycardia and pause.", "functional", True, True)
req(4, "An atrial fibrillation episode shall be reported only after >= 30 s of sustained irregular RR intervals.", "functional", True, True)
req(5, "The module shall raise a pause alert when no QRS is detected for > 3.0 s.", "functional", True, True)
req(6, "The module shall display the current rhythm classification within 2 s of episode end.", "performance", True, False)
req(7, "The module shall store episodes locally for 30 days with timestamp and lead quality index.", "functional", False, False)
req(8, "The module shall flag lead-off and low signal quality and suppress classification during those intervals.", "functional", True, True)
req(9, "The module shall synchronise stored episodes to the clinician portal over TLS 1.2 or higher.", "interface", False, False)
req(10, "The module shall reject firmware or software packages whose signature does not verify.", "security", True, True)
req(11, "The module shall log all classification threshold changes with user identity and time.", "functional", False, False)
req(12, "The module shall limit false positive atrial fibrillation episode rate to <= 1 per 24 h on the reference set.", "performance", True, True, changed="2026-02-10")
req(13, "The module shall recompute classification when the user corrects the patient age band.", "functional", True, False, changed="2026-02-10")
req(14, "The module shall run on the CS-Patch Hub v2 (Linux 5.15, ARM64) and the CS-Patch Hub v3 (Linux 6.1, ARM64).", "platform", False, True)
req(15, "The module shall display its software version, build identifier and date on the About screen.", "functional", False, False)
req(16, "The module shall complete a cold start to monitoring state within 20 s.", "performance", False, False)
req(17, "On loss of the BLE link for > 60 s the module shall alert the user and mark the gap in the episode record.", "functional", True, True)
req(18, "The module shall export episodes in the CS-ECG v1.2 interchange format.", "interface", False, False)
req(19, "User-configurable thresholds shall be bounded to clinically validated ranges defined in Table 4.", "functional", True, True)
req(20, "The module shall authenticate clinician users with a username and password of >= 12 characters, or SSO.", "security", False, True)
req(21, "The module shall encrypt the local episode store with AES-256 using a device-unique key.", "security", False, True)
req(22, "The module shall report audit log integrity failures to the clinician portal.", "security", False, False)
req(23, "The module shall provide a manual rhythm review workflow permitting the clinician to overrule a classification.", "functional", True, False)
req(24, "The module shall degrade to single-channel monitoring with an on-screen notice when the processing load exceeds 80%.", "functional", True, True)
SEC_REQS = [("SEC-001", "Signed update packages only; signature algorithm ECDSA P-256; rejection logged.", "SRS-010"),
            ("SEC-002", "Clinician authentication with lockout after 5 failures for 15 min.", "SRS-020"),
            ("SEC-003", "Local episode store encrypted at rest (AES-256-GCM, device-unique key in secure element).", "SRS-021"),
            ("SEC-004", "TLS 1.2+ with certificate pinning for portal synchronisation.", "SRS-009"),
            ("SEC-005", "Audit log protected by hash chain; tamper detection reported.", "SRS-022"),
            ("SEC-006", "Cloud synchronisation listener accepts connections only from the paired portal (mutual TLS).", "SRS-009")]

# ------------------------------------------------------------------ test cases
TCS = []
def tc(i, level, reqs, proto, approved, rc=""):
    TCS.append({"id": f"TC-{i:03d}", "level": level, "reqs": reqs, "proto": proto, "approved": approved, "rc": rc})

PA = "2026-03-12"
tc(1, "system", ["SRS-001"], "TP-SYS-01 v2.0", PA)
tc(2, "system", ["SRS-002"], "TP-SYS-01 v2.0", PA, "RC-01")
tc(3, "system", ["SRS-003"], "TP-SYS-01 v2.0", PA)
tc(4, "system", ["SRS-004"], "TP-SYS-02 v2.0", PA, "RC-02")
tc(5, "system", ["SRS-005"], "TP-SYS-02 v2.0", PA, "RC-03")
tc(6, "system", ["SRS-006"], "TP-SYS-02 v2.0", PA)
tc(7, "system", ["SRS-007"], "TP-SYS-03 v1.1", PA)
tc(8, "system", ["SRS-008"], "TP-SYS-03 v1.1", "2026-03-25", "RC-04")   # PD-13 protocol approved after run
tc(9, "system", ["SRS-009"], "TP-SYS-04 v1.0", PA)
tc(10, "system", ["SRS-010", "SEC-001"], "TP-SEC-01 v1.0", PA, "RC-05")
tc(11, "system", ["SRS-011"], "TP-SYS-04 v1.0", PA)
tc(12, "system", ["SRS-014"], "TP-SYS-05 v1.0", PA)
tc(13, "system", ["SRS-015"], "TP-SYS-05 v1.0", PA)
tc(14, "system", ["SRS-016"], "TP-SYS-05 v1.0", PA)
tc(15, "system", ["SRS-018"], "TP-SYS-05 v1.0", PA)
tc(16, "system", ["SRS-019"], "TP-SYS-02 v2.0", PA, "RC-06")
tc(17, "system", ["SRS-020", "SEC-002"], "TP-SEC-01 v1.0", PA)
tc(18, "system", ["SRS-021", "SEC-003"], "TP-SEC-01 v1.0", PA)
tc(19, "system", ["SRS-022", "SEC-005"], "TP-SEC-01 v1.0", PA)
tc(20, "system", ["SRS-023"], "TP-SYS-06 v1.0", PA)
tc(21, "system", ["SRS-024"], "TP-SYS-06 v1.0", PA, "RC-07")
tc(22, "system", ["SRS-006", "SRS-013"], "TP-SYS-06 v1.0", PA)
tc(23, "system", ["SRS-009", "SEC-004"], "TP-SEC-01 v1.0", PA)
tc(24, "system", ["SRS-009", "SEC-006"], "TP-SEC-02 v1.0", "2026-03-14")
tc(25, "system", ["SRS-008"], "TP-SYS-03 v1.1", PA)
tc(27, "system", ["SRS-003", "SRS-004"], "TP-SYS-01 v2.0", PA)
tc(28, "system", ["SRS-001", "SRS-008"], "TP-SYS-03 v1.1", PA)
tc(29, "system", ["SRS-007", "SRS-018"], "TP-SYS-05 v1.0", PA)
tc(30, "system", ["SRS-011", "SRS-022"], "TP-SYS-04 v1.0", PA)
tc(31, "system", ["SRS-012", "SRS-013"], "TP-SYS-07 v1.0", "2026-02-20")   # PD-02: only run on previous build
tc(32, "system", ["SRS-002", "SRS-012"], "TP-SYS-07 v1.0", "2026-02-20")
tc(33, "system", ["SRS-019", "SRS-023"], "TP-SYS-06 v1.0", PA)
tc(34, "system", ["SRS-024"], "TP-SYS-06 v1.0", PA)
tc(35, "system", ["SRS-016", "SRS-014"], "TP-SYS-05 v1.0", PA)
tc(36, "system", ["SRS-010"], "TP-SEC-01 v1.0", PA)
tc(37, "system", ["SRS-004", "SRS-012"], "TP-SYS-07 v1.0", "2026-02-20")
tc(38, "system", ["SRS-020"], "TP-SEC-01 v1.0", PA)
tc(39, "system", ["SRS-021"], "TP-SEC-01 v1.0", PA)
tc(40, "system", ["SRS-015", "SRS-006"], "TP-SYS-05 v1.0", PA)
TCS = [t for t in TCS if t]

# ------------------------------------------------------------------ runs
RUNS = []
def run(i, tcid, build, ver, start, end, result, anomalies="", retest_of=""):
    t = next(x for x in TCS if x["id"] == tcid)
    RUNS.append({"id": f"TR-{i:04d}", "tc": tcid, "reqs": t["reqs"], "build": build, "ver": ver, "start": start, "end": end,
                 "result": result, "anom": anomalies, "retest": retest_of})

day = {k: f"2026-03-{23+k:02d}" if 23 + k <= 31 else f"2026-04-{23+k-31:02d}" for k in range(0, 17)}
n = 400
for k, t in enumerate(TCS):
    n += 1
    if t["id"] == "TC-031":
        run(n, t["id"], PREV_B, PREV_V, "2026-03-02", "2026-03-02", "Pass")       # PD-02 superseded build, never rerun
        continue
    if t["id"] == "TC-008":
        run(n, t["id"], RB, PV, "2026-03-24", "2026-03-24", "Pass")              # PD-13 before protocol approval 2026-03-25
        continue
    d = day[k % 15]
    if t["id"] == "TC-022":
        run(n, t["id"], RB, PV, d, d, "Fail", "ANM-104")                          # on the unresolved list (ok)
        continue
    if t["id"] == "TC-035":
        run(n, t["id"], RB, PV, d, d, "Fail", "ANM-109")                          # PD-15 anomaly not on list
        continue
    if t["id"] == "TC-040":
        run(n, t["id"], RB, PV, d, d, "Blocked")
        continue
    run(n, t["id"], RB, PV, d, d, "Pass")
# a legitimate fail + retest pair (should not be flagged)
n += 1; run(n, "TC-018", RB, PV, "2026-03-26", "2026-03-26", "Fail", "ANM-101")
n += 1; run(n, "TC-018", RB, PV, "2026-04-02", "2026-04-02", "Pass", "", f"TR-{n-1:04d}")

# ------------------------------------------------------------------ hazards and controls
HAZ = [("H-01", "HS-01", "Missed atrial fibrillation episode", "Delayed anticoagulation decision; stroke", "serious", ["SRS-002", "SRS-004"], False),
       ("H-02", "HS-02", "False atrial fibrillation episode", "Unnecessary anticoagulation; bleeding", "serious", ["SRS-004", "SRS-012"], False),
       ("H-03", "HS-03", "Missed pause", "Syncope, fall", "serious", ["SRS-005"], False),
       ("H-04", "HS-04", "Classification during lead-off treated as valid", "Wrong rhythm reported", "moderate", ["SRS-008"], False),
       ("H-05", "HS-05", "Unauthorised software/firmware installed", "Any of the above", "serious", ["SRS-010"], True),
       ("H-06", "HS-06", "User sets threshold outside validated range", "Missed or false episode", "serious", ["SRS-019"], False),
       ("H-07", "HS-07", "Processing overload drops samples silently", "Missed episode", "serious", ["SRS-024"], False),
       ("H-08", "HS-08", "Episode store corrupted during portal sync", "Loss of 30-day record", "moderate", ["SRS-007", "SRS-009"], False)]  # PD-17 no control
RCS = [("RC-01", "H-01", "Validated QRS detector with reference-set acceptance", ["SRS-002"], ["U-02"], ["TC-002", "TC-032"], "Performance study CS-PS-02 report (bench, 2026-04-06)"),
       ("RC-02", "H-01", "30 s sustained-irregularity rule", ["SRS-004"], ["U-03"], ["TC-004", "TC-027"], "Performance study CS-PS-02 report"),
       ("RC-03", "H-03", "Pause alert at 3.0 s", ["SRS-005"], ["U-03"], ["TC-005"], "Simulated-use validation SUV-03 (2026-04-07)"),
       ("RC-04", "H-04", "Lead-off and quality gating", ["SRS-008"], ["U-01"], ["TC-008", "TC-025"], "Performance study CS-PS-02 report, section 6"),
       ("RC-05", "H-05", "Signed package verification", ["SRS-010", "SEC-001"], ["U-07"], ["TC-010", "TC-036"], "Security test ST-01 (threat mitigation)"),
       ("RC-06", "H-06", "Bounded threshold entry (Table 4)", ["SRS-019"], ["U-05"], ["TC-016"], "Summative usability evaluation HFV-02 task T4"),
       ("RC-07", "H-07", "Load shedding to single channel with notice", ["SRS-024"], ["U-04"], ["TC-021", "TC-034"], "")]   # PD-07 no effectiveness evidence

# ------------------------------------------------------------------ SOUP and SBOM
SOUP = [("SOUP-01", "libdsp", "Signalworks AG", "4.1.2", "2025-12-01", "QRS filtering and resampling"),      # PD-05 SBOM says 4.1.0
        ("SOUP-02", "zlib-ng", "zlib-ng project", "2.1.6", "2026-01-10", "Episode record compression"),         # PD-06 review on 2.1.3, dated before adoption
        ("SOUP-03", "OpenSSL", "OpenSSL Software Foundation", "3.0.13", "2024-01-30", "TLS, signature verification"),
        ("SOUP-04", "SQLite", "SQLite Consortium", "3.45.1", "2024-01-30", "Episode store"),
        ("SOUP-05", "Qt", "The Qt Company", "6.5.3 LTS", "2023-10-10", "User interface"),
        ("SOUP-06", "Linux kernel (Hub BSP)", "Halden BSP team / kernel.org", "6.1.77", "2024-02-01", "Operating system")]
SOUP_REVIEW = [("SOUP-01", "https://signalworks.example/libdsp/errata", "4.1.2", "2026-02-02", "", True),
               ("SOUP-02", "https://github.com/zlib-ng/zlib-ng/issues", "2.1.3", "2025-10-02", "", True),
               ("SOUP-03", "https://openssl.org/news/vulnerabilities.html", "3.0.13", "2026-03-10", "CVE-2024-0727 (not applicable: PKCS12 not used)", True),
               ("SOUP-04", "https://sqlite.org/cves.html", "3.45.1", "2026-03-10", "", True),
               ("SOUP-05", "https://bugreports.qt.io", "6.5.3", "2026-03-11", "QTBUG-118 rendering glitch; H-04 not affected (display only)", True),
               ("SOUP-06", "https://kernel.org / Debian security tracker", "6.1.77", "2026-03-12", "", True)]
SBOM = [("CardioSense ARR Module", COMPANY, PV, "pkg:generic/cardiosense-arr@3.2.0", "root", "active", "2032-12-31", ""),
        ("libdsp", "Signalworks AG", "4.1.0", "pkg:generic/libdsp@4.1.0", "depends-on", "active", "2028-06-30", ""),          # PD-05
        ("zlib-ng", "zlib-ng project", "2.1.6", "pkg:github/zlib-ng/zlib-ng@2.1.6", "depends-on", "active", "", ""),
        ("OpenSSL", "OpenSSL Software Foundation", "3.0.13", "pkg:generic/openssl@3.0.13", "depends-on", "active (LTS)", "2026-09-07", "CVE-2024-0727"),
        ("SQLite", "SQLite Consortium", "3.45.1", "pkg:generic/sqlite@3.45.1", "depends-on", "active", "", ""),
        ("Qt", "The Qt Company", "6.5.3", "pkg:generic/qt@6.5.3", "depends-on", "active (LTS)", "2026-05-26", ""),
        ("Linux kernel", "kernel.org / Halden BSP", "6.1.77", "pkg:generic/linux@6.1.77", "depends-on", "active (LTS)", "2026-12-31", ""),
        ("BlueZ", "bluez.org", "5.66", "pkg:generic/bluez@5.66", "depends-on", "active", "", ""),
        ("libcurl", "curl project", "8.5.0", "pkg:generic/curl@8.5.0", "depends-on", "active", "", "CVE-2023-46218"),
        ("protobuf", "Google", "25.2", "pkg:generic/protobuf@25.2", "depends-on", "active", "", ""),
        ("glibc", "GNU", "2.36", "pkg:generic/glibc@2.36", "depends-on", "active (Debian LTS)", "2026-06-30", ""),
        ("busybox", "busybox.net", "1.36.1", "pkg:generic/busybox@1.36.1", "depends-on", "active", "", ""),
        ("mbedtls (bootloader)", "Arm", "3.5.2", "pkg:generic/mbedtls@3.5.2", "depends-on", "active", "", ""),
        ("CS-Patch firmware interface lib", COMPANY, "2.4.0", "pkg:generic/cspatch-if@2.4.0", "depends-on", "active", "2032-12-31", "")]

# ------------------------------------------------------------------ security
THREATS = [("T-01", "Malicious update package installed via USB service port", ["IF-03"], ["SC-01"], ["ST-02"]),
           ("T-02", "Credential stuffing against clinician login", ["IF-04"], ["SC-02"], ["ST-03"]),
           ("T-03", "Theft of hub; extraction of episode store", ["IF-05"], ["SC-03"], ["ST-04"]),
           ("T-04", "Man-in-the-middle on portal synchronisation", ["IF-02"], ["SC-04", "SC-06"], ["ST-05"]),
           ("T-05", "Tampering with audit log to hide threshold changes", ["IF-05"], ["SC-05"], ["ST-06"]),
           ("T-06", "Replay of BLE sensor frames to inject false ECG", ["IF-01"], ["SC-07"], ["ST-07"]),
           ("T-07", "Denial of service on cloud sync listener", ["IF-02"], ["SC-08"], ["ST-07"]),
           ("T-08", "Unauthorised remote service session", ["IF-02"], ["SC-10"], ["ST-05"])]
SCS = [("SC-01", "Code, Data, and Execution Integrity", ["SEC-001"], "Bootloader and updater verify ECDSA P-256 signature", ["ST-02"], "L2-21.04"),
       ("SC-02", "Authentication", ["SEC-002"], "Password policy and lockout in auth service", ["ST-03"], "L2-21.01"),
       ("SC-03", "Confidentiality", ["SEC-003"], "AES-256-GCM store encryption, key in SE050", ["ST-04"], "L2-21.05"),
       ("SC-04", "Cryptography", ["SEC-004"], "TLS 1.2+ with pinned portal certificate", ["ST-05"], "L2-21.03"),
       ("SC-05", "Event Detection and Logging", ["SEC-005"], "Hash-chained audit log", ["ST-06"], "L2-21.06"),
       ("SC-06", "Authentication", ["SEC-006"], "Mutual TLS on sync listener (new in 3.2.0)", ["ST-05"], "L2-21.01"),
       ("SC-07", "Code, Data, and Execution Integrity", ["SRS-001"], "BLE frame counter and session nonce", ["ST-07"], "L2-21.04"),
       ("SC-08", "Resiliency and Recovery", ["SRS-024"], "Connection rate limiting; monitoring continues when sync unavailable", ["ST-07"], "L2-21.07"),
       ("SC-09", "Event Detection and Logging", ["SEC-005"], "Security event forwarding to portal", [], "L2-21.06"),   # PD-16 no verification test
       ("SC-10", "Authorization", ["SEC-002"], "Role-based access: clinician, admin, service", ["ST-03"], "L2-21.02")]
STS = [("ST-01", "L2-23.02", RB, PV, "2026-03-30 to 2026-03-31", "Halden product security team (separate from development)", ["SC-01"], ["T-01"]),
       ("ST-02", "L2-23.01", RB, PV, "2026-03-30 to 2026-03-31", "Halden product security team (separate from development)", ["SC-01"], []),
       ("ST-03", "L2-23.01", RB, PV, "2026-04-01 to 2026-04-01", "Halden product security team (separate from development)", ["SC-02", "SC-10"], []),
       ("ST-04", "L2-23.01", RB, PV, "2026-04-01 to 2026-04-02", "Halden product security team (separate from development)", ["SC-03"], []),
       ("ST-05", "L2-23.02", RB, PV, "2026-04-02 to 2026-04-03", "Halden product security team (separate from development)", ["SC-04", "SC-06", "SC-10"], ["T-04", "T-08"]),
       ("ST-06", "L2-23.01", RB, PV, "2026-04-03 to 2026-04-03", "Halden product security team (separate from development)", ["SC-05"], []),
       ("ST-07", "L2-23.03", RB, PV, "2026-04-04 to 2026-04-06", "Halden product security team (separate from development)", ["SC-07", "SC-08"], ["T-06", "T-07"])]
PEN = {"id": "PT-01", "build": "b1098", "ver": "3.1.0", "range": "2025-11-03 to 2025-11-14", "tester": "Halden internal development team (two engineers from the ARR software team)",
       "tools": ["nmap 7.94", "Burp Suite Pro 2025.9", "custom BLE fuzzer v0.3"], "scope": ["IF-01", "IF-02", "IF-03", "IF-04"], "findings_stmt": "3 findings (0 critical, 1 high, 2 medium)",
       "findings": [("PF-01", "high", "Session token not invalidated at logout", "fixed", "b1120", "2025-12-15"),
                    ("PF-02", "medium", "Verbose TLS error reveals library version", "fixed", "b1120", "2025-12-15")]}   # PD-03, PD-10b (count 3 vs 2 records)
VULNS = [("CVE-2024-0727", "OpenSSL 3.0.13", "SBOM scan (Grype 0.74, 2026-03-19)", False, "not applicable: PKCS12 parsing not used; compensating control none required", "not_affected"),
         ("CVE-2023-46218", "libcurl 8.5.0", "SBOM scan (Grype 0.74, 2026-03-19)", False, "cookie handling not used; portal client uses pinned TLS only", "not_affected"),
         ("CVE-2024-2511", "OpenSSL 1.1.1w", "SBOM scan (Grype 0.74, 2026-03-19)", False, "unbounded session cache growth; mitigated by rate limiting SC-08", "mitigated")]   # PD-12 component not in SBOM
ANOMS = [("ANM-101", "Audit export truncates entries > 4 kB", "system test", ["3.2.0"], "minor", "2026-04-02 fixed in b1187 hotpatch? no: deferred, workaround documented", "H-none"),
         ("ANM-102", "About screen shows build date in UTC not local", "system test", ["3.1.4", "3.2.0"], "minor", "deferred", ""),
         ("ANM-103", "Episode list scroll jitter on Hub v2", "formative usability", ["3.2.0"], "minor", "deferred", ""),
         ("ANM-104", "Classification latency 2.4 s under max load (requirement 2 s)", "system test", ["3.2.0"], "major", "deferred to 3.2.1; risk file H-07 updated", "H-07"),
         ("ANM-105", "Lead-off indicator flickers at low battery", "field (prior version)", ["3.1.4", "3.2.0"], "minor", "deferred", "H-04"),
         ("ANM-106", "Portal sync retry counter not reset after success", "integration test", ["3.2.0"], "minor", "deferred", "")]
# ANM-109 from TC-035 is deliberately absent (PD-15); list says build b1180 and "5 open" (PD-08)

VERSIONS = [("3.0.0", "b0912", "2025-03-14", "Initial design-controlled release candidate; bench study CS-PS-01", "CS-PS-01"),
            ("3.1.0", "b1098", "2025-10-20", "Portal sync, clinician login; penetration test PT-01", ""),
            ("3.1.4", "b1142", "2026-02-27", "Age-band recompute (SRS-013), false-positive tuning (SRS-012); full system regression", "CS-PS-02"),
            (PV, RB, BUILD_DATE, "Mutual-TLS sync listener (CH-31), load shedding notice text, About screen build id; release candidate", "")]
CHANGES = [("CH-29", "3.1.0", "3.1.4", ["SRS-012", "SRS-013", "U-03"], False),
           ("CH-30", "3.1.4", PV, ["SRS-024", "U-04", "notice text"], False),
           ("CH-31", "3.1.4", PV, ["SRS-009", "SEC-006", "SC-06", "IF-02", "sync listener"], True),   # security-relevant, dated via version 3.2.0 build 2026-03-21; threat model dated 2026-01-30 (PD-11)
           ("CH-32", "3.1.4", PV, ["SRS-015", "About screen"], False)]

DOCS_DEFS = [
    ("D01-Module-Cover", "Software Module Cover Letter and Contents", "1.0", "2026-05-01", "R. Lindqvist, Regulatory Affairs Director"),
    ("D02-Software-Description", "Software Description", "3.0", "2026-04-20", "M. Okafor, Systems Engineering Lead"),
    ("D03-Version-Configuration", "Software Version and Configuration Identification", "2.0", "2026-04-16", "P. Haas, Configuration Manager"),
    ("D04-SRS", "Software Requirements Specification", "4.2", "2026-02-12", "M. Okafor, Systems Engineering Lead"),
    ("D05-Architecture", "System and Software Architecture", "2.3", "2026-02-18", "M. Okafor, Systems Engineering Lead"),
    ("D06-SDS", "Software Design Specification", "2.1", "2026-02-25", "A. Reyes, Software Architect"),
    ("D07-Risk-File", "Software Risk Management File and Report", "3.1", "2026-04-12", "S. Brandt, Risk Manager; Dr. L. Meyer, Clinical"),
    ("D08-Lifecycle-Plans", "Software Development, Configuration Management and Maintenance Plan Summary", "1.4", "2026-01-15", "P. Haas, Configuration Manager"),
    ("D09-VV-Plan-Protocols", "Verification and Validation Plan and Protocol Index", "2.0", "2026-03-12", "K. Novak, V&V Lead"),
    ("D10-System-Verification-Report", "System Verification Report SVR-3.2", "2.0", "2026-04-10", "K. Novak, V&V Lead; QA: J. Doe"),
    ("D11-Unit-Integration-Summary", "Unit and Integration Test Summary", "1.0", "2026-04-09", "K. Novak, V&V Lead"),
    ("D12-Version-History", "Software Version History", "1.6", "2026-04-16", "P. Haas, Configuration Manager"),
    ("D13-Unresolved-Anomalies", "Unresolved Software Anomalies", "1.2", "2026-04-11", "K. Novak, V&V Lead"),
    ("D14-SOUP-OTS", "SOUP and Off-the-Shelf Software List and Anomaly Review", "2.2", "2026-03-12", "A. Reyes, Software Architect"),
    ("D15-SBOM", "Software Bill of Materials", "3.2.0-sbom-1", "2026-03-18", "DevSecOps pipeline (automated); reviewed P. Haas"),
    ("D16-Threat-Model", "Threat Model", "2.1", "2026-01-30", "E. Varga, Product Security Lead"),
    ("D17-Security-Risk-Assessment", "Cybersecurity Risk Assessment and Report", "2.0", "2026-04-09", "E. Varga, Product Security Lead"),
    ("D18-Security-Architecture", "Security Architecture: Controls and Views", "2.0", "2026-02-20", "E. Varga, Product Security Lead"),
    ("D19-Security-Testing", "Cybersecurity Testing Report", "1.1", "2026-04-08", "E. Varga, Product Security Lead"),
    ("D20-Vulnerability-Assessment", "Vulnerability Assessment", "1.0", "2026-03-19", "E. Varga, Product Security Lead"),
    ("D21-Cyber-Management-Plan", "Cybersecurity Management Plan (Postmarket)", "1.3", "2026-04-01", "E. Varga, Product Security Lead"),
    ("D22-Declarations", "Declarations of Conformity to Recognized Standards", "1.0", "2026-04-28", "R. Lindqvist, Regulatory Affairs Director"),
    ("D23-Labeling-Excerpt", "Instructions for Use: Software and Cybersecurity Sections (excerpt)", "IFU-ARR-07", "2026-04-22", "R. Lindqvist, Regulatory Affairs Director"),
]


def build():
    DOCS.mkdir(parents=True, exist_ok=True)
    for f in DOCS.glob("*.md"):
        f.unlink()
    meta = {d[0]: d for d in DOCS_DEFS}

    # D01
    d = meta["D01-Module-Cover"]
    toc = table(["Document", "Title", "Version", "Approval date"], [(x[0], x[1], x[2], x[3]) for x in DOCS_DEFS])
    doc(*d, f"""
## 1. Purpose
{COMPANY} submits the **software module** of the modular PMA P26xxxx for the {DEVICE}, a Class III device software function that detects and classifies cardiac arrhythmias from a single-lead wearable ECG patch and presents episodes to clinicians.

**Software version proposed for approval: {PV}**
**Release build identifier: {RB}**
**Module submission date: {SUBMIT}**
**Documentation Level: Enhanced** (a failure or latent flaw could present a probability of serious injury or death; see D07 pre-control severity).
**IEC 62304 software safety class: C** (see D03 section 4).

## 2. Modular PMA shell
This module corresponds to shell entry M3 "Software" of the accepted PMA shell (FDA acceptance letter dated 2025-08-22). Bench and clinical modules (M1, M2) reference software version 3.1.4 for study CS-PS-02; differences to {PV} are assessed in D12 section 5.

## 3. Contents
{toc}

## 4. Statement
All documents listed above describe software version {PV}, build {RB}, unless stated otherwise in the document.
""")

    # D02
    d = meta["D02-Software-Description"]
    doc(*d, f"""
## 1. Software operation
The ARR module receives ECG samples from the CS-Patch sensor over Bluetooth Low Energy, detects QRS complexes, classifies rhythm episodes (normal, atrial fibrillation, bradycardia, tachycardia, pause) and presents them on the CS-Patch Hub display and, after synchronisation, on the clinician portal. Intended users are cardiologists and cardiac nurses; patients wear the patch and see only lead-quality and alert indications.

## 2. Inputs and outputs
Inputs: ECG samples (256 Hz, 24-bit), lead impedance, patient age band (clinician entry), configurable thresholds (Table 4 of D04). Outputs: episode records (CS-ECG v1.2), alerts (pause, BLE link loss), audit log, synchronisation to portal.

## 3. Software specifics
- Final release version stated: **{PV}**, build {RB}.
- Hardware platforms: CS-Patch Hub v2 (i.MX8M, ARM64) and CS-Patch Hub v3 (i.MX93, ARM64).
- Software platforms / OS: Linux 5.15.y (Hub v2), Linux 6.1.77 Halden BSP (Hub v3). Qt 6.5.3 LTS UI framework.
- Hosting: on-device; portal synchronisation to Halden Cloud (AWS eu-central-1) over TLS. The portal is a separate device software function covered in module M4.
- OTS software is used: see D14 and D15.

## 4. Interfaces and other functions
IF-01 BLE sensor link; IF-02 portal synchronisation (HTTPS, mutual TLS from {PV}); IF-03 USB service port (updates, logs); IF-04 clinician login UI; IF-05 local encrypted store. A non-device function (battery statistics export) shares the hub and was assessed per the Multiple Function guidance (D07 Annex B).
""")

    # D03
    d = meta["D03-Version-Configuration"]
    cfg = [("CI-01", "ARR application", "software item", PV, "yes", "yes"), ("CI-02", "Classification model parameters", "model/reference data", "3.2.0-p4", "yes", "no"),
           ("CI-03", "libdsp", "SOUP", "4.1.2", "yes", "yes"), ("CI-04", "zlib-ng", "SOUP", "2.1.6", "yes", "yes"), ("CI-05", "OpenSSL", "SOUP", "3.0.13", "yes", "no"),
           ("CI-06", "SQLite", "SOUP", "3.45.1", "yes", "no"), ("CI-07", "Qt", "SOUP", "6.5.3", "yes", "no"), ("CI-08", "Linux kernel Hub v3 BSP", "OS", "6.1.77", "yes", "no"),
           ("CI-09", "Linux kernel Hub v2 BSP", "OS", "5.15.148", "yes", "no"), ("CI-10", "Bootloader (mbedtls)", "software item", "1.9.0 / mbedtls 3.5.2", "yes", "no")]
    doc(*d, f"""
## 1. Proposed release version
Proposed version: **{PV}**. Versioning rule: MAJOR.MINOR.PATCH per Halden SOP-SW-004; a build identifier `bNNNN` is assigned by the CI pipeline. The version, build identifier and build date are shown on the About screen (SRS-015) and in the device UDI-DI production identifier.

## 2. Release build record
- Release build identifier: **{RB}**
- Build date: {BUILD_DATE}
- Build environment: Yocto Kirkstone, GCC 11.4, CI runner image halden-ci:2026.03; reproducible-build hash 9f3c…e21a (full hash in DHF record CM-BLD-1187)
- Archive: DHF vault, record CM-BLD-1187

## 3. Configuration item list (release baseline {RB})
{table(["Item", "Name", "Type", "Version", "In release baseline", "Changed since 3.1.4"], cfg)}

## 4. Software safety classification
The software system is classified **IEC 62304 Class C**: a failure of the classification function can contribute to a hazardous situation (HS-01, HS-03) that may result in death or serious injury, and no external risk control measure reduces the probability to acceptable. Software items U-01 to U-05 are Class C; U-06 (UI theming) and U-08 (battery statistics) are segregated as Class A per the architecture (D05 section 3) with the segregation rationale in D06 section 2.

## 5. Baseline dates
- Code freeze: **{CODE_FREEZE}** (last change request implemented: CH-32)
- Verification complete attestation: {TEST_END}
- Release approval date: **{RELEASE}**
""")

    # D04
    d = meta["D04-SRS"]
    rows = [(r["id"], r["text"], r["cat"], "yes" if r["safety"] else "no", "yes" if r["crit"] else "no", r["method"], r["changed"]) for r in REQS]
    sec = [(s[0], s[1], s[2], "2026-02-11") for s in SEC_REQS]
    doc(*d, f"""
## 1. Requirement identification and traceability
Requirements are identified SRS-nnn (functional, performance, interface, platform, security) and SEC-nnn (security requirements derived from the threat model, D16). Each requirement states its verification method; the trace to test cases is held in the V&V protocol index (D09) and the trace matrix export TM-3.2 (DHF). Requirements changed for {PV} carry a change date of 2026-02-10 or later.

## 2. Software requirements
{table(["ID", "Requirement", "Category", "Safety-related", "Critical", "Verification", "Last change"], rows)}

## 3. Security requirements
{table(["ID", "Requirement", "Derived from", "Review date"], sec)}

## 4. Approval
SRS 4.2 approved 2026-02-12 by M. Okafor (Systems) and S. Brandt (Risk). Changes since 4.1: SRS-012, SRS-013 (CH-29), SRS-009/SEC-006 (CH-31), SRS-024 (CH-30), SRS-015 (CH-32).
""")

    # D05
    d = meta["D05-Architecture"]
    ifs = [("IF-01", "BLE 5.0 GATT, proprietary sensor profile", "CS-Patch sensor", "yes"), ("IF-02", "HTTPS/TLS 1.2+, mutual TLS, port 443 outbound", "Clinician portal", "yes"),
           ("IF-03", "USB 2.0 CDC service port", "Service tool", "yes"), ("IF-04", "Touch UI (Qt)", "Clinician / patient", "no"), ("IF-05", "Local file system (encrypted)", "Episode store", "no")]
    doc(*d, f"""
## 1. Modules and layers
Acquisition (U-01) → Detection (U-02) → Classification (U-03) → Load manager (U-04) → Settings and thresholds (U-05) → UI (U-06) → Update and integrity (U-07) → Battery statistics (U-08, non-device function). Sync service (U-09) handles IF-02.

## 2. Interfaces
{table(["Interface", "Protocol", "External party", "Crosses trust boundary"], ifs)}

## 3. SOUP items and segregation
SOUP items are listed in D14. Class A items U-06 and U-08 run in a separate process with a message-queue boundary; a fault in them cannot block the Class C pipeline (watchdog W-1).

## 4. Data flow
Samples → ring buffer → detector → classifier → episode store (AES-256-GCM) → sync queue → portal. Thresholds flow from U-05 to U-03 with range checks (SRS-019).
""")

    # D06
    d = meta["D06-SDS"]
    units = [("U-01", "Acquisition and lead quality", ["SRS-001", "SRS-008"]), ("U-02", "QRS detector", ["SRS-002"]), ("U-03", "Rhythm classifier", ["SRS-003", "SRS-004", "SRS-005", "SRS-012", "SRS-013"]),
             ("U-04", "Load manager", ["SRS-024", "SRS-016"]), ("U-05", "Settings", ["SRS-019", "SRS-011"]), ("U-06", "UI", ["SRS-006", "SRS-015", "SRS-023"]), ("U-07", "Update and integrity", ["SRS-010", "SEC-001"]),
             ("U-08", "Battery statistics (non-device)", []), ("U-09", "Sync service", ["SRS-009", "SEC-004", "SEC-006", "SRS-018", "SRS-007"])]
    doc(*d, f"""
## 1. Detailed design per unit
{table(["Unit", "Responsibility", "Implements requirements"], [(u[0], u[1], ", ".join(u[2]) or "—") for u in units])}

## 2. Segregation
U-06 and U-08 are Class A per D03 section 4; IPC boundary via ZeroMQ with bounded queues; watchdog W-1 restarts UI without affecting classification.

## 3. Design evidence dates
SDS 2.0 approved 2025-11-28 before unit testing started (2025-12-02); SDS 2.1 (this version) approved 2026-02-25 after CH-30/CH-31 design changes; unit tests for U-04 and U-09 were re-run (D11).
""")

    # D07
    d = meta["D07-Risk-File"]
    hz = [(h[0], h[1], h[2], h[3], h[4], ", ".join(h[5]), "yes" if h[6] else "no") for h in HAZ]
    rc = [(c[0], c[1], c[2], ", ".join(c[3]), ", ".join(c[4]), ", ".join(c[5]), c[6] or "—") for c in RCS]
    doc(*d, f"""
## 1. Risk management plan
Plan RMP-ARR-03 approved 2025-09-01 (S. Brandt). Acceptability criteria: severity × probability matrix (Annex A); for software failures the probability of occurrence of harm is set to 1 before controls (IEC/TR 80002-1 approach). Cybersecurity risks are assessed on exploitability in D17 and transferred here where they have a safety impact (D17 section 6).

## 2. Hazards and hazardous situations
{table(["Hazard", "Hazardous situation", "Description", "Harm", "Severity", "Contributing requirements", "Security origin"], hz)}

Initial evaluation (2025-09-15): HS-01, HS-02, HS-03, HS-05, HS-06, HS-07 unacceptable before controls; HS-04, HS-08 ALARP review required.

## 3. Risk control measures and verification
{table(["Control", "Hazard", "Measure", "Implementing requirements", "Design units", "Implementation verification tests", "Effectiveness verification"], rc)}

## 4. Residual risk
After controls, all hazardous situations are acceptable per the matrix except HS-07, which is ALARP with ANM-104 open (latency 2.4 s under maximum load); benefit-risk rationale in Annex C. HS-08 (store corruption during sync) was evaluated as acceptable without a dedicated control on the basis of SQLite journaling; see Annex D.

## 5. Overall residual risk and disclosure
Overall residual risk acceptable. Disclosed in labeling: pause alert limits, lead-off suppression behaviour, latency under load (ANM-104 workaround: reduce concurrent portal sync).

## 6. Risk management report
Report RMR-ARR-3.2 Rev 3.1 dated **2026-04-12**, software version covered **{PV}**, reviewed by S. Brandt (Risk), Dr. L. Meyer (Clinical) and M. Okafor (Systems). Post-production information: complaint and vigilance review per SOP-PMS-002, quarterly.
""")

    # D08
    d = meta["D08-Lifecycle-Plans"]
    doc(*d, f"""
## 1. Development plan
Software development plan SDP-ARR-02 (approved 2025-04-10) follows IEC 62304 Ed 1.1 with a staged V-model; agile sprints are used within implementation (AAMI TIR45:2023 referenced for sprint-level documentation). The DoC route to IEC 62304 (D22, DoC-1) covers clauses 5.1, 6 and 8 in addition to 5.2–5.8, 7 and 9.

## 2. Configuration management
CM plan CMP-ARR-02 (approved 2025-04-10): Git with signed tags, CI build identifiers bNNNN, baselines per release, change requests CR-nnnn with impact analysis; configuration items listed in D03.

## 3. Maintenance and problem resolution
Maintenance plan MP-ARR-01 (approved 2025-04-10): problem reports PR-nnnn triaged weekly; anomalies classified per ANSI/AAMI SW91; security vulnerabilities routed to the product security process (D21).

## 4. Tools and coding standards
C++17 with MISRA C++:2023 subset; static analysis (Coverity 2024.3) at every merge; unit test framework GoogleTest 1.14.
""")

    # D09
    d = meta["D09-VV-Plan-Protocols"]
    rows = [(t["id"], t["level"], ", ".join(t["reqs"]), t["rc"] or "—", t["proto"], t["approved"], "K. Novak") for t in TCS]
    doc(*d, f"""
## 1. Verification strategy
Unit tests (GoogleTest) per Class C unit; integration tests per interface; system tests per requirement on both hub platforms; software validation in simulated clinical use (SUV-03). Regression: full system regression on each release candidate; selective re-run after late changes per regression analysis RA-nnn (D10 section 5).

## 2. Declared test window
System verification of release candidate {RB}: **{TEST_START} to {TEST_END}**.

## 3. Test case and protocol index
{table(["Test case", "Level", "Requirements / design", "Risk control verified", "Protocol id / version", "Protocol approval", "Approver"], rows)}
""")

    # D10
    d = meta["D10-System-Verification-Report"]
    rows = [(r["id"], r["tc"], ", ".join(r["reqs"]), f"{r['ver']} ({r['build']})", "Hub v3 / Linux 6.1.77" if int(r["id"][3:]) % 2 else "Hub v2 / Linux 5.15.148", "libdsp 4.1.2; zlib-ng 2.1.6; OpenSSL 3.0.13; Qt 6.5.3", r["start"], r["end"], r["result"], r["anom"] or "—", r["retest"] or "—") for r in RUNS]
    n_pass = sum(r["result"] == "Pass" for r in RUNS); n_fail = sum(r["result"] == "Fail" for r in RUNS); n_block = sum(r["result"] == "Blocked" for r in RUNS)
    FAIL_RUN = next(r["id"] for r in RUNS if r["tc"] == "TC-018" and r["result"] == "Fail"); RETEST_RUN = next(r["id"] for r in RUNS if r["retest"] == FAIL_RUN)
    doc(*d, f"""
## 1. Scope
System verification of {DEVICE} version **{PV}**, release build **{RB}**, against SRS 4.2, executed per the protocols in D09 within the declared test window {TEST_START} to {TEST_END}.

## 2. Summary
**All 40 system test cases passed on build {RB}.** Software version tested: {PV}. No deviations from plan. Deferred anomalies: ANM-104, ANM-101.

## 3. Test environments
ENV-01 CS-Patch Hub v3, Linux 6.1.77, Qt 6.5.3, libdsp 4.1.2, zlib-ng 2.1.6, OpenSSL 3.0.13. ENV-02 CS-Patch Hub v2, Linux 5.15.148, same OTS versions. Test tools: Halden ECG simulator HES-4 v2.2, pytest 8.0 harness.

## 4. Execution records
{table(["Run", "Test case", "Requirements", "Version (build)", "Platform", "OTS in configuration", "Start", "End", "Result", "Anomaly", "Retest of"], rows)}

Executed {len(RUNS)} runs: {n_pass} pass, {n_fail} fail, {n_block} blocked. Observed results are recorded in the protocol execution sheets (DHF, VV-EXEC-3.2).

## 5. Failed tests and regression
{FAIL_RUN} (TC-018) failed on audit export truncation (ANM-101); fixed in the audit exporter configuration and re-run as {RETEST_RUN} (pass). TC-022 and TC-035 failures are deferred (see D13). Regression analysis RA-32-01 (2026-03-22) selected the full system set for re-run on {RB}; TC-031 was run on 3.1.4 ({PREV_B}) under TP-SYS-07 and is carried forward because the classifier parameters are unchanged (see D12 section 5).

## 6. Software validation
Simulated-use validation SUV-03 (2026-04-07, 6 clinicians, Hub v3) passed all 12 scenarios; report SUV-03-R1.
""")

    # D11
    d = meta["D11-Unit-Integration-Summary"]
    ut = [(f"UT-{u[0][2:]}", u[0], ", ".join(u[2]) or "—", f"{PV} ({RB})", "2026-03-23", "2026-03-24", "Pass", "GoogleTest 1.14; coverage 94% lines") for u in units if u[2]]
    it = [("IT-01", "IF-01", "SRS-001, SRS-008", f"{PV} ({RB})", "2026-03-25", "Pass"), ("IT-02", "IF-02", "SRS-009, SEC-004, SEC-006", f"{PV} ({RB})", "2026-03-26", "Pass"),
          ("IT-03", "IF-03", "SRS-010, SEC-001", f"{PV} ({RB})", "2026-03-26", "Pass"), ("IT-04", "IF-04", "SRS-020, SEC-002", f"{PV} ({RB})", "2026-03-27", "Pass"), ("IT-05", "IF-05", "SRS-007, SRS-021, SEC-003", f"{PV} ({RB})", "2026-03-27", "Pass")]
    doc(*d, f"""
## 1. Unit tests (Enhanced level)
{table(["Run", "Unit", "Requirements covered", "Version (build)", "Start", "End", "Result", "Tools / criteria"], ut)}

## 2. Integration tests
{table(["Run", "Interface", "Requirements covered", "Version (build)", "Date", "Result"], it)}

Unit acceptance criteria: 100% statement coverage of Class C safety functions, 90% overall (achieved 94%). Integration tests executed on ENV-01 and ENV-02.
""")

    # D12
    d = meta["D12-Version-History"]
    vh = [(v[0], v[1], v[2], v[3], v[4] or "—") for v in VERSIONS]
    ch = [(c[0], c[1], c[2], ", ".join(c[3]), "yes" if c[4] else "no") for c in CHANGES]
    doc(*d, f"""
## 1. Tested versions since design-control start
{table(["Version", "Build", "Date", "Testing / notes", "Used in bench or clinical study"], vh)}

## 2. Changes between tested versions
{table(["Change", "From", "To", "Affected items", "Safety/security relevant"], ch)}

## 3. Previously authorized versions
None; this is the initial PMA.

## 4. Final entry: tested versus released
Last fully tested version: **{PV}** ({RB}); version to be released: **{PV}** ({RB}). No differences.

## 5. Study version bridge
Bench study CS-PS-02 used 3.1.4 ({PREV_B}). Differences to {PV}: CH-30 (load manager notice), CH-31 (sync listener), CH-32 (About screen). None affects the detector or classifier parameters (CI-02 unchanged); assessment in D07 Annex E. Test TC-031 (TP-SYS-07) executed on 3.1.4 is therefore carried forward without re-execution.
""")

    # D13
    d = meta["D13-Unresolved-Anomalies"]
    rows = [(a[0], a[1], a[2], ", ".join(a[3]), a[4], a[5], a[6] or "—", "yes") for a in ANOMS]
    doc(*d, f"""
## 1. Scope
Unresolved anomalies for the release candidate, build **b1180**, software version {PV}, extracted from the problem tracker (Jira project ARR, filter "Open AND fixVersion != 3.2.0") on **2026-04-05**.

**Open anomalies: 5** (0 critical, 1 major, 4 minor).

## 2. Anomaly records
{table(["Anomaly", "Description", "Discovery", "Affected versions", "Class (SW91)", "Disposition", "Risk file link", "Security impact assessed"], rows)}

## 3. Workarounds communicated
ANM-104: reduce concurrent synchronisation during continuous monitoring (IFU section 9.3). ANM-101: export audit log in 4 kB pages.
""")

    # D14
    d = meta["D14-SOUP-OTS"]
    rows = [(s[0], s[1], s[2], s[3], s[4], s[5]) for s in SOUP]
    rv = [(r[0], r[1], r[2], r[3], r[4] or "none hazard-relevant", "yes" if r[5] else "no") for r in SOUP_REVIEW]
    doc(*d, f"""
## 1. SOUP / OTS identification
{table(["SOUP id", "Title", "Manufacturer / supplier", "Version", "Release / adoption date", "Function in device"], rows)}

Required hardware/software: see D02 section 3. Each SOUP item has functional and performance requirements in the SOUP requirements sheet SR-ARR-02 (DHF).

## 2. Published anomaly list review (IEC 62304 7.1.3)
{table(["SOUP id", "Anomaly list source", "List version scope", "Review date", "Hazard-relevant anomalies", "Security vulnerabilities cross-checked"], rv)}

## 3. Risk assessment of SOUP
SOUP-01 (libdsp) contributes to HS-01 and HS-03 (detector filtering); SOUP-02 to HS-08; others have no hazard contribution. Residual risk: see D07.

## 4. OTS verification
All SOUP items are exercised in the system tests of D10 at the versions listed in section 1 and in D15. Qt rendering glitch QTBUG-118 was evaluated against H-04 and found not applicable.

## 5. Control of versions in the field
Software is delivered as a signed monolithic image; users cannot install or update OTS components (SEC-001).
""")

    # D15
    d = meta["D15-SBOM"]
    rows = [(s[0], s[1], s[2], s[3], s[4], s[5], s[6] or "—", s[7] or "—") for s in SBOM]
    doc(*d, f"""
## 1. SBOM identity
Format: CycloneDX 1.5 (JSON; this document is the human-readable rendering). Generated **2026-03-18** by the DevSecOps pipeline (syft 0.105) for build **b1150**, software version {PV}. Transitive dependencies included. Covers the ARR application, bootloader and Hub v3 BSP; the Hub v2 BSP SBOM is a separate file (SBOM-HUBV2-5.15).

## 2. Components
{table(["Component", "Supplier", "Version", "Identifier", "Relationship", "Level of support", "End of support", "Known vulnerabilities"], rows)}
""", covers=PV)

    # D16
    d = meta["D16-Threat-Model"]
    th = [(t[0], t[1], ", ".join(t[2]), ", ".join(t[3]), ", ".join(t[4])) for t in THREATS]
    doc(*d, f"""
## 1. Identity
Threat model TM-ARR Rev 2.1 dated **2026-01-30**; methodology STRIDE per element with attack trees for T-01 and T-04 (MITRE playbook); configuration covered: **{PV}** (release candidate scope as designed in D05 Rev 2.2).

## 2. System decomposition
Assets: ECG samples, episode store, clinician credentials, audit log, update packages. Trust boundaries: BLE link (IF-01), portal link (IF-02), USB service port (IF-03). Processes: U-01 to U-09. Data stores: episode store, audit log, settings.

## 3. Assumptions
Hub is installed in a clinic or patient home; physical access by patient assumed; portal is a trusted but separately secured system; BLE pairing is performed by clinic staff.

## 4. Threats
{table(["Threat", "Attack vector", "Targeted elements", "Mitigating controls", "Threat-mitigation tests"], th)}

## 5. Lifecycle and supply chain
Build pipeline signing keys in HSM; SOUP intake review per D14; vulnerability monitoring per D21.
""")

    # D17
    d = meta["D17-Security-Risk-Assessment"]
    sra = [("SR-01", "T-01", "CWE-347 improper signature verification", "SC-01", "7.8 (CVSS 3.1 base) / exploitability high", "2.1", "controlled", "2026-04-08"),
           ("SR-02", "T-02", "CWE-307 excessive auth attempts", "SC-02, SC-10", "6.5 / medium", "2.0", "controlled", "2026-04-08"),
           ("SR-03", "T-03", "CWE-311 missing encryption", "SC-03", "6.1 / medium", "1.5", "controlled", "2026-04-08"),
           ("SR-04", "T-04", "CWE-295 improper certificate validation", "SC-04, SC-06", "8.1 / high", "2.2", "controlled", "2026-04-08"),
           ("SR-05", "T-05", "CWE-117 log tampering", "SC-05, SC-09", "5.3 / medium", "2.0", "controlled", "2026-04-08"),
           ("SR-06", "T-06", "CWE-294 replay", "SC-07", "7.1 / high", "2.5", "controlled; safety transfer to HS-02", "2026-04-08"),
           ("SR-07", "T-07", "CWE-400 resource exhaustion", "SC-08", "5.9 / medium", "2.0", "controlled; safety transfer to HS-07", "2026-04-08"),
           ("SR-08", "T-08", "CWE-287 improper authentication", "SC-10, SC-06", "7.5 / high", "2.0", "controlled", "2026-04-08")]
    doc(*d, f"""
## 1. Method
Security risk management plan SRMP-ARR-01 (approved 2025-06-20) per ANSI/AAMI SW96:2023; scoring with CVSS v3.1 base and the MITRE medical device rubric for exploitability; acceptance threshold: post-mitigation exploitability ≤ 3.0 and no unmitigated high.

## 2. Security risk entries
{table(["Risk", "Threat", "Vulnerability / weakness", "Controls", "Pre-mitigation", "Post-mitigation", "Status", "Evaluation date"], sra)}

## 3. Residual security risk
All entries below threshold. Overall residual security risk acceptable (E. Varga, 2026-04-09).

## 4. Risks arising from controls
Lockout (SC-02) can delay clinician access: transferred to usability task T7 (D07 Annex F).

## 5. Report
Security risk management report SRMR-ARR-3.2 Rev 2.0 dated **2026-04-09**, software version covered **{PV}**; traceability in section 7; version history: Rev 1.0 (3.1.0), Rev 2.0 (3.2.0).

## 6. Transfer to safety risk management
SR-06 → HS-02 (false episode from injected frames; security origin). SR-07 → HS-07 (overload). Both recorded in D07 section 2.

## 7. Traceability
Threat → risk → control → requirement → test: T-01/SR-01/SC-01/SEC-001/ST-01, ST-02; T-02/SR-02/SC-02,SC-10/SEC-002/ST-03; T-03/SR-03/SC-03/SEC-003/ST-04; T-04/SR-04/SC-04,SC-06/SEC-004,SEC-006/ST-05; T-05/SR-05/SC-05,SC-09/SEC-005/ST-06; T-06/SR-06/SC-07/SRS-001/ST-07; T-07/SR-07/SC-08/SRS-024/ST-07; T-08/SR-08/SC-10,SC-06/SEC-002,SEC-006/ST-05. Export date 2026-04-09.
""")

    # D18
    d = meta["D18-Security-Architecture"]
    sc = [(c[0], c[1], ", ".join(c[2]), c[3], ", ".join(c[4]) or "—") for c in SCS]
    paths = [("P-01", "IF-01", "BLE 5.0 GATT, LE Secure Connections", "sensor ↔ hub", "encrypted, authenticated pairing"), ("P-02", "IF-02", "HTTPS, TLS 1.2/1.3, port 443 outbound, mutual TLS", "hub → portal", "pinned certificate"),
             ("P-03", "IF-03", "USB CDC, service protocol v2", "service tool → hub", "signed packages only"), ("P-04", "IF-02", "Sync listener, TCP 8443 inbound (LAN only), mutual TLS", "portal → hub (new in 3.2.0)", "rate limited")]
    doc(*d, f"""
## 1. Security controls by category
{table(["Control", "Category", "Security requirements", "Implementation", "Verification tests"], sc)}

## 2. Views
Global system view, multi-patient harm view (portal fleet update), updatability/patchability view (signed images via IF-03 and IF-02) and security use-case views are in Annex A (diagrams SA-01 to SA-04).

## 3. Communication paths
{table(["Path", "Interface", "Protocol / ports", "Direction", "Protection"], paths)}
""")

    # D19
    d = meta["D19-Security-Testing"]
    st = [(s[0], {"L2-23.01": "security requirements test", "L2-23.02": "threat mitigation test", "L2-23.03": "vulnerability/fuzz test"}[s[1]], f"{s[3]} ({s[2]})", s[4], s[5], ", ".join(s[6]), ", ".join(s[7]) or "—", "none") for s in STS]
    pf = [(f[0], f[1], f[2], f[3], f[4], f[5]) for f in PEN["findings"]]
    doc(*d, f"""
## 1. Security requirements, threat-mitigation and vulnerability testing
{table(["Activity", "Type", "Version (build)", "Dates", "Tester", "Controls covered", "Threats covered", "Findings"], st)}

Tools: OWASP ZAP 2.14, boofuzz 0.4.2, Grype 0.74, Halden BLE fuzzer v0.4. Scope: IF-01 to IF-05. No findings; boundary assumptions in Annex B.

## 2. Penetration testing
Penetration test **{PEN['id']}** on version **{PEN['ver']}** (build **{PEN['build']}**), **{PEN['range']}**, performed by {PEN['tester']}. Tools: {', '.join(PEN['tools'])}. Scope: {', '.join(PEN['scope'])}. Methodology: OWASP MASVS/ASVS checklist plus manual exploitation. Duration: 10 person-days. Result: **{PEN['findings_stmt']}**. Original report PT-01-R1 is attached (Annex C).

{table(["Finding", "Severity", "Description", "Disposition", "Fixed in build", "Disposition date"], pf)}

No retest was performed; both findings were verified closed by code review. No penetration test has been performed on {PV}; the attack surface change of CH-31 (new inbound sync listener) was covered by threat-mitigation test ST-05.

## 3. Findings assessment and deferrals
No deferred security findings. Future-release plan: none required.
""")

    # D20
    d = meta["D20-Vulnerability-Assessment"]
    vu = [(v[0], v[1], v[2], "yes" if v[3] else "no", v[4], v[5]) for v in VULNS]
    doc(*d, f"""
## 1. Known vulnerabilities
Source: SBOM scan with Grype 0.74 against NVD and the CISA KEV catalogue on 2026-03-19 (KEV check date 2026-03-19). Scan target: SBOM for build b1150.

{table(["Vulnerability", "Component", "Discovery", "In CISA KEV", "Assessment", "Disposition"], vu)}

## 2. KEV
No KEV-listed vulnerabilities are present in the release.

## 3. Component support horizon
OpenSSL 3.0 LTS end of support 2026-09-07: migration to 3.3 LTS planned for release 3.3.0 (Q4 2026). Qt 6.5 LTS end 2026-05-26: commercial extended support contract in place to 2028.
""")

    # D21
    d = meta["D21-Cyber-Management-Plan"]
    doc(*d, f"""
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
""")

    # D22
    d = meta["D22-Declarations"]
    docs_ = [("DoC-1", "IEC 62304:2006 + AMD1:2015 (Edition 1.1)", "13-79", "5.1 (all), 5.2–5.8, 6, 7, 8, 9", "none", "2026-04-20"),
             ("DoC-2", "ISO 14971:2019 (third edition)", "5-125", "4–10", "none", "2026-04-20"),
             ("DoC-3", "ANSI/UL 2900-1, Second Edition (2023)", "13-96", "all", "none", "2026-04-20"),
             ("DoC-4", "IEC 62366-1:2015 + AMD1:2020 (Edition 1.1)", "5-129", "all", "none", "2026-04-20"),
             ("DoC-5", "IEC 81001-5-1:2021 (Edition 1.0)", "13-122", "4–9 (Annex A not claimed)", "none", "2026-04-20")]
    doc(*d, f"""
## 1. Declarations
Applicant: {COMPANY}, Industriestrasse 12, 30457 Hannover, Germany. Product: {DEVICE}, software version **{PV}**, build {RB}.

{table(["Declaration", "Standard and edition", "FDA recognition number", "Clauses claimed", "Deviations", "Date of issue"], docs_)}

Statement of conformity: the product identified above conforms to the standards listed, as declared. Place of issue: Hannover. Signatory: R. Lindqvist, Regulatory Affairs Director. Limitations on validity: declarations apply to software version {PV} as verified in D10 and D19; conformity activities completed by 2026-04-12.

## 2. Supplemental documentation (process standards)
IEC 62304: D08 and DHF plan records; IEC 62366-1: usability engineering file UEF-ARR-02 (module M5); IEC 81001-5-1: D16–D21. Standards used for general information without declaration: ANSI/AAMI SW96:2023, AAMI TIR57:2016, AAMI TIR45:2023, IEC TR 80002-1:2009.
""")

    # D23
    d = meta["D23-Labeling-Excerpt"]
    doc(*d, f"""
## 1. Software identification
This IFU applies to {DEVICE} software version **3.2.1**. The version and build identifier are shown under Settings → About.

## 2. Network ports and interfaces
BLE 5.0 (sensor), HTTPS outbound TCP 443 (portal), TCP 8443 inbound LAN-only (portal sync listener, mutual TLS), USB service port (updates by trained service personnel only).

## 3. Cybersecurity information for users
Recommended controls: place the hub on a segmented clinical network; do not connect unlisted USB devices. The SBOM for version 3.2.0 is available from the Halden customer portal. Security events are logged and forwarded to the portal; contact security@halden.example to report a vulnerability. Backup: episodes are synchronised to the portal; local recovery via Settings → Restore.

## 4. Support horizon
Software support for this version ends on 2032-12-31. Updates are notified through the portal and installed as signed images.

## 5. Residual risks and workarounds
Classification latency may exceed 2 s under maximum load; reduce concurrent synchronisation during continuous monitoring (ANM-104). Lead-off suppresses classification; check electrode contact when the quality indicator is amber.
""")

    # ------------------------------------------------------------- answer key
    defects = {
        "fixture": "SYN-PMA-SW-01", "generated_by": "review/v3/fixtures/gen_syn01.py", "anchors": {"A.proposed_version": PV, "A.release_build_id": RB, "A.code_freeze_date": CODE_FREEZE, "A.release_date": RELEASE, "A.module_submission_date": SUBMIT},
        "defects": [
            {"id": "PD-01", "title": "SRS-017 (safety-critical BLE link-loss alert) has no test case", "detect_by": ["CC-01"], "match_any": ["SRS-017"], "severity": "S3", "docs": ["D04", "D09"]},
            {"id": "PD-02", "title": "TC-031/TC-032/TC-037 (SRS-012/013) passed only on superseded build b1142; carried forward by narrative with no L2-10.04 bridge", "detect_by": ["CC-01"], "match_any": ["TC-031", "TC-032", "TC-037", "SRS-012", "SRS-013"], "severity": "S3", "docs": ["D10", "D12"]},
            {"id": "PD-08c", "title": "Anomaly list extracted 2026-04-05, before the last test run ended 2026-04-06", "detect_by": ["CC-06"], "match_any": ["extracted"], "severity": "S2", "docs": ["D13", "D10"]},
            {"id": "PD-03", "title": "Penetration test on v3.1.0 build b1098 (Nov 2025), not on the release build; no retest", "detect_by": ["CC-04", "CC-12"], "match_any": ["PT-01", "b1098"], "severity": "S3", "docs": ["D19"]},
            {"id": "PD-03b", "title": "Penetration tester is the internal development team; independence not shown", "detect_by": ["CC-23"], "match_any": ["PT-01"], "severity": "S2", "docs": ["D19"]},
            {"id": "PD-04a", "title": "SBOM generated 2026-03-18, before code freeze 2026-03-20", "detect_by": ["CC-12"], "match_any": ["sbom"], "severity": "S3", "docs": ["D15"]},
            {"id": "PD-04b", "title": "SBOM describes build b1150, release build is b1187", "detect_by": ["CC-05", "rule"], "match_any": ["b1150"], "severity": "S3", "docs": ["D15"]},
            {"id": "PD-05", "title": "libdsp version 4.1.2 in SOUP list and config items vs 4.1.0 in SBOM", "detect_by": ["CC-03", "CC-11"], "match_any": ["libdsp", "SOUP-01"], "severity": "S3", "docs": ["D14", "D15"]},
            {"id": "PD-06a", "title": "zlib-ng anomaly review covers 2.1.3, SOUP in use is 2.1.6", "detect_by": ["CC-03"], "match_any": ["zlib", "SOUP-02"], "severity": "S3", "docs": ["D14"]},
            {"id": "PD-06b", "title": "zlib-ng anomaly review dated 2025-10-02 precedes adoption 2026-01-10", "detect_by": ["CC-12"], "match_any": ["zlib", "SOUP-02"], "severity": "S2", "docs": ["D14"]},
            {"id": "PD-07", "title": "RC-07 (load shedding) has no effectiveness verification evidence", "detect_by": ["CC-02"], "match_any": ["RC-07"], "severity": "S3", "docs": ["D07"]},
            {"id": "PD-08a", "title": "Unresolved anomaly list describes build b1180, not release build b1187", "detect_by": ["CC-06", "CC-05", "anchor"], "match_any": ["b1180"], "severity": "S3", "docs": ["D13"]},
            {"id": "PD-08b", "title": "Anomaly list states 5 open; 6 records listed", "detect_by": ["CC-22"], "match_any": ["anomal"], "severity": "S2", "docs": ["D13"]},
            {"id": "PD-09", "title": "DoC-3 cites UL 2900-1 Second Edition under 13-96; recognized edition is the First Edition 2017", "detect_by": ["CC-07"], "match_any": ["DoC-3", "2900"], "severity": "S3", "docs": ["D22"]},
            {"id": "PD-10a", "title": "SVR summary says all 40 system tests passed; records show 2 fail and 1 blocked", "detect_by": ["CC-22"], "match_any": ["SVR", "passed"], "severity": "S2", "docs": ["D10"]},
            {"id": "PD-10b", "title": "Pen test states 3 findings; 2 finding records", "detect_by": ["CC-22"], "match_any": ["PT-01"], "severity": "S2", "docs": ["D19"]},
            {"id": "PD-11", "title": "Threat model dated 2026-01-30 predates security-relevant change CH-31 (inbound sync listener) in 3.2.0", "detect_by": ["CC-12"], "match_any": ["CH-31", "threat model"], "severity": "S2", "docs": ["D16", "D12"]},
            {"id": "PD-12", "title": "CVE-2024-2511 assessed against OpenSSL 1.1.1w, a component not in the SBOM", "detect_by": ["CC-13"], "match_any": ["CVE-2024-2511", "1.1.1w"], "severity": "S3", "docs": ["D20", "D15"]},
            {"id": "PD-13", "title": "TC-008 run executed 2026-03-24, protocol TP-SYS-03 approved 2026-03-25", "detect_by": ["CC-12"], "match_any": ["TC-008"], "severity": "S2", "docs": ["D09", "D10"]},
            {"id": "PD-14", "title": "IFU states software version 3.2.1; proposed is 3.2.0", "detect_by": ["CC-05", "anchor"], "match_any": ["3.2.1"], "severity": "S3", "docs": ["D23"]},
            {"id": "PD-15", "title": "TC-035 failed raising ANM-109, which is not on the unresolved anomaly list and has no retest", "detect_by": ["CC-06"], "match_any": ["ANM-109"], "severity": "S3", "docs": ["D10", "D13"]},
            {"id": "PD-16", "title": "Security control SC-09 (event forwarding) has no verification test", "detect_by": ["CC-04"], "match_any": ["SC-09"], "severity": "S3", "docs": ["D18"]},
            {"id": "PD-17", "title": "Hazard H-08 / HS-08 has no risk control traced (acceptability argued in an annex)", "detect_by": ["CC-02"], "match_any": ["H-08", "HS-08"], "severity": "S2", "docs": ["D07"]},
        ],
        "unplanted_kept": [
            {"id": "UK-01", "title": "CH-29 and CH-30 marked not safety-relevant although they change safety-related requirements", "detect_by": ["independent"], "match_any": ["CH-29", "CH-30"]},
            {"id": "UK-02", "title": "SRS change dates (2025-11-20) do not match the changes the SRS says they received", "detect_by": ["independent"], "match_any": ["2025-11-20", "change date"]},
            {"id": "UK-03", "title": "SR-06/SR-07 transferred with security origin per D17; hazard table says security origin no", "detect_by": ["independent"], "match_any": ["security origin", "SR-06", "SR-07"]},
            {"id": "UK-04", "title": "H-02 unacceptable before controls has no risk control", "detect_by": ["CC-02", "independent"], "match_any": ["H-02", "HS-02"]},
            {"id": "UK-05", "title": "SOUP list covers 6 of 13 third-party SBOM components; seven have no anomaly-list review", "detect_by": ["CC-03", "CC-11", "independent"], "match_any": ["bluez", "libcurl", "curl", "protobuf", "glibc", "busybox", "mbedtls"]}
        ],
        "expected_no_finding": [
            {"id": "OK-01", "title": "TC-018 fail followed by passing retest TR-0443 must not be flagged", "match_any": ["TR-0418", "ANM-101 raised"]},
            {"id": "OK-02", "title": "DoC-1 to IEC 62304 Ed 1.1 under 13-79 with clauses 5.1, 6, 8 is valid", "match_any": ["DoC-1"]},
            {"id": "OK-03", "title": "Executor identity per run is DHF scope; absence is normal", "match_any": ["executor_identity"]},
        ],
    }
    (OUT / "defects.json").write_text(json.dumps(defects, indent=1, ensure_ascii=False) + "\n")
    (OUT / "README.md").write_text(f"# SYN-PMA-SW-01\n\nSynthetic, fictional PMA software module for testing review/v3. {len(DOCS_DEFS)} documents in `docs/`, planted defects in `defects.json`. Regenerate with `python3 review/v3/fixtures/gen_syn01.py`.\n\nAll names, products, identifiers and results are invented. Nothing here describes a real device or company.\n")
    print(f"wrote {len(list(DOCS.glob('*.md')))} documents and {len(defects['defects'])} planted defects to {OUT}")


if __name__ == "__main__":
    build()
