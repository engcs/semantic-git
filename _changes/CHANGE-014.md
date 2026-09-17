change: CHANGE-014
status: DRAFT
base_commit: 2bafd8c8b5279c8c1ed8e887d46d20d13ac137a5
depends_on:
  - root:CHANGE-013
reason: null

# CHANGE-014

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - A extração semântica assistida deve produzir conhecimento conciso, compreensível por humanos e suficiente para reconstruir o significado relevante sem consultar a implementação.
- **ADD R-B** - Evidências físicas devem sustentar a extração sem integrar automaticamente o contrato semântico resultante.
- **ADD R-C** - A extração deve preservar somente conhecimento próprio do namespace, subtraindo herança, detalhes substituíveis e fatos físicos sem significado duradouro.

### DECISIONS

- **ADD D-A** - Criar uma skill derivada de `SEMANTIC_GIT.md` que conduza a investigação ampla e a síntese mínima, sem constituir fonte normativa paralela. Atende R-A, R-B e R-C.
- **ADD D-B** - Separar explicitamente mapa de evidências, classificação semântica e contrato persistente; somente o último compõe o R/D/O ou Semantic Diff. Atende R-B.
- **ADD D-C** - Aplicar testes de herança, reimplementação, leitura humana, reconstruibilidade e compressão antes de apresentar o resultado. Atende R-A e R-C.

### OPERATIONS

- **ADD O-A** - Disponibilizar a skill em `.opencode/skills/semantic-extraction/SKILL.md`, com gatilhos para extração de essência semântica a partir de código, dados, documentos ou materializações.
- **ADD O-B** - Orientar a skill a investigar evidências, classificar cada achado, formar propósito, fatos, variáveis, população, regras e recortes, subtrair herança e eliminar detalhes substituíveis antes de escrever R/D/O ou CHANGE.
- **ADD O-C** - Incluir critérios negativos para impedir que lineage, caminhos, tabelas, colunas, flags, SQL, debug e outros detalhes físicos sejam promovidos por padrão ao contrato.
- **ADD O-D** - Validar a skill por cenários contrastantes de extração mecânica e extração semanticamente econômica, verificando fidelidade, concisão e utilidade humana.
