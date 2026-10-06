# v3 handoff — where things stand (2026-10-02, after the per-document runtime pass)

State: committed on master (`review/v3: lightweight decompose/recompose ...` and the follow-up commit). Nothing outside `review/v3/` changed except the `_projects/standards` library copy, which lives outside this repo.

## Done
- Standards axis (Opus 5.5): `standards-axis/` register, 31/172/800 hierarchy, 25 chains. Independent review (Fable): `REVIEW-FABLE-2026-10-01.md` + `REVIEW-FABLE-DECISIONS.json`; all decisions applied via `profile/build_activation.py` → `activation.json` → `profile.json` (18 L1, 91 L2, 518 params, 45 DHF-scope, 40 at importance 3).
- Tools: `tools/profile.py`, `tools/v3.py`, `tools/recompose.py` (15 chains), `tools/score.py`, `tools/compare_oracle.py`; prompts in `prompts/`.
- Fixture SYN-PMA-SW-01 (`fixtures/gen_syn01.py`, 23 docs, 23 planted + 5 kept unplanted defects in `defects.json`); oracle `fixtures/oracle_syn01.py`.
- Oracle run (current fixture and tools): 23/23, 0 unmatched S2/S3, UK-04 and UK-05 found mechanically. Model run 1 archived in `runs/syn-pma-sw-01-run1/` (RESULTS.md); its returns re-run through the retooled recomposition: 23/23, 5/5 kept unplanted, 19 unmatched S2/S3, 228 candidate groups from 285 statements (`report-retooled/`).
- Retooling pass (this session): structured anchors (`ANCHOR_SHAPE` in v3.py: scalar / list / object with fields; per-field majority; legacy strings coerced into the one field they can only be), grouped independent candidates with corroboration flags, reverse SBOM→SOUP check in CC-11, component names in CC-03 messages, scorer handles `unplanted_kept` and ignores parameter aggregates and candidates for `expected_no_finding`, three per-row "required" parameters relaxed.

## Per-document runtime (2026-10-02)
Built for the real operating shape (about 5,000 pages in 20 to 50 documents, one Sonnet-class extractor per document, index and executive summary read first):
- `ingest`: per-page text (`docs/Dnn.pages.json`), pdfplumber with tables rendered as rows, pypdf fallback; text documents get heading sections as pseudo-pages. Source path and page count in the index.
- `plan brief` + `merge-brief`: a package brief from the index and executive summary (roster with roles and `feeds_l1`, anchors with quotes, standards claimed). Anchor claims from the brief enter the registry.
- `plan decompose --replicates N --max-pages M`: one job per document, split by page range when long, N replicates (`J-D-05-a`, `J-D-05-b`); bins sliced by the roster, other bins listed compactly; `<job>.meta.json` carries the source path for native-PDF dispatch.
- `merge`: `page` on every record, quote verified against that page then every page (`flag_page_mismatch`, `flag_quote_not_found`); entities without a quote go to unbinned; new `coverage` record type (searched / found per bin per document).
- `registry`: replicate agreement per entity and per parameter, `confidence_level` high / medium / single / low; `coverage` per bin; `replicates` per document.
- `recompose`: bin rows carry `confidence`, `searched_docs`, `searched_not_found`, `absence_basis`; evidence lines carry pages.
- Tests: `review/tests/test_v3.py` (8 tests, including the golden oracle run). Oracle and run 1 findings are byte-identical before and after the change.
- Not done: a native-PDF dispatcher (the orchestrator still hands job files to agents by hand); a Sonnet run; a realistic-scale PDF fixture.

## Next (in order)
0. Run the three run-1 documents' worth of jobs on Sonnet 5.5 with `--replicates 2` and compare entity recall and parameter agreement against the oracle (Opus run 1: 0.96 / 0.96). This is the Sonnet feasibility number the user asked for; it needs the user's go-ahead because it is a model run.
1. Run 2 on the current fixture with the revised prompts (model run; only when asked). Workspace outside the repo; `README.md` "Run". Expect: structured anchors for risk file / threat model / SBOM, fewer SOUP identity fragments, UK-01..05 detected, candidate groups smaller than run 1.
2. From run 2 decide whether extraction noise (CC-04 findings without dispositions, SOUP rows created from SBOM/config rows) needs a prompt change or a routing guard.
3. Second wave of bins: L1-27 usability together with L1-22/24/25 (CC-08, CC-16 need both sides); then L1-02, 06, 07, 08, 18, 19. Each needs fixture documents and planted defects before activation.
4. Before any real case: re-run FDA recognition lookups; the snapshot in `activation.json` is dated 2026-10-01.
5. Later, by the user's call: the integrity machinery v3 deliberately dropped (hashes, job queue, authorization gate, coverage, revision invalidation).

## Run commands
See `README.md` "Run". Workspaces go outside the repo (scratchpad). Model runs only when the user asks.

## Library
`/Volumes/aro/projects/standards` (copy of `_backup/standards` + user additions + `fda/`, `cfr/`, `other/` downloads, manifest `DOWNLOAD-MANIFEST-2026-10-01.json`). Added 2026-10-02: CSA guidance Feb 3 2026 edition, NTIA SBOM Framing 2nd edition. Still absent: IEC TR 60601-4-5 (context only, not recognized, not needed), IEEE 11073-40101, ANSI/NEMA HN 1, CVSS specs (user is sourcing), IEC 60601-1-8. 11073-40102 is present as the ISO/IEEE 2022 adoption. Two DRM PDFs `30416038.pdf`, `30416046.pdf` are FileOpen-protected IEC webstore files (26 and 24 pages), unidentified. The standards register still describes CSA 2026 and NTIA Framing as gaps.
