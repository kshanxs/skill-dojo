import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "calligraph-sensei" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import preserve_check  # noqa: E402
import prose_lint  # noqa: E402
import snapshot  # noqa: E402
import voice_profile  # noqa: E402

PATTERN_HEAVY = """In today's fast-paced world, innovation plays a crucial role. This robust platform delves into a rich tapestry of seamless solutions. It's not just a tool — it's a movement — and experts say it is a game-changer — truly. I hope this helps!"""


def rule_set(text, **config):
    return {f["rule"] for f in prose_lint.lint(text, config)["findings"]}


class Lint(unittest.TestCase):
    def test_finds_objective_errors(self):
        found = rule_set("We has went to the the store. I recieved it. You could of been there.")
        self.assertTrue({"subject-verb", "verb-form", "doubled-word", "spelling", "modal-of"} <= found)

    def test_finds_stock_patterns(self):
        found = rule_set(PATTERN_HEAVY)
        self.assertTrue({"stock-phrase", "vague-source", "chat-residue", "em-dash", "overused-word"} <= found)

    def test_ignores_code_links_and_quotes(self):
        text = '```\nthe the recieve\n```\n\nSee `the the` and [a](http://x.io/the-the).\n\n> In today\'s fast-paced world, it plays a crucial role.\n'
        self.assertEqual(rule_set(text), set())

    def test_legitimate_repeats(self):
        self.assertEqual(rule_set("He had had enough. I knew that that was true."), set())

    def test_a_an_sound(self):
        self.assertEqual(rule_set("It was an hour at a university with a European and an honest man."), set())
        self.assertIn("a-an", rule_set("It was a apple."))

    def test_em_dash_policy(self):
        text = "One — two — three — four."
        self.assertIn("em-dash", rule_set(text))
        self.assertNotIn("em-dash", rule_set(text, em_dash="allow"))
        self.assertIn("em-dash", rule_set("One — two.", em_dash="avoid"))
        self.assertNotIn("em-dash", rule_set("One — two."))

    def test_project_style_guide(self):
        self.assertNotIn("spelling", rule_set("The teh ceremony.", allow=["teh"]))
        self.assertIn("project-deny", rule_set("We utilize it.", deny=["utilize"]))
        self.assertNotIn("doubled-word", rule_set("the the", disable=["doubled-word"]))

    def test_config_rejects_typos(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / ".calligraph.json"
            path.write_text('{"alow": []}', encoding="utf-8")
            with self.assertRaises(ValueError):
                prose_lint.load_config(path, None)

    def test_config_is_discovered_from_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / ".calligraph.json").write_text('{"em_dash": "allow"}', encoding="utf-8")
            (Path(tmp) / "ch").mkdir()
            draft = Path(tmp) / "ch" / "one.md"
            draft.write_text("x", encoding="utf-8")
            self.assertEqual(prose_lint.load_config(None, draft)["em_dash"], "allow")

    def test_report_makes_no_authorship_claim(self):
        report = prose_lint.render(prose_lint.lint(PATTERN_HEAVY), "a.md")
        self.assertIn("does not detect AI authorship", report)
        self.assertNotIn("probability", report.lower())


class Calibration(unittest.TestCase):
    def test_human_prose_is_quiet(self):
        for path in sorted((ROOT / "tests" / "corpus").glob("*.md")):
            result = prose_lint.lint(path.read_text(encoding="utf-8"))
            words = result["stats"]["words"]
            serious = result["counts"].get("error", 0) + result["counts"].get("warning", 0)
            self.assertLess(serious * 1000 / words, 2.0, path.name)

    def test_pattern_heavy_text_is_much_louder_than_human_prose(self):
        result = prose_lint.lint(PATTERN_HEAVY)
        serious = result["counts"].get("error", 0) + result["counts"].get("warning", 0)
        self.assertGreater(serious * 1000 / result["stats"]["words"], 50)


