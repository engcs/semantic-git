change: CHANGE-005
status: DRAFT
base_commit: a1f3f96e8434c6d1bc43267382412d89c880e0cb
reason: null

# CHANGE-005

## Semantic Diff

### REQUIREMENTS

- **ADD** - Permitir que a criação inicial governada de um Semantic Namespace inexistente seja representada por um CHANGE localizado no namespace que será criado, ainda que esse namespace não exista no AS-IS do `base_commit`.
- **ADD** - Exigir que toda alteração semântica material posterior à criação inicial do namespace permaneça governada por CHANGE.

### DECISIONS

- **ADD** - Reservar `CHANGE-INIT` como identificador especial, único por namespace, para a primeira criação governada de seu AS-IS.
- **ADD** - Definir `CHANGE-INIT` como marcador do papel de inicialização semântica, e não como registro da ferramenta ou do agente que produziu a alteração.
- **ADD** - Definir que `CHANGE-INIT` não consome o primeiro identificador numérico; a primeira evolução normal do namespace utilizará `CHANGE-001`.
- **ADD** - Permitir que o CHANGE de inicialização esteja no caminho do namespace alvo na branch, mesmo quando o namespace estiver ausente do AS-IS de origem, sem exigir CHANGE ou alteração no namespace pai.
- **ADD** - Submeter `CHANGE-INIT` ao fluxo normal de branch, aprovação, implementação, RECONCILIATION, pre-merge recheck, merge e arquivamento.

### OPERATIONS

- **ADD** - Validar, antes da aprovação de `CHANGE-INIT`, que o namespace alvo não possui AS-IS no `base_commit` e que a branch adiciona seu primeiro AS-IS.
- **ADD** - Validar que `CHANGE-INIT` não altera Requirements, Decisions, Operations ou qualquer outro AS-IS de namespace ancestral.
- **ADD** - Validar que existe no máximo um `CHANGE-INIT` por identidade canônica de namespace e que ele não pode ser reutilizado.
- **ADD** - Arquivar `CHANGE-INIT` no diretório `changes/archived/` do namespace inicializado após o merge confirmado.
- **ADD** - Alocar `CHANGE-001` como primeira evolução normal quando o namespace tiver sido criado fora do Semantic Git, sem inventar ou inferir retroativamente um `CHANGE-INIT`.

## Escopo de implementação

- Alterar somente `SEMANTIC_GIT.md` para incorporar o contrato aprovado.
- Atualizar a versão normativa de 1.4 para 1.5.
- Atualizar testes conceituais e invariantes relacionados a `CHANGE-INIT`.
- Não criar `applications/mop/programacao` neste CHANGE.
- Não alterar `applications/mop` nem qualquer materialização física de aplicação.
