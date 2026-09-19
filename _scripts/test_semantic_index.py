from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("semantic_index", Path(__file__).with_name("semantic_index.py"))
si = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules["semantic_index"] = si
SPEC.loader.exec_module(si)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class SemanticIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(self.root), "config", "user.name", "Test"], check=True)
        write(self.root / "SEMANTIC_GIT.md", "# spec\n")
        write(self.root / "_scripts" / "validate_structure.py", "import sys\nprint(\"{\\\"result\\\": \\\"PASS\\\"}\")\nsys.exit(0)\n")
        write(self.root / "REQUIREMENTS.md", """# Requirements - root

## Cabeçalho

Global.

## Corpo

- **R-001** - Regra global.
""")
        write(self.root / "DECISIONS.md", """# Decisions - root

## Cabeçalho

Escolhas.

## Corpo

- **D-001** - Escolha global. Atende R-001.
""")
        write(self.root / "_changes" / "archived" / "CHANGE-001.md", """change: CHANGE-001
status: MERGED
base_commit: 1111111
approved_semantic_commit: 2222222
approval_scope:
  - _changes/CHANGE-001.md
reason: null

# CHANGE-001
""")
        write(self.root / "domain" / "child" / "DECISIONS.md", """# Decisions - child

## Cabeçalho

Child.

## Corpo

- **D-001** - Usa root:R-001 como contrato externo.
""")
        write(self.root / "domain" / "child" / "_memory" / "FINDINGS.yaml", """namespace: domain/child
findings:
  - id: F-001
    status: active
    category: evidence_gap
    summary: \"Gap conhecido\"
    evidence: proven
    risk: medium
    semantic_status: unresolved
    semantic_refs:
      - root:R-001
""")
        write(self.root / "domain" / "sibling" / "REQUIREMENTS.md", """# Requirements - sibling

## Cabeçalho

Sibling.

## Corpo

- **R-001** - Não deve aparecer no índice do child.
""")
        write(self.root / "implementation" / "code.py", "print('x')\n")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "fixture"], check=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_root_index_is_deterministic_and_indexes_core_artifacts(self) -> None:
        first = si.build_index(self.root, ".", check_structure=False)
        second = si.build_index(self.root, ".", check_structure=False)
        self.assertEqual(first, second)
        ids = {node["id"] for node in first["nodes"]}
        self.assertIn("root:R-001", ids)
        self.assertIn("root:D-001", ids)
        self.assertIn("root:CHANGE-001", ids)
        self.assertIn("domain/child:F-001", ids)
        self.assertNotIn("namespace:implementation", ids)
        self.assertIn({"from": "root:D-001", "type": "satisfies", "to": "root:R-001"}, first["edges"])

    def test_descendant_scope_excludes_sibling_and_uses_external_stubs(self) -> None:
        index = si.build_index(self.root, "domain/child", check_structure=False)
        ids = {node["id"] for node in index["nodes"]}
        self.assertIn("namespace:domain/child", ids)
        self.assertIn("domain/child:D-001", ids)
        self.assertIn("domain/child:F-001", ids)
        self.assertNotIn("domain/sibling:R-001", ids)
        root_r = next(node for node in index["nodes"] if node["id"] == "root:R-001")
        self.assertTrue(root_r["external"])
        parent = next(node for node in index["nodes"] if node["id"] == "namespace:domain")
        self.assertTrue(parent["external"])
        self.assertNotIn("root:D-001", ids)
        self.assertIn({"from": "domain/child:D-001", "type": "references", "to": "root:R-001"}, index["edges"])
        self.assertIn({"from": "domain/child:F-001", "type": "semantic_ref", "to": "root:R-001"}, index["edges"])

    def test_parent_child_namespace_relation(self) -> None:
        index = si.build_index(self.root, ".", check_structure=False)
        self.assertIn({"from": "namespace:domain/child", "type": "parent_namespace", "to": "namespace:domain"}, index["edges"])
        self.assertIn({"from": "namespace:domain", "type": "parent_namespace", "to": "namespace:root"}, index["edges"])

    def test_validation_rejects_missing_endpoint_and_missing_source(self) -> None:
        payload = si.build_index(self.root, ".", check_structure=False)
        broken = json.loads(json.dumps(payload))
        broken["edges"].append({"from": "root:R-001", "type": "references", "to": "root:R-999"})
        errors = si.validate_payload(self.root, broken)
        self.assertTrue(any("edge target does not exist" in error for error in errors))
        broken2 = json.loads(json.dumps(payload))
        broken2["nodes"][0]["source"]["path"] = "missing.file"
        errors = si.validate_payload(self.root, broken2)
        self.assertTrue(any("source does not exist" in error for error in errors))

    def test_validation_rejects_duplicate_node_id(self) -> None:
        payload = si.build_index(self.root, ".", check_structure=False)
        payload["nodes"].append(dict(payload["nodes"][0]))
        errors = si.validate_payload(self.root, payload)
        self.assertTrue(any("duplicate node id" in error for error in errors))

    def test_stale_index_is_detected_when_source_changes(self) -> None:
        payload = si.build_index(self.root, ".", check_structure=False)
        path = self.root / "REQUIREMENTS.md"
        path.write_text(path.read_text().replace("Regra global.", "Regra global alterada."), encoding="utf-8")
        expected = si.build_index(self.root, ".", check_structure=False)
        errors = si.validate_payload(self.root, payload, expected)
        self.assertTrue(any(error.startswith("STALE:") for error in errors))
        self.assertTrue(any(error.startswith("DRIFT:") for error in errors))

    def test_build_validate_and_query_commands_share_current_index(self) -> None:
        path = si.write_index(self.root, "domain/child")
        self.assertTrue(path.is_file())
        validated_path, errors = si.validate_index(self.root, "domain/child")
        self.assertEqual(path, validated_path)
        self.assertEqual([], errors)
        result = si.query_index(self.root, "domain/child", "domain/child:D-001", None, None)
        self.assertEqual(["domain/child:D-001"], [node["id"] for node in result["matches"]])

    def test_duplicate_rdo_identity_fails_build(self) -> None:
        path = self.root / "REQUIREMENTS.md"
        text = path.read_text(encoding="utf-8")
        path.write_text(text + "- **R-001** - Duplicada.\n", encoding="utf-8")
        with self.assertRaises(si.IndexErrorBase):
            si.build_index(self.root, ".", check_structure=False)


if __name__ == "__main__":
    unittest.main()
