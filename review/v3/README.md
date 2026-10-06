# review/v3 — lightweight decompose/recompose for a PMA software module

v3 tests one question: does decomposing a software module into standards-derived bins and recomposing it through entity joins make missing, inconsistent and stale evidence visible? It deliberately drops the integrity machinery of runtime 2.1 (hashes, SQLite job queue, authorization gate, character-interval coverage, native-inspection gate, revision invalidation). Those return in a later version once the idea has earned them. Stable document IDs and exact quotes are kept because they cost nothing and make the retrofit easy.

Status: the mechanics are verified against a synthetic module with an oracle extraction (23 of 23 planted defects, no unmatched S2/S3 finding). The first model run (three Opus 5.5 extractors, three independent reviewers) found 23 of 23 after three tool fixes, with 27 unmatched S2/S3 findings, about half of them real unplanted inconsistencies in the fixture; see `runs/syn-pma-sw-01-run1/RESULTS.md`. Re-running the same returns through the retooled recomposition (structured anchors, grouped candidates, reverse SBOM check) keeps 23 of 23, finds all five kept unplanted inconsistencies, and leaves 19 unmatched S2/S3 findings; see the last section of RESULTS.md. Nothing here is a regulatory conclusion or a qualified product.

## Layout

| Path | What it is |
|---|---|
| `standards-axis/` | Reference material from the standards research pass: register with live FDA recognition data, the 31/172/800 bin hierarchy, 25 consistency chains, the independent review of all of it. Never edited by the tools. |
| `profile/activation.json` | The overlay that turns the hierarchy into the v3 profile: which L1 bins are active, importance recalibration, parameter scope (submission vs DHF), merges, added sub-elements, rules, recognition snapshot. |
| `profile/profile.json` | Built profile (`tools/profile.py build`). |
| `ORCHESTRATION.md` | Runbook: roles and isolation, step-by-step commands, merge thresholds, dispatch rules, cost and time, failure handling, run record. |
| `tools/profile.py` | Hierarchy + overlay → profile. |
| `tools/v3.py` | Workspace runtime: `init`, `ingest`, `plan brief|decompose|independent`, `merge-brief`, `merge`, `registry`, `recompose`, `status`. |
| `tools/recompose.py` | Presence per bin, parameter gaps, rules, mechanical chains (CC-01 to 07, 11, 12, 13, 22, 23, 26, 27, 28), anchor agreement, grouped independent-pass diff, HTML/JSON report. |
| `../tests/test_v3.py` | Unit tests for ingest, merge, planning and agreement, plus the golden oracle test (23 of 23, no unmatched S2/S3). |
| `tools/score.py` | Scores a run against a fixture's planted-defect answer key; kept unplanted inconsistencies are scored separately. `tools/compare_oracle.py` compares a run's registry with the oracle's. |
| `prompts/brief.md`, `prompts/decompose.md`, `prompts/independent.md` | Agent prompts; `plan` renders them into self-contained job files. |
| `runs/` | Archived runs: report, scoring, agent returns, document snapshot and a RESULTS.md per run. |
| `fixtures/gen_syn01.py` | Generates the fictional module SYN-PMA-SW-01 (23 documents) and its answer key. `fixtures/oracle_syn01.py` writes a perfect-extractor return for it. |

## Run

```sh
cd /Volumes/aro/projects/book
python3 review/v3/tools/profile.py build                       # profile/profile.json from the overlay
WS=/path/outside/repo/case-01
python3 review/v3/tools/v3.py init $WS
python3 review/v3/tools/v3.py ingest $WS /path/to/package      # pdf via pdfplumber (tables rendered as rows; pypdf fallback);
                                                               # md/txt/csv/json/html as text. Per-page text in docs/Dnn.pages.json
python3 review/v3/tools/v3.py plan $WS brief [--docs D01,D02]  # jobs/J-B-01.md: index + executive summary -> package brief
# dispatch J-B-01 to one agent; it writes brief/J-B-01.json
python3 review/v3/tools/v3.py merge-brief $WS $WS/brief/J-B-01.json   # brief.json (roster, anchors) + returns/J-B-01.jsonl
python3 review/v3/tools/v3.py plan $WS decompose --replicates 2 --max-pages 250
                                                               # one job per document (per page range when longer than
                                                               # --max-pages), per replicate: jobs/J-D-05-a.md, J-D-05-b.md ...
                                                               # each carries the brief, the bins the roster routes to it, and
                                                               # a compact list of the others. jobs/<job>.meta.json has the
                                                               # source path and page range for native-PDF dispatch.
python3 review/v3/tools/v3.py plan $WS independent             # jobs/J-I-nn.md, original-first pass per group of bins
# dispatch: give each jobs/J-D-*.md to an extraction agent (replicates to different agents); it writes returns/<job>.jsonl
#           give each jobs/J-I-nn.md to a separate agent that has not seen any return; it writes independent/J-I-nn.json
python3 review/v3/tools/v3.py merge $WS $WS/returns/J-D-05-a.jsonl  # quotes verified against the stated page; entities
                                                                    # without a quote go to unbinned; coverage records kept
python3 review/v3/tools/v3.py registry $WS                      # merge entities by (type, id); replicate agreement and
                                                               # confidence_level per entity; anchors; coverage per bin
python3 review/v3/tools/v3.py recompose $WS                     # report/report.html, report.json, gaps.json
python3 review/v3/tools/v3.py status $WS                        # pending jobs
python3 review/v3/tools/score.py $WS review/v3/fixtures/syn-pma-sw-01/defects.json   # fixtures only
```

