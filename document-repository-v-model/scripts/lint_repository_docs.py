#!/usr/bin/env python3
"""Lint agent-facing repository documentation without modifying the repository."""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import re
import sys
from collections import defaultdict
from collections.abc import Iterable, Sequence
from pathlib import Path
from urllib.parse import unquote, urlsplit

SPEC_PREFIXES = ("STK", "SYS", "SUB", "CMP")
ACTION_PREFIXES = ("ACC", "SYSV", "INTV", "UNITV")
ALL_PREFIXES = SPEC_PREFIXES + ACTION_PREFIXES
PREFIX_PATTERN = "|".join(sorted(ALL_PREFIXES, key=len, reverse=True))
VALID_ID_RE = re.compile(rf"^(?:{PREFIX_PATTERN})-\d{{3}}$")
VALID_ID_FIND_RE = re.compile(rf"\b(?:{PREFIX_PATTERN})-\d{{3}}\b")
ID_CANDIDATE_RE = re.compile(
    rf"(?<![A-Z0-9])(?:{PREFIX_PATTERN})(?:-[A-Za-z0-9_#?]+|[0-9#?][A-Za-z0-9_#?]*)"
)
HEADING_CANDIDATE_RE = re.compile(
    rf"^(#{{1,6}})\s+((?:{PREFIX_PATTERN})"
    r"(?:-[^\s—–:]+|[0-9#?][^\s—–:]*))(.*)$"
)
FIELD_RE = re.compile(r"^\s*[-*]\s+\*\*([^*]+):\*\*\s*(.*)$")
LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^)\n]+)\s*\)")
REFERENCE_LINK_RE = re.compile(r"^\s*\[[^\]\n]+\]:\s*(<[^>\n]+>|\S+)")
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
PLACEHOLDER_RE = re.compile(
    r"\{\{[^{}\n]+\}\}|<[A-Z][A-Z0-9_ -]{2,}>|\b(?:TODO|TBD|FIXME|CHANGEME)\b"
)

LAYER_ENTRIES = {
    "01-stakeholder-outcomes": "STK",
    "02-system-requirements": "SYS",
    "03-subsystem-contracts": "SUB",
    "04-component-contracts": "CMP",
    "verification": "ACTION",
}
EXPECTED_PARENT = {"STK": None, "SYS": "STK", "SUB": "SYS", "CMP": "SUB"}
EXPECTED_ACTION = {"STK": "ACC", "SYS": "SYSV", "SUB": "INTV", "CMP": "UNITV"}
EXPECTED_SPEC = {value: key for key, value in EXPECTED_ACTION.items()}
METHODS = {"test", "analysis", "inspection", "demonstration"}
STATUSES = {"planned", "implemented", "passing", "failing", "blocked", "waived"}

SPEC_REQUIRED_FIELDS = {
    "normative statement",
    "parents",
    "acceptance criterion",
    "verification",
}
ACTION_REQUIRED_FIELDS = {
    "covers",
    "method",
    "procedure",
    "environment / configuration",
    "pass criterion",
    "status",
    "evidence",
    "nonconformance",
}

SKIPPED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "third_party",
    "dist",
    "build",
    "coverage",
}
BOUNDARY_SKIPPED_DIRS = SKIPPED_DIRS | {
    ".agents",
    "docs",
    "doc",
    "test",
    "tests",
    "fixtures",
    "examples",
    "generated",
    "artifacts",
}
CODE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".ex",
    ".exs",
    ".go",
    ".h",
    ".hpp",
    ".java",
    ".jl",
    ".js",
    ".jsx",
    ".kt",
    ".kts",
    ".lua",
    ".m",
    ".mm",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sh",
    ".swift",
    ".ts",
    ".tsx",
    ".vue",
}
BOUNDARY_MARKERS = {
    "CMakeLists.txt",
    "Cargo.toml",
    "Makefile",
    "Package.swift",
    "go.mod",
    "build.gradle",
    "build.gradle.kts",
    "mix.exs",
    "package.json",
    "pom.xml",
    "Project.toml",
    "pyproject.toml",
    "setup.cfg",
    "setup.py",
}
ARTIFACT_SUFFIXES = {
    ".bin",
    ".csv",
    ".db",
    ".gif",
    ".gz",
    ".html",
    ".jpeg",
    ".jpg",
    ".json",
    ".jsonl",
    ".log",
    ".mp4",
    ".pdf",
    ".png",
    ".sqlite",
    ".svg",
    ".tar",
    ".tsv",
    ".webm",
    ".webp",
    ".xml",
    ".yaml",
    ".yml",
    ".zip",
}
NONE_VALUES = {"", "-", "—", "none", "n/a", "na", "not applicable"}
CONTEXT_NEEDS = {
    "guided learning": "Guided learning",
    "task playbook": "Task playbook",
    "reference": "Reference",
    "explanation": "Explanation",
}
CONTEXT_METADATA_FIELDS = {
    "context need",
    "open when",
    "do not open when",
    "related specification ids",
    "review when",
}
H2_RE = re.compile(r"^\s{0,3}##(?:[ \t]+|$)")
JUSTIFIED_CONTEXT_WITHOUT_SPEC_RE = re.compile(
    r"^none\s+—\s+\S(?:.*\S)?$", re.IGNORECASE
)


class InputError(Exception):
    """Raised when repository input cannot be read safely."""


@dataclasses.dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int | None
    message: str

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }
        if self.line is not None:
            result["line"] = self.line
        return result


@dataclasses.dataclass
class Record:
    identifier: str
    title: str
    path: Path
    line: int
    fields: dict[str, str]
    field_lines: dict[str, int]

    @property
    def prefix(self) -> str:
        return self.identifier.split("-", 1)[0]


