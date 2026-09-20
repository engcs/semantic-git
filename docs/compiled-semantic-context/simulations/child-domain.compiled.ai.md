# COMPILED SEMANTIC CONTEXT

> **STRUCTURAL SIMULATION ONLY** — este arquivo representa como um CSC de um domínio filho poderia ser montado. `mop/programacao` não está materializado na `main` usada como base desta branch; por isso nenhum conhecimento local fictício é introduzido.

## Metadata

```yaml
artifact: compiled-semantic-context
target_namespace: mop/programacao
scope_depth: 2
authority: DERIVED
simulation: true
content_mode: STRUCTURE_ONLY
```

## Reading Contract

- Este exemplo valida o formato de compilação de um domínio filho.
- Nenhuma entidade local de `mop/programacao` abaixo é inventada.
- Em uma compilação real, os blocos marcados como `GENERATED FROM SOURCE` seriam preenchidos literalmente a partir dos R/D/O governados.
- A cadeia ancestral é materializada integralmente segundo a regra estrutural; não há seleção por similaridade ou por interpretação de LLM.

## Effective Scope Chain

```text
mop                [ANCESTOR 0]
└── programacao     [TARGET]
```

---

# Scope: mop

Role: `INHERITED`

## Requirements

```text
[GENERATED FROM SOURCE]
Todos os nodes mop:R-* existentes no índice/fonte governada,
com IDs qualificados e texto preservado.
```

## Decisions

```text
[GENERATED FROM SOURCE]
Todos os nodes mop:D-* existentes no índice/fonte governada.
```

## Operations

```text
[GENERATED FROM SOURCE]
Todos os nodes mop:O-* existentes no índice/fonte governada.
```

A compilação real deste bloco usaria:

```text
_applications/mop/REQUIREMENTS.md
_applications/mop/DECISIONS.md
_applications/mop/OPERATIONS.md
```

---

# Scope: mop/programacao

Role: `LOCAL / TARGET`

## Requirements

```text
[GENERATED FROM SOURCE IF DOMAIN EXISTS]
mop/programacao:R-...
```

## Decisions

```text
[GENERATED FROM SOURCE IF DOMAIN EXISTS]
mop/programacao:D-...
```

## Operations

```text
[GENERATED FROM SOURCE IF DOMAIN EXISTS]
mop/programacao:O-...
```

Nenhum conteúdo foi preenchido nesta simulação porque o domínio não existe na `main` usada como fonte.

---

# Explicit Relationships

Em uma compilação real, esta seção conteria a união determinística de:

```text
1. relações explícitas internas de mop;
2. relações explícitas internas de mop/programacao;
3. relações explícitas cross-namespace que apontem entre esses dois escopos.
```

Formato proposto:

```yaml
relations:
  - source: <qualified-id>
    predicate: <governed-predicate>
    target: <qualified-id>
    source_scope: <namespace>
    target_scope: <namespace>
```

Nenhuma relação cross-namespace é criada apenas porque um texto local menciona informalmente um conceito ancestral.

---

# Inheritance Materialization

Esta seção existe para deixar claro à IA **por que** o conteúdo de `mop` está no arquivo.

```yaml
inheritance:
  target: mop/programacao
  chain:
    - namespace: mop
      role: ancestor
      included_by: namespace_closure
    - namespace: mop/programacao
      role: target
      included_by: target
```

Não há tentativa de responder:

> "quais entidades de mop são mais relevantes para programacao?"

O CSC base inclui o fechamento estrutural definido. Redução de tokens, se necessária, é responsabilidade de uma etapa posterior.

---

# Unresolved References

Forma proposta:

```yaml
unresolved_references:
  # preenchido deterministicamente durante a resolução de IDs
```

Se uma Decision local declarar, por exemplo, uma referência explícita a `mop:R-999` e esse node não existir, a referência deve aparecer aqui; o compilador não deve tentar encontrar um substituto semanticamente parecido.

---

# Provenance

```yaml
sources:
  - namespace: mop
    role: ancestor
    requirements: _applications/mop/REQUIREMENTS.md
    decisions: _applications/mop/DECISIONS.md
    operations: _applications/mop/OPERATIONS.md
  - namespace: mop/programacao
    role: target
    requirements: _applications/mop/programacao/REQUIREMENTS.md
    decisions: _applications/mop/programacao/DECISIONS.md
    operations: _applications/mop/programacao/OPERATIONS.md
    status_in_this_simulation: NOT_PRESENT_ON_SOURCE_MAIN
```

---

# What This Simulation Tests

Este exemplo testa a primeira diferença realmente importante entre `PUBLICATION.md` e CSC:

```text
PUBLICATION do filho
    tende a mostrar o conhecimento local
    e confiar na herança para evitar repetição.

CSC do filho
    materializa o ancestral + o local
    para reduzir navegação necessária à IA.
```

A redundância é deliberada e derivada; não muda o modelo autoritativo.
