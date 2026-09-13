change: CHANGE-005
status: DRAFT
base_commit: a1f3f96e8434c6d1bc43267382412d89c880e0cb
approved_semantic_commit: 156fcabbbf58c2d3ab62919b2f34c1106c4b88f6
approval_scope:
  - SEMANTIC_GIT.md
  - changes/CHANGE-005.md
reason: null

# CHANGE-005

## Semantic Diff

### REQUIREMENTS

- **ADD** - Exigir que a criação inicial de um Semantic Namespace inexistente, quando realizada sob o Semantic Git, seja governada por um único `CHANGE-INIT` localizado no namespace que será criado, ainda que esse namespace não exista no AS-IS do `base_commit`.
- **ADD** - Reconhecer que a criação inicial de um Semantic Namespace também pode ocorrer manualmente ou fora do Semantic Git; nessa modalidade não existe CHANGE de inicialização e o AS-IS resultante é reconhecido sem invalidação ou reconstrução retroativa.
- **ADD** - Exigir que toda alteração semântica material posterior à criação inicial do namespace permaneça governada por CHANGE.
- **ADD** - Tratar a ausência de AS-IS do namespace alvo como ausência de predecessor, sem criar ou atribuir um AS-IS vazio para a reconciliação de `CHANGE-INIT`.

### DECISIONS

- **ADD** - Reservar `CHANGE-INIT` como identificador especial, único por namespace, para a primeira criação governada de seu AS-IS.
- **ADD** - Exigir `CHANGE-INIT` como o único caminho de criação inicial quando o namespace for criado sob o Semantic Git.
- **ADD** - Definir `CHANGE-INIT` como marcador do papel de inicialização semântica, e não como registro da ferramenta ou do agente que produziu a alteração.
- **ADD** - Definir que `CHANGE-INIT` não consome o primeiro identificador numérico; a primeira evolução normal do namespace utilizará `CHANGE-001`.
- **ADD** - Permitir que o CHANGE de inicialização esteja no caminho do namespace alvo na branch, mesmo quando o namespace estiver ausente do AS-IS de origem, sem exigir CHANGE ou alteração no namespace pai.
- **ADD** - Submeter `CHANGE-INIT` ao fluxo normal de branch, aprovação, implementação, RECONCILIATION, pre-merge recheck, merge e arquivamento.
- **ADD** - Identificar a especificação resultante como Semantic Git v1.5.

### OPERATIONS

- **ADD** - Validar, antes da aprovação de `CHANGE-INIT`, que o namespace alvo não possui AS-IS no `base_commit` e que a branch adiciona seu primeiro AS-IS.
- **ADD** - Validar que `CHANGE-INIT` não altera Requirements, Decisions, Operations ou qualquer outro AS-IS de namespace ancestral.
- **ADD** - Validar que existe no máximo um `CHANGE-INIT` por identidade canônica de namespace e que ele não pode ser reutilizado.
- **ADD** - Arquivar `CHANGE-INIT` no diretório `changes/archived/` do namespace inicializado após o merge confirmado.
- **ADD** - Quando o namespace já existir no AS-IS de origem sem registro de `CHANGE-INIT`, tratar esse estado como criação externa ao protocolo e alocar `CHANGE-001` para a primeira evolução governada, sem inferir ou registrar a autoria de sua criação.
