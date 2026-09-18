change: CHANGE-017
status: APPROVED
base_commit: 2f423a975ac71af1f4a1adda6c0798ae99dcd035
approved_semantic_commit: ce5283493815ae05f646ad2fe9062c0e1f1ca12f
approval_scope:
  - _changes/CHANGE-017.md
depends_on:
  - root:CHANGE-014
  - root:CHANGE-016
reason: null

# CHANGE-017

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - O conjunto de skills semânticas deve distinguir explicitamente três atividades: extração de conhecimento já expresso, reconstrução de conhecimento implícito em implementação existente e revisão conceitual de um contrato candidato.
- **ADD R-B** - A revisão conceitual deve elevar um modelo comportamental a um contrato de domínio mais humano sem reduzir fidelidade, evidência, reconstruibilidade ou independência da implementação.
- **ADD R-C** - As três skills devem possuir fronteiras e handoffs explícitos para que o agente selecione a atividade correta e preserve os artefatos necessários entre etapas.
- **ADD R-D** - Atividades de maior exigência conceitual devem poder recomendar ao humano o uso de maior capacidade de raciocínio sem acoplar as skills a fornecedor, família ou nome específico de modelo.

### DECISIONS

- **ADD D-A** - Manter `semantic-extraction` para conhecimento já explicitado em fontes humanas, `semantic-reconstruction` para engenharia reversa de comportamento implementado e criar `semantic-conceptual-review` para crítica, abstração e síntese conceitual de R/D/O candidato. Atende R-A e R-C.
- **ADD D-B** - Fazer a revisão conceitual receber o contrato candidato, o mapa de evidências e acesso às fontes originais relevantes, permitindo reabrir a investigação quando detectar perda, ambiguidade ou abstração insuficiente. Atende R-B e R-C.
- **ADD D-C** - Proibir que `semantic-conceptual-review` funcione como simples reescrita estilística: ela deve poder fundir conceitos equivalentes, elevar propósito, contestar REVIEW prematuro, remover linguagem física residual e detectar conhecimento ausente. Atende R-B.
- **ADD D-D** - Tratar seleção de modelo como responsabilidade do host/agente/comando, não da skill. A skill de revisão deve emitir uma recomendação curta ao humano quando uma etapa se beneficiar materialmente de maior capacidade de raciocínio e o ambiente não garantir essa capacidade. Atende R-D.

### OPERATIONS

- **ADD O-A** - Criar `.opencode/skills/semantic-conceptual-review/SKILL.md` com instruções de revisão conceitual baseada em evidência e fontes originais.
- **ADD O-B** - Ajustar as descrições e os handoffs de `semantic-extraction` e `semantic-reconstruction` para diferenciar claramente quando cada skill deve ser usada e quando encaminhar para revisão conceitual.
- **ADD O-C** - Na revisão conceitual, formar primeiro uma explicação coerente do domínio em linguagem humana e somente depois produzir o R/D/O revisado.
- **ADD O-D** - Implementar orientação de capacidade independente de modelo: recomendar um modelo/configuração de alta capacidade de raciocínio para revisão conceitual, sem assumir que a skill pode trocar o modelo em execução.
- **ADD O-E** - Validar descoberta e compatibilidade das três skills verificando caminho, identificador, frontmatter reconhecido, descrições não sobrepostas, handoffs e ausência de dependência em modelo específico.
