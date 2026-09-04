#!/usr/bin/env python3
"""check.py — repository checks for LifeYoda, run identically by CI and by hand.

Last Modified: 2026-08-31 18:10, initial version for the v1.0.0 public release.
Inputs:  the repository working tree, plus `git ls-files` for the tracked-file checks
Outputs: a per-check report on stdout; exit 0 when every check passes, 1 otherwise

Workflow:
  - parse every JSON file
  - validate each private.example file against its schema (minimal validator, stdlib only)
  - assert the four version strings agree, and that LICENSE agrees with both plugin.json
  - scan tracked files for personal identifiers and absolute home paths
  - assert no .DS_Store is tracked and that private/ holds only .gitkeep
  - validate command and skill frontmatter
  - resolve every repository path referenced from a markdown file

CAUTION: this file is a build-time check. It is deliberately not part of the shipped
plugin and must never be referenced from a workflow.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Constants
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "lifeyoda"

#: Files whose `version` must all agree.
VERSION_SOURCES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("plugins/lifeyoda/.claude-plugin/plugin.json", ("version",)),
    ("plugins/lifeyoda/.codex-plugin/plugin.json", ("version",)),
    ("plugins/lifeyoda/config/public.defaults.json", ("toolkit", "version")),
    (".claude-plugin/marketplace.json", ("metadata", "version")),
    (".claude-plugin/marketplace.json", ("plugins", "0", "version")),
    (".agents/plugins/marketplace.json", ("plugins", "0", "version")),
)

#: Files declaring an SPDX license id, checked against the LICENSE file's first line.
LICENSE_SOURCES: tuple[str, ...] = (
    "plugins/lifeyoda/.claude-plugin/plugin.json",
    "plugins/lifeyoda/.codex-plugin/plugin.json",
)

#: Config paired with the schema it must satisfy. The demo fixtures are included on
#: purpose: a schema change that would break a user's config breaks the demo first.
EXAMPLE_SCHEMA_PAIRS: tuple[tuple[str, str], ...] = (
    ("plugins/lifeyoda/private.example/local.example.json",
     "plugins/lifeyoda/config/local.schema.json"),
    ("plugins/lifeyoda/private.example/horizon.example.json",
     "plugins/lifeyoda/config/horizon.schema.json"),
    ("plugins/lifeyoda/fixtures/local.json",
     "plugins/lifeyoda/config/local.schema.json"),
    ("plugins/lifeyoda/fixtures/horizon.json",
     "plugins/lifeyoda/config/horizon.schema.json"),
)

#: Personal data that must never reach a tracked file. Each entry is (label, pattern).
PRIVACY_PATTERNS: tuple[tuple[str, str], ...] = (
    ("email address", r"[A-Za-z0-9._%+-]+@(?!example\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ("google calendar id", r"[A-Za-z0-9._%+-]+@group\.calendar\.google\.com"),
    ("absolute home path", r"/Users/[A-Za-z0-9._-]+/"),
    ("notion id", r"\b[0-9a-f]{32}\b"),
    ("uuid", r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
)

#: Files allowed to contain privacy patterns because they define or discuss them.
#: Deliberately empty — no tracked file needs an exemption today. Adding one should be
#: a conscious act, which is exactly what a failing check forces.
PRIVACY_ALLOWLIST: frozenset[str] = frozenset()

#: CJK ranges — Han, kana, Hangul. The shipped product is written in English, so a CJK
#: character in a packaged file is text that leaked in from a conversation rather than
#: text anyone wrote for a user. Emoji sit far outside these ranges and are core to the
#: product's output, so they are deliberately not matched here.
CJK_PATTERN = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af]")

#: Frontmatter keys every command file must declare.
COMMAND_REQUIRED_KEYS: frozenset[str] = frozenset({"description"})

#: Frontmatter keys every skill file must declare.
SKILL_REQUIRED_KEYS: frozenset[str] = frozenset({"name", "description"})

#: A backticked string is treated as a repository path only if it ends in one of these.
PATH_SUFFIXES: tuple[str, ...] = (".md", ".json", ".py", ".yml", ".yaml")

#: "someKey.path in some/file.json" — a prose reference to a key in a shipped JSON file.
#: This shape is checked because a wrong key here fails silently at run time: the workflow
#: looks for a setting that is not there and carries on with a default.
#: Matches both the markdown form (`a.b` in `x.json`) and the bare form used inside JSON
#: string values (a.b in x.json), because the reference that actually broke was the latter.
KEY_REFERENCE = re.compile(
    r"`?([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)+)`?"
    r"\s+in\s+"
    r"`?((?:[\w.-]+/)*[\w.-]+\.json)`?"
)

#: Backticked strings that look like paths but are not repository paths.
#: `private/` is the tier-3 runtime config location: gitignored, absent by design.
PATH_IGNORE_PREFIXES: tuple[str, ...] = ("~", "$", "/", "http", "private/")

TICKED = re.compile(r"`([^`\n]+)`")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Result plumbing
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


class Report:
    """Collects one line per check plus any failure detail beneath it."""

    def __init__(self) -> None:
        self.rows: list[tuple[str, str, bool, list[str]]] = []

    def add(self, name: str, summary: str, ok: bool, detail: Iterable[str] = ()) -> None:
        """Record one check.

        Args:
            name: short check name, printed in the left column.
            summary: one-line result, printed in the middle column.
            ok: whether the check passed.
            detail: lines printed beneath a failing check.
        """
        self.rows.append((name, summary, ok, list(detail)))

    @property
    def failed(self) -> int:
        """Number of failing checks."""
        return sum(1 for _, _, ok, _ in self.rows if not ok)

    def render(self) -> str:
        """Return the full report as text."""
        width = max((len(n) for n, _, _, _ in self.rows), default=0)
        out: list[str] = []
        for name, summary, ok, detail in self.rows:
            out.append(f"{name:<{width}}  {summary:<28}  {'OK' if ok else 'FAIL'}")
            out.extend(f"{'':<{width}}    {line}" for line in detail)
        out.append("")
        out.append("all checks passed" if self.failed == 0
                   else f"{self.failed} check(s) failed")
        return "\n".join(out)


# .............................................................................
# Repository helpers
# .............................................................................


def tracked_files() -> list[str]:
    """Return every path git would publish, repo-relative.

    This is the tracked set plus files that are new but not gitignored. A check that
    ignored new work would stay green right up until the commit that breaks it, which
    is precisely when it needs to fail.

    Falls back to a filesystem walk when git is unavailable, so the script still runs
    inside an exported tree.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "ls-files", "--cached", "--others",
             "--exclude-standard"],
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return [str(p.relative_to(REPO)) for p in REPO.rglob("*")
                if p.is_file() and ".git" not in p.parts]
    # --cached and --others can both list a path; dict.fromkeys keeps order and dedupes.
    return list(dict.fromkeys(line for line in out.splitlines() if line))


