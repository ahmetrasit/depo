# Run 1 — SYN-PMA-SW-01 with model extraction

Date: 2026-10-01. Fixture: `fixtures/syn-pma-sw-01` as generated at the time of the run (snapshot in `docs-snapshot/`; the generator was corrected afterwards, see "Fixture bugs"). Profile: `profile/profile.json` built from `activation.json` (18 L1, 91 L2, 518 parameters). Agents: three extraction agents and three original-first independent agents, all Opus 5.5, each given one self-contained job file. The independent agents never saw extraction output.

## Headline

| Measure | Oracle extraction | Model extraction, as first recomposed | Model extraction, after three tool fixes |
|---|---|---|---|
| Planted defects detected (of 23) | 23 | 22 | 23 |
| Unmatched S2/S3 breaks (false-positive candidates) | 0 | 46 | 27 |
| Unmatched S1 (parameter-gap aggregates) | 28 | 56 | 56 |
| Entity recall against the oracle | 1.00 | 0.96 | 0.96 |
| Parameter fill against the oracle, agreement when filled | 1.00 / 1.00 | 0.93 / 0.96 | 0.94 / 0.96 |
| Reviewer candidates from the independent pass | 3 | 295 | 295 |

The three tool fixes were made on the same agent returns, with no new model run: deterministic alias resolution for component entities (the same SOUP item had been extracted under five identifiers across agents), a guard so security requirements routed into the controls bin are not treated as controls, and anomaly-list membership defined by the anomaly-list document rather than by any mention of an anomaly ID. The oracle result was unchanged by these fixes.

## What the model run got right

- Every table row became an entity. Across the three extractors, 615 entities, 47 anchor statements, 23 document records, 55 notes and 18 unbinned items. Every quote was an exact substring of its document; the extractors verified this themselves before returning.
- All anchors the fixture states were found, and every planted disagreement surfaced as an anchor conflict: release build b1187 versus b1180 in the anomaly list, labeled version 3.2.1 versus 3.2.0, SBOM build b1150.
- The one planted defect missed on the first pass (PD-15, a failed run whose anomaly is absent from the unresolved list) was missed because an extractor created an anomaly entity from the test-run row that mentioned it. That is an extraction over-reach the tool now guards against; it is also exactly the kind of thing the prompt should forbid, and now does.
- The independent agents found every planted defect in their bins without seeing extraction output, and additionally found eight genuine inconsistencies the fixture author had not planted (listed below).

## What produced noise

- **Identity fragmentation.** Extractors chose different IDs for the same component: `SOUP-01`, `libdsp`, `libdsp 4.1.0`, `CI-03`, `pkg:generic/libdsp@4.1.0`. Before alias resolution this produced 20 spurious SOUP chain breaks. After resolution, 12 remain, and most of those are a real inconsistency: the SBOM lists 13 third-party components, the sponsor's SOUP list only 6, so seven components have no anomaly-list review. The independent agents raised the same point.
- **Anchor phrasing.** Document-version anchors (risk file version, threat model version, supported platforms) were stated by different agents in different words and flagged as conflicts although they agree in substance. These anchors need a structured shape (id, version, date, covered version) rather than free text.
- **Parameter-gap aggregates.** 56 S1 findings say that some submission-scope parameter is unfilled for some entities. Most are honest: the fixture does not state them. A few are profile defects: `why_appropriate` and `design_limitations` on every SOUP row, and `device_in_standard_scope` on every declaration, read as required where the fixture (and most real submissions) would not state them per row.
- **Independent-pass volume.** 295 candidates from three agents, with heavy duplication across agents and across bins. They are candidates, not breaks, and they are where the most interesting unplanted findings live, but the report needs grouping and deduplication before a reviewer can use it.

## Unplanted inconsistencies found by the independent pass (fixture bugs)

These are real inconsistencies in the generated fixture that were not in the answer key. They are evidence the method finds things its author did not intend, and they are generator defects to fix:

