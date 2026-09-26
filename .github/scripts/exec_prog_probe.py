from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from _scripts._internal import memory_reconciliation

ROOT = Path.cwd().resolve()
NS = ROOT / "_applications" / "exec_prog"
MEMORY = NS / "_memory" / "FINDINGS.yaml"
CHANGE = NS / "_changes" / "CHANGE-001.md"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True)


(NS / "_memory").mkdir(parents=True, exist_ok=True)
(NS / "_changes").mkdir(parents=True, exist_ok=True)

(NS / "REQUIREMENTS.md").write_text("""# Requirements - exec_prog

## Cabeçalho
Contrato semântico mínimo do fixture EXEC_PROG para testar memória analítica.

## Corpo
- **R-001** - Ocorrências expurgadas não devem contribuir para a apuração do indicador.
- **R-003** - Para uma mesma competência e objeto de apuração, deve existir no máximo uma versão de catálogo vigente.
""", encoding="utf-8")

(NS / "DECISIONS.md").write_text("""# Decisions - exec_prog

## Cabeçalho
Decisões mínimas do fixture EXEC_PROG.

## Corpo
- **D-001** - A decisão manual de expurgo prevalece sobre regras automáticas; decisão manual de proteção veta o expurgo automático. Atende R-001.
- **D-002** - A leitura operacional considera programada a linha com VAR2_VALOR = 1 e executada a linha com VAR1_VALOR = 1.
""", encoding="utf-8")

(NS / "OPERATIONS.md").write_text("""# Operations - exec_prog

## Cabeçalho
Operação mínima para materializar o contrato do fixture.

## Corpo
- **O-001** - Apurar EXEC_PROG preservando a seleção da versão vigente e as flags de execução e programação.
""", encoding="utf-8")

MEMORY.write_text("""namespace: exec_prog
findings:
  - id: F-001
    status: promoted
    category: reconstructed_rule
    summary: >
      A investigação do SQL de EXEC_PROG encontrou precedência explícita da curadoria manual sobre a regra automática de expurgo.
    evidence:
      certainty: proven
      sources:
        - repository: dbt_performance_operacional
          path: models/legado/indicadores/aderencia_execucao_framework
          locator: FLAG_EXPURGO_GLOBAL
    risk:
      level: high
      consequence: >
        Uma reimplementação que ignore a precedência manual pode expurgar programações protegidas ou manter programações que deveriam ser expurgadas.
    semantic_status:
      state: promoted
      reason: >
        O significado durável foi promovido para a decisão canônica correspondente.
    semantic_refs:
      - exec_prog:D-001

  - id: F-002
    status: active
    category: physical_exception
    summary: >
      Existe um alias legado deprecated mantido temporariamente por compatibilidade e apontando para o nome canônico de regras de negócio.
    evidence:
      certainty: proven
      sources:
        - repository: dbt_performance_operacional
          path: models/legado/indicadores/aderencia_execucao_framework/intermediate/siprog_prata__vw__fato_programacao__controle_de_janela.sql
          locator: DEPRECATED Mantido temporariamente por compatibilidade
    risk:
      level: medium
      consequence: >
        Remover o alias sem verificar consumidores pode quebrar dependências físicas ainda existentes.
    semantic_status:
      state: non_semantic
      reason: >
        A evidência demonstra compatibilidade física temporária, não uma regra durável do indicador.

  - id: F-003
    status: promoted
    category: reconstructed_invariant
    summary: >
      A investigação encontrou teste explícito que rejeita mais de uma versão vigente para a mesma competência nos fatos e KPIs de EXEC_PROG.
    evidence:
      certainty: proven
      sources:
        - repository: dbt_performance_operacional
          path: tests/exec_prog
          locator: QTD_VERSOES_VIGENTES > 1
    risk:
      level: high
      consequence: >
        Múltiplas versões vigentes podem tornar a apuração ambígua e duplicar ou divergir resultados por competência.
    semantic_status:
      state: promoted
      reason: >
        O invariável foi promovido para Requirement; o finding preserva descoberta e evidência.
    semantic_refs:
      - exec_prog:R-002

  - id: F-004
    status: promoted
    category: methodology
    summary: >
      A metodologia operacional separa explicitamente linha programada por VAR2_VALOR = 1 e linha executada por VAR1_VALOR = 1.
    evidence:
      certainty: proven
      sources:
        - repository: methodology-session
          locator: EXEC_PROG regra soberana VAR2_VALOR e VAR1_VALOR
    risk:
      level: high
      consequence: >
        Usar colunas textuais como critério de contagem pode produzir números diferentes do KPI governado.
    semantic_status:
      state: promoted
      reason: >
        A regra de leitura operacional foi promovida para decisão canônica.
    semantic_refs:
      - exec_prog:D-002
""", encoding="utf-8")

