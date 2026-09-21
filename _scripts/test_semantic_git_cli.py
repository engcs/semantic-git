from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("semantic_git.py")
SPEC = importlib.util.spec_from_file_location("semantic_git", SCRIPT)
sg = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules["semantic_git"] = sg
SPEC.loader.exec_module(sg)


class CanonicalCliTests(unittest.TestCase):
    def test_namespace_defaults_to_root(self) -> None:
        args = sg.parser().parse_args(["index", "build"])
        self.assertEqual(".", args.namespace)
        self.assertIsNone(args.root)

    def test_namespace_is_explicit_and_scope_is_not_supported(self) -> None:
        args = sg.parser().parse_args(["compiled", "build", "--namespace", "_applications/mop"])
        self.assertEqual("_applications/mop", args.namespace)
        with self.assertRaises(SystemExit):
            sg.parser().parse_args(["compiled", "build", "--scope", "_applications/mop"])

    def test_root_is_only_global_repository_override(self) -> None:
        args = sg.parser().parse_args(["--root", "D:/semantic", "publication", "status"])
        self.assertEqual("D:/semantic", args.root)
        self.assertEqual(".", args.namespace)

    def test_repository_is_auto_detected_from_nested_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            (repo / "SEMANTIC_GIT.md").write_text("# spec\n", encoding="utf-8")
            nested = repo / "domain" / "child"
            nested.mkdir(parents=True)
            previous = Path.cwd()
            try:
                os.chdir(nested)
                self.assertEqual(repo.resolve(), sg.repository_root(None))
            finally:
                os.chdir(previous)

    def test_root_override_must_be_repository_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            (repo / "SEMANTIC_GIT.md").write_text("# spec\n", encoding="utf-8")
            nested = repo / "domain"
            nested.mkdir()
            with self.assertRaises(sg.CliError):
                sg.repository_root(str(nested))

    def test_capabilities_json_contains_commands_and_skills(self) -> None:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            code = sg.emit_capabilities(True)
        payload = json.loads(buffer.getvalue())
        self.assertEqual(0, code)
        routes = {item["route"] for item in payload["capabilities"]}
        self.assertIn("semantic-git://compiled/build", routes)
        self.assertIn("semantic-git://skills/reconstruction", routes)


if __name__ == "__main__":
    unittest.main()
