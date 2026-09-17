change: CHANGE-013
status: DRAFT
base_commit: f84c5c88f7d3587f4e15d66df638d7d4eb8456cc
reason: null

# CHANGE-013

## Semantic Diff

### REQUIREMENTS

- **ADD** - A execução do Semantic Git deve seguir um protocolo operacional curto, obrigatório e sequencial antes de qualquer escrita governada.
- **ADD** - Transições de estado e gates devem ser sustentados por evidências explícitas; a IA não deve declarar estados como `RECONCILED`, `READY` ou equivalentes sem demonstrar as condições que os sustentam.
- **ADD** - Na ausência de automação dedicada, a execução deve continuar assertiva por meio de progressive disclosure, checklist normativa, autoauditoria e bloqueio explícito quando uma condição não puder ser confirmada.
- **ADD** - Regras objetivas verificáveis com Git, filesystem, referências ou metadados devem ser checadas antes de qualquer julgamento semântico por IA, mesmo quando a verificação for manual.

### DECISIONS

- **ADD** - Introduzir um `Execution Protocol` normativo e conciso em `SEMANTIC_GIT.md`, sem criar nova fonte de verdade e sem depender de scripts.
- **ADD** - Estruturar o fluxo como intenção → descoberta de namespace → contexto mínimo → identificação de CHANGE/estado → verificação de autorização → execução limitada → autoauditoria → evidências → próximo gate humano.
- **ADD** - Definir um bloco canônico de evidências para resultados de gate, incluindo identidade canônica da CHANGE, branch, commits relevantes, escopo, verificações executadas, pendências e resultado.
- **ADD** - Exigir que qualquer condição não verificada seja representada como `REVIEW`, `FAIL` ou resultado bloqueado aplicável, nunca presumida como válida.
- **ADD** - Reforçar `AGENTS.md` como interface operacional enxuta para aplicar o protocolo e consultar `SEMANTIC_GIT.md` progressivamente.

### OPERATIONS

- **ADD** - Atualizar `AGENTS.md` para exigir preflight, execução limitada por estado/autorização e autoauditoria final com evidências.
- **ADD** - Atualizar `SEMANTIC_GIT.md` com o protocolo operacional, checklist de reconciliação manual e formato mínimo de evidências.
- **ADD** - Manter a mudança exclusivamente documental/normativa; nenhum script, workflow ou automação nova deve ser criado por este CHANGE.
- **ADD** - Validar a mudança por três simulações independentes: implementação autorizada, pedido ambíguo que deve bloquear e reconciliação com inconsistência que deve produzir `REVIEW` ou `FAIL` em vez de conclusão indevida.

## Acceptance Criteria

- Existe um protocolo operacional curto e normativo que possa ser seguido sem carregar toda a especificação antecipadamente.
- `AGENTS.md` conduz o agente por preflight, execução e autoauditoria sem duplicar a especificação inteira.
- Nenhum estado de sucesso crítico pode ser declarado sem evidências mínimas explícitas.
- Condições não verificadas não podem ser tratadas como satisfeitas.
- O protocolo continua compatível com os gates e estados já definidos no Semantic Git 1.5.
- Nenhum script, workflow ou automação é adicionado.
- Três simulações independentes demonstram comportamento aderente ou expõem desvios de forma explícita.
