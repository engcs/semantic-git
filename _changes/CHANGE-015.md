change: CHANGE-015
status: DRAFT
base_commit: bbcd72aea649fe07d55cbcdbb28640bf41220147
reason: null

# CHANGE-015

## Semantic Diff

### REQUIREMENTS

- **MODIFY** - A publicação de namespace deve identificar inequivocamente o namespace publicado pelo seu caminho completo, em vez de apresentar apenas o nome do diretório terminal.
- **MODIFY** - A publicação PDF deve preservar o visual clean atual com espaçamento vertical suficiente entre itens R/D/O para leitura confortável.

### DECISIONS

- **ADD** - O título da publicação deve usar duas linhas: `GIT SEMÂNTICO:` e, abaixo, o caminho completo do namespace relativo à raiz do Semantic Repository.
- **ADD** - A melhoria de legibilidade deve ser cirúrgica: manter fundo, tipografia, cores e estrutura atuais, alterando somente o espaçamento vertical entre itens e o tratamento do título.

### OPERATIONS

- **MODIFY** - Ajustar `_scripts/build_publication.py` para resolver o caminho completo do namespace a partir da raiz Git e utilizá-lo no título da publicação Markdown/PDF.
- **MODIFY** - Aumentar somente o espaçamento posterior dos parágrafos de itens R/D/O no PDF, sem introduzir cards, painéis ou novos elementos gráficos.
- **ADD** - Validar a saída em um namespace aninhado, confirmando o título em duas linhas e a separação visual entre itens.

## Acceptance Criteria

- O título apresenta exatamente `GIT SEMÂNTICO:` na primeira linha e o caminho completo do namespace na segunda.
- Um namespace como `aderencia_execucao_framework/exec_prog/v1` não é reduzido a `V1`.
- Os itens R/D/O possuem maior respiro vertical entre si.
- Não há redesign por cards, caixas ou painéis.
- A publicação Markdown continua determinística.
- A publicação PDF mantém a identidade visual atual e permanece legível em escala de cinza.
