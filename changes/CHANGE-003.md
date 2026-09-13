change: CHANGE-003
status: IN_PROGRESS
base_commit: f01605f607761f976dbe62aa1cc57fc97d4ef1d3
approved_semantic_commit: 6ec278873e371633e38b4b3ebe1d999baa1b8046
approval_scope:
  - SEMANTIC_GIT.md
  - changes/CHANGE-003.md
reason: null

# CHANGE-003

## Semantic Diff

### REQUIREMENTS

- **ADD** - Impedir alocação de recursos de implementação antes da aprovação semântica registrada.
- **ADD** - Separar aprovação semântica, autorização de implementação, autorização de merge, autorização de tag e autorização de publicação.
- **ADD** - Tratar a `main` local do Semantic Repository governante como AS-IS oficial; push é somente publicação ou replicação.
- **ADD** - Incorporar implementação, arquivamento e estado `MERGED` em uma transação local única.

### DECISIONS

- **ADD** - Permitir em `DRAFT` somente leitura, síntese, análise de gaps e escrita na própria CHANGE.
- **ADD** - Exigir preflight de recursos, escopo, aprovação e estado antes de alocar agente de implementação.
- **ADD** - Exigir autorização textual explícita e identificada para merge, tag e push; aprovação semântica não implica nenhuma delas.
- **ADD** - Invalidar o gate pré-merge quando qualquer entrada imutável observada mudar.
- **ADD** - Identificar a especificação resultante como Semantic Git v1.3.

### OPERATIONS

- **ADD** - Bloquear a operação com `IMPLEMENTATION_BLOCKED`, `MERGE_BLOCKED`, `RELEASE_BLOCKED` ou `PUBLICATION_BLOCKED` quando o gate correspondente não estiver satisfeito.
- **ADD** - Executar somente o delta aprovado em `IN_PROGRESS` e retornar a `DRAFT` diante de drift material.
- **ADD** - Executar o merge local autorizado em transação controlada que já contenha o arquivamento e o estado `MERGED` antes do commit final.
- **ADD** - Não criar tag ou executar push automaticamente após merge.
