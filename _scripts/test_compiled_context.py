from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


si = load("semantic_index", "semantic_index.py")
bp = load("build_publication", "build_publication.py")
csc = load("compile_semantic_context", "compile_semantic_context.py")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class CompiledSemanticContextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Test"], check=True)
        write(self.root / "SEMANTIC_GIT.md", "# spec\n")
        write(
            self.root / "_scripts" / "validate_structure.py",
            'import sys\nprint("{\\"result\\": \\"PASS\\"}")\nsys.exit(0)\n',
        )
        write(
            self.root / "REQUIREMENTS.md",
            """# Requirements - root

## Cabeçalho

Contrato global.

## Corpo

- **R-001** - Regra global reutilizável.
""",
        )
        self.mop = self.root / "_applications" / "mop"
        write(self.mop / "README.md", "# MOP\n\nAplicação de teste.\n")
        write(
            self.mop / "REQUIREMENTS.md",
            """# Requirements - MOP

## Cabeçalho

Requisitos locais.

## Corpo

- **R-001** - O domínio deve preservar identidade local.
""",
        )
        write(
            self.mop / "DECISIONS.md",
            """# Decisions - MOP

## Cabeçalho

Decisões locais.

## Corpo

- **D-001** - Usar identidade local explícita. Atende R-001.
""",
        )
        write(
            self.mop / "OPERATIONS.md",
            """# Operations - MOP

## Cabeçalho

Operações locais.

## Corpo

- **O-001** - Executar D-001 respeitando também root:R-001.
""",
        )
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture"], check=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_same_commit_produces_byte_identical_compiled_output(self) -> None:
        _, first = csc.build_text(self.root, "_applications/mop")
        _, second = csc.build_text(self.root, "_applications/mop")
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

    def test_source_blocks_are_lossless_for_publication_inputs(self) -> None:
        _, compiled = csc.build_text(self.root, "_applications/mop")
        extracted = csc.extract_source_texts(compiled)
        expected, _ = bp.source_texts(self.mop)
        self.assertEqual(expected, extracted)

    def test_publication_projection_is_exactly_current_publication(self) -> None:
        _, compiled = csc.build_text(self.root, "_applications/mop")
        expected_texts, _ = bp.source_texts(self.mop)
        expected = bp.render_publication(self.mop, expected_texts)
        actual = csc.publication_projection(self.mop, compiled)
        self.assertEqual(expected, actual)

    def test_compiled_enriches_local_units_and_materializes_explicit_external_dependency(self) -> None:
        _, compiled = csc.build_text(self.root, "_applications/mop")
        self.assertIn('"id":"mop:R-001"', compiled)
        self.assertIn('"type":"satisfies"', compiled)
        self.assertIn('### root:R-001', compiled)
        self.assertIn('Regra global reutilizável.', compiled)
        self.assertIn('"type":"depends_on"', compiled)

    def test_build_and_validate_detect_drift(self) -> None:
        path = csc.build(self.root, "_applications/mop")
        validated_path, errors = csc.validate(self.root, "_applications/mop")
        self.assertEqual(path, validated_path)
        self.assertEqual([], errors)
        path.write_text(path.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
        _, errors = csc.validate(self.root, "_applications/mop")
        self.assertTrue(any(error.startswith("DRIFT:") for error in errors))

    def test_dirty_semantic_source_is_rejected(self) -> None:
        path = self.mop / "REQUIREMENTS.md"
        path.write_text(path.read_text(encoding="utf-8").replace("identidade local", "identidade alterada"), encoding="utf-8")
        with self.assertRaises(csc.CompilationError):
            csc.build_text(self.root, "_applications/mop")


if __name__ == "__main__":
    unittest.main()
