import datetime as dt
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "research-dojo" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_dates  # noqa: E402
import check_sources  # noqa: E402
import dojo_check  # noqa: E402
import extract_claims  # noqa: E402

TODAY = dt.date(2026, 11, 22)


def rules(text):
    return {f["rule"] for f in check_dates.check(text, TODAY)}


class Dates(unittest.TestCase):
    def test_impossible_date(self):
        self.assertIn("impossible-date", rules("It was signed on February 30, 1920."))
        self.assertIn("impossible-date", rules("It happened on 29 February 1900."))
        self.assertNotIn("impossible-date", rules("It happened on 29 February 2000."))

    def test_weekday(self):
        self.assertIn("weekday-mismatch", rules("He died on Tuesday, April 19, 1882."))
        self.assertEqual(rules("He died on Wednesday, April 19, 1882."), set())
        self.assertIn("weekday-mismatch", rules("We met on Monday, March 3, 2025 and left."[:0] + "We met on Tuesday, March 4, 2024."))

    def test_old_style_weekday_is_not_an_error(self):
        found = check_dates.check("Washington was born on Friday, February 11, 1731.", TODAY)
        self.assertTrue(all(f["severity"] != "error" for f in found))

    def test_ranges(self):
        self.assertIn("reversed-range", rules("The war ran 1918–1914."))
        self.assertEqual(rules("The war ran 1914–18."), set())
        self.assertEqual(rules("See pp. 1918-1914 of the volume."), set())

    def test_age(self):
        self.assertIn("age-mismatch", rules("Charles Darwin (1809–1882) published in 1859 at age 70."))
        self.assertNotIn("age-mismatch", rules("Charles Darwin (1809–1882) published in 1859 at age 50."))
        self.assertIn("death-before-birth", rules("She was born in 1900 and died in 1850."))

    def test_relative(self):
        self.assertIn("relative-date", rules("In 1900 it opened. Ten years later, in 1920, it closed."))
        self.assertEqual(rules("In 1900 it opened. Ten years later, in 1910, it closed."), set())

    def test_future_needs_past_tense(self):
        self.assertIn("future-date", rules("The launch was in 2031."))
        self.assertEqual(rules("The launch will happen in 2031."), set())

    def test_code_is_ignored(self):
        self.assertEqual(rules("```\nFebruary 31, 2020\n```\n\nInline `February 31, 2020` too."), set())


class Identifiers(unittest.TestCase):
    def test_checksums(self):
        self.assertTrue(check_sources.isbn_valid("978-0-14-044913-6"))
        self.assertFalse(check_sources.isbn_valid("978-0-14-044913-7"))
        self.assertTrue(check_sources.isbn_valid("0-306-40615-2"))
        self.assertTrue(check_sources.issn_valid("0028-0836"))
        self.assertFalse(check_sources.issn_valid("0028-0837"))

    def test_arxiv(self):
        self.assertTrue(check_sources.arxiv_valid("1706.03762", TODAY))
        self.assertFalse(check_sources.arxiv_valid("2613.00001", TODAY))
        self.assertFalse(check_sources.arxiv_valid("1713.00001", TODAY))

    def test_trailing_punctuation_is_not_part_of_a_doi(self):
        item = check_sources.extract("See doi:10.1038/nature14539.")[0]
        self.assertEqual(item["value"], "10.1038/nature14539")

    def test_offline_never_claims_found(self):
        items = check_sources.check(check_sources.extract("doi:10.1038/nature14539 https://example.com/a"))
        self.assertEqual({i["status"] for i in items}, {"format_ok", "not_checked"})

    def test_private_addresses_are_not_fetched(self):
        for url in ("http://127.0.0.1:8080/x", "http://169.254.169.254/latest/", "file:///etc/passwd"):
            self.assertEqual(check_sources.fetch(url), (-1, ""))


def crossref(**extra):
    message = {"title": ["Deep learning"], "issued": {"date-parts": [[2015, 5, 27]]}, "author": [{"family": "LeCun"}], "container-title": ["Nature"]}
    message.update(extra)
    return 200, json.dumps({"message": message})


class Online(unittest.TestCase):
    def run_one(self, line, fetcher):
        return check_sources.check(check_sources.extract(line), online=True, fetcher=fetcher, delay=0)[0]

    def test_found_is_not_verified(self):
        item = self.run_one("LeCun et al. (2015). Deep learning. Nature. doi:10.1038/nature14539", lambda u: crossref())
        self.assertEqual(item["status"], "source_found")
        self.assertIn("confirm", item["detail"])

    def test_wrong_year(self):
        item = self.run_one("LeCun et al. (2009). Deep learning. Nature. doi:10.1038/nature14539", lambda u: crossref())
        self.assertEqual(item["status"], "metadata_mismatch")

    def test_wrong_paper(self):
        item = self.run_one("Smith, J. (2015). Soil chemistry of river basins in Peru. doi:10.1038/nature14539", lambda u: crossref())
        self.assertEqual(item["status"], "metadata_mismatch")

    def test_retraction(self):
        item = self.run_one("doi:10.1/x".replace("10.1/", "10.1021/"), lambda u: crossref(**{"updated-by": [{"type": "retraction", "DOI": "10.1/n", "source": "retraction-watch"}]}))
        self.assertEqual(item["status"], "retracted")

    def test_404_then_handle_missing(self):
        item = self.run_one("doi:10.1038/fake", lambda u: (404, ""))
        self.assertEqual(item["status"], "not_found")

    def test_outage_is_unreachable_not_missing(self):
        item = self.run_one("doi:10.1038/fake", lambda u: (0, ""))
        self.assertEqual(item["status"], "unreachable")

    def test_bad_json_is_unreachable(self):
        item = self.run_one("doi:10.1038/fake", lambda u: (200, "not json"))
        self.assertEqual(item["status"], "unreachable")


