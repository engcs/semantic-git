change: CHANGE-008
status: IN_PROGRESS
base_commit: 345b4615b94dc0699b7965c55af3f13c6da82b2e
approved_semantic_commit: 31997d29462aa0eea404bbbc930ae4cf58f8837c
approval_scope:
  - SEMANTIC_GIT.md
  - changes/CHANGE-008.md
reason: null

# CHANGE-008

## Semantic Diff

### REQUIREMENTS

- **ADD** - Cada namespace deve separar verdades e invariantes estáveis, escolhas conceituais e operações de cálculo ou materialização.
- **ADD** - O R/D/O de um namespace deve conter somente o conhecimento comum ao seu próprio domínio; detalhes específicos devem permanecer no consumidor ou subdomínio correspondente.
- **ADD** - A classificação de uma regra deve distinguir conceito semântico de materialização física antes da conclusão do R/D/O.

### DECISIONS

- **ADD** - Requirements devem expressar somente verdades, necessidades e invariantes estáveis, sem detalhes físicos, nomes de consumidores ou regras específicas de indicadores.
- **ADD** - Decisions devem expressar escolhas conceituais, definições, fórmulas abstratas, convenções e critérios de identidade, sem colunas, tabelas, SQL, modelos, formatos físicos ou mapeamentos.
- **ADD** - Regras que puderem ser expressas matematicamente devem ser formuladas com conceitos abstratos; a composição física do resultado pertence a Operations.
- **ADD** - O domínio pai deve usar referências genéricas como consumidor, uso especializado ou aplicação, sem citar nominalmente seus subdomínios.
- **ADD** - Dúvida material sobre a camada correta deve permanecer como REVIEW, sem decisão arbitrária.

### OPERATIONS

- **ADD** - Antes de escrever ou concluir R/D/O, determinar o namespace, seu nível de abstração, o conhecimento comum, os consumidores e a distinção entre conceito e materialização.
- **ADD** - Registrar em Operations os cálculos, transformações e materializações, incluindo campos, tabelas, funções, modelos, fórmulas físicas, mapeamentos e validações técnicas quando aplicáveis.
- **ADD** - Verificar antes da conclusão que todo Requirement possui Decision correspondente, toda Decision materializada possui Operation correspondente e nenhuma Operation cria regra semântica nova.
- **ADD** - Verificar que o R/D/O contém somente conceitos comuns ao namespace e que detalhes específicos foram deslocados para o consumidor correto.
- **ADD** - Apresentar o RDO somente após o gate de separação e listar todo item ainda classificado como REVIEW.
