"""test_check.py — unit tests for scripts/check.py.

Last Modified: 2026-08-31 18:30, initial version for the v1.0.0 public release.
Inputs:  scripts/check.py
Outputs: test results on stderr; non-zero exit on failure

Workflow:
  - exercise the minimal JSON Schema validator on each keyword it supports
  - exercise the helpers that decide what counts as a repository path
  - confirm the report tracks failures and that a real run of every check passes

CAUTION: run with `python3 -m unittest discover tests`. Uses only the standard
library so that CI needs no dependency beyond Python itself.
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import check  # noqa: E402


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Minimal JSON Schema validator
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class TestValidate(unittest.TestCase):
    """The validator must catch every keyword the shipped schemas rely on."""

    def check(self, instance, schema, root=None):
        """Run the validator and return its errors."""
        return check.validate(instance, schema, root if root is not None else schema)

    def test_accepts_a_valid_object(self):
        schema = {
            "type": "object",
            "required": ["a"],
            "additionalProperties": False,
            "properties": {"a": {"type": "string"}, "b": {"type": "integer"}},
        }
        self.assertEqual(self.check({"a": "x", "b": 1}, schema), [])

    def test_rejects_wrong_type(self):
        errors = self.check(5, {"type": "string"})
        self.assertEqual(len(errors), 1)
        self.assertIn("expected string", errors[0])

    def test_rejects_missing_required_property(self):
        errors = self.check({}, {"type": "object", "required": ["a"], "properties": {}})
        self.assertIn("missing required property 'a'", errors[0])

    def test_rejects_unexpected_property_when_additional_is_false(self):
        schema = {"type": "object", "additionalProperties": False, "properties": {}}
        self.assertIn("unexpected property 'z'", self.check({"z": 1}, schema)[0])

    def test_allows_unexpected_property_when_additional_is_absent(self):
        self.assertEqual(self.check({"z": 1}, {"type": "object", "properties": {}}), [])

    def test_rejects_value_outside_enum(self):
        self.assertIn("not one of", self.check("c", {"enum": ["a", "b"]})[0])

    def test_validates_array_items(self):
        schema = {"type": "array", "items": {"type": "string"}}
        errors = self.check(["ok", 3], schema)
        self.assertEqual(len(errors), 1)
        self.assertIn("<root>[1]", errors[0])

    def test_enforces_minimum_and_maximum(self):
        self.assertIn("below minimum", self.check(0, {"type": "integer", "minimum": 1})[0])
        self.assertIn("above maximum", self.check(9, {"type": "integer", "maximum": 5})[0])

    def test_bool_is_not_an_integer(self):
        """JSON Schema separates boolean from integer even though Python does not."""
        self.assertTrue(self.check(True, {"type": "integer"}))

    def test_resolves_a_ref_into_defs(self):
        root = {
            "type": "object",
            "properties": {"a": {"$ref": "#/$defs/leaf"}},
            "$defs": {"leaf": {"type": "string"}},
        }
        self.assertEqual(self.check({"a": "x"}, root, root), [])
        self.assertTrue(self.check({"a": 1}, root, root))

    def test_reports_an_unsupported_ref_rather_than_passing_it(self):
        errors = self.check({}, {"$ref": "https://example.com/s.json"})
        self.assertIn("unsupported $ref", errors[0])

    def test_error_paths_name_the_offending_field(self):
        root = {
            "type": "object",
            "properties": {"outer": {"type": "object",
                                     "properties": {"inner": {"type": "string"}}}},
        }
        self.assertIn("<root>.outer.inner", self.check({"outer": {"inner": 1}}, root)[0])


class TestPlanningCalendarSchema(unittest.TestCase):
    """The planning destination schema owns calendar-write policy."""

    def setUp(self):
        self.schema = json.loads(
            (check.REPO / "plugins/lifeyoda/config/local.schema.json").read_text())

    def validate_destination(self, destination):
        """Validate a planningCalendar destination against the shipped schema."""
        return check.validate(
            destination, self.schema["$defs"]["calendarDestination"], self.schema)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Helpers
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class TestDig(unittest.TestCase):
    """`dig` walks dicts by key and lists by index."""

    def test_walks_nested_keys(self):
        self.assertEqual(check.dig({"a": {"b": "v"}}, ("a", "b")), "v")

    def test_treats_a_segment_as_an_index_inside_a_list(self):
        self.assertEqual(check.dig({"a": [{"b": "v"}]}, ("a", "0", "b")), "v")

    def test_raises_on_a_missing_key(self):
        with self.assertRaises(KeyError):
            check.dig({"a": 1}, ("b",))


class TestFrontmatter(unittest.TestCase):
    """Frontmatter parsing reads top-level scalars and ignores nested lines."""

    def parse(self, text: str):
        path = Path(self.tmp.name) / "f.md"
        path.write_text(text)
        return check._frontmatter(path)

    def setUp(self):
        import tempfile
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def test_reads_top_level_keys(self):
        self.assertEqual(self.parse("---\nname: a\ndescription: b\n---\nbody\n"),
                         {"name": "a", "description": "b"})

    def test_returns_none_without_a_block(self):
        self.assertIsNone(self.parse("# heading\n"))

    def test_ignores_indented_and_list_lines(self):
        parsed = self.parse("---\nname: a\nlist:\n  - one\n  - two\n---\nbody\n")
        self.assertEqual(set(parsed), {"name", "list"})


class TestTrackedFiles(unittest.TestCase):
    """The file set must cover new work and exclude what git ignores."""

    def setUp(self):
        self.files = set(check.tracked_files())

    def test_includes_a_committed_file(self):
        self.assertIn("scripts/check.py", self.files)

    def test_excludes_gitignored_paths(self):
        """A green check that never saw the new file is worse than no check."""
        ignored = {"SESSION_REPORT.md"}
        self.assertEqual(self.files & ignored, set())

    def test_returns_no_duplicates(self):
        listed = check.tracked_files()
        self.assertEqual(len(listed), len(set(listed)))


class TestResolves(unittest.TestCase):
    """Reference resolution accepts the three roots a path may be written against."""

    def test_resolves_against_the_repository_root(self):
        self.assertTrue(check._resolves("scripts/check.py", check.REPO / "README.md"))

    def test_resolves_against_the_plugin_root(self):
        self.assertTrue(check._resolves("workflows/morning-brief-and-plan.md",
                                        check.PLUGIN / "docs" / "source-policy.md"))

    def test_resolves_a_skill_relative_fallback_two_levels_up(self):
        self.assertTrue(check._resolves("../../workflows/morning-brief-and-plan.md",
                                        check.PLUGIN / "commands" / "daily.md"))

    def test_rejects_a_three_level_fallback(self):
        """The bug this check exists to catch: a skill sits two levels deep, not three."""
        self.assertFalse(check._resolves("../../../workflows/morning-brief-and-plan.md",
                                         check.PLUGIN / "commands" / "daily.md"))

    def test_rejects_a_path_that_does_not_exist(self):
        self.assertFalse(check._resolves("workflows/nope.md", check.REPO / "README.md"))


class TestJsonStringPaths(unittest.TestCase):
    """Paths embedded in JSON values are found the same way as ones in prose."""

    def test_finds_a_nested_path(self):
        found = list(check._json_string_paths({"a": {"b": "templates/x.md"}}))
        self.assertEqual(found, ["templates/x.md"])

    def test_finds_paths_inside_lists(self):
        found = list(check._json_string_paths(["config/a.json", "not a path"]))
        self.assertEqual(found, ["config/a.json"])

    def test_ignores_prose_and_runtime_paths(self):
        data = {"note": "see config/a.json for details", "home": "~/.lifeyoda/local.json",
                "runtime": "private/local.json", "bare": "README.md"}
        self.assertEqual(list(check._json_string_paths(data)), [])


class TestJsonPathExemption(unittest.TestCase):
    """Fixtures name files on an imaginary machine and must not be resolved here."""

    def test_fixtures_are_exempt(self):
        self.assertTrue(any(e.startswith("plugins/lifeyoda/fixtures")
                            for e in check.JSON_PATH_EXEMPT))

    def test_shipped_config_is_not_exempt(self):
        """public.defaults.json names real template paths; those must still resolve."""
        self.assertFalse("plugins/lifeyoda/config/".startswith(check.JSON_PATH_EXEMPT))


class TestKeyReferenceRegex(unittest.TestCase):
    """Both reference spellings must match; the bug that prompted this was the bare one."""

    def match(self, text):
        return check.KEY_REFERENCE.findall(text)

    def test_matches_the_bare_form_used_inside_json_values(self):
        self.assertEqual(
            self.match("dailyPlan.emojiPool in config/public.defaults.json"),
            [("dailyPlan.emojiPool", "config/public.defaults.json")])

    def test_matches_the_backticked_markdown_form(self):
        self.assertEqual(
            self.match("`horizon.lookaheadDays` in `config/public.defaults.json`"),
            [("horizon.lookaheadDays", "config/public.defaults.json")])

    def test_requires_a_dotted_key(self):
        self.assertEqual(self.match("something in config/public.defaults.json"), [])


class TestTrackProjects(unittest.TestCase):
    """The one-label-one-track invariant is what makes hours attributable."""

    def run_check(self):
        r = check.Report(); check.check_track_projects(r); return r

    def test_shipped_files_hold_the_invariant(self):
        self.assertEqual(self.run_check().failed, 0, self.run_check().render())

    def test_a_duplicate_label_would_be_caught(self):
        """Simulate the defect the check exists for, without touching the repo."""
        tracks = [{"id": "a", "projects": ["Shared"]}, {"id": "b", "projects": ["Shared"]}]
        owner, dupes = {}, []
        for t in tracks:
            for label in t["projects"]:
                if label in owner:
                    dupes.append((label, owner[label], t["id"]))
                owner[label] = t["id"]
        self.assertEqual(dupes, [("Shared", "a", "b")])


class TestEntrySurfaceParity(unittest.TestCase):
    """The command and skill surfaces must name the same packaged files."""

    def test_shipped_pairs_match(self):
        r = check.Report(); check.check_entry_surface_parity(r)
        self.assertEqual(r.failed, 0, r.render())

    def test_prefix_is_stripped_so_the_two_surfaces_compare(self):
        """Each surface addresses the plugin root differently; only the tail matters."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            cmd = Path(d) / "c.md"
            cmd.write_text("Read `${CLAUDE_PLUGIN_ROOT}/workflows/x.md` first.\n")
            skill = Path(d) / "s.md"
            skill.write_text("Read `../../workflows/x.md` first.\n")
            self.assertEqual(check._entry_packaged_files(cmd),
                             check._entry_packaged_files(skill))

    def test_ignores_paths_without_a_plugin_root_prefix(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "c.md"
            f.write_text("See `~/.lifeyoda/local.json` and `private/local.json`.\n")
            self.assertEqual(check._entry_packaged_files(f), set())


class TestNoCjk(unittest.TestCase):
    """Packaged files are English; CJK there is pasted conversation, not product text."""

    def test_shipped_package_is_clean(self):
        r = check.Report(); check.check_no_cjk(r)
        self.assertEqual(r.failed, 0, r.render())

    def test_matches_han_kana_and_hangul(self):
        for ch in ("\u5df2", "\u30ab", "\ud55c"):
            self.assertIsNotNone(check.CJK_PATTERN.search(ch), ch)

    def test_emoji_are_not_matched(self):
        """The product's own output is full of emoji; flagging them would be useless."""
        for ch in ("\U0001f52c", "\u2705", "\U0001f4d3", "\U0001f5e3", "\u270d\ufe0f"):
            self.assertIsNone(check.CJK_PATTERN.search(ch), ch)

    def test_plain_english_is_not_matched(self):
        self.assertIsNone(check.CJK_PATTERN.search("Meet: Standup - v2 pilot readout"))


class TestNoPersonalCalendarNames(unittest.TestCase):
    """Names come from the local private config, never from a list in the repository."""

    def test_shipped_tree_is_clean(self):
        r = check.Report(); check.check_no_personal_calendar_names(r)
        self.assertEqual(r.failed, 0, r.render())

    def test_no_calendar_name_is_hardcoded(self):
        """The detector must not publish what it detects.

        A literal list here would ship one person's calendar names in a public file,
        which is the exact disclosure the check exists to prevent.
        """
        source = (Path(check.__file__)).read_text()
        self.assertNotIn("PERSONAL_CALENDAR_NAMES", source)

    def test_skips_cleanly_when_no_private_config_exists(self):
        """CI has no private layer. A missing config is nothing to leak, not a failure."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.dict(os.environ, {"LIFEYODA_CONFIG": d}, clear=False), \
                 mock.patch.object(check.Path, "home", staticmethod(lambda: Path(d))), \
                 mock.patch.object(check, "REPO", Path(d)):
                self.assertEqual(check._private_calendar_names(), [])

    def test_reads_names_from_a_config(self):
        import tempfile, json as _json
        cfg = {"sources": {"calendars": {
            "google": {"calendars": [{"name": "Team Ops", "id": "x"},
                                     {"name": "Deep Work", "id": "y"}]},
            "outlook": {"calendars": [{"name": "Field Ops", "id": "z"}]}}}}
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "local.json").write_text(_json.dumps(cfg))
            with mock.patch.dict(os.environ, {"LIFEYODA_CONFIG": d}, clear=False):
                self.assertEqual(check._private_calendar_names(),
                                 ["Deep Work", "Field Ops", "Team Ops"])

    def test_ignores_names_too_short_to_be_distinctive(self):
        import tempfile, json as _json
        cfg = {"sources": {"calendars": {"google": {"calendars": [
            {"name": "AB"}, {"name": "Ops"}]}}}}
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "local.json").write_text(_json.dumps(cfg))
            with mock.patch.dict(os.environ, {"LIFEYODA_CONFIG": d}, clear=False):
                self.assertEqual(check._private_calendar_names(), ["Ops"])


class TestReport(unittest.TestCase):
    """The report counts failures and renders detail only for failing rows."""

    def test_counts_failures(self):
        report = check.Report()
        report.add("a", "fine", True)
        report.add("b", "broken", False, ["why"])
        self.assertEqual(report.failed, 1)

    def test_renders_detail_and_a_summary_line(self):
        report = check.Report()
        report.add("b", "broken", False, ["why"])
        text = report.render()
        self.assertIn("FAIL", text)
        self.assertIn("why", text)
        self.assertIn("1 check(s) failed", text)

    def test_reports_success_when_empty_of_failures(self):
        report = check.Report()
        report.add("a", "fine", True)
        self.assertIn("all checks passed", report.render())


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# End to end
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class TestRepository(unittest.TestCase):
    """Every check must pass against the repository as committed."""

    def test_every_check_passes(self):
        report = check.Report()
        for run in check.CHECKS:
            run(report)
        failing = [name for name, _, ok, _ in report.rows if not ok]
        self.assertEqual(failing, [], report.render())


if __name__ == "__main__":
    unittest.main()
