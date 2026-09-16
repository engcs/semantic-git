change: CHANGE-009
status: IN_PROGRESS
base_commit: 11a885ce1365839b711ef3eca5f7e7fd4f59cc92
approved_semantic_commit: de2a72576245375fc4aaac94a380a1accdc6e2ca
approval_scope:
  - SEMANTIC_GIT.md
  - AGENTS.md
  - changes/CHANGE-009.md
reason: null

# CHANGE-009

## Semantic Diff

### REQUIREMENTS

- **ADD** - O Semantic Repository deve distinguir visualmente diretórios de governança, suporte, publicação e ferramentas dos diretórios que representam domínios e subdomínios.
- **ADD** - A reorganização física deve preservar integralmente o conteúdo, a identidade e a rastreabilidade dos arquivos existentes.

### DECISIONS

- **ADD** - Usar `_changes/` como diretório canônico de CHANGEs ativas e `_changes/archived/` como seu diretório canônico de arquivamento.
- **ADD** - Usar `_foundations/` para fundamentos e materiais de suporte; metodologias de transformação devem ficar em `_foundations/transformations/`.
- **ADD** - Usar `_publications/` para publicações derivadas rastreadas, sem tratá-las como uma nova dimensão R/D/O ou como fonte de verdade.
- **ADD** - No repositório core, usar `_applications/` para aplicações de contexto e `_scripts/` para ferramentas executáveis; aplicações e subdomínios continuam sendo pastas normais dentro desses contextos.
- **ADD** - Manter `archived` sem prefixo adicional, pois sua função já é determinada pelo diretório pai `_changes/`.

### OPERATIONS

- **ADD** - Migrar os diretórios existentes com `git mv`, preservando conteúdo e histórico detectável pelo Git.
- **ADD** - Atualizar somente referências operacionais vigentes necessárias para os novos caminhos; não reescrever o conteúdo semântico de CHANGEs históricas.
- **ADD** - Atualizar `SEMANTIC_GIT.md`, `AGENTS.md` e `validate_structure.py` para reconhecer os caminhos canônicos novos.
- **ADD** - Mover `transformations/IES_RDO_Transform.md` para `_foundations/transformations/IES-RDO-TRANSFORMATION.md` e `scripts/validate_structure.py` para `_scripts/validate_structure.py`.
- **ADD** - Mover `applications/mop/` para `_applications/mop/` e aplicar `_foundations/` ao material de suporte específico da aplicação.
- **ADD** - Manter `_publications/` sem arquivo artificial até que um gerador produza uma publicação real e seu manifesto de atualização.
