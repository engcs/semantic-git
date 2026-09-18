change: CHANGE-015
status: RECONCILED
base_commit: bbcd72aea649fe07d55cbcdbb28640bf41220147
approved_semantic_commit: 1332c4c5e99384bd3204aca9668e2dcd0e11a6cc
approval_scope:
  - _changes/CHANGE-015.md
reason: null

# CHANGE-015

## Semantic Diff

### REQUIREMENTS

- **MODIFY** - A publicação de namespace deve identificar inequivocamente o namespace publicado pelo seu caminho completo, em vez de apresentar apenas o nome do diretório terminal.
- **MODIFY** - A publicação PDF deve preservar o visual clean atual com espaçamento vertical suficiente entre itens R/D/O para leitura confortável.
- **ADD** - A publicação PDF deve registrar visivelmente o caminho absoluto completo do `PUBLICATION.md` que originou a renderização, sem truncamento.

### DECISIONS

- **ADD** - O título da publicação deve usar duas linhas: `GIT SEMÂNTICO:` e, abaixo, o caminho completo do namespace relativo à raiz do Semantic Repository.
- **ADD** - Na publicação derivada, os títulos das dimensões devem aparecer somente como `Requirements`, `Decisions` e `Operations`; o caminho do namespace permanece nos documentos R/D/O canônicos, mas não deve ser repetido nos títulos da publicação.
- **ADD** - A melhoria de legibilidade deve ser cirúrgica: manter fundo, tipografia, cores e estrutura atuais, alterando somente espaçamento vertical, tratamento do título e identificação da fonte.
- **ADD** - O cabeçalho do PDF deve exibir `Fonte da publicação: <caminho absoluto de PUBLICATION.md>`; caminhos longos devem quebrar linha sem perda de caracteres.
- **ADD** - Metadados internos adicionais do PDF ficam fora do escopo desta CHANGE.

### OPERATIONS

- **MODIFY** - Ajustar `_scripts/build_publication.py` para resolver o caminho completo do namespace a partir da raiz Git e utilizá-lo no título da publicação Markdown/PDF.
- **MODIFY** - Simplificar somente na publicação derivada os títulos R/D/O, sem modificar `REQUIREMENTS.md`, `DECISIONS.md` ou `OPERATIONS.md`.
- **MODIFY** - Aumentar o espaçamento posterior dos parágrafos de itens R/D/O no PDF, sem introduzir cards, painéis ou novos elementos gráficos.
- **MODIFY** - Substituir o rótulo sintético `GIT_SEMANTICO_<NAMESPACE>.md` pelo caminho absoluto completo do `PUBLICATION.md` no cabeçalho do PDF, com quebra automática quando necessário.
- **ADD** - Validar a saída em namespace aninhado, confirmando título, fonte completa, títulos simplificados e separação visual entre itens.

## Acceptance Criteria

- O título apresenta exatamente `GIT SEMÂNTICO:` na primeira linha e o caminho completo do namespace na segunda.
- Um namespace como `aderencia_execucao_framework/exec_prog/v1` não é reduzido a `V1`.
- A publicação mostra `Requirements`, `Decisions` e `Operations` sem repetir o caminho do namespace.
- Os itens R/D/O possuem maior respiro vertical entre si.
- O cabeçalho mostra o caminho absoluto completo do `PUBLICATION.md`, sem reticências ou truncamento e com quebra de linha quando necessária.
- Não há redesign por cards, caixas ou painéis.
- A publicação Markdown continua determinística.
- A publicação PDF mantém a identidade visual atual e permanece legível em escala de cinza.
- Nenhum metadado interno adicional de PDF é introduzido nesta CHANGE.

## Validation Evidence

- O contrato aprovado está ancorado em `approved_semantic_commit: 1332c4c5e99384bd3204aca9668e2dcd0e11a6cc` e o escopo aprovado permanece restrito a esta CHANGE.
- O Git Diff da branch está restrito a `_changes/CHANGE-015.md` e `_scripts/build_publication.py`.
- O caminho de renderização alterado foi reproduzido localmente com o namespace aninhado `aderencia_execucao_framework/exec_prog/v1`.
- A publicação resultante apresentou `GIT SEMÂNTICO:` e o caminho completo do namespace em linha própria.
- Os títulos derivados apareceram como `Requirements`, `Decisions` e `Operations`, sem alterar os títulos canônicos dos arquivos R/D/O de origem.
- A tipografia foi reduzida de forma moderada (`heading` 17 pt, namespace 10,5 pt, subheading 13 pt e corpo 9,5 pt) e o espaçamento posterior entre itens foi mantido em 8 pt, preservando o visual clean sem cards ou painéis.
- O cabeçalho exibiu `Fonte da publicação:` seguido do caminho absoluto completo do `PUBLICATION.md`; pontos de quebra invisíveis são inseridos após separadores de caminho para permitir quebra em múltiplas linhas sem remoção de caracteres.
- O PDF de validação principal passou de 3 para 2 páginas após o refinamento tipográfico e foi inspecionado visualmente; não foram observados cortes, sobreposições ou glyphs quebrados.
- Um segundo teste com caminho absoluto artificialmente longo confirmou quebra em múltiplas linhas no cabeçalho sem truncamento; o harness local usado para validar o caminho de renderização passou em `py_compile`.
- O diff final não introduz metadados internos adicionais de PDF.

### Reconciliation Summary

- Semantic Diff aprovado e Git Diff permanecem compatíveis.
- Nenhum arquivo R/D/O, regra semântica de domínio ou outro gerador foi alterado.
- A alteração permanece exclusivamente na apresentação derivada da publicação.
- Não há `FAIL` ou `REVIEW` impeditivo identificado para esta implementação.
