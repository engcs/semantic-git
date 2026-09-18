change: CHANGE-018
status: IN_PROGRESS
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
