change: CHANGE-018
status: MERGED
base_commit: 002a7f4de618d6331a35366abdf5cfcf6afaee46
approved_semantic_commit: abda08469329371f4c51a12fd8c27e6087c57176
approval_scope:
  - _changes/CHANGE-018.md
depends_on: []
reason: null

# CHANGE-018

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - Ao criar ou apresentar um CHANGE ao humano, a IA deve fornecer uma síntese curta em linguagem natural que permita compreender rapidamente o propósito e o efeito principal da transformação sem exigir a leitura imediata do Semantic Diff completo.

### DECISIONS

- **ADD D-A** - Tratar a síntese como saída de interação humano–IA, e não como novo campo canônico persistente do CHANGE. A forma preferencial é um ou dois períodos corridos; listas ou bullets devem ser usados somente quando melhorarem materialmente a compreensão. Atende R-A.

### OPERATIONS

- **ADD O-A** - Incluir a síntese humana imediatamente após a criação ou apresentação inicial de um CHANGE e antes de expor detalhes extensos, mantendo-a curta, sem repetir item a item Requirements, Decisions ou Operations.
- **ADD O-B** - Registrar a convenção em `AGENTS.md` como orientação operacional obrigatória aos agentes deste repositório, sem criar novo campo no formato canônico do CHANGE nem alterar `SEMANTIC_GIT.md` apenas por uma preferência de apresentação. Atende R-A.

## Validation Evidence

- A branch parte de `main` em `002a7f4de618d6331a35366abdf5cfcf6afaee46`, está 4 commits à frente e 0 atrás da base.
- O diff material está limitado a `AGENTS.md` e a esta CHANGE.
- `AGENTS.md` agora exige um resumo humano curto ao criar ou apresentar inicialmente um CHANGE.
- O resumo é definido como 1–2 períodos corridos por padrão, sem repetir o Semantic Diff item a item e usando bullets somente quando melhorarem a compreensão.
- A orientação explicita que o resumo é saída de interação, não novo campo canônico, não substitui o Semantic Diff e não cria nova fonte de verdade.
- `SEMANTIC_GIT.md` não foi alterado, preservando a separação entre norma do protocolo e convenção operacional de apresentação do agente.

### Reconciliation Summary

- A alteração implementa integralmente o resumo humano solicitado sem ampliar o formato canônico de CHANGE.
- Não foi identificado FAIL ou REVIEW impeditivo para incorporação.

### Merge Evidence

- Incorporada na `main` pelo PR #6.
- Merge commit: `be9d9ade084949994dad6e135b15fe8e6eb793e2`.