def json_files() -> Iterator[Path]:
    """Yield every tracked JSON file as an absolute path."""
    for rel in tracked_files():
        if rel.endswith(".json"):
            yield REPO / rel


def dig(data: Any, path: tuple[str, ...]) -> Any:
    """Walk a nested structure by key, treating digit segments as list indices.

    Raises:
        KeyError: when the path does not resolve.
    """
    node = data
    for key in path:
        node = node[int(key)] if isinstance(node, list) else node[key]
    return node


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Minimal JSON Schema validator
#
# Supports only the keywords these schemas use: type, properties, required,
# additionalProperties, items, enum, $ref into $defs, minimum, maximum. Anything
# else is ignored rather than silently treated as a pass of something stricter.
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

_TYPES: dict[str, type | tuple[type, ...]] = {
    "object": dict, "array": list, "string": str,
    "integer": int, "number": (int, float), "boolean": bool,
}


def validate(instance: Any, schema: dict, root: dict, where: str = "") -> list[str]:
    """Validate `instance` against `schema`, returning a list of error strings.

    Args:
        instance: the parsed JSON value under test.
        schema: the (sub)schema to apply.
        root: the top-level schema document, used to resolve `$ref`.
        where: dotted path to `instance`, used in error messages.

    Returns:
        Zero or more human-readable error strings.
    """
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/"):
            return [f"{where or '<root>'}: unsupported $ref {ref}"]
        target: Any = root
        for part in ref[2:].split("/"):
            target = target[part]
        return validate(instance, target, root, where)

    errors: list[str] = []
    loc = where or "<root>"

    expected = schema.get("type")
    if expected:
        py = _TYPES.get(expected)
        # bool is a subclass of int in Python; JSON Schema treats them as distinct.
        bad_bool = expected in {"integer", "number"} and isinstance(instance, bool)
        if py is not None and (not isinstance(instance, py) or bad_bool):
            return [f"{loc}: expected {expected}, got {type(instance).__name__}"]

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{loc}: {instance!r} not one of {schema['enum']}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if "minimum" in schema and instance < schema["minimum"]:
            errors.append(f"{loc}: {instance} below minimum {schema['minimum']}")
        if "maximum" in schema and instance > schema["maximum"]:
            errors.append(f"{loc}: {instance} above maximum {schema['maximum']}")

    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{loc}: missing required property {key!r}")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errors.append(f"{loc}: unexpected property {key!r}")
        for key, value in instance.items():
            if key in props:
                errors += validate(value, props[key], root, f"{loc}.{key}")

    if isinstance(instance, list) and "items" in schema:
        for i, value in enumerate(instance):
            errors += validate(value, schema["items"], root, f"{loc}[{i}]")

    return errors


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Checks
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def check_json_syntax(report: Report) -> None:
    """Every tracked JSON file must parse."""
    bad: list[str] = []
    total = 0
    for path in json_files():
        total += 1
        try:
            json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            bad.append(f"{path.relative_to(REPO)}: {exc}")
    report.add("JSON syntax", f"{total - len(bad)}/{total} parse", not bad, bad)


