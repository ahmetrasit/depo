"""v3 lightweight decompose/recompose runtime for a submission package.

No hashes, no job queue, no gates. Plain files in a workspace:

    <ws>/profile.json             built profile (see profile.py)
    <ws>/docs/<Dnn>.txt           extracted text, one file per source document, with <<page N>> markers
    <ws>/docs/<Dnn>.pages.json    per-page text (PDF pages, or heading sections for text documents)
    <ws>/docs/index.json          document index (id, filename, title, pages, chars, source_path)
    <ws>/brief.json               package brief: document roster with roles and bins, anchors from the index/summary
    <ws>/jobs/<job>.md            self-contained prompt for an agent (+ <job>.meta.json: doc, pages, source path)
    <ws>/brief/<job>.json         brief agent return
    <ws>/returns/<job>.jsonl      extraction agent return (entities, anchors, docs, coverage, unbinned, notes)
    <ws>/independent/*.json       original-first pass returns
    <ws>/registry.json            merged entities with agreement across replicates, anchors, documents, coverage
    <ws>/report/                  recomposition output (see recompose.py)

Commands:
    init <ws> --profile review/v3/profile/profile.json
    ingest <ws> <source_dir>                       pdf via pdfplumber (pypdf fallback); md/txt/csv/json/html as text
    plan <ws> brief [--docs D01,D02]               -> jobs/J-B-01.md   (index + executive summary -> package brief)
    merge-brief <ws> <brief.json>                  -> brief.json, returns/J-B-01.jsonl (anchor claims)
    plan <ws> decompose [--max-pages 250] [--replicates 2]
                                                   -> one job per document (per page range when long), per replicate
    plan <ws> independent [--l1-per-job 6]         -> jobs/J-I-nn.md
    merge <ws> <returns.jsonl> [--job J-D-05-a]    quotes verified against the stated page
    registry <ws>                                  merge by (type, id); replicate agreement; anchors; coverage
    recompose <ws>
    status <ws>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

ANCHOR_HELP = {
    "A.proposed_version": "the software version proposed for approval (release/version identification, cover letter, labeling)",
    "A.release_build_id": "the build identifier of the release candidate (build record, version history, test reports)",
    "A.configuration_set": "the configuration item list identifier/version for the release baseline",
    "A.code_freeze_date": "date the release candidate code was frozen (version history, CM record)",
    "A.release_date": "date of software release / release approval",
    "A.test_window": "declared start and end dates of verification testing for the release candidate",
    "A.module_submission_date": "date the software module was submitted (cover letter)",
    "A.labeled_version": "software version stated in labeling / IFU",
    "A.sbom_build": "build or version the SBOM states it describes",
    "A.risk_file_version": "risk management report version/date and the software version it covers",
    "A.threat_model_version": "threat model version/date and the configuration it covers",
    "A.documentation_level": "Basic or Enhanced as claimed",
    "A.supported_platforms": "hardware/OS platforms the device supports",
    "A.device_support_end": "declared end of support / end of life date for the device software",
    "A.prior_authorized_version": "previously authorized version, if any",
    "A.design_control_start_version": "first version under design control (start of version history)",
    "A.recognition_db_snapshot": "not extracted from the package; supplied by the reviewer (standards register)",
}

# Anchor value shapes. Scalars: version | build | date | enum | text. "list": JSON array of strings (never a conflict;
# the resolved value is the union). dict: structured anchor, one key per field with the field's scalar kind; fields are
# compared independently, so a claim that states only the date never conflicts with one that states only the version.
ANCHOR_SHAPE = {
    "A.proposed_version": "version", "A.labeled_version": "version", "A.prior_authorized_version": "version",
    "A.design_control_start_version": "version",
    "A.release_build_id": "build",
    "A.code_freeze_date": "date", "A.release_date": "date", "A.module_submission_date": "date", "A.device_support_end": "date",
    "A.documentation_level": "enum",
    "A.supported_platforms": "list",
    "A.test_window": {"start": "date", "end": "date"},
    "A.sbom_build": {"build": "build", "version": "version", "sbom_document_version": "text"},
    "A.configuration_set": {"id": "text", "version": "text", "build": "build"},
    "A.risk_file_version": {"id": "text", "version": "text", "date": "date", "covers": "version"},
    "A.threat_model_version": {"id": "text", "version": "text", "date": "date", "covers": "version"},
    "A.recognition_db_snapshot": "text",
}
BUILD_RE = re.compile(r"^(build\s*)?[a-z]{0,2}\d{3,6}$", re.I)
VERSION_RE = re.compile(r"^v?\d+(\.\d+){1,3}[a-z0-9.\-]*$", re.I)
DATE_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")
PAGE_MARK = re.compile(r"^<<page (\d+)(?: \| [^>]*)?>>$", re.M)
KEY_DOC_FILE_RE = re.compile(r"cover|index|toc\b|contents|executive|exec[-_ ]?summary|overview|roadmap", re.I)
KEY_DOC_TITLE_RE = re.compile(r"^(cover|index|table of contents|contents|executive summary|submission overview|submission roadmap)", re.I)
REP_RE = re.compile(r"^(.*)-([a-z])$")


def anchor_shape_text(name: str) -> str:
    sh = ANCHOR_SHAPE.get(name, "text")
    if isinstance(sh, dict):
        return "object {" + ", ".join(f"{k}: {v}" for k, v in sh.items()) + "}"
    return "list of strings" if sh == "list" else sh


def norm_anchor_scalar(kind: str, v) -> str:
    if v is None:
        return ""
    s = re.sub(r"\s+", " ", str(v)).strip()
    if kind == "version":
        s = re.sub(r"^(v|version|ver\.?|rev\.?|revision)\s*", "", s, flags=re.I)
        return re.sub(r"[\s()]+", "", s).lower()
    if kind == "build":
        return re.sub(r"^(build\s*)", "", s, flags=re.I).lower()
    if kind == "date":
        m = re.match(r"(\d{4})-(\d{2})(?:-(\d{2}))?", s)
        return f"{m.group(1)}-{m.group(2)}-{m.group(3) or '01'}" if m else s.lower()
    return s.lower()


def coerce_anchor_value(name: str, v):
    """Bring a claim's value into the anchor's shape. Returns (value, warning or None)."""
    sh = ANCHOR_SHAPE.get(name, "text")
    if isinstance(sh, dict):
        if isinstance(v, dict):
            unknown = [k for k in v if k not in sh]
            return {k: v[k] for k in v if k in sh}, (f"anchor {name}: fields {unknown} not in shape, dropped" if unknown else None)
        s = str(v or "").strip()
        # a bare string on a structured anchor: place it in the one field it can only be
        if "build" in sh and BUILD_RE.match(s):
            return {"build": s}, None
        if "version" in sh and VERSION_RE.match(s) and not ("covers" in sh):
            return {"version": s}, None
        if "covers" in sh and VERSION_RE.match(s):
            return {"covers": s}, None
        if "date" in sh and DATE_RE.match(s):
            return {"date": s}, None
        if "start" in sh:
            m = re.findall(r"\d{4}-\d{2}-\d{2}", s)
            if len(m) == 2:
                return {"start": m[0], "end": m[1]}, None
        return {"_text": s}, f"anchor {name}: unstructured value kept as text, excluded from field comparison: {s[:60]!r}"
    if sh == "list":
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()], None
        parts = [x.strip() for x in re.split(r"[;\n]", str(v or "")) if x.strip()]
        return parts, None
    if isinstance(v, (dict, list)):
        return json.dumps(v, ensure_ascii=False), f"anchor {name}: expected a {sh} string, got {type(v).__name__}; serialized"
    return v, None


def resolve_anchor(name: str, claims: list) -> dict:
    """Majority per field; any disagreement is a conflict. Claims carry coerced values."""
    sh = ANCHOR_SHAPE.get(name, "text")
    if not claims:
        return {"shape": anchor_shape_text(name), "value": None, "claims": [], "conflict": False, "alternatives": []}
    if sh == "list":
        seen, union = set(), []
        for c in claims:
            for x in c["value"]:
                if norm_ws(x).lower() not in seen:
                    seen.add(norm_ws(x).lower()); union.append(x)
        return {"shape": anchor_shape_text(name), "value": union, "claims": claims, "conflict": False, "alternatives": [],
                "note": "list anchor: union of all statements; partial mentions are not conflicts"}
    if isinstance(sh, dict):
        value, alts, fields_conf = {}, [], {}
        for field, kind in sh.items():
            groups = defaultdict(list)
            for c in claims:
                if isinstance(c["value"], dict) and c["value"].get(field) not in (None, ""):
                    groups[norm_anchor_scalar(kind, c["value"][field])].append(c)
            if not groups:
                continue
            best = max(groups.values(), key=len)
            value[field] = best[0]["value"][field]
            if len(groups) > 1:
                fields_conf[field] = [g[0]["value"][field] for g in groups.values() if g is not best]
                alts.extend(f"{field}={a!r}" for a in fields_conf[field])
        unstructured = [c for c in claims if isinstance(c["value"], dict) and "_text" in c["value"]]
        return {"shape": anchor_shape_text(name), "value": value or None, "claims": claims, "conflict": bool(fields_conf),
                "alternatives": alts, "conflict_fields": fields_conf, "unstructured_claims": len(unstructured)}
    groups = defaultdict(list)
    for c in claims:
        groups[norm_anchor_scalar(sh, c["value"])].append(c)
    best = max(groups.values(), key=len)
    return {"shape": anchor_shape_text(name), "value": best[0]["value"], "claims": claims, "conflict": len(groups) > 1,
            "alternatives": [g[0]["value"] for g in groups.values() if g is not best]}


RECORD_TYPES = {"entity", "anchor", "doc", "unbinned", "note", "coverage"}


def read_json(p: Path):
    return json.loads(Path(p).read_text())


def write_json(p: Path, obj):
    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()


def split_job(job: str) -> tuple[str, str | None]:
    """'J-D-05-a' -> ('J-D-05', 'a'); 'J-D-05' -> ('J-D-05', None). The suffix letter is the replicate."""
    m = REP_RE.match(job or "")
    return (m.group(1), m.group(2)) if m else (job, None)


# ----------------------------------------------------------------------------- init / ingest

def init(ws: Path, profile: Path):
    ws.mkdir(parents=True, exist_ok=True)
    for d in ("docs", "jobs", "returns", "independent", "brief", "report"):
        (ws / d).mkdir(exist_ok=True)
    prof = read_json(profile)
    write_json(ws / "profile.json", prof)
    print(f"initialized {ws} with profile {profile} ({prof['counts']['l1']} L1, {prof['counts']['l2']} L2)")


def render_table(rows) -> str:
    out = []
    for r in rows or []:
        cells = [norm_ws(str(c)) if c is not None else "" for c in r]
        if any(cells):
            out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def pdf_pages(path: Path) -> tuple[list[dict], str]:
    """Per-page text. pdfplumber keeps reading order and renders detected tables as pipe rows after the page text;
    pypdf is the fallback. An unreadable page is kept as a page with a note so page numbers stay aligned."""
    try:
        import pdfplumber
        pages = []
        with pdfplumber.open(str(path)) as pdf:
            for i, pg in enumerate(pdf.pages):
                try:
                    text = pg.extract_text() or ""
                    tables = [render_table(t) for t in (pg.extract_tables() or [])]
                    tables = [t for t in tables if t]
                    if tables:
                        text += "\n\n[tables detected on this page, rendered as rows]\n" + "\n\n".join(tables)
                except Exception as e:  # noqa: BLE001
                    text = f"[page {i+1} UNREADABLE: {e}]"
                pages.append({"page": i + 1, "label": f"p{i+1}", "text": text})
        return pages, "pdfplumber"
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001
        print(f"  pdfplumber failed on {path.name}: {e}; trying pypdf")
    try:
        from pypdf import PdfReader
        r = PdfReader(str(path), strict=False)
        pages = []
        for i, pg in enumerate(r.pages):
            try:
                pages.append({"page": i + 1, "label": f"p{i+1}", "text": pg.extract_text() or ""})
            except Exception as e:  # noqa: BLE001
                pages.append({"page": i + 1, "label": f"p{i+1}", "text": f"[page {i+1} UNREADABLE: {e}]"})
        return pages, "pypdf"
    except Exception as e:  # noqa: BLE001
        return [], f"pdf extraction failed: {e}"


def text_pages(text: str, target: int = 6000) -> list[dict]:
    """Pseudo-pages for text documents: one per level-2 heading section; a section longer than `target` characters is
    split at paragraph boundaries. Page numbers are sequential; labels carry the heading."""
    lines = text.splitlines(keepends=True)
    sections, cur, label = [], [], "start"
    for ln in lines:
        if ln.startswith("## "):
            if "".join(cur).strip():
                sections.append((label, "".join(cur)))
            cur, label = [ln], ln[3:].strip()[:60]
        else:
            cur.append(ln)
    if "".join(cur).strip() or not sections:
        sections.append((label, "".join(cur)))
    pages = []
    for label, body in sections:
        if len(body) <= target:
            pages.append({"page": len(pages) + 1, "label": label, "text": body})
            continue
        buf, k = "", 1
        for para in re.split(r"(?<=\n\n)", body):
            if buf and len(buf) + len(para) > target:
                pages.append({"page": len(pages) + 1, "label": f"{label} ({k})", "text": buf}); buf, k = "", k + 1
            buf += para
        if buf.strip():
            pages.append({"page": len(pages) + 1, "label": f"{label} ({k})", "text": buf})
    return pages


def pages_to_text(pages: list[dict]) -> str:
    return "".join(f"\n<<page {p['page']} | {p['label']}>>\n{p['text']}" for p in pages)


def load_pages(ws: Path, doc_id: str) -> list[dict]:
    pj = ws / "docs" / f"{doc_id}.pages.json"
    if pj.exists():
        return read_json(pj)
    txt = (ws / "docs" / f"{doc_id}.txt").read_text()
    marks = list(PAGE_MARK.finditer(txt))
    if not marks:
        return [{"page": 1, "label": "p1", "text": txt}]
    pages = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(txt)
        pages.append({"page": int(m.group(1)), "label": f"p{m.group(1)}", "text": txt[m.end():end]})
    return pages


def ingest(ws: Path, source: Path):
    index_path = ws / "docs" / "index.json"
    index = read_json(index_path) if index_path.exists() else []
    known = {d["filename"] for d in index}
    files = sorted(p for p in source.rglob("*") if p.is_file() and not p.name.startswith("."))
    for f in files:
        rel = str(f.relative_to(source))
        if rel in known:
            continue
        ext = f.suffix.lower()
        method = "text"
        if ext == ".pdf":
            pages, method = pdf_pages(f)
        elif ext in {".md", ".txt", ".csv", ".tsv", ".json", ".xml", ".html", ".htm"}:
            pages = text_pages(f.read_text(errors="replace"))
        else:
            pages, method = [], f"unsupported extension {ext}"
        text = pages_to_text(pages)
        doc_id = f"D{len(index)+1:02d}"
        title = ""
        for p in pages:
            for line in p["text"].splitlines():
                if line.strip() and not line.startswith("[page"):
                    title = line.strip().lstrip("# ").strip()[:120]
                    break
            if title:
                break
        (ws / "docs" / f"{doc_id}.txt").write_text(text)
        write_json(ws / "docs" / f"{doc_id}.pages.json", pages)
        readable = bool(norm_ws(text)) and not all(p["text"].startswith("[page") for p in pages)
        index.append({"doc_id": doc_id, "filename": rel, "title": title, "chars": len(text), "pages": len(pages), "method": method,
                      "readable": readable, "is_pdf": ext == ".pdf", "source_path": str(f.resolve())})
    write_json(index_path, index)
    unreadable = [d for d in index if not d["readable"]]
    print(f"{len(index)} documents indexed ({sum(d['pages'] for d in index)} pages); {len(unreadable)} unreadable: {[d['filename'] for d in unreadable]}")


# ----------------------------------------------------------------------------- plan

def profile_slice(prof: dict, l1_ids=None, with_params=True) -> str:
    out = []
    for b in prof["bins"]:
        if l1_ids is not None and b["id"] not in l1_ids:
            continue
        out.append(f"\n### {b['id']} {b['title']}")
        out.append(f"Applies: {b.get('applicability','')}")
        for x in b["l2"]:
            out.append(f"- **{x['id']}** {x['title']} (importance {x['importance']}; entities: {', '.join(x['entity_types'])})")
            out.append(f"  Expect: {x['expectation']}")
            if with_params:
                sub = [f"{p['name']}:{p['type']}" for p in x["parameters"] if p["scope"] == "submission"]
                dhf = [f"{p['name']}:{p['type']}" for p in x["parameters"] if p["scope"] != "submission"]
                out.append(f"  Parameters (capture when stated): {', '.join(sub)}")
                if dhf:
                    out.append(f"  Optional, usually in the DHF not the submission: {', '.join(dhf)}")
    return "\n".join(out)


def profile_compact(prof: dict, l1_ids) -> str:
    """One line per L1 with its L2 ids and titles: enough to route a stray item, not enough to extract against."""
    out = []
    for b in prof["bins"]:
        if b["id"] in l1_ids:
            out.append(f"- {b['id']} {b['title']}: " + "; ".join(f"{x['id']} {x['title']}" for x in b["l2"]))
    return "\n".join(out)


def render(template: str, **kw) -> str:
    for k, v in kw.items():
        template = template.replace("{{" + k + "}}", v)
    return template


def anchors_text(prof: dict) -> str:
    return "\n".join(f"- `{a}` — value: {anchor_shape_text(a)} — {ANCHOR_HELP.get(a,'')}" for a in prof["anchors"])


def brief_text(brief: dict | None, doc_id: str | None = None) -> str:
    """The package brief as the per-document agents see it: anchors from the index/summary and the roster row."""
    if not brief:
        return "(no package brief available; routing by the full profile)"
    out = ["Anchors stated by the index / executive summary (verify against this document; disagreements are findings):"]
    for a in brief.get("anchors", []):
        v = a.get("value")
        out.append(f"- {a['name']} = {json.dumps(v, ensure_ascii=False)} ({a.get('doc_id','')}{', p'+str(a['page']) if a.get('page') else ''})")
    if brief.get("standards_claimed"):
        out.append("Standards the summary claims conformity to: " + "; ".join(map(str, brief["standards_claimed"])))
    rows = [r for r in brief.get("roster", []) if doc_id is None or r.get("doc_id") == doc_id]
    if rows:
        out.append("Document roster" + (" entry for this document" if doc_id else "") + ":")
        for r in rows:
            out.append(f"- {r['doc_id']}: role {r.get('role','?')}; feeds {', '.join(r.get('feeds_l1', [])) or '?'}"
                       + (f"; covers {r['covers_version']}" if r.get("covers_version") else "")
                       + (f"; note: {r['note']}" if r.get("note") else ""))
    return "\n".join(out)


def plan_brief(ws: Path, prof: dict, index: list, docs: str | None):
    tmpl = (HERE.parent / "prompts" / "brief.md").read_text()
    if docs:
        key = [d for d in index if d["doc_id"] in {x.strip() for x in docs.split(",")}]
    else:
        key = [d for d in index if d["readable"] and (KEY_DOC_FILE_RE.search(Path(d["filename"]).stem) or KEY_DOC_TITLE_RE.search(d["title"]))]
        if not key:
            key = [d for d in index if d["readable"]][:2]
    jid = "J-B-01"
    key_txt = "\n\n".join(f"=============== DOCUMENT {d['doc_id']} | {d['filename']} | {d['title']}\n" + (ws/'docs'/f"{d['doc_id']}.txt").read_text() for d in key)
    previews = []
    for d in index:
        first = load_pages(ws, d["doc_id"])[0]["text"] if d["readable"] else ""
        previews.append(f"--- {d['doc_id']} | {d['filename']} | {d['title']} | {d['pages']} pages, {d['chars']} chars{'' if d['readable'] else ' | UNREADABLE'}\n{norm_ws(first)[:1200]}")
    l1s = "\n".join(f"- {b['id']} {b['title']} — applies: {b.get('applicability','')}" for b in prof["bins"])
    body = render(tmpl, JOB_ID=jid, RETURN_PATH=str(ws / "brief" / f"{jid}.json"), L1_LIST=l1s, ANCHORS=anchors_text(prof),
                  KEY_DOC_IDS=", ".join(d["doc_id"] for d in key), KEY_DOCUMENTS=key_txt, DOC_PREVIEWS="\n\n".join(previews))
    (ws / "jobs" / f"{jid}.md").write_text(body)
    write_json(ws / "jobs" / f"{jid}.meta.json", {"job": jid, "role": "brief", "key_docs": [d["doc_id"] for d in key], "return": str(ws / "brief" / f"{jid}.json")})
    print(f"{jid}: key documents {[d['doc_id'] for d in key]} -> {ws/'jobs'/(jid+'.md')}")


def plan_decompose(ws: Path, prof: dict, index: list, max_pages: int, replicates: int):
    tmpl = (HERE.parent / "prompts" / "decompose.md").read_text()
    brief = read_json(ws / "brief.json") if (ws / "brief.json").exists() else None
    roster = {r["doc_id"]: r for r in (brief or {}).get("roster", [])}
    all_l1 = [b["id"] for b in prof["bins"]]
    reps = [chr(ord("a") + i) for i in range(replicates)] if replicates > 1 else [None]
    made = []
    for d in index:
        if not d["readable"]:
            continue
        pages = load_pages(ws, d["doc_id"])
        l1s = [x for x in (roster.get(d["doc_id"], {}).get("feeds_l1") or []) if x in all_l1] or all_l1
        chunks = [pages[i:i + max_pages] for i in range(0, len(pages), max_pages)] or [[]]
        for ci, chunk in enumerate(chunks, 1):
            base = f"J-D-{d['doc_id'][1:]}" + (f"p{ci}" if len(chunks) > 1 else "")
            doc_txt = (f"=============== DOCUMENT {d['doc_id']} | {d['filename']} | {d['title']} | pages {chunk[0]['page']}–{chunk[-1]['page']} of {len(pages)}\n"
                       + pages_to_text(chunk)) if chunk else f"=============== DOCUMENT {d['doc_id']} (empty)"
            for rep in reps:
                jid = base + (f"-{rep}" if rep else "")
                body = render(tmpl, JOB_ID=jid, RETURN_PATH=str(ws / "returns" / f"{jid}.jsonl"), DOC_ID=d["doc_id"],
                              ENTITY_TYPES=", ".join(prof["entity_types"]), ANCHORS=anchors_text(prof),
                              BRIEF=brief_text(brief, d["doc_id"]), BINS=profile_slice(prof, l1s),
                              OTHER_BINS=profile_compact(prof, [x for x in all_l1 if x not in l1s]) or "(none)",
                              DOCUMENT=doc_txt)
                (ws / "jobs" / f"{jid}.md").write_text(body)
                write_json(ws / "jobs" / f"{jid}.meta.json", {"job": jid, "role": "decompose", "doc_id": d["doc_id"], "replicate": rep,
                                                             "pages": [chunk[0]["page"], chunk[-1]["page"]] if chunk else [0, 0],
                                                             "total_pages": len(pages), "source_path": d.get("source_path"), "is_pdf": d.get("is_pdf", False),
                                                             "l1": l1s, "chars": sum(len(p["text"]) for p in chunk), "return": str(ws / "returns" / f"{jid}.jsonl")})
                made.append((jid, d["doc_id"], len(chunk), l1s))
    for jid, did, n, l1s in made:
        print(f"{jid}: {did} {n} pages, bins {l1s if len(l1s) < len(all_l1) else 'all'}")
    print(f"{len(made)} decompose job(s) written to {ws/'jobs'}" + ("" if brief else " (no brief.json: every job carries the full profile)"))


def plan_independent(ws: Path, prof: dict, index: list, l1_per_job: int):
    tmpl = (HERE.parent / "prompts" / "independent.md").read_text()
    brief = read_json(ws / "brief.json") if (ws / "brief.json").exists() else None
    roster = {r["doc_id"]: r for r in (brief or {}).get("roster", [])}
    existing = sorted((ws / "jobs").glob("J-I-*.md"))
    n = len(existing)
    l1s = [b["id"] for b in prof["bins"]]
    for i in range(0, len(l1s), l1_per_job):
        n += 1
        jid = f"J-I-{n:02d}"
        sel = l1s[i:i + l1_per_job]
        idx = "\n".join(f"- {d['doc_id']} | {d['filename']} | {d['title']} | {d['pages']} pages | role: {roster.get(d['doc_id'], {}).get('role', '?')} | feeds: {', '.join(roster.get(d['doc_id'], {}).get('feeds_l1', [])) or '?'} | {ws/'docs'/(d['doc_id']+'.txt')}" for d in index)
        body = render(tmpl, JOB_ID=jid, RETURN_PATH=str(ws / "independent" / f"{jid}.json"), BRIEF=brief_text(brief),
                      PROFILE=profile_slice(prof, sel, with_params=False), DOC_INDEX=idx, L1_IDS=", ".join(sel))
        (ws / "jobs" / f"{jid}.md").write_text(body)
        write_json(ws / "jobs" / f"{jid}.meta.json", {"job": jid, "role": "independent", "l1": sel, "return": str(ws / "independent" / f"{jid}.json")})
        print(f"{jid}: {sel}")


def plan(ws: Path, role: str, max_pages: int = 250, replicates: int = 1, l1_per_job: int = 6, docs: str | None = None):
    prof = read_json(ws / "profile.json")
    index = read_json(ws / "docs" / "index.json")
    if role == "brief":
        plan_brief(ws, prof, index, docs)
    elif role == "decompose":
        plan_decompose(ws, prof, index, max_pages, replicates)
    else:
        plan_independent(ws, prof, index, l1_per_job)


# ----------------------------------------------------------------------------- merge

def verify_quote(r: dict, pages: list[dict], pages_norm: list[str]) -> str | None:
    """Check the record's quote against its stated page, then every page. Sets flags; returns a warning or None."""
    q = r.get("quote")
    if not q:
        return None
    qn = norm_ws(q)
    page = r.get("page")
    by_page = {p["page"]: i for i, p in enumerate(pages)}
    if isinstance(page, int) and page in by_page and qn in pages_norm[by_page[page]]:
        r["quote_ok"] = True
        return None
    hits = [p["page"] for p, t in zip(pages, pages_norm) if qn in t]
    if hits:
        r["quote_ok"] = True
        r["page_found"] = hits[0]
        if isinstance(page, int) and page != hits[0]:
            r["flag_page_mismatch"] = True
            return f"quote stated on page {page} but found on page {hits[0]}: {q[:50]!r}"
        return None
    r["quote_ok"] = False
    r["flag_quote_not_found"] = True
    return f"quote not found verbatim in {r.get('doc_id')}: {q[:60]!r}"