1. The system verification report narrative names runs TR-0418 and TR-0443 for the TC-018 failure and retest; the table has TR-0440 and TR-0441.
2. The narrative says TC-032 and TC-037 were run on 3.1.4 and carried forward; the table shows them on b1187. Only TC-031 was actually planted on the old build.
3. The version history marks CH-29 and CH-30 as not safety-relevant although they change safety-related requirements.
4. SRS change dates do not match the changes the SRS says they received.
5. Test case numbering skips TC-026; unit UT-08 is absent from the unit table.
6. The security risk assessment says SR-06 and SR-07 were transferred to the safety file with security origin; the hazard table marks both "security origin: no".
7. Hazard H-02, unacceptable before controls, has no control at all (only H-08 was planted that way).
8. The SOUP list covers 6 of the 13 third-party SBOM components.

Items 1 and 2 are corrected in the generator after this run. Item 5 is left in place as a documented numbering gap. Items 3, 4, 6, 7 and 8 are kept deliberately as additional, now documented, defects for run 2 and recorded in the answer key under `unplanted_kept`.

## Reviewer-facing observations the chains cannot make

The independent agents raised several points that require judgment and that no chain computes: the penetration test was never repeated on the release although a new inbound listener was added; Qt and OpenSSL support ends during 2026 while device support runs to 2032; the same person approves every security document; the UI unit is Class A by segregation yet implements safety-related requirements. These belong in the report as candidates, and they are there.

## Cost

Six agents, about 560,000 tokens in total, under five minutes wall time each. The recomposition itself runs in under two seconds.

## Changes made because of this run

- `tools/v3.py`: alias resolution in the registry (exact identifier matches and version-stripped names, component types only, every merge recorded under `aliases`).
- `tools/recompose.py`: controls are only `security_control` entities with a control id; anomaly-list membership comes from the anomaly-list document; SBOM lookup accepts aliases and unique identifiers; SOUP chain runs only on rows with SOUP-list parameters.
- `prompts/decompose.md`: routing by document role, one id per object, and the labeled-version anchor restricted to the IFU's own statement.
- `fixtures/gen_syn01.py`: narrative run ids and the carried-forward test list corrected; the five kept inconsistencies recorded in the answer key.

## Files

`report/report.html` and `report.json` are the recomposition after the tool fixes; `report/score.json` and `compare_oracle.json` the scoring; `returns/` the three extraction returns; `independent/` the three original-first returns; `docs-snapshot/` the exact documents the agents read; `jobs/J-I-01.md` one independent job as rendered and `jobs/J-D-01.prompt-head.md` the first part of one extraction job (the full job is the prompt plus the documents). The oracle run on the same profile is in `../syn-pma-sw-01-oracle/`.

## Re-run of the same returns through the retooled recomposition (later on 2026-10-01)

No new model run. The three extraction returns and three independent returns above were re-registered and recomposed with the tools as changed after this run: structured anchors, grouped independent candidates with corroboration, a reverse SBOM-to-SOUP check in CC-11, component names in CC-03 messages, and the profile tidy-ups (SOUP `why_appropriate`/`design_limitations` and declaration `device_in_standard_scope` no longer required per row). Report in `report-retooled/`.

| Measure | After the three tool fixes (above) | Retooled |
|---|---|---|
| Planted defects detected (of 23) | 23 | 23 |
| Kept unplanted inconsistencies detected (of 5) | not scored | 5 |
| Anchor conflicts | 6 (3 planted, 3 phrasing) | 2 (both planted) |
| Unmatched S2/S3 breaks | 27 | 19 |
| Reviewer candidates | 295 statements, ungrouped | 228 groups from 285 statements; 88 corroborate a break, 130 new |

The 19 remaining unmatched S2/S3 breaks: five parameter-gap aggregates where the extractors left fields empty; six about the Hub v2 Linux kernel, whose SBOM the fixture says is a separate file that is not supplied (a real gap the independent agents also raised); five CC-04 items where an extractor filed a test anomaly and the SBOM-scan CVEs as security findings without their dispositions (extraction noise); two tester-independence statements on a document-level entity that duplicate planted defect PD-07; one anomaly whose risk-file link is `H-none`, which is a real fixture quirk worth a reviewer's glance.

The free-text anchors for the risk file and threat model from this run do not fit the structured shapes and resolve to nothing; that is expected for legacy returns and is what the revised prompt fixes for run 2. The oracle, re-run on the regenerated fixture with the same tools, stays at 23 of 23 with no unmatched S2/S3 finding and now also finds UK-04 and UK-05 mechanically (`../syn-pma-sw-01-oracle/report/`).