def check_example_against_schema(report: Report) -> None:
    """Each shipped example config must satisfy its schema."""
    errors: list[str] = []
    passed = 0
    for example_rel, schema_rel in EXAMPLE_SCHEMA_PAIRS:
        example, schema_path = REPO / example_rel, REPO / schema_rel
        if not example.exists() or not schema_path.exists():
            errors.append(f"missing: {example_rel} or {schema_rel}")
            continue
        schema = json.loads(schema_path.read_text())
        found = validate(json.loads(example.read_text()), schema, schema)
        if found:
            errors += [f"{example_rel} {e}" for e in found]
        else:
            passed += 1
    total = len(EXAMPLE_SCHEMA_PAIRS)
    report.add("example vs schema", f"{passed}/{total} valid", not errors, errors)


def check_versions(report: Report) -> None:
    """All version strings must agree."""
    seen: dict[str, list[str]] = {}
    missing: list[str] = []
    for rel, path in VERSION_SOURCES:
        file = REPO / rel
        if not file.exists():
            missing.append(f"{rel}: file not found")
            continue
        try:
            value = str(dig(json.loads(file.read_text()), path))
        except (KeyError, IndexError, TypeError):
            missing.append(f"{rel}: no {'.'.join(path)}")
            continue
        seen.setdefault(value, []).append(f"{rel} ({'.'.join(path)})")
    detail = missing + ([] if len(seen) <= 1 else
                        [f"{v}: {', '.join(files)}" for v, files in sorted(seen.items())])
    version = next(iter(seen), "?")
    total = len(VERSION_SOURCES)
    report.add("version consistency",
               f"{total - len(missing)}/{total} agree  {version}",
               not detail, detail)


def check_license(report: Report) -> None:
    """LICENSE and every declared SPDX id must name the same license."""
    license_file = REPO / "LICENSE"
    if not license_file.exists():
        report.add("license consistency", "LICENSE missing", False)
        return
    first = license_file.read_text().splitlines()[0].strip()
    name = first.removesuffix(" License").strip() or first
    detail = [f"LICENSE reads {first!r}, not a recognised license"] if "License" not in first else []
    agreeing = 0
    for rel in LICENSE_SOURCES:
        declared = json.loads((REPO / rel).read_text()).get("license")
        if declared == name:
            agreeing += 1
        else:
            detail.append(f"{rel}: declares {declared!r}, LICENSE says {name!r}")
    total = len(LICENSE_SOURCES) + 1
    report.add("license consistency", f"{agreeing + 1}/{total} agree  {name}",
               not detail, detail)


def check_privacy(report: Report) -> None:
    """No tracked file may carry personal identifiers or an absolute home path."""
    hits: list[str] = []
    compiled = [(label, re.compile(pattern)) for label, pattern in PRIVACY_PATTERNS]
    for rel in tracked_files():
        if rel in PRIVACY_ALLOWLIST:
            continue
        path = REPO / rel
        try:
            text = path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for label, pattern in compiled:
                match = pattern.search(line)
                if match:
                    hits.append(f"{rel}:{lineno} {label}: {match.group(0)}")
    report.add("privacy scan", f"{len(hits)} hits", not hits, hits[:20])


