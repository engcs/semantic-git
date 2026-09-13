change: CHANGE-002
status: RECONCILED
base_commit: 517f643f9d56338ff5b34146671c6aaa74a946fb
approved_semantic_commit: 3dc2921a70f44a91b9055f8fcff33ccff08d7020
approval_scope:
  - SEMANTIC_GIT.md
  - changes/CHANGE-001.md
  - changes/CHANGE-002.md
reason: null

# CHANGE-002

## Semantic Diff

### REQUIREMENTS

- **ADD** - Toda CHANGE com estado `MERGED` deve ser preservada em `changes/archived/<CHANGE-ID>.md`.
- **ADD** - Nenhuma CHANGE `MERGED` pode permanecer no diretório ativo `changes/`.

### DECISIONS

- **ADD** - Usar `changes/archived/` como único caminho canônico para CHANGEs `MERGED`.
- **ADD** - Arquivar por `git mv`, preservando conteúdo semântico, identidade e histórico, sem criar o estado `ARCHIVED`.
- **ADD** - Registrar `MERGED` somente depois da validação do movimento pós-merge.
- **ADD** - Resolver referências de `approval_scope` pela mesma identidade `CHANGE-ID` após a relocação canônica.

### OPERATIONS

- **ADD** - Após o merge confirmado, a IA deve mover automaticamente a CHANGE mergeada para `changes/archived/` e validar a ausência da origem.
- **ADD** - Na entrada da regra em vigor, migrar todas as CHANGEs já `MERGED` que ainda estiverem no diretório ativo.
- **ADD** - Produzir `FAIL` se o arquivamento obrigatório não puder ser concluído ou se restar uma CHANGE `MERGED` em `changes/`.