class Ledger(unittest.TestCase):
    def claim(self, **kw):
        return {"claims": [{"id": "C001", "status": "verified", "evidence": [], **kw}]}

    def test_verified_requires_evidence(self):
        self.assertTrue(dojo_check.validate(self.claim(), TODAY))

    def test_verified_requires_a_locator_and_date(self):
        self.assertTrue(dojo_check.validate(self.claim(evidence=[{"source": "x"}]), TODAY))
        self.assertTrue(dojo_check.validate(self.claim(evidence=[{"source": "x", "locator": "p. 2", "checked_on": "2099-01-01"}]), TODAY))

    def test_good_evidence_passes(self):
        evidence = [{"source": "https://example.org/a", "locator": "p. 2", "checked_on": "2026-11-01"}]
        self.assertEqual(dojo_check.validate(self.claim(evidence=evidence), TODAY), [])

    def test_tools_never_output_verified(self):
        ledger = dojo_check.build("In 1900, 73% of people voted. doi:10.1038/nature14539", "a.md", True, TODAY, fetcher=lambda u: crossref())
        self.assertEqual({c["status"] for c in ledger["claims"]}, {"unchecked"})
        self.assertIn("**0 of 1 claims are verified.**", dojo_check.render(ledger))

    def test_reviews_survive_a_rerun(self):
        text = "In 1900, 73% of people voted."
        first = dojo_check.build(text, "a.md", False, TODAY)
        first["claims"][0].update(status="verified", evidence=[{"source": "s", "locator": "p", "checked_on": "2026-01-01"}])
        second = dojo_check.build("New opening.\n\n" + text, "a.md", False, TODAY, previous=first)
        self.assertEqual(second["claims"][0]["status"], "verified")

    def test_hand_edited_verified_without_evidence_is_not_counted(self):
        first = dojo_check.build("In 1900, 73% of people voted.", "a.md", False, TODAY)
        first["claims"][0]["status"] = "verified"
        second = dojo_check.build("In 1900, 73% of people voted.", "a.md", False, TODAY, previous=first)
        self.assertEqual(second["claims"][0]["status"], "unchecked")
        self.assertIn("**0 of 1 claims are verified.**", dojo_check.render(second))

    def test_edited_sentence_loses_its_review(self):
        first = dojo_check.build("In 1900, 73% of people voted.", "a.md", False, TODAY)
        first["claims"][0].update(status="verified", evidence=[{"source": "s", "locator": "p", "checked_on": "2026-01-01"}])
        second = dojo_check.build("In 1900, 75% of people voted.", "a.md", False, TODAY, previous=first)
        self.assertEqual(second["claims"][0]["status"], "unchecked")


class Cli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / "dojo_check.py"), *map(str, args)], capture_output=True, text=True)

    def test_input_is_never_changed_and_reports_are_predictable(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "draft.md"
            draft.write_text("It was signed on February 30, 1920.\n", encoding="utf-8")
            before = draft.read_bytes()
            result = self.run_cli(draft, "--out-dir", Path(tmp) / "reports", "--annotate", Path(tmp) / "flagged.md")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(draft.read_bytes(), before)
            self.assertTrue((Path(tmp) / "reports" / "draft.factcheck.md").is_file())
            self.assertTrue((Path(tmp) / "reports" / "draft.factcheck.json").is_file())
            self.assertIn("[DATE:", (Path(tmp) / "flagged.md").read_text(encoding="utf-8"))

    def test_bom_crlf_and_bad_encoding(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "win.md"
            draft.write_bytes("\ufeff---\r\ntitle: February 31, 2020\r\n---\r\nSigned on February 30, 1920.\r\n".encode("utf-8"))
            result = self.run_cli(draft, "--format", "json")
            self.assertEqual(result.returncode, 0, result.stderr)
            findings = json.loads(result.stdout)["date_findings"]
            self.assertEqual([(f["line"], f["rule"]) for f in findings], [(4, "impossible-date")])
            draft.write_bytes(b"caf\xe9 latin-1")
            result = self.run_cli(draft)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Traceback", result.stderr)

    def test_corrupt_ledger_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "d.md"
            draft.write_text("In 1900, 40% left.\n", encoding="utf-8")
            ledger = Path(tmp) / "d.factcheck.json"
            ledger.write_text("{broken", encoding="utf-8")
            self.assertNotEqual(self.run_cli(draft, "--out-dir", tmp).returncode, 0)
            self.assertEqual(ledger.read_text(encoding="utf-8"), "{broken")

    def test_annotate_refuses_the_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "draft.md"
            draft.write_text("Text.\n", encoding="utf-8")
            self.assertNotEqual(self.run_cli(draft, "--annotate", draft).returncode, 0)
            self.assertEqual(draft.read_text(encoding="utf-8"), "Text.\n")


class Calibration(unittest.TestCase):
    def test_public_domain_text_has_no_date_errors(self):
        for path in sorted((ROOT / "tests" / "corpus").glob("*.md")):
            found = [f for f in check_dates.check(path.read_text(encoding="utf-8"), TODAY) if f["severity"] == "error"]
            self.assertEqual(found, [], path.name)

    def test_claims_have_ids_and_start_unchecked(self):
        claims = extract_claims.extract("According to the census, 40% moved in 1900.")
        self.assertEqual(claims[0]["id"], "C001")
        self.assertEqual(claims[0]["status"], "unchecked")
        self.assertEqual(claims[0]["priority"], "high")


if __name__ == "__main__":
    unittest.main()