def merge_records(ws: Path, records: list, job: str, source_lines=None) -> tuple[list, list]:
    prof = read_json(ws / "profile.json")
    l2map = {x["id"]: x for b in prof["bins"] for x in b["l2"]}
    l1ids = {b["id"] for b in prof["bins"]}
    index = read_json(ws / "docs" / "index.json")
    pages = {d["doc_id"]: load_pages(ws, d["doc_id"]) for d in index}
    pages_norm = {k: [norm_ws(p["text"]) for p in v] for k, v in pages.items()}
    base, rep = split_job(job)
    kept, warnings = [], []
    for ln, r in enumerate(records, 1):
        t = r.get("type")
        if t not in RECORD_TYPES:
            warnings.append(f"line {ln}: unknown type {t!r}; dropped"); continue
        did = r.get("doc_id")
        if did not in pages:
            warnings.append(f"line {ln}: unknown doc_id {did!r}; kept with flag"); r["flag_unknown_doc"] = True
        else:
            w = verify_quote(r, pages[did], pages_norm[did])
            if w:
                warnings.append(f"line {ln}: {w}")
        if t == "entity":
            l2 = r.get("l2")
            if not r.get("quote"):
                warnings.append(f"line {ln}: entity {r.get('entity_type')} {r.get('id')} has no quote; moved to unbinned")
                r = {"type": "unbinned", "doc_id": did, "page": r.get("page"), "quote": "", "reason": f"entity without quote: {r.get('entity_type')} {r.get('id')} in {l2}", "original": r}
            elif l2 not in l2map:
                warnings.append(f"line {ln}: unknown or inactive L2 {l2!r}; moved to unbinned")
                r = {"type": "unbinned", "doc_id": did, "page": r.get("page"), "quote": r.get("quote") or "", "reason": f"agent routed to unknown L2 {l2}: {r.get('entity_type')} {r.get('id')}", "original": r}
            else:
                known = {p["name"] for p in l2map[l2]["parameters"]}
                extra = {k: v for k, v in (r.get("params") or {}).items() if k not in known}
                if extra:
                    r["extra_params"] = extra
                    r["params"] = {k: v for k, v in r["params"].items() if k in known}
                if r.get("entity_type") not in prof["entity_types"]:
                    warnings.append(f"line {ln}: entity_type {r.get('entity_type')!r} not in profile; kept")
                if not r.get("id"):
                    warnings.append(f"line {ln}: entity without id; kept as anonymous"); r["id"] = f"ANON-{job}-{ln}"
        elif t == "anchor":
            if r.get("name") not in prof["anchors"]:
                warnings.append(f"line {ln}: unknown anchor {r.get('name')!r}; kept with flag"); r["flag_unknown_anchor"] = True
            else:
                r["value_as_stated"] = r.get("value")
                r["value"], w = coerce_anchor_value(r["name"], r.get("value"))
                if w:
                    warnings.append(f"line {ln}: {w}")
        elif t == "doc":
            bad = [x for x in (r.get("l1") or []) if x not in l1ids]
            if bad:
                warnings.append(f"line {ln}: doc record cites inactive L1 {bad}")
        elif t == "coverage":
            if r.get("l2") not in l2map:
                warnings.append(f"line {ln}: coverage record for unknown L2 {r.get('l2')!r}; dropped"); continue
            r["found"] = bool(r.get("found"))
        r["job"], r["job_base"], r["rep"] = job, base, rep
        kept.append(r)
    return kept, warnings