class Preserve(unittest.TestCase):
    ORIGINAL = 'Marie Curie won in 1903 (Curie, 1903). She said "radium is not a toy at all". See https://a.org/x and `run()`.\n\n## Results\n\nIt did not fail in 42% of cases.\n'

    def test_identical(self):
        self.assertTrue(preserve_check.compare(self.ORIGINAL, self.ORIGINAL)["preserved"])

    def test_changed_number(self):
        result = preserve_check.compare(self.ORIGINAL, self.ORIGINAL.replace("42%", "24%"))
        self.assertFalse(result["preserved"])
        self.assertEqual({c["kind"] for c in result["changes"]}, {"number"})

    def test_each_protected_type(self):
        for old, new, kind in [("https://a.org/x", "https://a.org/y", "url"), ("`run()`", "`go()`", "inline_code"), ("(Curie, 1903)", "", "citation"), ("radium is not a toy", "radium is no toy", "quotation"), ("## Results", "## Findings", "heading")]:
            changed = {c["kind"] for c in preserve_check.compare(self.ORIGINAL, self.ORIGINAL.replace(old, new))["changes"]}
            self.assertIn(kind, changed, old)

    def test_dropped_negation_is_raised(self):
        review = preserve_check.compare("It did not fail.", "It did fail.")["review"]
        self.assertIn("negation", {r["kind"] for r in review})

    def test_new_name_is_raised(self):
        review = preserve_check.compare("We met the mayor.", "We met the mayor, Ada Lovelace.")["review"]
        self.assertIn("name", {r["kind"] for r in review})

    def test_code_block_change(self):
        a, b = "```py\nx = 1\n```\n", "```py\nx = 2\n```\n"
        self.assertIn("code_block", {c["kind"] for c in preserve_check.compare(a, b)["changes"]})


class Voice(unittest.TestCase):
    def test_detects_drift(self):
        sample = "I can't say I'm sure. We don't know. I won't guess, and you shouldn't either. " * 30
        edit = "The committee subsequently determined that further deliberation would be required before proceeding with the proposal under consideration. " * 20
        drift = {d["metric"] for d in voice_profile.compare(voice_profile.profile(sample), voice_profile.profile(edit))}
        self.assertIn("contractions_per_1000", drift)
        self.assertIn("mean_sentence_words", drift)

    def test_same_text_has_no_drift(self):
        text = (ROOT / "tests" / "corpus" / "mill.md").read_text(encoding="utf-8")
        profile = voice_profile.profile(text)
        self.assertEqual(voice_profile.compare(profile, profile), [])

    def test_light_proofreading_of_real_prose_shows_no_drift(self):
        for name in ("mill", "austen", "darwin", "douglass"):
            text = (ROOT / "tests" / "corpus" / f"{name}.md").read_text(encoding="utf-8")
            edit = text.replace(" the ", " teh ", 1).replace("  ", " ")
            self.assertEqual(voice_profile.compare(voice_profile.profile(text), voice_profile.profile(edit)), [], name)

    def test_indented_plain_text_is_prose(self):
        text = "\n\n".join("    I can't say this is code. It is a paragraph." for _ in range(5))
        self.assertGreater(voice_profile.profile(text)["words"], 0)


class Snapshot(unittest.TestCase):
    def test_copy_is_exact_and_original_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft.md"
            path.write_text("words\n", encoding="utf-8")
            copy = snapshot.take(path)
            self.assertEqual(copy.read_bytes(), path.read_bytes())
            self.assertEqual(snapshot.take(path), copy)
            path.write_text("changed\n", encoding="utf-8")
            second = snapshot.take(path)
            self.assertNotEqual(second, copy)
            self.assertEqual(copy.read_text(encoding="utf-8"), "words\n")


class Cli(unittest.TestCase):
    def test_lint_refuses_to_write_over_input(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft.md"
            path.write_text("Text.\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPTS / "prose_lint.py"), str(path), "--out", str(path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(path.read_text(encoding="utf-8"), "Text.\n")

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "draft.md"
            path.write_text("The the end.\n", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPTS / "prose_lint.py"), str(path), "--format", "json", "--fail-on", "error"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads(result.stdout)["counts"]["error"], 1)


if __name__ == "__main__":
    unittest.main()
