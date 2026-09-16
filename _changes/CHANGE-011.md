change: CHANGE-011
status: DRAFT
base_commit: c839340b5b81891a5f0db29433cded2e89989beb
operation: BUILD_PUBLICATION
reason: null

# CHANGE-011

## Semantic Diff

### REQUIREMENTS

- **ADD** - Um namespace deve poder ser compilado em um documento único, legível e adequado para exportação em PDF.
- **ADD** - A publicação deve permitir verificar deterministicamente se continua correspondente às fontes que a produziram.
- **ADD** - A publicação deve permanecer derivada e não pode substituir README, Requirements, Decisions ou Operations como fonte de verdade.

### DECISIONS

- **ADD** - Usar `_publications/` para os artefatos de publicação do namespace.
- **ADD** - Usar `PUBLICATION.md`, `PUBLICATION.pdf` e `PUBLICATION.manifest.json` como nomes canônicos dos artefatos correspondentes.
- **ADD** - Compilar somente o README e os documentos R/D/O do namespace indicado, sem misturar automaticamente subdomínios, CHANGEs, foundations ou materializações.
- **ADD** - O manifesto deve registrar hashes do README, dos R/D/O, da especificação, do gerador e da publicação produzida.
- **ADD** - A publicação Markdown deve ser determinística; o manifesto não é fonte de verdade e não deve ser editado manualmente.
- **ADD** - A geração de PDF pode usar uma ferramenta externa de conversão e não deve impor uma dependência de PDF ao core.

### OPERATIONS

- **ADD** - Disponibilizar `_scripts/build_publication.py` com operações `build` e `status`.
- **ADD** - Aceitar `--root` como namespace a compilar e `--spec` como fonte normativa, permitindo que core e domínio estejam em locais diferentes.
- **ADD** - Executar `validate_structure.py` antes de gerar a publicação e bloquear a geração quando houver `FAIL` estrutural.
- **ADD** - Gerar `PUBLICATION.md` com README, Requirements, Decisions e Operations em ordem fixa, preservando os IDs e sem alterar as fontes.
- **ADD** - Gerar ou atualizar `PUBLICATION.manifest.json` com hashes do conteúdo atual e do resultado produzido.
- **ADD** - Informar `CURRENT`, `MISSING`, `STALE`, `DRIFT` ou `INVALID` no comando `status`.
- **ADD** - Gerar `PUBLICATION.pdf` somente quando a conversão externa for solicitada e estiver disponível.
- **ADD** - Não afirmar que a publicação está semanticamente aprovada; o script verifica compilação, estrutura e frescor.
