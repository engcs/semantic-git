change: CHANGE-012
status: DRAFT
base_commit: ba5fe680020ccb8eeef479d7738b53c5f046b2f0
operation: REFINE_PUBLICATION_PDF
reason: null

# CHANGE-012

## Semantic Diff

### REQUIREMENTS

- **ADD** - A publicação PDF deve apresentar README e R/D/O em formato legível para inspeção humana, preservando integralmente seu conteúdo.
- **ADD** - A publicação PDF deve permanecer legível quando impressa em escala de cinza ou preto e branco.
- **ADD** - A publicação PDF deve identificar o namespace, a origem documental, a data de geração e a paginação.

### DECISIONS

- **ADD** - Usar o título do README como identificação legível do namespace e apresentar as dimensões como `Requirements - <namespace>`, `Decisions - <namespace>` e `Operations - <namespace>`.
- **ADD** - Apresentar `Cabeçalho`, `Corpo` e os IDs R/D/O como elementos editoriais do documento, sem alterar o conteúdo semântico das fontes.
- **ADD** - Usar contraste suficiente para que a hierarquia visual não dependa de amarelo claro ou de cor sem equivalente legível em escala de cinza.
- **ADD** - Manter `PUBLICATION.md` como fonte textual derivada e `PUBLICATION.pdf` como sua apresentação visual derivada.

### OPERATIONS

- **ADD** - Ajustar `_scripts/build_publication.py` para renderizar o PDF com cabeçalho, rodapé, título, seções e quebras de linha adequados à leitura humana.
- **ADD** - Usar cor de destaque em tom queimado escuro, texto preto ou branco de alto contraste e elementos de borda que preservem a hierarquia na impressão monocromática.
- **ADD** - Renderizar no rodapé o nome derivado `GIT_SEMANTICO_<NAMESPACE>.md`, a data de geração e o número da página no formato `1 / N`.
- **ADD** - Testar a saída com `mop/programacao`, verificando texto extraído, paginação, legibilidade e atualização do manifesto.
- **ADD** - Manter o comportamento de frescor e não modificar README, Requirements, Decisions ou Operations durante a exportação.
