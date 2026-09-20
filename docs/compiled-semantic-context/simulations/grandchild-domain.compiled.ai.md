# COMPILED SEMANTIC CONTEXT

> **STRUCTURAL SIMULATION ONLY** — este arquivo representa o caso de um domínio com dois níveis ancestrais, usando `mop/programacao/exec_prog` como forma de namespace. O conteúdo local não é preenchido porque esses domínios não existem na `main` usada como fonte desta branch.

## Metadata

```yaml
artifact: compiled-semantic-context
target_namespace: mop/programacao/exec_prog
scope_depth: 3
authority: DERIVED
simulation: true
content_mode: STRUCTURE_ONLY
```

## Reading Contract

- O objetivo é mostrar o fechamento de contexto de um domínio profundo.
- O compilador percorre a cadeia estrutural, não uma busca semântica.
- R/D/O seriam reproduzidos literalmente por escopo.
- Nenhum resumo, seleção vetorial, inferência de relação ou preenchimento de lacuna ocorre nesta etapa.
- O arquivo é regenerável e não pode introduzir nova autoridade.

## Effective Scope Chain

```text
mop                         [ANCESTOR 0]
└── programacao             [ANCESTOR 1]
    └── exec_prog           [TARGET]
```

---

# Scope: mop

Role: `INHERITED`

```text
[GENERATED FROM SOURCE]

Requirements:
  mop:R-*

Decisions:
  mop:D-*

Operations:
  mop:O-*
```

O conteúdo real seria copiado dos arquivos governados existentes na `main`.

---

# Scope: mop/programacao

Role: `INHERITED`

```text
[GENERATED FROM SOURCE IF DOMAIN EXISTS]

Requirements:
  mop/programacao:R-*

Decisions:
  mop/programacao:D-*

Operations:
  mop/programacao:O-*
```

Nesta simulação o namespace não está materializado na fonte `main`, então nenhum conteúdo é fabricado.

---

# Scope: mop/programacao/exec_prog

Role: `LOCAL / TARGET`

```text
[GENERATED FROM SOURCE IF DOMAIN EXISTS]

Requirements:
  mop/programacao/exec_prog:R-*

Decisions:
  mop/programacao/exec_prog:D-*

Operations:
  mop/programacao/exec_prog:O-*
```

---

# Explicit Relationships

Uma compilação real pode materializar relações explícitas de todos os escopos do fechamento:

```text
mop:*                         -> mop:*
mop/programacao:*             -> mop/programacao:*
mop/programacao/exec_prog:*   -> mop/programacao/exec_prog:*
```

Também podem existir relações explícitas entre namespaces, desde que a própria fonte/índice permita resolvê-las inequivocamente:

```text
mop/programacao/exec_prog:D-x
    --references/satisfies/etc-->
mop/programacao:R-y
```

Formato sugerido:

```yaml
relations:
  - source: <qualified-id>
    predicate: <explicit-predicate>
    target: <qualified-id>
    resolution: explicit
```

Relações apenas plausíveis semanticamente permanecem fora do CSC.

---

# Inheritance Materialization

```yaml
inheritance:
  target: mop/programacao/exec_prog
  chain:
    - namespace: mop
      role: ancestor
      depth: 0
      included_by: namespace_closure
    - namespace: mop/programacao
      role: ancestor
      depth: 1
      included_by: namespace_closure
    - namespace: mop/programacao/exec_prog
      role: target
      depth: 2
      included_by: target
```

A ordem é estável: ancestral mais geral primeiro, alvo por último. Isso permite que uma IA leia o arquivo como uma progressão de contexto geral para específico sem precisar navegar no repositório.

---

# Shadowing / Override Policy — questão de design

O CSC precisa deixar explícito o que acontece quando um domínio filho especializa ou substitui algo ancestral.

Nesta simulação, **nenhuma política de override é assumida**. Até que o Semantic-Git tenha uma regra formal para substituição/supersessão, o compilador deve preservar ambos os nodes e suas identidades.

Exemplo de comportamento conservador:

```text
ANCESTOR:
  mop/programacao:D-010

LOCAL:
  mop/programacao/exec_prog:D-004

=> ambos permanecem no CSC.
=> o compilador não decide que D-004 "substitui" D-010.
```

Se futuramente existir uma relação governada do tipo `supersedes`, `overrides` ou equivalente, ela poderá ser materializada explicitamente.

---

# Unresolved References

```yaml
unresolved_references:
  # referências sintaticamente detectadas cujo target não foi encontrado
```

Possíveis causas determinísticas:

- ID inexistente;
- namespace ausente;
- referência curta ambígua;
- formato não reconhecido;
- target fora do fechamento permitido pela regra.

O compilador registra a falha; não usa embedding/LLM para "adivinhar" o alvo.

---

# Provenance

```yaml
sources:
  - namespace: mop
    role: ancestor
    path: _applications/mop
    status_in_source_main: PRESENT

  - namespace: mop/programacao
    role: ancestor
    path: _applications/mop/programacao
    status_in_source_main: NOT_PRESENT

  - namespace: mop/programacao/exec_prog
    role: target
    path: _applications/mop/programacao/exec_prog
    status_in_source_main: NOT_PRESENT
```

Em um CSC real, cada entidade também pode carregar:

```yaml
entity_provenance:
  id: mop/programacao/exec_prog:D-004
  source_path: _applications/mop/programacao/exec_prog/DECISIONS.md
  locator: D-004
  source_commit: <sha>
```

---

# Expected AI Consumption

Uma IA receberia um único arquivo com o contexto de três níveis já materializado:

```text
[regras gerais de mop]
        ↓
[regras comuns de programacao]
        ↓
[regras específicas de exec_prog]
```

Isso elimina a necessidade mecânica de:

1. descobrir quem é o pai do domínio;
2. abrir arquivos ancestrais;
3. resolver IDs curtos manualmente;
4. reconstruir a cadeia de proveniência;
5. descobrir quais relações explícitas já existem.

Não elimina a necessidade de interpretação semântica da linguagem natural. O CSC reduz navegação e reconstrução estrutural; não transforma significado em algo puramente determinístico.

---

# Publication Contrast

No domínio profundo, a diferença tende a ficar mais visível:

```text
PUBLICATION.md
  foco: o que este domínio quer comunicar ao humano
  herança: pode permanecer implícita/declarada
  repetição: minimizada

compiled.ai.md
  foco: contexto estruturalmente fechado para IA
  herança: expandida
  repetição: deliberada
```

Esse é o caso em que o CSC tende a gerar maior ganho de reconstrução, porque o custo de navegação cresce com a profundidade do namespace.
