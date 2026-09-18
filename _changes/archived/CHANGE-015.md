change: CHANGE-015
status: MERGED
base_commit: bbcd72aea649fe07d55cbcdbb28640bf41220147
approved_semantic_commit: e5246a6775618f39d843bba33d5cb59a6e776ddb
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
- **ADD** - A renderização PDF deve oferecer paletas selecionáveis por `--theme`, com `blue` como padrão para leitura digital e `mono` para impressão monocromática; a escolha de tema não altera o conteúdo nem a estrutura da publicação.
- **ADD** - O tema efetivamente usado deve ser registrado no manifesto da publicação para preservar rastreabilidade do artefato visual.
- **ADD** - Metadados internos adicionais do PDF ficam fora do escopo desta CHANGE.

### OPERATIONS

- **MODIFY** - Ajustar `_scripts/build_publication.py` para resolver o caminho completo do namespace a partir da raiz Git e utilizá-lo no título da publicação Markdown/PDF.
- **MODIFY** - Simplificar somente na publicação derivada os títulos R/D/O, sem modificar `REQUIREMENTS.md`, `DECISIONS.md` ou `OPERATIONS.md`.
- **MODIFY** - Aumentar o espaçamento posterior dos parágrafos de itens R/D/O no PDF, sem introduzir cards, painéis ou novos elementos gráficos.
- **MODIFY** - Substituir o rótulo sintético `GIT_SEMANTICO_<NAMESPACE>.md` pelo caminho absoluto completo do `PUBLICATION.md` no cabeçalho do PDF, com quebra automática quando necessário.
- **ADD** - Adicionar `--theme {blue,mono}` ao comando `build`, usando `blue` por padrão e aplicando a paleta escolhida apenas ao PDF.
- **ADD** - Registrar o tema selecionado na entrada `pdf` do `PUBLICATION.manifest.json`.
- **ADD** - Validar a saída em namespace aninhado nos temas `blue` e `mono`, confirmando título, fonte completa, títulos simplificados, separação visual entre itens e equivalência estrutural entre as duas renderizações.

## Acceptance Criteria

- O título apresenta exatamente `GIT SEMÂNTICO:` na primeira linha e o caminho completo do namespace na segunda.
- Um namespace como `aderencia_execucao_framework/exec_prog/v1` não é reduzido a `V1`.
- A publicação mostra `Requirements`, `Decisions` e `Operations` sem repetir o caminho do namespace.
- Os itens R/D/O possuem maior respiro vertical entre si.
- O cabeçalho mostra o caminho absoluto completo do `PUBLICATION.md`, sem reticências ou truncamento e com quebra de linha quando necessária.
- Não há redesign por cards, caixas ou painéis.
- A publicação Markdown continua determinística.
- A publicação PDF mantém a identidade visual atual e permanece legível em escala de cinza.
- `--theme blue` é o padrão e `--theme mono` produz a mesma publicação em paleta monocromática apropriada para impressão.
- O manifesto registra o tema usado para gerar o PDF.
- Nenhum metadado interno adicional de PDF é introduzido nesta CHANGE.

## Validation Evidence

- O contrato refinado aprovado está ancorado em `approved_semantic_commit: e5246a6775618f39d843bba33d5cb59a6e776ddb`.
- O Git Diff permanece restrito a `_changes/CHANGE-015.md` e `_scripts/build_publication.py`.
- O comando `build` oferece `--theme {blue,mono}`, com `blue` como padrão.
- A paleta `blue` usa azul-marinho nos títulos, azul discreto nos subtítulos, texto azul-acinzentado escuro e divisores azul-acinzentados, sem alterar o layout.
- A paleta `mono` usa somente preto e cinza e preserva a mesma hierarquia e espaçamento da versão colorida.
- O tema selecionado é registrado em `pdf.theme` no `PUBLICATION.manifest.json`.
- O Markdown gerado é independente do tema; somente a renderização PDF é afetada.
- A quebra do caminho absoluto de `PUBLICATION.md` permanece ativa nos dois temas, sem truncamento.
- Um harness local equivalente ao caminho de renderização passou em `py_compile` e gerou os temas `blue` e `mono` com 2 páginas cada.
- As duas renderizações foram inspecionadas visualmente após renderização para PNG; não foram observados cortes, sobreposições ou glyphs quebrados.
- Quando ReportLab não estiver disponível, o fallback Pandoc é permitido somente para `mono`; `blue` bloqueia em vez de produzir uma paleta incorreta silenciosamente.
- Nenhum metadado interno adicional de PDF foi introduzido.

### Reconciliation Summary

- Semantic Diff aprovado e Git Diff permanecem compatíveis.
- Nenhum arquivo R/D/O ou regra semântica de domínio foi alterado.
- O refinamento permanece limitado à apresentação derivada e à seleção explícita de paleta.
- Não há `FAIL` ou `REVIEW` impeditivo identificado.