head = run("git", "rev-parse", "HEAD").stdout.strip()
CHANGE.write_text(f"""change: CHANGE-001
status: RECONCILED
base_commit: {head}
approved_semantic_commit: {head}
approval_scope:
  - _applications/exec_prog/_changes/CHANGE-001.md
reason: null

# CHANGE-001

## Semantic Diff

### REQUIREMENTS

- **REMOVE R-002** - Substitui o requisito anterior de versão vigente.
- **ADD R-003** - Para uma mesma competência e objeto de apuração, deve existir no máximo uma versão de catálogo vigente.

### DECISIONS

- **MODIFY D-001** - Mantém a identidade da regra de precedência de expurgo após revisão de formulação.

### OPERATIONS

- **NONE** - Sem alteração operacional adicional neste fixture.
""", encoding="utf-8")

subprocess.run(["git", "config", "user.name", "exec-prog-probe"], cwd=ROOT, check=True)
subprocess.run(["git", "config", "user.email", "exec-prog-probe@example.invalid"], cwd=ROOT, check=True)
subprocess.run(["git", "add", "_applications/exec_prog"], cwd=ROOT, check=True)
subprocess.run(["git", "commit", "-m", "test fixture: exec_prog stale promoted finding"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)

print("===== FINDINGS.yaml =====")
print(MEMORY.read_text(encoding="utf-8"))

payload = memory_reconciliation.impacted_promoted_findings(ROOT, CHANGE)
print("===== IMPACT LOCATOR =====")
print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))

got = {(x["finding"], x["semantic_ref"]) for x in payload["impacted_promoted_findings"]}
expected = {("exec_prog:F-001", "exec_prog:D-001"), ("exec_prog:F-003", "exec_prog:R-002")}
assert got == expected, (got, expected)
print("LOCATOR_ASSERTION=PASS")
print("UNRELATED_F002_NOT_SELECTED=True")
print("UNRELATED_F004_NOT_SELECTED=True")

validate = run(sys.executable, "_scripts/semantic_git.py", "validate", "--json")
print("===== CANONICAL STRUCTURAL VALIDATION =====")
print(validate.stdout or validate.stderr)
print(f"STRUCTURAL_EXIT_CODE={validate.returncode}")
try:
    structure = json.loads(validate.stdout)
    print("STRUCTURAL_RESULT=" + structure.get("result", "UNKNOWN"))
    stale_gate = any("R-002" in x.get("message", "") for x in structure.get("findings", []))
    print("STALE_MEMORY_GATE_PRESENT=" + str(stale_gate))
except json.JSONDecodeError:
    print("STRUCTURAL_JSON_PARSE=FAIL")

index_build = run(sys.executable, "_scripts/semantic_git.py", "index", "build", "--namespace", "_applications/exec_prog")
print("===== INDEX BUILD =====")
print(index_build.stdout)
print(index_build.stderr)
print(f"INDEX_EXIT_CODE={index_build.returncode}")
index_detected = "unresolved reference" in (index_build.stdout + index_build.stderr)
print("INDEX_STALE_REFERENCE_DETECTION=" + ("PASS" if index_detected else "FAIL"))

if not index_detected:
    raise SystemExit("expected semantic index to reject stale exec_prog:R-002 reference")
