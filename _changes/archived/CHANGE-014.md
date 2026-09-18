change: CHANGE-014
status: MERGED
base_commit: 2bafd8c8b5279c8c1ed8e887d46d20d13ac137a5
approved_semantic_commit: 0b87a643cc5eddcfdb5a15dd19a9507df0e5b64b
approval_scope:
  - _changes/CHANGE-014.md
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

## Validation Evidence

- A skill declara compatibilidade com Semantic Git 1.5 e mantém `SEMANTIC_GIT.md` como única autoridade normativa.
- A implementação separa mapa de evidências, classificação semântica e contrato persistente; aplica subtração, gates de compressão e o gate canônico R/D/O.
- Os cenários contrastantes rejeitam inventário técnico como contrato e aceitam síntese semântica somente após os gates.
- Revisão independente restrita concluiu `PASS`, sem achados remanescentes.
- `validate_structure.py`, validação de frontmatter UTF-8 e `git diff --check` concluíram com `PASS`.
- O Git Diff está restrito a esta CHANGE e a `.opencode/skills/semantic-extraction/SKILL.md`.

- Reconciliação pré-merge executada contra a `main` em `ee5021c53378527e3a576a037db4bddb4600262b`.
- A dependência `root:CHANGE-013` está arquivada na `main` com status `MERGED`.
- O delta da `main` desde o `base_commit` não altera `.opencode/skills/semantic-extraction/SKILL.md` nem `_changes/CHANGE-014.md`; não houve conflito técnico ou semântico na reconciliação.