@dataclasses.dataclass
class Profile:
    root: Path
    files: set[Path]
    status: str | None


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _normalize_field(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def _clean_scalar(value: str) -> str:
    return value.strip().strip("`*_").strip().lower()


def _is_none(value: str) -> bool:
    return _clean_scalar(value) in NONE_VALUES


def _visible_lines(text: str) -> list[str]:
    result: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if fence is None and marker in {"```", "~~~"}:
            fence = marker
            result.append("")
        elif fence is not None:
            result.append("")
            if stripped.startswith(fence):
                fence = None
        else:
            result.append(line)
    return result


def _normalized_paragraph(block: Sequence[tuple[int, str]]) -> str | None:
    if any(line.lstrip().startswith(("#", "|", "<!--")) for _, line in block):
        return None
    joined = " ".join(line.strip() for _, line in block)
    joined = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", joined)
    joined = re.sub(r"^[\s>*+-]+", "", joined)
    normalized = re.sub(r"[^\w]+", " ", joined.lower()).strip()
    return normalized if len(WORD_RE.findall(normalized)) >= 40 else None


class RepositoryDocsLinter:
    def __init__(self, repository: Path, source_roots: Sequence[Path]) -> None:
        self.repository = repository.resolve()
        self.source_roots = [path.resolve() for path in source_roots]
        self.errors: list[Finding] = []
        self.warnings: list[Finding] = []
        self._finding_keys: set[tuple[str, str, str, int | None, str]] = set()
        self._text_cache: dict[Path, str] = {}
        self.records: list[Record] = []
        self.records_by_id: dict[str, Record] = {}
        self.record_counts: dict[Path, int] = defaultdict(int)
        self.file_categories: dict[Path, str] = {}
        self.profiles: list[Profile] = []

    def _relative(self, path: object) -> str:
        if isinstance(path, Path):
            candidate = path.resolve(strict=False)
            try:
                return candidate.relative_to(self.repository).as_posix() or "."
            except ValueError:
                return str(path)
        return str(path)

    def _add(
        self,
        severity: str,
        code: str,
        path: object,
        message: str,
        line: int | None = None,
    ) -> None:
        relative = self._relative(path)
        key = (severity, code, relative, line, message)
        if key in self._finding_keys:
            return
        self._finding_keys.add(key)
        finding = Finding(severity, code, relative, line, message)
        if severity == "error":
            self.errors.append(finding)
        else:
            self.warnings.append(finding)

    def error(
        self, code: str, path: object, message: str, line: int | None = None
    ) -> None:
        self._add("error", code, path, message, line)

    def warn(
        self, code: str, path: object, message: str, line: int | None = None
    ) -> None:
        self._add("warning", code, path, message, line)

    def _read(self, path: Path) -> str:
        resolved = path.resolve()
        if resolved not in self._text_cache:
            try:
                self._text_cache[resolved] = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                raise InputError(f"cannot read {path}: {exc}") from exc
        return self._text_cache[resolved]

    def run(self) -> None:
        self._check_required_routers()
        document_files = self._document_files()
        self._check_links(document_files)
        self._discover_profiles()
        self._parse_records()
        self._validate_record_locations()
        self._validate_records()
        self._check_context_topics()
        self._check_sizes(document_files)
        self._check_duplicate_paragraphs(document_files)
        self._check_artifacts()
        self._check_boundary_routers()
        self._check_baselined_placeholders()
        self.errors.sort(key=lambda item: (item.path, item.line or 0, item.code))
        self.warnings.sort(key=lambda item: (item.path, item.line or 0, item.code))

    def _check_required_routers(self) -> None:
        required = [
            (
                self.repository / "AGENTS.md",
                "file",
                "missing_root_router",
                "required root AGENTS.md is missing",
            ),
            (
                self.repository / ".agents",
                "directory",
                "missing_agents_directory",
                "required .agents directory is missing",
            ),
            (
                self.repository / ".agents" / "index.md",
                "file",
                "missing_agents_router",
                "required .agents/index.md router is missing",
            ),
            (
                self.repository / ".agents" / "v-model",
                "directory",
                "missing_vmodel_directory",
                "required .agents/v-model directory is missing",
            ),
            (
                self.repository / ".agents" / "v-model" / "index.md",
                "file",
                "missing_vmodel_router",
                "required .agents/v-model/index.md router is missing",
            ),
        ]
        for path, expected_type, code, message in required:
            valid = path.is_file() if expected_type == "file" else path.is_dir()
            if not valid:
                self.error(code, path, message)
        for source_root in self.source_roots:
            router = source_root / "AGENTS.md"
            if not router.is_file():
                self.error(
                    "missing_source_router",
                    router,
                    f"code root {self._relative(source_root)} requires AGENTS.md",
                )

    def _document_files(self) -> list[Path]:
        files: set[Path] = set()
        for directory, names, filenames in os.walk(self.repository, followlinks=False):
            names[:] = [name for name in names if name not in SKIPPED_DIRS]
            if "AGENTS.md" in filenames:
                files.add(Path(directory) / "AGENTS.md")
        agents_directory = self.repository / ".agents"
        if agents_directory.is_dir():
            try:
                files.update(
                    path for path in agents_directory.rglob("*.md") if path.is_file()
                )
            except OSError as exc:
                raise InputError(f"cannot inspect {agents_directory}: {exc}") from exc
        return sorted(files)

    def _check_links(self, files: Iterable[Path]) -> None:
        external_schemes = {"data", "ftp", "http", "https", "mailto", "tel"}
        for path in files:
            lines = _visible_lines(self._read(path))
            for line_number, line in enumerate(lines, 1):
                destinations = [match.group(1) for match in LINK_RE.finditer(line)]
                reference_match = REFERENCE_LINK_RE.match(line)
                if reference_match:
                    destinations.append(reference_match.group(1))
                for raw_destination in destinations:
                    raw = raw_destination.strip()
                    if raw.startswith("<") and raw.endswith(">"):
                        destination = raw[1:-1].strip()
                    else:
                        destination = raw.split(maxsplit=1)[0]
                    if not destination or destination.startswith("#"):
                        continue
                    if destination.startswith("//"):
                        continue
                    try:
                        parsed = urlsplit(destination)
                    except ValueError:
                        self.error(
                            "malformed_link",
                            path,
                            f"cannot parse local link destination {destination!r}",
                            line_number,
                        )
                        continue
                    if parsed.scheme.lower() in external_schemes or parsed.netloc:
                        continue
                    if parsed.scheme and len(parsed.scheme) > 1:
                        continue
                    local_path = unquote(parsed.path)
                    if not local_path:
                        continue
                    if local_path.startswith("/"):
                        candidate = self.repository / local_path.lstrip("/")
                    else:
                        candidate = path.parent / local_path
                    resolved = candidate.resolve(strict=False)
                    if not _is_within(resolved, self.repository):
                        self.error(
                            "escaping_link",
                            path,
                            f"local link escapes the repository: {destination}",
                            line_number,
                        )
                    elif not candidate.exists():
                        self.error(
                            "broken_link",
                            path,
                            f"local link target does not exist: {destination}",
                            line_number,
                        )

    def _discover_profiles(self) -> None:
        vmodel_root = self.repository / ".agents" / "v-model"
        if not vmodel_root.is_dir():
            return
        directories = [vmodel_root]
        try:
            directories.extend(path for path in vmodel_root.rglob("*") if path.is_dir())
        except OSError as exc:
            raise InputError(f"cannot inspect {vmodel_root}: {exc}") from exc
        profile_roots = [
            directory
            for directory in directories
            if any(
                (directory / f"{entry}.md").exists() or (directory / entry).is_dir()
                for entry in LAYER_ENTRIES
            )
        ]
        if not profile_roots:
            self.error(
                "missing_vmodel_profile",
                vmodel_root,
                "no complete V-model profile entries were found",
            )
            return
        for profile_root in sorted(set(profile_roots)):
            files: set[Path] = set()
            index = profile_root / "index.md"
            if not index.is_file():
                self.error(
                    "missing_profile_router",
                    index,
                    "each product profile requires index.md",
                )
            else:
                files.add(index.resolve())
            for entry, category in LAYER_ENTRIES.items():
                file_path = profile_root / f"{entry}.md"
                directory_path = profile_root / entry
                if file_path.exists() and directory_path.exists():
                    self.error(
                        "ambiguous_layer_storage",
                        profile_root,
                        f"use either {entry}.md or {entry}/, not both",
                    )
                if file_path.is_file():
                    resolved = file_path.resolve()
                    files.add(resolved)
                    self.file_categories[resolved] = category
                elif directory_path.is_dir():
                    layer_index = directory_path / "index.md"
                    if not layer_index.is_file():
                        self.error(
                            "missing_layer_router",
                            layer_index,
                            f"sharded layer {entry}/ requires index.md",
                        )
                    else:
                        files.add(layer_index.resolve())
                    try:
                        shards = [
                            path
                            for path in directory_path.rglob("*.md")
                            if path.is_file() and path.name != "index.md"
                        ]
                    except OSError as exc:
                        raise InputError(
                            f"cannot inspect sharded layer {directory_path}: {exc}"
                        ) from exc
                    for shard in shards:
                        resolved = shard.resolve()
                        files.add(resolved)
                        self.file_categories[resolved] = category
                else:
                    self.error(
                        "missing_profile_layer",
                        file_path,
                        f"profile requires {entry}.md or {entry}/",
                    )
            status = self._profile_status(index) if index.is_file() else None
            self.profiles.append(Profile(profile_root.resolve(), files, status))

    def _profile_status(self, index: Path) -> str | None:
        pattern = re.compile(
            r"^\s*[-*]\s+\*\*Profile status:\*\*\s*(.+?)\s*$", re.IGNORECASE
        )
        for line_number, line in enumerate(_visible_lines(self._read(index)), 1):
            match = pattern.match(line)
            if match:
                status = _clean_scalar(match.group(1))
                if status not in {"draft", "baselined"}:
                    self.error(
                        "invalid_profile_status",
                        index,
                        "Profile status must be draft or baselined",
                        line_number,
                    )
                return status
        self.warn(
            "missing_profile_status",
            index,
            "profile index should declare Profile status as draft or baselined",
        )
        return None

    def _parse_records(self) -> None:
        vmodel_root = self.repository / ".agents" / "v-model"
        if not vmodel_root.is_dir():
            return
        try:
            files = sorted(path for path in vmodel_root.rglob("*.md") if path.is_file())
        except OSError as exc:
            raise InputError(f"cannot inspect {vmodel_root}: {exc}") from exc
        for path in files:
            lines = _visible_lines(self._read(path))
            candidates: list[tuple[int, re.Match[str]]] = []
            for index, line in enumerate(lines):
                match = HEADING_CANDIDATE_RE.match(line)
                if match:
                    candidates.append((index, match))
            for candidate_index, (start, match) in enumerate(candidates):
                identifier = match.group(2).rstrip(".,;")
                line_number = start + 1
                if len(match.group(1)) < 2:
                    self.error(
                        "invalid_record_heading_level",
                        path,
                        f"{identifier} must use a level-two or deeper heading",
                        line_number,
                    )
                if not VALID_ID_RE.fullmatch(identifier):
                    self.error(
                        "malformed_id",
                        path,
                        f"malformed record ID {identifier!r}; use PREFIX-###",
                        line_number,
                    )
                    continue
                raw_title = match.group(3) or ""
                title = re.sub(r"^[\s—–:|-]+", "", raw_title).strip()
                if not title:
                    self.error(
                        "missing_record_title",
                        path,
                        f"{identifier} requires a concise title",
                        line_number,
                    )
                end = (
                    candidates[candidate_index + 1][0]
                    if candidate_index + 1 < len(candidates)
                    else len(lines)
                )
                fields, field_lines = self._parse_fields(
                    path, lines[start + 1 : end], start + 2
                )
                record = Record(
                    identifier, title, path.resolve(), line_number, fields, field_lines
                )
                self.records.append(record)
                self.record_counts[path.resolve()] += 1
                if identifier in self.records_by_id:
                    first = self.records_by_id[identifier]
                    first_location = f"{self._relative(first.path)}:{first.line}"
                    self.error(
                        "duplicate_id",
                        path,
                        f"{identifier} duplicates {first_location}",
                        line_number,
                    )
                else:
                    self.records_by_id[identifier] = record

    def _parse_fields(
        self, path: Path, lines: Sequence[str], first_line: int
    ) -> tuple[dict[str, str], dict[str, int]]:
        fields: dict[str, str] = {}
        field_lines: dict[str, int] = {}
        active: str | None = None
        values: list[str] = []

        def flush() -> None:
            nonlocal active, values
            if active is not None:
                fields[active] = " ".join(
                    part.strip() for part in values if part.strip()
                )
            active = None
            values = []

        for offset, line in enumerate(lines):
            line_number = first_line + offset
            match = FIELD_RE.match(line)
            if match:
                flush()
                name = _normalize_field(match.group(1))
                if name in fields or name in field_lines:
                    self.error(
                        "duplicate_field",
                        path,
                        f"record field {match.group(1)!r} appears more than once",
                        line_number,
                    )
                active = name
                field_lines[name] = line_number
                values = [match.group(2)]
            elif not line.strip() or line.lstrip().startswith("#"):
                flush()
            elif active is not None:
                values.append(line)
        flush()
        return fields, field_lines

    def _validate_record_locations(self) -> None:
        for record in self.records:
            category = self.file_categories.get(record.path)
            expected = "ACTION" if record.prefix in ACTION_PREFIXES else record.prefix
            if category is None:
                message = (
                    f"{record.identifier} is outside its canonical layer "
                    "or verification shard"
                )
                self.error(
                    "record_outside_layer",
                    record.path,
                    message,
                    record.line,
                )
            elif category != expected:
                self.error(
                    "record_wrong_layer",
                    record.path,
                    f"{record.identifier} belongs in {expected}, not {category}",
                    record.line,
                )

    def _validate_records(self) -> None:
        specifications = [
            record for record in self.records if record.prefix in SPEC_PREFIXES
        ]
        actions = [
            record for record in self.records if record.prefix in ACTION_PREFIXES
        ]
        spec_verifications: dict[str, dict[str, str]] = {}
        action_coverage: dict[str, set[str]] = {}

        for record in specifications:
            self._require_fields(record, SPEC_REQUIRED_FIELDS)
            self._check_reference_tokens(record, ("parents", "verification"))
            self._validate_parents(record)
            spec_verifications[record.identifier] = self._verification_mappings(record)

        for record in actions:
            self._require_fields(record, ACTION_REQUIRED_FIELDS)
            self._check_reference_tokens(record, ("covers",))
            action_coverage[record.identifier] = self._validate_action(record)

        for spec_id, mappings in spec_verifications.items():
            specification = self.records_by_id.get(spec_id)
            if specification is None:
                continue
            for action_id, declared_method in mappings.items():
                action = self.records_by_id.get(action_id)
                if action is None or action.prefix not in ACTION_PREFIXES:
                    self.error(
                        "unknown_verification_action",
                        specification.path,
                        f"{spec_id} references missing action {action_id}",
                        specification.field_lines.get(
                            "verification", specification.line
                        ),
                    )
                    continue
                if spec_id not in action_coverage.get(action_id, set()):
                    message = (
                        f"{spec_id} lists {action_id}, but {action_id} "
                        f"does not cover {spec_id}"
                    )
                    self.error(
                        "nonbidirectional_trace",
                        specification.path,
                        message,
                        specification.field_lines.get(
                            "verification", specification.line
                        ),
                    )
                action_method = _clean_scalar(action.fields.get("method", ""))
                if action_method in METHODS and declared_method != action_method:
                    self.error(
                        "trace_method_mismatch",
                        specification.path,
                        f"{spec_id} declares {action_id} as {declared_method}, "
                        f"but the action method is {action_method}",
                        specification.field_lines.get(
                            "verification", specification.line
                        ),
                    )

        for action_id, covered_ids in action_coverage.items():
            action = self.records_by_id.get(action_id)
            if action is None:
                continue
            for spec_id in covered_ids:
                specification = self.records_by_id.get(spec_id)
                if specification is None or specification.prefix not in SPEC_PREFIXES:
                    continue
                if action_id not in spec_verifications.get(spec_id, {}):
                    message = (
                        f"{action_id} covers {spec_id}, but {spec_id} "
                        f"does not list {action_id}"
                    )
                    self.error(
                        "nonbidirectional_trace",
                        action.path,
                        message,
                        action.field_lines.get("covers", action.line),
                    )

    def _require_fields(self, record: Record, required: set[str]) -> None:
        for field in sorted(required):
            if field not in record.fields or not record.fields[field].strip():
                self.error(
                    "missing_record_field",
                    record.path,
                    f"{record.identifier} requires field {field!r}",
                    record.line,
                )

    def _check_reference_tokens(
        self, record: Record, field_names: Sequence[str]
    ) -> None:
        for field_name in field_names:
            value = record.fields.get(field_name, "")
            for match in ID_CANDIDATE_RE.finditer(value):
                candidate = match.group(0).rstrip(".,;")
                if not VALID_ID_RE.fullmatch(candidate):
                    self.error(
                        "malformed_id",
                        record.path,
                        f"malformed ID {candidate!r} in {field_name}",
                        record.field_lines.get(field_name, record.line),
                    )

    def _validate_parents(self, record: Record) -> None:
        value = record.fields.get("parents", "")
        parent_ids = VALID_ID_FIND_RE.findall(value)
        expected_prefix = EXPECTED_PARENT[record.prefix]
        if expected_prefix is None:
            if parent_ids or (value and not _is_none(value)):
                message = (
                    f"{record.identifier} is a stakeholder outcome and "
                    "must have Parents: None"
                )
                self.error(
                    "invalid_parent_layer",
                    record.path,
                    message,
                    record.field_lines.get("parents", record.line),
                )
            return
        if not parent_ids:
            self.error(
                "missing_parent",
                record.path,
                f"{record.identifier} requires at least one {expected_prefix} parent",
                record.field_lines.get("parents", record.line),
            )
            return
        for parent_id in parent_ids:
            parent_prefix = parent_id.split("-", 1)[0]
            if parent_prefix != expected_prefix:
                message = (
                    f"{record.identifier} may reference only "
                    f"{expected_prefix} parents, not {parent_id}"
                )
                self.error(
                    "invalid_parent_layer",
                    record.path,
                    message,
                    record.field_lines.get("parents", record.line),
                )
            parent = self.records_by_id.get(parent_id)
            if parent is None or parent.prefix not in SPEC_PREFIXES:
                self.error(
                    "unknown_parent",
                    record.path,
                    f"{record.identifier} references missing parent {parent_id}",
                    record.field_lines.get("parents", record.line),
                )

    def _verification_mappings(self, record: Record) -> dict[str, str]:
        value = record.fields.get("verification", "")
        action_ids = [
            identifier
            for identifier in VALID_ID_FIND_RE.findall(value)
            if identifier.split("-", 1)[0] in ACTION_PREFIXES
        ]
        all_ids = VALID_ID_FIND_RE.findall(value)
        for identifier in all_ids:
            if identifier.split("-", 1)[0] in SPEC_PREFIXES:
                message = (
                    f"{record.identifier} verification field contains "
                    f"specification {identifier}"
                )
                self.error(
                    "invalid_verification_reference",
                    record.path,
                    message,
                    record.field_lines.get("verification", record.line),
                )
        if not action_ids:
            self.error(
                "unmapped_specification",
                record.path,
                f"{record.identifier} has no right-side verification action",
                record.field_lines.get("verification", record.line),
            )
            return {}
        mappings: dict[str, str] = {}
        expected_prefix = EXPECTED_ACTION[record.prefix]
        for action_id in action_ids:
            action_prefix = action_id.split("-", 1)[0]
            if action_prefix != expected_prefix:
                message = (
                    f"{record.identifier} must map to {expected_prefix}, "
                    f"not {action_id}"
                )
                self.error(
                    "invalid_action_layer",
                    record.path,
                    message,
                    record.field_lines.get("verification", record.line),
                )
            method_match = re.search(
                rf"\b{re.escape(action_id)}\s*\(\s*"
                r"(test|analysis|inspection|demonstration)\s*\)",
                value,
                re.IGNORECASE,
            )
            if method_match is None:
                self.error(
                    "missing_mapping_method",
                    record.path,
                    f"{action_id} must include its method in parentheses",
                    record.field_lines.get("verification", record.line),
                )
            else:
                mappings[action_id] = method_match.group(1).lower()
        return mappings

    def _validate_action(self, record: Record) -> set[str]:
        covers_value = record.fields.get("covers", "")
        covered_ids = {
            identifier
            for identifier in VALID_ID_FIND_RE.findall(covers_value)
            if identifier.split("-", 1)[0] in SPEC_PREFIXES
        }
        for identifier in VALID_ID_FIND_RE.findall(covers_value):
            if identifier.split("-", 1)[0] in ACTION_PREFIXES:
                self.error(
                    "invalid_covered_reference",
                    record.path,
                    f"{record.identifier} Covers contains action {identifier}",
                    record.field_lines.get("covers", record.line),
                )
        if not covered_ids:
            self.error(
                "action_without_specification",
                record.path,
                f"{record.identifier} covers no specification",
                record.field_lines.get("covers", record.line),
            )
        expected_spec = EXPECTED_SPEC[record.prefix]
        for spec_id in sorted(covered_ids):
            spec_prefix = spec_id.split("-", 1)[0]
            if spec_prefix != expected_spec:
                message = (
                    f"{record.identifier} may cover only {expected_spec}, not {spec_id}"
                )
                self.error(
                    "invalid_action_layer",
                    record.path,
                    message,
                    record.field_lines.get("covers", record.line),
                )
            specification = self.records_by_id.get(spec_id)
            if specification is None or specification.prefix not in SPEC_PREFIXES:
                self.error(
                    "unknown_covered_specification",
                    record.path,
                    f"{record.identifier} references missing specification {spec_id}",
                    record.field_lines.get("covers", record.line),
                )
        method = _clean_scalar(record.fields.get("method", ""))
        if method not in METHODS:
            methods = ", ".join(sorted(METHODS))
            self.error(
                "invalid_verification_method",
                record.path,
                f"{record.identifier} Method must be one of {methods}",
                record.field_lines.get("method", record.line),
            )
        status = _clean_scalar(record.fields.get("status", ""))
        if status not in STATUSES:
            statuses = ", ".join(sorted(STATUSES))
            self.error(
                "invalid_verification_status",
                record.path,
                f"{record.identifier} Status must be one of {statuses}",
                record.field_lines.get("status", record.line),
            )
        if status == "passing" and not self._durable_evidence(
            record.fields.get("evidence", "")
        ):
            self.error(
                "passing_without_evidence",
                record.path,
                f"{record.identifier} is passing without a durable evidence reference",
                record.field_lines.get("evidence", record.line),
            )
        return covered_ids

    @staticmethod
    def _durable_evidence(value: str) -> bool:
        if _is_none(value) or PLACEHOLDER_RE.search(value):
            return False
        return bool(
            re.search(r"\[[^\]]+\]\([^)]+\)", value)
            or re.search(r"`[^`]+`", value)
            or re.search(r"https?://\S+", value)
            or re.search(
                r"(?:^|\s)(?:artifacts?|docs?|reports?|test|tests|ci)/\S+", value
            )
        )

    def _check_context_topics(self) -> None:
        context_root = self.repository / ".agents" / "context"
        if not context_root.is_dir():
            return
        try:
            topics = [
                path
                for path in context_root.rglob("*.md")
                if path.is_file() and path.name != "index.md"
            ]
        except OSError as exc:
            raise InputError(f"cannot inspect {context_root}: {exc}") from exc
        reachable_topics = self._reachable_context_topics(context_root)
        for topic in sorted(topics):
            lines = _visible_lines(self._read(topic))
            metadata = self._context_metadata(lines)
            self._check_context_metadata(topic, metadata)
            text = "\n".join(lines)
            specification_ids = {
                identifier
                for identifier in VALID_ID_FIND_RE.findall(text)
                if identifier.split("-", 1)[0] in SPEC_PREFIXES
            }
            if not specification_ids and not self._has_justified_missing_specification(
                metadata
            ):
                self.warn(
                    "context_without_specification",
                    topic,
                    "context topic does not link to a specification ID",
                )
            for identifier in sorted(specification_ids):
                record = self.records_by_id.get(identifier)
                if record is None or record.prefix not in SPEC_PREFIXES:
                    self.warn(
                        "context_unknown_specification",
                        topic,
                        f"context topic references missing specification {identifier}",
                    )
            if topic.resolve() not in reachable_topics:
                self.warn(
                    "unreachable_context_topic",
                    topic,
                    "context topic is not reachable from .agents/index.md "
                    "through linked context index files",
                )

    @staticmethod
    def _context_metadata(
        lines: Sequence[str],
    ) -> dict[str, list[tuple[int, str]]]:
        metadata: dict[str, list[tuple[int, str]]] = defaultdict(list)
        for line_number, line in enumerate(lines, 1):
            if H2_RE.match(line):
                break
            match = FIELD_RE.match(line)
            if match is None:
                continue
            name = _normalize_field(match.group(1))
            if name in CONTEXT_METADATA_FIELDS:
                metadata[name].append((line_number, match.group(2).strip()))
        return dict(metadata)

    def _check_context_metadata(
        self,
        topic: Path,
        metadata: dict[str, list[tuple[int, str]]],
    ) -> None:
        need_entries = metadata.get("context need", [])
        nonempty_needs = [
            (line_number, value) for line_number, value in need_entries if value.strip()
        ]
        if not nonempty_needs:
            self.warn(
                "missing_context_need",
                topic,
                "context topic should declare Context need before its first "
                "level-two heading",
                need_entries[0][0] if need_entries else None,
            )
        else:
            line_number, value = nonempty_needs[0]
            normalized = re.sub(
                r"\s+", " ", value.strip().strip("`*_").strip()
            ).casefold()
            if normalized not in CONTEXT_NEEDS:
                choices = ", ".join(CONTEXT_NEEDS.values())
                self.warn(
                    "invalid_context_need",
                    topic,
                    f"Context need must be one of: {choices}",
                    line_number,
                )
        for line_number, _ in need_entries[1:]:
            self.warn(
                "duplicate_context_need",
                topic,
                "Context need appears more than once before the first "
                "level-two heading",
                line_number,
            )

        for field, code, label in (
            ("open when", "missing_context_open_when", "Open when"),
            (
                "do not open when",
                "missing_context_do_not_open_when",
                "Do not open when",
            ),
            (
                "related specification ids",
                "missing_context_related_specification_ids",
                "Related specification IDs",
            ),
            ("review when", "missing_context_review_when", "Review when"),
        ):
            entries = metadata.get(field, [])
            if not any(value.strip() for _, value in entries):
                self.warn(
                    code,
                    topic,
                    f"context topic should declare {label} before its first "
                    "level-two heading",
                    entries[0][0] if entries else None,
                )

    @staticmethod
    def _has_justified_missing_specification(
        metadata: dict[str, list[tuple[int, str]]],
    ) -> bool:
        return any(
            JUSTIFIED_CONTEXT_WITHOUT_SPEC_RE.fullmatch(
                value.strip().strip("`*_").strip()
            )
            is not None
            for _, value in metadata.get("related specification ids", [])
        )

    def _reachable_context_topics(self, context_root: Path) -> set[Path]:
        root_index = self.repository / ".agents" / "index.md"
        if not root_index.is_file():
            return set()
        resolved_context_root = context_root.resolve()
        pending = [(root_index.resolve(), 0)]
        visited_depths: dict[Path, int] = {}
        reachable: set[Path] = set()
        while pending:
            router, depth = pending.pop()
            if depth >= visited_depths.get(router, depth + 1):
                continue
            visited_depths[router] = depth
            context_targets = {
                target
                for target in self._linked_local_files(router)
                if _is_within(target, resolved_context_root)
                and (target.name == "index.md" or target.suffix.lower() == ".md")
            }
            if len(context_targets) > 7:
                self.warn(
                    "context_router_choice_budget",
                    router,
                    f"context index presents {len(context_targets)} choices; "
                    "use at most 7",
                )
            for target in context_targets:
                if target.name == "index.md":
                    next_depth = depth + 1
                    if next_depth > 1:
                        self.warn(
                            "context_router_depth_budget",
                            router,
                            f"context index links to nested router "
                            f"{self._relative(target)} beyond the one-hop budget",
                        )
                    pending.append((target, next_depth))
                else:
                    reachable.add(target)
        return reachable

    def _linked_local_files(self, path: Path) -> set[Path]:
        external_schemes = {"data", "ftp", "http", "https", "mailto", "tel"}
        targets: set[Path] = set()
        for line in _visible_lines(self._read(path)):
            destinations = [match.group(1) for match in LINK_RE.finditer(line)]
            reference_match = REFERENCE_LINK_RE.match(line)
            if reference_match:
                destinations.append(reference_match.group(1))
            for raw_destination in destinations:
                raw = raw_destination.strip()
                if raw.startswith("<") and raw.endswith(">"):
                    destination = raw[1:-1].strip()
                else:
                    destination = raw.split(maxsplit=1)[0]
                if not destination or destination.startswith(("#", "//")):
                    continue
                try:
                    parsed = urlsplit(destination)
                except ValueError:
                    continue
                if parsed.scheme.lower() in external_schemes or parsed.netloc:
                    continue
                if parsed.scheme and len(parsed.scheme) > 1:
                    continue
                local_path = unquote(parsed.path)
                if not local_path:
                    continue
                if local_path.startswith("/"):
                    candidate = self.repository / local_path.lstrip("/")
                else:
                    candidate = path.parent / local_path
                resolved = candidate.resolve(strict=False)
                if _is_within(resolved, self.repository) and candidate.is_file():
                    targets.add(resolved)
        return targets

    def _check_sizes(self, document_files: Iterable[Path]) -> None:
        for path in document_files:
            text = self._read(path)
            line_count = len(text.splitlines())
            word_count = len(WORD_RE.findall(text))
            record_count = self.record_counts.get(path.resolve(), 0)
            if path.resolve() == (self.repository / "AGENTS.md").resolve():
                limits = (100, 700, None, "root AGENTS.md")
            elif path.name == "AGENTS.md":
                limits = (40, 250, None, "nested AGENTS.md")
            elif (
                _is_within(path.resolve(), (self.repository / ".agents").resolve())
                and path.name == "index.md"
            ):
                limits = (100, 600, None, "router index")
            elif _is_within(path.resolve(), (self.repository / ".agents").resolve()):
                limits = (200, 1200, 40, "detail or V-model shard")
            else:
                continue
            line_limit, word_limit, record_limit, label = limits
            exceeded = []
            if line_count > line_limit:
                exceeded.append(f"{line_count} lines > {line_limit}")
            if word_count > word_limit:
                exceeded.append(f"{word_count} words > {word_limit}")
            if record_limit is not None and record_count > record_limit:
                exceeded.append(f"{record_count} records > {record_limit}")
            if exceeded:
                self.warn(
                    "size_budget",
                    path,
                    f"{label} exceeds warning budget: {', '.join(exceeded)}",
                )

    def _check_duplicate_paragraphs(self, document_files: Iterable[Path]) -> None:
        occurrences: dict[str, list[tuple[Path, int]]] = defaultdict(list)
        for path in document_files:
            lines = _visible_lines(self._read(path))
            block: list[tuple[int, str]] = []
            for line_number, line in enumerate(lines + [""], 1):
                if line.strip():
                    block.append((line_number, line))
                elif block:
                    normalized = _normalized_paragraph(block)
                    if normalized is not None:
                        occurrences[normalized].append((path, block[0][0]))
                    block = []
        for locations in occurrences.values():
            unique = {(path.resolve(), line) for path, line in locations}
            if len(unique) < 2:
                continue
            ordered = sorted(unique, key=lambda item: (str(item[0]), item[1]))
            display = ", ".join(
                f"{self._relative(path)}:{line}" for path, line in ordered[:4]
            )
            if len(ordered) > 4:
                display += f", and {len(ordered) - 4} more"
            first_path, first_line = ordered[0]
            message = (
                "identical normalized paragraph of at least 40 words "
                f"appears at {display}"
            )
            self.warn(
                "duplicate_paragraph",
                first_path,
                message,
                first_line,
            )

    def _check_artifacts(self) -> None:
        agents_root = self.repository / ".agents"
        if not agents_root.is_dir():
            return
        try:
            files = [path for path in agents_root.rglob("*") if path.is_file()]
        except OSError as exc:
            raise InputError(f"cannot inspect {agents_root}: {exc}") from exc
        for path in sorted(files):
            try:
                size = path.stat().st_size
            except OSError as exc:
                raise InputError(f"cannot stat {path}: {exc}") from exc
            reasons = []
            if path.suffix.lower() in ARTIFACT_SUFFIXES:
                reasons.append(f"{path.suffix or 'binary'} artifact")
            if size > 256 * 1024:
                reasons.append(f"{size} bytes")
            if reasons:
                self.warn(
                    "non_context_artifact",
                    path,
                    "large or generated artifact under .agents: " + ", ".join(reasons),
                )

    def _check_boundary_routers(self) -> None:
        for source_root in self.source_roots:
            if not source_root.is_dir():
                continue
            for directory, names, filenames in os.walk(source_root, followlinks=False):
                names[:] = [name for name in names if name not in BOUNDARY_SKIPPED_DIRS]
                path = Path(directory)
                try:
                    depth = len(path.relative_to(source_root).parts)
                except ValueError:
                    continue
                if depth > 3:
                    names[:] = []
                    continue
                if path == source_root or "AGENTS.md" in filenames:
                    continue
                direct_code = sum(
                    Path(filename).suffix.lower() in CODE_SUFFIXES
                    for filename in filenames
                )
                child_code_dirs = 0
                for child_name in names:
                    child = path / child_name
                    try:
                        if any(
                            item.is_file() and item.suffix.lower() in CODE_SUFFIXES
                            for item in child.iterdir()
                        ):
                            child_code_dirs += 1
                    except OSError as exc:
                        raise InputError(f"cannot inspect {child}: {exc}") from exc
                has_marker = any(marker in filenames for marker in BOUNDARY_MARKERS)
                appears_meaningful = (
                    (has_marker and (direct_code >= 1 or child_code_dirs >= 1))
                    or (direct_code >= 1 and child_code_dirs >= 2)
                    or child_code_dirs >= 3
                )
                if appears_meaningful:
                    self.warn(
                        "missing_boundary_router",
                        path / "AGENTS.md",
                        f"{self._relative(path)} appears to be a meaningful source "
                        "boundary but has no AGENTS.md",
                    )

    def _check_baselined_placeholders(self) -> None:
        for profile in self.profiles:
            if profile.status != "baselined":
                continue
            for path in sorted(profile.files):
                if not path.is_file():
                    continue
                for line_number, line in enumerate(_visible_lines(self._read(path)), 1):
                    match = PLACEHOLDER_RE.search(line)
                    if match:
                        self.warn(
                            "baselined_placeholder",
                            path,
                            f"baselined profile contains unresolved placeholder "
                            f"{match.group(0)!r}",
                            line_number,
                        )

    def result(self, fail_on_warn: bool) -> dict[str, object]:
        exit_code = 1 if self.errors or (fail_on_warn and self.warnings) else 0
        return {
            "repository": str(self.repository),
            "source_roots": [self._relative(path) for path in self.source_roots],
            "errors": [finding.as_dict() for finding in self.errors],
            "warnings": [finding.as_dict() for finding in self.warnings],
            "summary": {
                "errors": len(self.errors),
                "warnings": len(self.warnings),
                "exit_code": exit_code,
            },
        }


def _resolve_source_roots(repository: Path, values: Sequence[str] | None) -> list[Path]:
    if values is None:
        default = repository / "src"
        if not default.is_dir():
            return []
        resolved = default.resolve()
        if not _is_within(resolved, repository):
            raise InputError("default source root src escapes repository")
        return [resolved]
    roots: list[Path] = []
    seen: set[Path] = set()
    for value in values:
        raw = Path(value)
        candidate = raw if raw.is_absolute() else repository / raw
        resolved = candidate.resolve(strict=False)
        if not _is_within(resolved, repository):
            raise InputError(f"source root escapes repository: {value}")
        if not candidate.is_dir():
            raise InputError(f"source root is not a readable directory: {value}")
        if resolved not in seen:
            seen.add(resolved)
            roots.append(resolved)
    return roots


def _print_human(result: dict[str, object]) -> None:
    print(f"Repository: {result['repository']}")
    for group_name in ("errors", "warnings"):
        findings = result[group_name]
        assert isinstance(findings, list)
        for finding in findings:
            assert isinstance(finding, dict)
            location = str(finding["path"])
            if "line" in finding:
                location += f":{finding['line']}"
            print(
                f"{str(finding['severity']).upper()} "
                f"[{finding['code']}] {location}: {finding['message']}"
            )
    summary = result["summary"]
    assert isinstance(summary, dict)
    print(f"Summary: {summary['errors']} error(s), {summary['warnings']} warning(s)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read-only integrity and size checks for repository agent documentation."
        )
    )
    parser.add_argument("repository", help="repository root to inspect")
    parser.add_argument(
        "--source-root",
        action="append",
        metavar="PATH",
        help="repository-relative code root; repeat for polyglot layouts",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit machine-readable JSON"
    )
    parser.add_argument(
        "--fail-on-warn",
        action="store_true",
        help="return exit status 1 when warnings are present",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    repository = Path(args.repository).expanduser()
    if not repository.is_dir():
        parser.error(f"repository is not a readable directory: {args.repository}")
    repository = repository.resolve()
    try:
        source_roots = _resolve_source_roots(repository, args.source_root)
        linter = RepositoryDocsLinter(repository, source_roots)
        linter.run()
        result = linter.result(args.fail_on_warn)
    except InputError as exc:
        if args.json:
            print(
                json.dumps(
                    {
                        "repository": str(repository),
                        "input_error": str(exc),
                        "summary": {"errors": 0, "warnings": 0, "exit_code": 2},
                    },
                    indent=2,
                    sort_keys=True,
                )
            )
        else:
            print(f"INPUT ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        _print_human(result)
    summary = result["summary"]
    assert isinstance(summary, dict)
    return int(summary["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())