def check_no_cjk(report: Report) -> None:
    """Packaged files must not carry CJK text.

    A workflow is read aloud by an English-language agent for an English-language user.
    CJK characters in one mean a phrase from a working conversation was pasted into the
    product, which is how a private calendar name reached five packaged files once.
    """
    hits: list[str] = []
    for rel in tracked_files():
        if not rel.startswith("plugins/"):
            continue
        try:
            text = (REPO / rel).read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            match = CJK_PATTERN.search(line)
            if match:
                hits.append(f"{rel}:{lineno} CJK: {match.group(0)}")
    report.add("no CJK in package", f"{len(hits)} hits", not hits, hits[:20])


def _private_calendar_names() -> list[str]:
    """Calendar and database names taken from whatever private config exists locally.

    Nothing is hardcoded. Listing a real calendar name in this file would publish the
    very thing the check exists to keep unpublished, and it would only ever cover one
    person's setup. Read at run time, the check protects whoever is running it.
    """
    names: list[str] = []
    for base in (os.environ.get("LIFEYODA_CONFIG"), Path.home() / ".lifeyoda",
                 REPO / "private"):
        if not base:
            continue
        config = Path(base) / "local.json"
        try:
            data = json.loads(config.read_text())
        except (OSError, ValueError):
            continue
        providers = (data.get("sources", {}) or {}).get("calendars", {}) or {}
        for entry in providers.values():
            if not isinstance(entry, dict):
                continue
            for calendar in entry.get("calendars", []) or []:
                name = calendar.get("name") if isinstance(calendar, dict) else None
                if isinstance(name, str) and len(name) >= 3:
                    names.append(name)
        break
    return sorted(set(names))


def check_no_personal_calendar_names(report: Report) -> None:
    """No tracked file may name a calendar from the local private config.

    This is the net that a hardcoded string list cannot be: it needs no maintenance,
    it covers a calendar added tomorrow, and it publishes nothing. Where no private
    config exists — CI, a fresh clone — there is nothing to leak and the check says so.
    """
    names = _private_calendar_names()
    if not names:
        report.add("no personal calendars", "no private config; skipped", True, [])
        return
    pattern = re.compile(r"\b(" + "|".join(re.escape(n) for n in names) + r")\b",
                         re.IGNORECASE)
    hits: list[str] = []
    for rel in tracked_files():
        if rel == "scripts/check.py":
            continue
        try:
            text = (REPO / rel).read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            match = pattern.search(line)
            if match:
                hits.append(f"{rel}:{lineno} private calendar name: {match.group(0)}")
    report.add("no personal calendars", f"{len(names)} name(s) checked, {len(hits)} hits",
               not hits, hits[:20])


def check_ds_store(report: Report) -> None:
    """No .DS_Store may be tracked."""
    hits = [rel for rel in tracked_files() if Path(rel).name == ".DS_Store"]
    report.add(".DS_Store", f"{len(hits)} tracked", not hits, hits)


def check_private_dir(report: Report) -> None:
    """Only .gitkeep may be tracked under private/."""
    hits = [rel for rel in tracked_files() if rel.startswith("private/")]
    unexpected = [rel for rel in hits if rel != "private/.gitkeep"]
    report.add("private/ tracked", f"{len(hits)} file(s)", not unexpected, unexpected)


def _frontmatter(path: Path) -> dict[str, str] | None:
    """Parse a markdown file's YAML frontmatter as flat key/value pairs.

    Returns:
        A dict of top-level scalar keys, or None when there is no frontmatter block.
    """
    match = FRONTMATTER.match(path.read_text())
    if not match:
        return None
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "-")) or ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def _check_frontmatter(report: Report, name: str, paths: list[Path],
                       required: frozenset[str]) -> None:
    """Assert every file in `paths` declares `required` frontmatter keys."""
    detail: list[str] = []
    good = 0
    for path in sorted(paths):
        fields = _frontmatter(path)
        rel = path.relative_to(REPO)
        if fields is None:
            detail.append(f"{rel}: no frontmatter block")
            continue
        missing = sorted(required - fields.keys())
        if missing:
            detail.append(f"{rel}: missing {', '.join(missing)}")
        else:
            good += 1
    report.add(name, f"{good}/{len(paths)} valid", not detail, detail)


def check_command_frontmatter(report: Report) -> None:
    """Every Claude Code command file must declare a description."""
    _check_frontmatter(report, "command frontmatter",
                       list((PLUGIN / "commands").glob("*.md")), COMMAND_REQUIRED_KEYS)