def merge(ws: Path, path: Path, job: str | None = None):
    job = job or path.stem
    records, warnings = [], []
    for ln, line in enumerate(path.read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as e:
            warnings.append(f"line {ln}: invalid JSON ({e}); dropped")
    kept, w2 = merge_records(ws, records, job)
    warnings += w2
    out = ws / "returns" / f"{job}.jsonl"
    with out.open("w") as f:
        for r in kept:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    counts = Counter(r["type"] for r in kept)
    qnf = sum(1 for r in kept if r.get("flag_quote_not_found"))
    print(f"merged {job}: {dict(counts)}; quotes not found: {qnf} -> {out}")
    for w in warnings[:40]:
        print("  warn:", w)
    if len(warnings) > 40:
        print(f"  ... {len(warnings)-40} more warnings")
    (ws / "returns" / f"{job}.warnings.txt").write_text("\n".join(warnings))


def merge_brief(ws: Path, path: Path):
    prof = read_json(ws / "profile.json")
    index = {d["doc_id"] for d in read_json(ws / "docs" / "index.json")}
    l1ids = {b["id"] for b in prof["bins"]}
    data = read_json(path)
    warnings = []
    roster = []
    for r in data.get("roster", []):
        if r.get("doc_id") not in index:
            warnings.append(f"roster: unknown doc_id {r.get('doc_id')!r}; dropped"); continue
        bad = [x for x in (r.get("feeds_l1") or []) if x not in l1ids]
        if bad:
            warnings.append(f"roster {r['doc_id']}: unknown L1 {bad}; removed")
        r["feeds_l1"] = [x for x in (r.get("feeds_l1") or []) if x in l1ids]
        roster.append(r)
    missing = sorted(index - {r["doc_id"] for r in roster})
    if missing:
        warnings.append(f"roster: documents without a row (will get the full profile): {missing}")
    anchor_records = [{"type": "anchor", "name": a.get("name"), "value": a.get("value"), "doc_id": a.get("doc_id"), "page": a.get("page"),
                       "quote": a.get("quote", ""), "confidence": a.get("confidence", 2)} for a in data.get("anchors", [])]
    kept, w2 = merge_records(ws, anchor_records, "J-B-01")
    warnings += w2
    brief = {"job_id": data.get("job_id", "J-B-01"), "roster": roster, "anchors": [{k: a.get(k) for k in ("name", "value", "doc_id", "page", "quote")} for a in kept if not a.get("flag_unknown_anchor")],
             "standards_claimed": data.get("standards_claimed", []), "package_summary": data.get("package_summary", ""), "notes": data.get("notes", [])}
    write_json(ws / "brief.json", brief)
    with (ws / "returns" / "J-B-01.jsonl").open("w") as f:
        for r in kept:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"brief: {len(roster)} roster rows, {len(kept)} anchor claims -> {ws/'brief.json'}")
    for w in warnings[:40]:
        print("  warn:", w)
    (ws / "brief" / "J-B-01.warnings.txt").write_text("\n".join(warnings))


