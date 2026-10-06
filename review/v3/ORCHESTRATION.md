# v3 orchestration runbook

How to run one submission package through review/v3 end to end. The runtime (`tools/v3.py`, `tools/recompose.py`) makes no model calls; the orchestrator dispatches job files to agents, merges what comes back, and keeps the independent agents away from extraction output. The orchestrator is a person or a Claude session. Everything below is written so that either can follow it without having seen the code.

Operating shape this runbook assumes: a package of roughly 5,000 pages in 20 to 50 documents, with an index and an executive summary; one Sonnet-class extractor per document, two replicates per document; Opus-class agents for the brief and the independent pass.

## 0. Roles and isolation

| Role | Model | Reads | Writes | Must never see |
|---|---|---|---|---|
| Orchestrator | person or Claude session | everything | nothing by hand inside `returns/`, `brief/`, `independent/` | — |
| Brief agent | Opus 5.5 | `jobs/J-B-01.md` (index, summary, first pages) | `brief/J-B-01.json` | — |
| Extraction agent | Sonnet 5.5 (target); Opus 5.5 for comparison runs | one `jobs/J-D-*.md`, optionally the native PDF named in its `.meta.json` | `returns/<job>.jsonl` | other returns, `registry.json`, `report/` |
| Independent agent | Opus 5.5 | one `jobs/J-I-*.md` and the documents in `docs/` it chooses to open | `independent/<job>.json` | `returns/`, `brief/`, `registry.json`, `report/` |
| Reviewer | person | `report/report.html` | their own notes | — |

Replicates `a` and `b` of the same document go to different agents. In a Claude Code session that means two separate `Agent` calls; over the API it means two separate requests. The same agent must not do both.

An independent agent is dispatched only after extraction is merged, in a fresh context, with the job file and the `docs/` directory and nothing else. The prompt says it has not seen extraction output; the orchestrator makes that true.

## 1. Preconditions

- The repository tests pass: `python3 -B -m unittest discover -s review/tests` from the repo root (96 tests as of 2026-10-02, including the golden oracle run).
- `review/v3/profile/profile.json` exists and is built from the current overlay: `python3 review/v3/tools/profile.py build`.
- The recognition snapshot in `profile/activation.json` is dated. Before a real case, re-run the FDA recognition lookups (register section "recognition lookup log") and update the snapshot date.
- The package is a directory of files. PDF, Markdown, text, CSV, JSON and HTML are read; anything else is indexed as unreadable and must be converted first. Scanned PDFs with no text layer come out as empty pages; run them through the 2.1 runtime's Vision OCR first and ingest the text.
- The workspace is outside the repository (scratchpad or a case directory). Real-case output never goes into git or into logs.

## 2. Steps

Set once:

```sh
cd /Volumes/aro/projects/book
WS=/path/outside/repo/<case-id>
PKG=/path/to/package
```

### 2.1 Ingest

```sh
python3 review/v3/tools/v3.py init $WS
python3 review/v3/tools/v3.py ingest $WS $PKG
```

Check `docs/index.json`:

- `readable: false` on any document: convert or OCR it, delete the workspace `docs/` entry for it, re-run ingest (ingest skips filenames it already knows).
- `pages` that look wrong for the file size (a 300-page PDF with 3 pages) mean pdfplumber failed and pypdf took over, or the PDF is scanned. Look at `docs/Dnn.pages.json` for that document.
- `title` is the first non-empty line; fix nothing, it is only a hint for the brief agent.

Budget: about 150 pages per second of wall time on pdfplumber; a 5,000-page package takes 10 to 15 minutes.

### 2.2 Brief

```sh
python3 review/v3/tools/v3.py plan $WS brief            # auto-detects cover / index / contents / executive summary
python3 review/v3/tools/v3.py plan $WS brief --docs D01,D02   # or name them
```

Dispatch `jobs/J-B-01.md` to one Opus agent. It writes `brief/J-B-01.json`.

```sh
python3 review/v3/tools/v3.py merge-brief $WS $WS/brief/J-B-01.json
```

Check the output and `brief/J-B-01.warnings.txt`:

