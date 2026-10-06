# Review v4 — submission review through chat

Version 4.0.0. Prepared 2026-10-06 from the v3 standards hierarchy and its recorded corrections.

The operating package is two self-contained Markdown files:

| File | Use |
|---|---|
| [DECOMPOSE.md](DECOMPOSE.md) | Give this same file to every decomposition chat, with any batch of submission PDFs. It contains the complete catalog and return contract. |
| [RECOMPOSE.md](RECOMPOSE.md) | Main chat: `Mode: COORDINATE` plans batches and tracks handoffs; `Mode: CONSOLIDATE` combines the returned files. Reuse it in a final chat with `Mode: REVIEW`. |

This README is navigation for the repository; it is not a required chat input. The two prompt files embed the complete schema, source register, interpretation rules, and consistency checks they use. Running the workflow requires no scripts, repository access, external retrieval, provider-specific projects, or shared chat memory. The chat interface supplies converted PDF text. Outputs are ordinary text artifacts; a fenced text response is the fallback when downloadable artifacts are unavailable.

## Use

For a main chat that guides the process, upload **RECOMPOSE.md** with the document list/table of contents or executive summary and say **`Mode: COORDINATE`**. It tells you which PDFs and prompt to use in each extraction chat, tracks the returned handoffs/files, and later consolidates them in that same main chat. You can also choose batches yourself and start directly with step 1.

1. Start each extraction chat with **DECOMPOSE.md** and that batch's PDFs. A short batch label such as `B1` is helpful but optional. Use exactly the same prompt for a single PDF or a large mixed batch. Do not select a narrower schema based on filenames.
2. Keep **both** `decomposition-<batch>.jsonl` and `unmapped-<batch>.jsonl`, and read the short **Extraction handoff**. The second file retains unassigned data, uncertain placements, unreadable regions and other exceptions, including an explicit empty-file declaration when none exist.
3. In the main chat, or a new chat with **RECOMPOSE.md**, supply every decomposition and unmapped file and say `Mode: CONSOLIDATE`. You may attach the files separately or paste their contents unchanged. Do not manually reconcile IDs or average batch scores. If an index/file list is available, include it; otherwise package-wide document completeness stays provisional.
4. For the final review, start a fresh chat with **RECOMPOSE.md**, say `Mode: REVIEW`, and provide the complete consolidated evidence **and unmapped** artifacts, their manifests, and all parts. A narrative report alone is insufficient. The session examines expected data, parameters, consistency, and the criteria actually supported by the embedded basis or submission.

Two or three decomposition chats plus consolidation and final review give four or five sessions. Larger batches can need more. The prompts require honest partial returns when input access or output limits prevent full extraction; they never substitute sampling or a summary for the requested records to meet a session target.

### Copyable starter messages

| Chat | Attach | Message |
|---|---|---|
| Main chat | RECOMPOSE.md + document list/summary | `Mode: COORDINATE. Plan two or three PDF batches and guide me through extraction, consolidation and final review.` |
| Each extraction chat | DECOMPOSE.md + assigned PDFs | `Batch: B1. Decompose these PDFs and return both data files and the extraction handoff.` |
| Main chat, after extraction | All decomposition/unmapped files and parts | `Mode: CONSOLIDATE. Reconcile these batches with our document roster and produce the combined evidence and unmapped files.` |
| Final review chat | RECOMPOSE.md + both consolidated files and parts | `Mode: REVIEW. Assess bin completeness, exposed parameters and applicable criteria; report unresolved issues and the information needed to close them.` |

## Two simple bin scores

Completeness scores exist only at bin level. Individual entries and parameters expose values and missingness, without separate completeness scores.

Every bin has **confidence 0–3** and **completeness %** in both decomposition and consolidation. Completeness is **100 × provided expected fields / applicable expected fields**. Show the counts, missing fields, unassessed fields, and any provisional basis beside it. There are no weights, confidence percentages, composite scores, or a 90% completion cutoff. Known missing records contribute their expected fields. Conditions determine which fields belong in the denominator. Optional and internal-record fields remain visible. Batch percentages apply only to that batch; consolidation recalculates from grouped evidence. Findings and criterion outcomes are shown separately.

## Full schema, bounded evidence

Every extractor receives the full catalog: **31 categories, 175 bins and 827 bin parameters**, including areas that v3 left dormant or collapsed. It considers that schema throughout the supplied text, records document coverage, and reports bin scores once per batch. Empty bins describe that batch and its access limitations.

The catalog retains v3 identifiers and field names, incorporates the recorded source corrections, restores the detailed security-control/labeling/management-plan categories, and adds explicit observed-result fields so a later reviewer can examine values rather than only a presence flag. Evidence uses concise summaries, exact parameter values, and short document/page/paragraph references. Full filenames appear once in a register. Missing page information is an explicit exception. New or unfamiliar evidence is retained in a separate unmapped file. The catalog's substantive scope remains the software module and its interfaces; other submission domains receive an explicit routing disposition.

Every bin assignment has a simple placement-confidence score: **3 clear, 2 plausible, 1 tentative**; unmapped data has 0. Bin confidence is the lowest current assignment score, or 0 if empty, with the uncertain record IDs exposed. This describes bin fit only and never weights completeness. One fact may support multiple bins. Consolidation accumulates all records, preserves every duplicate input, groups duplicates only for display/counting, and appends resolutions without deleting earlier evidence. Input-to-output accounting exposes skipped, malformed or unresolved material.

## Extractor handoff

The user receives a data artifact, a separate unmapped artifact, and a short message with six items:

1. **Artifacts and status** — exact filenames/parts, batch and schema IDs, complete or partial extraction.
2. **Documents and coverage** — supplied filenames, identifiable versions, examined scope and table/record accounting where determinable.
3. **Evidence captured and scores** — populated bins, confidence and bin completeness with provided/expected counts.
4. **Exceptions needing attention** — unreadable/misaligned text, conflicting statements, unresolved identities, and referenced material outside this batch.
5. **Follow-up requests** — the specific content needed, its reason, and candidate document names only when supported by a source.
6. **Resume/consolidation instructions** — an exact checkpoint if unfinished, and a copyable handoff block for the next chat.

## Provenance and limits

The embedded basis is a dated adaptation of `review/v3/standards-axis/BIN-HIERARCHY.json`, `STANDARDS-REGISTER.md`, `CONSISTENCY-CHAINS.md`, `REVIEW-FABLE-DECISIONS.json`, and `review/v3/profile/activation.json`. The broader domain screen comes from `review/profiles/DOMAINS.json`. These paths describe preparation provenance; none is a runtime dependency.

V3's standards research is dated 2026-10-01. It includes uneven clause-inspection depth, unresolved recognition questions, and an independent sample audit rather than a complete source audit. V4 preserves those boundaries. It does not claim fresh authority verification, comprehensive device-specific acceptance thresholds, native PDF inspection, or model qualification at 5,000-page scale. A reference not sufficiently established in the embedded basis produces a bounded question or `indeterminate` assessment, not a fabricated requirement or automatic pass.

Local preparation checks concern embedded catalog completeness, references, examples, and consistency between the two files. They do not establish extraction accuracy or regulatory adequacy on real submissions.