def check_skill_frontmatter(report: Report) -> None:
    """Every Codex skill file must declare a name and description."""
    _check_frontmatter(report, "skill frontmatter",
                       list((PLUGIN / "codex-skills").glob("*/SKILL.md")), SKILL_REQUIRED_KEYS)


def _resolves(ref: str, source: Path) -> bool:
    """Whether a referenced repository path exists.

    A reference resolves if it is found relative to the referring file's directory,
    the repository root, or the plugin root. A `../../` reference from a command file
    is additionally tried from a skill directory, which is the depth those fallbacks
    are written for.
    """
    bases = [source.parent, REPO, PLUGIN]
    if ref.startswith("../../"):
        # Fallbacks in command files are written for a skill at <plugin>/codex-skills/<name>/.
        bases.append(PLUGIN / "codex-skills" / "any-skill")
    # normpath rather than Path.exists so `..` collapses textually; the intermediate
    # directory of a hypothetical skill does not have to exist on disk.
    return any(os.path.exists(os.path.normpath(base / ref)) for base in bases)


def check_cross_references(report: Report) -> None:
    """Every repository path named in a markdown file must exist."""
    broken: list[str] = []
    checked = 0
    for rel in tracked_files():
        if not rel.endswith(".md"):
            continue
        path = REPO / rel
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            for ref in TICKED.findall(line):
                ref = ref.strip()
                if (not ref.endswith(PATH_SUFFIXES)
                        or "/" not in ref
                        or " " in ref
                        or "*" in ref
                        or ref.startswith(PATH_IGNORE_PREFIXES)):
                    continue
                checked += 1
                if not _resolves(ref, path):
                    broken.append(f"{rel}:{lineno} -> {ref}")
    report.add("cross-file refs", f"{checked - len(broken)}/{checked} resolve",
               not broken, broken)


def check_fixtures(report: Report) -> None:
    """Demo fixtures, once present, must be parseable JSON."""
    fixtures = PLUGIN / "fixtures"
    if not fixtures.is_dir():
        report.add("fixtures", "not present yet", True)
        return
    files = sorted(fixtures.glob("*.json"))
    bad: list[str] = []
    for path in files:
        try:
            json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            bad.append(f"{path.relative_to(REPO)}: {exc}")
    report.add("fixtures", f"{len(files) - len(bad)}/{len(files)} parse", not bad, bad)


def _json_string_paths(data: Any) -> Iterator[str]:
    """Yield every string in a JSON document that looks like a repository path."""
    if isinstance(data, dict):
        for value in data.values():
            yield from _json_string_paths(value)
    elif isinstance(data, list):
        for value in data:
            yield from _json_string_paths(value)
    elif isinstance(data, str):
        if ("/" in data and " " not in data and data.endswith(PATH_SUFFIXES)
                and not data.startswith(PATH_IGNORE_PREFIXES)):
            yield data


#: Paths inside these directories describe an imaginary user's machine, not this repository.
JSON_PATH_EXEMPT: tuple[str, ...] = ("plugins/lifeyoda/fixtures/",)


def check_json_path_references(report: Report) -> None:
    """A path embedded in a JSON value must exist, the same as one named in a document.

    Fixtures are exempt: they stand in for someone else's repository, so a file named in
    one is expected not to exist here.
    """
    broken: list[str] = []
    checked = 0
    for path in json_files():
        if str(path.relative_to(REPO)).startswith(JSON_PATH_EXEMPT):
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue  # already reported by check_json_syntax
        for ref in _json_string_paths(data):
            checked += 1
            if not _resolves(ref, path):
                broken.append(f"{path.relative_to(REPO)} -> {ref}")
    report.add("json path refs", f"{checked - len(broken)}/{checked} resolve",
               not broken, broken)