- `roster: documents without a row`: those documents will be extracted against the full profile. Acceptable for a few; if many, the brief agent did not get usable first pages, so re-dispatch with `--docs` naming the real index.
- `unknown L1`: the agent invented a bin id; the row is kept without it.
- `quote not found`: an anchor claim whose quote is not on the stated page or anywhere; it is kept flagged. More than one or two means the agent paraphrased; re-dispatch.
- A roster row with `feeds_l1: []` and a note is the agent saying it could not tell the role. Leave it; the full profile covers it.

Do not edit `brief.json` by hand to add bins you believe a document feeds. The extractor's catch-all section lets it route to any bin; the roster only decides which bins get full parameter lists.

### 2.3 Plan extraction

```sh
python3 review/v3/tools/v3.py plan $WS decompose --replicates 2 --max-pages 250
```

One job per document per replicate, split into page ranges when a document exceeds `--max-pages`. Each `jobs/<job>.meta.json` gives `doc_id`, `pages`, `source_path`, `is_pdf`, `l1` and `return`.

Choosing `--max-pages`: the job file holds the text of the pages plus the bins slice. Keep a job under about 400k characters of document text so the agent has room to write; 250 pages of dense report text is near that. Lower it for packages with very dense tables.

### 2.4 Dispatch extraction

For each `jobs/J-D-*.md`:

- Give the agent the job file. If `is_pdf` is true and the page range is 600 pages or fewer, also attach the native PDF (pages from `meta.json`) so tables are read from the rendered page rather than from the text rendering. The text rendering stays in the job file as the quote source; quotes are verified against it.
- Replicates `a` and `b` go to different agents.
- Model: Sonnet 5.5 for the extraction tier. Effort medium is the starting point; raise it if the quote-not-found rate in step 2.5 is high.
- The agent writes `returns/<job>.jsonl` and nothing else. If it answers with prose instead of writing the file, save its JSON Lines content to that path yourself and note it in the run record.

Dispatch in batches of whatever the environment allows in parallel; jobs are independent. Over the API, the Batch endpoint halves the cost and suits this stage.

### 2.5 Merge extraction returns

For every return:

```sh
python3 review/v3/tools/v3.py merge $WS $WS/returns/J-D-05-a.jsonl
```

Merge is idempotent: it rewrites `returns/<job>.jsonl` in validated form and `returns/<job>.warnings.txt`. Read the summary line and the warnings. Thresholds, per job:

| Signal | Acceptable | Action above it |
|---|---|---|
| `quotes not found` as a share of entities | under 5% | re-dispatch the job; the agent paraphrased or read a different rendering |
| `flag_page_mismatch` | any number | none; the found page is recorded |
| `moved to unbinned` for entities without a quote | under 2% | re-dispatch |
| `unknown or inactive L2` | a few | none; they stay in unbinned with the original record |
| `coverage` records | one per bin in the job's `l1` slice | missing entirely: re-dispatch; the coverage signal is what makes "absent" mean something |
| `invalid JSON` lines | 0 | fix the line if it is a trailing comma or a stray prose line; otherwise re-dispatch |
| `unknown doc_id` | 0 | the agent used a different id than the job's; fix the id in the file and re-merge |

A re-dispatched job overwrites the previous return on merge. Keep the failed return under `returns/failed/<job>.<n>.jsonl` if it matters for the run record.

### 2.6 Registry

```sh
python3 review/v3/tools/v3.py registry $WS
```

Read the counts:

- `confidence_levels`: with two replicates, expect most entities `high`, a minority `medium`, few `low`. A large `medium` share on one document means the two replicates disagree on identities (the same row extracted under different ids) and that document's two returns should be compared before going on. `low` entities have a quote that could not be found; they stay in the registry flagged.
- `replicated_docs` should equal the number of readable documents when every replicate returned. A document with one replicate missing shows as `single` entities.
- `alias_merges`: component entities merged on identifier or name. The merges are listed under each entity's `aliases`; check them when `conflicting_entities` rises.
- `anchor conflict` lines: each is a finding, not an error. Leave them.

### 2.7 Independent pass

```sh
python3 review/v3/tools/v3.py plan $WS independent --l1-per-job 6
```

Dispatch each `jobs/J-I-*.md` to a fresh Opus agent with access to `docs/` only. The job carries the brief and the roster, so the agent knows where to start; the prompt tells it to open other documents when evidence is not where the roster says. It writes `independent/J-I-nn.json`.

At 5,000 pages an independent agent cannot read everything. It reads the roster-routed documents for its bins and samples the rest. Record which documents each agent opened (`documents_read` in its return) in the run record; it is the coverage statement for this pass.

