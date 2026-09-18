change: CHANGE-017
status: RECONCILED
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

## Validation Evidence

- A branch parte exatamente de `main` em `2f423a975ac71af1f4a1adda6c0798ae99dcd035`, está à frente e não está atrás da base.
- O conjunto contém exatamente as três responsabilidades semânticas pretendidas: `semantic-extraction`, `semantic-reconstruction` e `semantic-conceptual-review`.
- `semantic-extraction` agora se anuncia para conhecimento já expresso em fontes humanas e encaminha engenharia reversa de implementação para `semantic-reconstruction`, removendo a principal sobreposição de descoberta entre as duas skills.
- `semantic-reconstruction` preserva behavioral closure, isolamento de versão semântica, síntese determinística, subtração de herança, testes de reconstrução/reimplementação e passa a produzir explicitamente um pacote de handoff para revisão conceitual.
- `semantic-conceptual-review` recebe candidato, herança, mapa de evidências e fontes originais; forma primeiro uma narrativa conceitual do domínio, pode reabrir evidências, desafia REVIEW prematuro e diferencia KEEP/REWRITE/MERGE/SPLIT/REMOVE/ADD antes de emitir R/D/O revisado.
- A revisão conceitual não é definida como polimento de prosa e possui gates explícitos de evidência, elevação conceitual, leitura humana, reconstrução, reimplementação e não regressão.
- Os três arquivos usam caminhos e identificadores distintos e compatíveis com descoberta por skill; os frontmatters usam apenas campos portáveis já utilizados pelo projeto (`name`, `description`, `compatibility`).
- Nenhuma skill contém seleção automática, nome de fornecedor ou família específica de LLM. A revisão conceitual contém um `Capability advisory` que recomenda ao humano uma configuração de alta capacidade de raciocínio quando aplicável, sem bloquear execução.
- A seleção de modelo fica fora da skill e pode ser feita pelo host/agente/comando; portanto não foi introduzido campo `model` não interpretado no frontmatter.
- O diff da branch permanece limitado às três skills e a esta CHANGE; nenhum R/D/O de domínio, benchmark ou referência específica foi incluído.

### Reconciliation Summary

- As três skills possuem fronteiras de responsabilidade e handoffs explícitos.
- O fluxo de engenharia reversa passa a ser `semantic-reconstruction -> semantic-conceptual-review`, preservando fontes e evidências entre as etapas.
- O fluxo de conhecimento humano permanece `semantic-extraction`, com revisão conceitual opcional para contratos complexos ou de alto impacto.
- A orientação de capacidade é host-agnostic e não acopla o repositório a um modelo específico.
- Não foi identificado FAIL ou REVIEW impeditivo para a incorporação desta suite.
