# Standards axis for the PMA software module (review v3)

Research draft, 2026-10-01. This folder supplies the standards backbone for a review profile of a **modular PMA, software module first**, at the **Enhanced** Documentation Level. No existing repository file was changed.

| File | What it contains |
|---|---|
| `STANDARDS-REGISTER.md` | 92 rows: 20 authorities, 63 standard rows covering about 95 designations, and 9 references. Each row gives the exact library filename, live FDA recognition status, a relevance class and reviewer checks. It also contains the library gaps, the 17-item Declaration of Conformity check list and the recognition lookup log. |
| `BIN-HIERARCHY.json` | 31 L1 bins, 172 L2 sub-elements, 800 L3 parameters (668 mechanical, 132 judgment; 603 required at Enhanced) and 210 document-level parameters. 17 anchors (`A.*`) bind all version and date checks. Every cross-reference has been machine-checked to resolve. |
| `CONSISTENCY-CHAINS.md` | 25 cross-bin chains: 19 mechanical (2 of them with a judgment element), 5 mixed and 1 judgment. CC-12 contains 18 date-ordering checks. |

## Verified from the PDFs I opened

Text was extracted with pypdf, and with pymupdf for UL 2900. Clause numbers come from the documents themselves. Paraphrases are kept short.

- **FDA guidances.**
  - Software functions 2023: read in full, including V, VI.A–J and Table 1.
  - Cybersecurity 2026: IV.B–D, V.A.1–6, V.B.1–2, V.C, VI.A–B, VII.A–E, and Appendices 2, 3 and 4. Appendix 1 by heading only.
  - OTS 2023: III–IV.
  - Standards use 2018: IV.A(1)–(3), Table 1, IV.B, V, VI, VIII.
  - Human factors content 2026: III–V.
  - Human factors 2016 (reissued 2026): TOC and section 8.
  - Modular PMA 2025: VI.B–C and Appendices II–III.
  - PMA acceptance and filing 2019: item 12.
  - Draft PMA eSTAR 2026: III and Table 1.
  - 21 CFR 814.20: eCFR text and the library PDF.
- **Standards.**
  - IEC 62304 Ed 1.1: every clause 4–9 heading, plus the text of 5.3.3–5.3.5, 5.6.7, 5.7.5, 5.8.x, 7.1.3, 8.1.2–8.1.3 and 9.8.
  - ISO 14971:2019: 4.4, 4.5, 7.2, 8, 9 and 10.
  - IEC 81001-5-1: all clause headings, plus the text of 4.1.5, 4.3, 5.1.1, 5.7.1–5.7.5, 5.8.1–5.8.3, 7.2–7.4 and 8.
  - ANSI/AAMI SW96: headings and Annex C.1–C.6.
  - IEC 62366-1 Ed 1.1: headings, plus the text of 5.1, 5.5, 5.6, 5.7.3 and 5.9.
  - IEC 60601-1 Ed 3.2: 14.1 and 14.13.
  - IEC 82304-1: 7.1.
  - UL 2900-1:2026 and UL 2900-2-1 (2023 revision): edition statements and contents.
  - NTIA SBOM Minimum Elements: the field list.
- **Opened for structure only (TOC or headings):** TIR57, TIR97, IEC 62443-4-1, ISO/IEC 29147, ISO/IEC 30111, ISO/IEC/IEEE 29119-2 and -3, SW91, IEC 80001-1:2021, TIR34971:2023, CR515, IEC TR 80002-1, IEC 60601-1-6, TIR45.
- **Could not open:** `30416038.pdf` and `30416046.pdf` (DRM; pypdf, PDFKit and pymupdf all failed), and `iec62443-2-4{ed2.0}b.zip`.

## Verified from the FDA database (live, 2026-10-01)

I read 121 SIS detail pages. They support 60 stated recognition numbers, recorded with edition, extent, list number, date of entry and any transition date. About 35 designations returned no record and are marked not recognized.

Findings that matter for review:

- **Edition traps.** The library holds non-recognized editions of several standards: ISO/IEC 29147:2018 (recognized edition is 2014, 13-77), ISO/IEC 30111:2019 (2013, 13-78), UL 2900-1 2nd edition (1st edition 2017, 13-96), HE75:2025 (2009/R2018, partial, 5-57), IEC 62443-2-1 Ed 2.0, ISO/IEC/IEEE 15026-1:2019, and IEC 80001-1:2021 (only 2010 is recognized).
- **AI risk guide.** The recognized designation is AAMI **CR34971:2022** (13-124). The library holds TIR34971:2023.
- **Partial recognitions.** IEEE 11073-40101 excludes 8.6. HE75 excludes section 9.
- **Open transitions.**
  - CVSS v3.0: DoC accepted until 2026-12-20.
  - CVSS v3.1: until 2028-07-02 (v4.0 is 13-140).
  - TIR45:2012: until 2028-07-02.
  - ISO 20417:2021: until 2029-07-01.
- **SIS cautions.** Every cybersecurity SIS states that conformance may not satisfy 524B. The SIS for 14971, SW96 and TIR57 adds that cybersecurity risk uses exploitability, not probability. That note is now part of check L2-13.01.
- **Not recognized:** ISO 13485 (it is incorporated by reference into the QMSR), ISO/IEC 27001, IEC 62443-4-2 and 3-3, ISO/TR 24971, ISO/TS 24971-2, ISO/IEC 17025 and IEC TR 60601-4-5.

## Still UNVERIFIED

- Whether these citations are accepted under the listed recognition:
  - IEC 62443-4-1 under 13-119, which names ANSI/ISA-62443-4-1-2018.
  - ISO/IEEE 11073-40102:2022 under 13-118, which names IEEE 2020.
  - The UL 2900-2-1 2023 revision under 13-104.
  - The R2023 printings of TIR57 and TIR97.
  - IEC 81001-5-1 ISH1:2025.
  - TIR34971:2023 as equivalent to CR34971:2022.