The runtime makes no model calls. The orchestrator (a person, or a Claude session) dispatches the job files and keeps the independent agent away from extraction output. The per-document design assumes a package of roughly 5,000 pages in 20 to 50 documents: each document goes to its own extractor (Sonnet-class is the target), the brief gives every extractor the same anchors and roster, and two replicates per document turn agreement into the confidence signal.

### Confidence and coverage

- `confidence_level` per entity, from the registry: **high** = seen in every replicate for its documents, every parameter value agrees across replicates, every quote verified; **medium** = missed by a replicate or a parameter disagrees; **single** = only one return exists for the document (no replicate ran); **low** = a quote could not be found on any page. Parameter-level agreement is under `agreement.params`.
- `coverage` records: each extractor states, per bin it was given, whether it searched the document and found anything. The report's bin rows carry `searched_docs` and `searched_not_found`; an empty bin whose routed documents were searched is `absent` with `absence_basis: searched`, which is the only honest "missing".
- Quotes carry a page. A quote found on a different page than stated is kept with `flag_page_mismatch` and `page_found`; a quote found nowhere is kept with `flag_quote_not_found` and drags its entity to `low`.

## What the recomposition produces

- **Anchors.** Seventeen shared reference values (proposed version, release build, code-freeze date, SBOM build, labeled version, submission date and so on) resolved by majority across every statement in the package. Each anchor has a declared shape: a scalar (version, build, date, enum), a list (supported platforms, resolved as a union), or an object with named fields (risk file: id, version, date, covers). Fields are compared one by one, so a statement that gives only a date never conflicts with one that gives only a version. Any disagreement on a field is itself a finding.
- **Bins.** Each active L2 sub-element gets a status (absent, unclear, partial, complete), a support score 0–3 from the fill rate of submission-scope parameters, and a priority P1–P3 from importance and the worst finding touching it. DHF-scope parameters are counted but never produce a "missing" finding.
- **Chains.** Mechanical joins across bins with severity S1–S3: requirement → test → passing run at the release build; hazard → control → implementation and effectiveness; SOUP → SBOM → configuration → anomaly review; threat → control → security test → finding disposition; single version identity; anomaly list build and counts; declaration edition versus recognized edition; SBOM versus tested OTS; 13 date-ordering rules; vulnerabilities versus SBOM; report counts versus records; tester independence. Chains the hierarchy defines but v3 does not compute are listed in the report.
- **Independent diff.** What the original-first agents expected and did not find, their parameter concerns and contradictions, and bins where they found evidence that extraction missed. Near-duplicate statements across agents, bins and kinds are grouped into one candidate each (by shared object identifiers or shared wording, compared against the group's representative so groups do not chain). Each group says whether it corroborates a mechanical break or is new.
- **Queues.** Unbinned material and agent notes stay visible.

Each finding carries the entities involved and the exact quotes they came from. A break is an inconsistency in what the sponsor supplied. Candidates need a reviewer.

## Fixture

SYN-PMA-SW-01 is a fictional arrhythmia-classification software module submitted as a modular PMA software module at Enhanced level with IEC 62304 Class C. Its 23 documents are consistent except for 23 planted defects listed in `fixtures/syn-pma-sw-01/defects.json`: a requirement with no test, tests carried forward from a superseded build, a penetration test on an old build by the development team, an SBOM generated before code freeze for a different build, SOUP version drift, a control with no effectiveness evidence, an anomaly list for the wrong build with miscounted entries, a declaration to a non-recognized edition, a summary that overstates the pass rate, a threat model older than a security-relevant change, a vulnerability assessed against a component not in the SBOM, a run before its protocol was approved, and a labeled version that differs from the proposed one. The oracle return in `fixtures/oracle_syn01.py` finds all of them; it is the upper bound against which model extraction is measured.

## Limits

- Light validation only. Quotes are checked for presence, not for meaning. Unknown parameters are kept aside, not rejected.
- Entity identity is the sponsor's ID string. For component types (SOUP, SBOM entries, configuration items) the registry merges identifiers that match exactly or after stripping a version (SOUP-01, libdsp, libdsp 4.1.0, pkg:generic/libdsp@4.1.0); every merge is recorded under `aliases`. Other types are not merged. A conflict between two statements of the same parameter is recorded, not adjudicated.
- Severity, importance and the recognition snapshot are configuration, not verified fact. Re-check the FDA recognition database before any real case.
- No model is qualified by this folder. Recall on the synthetic module measures the tooling and one extraction run, not performance on real submissions.