def check_config_key_references(report: Report) -> None:
    """A key named as living in a shipped JSON file must actually be there.

    Catches the failure mode where prose points at `a.b in config/x.json` and the key is
    spelled differently in the file. Nothing errors at run time; the setting is simply
    never found.
    """
    broken: list[str] = []
    checked = 0
    cache: dict[Path, Any] = {}
    for rel in tracked_files():
        if not rel.endswith((".md", ".json")):
            continue
        source = REPO / rel
        try:
            text = source.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for dotted, target in KEY_REFERENCE.findall(line):
                resolved = next((c for c in (source.parent / target, REPO / target,
                                             PLUGIN / target) if c.exists()), None)
                if resolved is None:
                    continue  # the path check owns missing files
                checked += 1
                if resolved not in cache:
                    try:
                        cache[resolved] = json.loads(resolved.read_text())
                    except json.JSONDecodeError:
                        cache[resolved] = None
                data = cache[resolved]
                node: Any = data
                for part in dotted.split("."):
                    node = node.get(part) if isinstance(node, dict) else None
                    if node is None:
                        broken.append(f"{rel}:{lineno} -> {dotted} not in {target}")
                        break
    report.add("config key refs", f"{checked - len(broken)}/{checked} resolve",
               not broken, broken)


def check_track_projects(report: Report) -> None:
    """A project label may belong to exactly one horizon track.

    Attribution runs project to track: a day's `Projects Touched` decides which track its
    hours land in. A label claimed by two tracks makes that day unassignable, and nothing
    at run time would say so — the hours would simply be counted twice or dropped.
    """
    detail: list[str] = []
    checked = 0
    for rel in ("plugins/lifeyoda/fixtures/horizon.json",
                "plugins/lifeyoda/private.example/horizon.example.json"):
        path = REPO / rel
        if not path.exists():
            continue
        try:
            tracks = json.loads(path.read_text()).get("tracks", [])
        except json.JSONDecodeError:
            continue
        owner: dict[str, str] = {}
        for track in tracks:
            checked += 1
            for label in track.get("projects", []):
                if label in owner:
                    detail.append(
                        f"{rel}: project {label!r} claimed by both "
                        f"{owner[label]!r} and {track.get('id')!r}")
                owner[label] = track.get("id", "?")
    report.add("track projects", f"{checked} track(s) checked", not detail, detail)


#: Packaged files an entry file may name without its counterpart naming the same one.
#: Each surface addresses the plugin root differently, so the prefixes differ by design.
ENTRY_PREFIXES: tuple[str, ...] = ("${CLAUDE_PLUGIN_ROOT}/", "../../")


def _entry_packaged_files(path: Path) -> set[str]:
    """Return the packaged files an entry file tells the agent to read.

    Both surfaces name the same file through different prefixes, so the prefix is
    stripped and only the plugin-relative path is compared.
    """
    found: set[str] = set()
    for ref in TICKED.findall(path.read_text()):
        ref = ref.strip()
        for prefix in ENTRY_PREFIXES:
            if ref.startswith(prefix) and ref.endswith(PATH_SUFFIXES):
                found.add(ref[len(prefix):])
    return found


def check_entry_surface_parity(report: Report) -> None:
    """A command and its skill must name the same packaged files.

    The two surfaces are hand-written, and they have drifted before: the skills read
    templates the commands never mentioned, which is enough to make the same workflow
    produce different output under each runtime. Anything either surface needs belongs
    in the workflow's own Inputs section, so both reach it by reading one file.
    """
    detail: list[str] = []
    checked = 0
    for command in sorted((PLUGIN / "commands").glob("*.md")):
        skill = PLUGIN / "codex-skills" / command.stem / "SKILL.md"
        if not skill.exists():
            detail.append(f"commands/{command.name}: no matching skill")
            continue
        checked += 1
        only_cmd = _entry_packaged_files(command) - _entry_packaged_files(skill)
        only_skill = _entry_packaged_files(skill) - _entry_packaged_files(command)
        for ref in sorted(only_cmd):
            detail.append(f"{command.stem}: command reads {ref}, skill does not")
        for ref in sorted(only_skill):
            detail.append(f"{command.stem}: skill reads {ref}, command does not")
    report.add("entry surface parity", f"{checked} pair(s) match", not detail, detail)


CHECKS: tuple[Callable[[Report], None], ...] = (
    check_json_syntax,
    check_example_against_schema,
    check_versions,
    check_license,
    check_privacy,
    check_no_cjk,
    check_no_personal_calendar_names,
    check_ds_store,
    check_private_dir,
    check_command_frontmatter,
    check_skill_frontmatter,
    check_entry_surface_parity,
    check_cross_references,
    check_json_path_references,
    check_config_key_references,
    check_track_projects,
    check_fixtures,
)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#
# Entry point
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def main() -> int:
    """Run every check and print the report.

    Returns:
        0 when all checks pass, 1 otherwise.
    """
    report = Report()
    for check in CHECKS:
        check(report)
    print(report.render())
    return 1 if report.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
