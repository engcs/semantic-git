change: CHANGE-005
status: IN_PROGRESS
base_commit: a1f3f96e8434c6d1bc43267382412d89c880e0cb
approved_semantic_commit: 12a43809e9a5e4d122c855a0542e11a4703431d4
approval_scope:
  - SEMANTIC_GIT.md
  - changes/CHANGE-005.md
reason: null

# CHANGE-005

## Semantic Diff

### REQUIREMENTS

- **ADD** - Permitir que a criação inicial governada de um Semantic Namespace inexistente seja representada por um CHANGE localizado no namespace que será criado, ainda que esse namespace não exista no AS-IS do `base_commit`.
- **ADD** - Reconhecer que a criação inicial de um Semantic Namespace também pode ocorrer manualmente ou fora do Semantic Git, sem CHANGE-INIT, sem invalidar o AS-IS resultante.
- **ADD** - Exigir que toda alteração semântica material posterior à criação inicial do namespace permaneça governada por CHANGE.

### DECISIONS

- **ADD** - Reservar `CHANGE-INIT` como identificador especial, único por namespace, para a primeira criação governada de seu AS-IS.
- **ADD** - Usar `CHANGE-INIT` como caminho padrão quando a criação inicial do namespace ocorrer sob o Semantic Git.
- **ADD** - Definir `CHANGE-INIT` como marcador do papel de inicialização semântica, e não como registro da ferramenta ou do agente que produziu a alteração.
- **ADD** - Definir que `CHANGE-INIT` não consome o primeiro identificador numérico; a primeira evolução normal do namespace utilizará `CHANGE-001`.
- **ADD** - Permitir que o CHANGE de inicialização esteja no caminho do namespace alvo na branch, mesmo quando o namespace estiver ausente do AS-IS de origem, sem exigir CHANGE ou alteração no namespace pai.
- **ADD** - Submeter `CHANGE-INIT` ao fluxo normal de branch, aprovação, implementação, RECONCILIATION, pre-merge recheck, merge e arquivamento.

### OPERATIONS

- **ADD** - Validar, antes da aprovação de `CHANGE-INIT`, que o namespace alvo não possui AS-IS no `base_commit` e que a branch adiciona seu primeiro AS-IS.
- **ADD** - Validar que `CHANGE-INIT` não altera Requirements, Decisions, Operations ou qualquer outro AS-IS de namespace ancestral.
- **ADD** - Validar que existe no máximo um `CHANGE-INIT` por identidade canônica de namespace e que ele não pode ser reutilizado.
- **ADD** - Arquivar `CHANGE-INIT` no diretório `changes/archived/` do namespace inicializado após o merge confirmado.
- **ADD** - Quando o namespace já existir no AS-IS de origem sem `CHANGE-INIT`, tratar esse estado como origem estabelecida e alocar `CHANGE-001` para a primeira evolução governada, sem inferir ou registrar a autoria de sua criação.
