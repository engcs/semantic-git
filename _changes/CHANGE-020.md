change: CHANGE-020
status: DRAFT
base_commit: 1099f6bc2c4b915af40610bff9074ff88ee707c7
approved_semantic_commit: null
approval_scope: null
reason: null

# CHANGE-020

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - O Semantic Git deve oferecer uma capacidade especializada de investigação matemática para regras quantitativas, fórmulas, agregações, limites e funções presentes em conhecimento semântico ou em sua materialização, com o objetivo de detectar situações em que o resultado não esteja matematicamente bem definido, seja contraditório ou dependa de convenção não explicitada.
- **ADD R-B** - A investigação deve abranger, quando aplicável, operações fora do domínio, divisão por zero e `0/0`, funções parciais, lacunas e sobreposições em regras por casos, fronteiras abertas ou fechadas, múltiplos resultados possíveis para a mesma entrada, contradições entre fórmulas, dependência da ordem de agregação, arredondamento ou truncamento não especificado e incompatibilidade dimensional material.
- **ADD R-C** - Todo gap matemático material deve ser rastreável à regra ou evidência analisada e, sempre que possível, acompanhado de prova, condição de domínio, contraexemplo ou entrada testemunha que demonstre concretamente a indeterminação ou inconsistência.
- **ADD R-D** - A análise deve distinguir comportamento matemático, comportamento físico da implementação e significado semântico. Um banco, linguagem ou engine produzir `NULL`, erro, infinito, arredondamento ou qualquer fallback não transforma esse comportamento físico em regra de domínio por si só.
- **ADD R-E** - A capacidade matemática não deve inventar a resolução de uma indeterminação. Quando mais de uma convenção semanticamente plausível puder fechar o gap, o resultado deve permanecer explícito como decisão semântica pendente de evidência ou validação humana.
- **ADD R-F** - Gaps matemáticos materiais que sejam caros ou perigosos de esquecer e ainda não pertençam ao R/D/O devem poder ser preservados em `_memory/FINDINGS.yaml` por meio de `semantic-memory`, sem duplicar conhecimento já normativamente representado em R/D/O.
- **ADD R-G** - A investigação matemática deve ser transversal e acionável sob demanda, não uma quarta etapa obrigatória do pipeline. Ela deve poder ser utilizada isoladamente ou por `semantic-reconstruction` e `semantic-conceptual-review` quando o objeto investigado contiver lógica quantitativa material.

### DECISIONS

- **ADD D-A** - Criar a skill `semantic-mathematical-review` como capacidade especializada de análise de consistência e determinação matemática, subordinada a `SEMANTIC_GIT.md` e complementar às skills semânticas existentes. Atende R-A e R-G.
- **ADD D-B** - Classificar achados, conforme aplicável, em famílias analíticas como `undefined_domain`, `underdetermined`, `contradiction`, `boundary_gap`, `overlap`, `aggregation_order`, `precision_unspecified` e `dimensional_inconsistency`. Essas classificações são analíticas e não criam nova taxonomia normativa R/D/O. Atende R-B.
- **ADD D-C** - Avaliar fórmulas sobre o domínio admissível sustentado pelas evidências. Quando o domínio de entrada não puder ser provado, expressar o achado condicionalmente em vez de assumir valores impossíveis ou inventar restrições ausentes. Atende R-C e R-E.
- **ADD D-D** - Exigir que um achado material registre a expressão ou regra afetada, a condição que o ativa e a consequência observável. Preferir contraexemplo concreto ou região de domínio quando isso tornar a falha verificável; uma prova simbólica suficiente pode substituir o exemplo concreto. Atende R-C.
- **ADD D-E** - Tratar semântica específica de engine, representação de `NULL`, overflow, infinito, precisão numérica ou ordem física de execução como evidência de implementação, não como resolução automática da regra matemática ou de negócio. Atende R-D.
- **ADD D-F** - Quando a inconsistência tiver resolução única já sustentada por R/D/O aplicável, tratá-la como divergência da materialização; quando houver múltiplas resoluções semanticamente plausíveis, produzir `REVIEW` ou finding analítico em vez de escolher arbitrariamente. Atende R-D e R-E.
- **ADD D-G** - Persistir em `_memory` apenas gaps materiais que satisfaçam os critérios de retenção de `semantic-memory`, usando identidade `F-*` e risco concreto; não persistir o checklist inteiro, resultados triviais ou verificações que passaram. Atende R-F.
- **ADD D-H** - Após uma resolução ser promovida e adequadamente representada em R/D/O, o finding matemático correspondente pode permanecer somente como `promoted` para proveniência, sem manter uma segunda cópia ativa da regra. Atende R-F.

### OPERATIONS

- **ADD O-A** - Criar `.opencode/skills/semantic-mathematical-review/SKILL.md` com procedimento para identificar domínio admissível, normalizar a regra quantitativa, testar totalidade e unicidade do resultado, procurar contradições, fronteiras, ordem de agregação, precisão e dimensões, e produzir evidência verificável para cada achado.
- **ADD O-B** - Documentar na skill um fluxo mínimo `regra -> domínio -> casos de fronteira -> prova/contraexemplo -> consequência -> classificação -> decisão sobre REVIEW/memory`, proibindo a escolha automática de convenção de negócio ausente.
- **ADD O-C** - Atualizar `AGENTS.md` para orientar a IA a usar `semantic-mathematical-review` quando o humano pedir gaps matemáticos, inconsistências quantitativas, indeterminações, casos de fronteira ou quando uma investigação semântica encontrar fórmulas cujo comportamento total não esteja demonstrado.
- **ADD O-D** - Atualizar `semantic-reconstruction` para poder delegar investigação matemática quando o comportamento reconstruído depender de fórmulas, agregações ou funções parciais, preservando separadamente comportamento físico e significado semântico.
- **ADD O-E** - Atualizar `semantic-conceptual-review` para desafiar contratos quantitativos que aparentem estar completos mas não determinem resultado para todo o domínio aplicável, e para usar achados matemáticos como evidência de incompletude sem transformá-los automaticamente em regra de negócio.
- **ADD O-F** - Atualizar `semantic-memory` somente o necessário para reconhecer gaps matemáticos como candidatos válidos de retenção e orientar sua consulta em perguntas sobre fragilidades quantitativas conhecidas, mantendo as regras atuais de não autoridade, upsert e exclusividade com R/D/O.
- **ADD O-G** - Adicionar exemplos e validações da skill cobrindo ao menos: denominador zero e `0/0`; regra por casos com intervalo sem cobertura; regras sobrepostas com resultados diferentes; diferença entre média de razões e razão das somas; arredondamento em etapas distintas; e unidade/dimensão incompatível.
- **ADD O-H** - Preferir verificações determinísticas ou simbólicas quando a propriedade puder ser provada mecanicamente e utilizar julgamento por IA somente para interpretar significado, domínio admissível, materialidade e necessidade de decisão humana.
- **ADD O-I** - Não criar `_memory` nem alterar R/D/O apenas porque a skill foi executada; escrita persistente deve ocorrer somente quando houver finding material ou mudança semântica governada pelos mecanismos já existentes.
