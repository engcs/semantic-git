from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("build_publication", Path(__file__).with_name("build_publication.py"))
bp = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules["build_publication"] = bp
SPEC.loader.exec_module(bp)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class PublicationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.mop = self.repo / "_applications" / "mop"
        write(self.repo / "SEMANTIC_GIT.md", "# spec\n")
        write(self.mop / "README.md", "# MOP\n\nAplicação.\n")
        write(self.mop / "REQUIREMENTS.md", """# Requirements - MOP

## Cabeçalho

Contrato parcial válido.

## Corpo

- **R-001** - Deve funcionar sem dimensões artificiais.
""")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_partial_rdo_namespace_can_be_rendered(self) -> None:
        texts, sources = bp.source_texts(self.mop)
        self.assertIn("REQUIREMENTS.md", texts)
        self.assertNotIn("DECISIONS.md", texts)
        self.assertNotIn("OPERATIONS.md", texts)
        rendered = bp.render_publication(self.mop, texts)
        self.assertIn("\nmop\n", rendered)
        self.assertNotIn("_applications/mop", rendered)
        self.assertIn("# Requirements", rendered)
        self.assertEqual({"README.md", "REQUIREMENTS.md"}, {source["path"] for source in sources})

    def test_manifest_uses_semantic_namespace_identity(self) -> None:
        texts, sources = bp.source_texts(self.mop)
        markdown = bp.render_publication(self.mop, texts)
        manifest = bp.base_manifest(self.mop, self.repo / "SEMANTIC_GIT.md", sources, bp.digest_text(markdown))
        self.assertEqual("mop", manifest["namespace"])

    def test_publication_requires_at_least_one_rdo_dimension(self) -> None:
        (self.mop / "REQUIREMENTS.md").unlink()
        with self.assertRaises(bp.PublicationError):
            bp.source_texts(self.mop)


if __name__ == "__main__":
    unittest.main()
