#!/usr/bin/env python3
"""Regression tests for V-model lifecycle modes."""

from __future__ import annotations

import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path

SCRIPT_DIRECTORY = Path(__file__).resolve().parent
if str(SCRIPT_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIRECTORY))

from lint_repository_docs import RepositoryDocsLinter, build_parser


class RepositoryDocsLinterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.repository = Path(self.temporary_directory.name)
        self._write("AGENTS.md", "# Repository Guidance\n")
        self._write(
            ".agents/index.md",
            "# Agent Context\n\n"
            "- [Overview](context/overview.md) — open for repository facts.\n",
        )
        self._write(
            ".agents/context/overview.md",
            "# Overview\n\n"
            "- **Context need:** Reference\n"
            "- **Open when:** Looking up repository facts.\n"
            "- **Do not open when:** No repository context is needed.\n"
            "- **Review when:** Repository structure changes.\n"
            "- **Known gaps:** None\n\n"
            "## Facts\n\n"
            "The fixture has durable agent documentation.\n",
        )

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def _write(self, relative_path: str, content: str) -> None:
        path = self.repository / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def _lint(self, state: str) -> RepositoryDocsLinter:
        linter = RepositoryDocsLinter(self.repository, [], state)
        linter.run()
        return linter

    def _add_complete_vmodel(self) -> None:
        index = self.repository / ".agents/index.md"
        index.write_text(
            index.read_text(encoding="utf-8")
            + "- [Active design](v-model/index.md) — open during the active task.\n",
            encoding="utf-8",
        )
        self._write(
            ".agents/v-model/index.md",
            "# Product V-Model\n\n"
            "- **Profile status:** draft\n\n"
            "1. [Stakeholder outcomes](01-stakeholder-outcomes.md)\n"
            "2. [System requirements](02-system-requirements.md)\n"
            "3. [Subsystem contracts](03-subsystem-contracts.md)\n"
            "4. [Component contracts](04-component-contracts.md)\n"
            "5. [Verification](verification.md)\n",
        )
        specifications = {
            "01-stakeholder-outcomes.md": (
                "STK-001",
                "None",
                "ACC-001 (demonstration)",
            ),
            "02-system-requirements.md": ("SYS-001", "STK-001", "SYSV-001 (test)"),
            "03-subsystem-contracts.md": ("SUB-001", "SYS-001", "INTV-001 (test)"),
            "04-component-contracts.md": ("CMP-001", "SUB-001", "UNITV-001 (analysis)"),
        }
        for filename, (identifier, parents, verification) in specifications.items():
            self._write(
                f".agents/v-model/{filename}",
                f"# Layer\n\n## {identifier} — Requirement\n\n"
                "- **Normative statement:** The product shall behave as specified.\n"
                f"- **Parents:** {parents}\n"
                "- **Acceptance criterion:** The stated behavior is observed.\n"
                f"- **Verification:** {verification}\n",
            )

        actions = (
            ("ACC-001", "STK-001", "demonstration"),
            ("SYSV-001", "SYS-001", "test"),
            ("INTV-001", "SUB-001", "test"),
            ("UNITV-001", "CMP-001", "analysis"),
        )
        records = ["# Verification\n"]
        for action, specification, method in actions:
            records.append(
                f"## {action} — Check\n\n"
                f"- **Covers:** {specification}\n"
                f"- **Method:** {method}\n"
                "- **Procedure:** Exercise the requirement.\n"
                "- **Environment / configuration:** Test fixture.\n"
                "- **Pass criterion:** The requirement is satisfied.\n"
                "- **Status:** planned\n"
                "- **Evidence:** None\n"
                "- **Nonconformance:** None\n"
            )
        self._write(".agents/v-model/verification.md", "\n".join(records))

    def test_absent_mode_accepts_durable_docs_without_vmodel(self) -> None:
        linter = self._lint("absent")

        self.assertEqual([], linter.errors)
        self.assertEqual([], linter.warnings)

    def test_active_mode_requires_vmodel(self) -> None:
        linter = self._lint("active")

        self.assertEqual(
            {"missing_vmodel_directory", "missing_vmodel_router"},
            {finding.code for finding in linter.errors},
        )

    def test_active_mode_validates_complete_vmodel(self) -> None:
        self._add_complete_vmodel()

        linter = self._lint("active")

        self.assertEqual([], linter.errors)
        self.assertEqual([], linter.warnings)

    def test_active_mode_rejects_empty_profile_layers(self) -> None:
        self._add_complete_vmodel()
        for filename in (
            "01-stakeholder-outcomes.md",
            "02-system-requirements.md",
            "03-subsystem-contracts.md",
            "04-component-contracts.md",
            "verification.md",
        ):
            self._write(f".agents/v-model/{filename}", "# Empty layer\n")

        linter = self._lint("active")

        self.assertEqual(
            ["empty_profile_layer"] * 5,
            [finding.code for finding in linter.errors],
        )

    def test_active_mode_requires_vmodel_route(self) -> None:
        self._add_complete_vmodel()
        index = self.repository / ".agents/index.md"
        index.write_text(
            "\n".join(
                line
                for line in index.read_text(encoding="utf-8").splitlines()
                if "v-model/index.md" not in line
            )
            + "\n",
            encoding="utf-8",
        )

        linter = self._lint("active")

        self.assertEqual(
            ["unrouted_vmodel"],
            [finding.code for finding in linter.errors],
        )

    def test_active_mode_requires_layer_routes(self) -> None:
        self._add_complete_vmodel()
        index = self.repository / ".agents/v-model/index.md"
        index.write_text(
            "\n".join(
                line
                for line in index.read_text(encoding="utf-8").splitlines()
                if "verification.md" not in line
            )
            + "\n",
            encoding="utf-8",
        )

        linter = self._lint("active")

        self.assertEqual(
            ["unrouted_profile_layer"],
            [finding.code for finding in linter.errors],
        )

    def test_active_mode_requires_shard_routes(self) -> None:
        self._add_complete_vmodel()
        layer_file = self.repository / ".agents/v-model/03-subsystem-contracts.md"
        layer_content = layer_file.read_text(encoding="utf-8")
        layer_file.unlink()
        self._write(
            ".agents/v-model/03-subsystem-contracts/index.md",
            "# Subsystem contracts\n",
        )
        self._write(
            ".agents/v-model/03-subsystem-contracts/storage.md",
            layer_content,
        )
        index = self.repository / ".agents/v-model/index.md"
        index.write_text(
            index.read_text(encoding="utf-8").replace(
                "03-subsystem-contracts.md",
                "03-subsystem-contracts/index.md",
            ),
            encoding="utf-8",
        )

        linter = self._lint("active")

        self.assertEqual(
            ["unrouted_layer_shard"],
            [finding.code for finding in linter.errors],
        )

    def test_cli_requires_explicit_vmodel_state(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as raised:
            build_parser().parse_args([str(self.repository)])

        self.assertEqual(2, raised.exception.code)

    def test_absent_mode_rejects_retained_vmodel(self) -> None:
        self._add_complete_vmodel()

        linter = self._lint("absent")

        self.assertEqual(
            ["stale_vmodel_link", "unexpected_vmodel"],
            [finding.code for finding in linter.errors],
        )

    def test_absent_mode_flags_possible_orphaned_ids(self) -> None:
        path = self.repository / ".agents/context/overview.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "- **Known gaps:** None", "- **Known gaps:** Finish SYS-001"
            ),
            encoding="utf-8",
        )

        linter = self._lint("absent")

        self.assertEqual([], linter.errors)
        self.assertEqual(
            ["possible_stale_vmodel_id"],
            [finding.code for finding in linter.warnings],
        )

    def test_absent_mode_checks_repository_markdown(self) -> None:
        self._write(
            "docs/design.md",
            "# Design\n\n"
            "Finish SYS-001, then read [the model](../.agents/v-model/index.md).\n",
        )

        linter = self._lint("absent")

        self.assertEqual(
            ["stale_vmodel_id", "stale_vmodel_link"],
            [finding.code for finding in linter.errors],
        )

    def test_absent_mode_ignores_unrelated_ids_in_regular_docs(self) -> None:
        self._write(
            "docs/issues.md",
            "# External issues\n\nTrack SYS-001, CMP-123, and ACC-001 here.\n",
        )

        linter = self._lint("absent")

        self.assertEqual([], linter.errors)
        self.assertEqual([], linter.warnings)

    def test_absent_mode_does_not_reject_ambiguous_ids(self) -> None:
        self._write(
            "docs/issues.md",
            "# V-model alternatives\n\nTrack unrelated ticket SYS-001 here.\n",
        )

        linter = self._lint("absent")

        self.assertEqual([], linter.errors)
        self.assertEqual(
            ["possible_stale_vmodel_id"],
            [finding.code for finding in linter.warnings],
        )

    def test_absent_mode_warns_about_vmodel_metadata(self) -> None:
        path = self.repository / ".agents/context/overview.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "- **Known gaps:** None",
                "- **Related specification IDs:** None — repository workflow",
            ),
            encoding="utf-8",
        )

        linter = self._lint("absent")

        self.assertEqual([], linter.errors)
        self.assertEqual(
            ["stale_vmodel_metadata"],
            [finding.code for finding in linter.warnings],
        )


if __name__ == "__main__":
    unittest.main()
