"""Tests for review/v3: page-level ingest, page-verified merge, brief and per-document planning, replicate agreement."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V3 = ROOT / "review" / "v3"
sys.path.insert(0, str(V3 / "tools"))
import v3  # noqa: E402

PROFILE = V3 / "profile" / "profile.json"


def run(*args):
    return subprocess.run([sys.executable, "-B", str(V3 / "tools" / "v3.py"), *map(str, args)], capture_output=True, text=True, check=True).stdout


class TextPages(unittest.TestCase):
    def test_sections_become_pages_and_long_sections_split(self):
        text = "# Title\n\nintro\n\n## 1. Scope\n\nbody one\n\n## 2. Records\n\n" + ("para\n\n" * 3000)
        pages = v3.text_pages(text, target=6000)
        self.assertEqual(pages[0]["label"], "start")
        self.assertEqual(pages[1]["label"], "1. Scope")
        self.assertTrue(pages[2]["label"].startswith("2. Records"))
        self.assertGreater(len(pages), 3)
        self.assertEqual([p["page"] for p in pages], list(range(1, len(pages) + 1)))
        self.assertEqual("".join(p["text"] for p in pages), text)

    def test_split_job(self):
        self.assertEqual(v3.split_job("J-D-05-a"), ("J-D-05", "a"))
        self.assertEqual(v3.split_job("J-D-05p2-b"), ("J-D-05p2", "b"))
        self.assertEqual(v3.split_job("J-O-01"), ("J-O-01", None))


class Workspace(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ws = Path(self.tmp.name) / "ws"
        src = Path(self.tmp.name) / "src"
        src.mkdir()
        (src / "01-Cover.md").write_text("# Cover Letter\n\nSoftware version proposed for approval: 3.2.0\n\n## Contents\n\nSVR, SBOM\n")
        (src / "10-SVR.md").write_text("# System Verification Report\n\n## 1. Scope\n\nBuild b1187.\n\n## 4. Runs\n\n| TR-0412 | TC-031 | Pass |\n| TR-0413 | TC-032 | Fail |\n")
        run("init", self.ws, "--profile", PROFILE)
        run("ingest", self.ws, src)
        self.index = json.loads((self.ws / "docs" / "index.json").read_text())

    def tearDown(self):
        self.tmp.cleanup()

    def write_return(self, job, records):
        p = Path(self.tmp.name) / f"{job}.jsonl"
        p.write_text("\n".join(json.dumps(r) for r in records) + "\n")
        return p

    def test_ingest_pages_and_index(self):
        self.assertEqual([d["doc_id"] for d in self.index], ["D01", "D02"])
        self.assertEqual(self.index[1]["pages"], 3)
        pages = v3.load_pages(self.ws, "D02")
        self.assertEqual(pages[2]["label"], "4. Runs")
        self.assertIn("<<page 3 | 4. Runs>>", (self.ws / "docs" / "D02.txt").read_text())
        self.assertTrue(self.index[1]["source_path"].endswith("10-SVR.md"))

    def test_merge_verifies_quote_on_page(self):
        recs = [
            {"type": "entity", "entity_type": "test_run", "id": "TR-0412", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {"test_case_id": "TC-031", "result": "pass"}, "quote": "TR-0412 | TC-031 | Pass", "status": "executed", "confidence": 3},
            {"type": "entity", "entity_type": "test_run", "id": "TR-0413", "l2": "L2-09.05", "doc_id": "D02", "page": 1, "params": {"result": "fail"}, "quote": "TR-0413 | TC-032 | Fail", "confidence": 3},
            {"type": "entity", "entity_type": "test_run", "id": "TR-0999", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {}, "quote": "this text is not in the document", "confidence": 3},
            {"type": "entity", "entity_type": "test_run", "id": "TR-0998", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {}},
            {"type": "coverage", "doc_id": "D02", "l2": "L2-09.06", "found": False, "note": "no regression analysis here"},
            {"type": "coverage", "doc_id": "D02", "l2": "L2-99.99", "found": True},
        ]
        out = run("merge", self.ws, self.write_return("J-D-02-a", recs))
        kept = [json.loads(l) for l in (self.ws / "returns" / "J-D-02-a.jsonl").read_text().splitlines()]
        by_id = {r.get("id"): r for r in kept if r["type"] == "entity"}
        self.assertTrue(by_id["TR-0412"]["quote_ok"]); self.assertNotIn("flag_page_mismatch", by_id["TR-0412"])
        self.assertTrue(by_id["TR-0413"]["flag_page_mismatch"]); self.assertEqual(by_id["TR-0413"]["page_found"], 3)
        self.assertTrue(by_id["TR-0999"]["flag_quote_not_found"])
        self.assertNotIn("TR-0998", by_id)
        self.assertEqual([r for r in kept if r["type"] == "unbinned"][0]["reason"][:20], "entity without quote")
        self.assertEqual([r["l2"] for r in kept if r["type"] == "coverage"], ["L2-09.06"])
        self.assertEqual(kept[0]["rep"], "a"); self.assertEqual(kept[0]["job_base"], "J-D-02")
        self.assertIn("quotes not found: 1", out)

    def test_plan_brief_and_decompose_use_roster(self):
        out = run("plan", self.ws, "brief")
        self.assertIn("['D01']", out)
        brief = {"job_id": "J-B-01", "roster": [{"doc_id": "D01", "role": "cover", "feeds_l1": ["L1-00"]}, {"doc_id": "D02", "role": "svr", "feeds_l1": ["L1-09", "L1-XX"]}],
                 "anchors": [{"name": "A.proposed_version", "value": "3.2.0", "doc_id": "D01", "page": 1, "quote": "proposed for approval: 3.2.0"}], "standards_claimed": []}
        bp = Path(self.tmp.name) / "brief.json"; bp.write_text(json.dumps(brief))
        out = run("merge-brief", self.ws, bp)
        self.assertIn("unknown L1 ['L1-XX']", out)
        self.assertTrue((self.ws / "returns" / "J-B-01.jsonl").exists())
        out = run("plan", self.ws, "decompose", "--replicates", "2", "--max-pages", "2")
        jobs = sorted(p.name for p in (self.ws / "jobs").glob("J-D-*.md"))
        self.assertEqual(jobs, ["J-D-01-a.md", "J-D-01-b.md", "J-D-02p1-a.md", "J-D-02p1-b.md", "J-D-02p2-a.md", "J-D-02p2-b.md"])
        meta = json.loads((self.ws / "jobs" / "J-D-02p2-a.meta.json").read_text())
        self.assertEqual(meta["pages"], [3, 3]); self.assertEqual(meta["l1"], ["L1-09"]); self.assertEqual(meta["replicate"], "a")
        body = (self.ws / "jobs" / "J-D-02p2-a.md").read_text()
        self.assertIn("### L1-09", body); self.assertNotIn("### L1-16", body)       # bins sliced by the roster
        self.assertIn("- L1-16 Software bill of materials", body)                   # other bins listed compactly
        self.assertIn("A.proposed_version = \"3.2.0\"", body)                       # brief anchors shown
        self.assertIn("<<page 3 | 4. Runs>>", body); self.assertNotIn("<<page 1 |", body.split("## Document")[1])
        out = run("plan", self.ws, "independent")
        self.assertIn("role: svr", (self.ws / "jobs" / "J-I-01.md").read_text())

    def test_registry_agreement_across_replicates(self):
        a = [{"type": "entity", "entity_type": "test_run", "id": "TR-0412", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {"test_case_id": "TC-031", "result": "pass"}, "quote": "TR-0412 | TC-031 | Pass", "confidence": 3},
             {"type": "entity", "entity_type": "test_run", "id": "TR-0413", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {"result": "fail"}, "quote": "TR-0413 | TC-032 | Fail", "confidence": 3},
             {"type": "coverage", "doc_id": "D02", "l2": "L2-09.06", "found": False}]
        b = [{"type": "entity", "entity_type": "test_run", "id": "TR-0412", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {"test_case_id": "TC-031", "result": "Pass"}, "quote": "TR-0412 | TC-031 | Pass", "confidence": 3},
             {"type": "entity", "entity_type": "test_run", "id": "TR-0413", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {"result": "pass"}, "quote": "TR-0413 | TC-032 | Fail", "confidence": 2},
             {"type": "entity", "entity_type": "test_run", "id": "TR-0414", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {}, "quote": "Build b1187", "confidence": 1},
             {"type": "coverage", "doc_id": "D02", "l2": "L2-09.06", "found": False}]
        run("merge", self.ws, self.write_return("J-D-02-a", a))
        run("merge", self.ws, self.write_return("J-D-02-b", b))
        run("registry", self.ws)
        reg = json.loads((self.ws / "registry.json").read_text())
        e = reg["entities"]
        self.assertEqual(e["test_run:TR-0412"]["confidence_level"], "high")      # both replicates, values agree after case folding
        self.assertEqual(e["test_run:TR-0413"]["confidence_level"], "medium")    # both replicates, `result` disagrees
        self.assertEqual(e["test_run:TR-0413"]["agreement"]["params_disagree"], ["result"])
        self.assertEqual(e["test_run:TR-0414"]["confidence_level"], "medium")    # seen in one of two replicates
        self.assertEqual(e["test_run:TR-0414"]["agreement"]["entity"], 0.5)
        self.assertEqual(reg["replicates"]["D02"], ["a", "b"])
        self.assertEqual(reg["coverage"]["L2-09.06"]["D02"], {"searched": 2, "found": 0})
        self.assertEqual(reg["counts"]["confidence_levels"], {"high": 1, "medium": 2})
        run("recompose", self.ws)
        rep = json.loads((self.ws / "report" / "report.json").read_text())
        row = {r["l2"]: r for r in rep["l2"]}
        self.assertEqual(row["L2-09.06"]["status"], "absent"); self.assertEqual(row["L2-09.06"]["absence_basis"], "searched")
        self.assertEqual(row["L2-09.06"]["searched_not_found"], ["D02"])
        self.assertEqual(row["L2-09.05"]["confidence"], {"high": 1, "medium": 2})
        self.assertEqual(rep["summary"]["replicated_docs"], 1)

    def test_single_return_is_single_confidence(self):
        a = [{"type": "entity", "entity_type": "test_run", "id": "TR-0412", "l2": "L2-09.05", "doc_id": "D02", "page": 3, "params": {}, "quote": "TR-0412 | TC-031 | Pass", "confidence": 3}]
        run("merge", self.ws, self.write_return("J-D-02", a))
        run("registry", self.ws)
        reg = json.loads((self.ws / "registry.json").read_text())
        self.assertEqual(reg["entities"]["test_run:TR-0412"]["confidence_level"], "single")


if __name__ == "__main__":
    unittest.main()


class OracleGolden(unittest.TestCase):
    """The oracle return on SYN-PMA-SW-01 must keep finding every planted defect with no unmatched S2/S3 break.
    Any change to the tools, profile, fixture or oracle that moves these numbers must be deliberate."""

    def test_oracle_recall_and_precision(self):
        with tempfile.TemporaryDirectory() as tmp:
            ws = Path(tmp) / "ws"
            oracle = Path(tmp) / "oracle.jsonl"
            run("init", ws, "--profile", PROFILE)
            run("ingest", ws, V3 / "fixtures" / "syn-pma-sw-01" / "docs")
            subprocess.run([sys.executable, "-B", str(V3 / "fixtures" / "oracle_syn01.py"), str(oracle)], check=True, capture_output=True)
            run("merge", ws, oracle, "--job", "J-O-01")
            run("registry", ws)
            run("recompose", ws)
            subprocess.run([sys.executable, "-B", str(V3 / "tools" / "score.py"), str(ws), str(V3 / "fixtures" / "syn-pma-sw-01" / "defects.json")], check=True, capture_output=True)
            score = json.loads((ws / "report" / "score.json").read_text())
            self.assertEqual(score["planted"], 23)
            self.assertEqual(score["detected"], 23, [m["id"] for m in score["missed"]])
            self.assertEqual([f for f in score["unmatched_breaks"] if f["severity"] in ("S2", "S3")], [])
            self.assertEqual(score["false_positive_checks"], [])
            self.assertEqual(score["unplanted_kept"]["detected"], 2)   # UK-04 and UK-05 are mechanical; UK-01..03 need the independent pass