### 2.8 Recompose

```sh
python3 review/v3/tools/v3.py recompose $WS
python3 review/v3/tools/v3.py status $WS
```

`report/report.html` is the reviewer's document; `report/report.json` and `report/gaps.json` are the data. Before handing it over:

- Anchors table: every conflict is a finding to carry forward.
- Bins table: a bin marked `absent` with `absence_basis: searched` is the only honest "missing from the package". `absent` without that basis means no document was routed to it and no extractor searched it; say so in the handover rather than reporting it as missing.
- Findings: breaks are mechanical inconsistencies in what the sponsor supplied; candidates come from the independent pass and need judgment. Chains listed as not computed were not checked; a bin can read "complete" and still have unchecked chains.
- Entity confidence: a finding whose evidence entities are `medium` or `low` should be re-read in the source before it is written up.

### 2.9 Fixture runs only

```sh
python3 review/v3/tools/score.py $WS review/v3/fixtures/syn-pma-sw-01/defects.json
python3 review/v3/tools/compare_oracle.py $WS review/v3/runs/syn-pma-sw-01-oracle
```

Record recall, unmatched S2/S3 breaks, entity recall and parameter agreement against the oracle. The scorer matches on chain reference and substrings; it is lenient, so a hit is an upper bound and unmatched breaks must be read one by one.

## 3. Run record

Archive under `review/v3/runs/<case-or-fixture>-run<n>/` for fixtures, or in the case directory for real packages (never in git):

- `brief.json`, `jobs/*.meta.json` (not the job bodies for real cases), `returns/`, `independent/`, `registry.json`, `report/`
- `RESULTS.md` with: date; profile version and overlay date; prompt files' git commit; models and effort per role; number of jobs, replicates, re-dispatches and why; the merge threshold table filled in; registry counts; for fixtures the score; what was changed because of the run.
- For fixtures also `docs-snapshot/`, since the generator may change later.

## 4. Cost and time, 5,000 pages, two replicates

| Stage | Tokens in | Model | Cost, standard | Wall time |
|---|---|---|---|---|
| Ingest | — | — | — | 10 to 15 min |
| Brief | ~100k | Opus 5.5 | under $1 | minutes |
| Extraction, 2 replicates | ~6M in, ~0.6M out | Sonnet 5.5 | about $18; about $9 on Batch | limited by parallelism; minutes per job |
| Independent pass, 3 to 4 jobs | ~2M | Opus 5.5 | about $10 | minutes per job |
| Registry, recompose | — | — | — | seconds |

Prices as of 2026-09: Sonnet 5.5 $2 per million input and $10 per million output; Opus 5.5 $4 and $20. Cost is not the constraint; spend it on replicates and re-dispatches.

## 5. Failure handling

- **Agent ran out of room and the return stops mid-file.** The last line is usually broken JSON; merge drops it and keeps the rest. Re-plan that document with a smaller `--max-pages`, re-dispatch only the affected page ranges, and merge. Delete the truncated return first so the registry does not count it as a replicate.
- **Two replicates disagree on identities for a whole table** (same rows, different ids). Neither is wrong by the rules; the registry's alias resolution merges components only. Prefer the replicate that used the sponsor's own identifier column, note the other in the run record, and tighten the id rule in the prompt for the next run rather than editing returns.
- **A document the index promises is not in the package.** The brief agent lists it under `notes`; carry it into the handover as a missing document. Nothing in the registry will show it, because no bin is routed to a document that does not exist.
- **The roster routes a document to the wrong bins.** The extractor's catch-all section lets it emit entities for any bin, with parameters it names itself; merge keeps unknown parameter names under `extra_params`. Expect lower fill rates for that document and re-run it with a corrected roster only when the bin is importance 3.
- **A re-run changes finding ids.** Finding ids are sequential per recomposition. Compare runs by message and evidence, not by id. (Stable finding keys are on the deferred list.)

## 6. What this runbook does not cover

- Qualification of any model. Recall on the synthetic fixture measures the tooling and one run.
- Regulatory conclusions. A break is an inconsistency in what the sponsor supplied; a candidate is a reviewer prompt.
- The integrity machinery v3 deliberately omits: hashes, job queue, authorization gate, character-interval coverage, revision invalidation. Until those return, the run record above is the provenance.
