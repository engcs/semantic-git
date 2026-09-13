change: CHANGE-001
status: APPROVED
base_commit: 7b6290a996937013a111ea9a0c969939de2516f8
approved_semantic_commit: cdc1b0c4e971f9ffa070e317e76817902229d18b
approval_scope:
  - SEMANTIC_GIT.md
  - AGENTS.md
  - README.md
  - applications/mop/README.md
  - changes/CHANGE-001.md
reason: null

# CHANGE-001

## Semantic Diff

### REQUIREMENTS

- **ADD** - Tornar o padrão documental usado pelo MOP o padrão global para documentos permanentes de Semantic Namespaces.
- **ADD** - Tornar `README.md` opcional e restrito à orientação essencial.
- **ADD** - Impedir a cópia textual de Requirements ancestrais para namespaces descendentes.
- **ADD** - Impedir a reutilização, por namespace descendente, de ID oficial do mesmo tipo usado por namespace ancestral.
- **ADD** - Retornar o mesmo CHANGE à `DRAFT` quando uma alteração material for identificada antes de `MERGED` dentro do mesmo escopo semântico.

### DECISIONS

- **ADD** - Usar exclusivamente `README.md`, `REQUIREMENTS.md`, `DECISIONS.md` e `OPERATIONS.md` como nomes canônicos do AS-IS, com a estrutura documental única definida na seção 23.3 de `SEMANTIC_GIT.md`.
- **ADD** - Rejeitar como `FAIL` nomes, estruturas, seções, itens, IDs, referências e tipos documentais permanentes não previstos.
- **ADD** - Separar validação estrutural determinística de síntese semântica por IA, sem permitir que a IA converta uma violação estrutural em conteúdo válido.
- **ADD** - Exigir branch exclusiva para cada CHANGE semântico material, usando a convenção operacional `change/<CHANGE-ID>-<slug-curto>` sem derivar namespace ou escopo do nome da branch.
- **ADD** - Manter o mesmo CHANGE-ID, a mesma branch e o mesmo `base_commit` em novo ciclo pré-merge, preservando as aprovações anteriores no histórico.

### OPERATIONS

- **ADD** - Aplicar a validação estrutural canônica antes de a IA interpretar ou reorganizar um namespace.
- **ADD** - Seguir o fluxo `branch exclusiva → CHANGE / DRAFT → proposta e análise de gaps → validação humana → implementação definitiva → RECONCILIATION → merge`.
- **ADD** - Manter `main` como AS-IS e a branch como TO-BE até a incorporação; não tratar proposta ou análise de gaps como implementação definitiva.
- **ADD** - Após alteração material antes de `MERGED`, atualizar o Semantic Diff, obter nova validação e novo `approved_semantic_commit`, implementar somente o delta e executar RECONCILIATION completa.
