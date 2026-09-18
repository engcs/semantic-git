change: CHANGE-018
status: DRAFT
base_commit: 002a7f4de618d6331a35366abdf5cfcf6afaee46
approved_semantic_commit: null
approval_scope: null
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
- **ADD O-B** - Incorporar essa orientação à ergonomia humano–IA e ao Execution Protocol de `SEMANTIC_GIT.md`, para que qualquer agente que opere CHANGEs siga a mesma convenção.