# ----------------------------------------------------------------------------- registry

def pnorm(v) -> str:
    """Normalized parameter value for agreement: whitespace-collapsed, case-folded JSON."""
    if isinstance(v, str):
        return norm_ws(v).lower()
    if isinstance(v, list):
        return json.dumps(sorted(pnorm(x) for x in v))
    return json.dumps(v, sort_keys=True).lower()


def registry(ws: Path):
    prof = read_json(ws / "profile.json")
    records = []
    for f in sorted((ws / "returns").glob("*.jsonl")):
        records += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    # replicates per document: distinct replicate letters among the jobs that returned anything for that document
    reps_by_doc = defaultdict(set)
    for r in records:
        if r.get("doc_id") and r.get("type") != "coverage":
            reps_by_doc[r["doc_id"]].add(r.get("rep") or "-")
    ents, docs, anchors, unbinned, notes = {}, {}, defaultdict(list), [], []
    coverage = defaultdict(lambda: defaultdict(lambda: {"searched": 0, "found": 0}))
    for r in records:
        t = r["type"]
        if t == "entity":
            key = f"{r.get('entity_type')}:{r['id']}"
            e = ents.setdefault(key, {"key": key, "entity_type": r.get("entity_type"), "id": r["id"], "l2": [], "params": {},
                                      "param_sources": defaultdict(list), "docs": [], "quotes": [], "conflicts": [],
                                      "status": set(), "confidence": [], "_seen": set(), "_quote_bad": 0})
            if r.get("l2") not in e["l2"]:
                e["l2"].append(r["l2"])
            if r.get("doc_id") not in e["docs"]:
                e["docs"].append(r.get("doc_id"))
            e["_seen"].add((r.get("doc_id"), r.get("rep") or "-"))
            if r.get("flag_quote_not_found"):
                e["_quote_bad"] += 1
            if r.get("quote"):
                e["quotes"].append({"doc_id": r.get("doc_id"), "page": r.get("page_found", r.get("page")), "quote": r["quote"], "l2": r.get("l2"), "job": r.get("job")})
            if r.get("status"):
                e["status"].add(r["status"])
            if isinstance(r.get("confidence"), int):
                e["confidence"].append(r["confidence"])
            for k, v in (r.get("params") or {}).items():
                if v in (None, "", [], {}):
                    continue
                e["param_sources"][k].append({"doc_id": r.get("doc_id"), "page": r.get("page_found", r.get("page")), "job": r.get("job"), "rep": r.get("rep") or "-",
                                              "value": v, "quote": (r.get("quote") or "")[:200], "quote_ok": r.get("quote_ok", True)})
                if k in e["params"] and json.dumps(e["params"][k], sort_keys=True) != json.dumps(v, sort_keys=True):
                    if isinstance(v, list) and isinstance(e["params"][k], list):
                        e["params"][k] = list(e["params"][k]) + [i for i in v if i not in e["params"][k]]
                    elif pnorm(v) != pnorm(e["params"][k]):
                        e["conflicts"].append({"param": k, "values": [e["params"][k], v], "doc_id": r.get("doc_id"), "job": r.get("job")})
                else:
                    e["params"][k] = v
        elif t == "doc":
            d = docs.setdefault(r["doc_id"], {"doc_id": r["doc_id"], "l1": [], "params": {}, "quotes": [], "jobs": []})
            for x in r.get("l1") or []:
                if x not in d["l1"]:
                    d["l1"].append(x)
            d["params"].update({k: v for k, v in (r.get("params") or {}).items() if v not in (None, "", [])})
            if r.get("quote"):
                d["quotes"].append(r["quote"])
            if r.get("job") and r["job"] not in d["jobs"]:
                d["jobs"].append(r["job"])
        elif t == "anchor":
            anchors[r.get("name")].append({"value": r.get("value"), "doc_id": r.get("doc_id"), "page": r.get("page_found", r.get("page")), "quote": r.get("quote", ""),
                                           "job": r.get("job"), "rep": r.get("rep") or "-", "quote_ok": r.get("quote_ok", True)})
        elif t == "unbinned":
            unbinned.append(r)
        elif t == "note":
            notes.append(r)
        elif t == "coverage":
            c = coverage[r["l2"]][r["doc_id"]]
            c["searched"] += 1
            c["found"] += 1 if r.get("found") else 0
    # alias resolution (deterministic, exact-match only, recorded): two entities of the same type are the same object when
    # one's id equals the other's identifier parameter (soup_id, configuration_item_id, unique_identifier, component_name, title),
    # or their names are equal after stripping a trailing version token. Component-like types only.
    ALIAS_TYPES = {"soup_component", "sbom_entry", "design_component"}
    ID_PARAMS = ("soup_id", "configuration_item_id", "unique_identifier", "component_name", "title", "name")
    def strip_version(x):
        x = re.sub(r"\s*\(.*?\)\s*", " ", str(x or ""))
        x = re.sub(r"\s+v?\d[\w.\-+]*(\s+lts)?$", "", x.strip(), flags=re.I)
        return re.sub(r"[^a-z0-9]", "", x.lower())
    parent = {}
    def find(k):
        while parent.get(k, k) != k:
            k = parent[k]
        return k
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    pool = [e for e in ents.values() if e["entity_type"] in ALIAS_TYPES]
    by_name = defaultdict(list)
    for e in pool:
        names = {norm_ws(e["id"]).lower()} | {norm_ws(str(e["params"].get(p))).lower() for p in ID_PARAMS if e["params"].get(p)}
        for n in names:
            by_name[n].append(e["key"])
        sv = strip_version(e["id"])
        if sv:
            by_name["~" + sv].append(e["key"])
        for p in ("title", "component_name", "name"):
            if e["params"].get(p):
                by_name["~" + strip_version(e["params"][p])].append(e["key"])
    for n, keys in by_name.items():
        for k in keys[1:]:
            union(keys[0], k)
    groups = defaultdict(list)
    for e in pool:
        groups[find(e["key"])].append(e)
    merged_count = 0
    for root, members in groups.items():
        if len(members) < 2:
            continue
        members.sort(key=lambda e: (-len(e["params"]), e["key"]))
        keep = members[0]
        keep.setdefault("aliases", [])
        for m in members[1:]:
            keep["aliases"].append({"key": m["key"], "id": m["id"], "entity_type": m["entity_type"], "docs": m["docs"]})
            for l2 in m["l2"]:
                if l2 not in keep["l2"]:
                    keep["l2"].append(l2)
            for d in m["docs"]:
                if d not in keep["docs"]:
                    keep["docs"].append(d)
            keep["quotes"] += m["quotes"]
            keep["_seen"] |= m["_seen"]; keep["_quote_bad"] += m["_quote_bad"]
            for k2, v in m["params"].items():
                if k2 not in keep["params"]:
                    keep["params"][k2] = v
                elif json.dumps(keep["params"][k2], sort_keys=True) != json.dumps(v, sort_keys=True):
                    if isinstance(v, list) and isinstance(keep["params"][k2], list):
                        keep["params"][k2] = list(keep["params"][k2]) + [i for i in v if i not in keep["params"][k2]]
                    elif pnorm(v) != pnorm(keep["params"][k2]):
                        keep["conflicts"].append({"param": k2, "values": [keep["params"][k2], v], "doc_id": m["docs"][0] if m["docs"] else None, "via_alias": m["id"]})
            for k2, src in m["param_sources"].items():
                keep["param_sources"].setdefault(k2, []).extend(src)
            del ents[m["key"]]
            merged_count += 1
        keep["alias_ids"] = sorted({a["id"] for a in keep["aliases"]} | {keep["id"]})
    # replicate agreement per entity: in how many of the replicate returns for its documents did it appear, and do the
    # replicates that filled a parameter agree on its value. confidence_level summarizes it for the report.
    replicated = any(len(v) > 1 for v in reps_by_doc.values())
    level_counts = Counter()
    for e in ents.values():
        possible = sum(len(reps_by_doc.get(d, {"-"})) for d in e["docs"])
        found = len(e["_seen"])
        disagree, by_param = [], {}
        for k, srcs in e["param_sources"].items():
            per_rep = defaultdict(set)
            for s in srcs:
                per_rep[(s["doc_id"], s["rep"])].add(pnorm(s["value"]))
            vals = {next(iter(v)) if len(v) == 1 else "∴" + "|".join(sorted(v)) for v in per_rep.values()}
            by_param[k] = {"reps": len(per_rep), "agree": len(vals) == 1}
            if len(vals) > 1:
                disagree.append(k)
        agreement = round(found / possible, 2) if possible else None
        if e["_quote_bad"]:
            level = "low"
        elif not replicated or possible < 2:
            level = "single"
        elif agreement == 1.0 and not disagree:
            level = "high"
        else:
            level = "medium"
        e["agreement"] = {"entity": agreement, "reps_possible": possible, "reps_found": found, "params_disagree": disagree, "params": by_param}
        e["confidence_level"] = level
        level_counts[level] += 1
        e["status"] = sorted(e["status"]); e["param_sources"] = dict(e["param_sources"])
        e["confidence"] = round(sum(e["confidence"]) / len(e["confidence"]), 1) if e["confidence"] else None
        e.pop("_seen", None); e.pop("_quote_bad", None)
    # resolve anchors: most frequent normalized value wins; any disagreement is a conflict
    resolved = {}
    for name in prof["anchors"]:
        claims = anchors.get(name, [])
        for c in claims:  # returns merged before shapes existed carry raw values; coerce here too (idempotent)
            c["value"], _ = coerce_anchor_value(name, c["value"])
        resolved[name] = resolve_anchor(name, claims)
    cov = {l2: dict(v) for l2, v in coverage.items()}
    reg = {"anchors": resolved, "documents": docs, "entities": ents, "unbinned": unbinned, "notes": notes, "coverage": cov,
           "replicates": {d: sorted(v) for d, v in reps_by_doc.items()},
           "counts": {"entities": len(ents), "documents": len(docs), "unbinned": len(unbinned), "alias_merges": merged_count,
                      "conflicting_entities": sum(bool(e["conflicts"]) for e in ents.values()),
                      "confidence_levels": dict(level_counts), "replicated_docs": sum(len(v) > 1 for v in reps_by_doc.values()),
                      "coverage_statements": sum(c["searched"] for v in cov.values() for c in v.values()),
                      "anchors_resolved": sum(v["value"] is not None for v in resolved.values()),
                      "anchors_conflicting": sum(v["conflict"] for v in resolved.values())}}
    write_json(ws / "registry.json", reg)
    print("registry:", reg["counts"])
    for k, v in resolved.items():
        if v["conflict"]:
            print(f"  anchor conflict {k}: {v['value']} vs {v['alternatives']}")


