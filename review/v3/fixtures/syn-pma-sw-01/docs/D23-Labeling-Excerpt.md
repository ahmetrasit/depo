# Instructions for Use: Software and Cybersecurity Sections (excerpt)

**Document ID:** D23-Labeling-Excerpt  
**Document version:** IFU-ARR-07  
**Approval date:** 2026-04-22  
**Approved by:** R. Lindqvist, Regulatory Affairs Director  
**Software version covered:** 3.2.0  
**Applicant:** Halden Cardiac Systems GmbH (fictional)  
**Device:** CardioSense ARR Software Module

## 1. Software identification
This IFU applies to CardioSense ARR Software Module software version **3.2.1**. The version and build identifier are shown under Settings → About.

## 2. Network ports and interfaces
BLE 5.0 (sensor), HTTPS outbound TCP 443 (portal), TCP 8443 inbound LAN-only (portal sync listener, mutual TLS), USB service port (updates by trained service personnel only).

## 3. Cybersecurity information for users
Recommended controls: place the hub on a segmented clinical network; do not connect unlisted USB devices. The SBOM for version 3.2.0 is available from the Halden customer portal. Security events are logged and forwarded to the portal; contact security@halden.example to report a vulnerability. Backup: episodes are synchronised to the portal; local recovery via Settings → Restore.

## 4. Support horizon
Software support for this version ends on 2032-12-31. Updates are notified through the portal and installed as signed images.

## 5. Residual risks and workarounds
Classification latency may exceed 2 s under maximum load; reduce concurrent synchronisation during continuous monitoring (ANM-104). Lead-off suppresses classification; check electrode contact when the quality indicator is amber.