- 29119-1: two editions are listed with no transition statement.
- Five context designations were not searched.
- Sub-field names inside the eSTAR sections were taken from an earlier template transcript. The PMA eSTAR draft itself **excludes modules and modular shells**, so a software module is filed outside eSTAR.
- The 524B statute HTML was not opened directly. Its content was taken from the cybersecurity guidance, section VII.

## Library gaps

The library was re-listed after the coordinator's update. Items added during the run are not counted as gaps. Full detail is in `STANDARDS-REGISTER.md`, section "Library gaps".

- **Absent:** IEC 60601-1-8, IEEE 11073-40101, ANSI/NEMA HN 1 (MDS2), CVSS specifications, the IEC TR 80001-2-x series, the UL 2800-1 series, IEEE/UL 2621.2, CLSI AUTO11-A2 and AUTO09-A, ASME V&V 40, AAMI TIR36, ISO/IEC 17050-1 and -2, ISO/IEC 27001/27002 (context only), IEC TR 60601-4-5, and the NTIA Framing document that the cybersecurity guidance actually cites.
- **Superseded copy:** the CSA guidance in the library is the Sept 2025 edition; the current edition is Feb 3 2026.
- **Library defect, now resolved:** a file named `FDA-Cybersecurity-Networked-Devices-OTS-2005.pdf` briefly held the bytes of the 2026 cybersecurity guidance and was later removed.

## Ten places where the existing `review/` bins are too coarse

Element IDs below are from `review/profiles/CORE-COVERAGE.md` and `AUTHORITIES.json`.

| # | Existing bin | Why it is too coarse | Replaced by |
|---|---|---|---|
| 1 | **SW-H** (all software testing in one row) | Cannot tell whether a test ran on the proposed build, after code freeze, under an approved protocol, by whom, or on which platform. Enhanced unit and integration reports are not separated. | L1-09: L2-09.01–09.09 (run L3 from 62304 5.7.5 a)–g) and 9.8); chains CC-01, CC-12 b/c/d/l, CC-18 |
| 2 | **FDA-STD** (one authority row, no declaration check anywhere) | There is no check of edition, recognition number, extent, transition, signatory, lab accreditation or promissory language. | L1-28: L2-28.01–28.10; register DoC checks 1–17; chains CC-07, CC-24 |
| 3 | **SW-G** (practices or DoC, one sentence) | The 62304 DoC route at Enhanced needs clauses 5.1, 6 and 8 plus supplemental documentation; CM and maintenance plans are separate deliverables. | L1-08: L2-08.01–08.04; L2-28.03 and L2-28.05 |
| 4 | **CY-A4 / CY-VII3** (SBOM) | Missing: build binding, generation date, NTIA fields, support level and end-of-support date, and the vulnerability scan source and date. | L1-16: L2-16.01–16.03; L1-17: L2-17.01–17.04; chains CC-05, CC-11, CC-13, CC-14 |
| 5 | **CY-C1–C4** (four testing rows) | Missing: penetration-test build, date range, tester independence, tool versions and settings, scope against interfaces, findings reconciliation, retest build and the original third-party report. | L1-23: L2-23.01–23.07; chains CC-04, CC-12 e/f, CC-15, CC-22, CC-23 |
| 6 | **SW-C / Q-RISK** (risk management file in one row) | ISO 14971 4.4 criteria before evaluation, 7.2 implementation versus effectiveness, 8 overall residual risk and 9 review before release are not separate. The security-to-safety transfer is missing. | L1-04: L2-04.01–04.09; L2-15.05; chains CC-02, CC-10, CC-12 a/g, CC-17 |
| 7 | **SW-J / CY-A5** (anomalies) | The anomaly list's build, extraction date, query scope and counts are not captured. There is no equality check between the unresolved, security-assessed and deferred anomaly sets. | L1-11: L2-11.01–11.04; L1-18: L2-18.01; chain CC-06 |
| 8 | **SW-I / SW-CHANGE / Q-CONFIG** (version and change) | There is no single version anchor, build id, code-freeze date or tested-versus-released bridge, and no modular reopening check. | L1-03: L2-03.01–03.04; L1-10: L2-10.01–10.05; L2-00.03; chains CC-05, CC-09, CC-21 |
| 9 | **D-HF** (one intake row) | There are no IEC 62366-1 clause bins, no HF Submission Category, and no check of summative testing on the final UI and labeling. | L1-27: L2-27.01–27.11; chains CC-08, CC-16 |
| 10 | **OTS/SOUP** (folded into SW-B and CY-A4) | Version-specific supplier anomaly review, validated configuration and the Enhanced assurance of developer methodology are lost. | L1-12: L2-12.01–12.09; chains CC-03, CC-11, CC-18 |

Other bins are also split. CY-A1 (threat model) becomes L1-14, which adds threat-model version, date and covered configuration. CY-B1/B2 become L1-21 (eight control-category L2s) and L1-22 (views plus Appendix 2 path details). CY-VIA becomes L1-24 (13 labeling items). CY-VIB/VII2 become L1-25 (management plan plus the 524B(b)(2) cycles).

## Suggested next steps (not done here)

1. Have a human approve the relevance classes and importance values in the register.
2. Map L1/L2 ids into `profiles/QUESTIONS.json` and `COVERAGE.csv` as a v3 profile.
3. Add anchor resolution and the mechanical chains (CC-05, CC-07, CC-12) to the recomposition tool.
4. Re-run the recognition lookups before any real case, because the database changes at least twice a year.