# ----------------------------------------------------------------------------- status

def status(ws: Path):
    idx = read_json(ws / "docs" / "index.json") if (ws / "docs" / "index.json").exists() else []
    metas = [read_json(p) for p in sorted((ws / "jobs").glob("*.meta.json"))]
    legacy = [p.stem for p in sorted((ws / "jobs").glob("*.md")) if not (ws / "jobs" / f"{p.stem}.meta.json").exists()]
    pending, done = [], []
    for m in metas:
        (done if Path(m["return"]).exists() else pending).append(m["job"])
    for j in legacy:
        target = (ws / "returns" / f"{j}.jsonl") if j.startswith("J-D") else (ws / "independent" / f"{j}.json") if j.startswith("J-I") else (ws / "brief" / f"{j}.json")
        (done if target.exists() else pending).append(j)
    print(f"docs: {len(idx)} ({sum(d.get('pages', 0) for d in idx)} pages) | brief: {'yes' if (ws/'brief.json').exists() else 'no'} | jobs: {len(metas)+len(legacy)} | returned: {len(done)}")
    print("pending jobs:", pending or "none")
    if (ws / "registry.json").exists():
        print("registry:", read_json(ws / "registry.json")["counts"])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("ws", type=Path); p.add_argument("--profile", type=Path, default=HERE.parent / "profile" / "profile.json")
    p = sub.add_parser("ingest"); p.add_argument("ws", type=Path); p.add_argument("source", type=Path)
    p = sub.add_parser("plan"); p.add_argument("ws", type=Path); p.add_argument("role", choices=["brief", "decompose", "independent"])
    p.add_argument("--max-pages", type=int, default=250); p.add_argument("--replicates", type=int, default=1); p.add_argument("--l1-per-job", type=int, default=6); p.add_argument("--docs")
    p = sub.add_parser("merge"); p.add_argument("ws", type=Path); p.add_argument("file", type=Path); p.add_argument("--job")
    p = sub.add_parser("merge-brief"); p.add_argument("ws", type=Path); p.add_argument("file", type=Path)
    p = sub.add_parser("registry"); p.add_argument("ws", type=Path)
    p = sub.add_parser("recompose"); p.add_argument("ws", type=Path)
    p = sub.add_parser("status"); p.add_argument("ws", type=Path)
    a = ap.parse_args()
    if a.cmd == "init": init(a.ws, a.profile)
    elif a.cmd == "ingest": ingest(a.ws, a.source)
    elif a.cmd == "plan": plan(a.ws, a.role, a.max_pages, a.replicates, a.l1_per_job, a.docs)
    elif a.cmd == "merge": merge(a.ws, a.file, a.job)
    elif a.cmd == "merge-brief": merge_brief(a.ws, a.file)
    elif a.cmd == "registry": registry(a.ws)
    elif a.cmd == "recompose":
        import recompose
        recompose.run(a.ws)
    elif a.cmd == "status": status(a.ws)


if __name__ == "__main__":
    main()
