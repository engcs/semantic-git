#!/usr/bin/env python3
"""One-shot correction for CHANGE-021: preserve archived CHANGE immutability."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"expected block not found in {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


validator = ROOT / "_scripts" / "validate_structure.py"
replace_once(
    validator,
    '''        if status in APPROVAL_STATUSES:\n            approved_commit = metadata.get("approved_semantic_commit", "")\n            if not COMMIT_RE.fullmatch(approved_commit):\n                self.add("CHANGE_APPROVAL", path, "approved_semantic_commit is required after approval", self.metadata_line(lines, "approved_semantic_commit"))\n            if not lists.get("approval_scope"):\n                self.add("CHANGE_APPROVAL", path, "approval_scope must contain at least one path after approval", self.metadata_line(lines, "approval_scope"))\n''',
    '''        if status in APPROVAL_STATUSES:\n            approved_commit = metadata.get("approved_semantic_commit", "")\n            approval_scope_present = "approval_scope" in metadata or "approval_scope" in lists\n            if archived:\n                # Archived CHANGEs are immutable historical records. Metadata rules\n                # introduced later must not force retroactive edits. When modern\n                # approval anchors are present, validate them; when they are absent,\n                # preserve the historical artifact as-is.\n                if approved_commit not in {"", "null"} and not COMMIT_RE.fullmatch(approved_commit):\n                    self.add("CHANGE_APPROVAL", path, "approved_semantic_commit is invalid", self.metadata_line(lines, "approved_semantic_commit"))\n                if approval_scope_present and not lists.get("approval_scope"):\n                    self.add("CHANGE_APPROVAL", path, "approval_scope is present but empty", self.metadata_line(lines, "approval_scope"))\n            else:\n                if not COMMIT_RE.fullmatch(approved_commit):\n                    self.add("CHANGE_APPROVAL", path, "approved_semantic_commit is required after approval", self.metadata_line(lines, "approved_semantic_commit"))\n                if not lists.get("approval_scope"):\n                    self.add("CHANGE_APPROVAL", path, "approval_scope must contain at least one path after approval", self.metadata_line(lines, "approval_scope"))\n''',
)

spec = ROOT / "SEMANTIC_GIT.md"
replace_once(
    spec,
    "Um CHANGE MERGED não deve ser reescrito para fingir que nunca existiu.\n\nReversão material deve ser representada por novo CHANGE.\n",
    "Um CHANGE MERGED não deve ser reescrito para fingir que nunca existiu.\n\nDepois de arquivada, uma CHANGE concluída é registro histórico imutável. Regras,\ncampos ou validações introduzidos posteriormente não autorizam nem exigem\nmigração retroativa de seu conteúdo. Validadores devem aceitar a forma histórica\npreservada e aplicar requisitos novos às CHANGEs ainda governáveis pelo ciclo\nativo antes do arquivamento; metadados modernos já presentes em artefatos\nhistóricos continuam sujeitos à validação de sua própria forma.\n\nInformação histórica ausente não deve ser inventada nem inserida retroativamente\nno arquivo arquivado. Quando sua ausência for material, a correção deve ocorrer\npor mecanismo atual governado — por exemplo novo CHANGE, evidência externa ou\nregra de compatibilidade do validador — sem reescrever o registro histórico.\n\nReversão material deve ser representada por novo CHANGE.\n",
)

agents = ROOT / "AGENTS.md"
replace_once(
    agents,
    "- preserve identidade, referências e histórico;\n- governe alterações semânticas materiais por CHANGE;\n",
    "- preserve identidade, referências e histórico;\n- nunca edite uma CHANGE já arquivada para satisfazer regra, campo ou validator introduzido depois; trate incompatibilidade histórica no fluxo atual, preservando o artefato arquivado byte a byte;\n- governe alterações semânticas materiais por CHANGE;\n",
)

tests = ROOT / "_scripts" / "test_semantic_index.py"
replace_once(
    tests,
    '''        write(self.root / "_changes" / "archived" / "CHANGE-001.md", """change: CHANGE-001\nstatus: MERGED\nbase_commit: 1111111\napproved_semantic_commit: 2222222\napproval_scope:\n  - _changes/CHANGE-001.md\nreason: null\n\n# CHANGE-001\n""")\n''',
    '''        # Legacy archived CHANGEs may predate approval-anchor metadata.\n        # They remain valid historical inputs and must never require retroactive edits.\n        write(self.root / "_changes" / "archived" / "CHANGE-001.md", """change: CHANGE-001\nstatus: MERGED\nbase_commit: 1111111\nreason: null\n\n# CHANGE-001\n""")\n''',
)

print("CHANGE-021 archive immutability correction applied")
