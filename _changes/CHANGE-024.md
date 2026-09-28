# CHANGE-024 - Memória reconstruível e verificável

## Metadados

```yaml
change: CHANGE-024
status: DRAFT
base_commit: a49e7004172c33bc76d9ddef0cc1dc26685a1fdd
reason: Evoluir a memória analítica para preservar o conjunto mínimo de descobertas necessário para reconstruir, verificar e reavaliar o R/D/O sem transformar FINDINGS em log ou fonte normativa concorrente.
namespace: root
branch: change/root/CHANGE-024-reconstructable-memory
```

## Escopo

Evoluir `_memory/FINDINGS.yaml` de uma memória predominantemente orientada a exceções, riscos e lacunas para uma memória de descoberta semanticamente suficiente: mínima, atômica, evidenciada, reconciliável por UPSERT e capaz de sustentar reconstrução e auditoria do R/D/O. O R/D/O continua sendo a única verdade semântica autoritativa; FINDINGS continua não normativo e não deve registrar o processo completo de investigação.

A mudança também fecha a reversibilidade operacional necessária para:

- reconstruir a essência semântica a partir de FINDINGS sem reabrir toda a investigação original;
- confrontar R/D/O novo ou editado com o conhecimento descoberto preservado;
- detectar drift quando uma nova investigação reobserva comportamento materialmente diferente;
- distinguir mudança legítima de contrato, R/D/O stale, implementação divergente e lacuna de evidência;
- impedir que `RECONCILED` seja alcançado com relações FINDINGS↔R/D/O materialmente stale ou não examinadas.

Não cria IES, ESSENCE.yaml, EVIDENCE_MAP.yaml ou qualquer quarta dimensão persistente. A essência é uma projeção derivada e transitória do conhecimento preservado em FINDINGS.

## Semantic Diff

### REQUIREMENTS

**ADD**

- **R-A** - A memória analítica de um namespace deve preservar o conjunto mínimo de descobertas materiais necessário para reconstruir, verificar e reavaliar o entendimento semântico do namespace sem repetir a investigação original, sem registrar o processo completo da investigação e sem competir com o R/D/O autoritativo.
- **R-B** - Todo conhecimento descoberto necessário para reconstruir uma proposição material do R/D/O deve poder permanecer em FINDINGS mesmo quando não representar risco, exceção ou lacuna; risco é contexto analítico opcional, não critério obrigatório de existência de um finding.
- **R-C** - Um finding deve representar uma unidade analítica semanticamente identificável e estável, suficiente para UPSERT: nova evidência da mesma descoberta deve enriquecer o mesmo finding, enquanto comportamento materialmente incompatível não pode sobrescrevê-lo silenciosamente.
- **R-D** - O conjunto de FINDINGS deve permitir derivar uma essência semântica transitória contendo, quando aplicável e sustentado, propósito, população, fato elementar, componentes, regras de contribuição, temporalidade, exclusões, agregação, fórmulas, invariantes, versões, exceções e limites necessários à reconstrução do R/D/O.
- **R-E** - Toda proposição material introduzida ou modificada em R/D/O deve poder ser confrontada com FINDINGS aplicáveis, conhecimento ancestral aplicável ou decisão humana explícita governada; ausência de sustentação, contradição, cobertura parcial ou ambiguidade material deve permanecer visível e bloquear conclusão automática como verdade reconciliada.
- **R-F** - Todo finding material aplicável deve possuir uma disposição conhecida em relação ao contrato semântico: promovido, parcialmente representado, mantido fora do R/D/O por justificativa explícita, não semântico, não resolvido, superseded ou outro estado normativamente definido que preserve sua situação sem desaparecimento silencioso.
- **R-G** - Reinvestigação deve reconciliar FINDINGS por UPSERT e detectar quando a mesma identidade analítica recebeu evidência materialmente incompatível com seu estado anterior; esse conflito deve produzir drift/review explícito em vez de substituir silenciosamente o conhecimento anterior.
- **R-H** - A transformação FINDINGS → R/D/O não precisa ser textualmente reversível, mas deve preservar equivalência do subconjunto de conhecimento promovido: a essência semanticamente derivável dos findings aplicáveis deve ser compatível com a essência semanticamente expressa pelo R/D/O, ressalvadas incertezas, conhecimento ancestral e decisões humanas governadas explícitas.
- **R-I** - Alterações materiais em R/D/O devem permitir localizar seletivamente findings relacionados e classificá-los como coerentes, contraditos, parcialmente cobertos, stale, reabertos ou não afetados; findings não relacionados devem permanecer intactos.
- **R-J** - Um CHANGE não pode alcançar `RECONCILED` quando houver finding promovido com referência órfã, finding material afetado sem reconciliação de sua disposição, ou proposição R/D/O materialmente contradita pelos findings aplicáveis sem resolução humana governada.
- **R-K** - Quando um Requirement define o significado de um indicador calculável, ele deve poder expressar a relação matemática principal usando os componentes semanticamente mais legíveis e estáveis sustentados pelo conhecimento disponível; a decomposição, definição, convenções e tratamento de casos-limite desses componentes pertencem às Decisions aplicáveis.

### DECISIONS

**ADD**

- **D-A** - Redefinir FINDINGS como memória estruturada da descoberta necessária à reconstrução e verificação do contrato, e não apenas como registro de risco/exceção; R/D/O permanece a formulação autoritativa comprimida, FINDINGS permanece não normativo e Git/fontes originais permanecem evidência do que fisicamente existiu.
- **D-B** - Manter `FINDINGS.yaml` como único arquivo canônico de `_memory` nesta versão; não criar IES ou outro artefato persistente intermediário. A essência semântica é derivada sob demanda a partir de findings, R/D/O e contexto ancestral aplicável.
- **D-C** - Tornar `risk` opcional. O critério de retenção passa a ser materialidade para reconstrução, verificação, distinção, delimitação, reavaliação ou custo/risco de redescoberta; um finding positivo e estável pode ser retido sem risco artificial quando necessário à reconstrução do entendimento.
- **D-D** - Adotar atomicidade semântica como identidade de finding: um finding representa uma proposição ou questão material identificável, não um arquivo, sessão, CTE, JOIN ou resumo indiscriminado de investigação.
- **D-E** - Preservar em cada finding somente estrutura suficiente para: declarar a descoberta, apontar evidência/proveniência, indicar papel semântico ou analítico, delimitar aplicabilidade e registrar sua relação/disposição perante R/D/O quando conhecida. Campos não sustentados não devem ser inventados.
- **D-F** - Tratar a essência reconstruída como projeção transitória, não como nova fonte de verdade. O fluxo esperado é `fontes/implementação → investigação → UPSERT FINDINGS → essência derivada → CHANGE/RDO` e, para auditoria, `RDO → proposições semânticas → confronto com FINDINGS`.
- **D-G** - Classificar o confronto RDO↔FINDINGS no mínimo em `SUPPORTED`, `PARTIAL`, `CONTRADICTED`, `UNSUPPORTED`, `AMBIGUOUS`, `STALE_EVIDENCE` ou equivalentes normativos, mantendo julgamento semântico por IA separado de verificações determinísticas de identidade, referência e estrutura.
- **D-H** - Preservar relações FINDING↔RDO como vínculo semântico referencial, não como espelho textual. Quando necessário à auditoria, a relação pode registrar natureza de cobertura/sustentação sem duplicar o texto normativo do R/D/O.
- **D-I** - Em reinvestigação, mesma identidade analítica + nova evidência compatível implica UPSERT; mesma identidade + evidência materialmente incompatível implica conflito/drift explícito; nova identidade material implica novo `F-*`.
- **D-J** - A validação de reversibilidade é semântica, não textual: não se exige `FINDINGS → RDO → FINDINGS` idêntico, mas deve ser possível justificar todas as proposições materiais do R/D/O e identificar findings materiais cuja disposição não esteja explicada.
- **D-K** - Para indicadores calculáveis, a reconstrução deve preservar nos findings os componentes semânticos e a relação matemática necessários para recuperar a melhor leitura humana da fórmula; detalhes físicos que implementam esses componentes permanecem evidência ou operação, não a fórmula semântica principal.
- **D-L** - A fórmula definidora de um indicador pode compor o Requirement quando expressa diretamente o que o indicador significa, usando componentes semânticos de alto nível; Decisions devem definir esses componentes, regras de elegibilidade, agregação, denominador zero, temporalidade e demais convenções necessárias sem rebaixar a fórmula principal a vocabulário físico.

### OPERATIONS

**ADD**

- **O-A** - Atualizar a seção normativa de memória para substituir o teste de retenção orientado predominantemente a risco por um teste de suficiência material para reconstrução/verificação, mantendo a proibição de logs, chain-of-thought, dumps completos e duplicação textual de R/D/O.
- **O-B** - Evoluir o schema/validador de `FINDINGS.yaml` para aceitar findings positivos reconstruíveis, tornar `risk` opcional, validar campos estruturais de identidade, evidência, aplicabilidade e relação semântica quando presentes e preservar compatibilidade/migração explícita dos findings existentes.
- **O-C** - Atualizar `semantic-memory` e `semantic-reconstruction` para exigir que a investigação reconcilie por UPSERT o conjunto mínimo de descobertas necessário à reconstrução do entendimento, em vez de enviar à memória somente exceções, riscos, gaps e significados não resolvidos.
- **O-D** - Implementar uma auditoria FINDINGS→RDO que identifique, para cada finding material aplicável, sua disposição no contrato e sinalize conhecimento semanticamente material sem disposição conhecida.
- **O-E** - Implementar uma auditoria RDO→FINDINGS que decomponha proposições materiais do R/D/O, localize sustentação aplicável e produza classificação de cobertura/contradição/ambiguidade, sem tratar FINDINGS como autoridade concorrente e sem inventar evidência ausente.
- **O-F** - Integrar ao gate de `RECONCILED` verificações determinísticas de referências órfãs/stale e a exigência de resultado explícito para findings materialmente afetados por MODIFY/REMOVE/REPLACE; conflitos semânticos materiais devem exigir revisão humana.
- **O-G** - Integrar reinvestigação e UPSERT para detectar evidência materialmente incompatível com finding existente e expor semantic drift, preservando a descoberta anterior no histórico Git e evitando sobrescrita silenciosa.
- **O-H** - Adicionar testes de round-trip semântico com fixture semelhante a EXEC_PROG: reconstruir R/D/O usando somente protocolo + FINDINGS; editar proposições do R/D/O e verificar detecção de supported/contradicted/unsupported; reobservar implementação alterada e verificar drift; preservar findings não relacionados.
- **O-I** - Adicionar teste de cobertura que prove que conhecimento positivo essencial — como propósito, definição de componentes, fórmula, agregação e invariantes — pode existir em FINDINGS sem `risk` artificial e é suficiente para reconstruir o R/D/O correspondente.
- **O-J** - Corrigir o fechamento referencial demonstrado no teste de EXEC_PROG: `semantic-git validate` deve falhar quando um finding promovido referencia entidade R/D/O removida ou inexistente, sem depender exclusivamente de uma construção separada do índice.
- **O-K** - Não criar novos arquivos permanentes de memória nem introduzir IES como requisito de entrada, saída ou persistência do protocolo nesta mudança.
- **O-L** - Atualizar a separação canônica R/D/O para permitir e orientar que Requirements de indicadores calculáveis expressem a fórmula semântica principal, mantendo em Decisions a definição dos componentes e convenções e em Operations a materialização física.

## Critérios de aceitação semântica

A implementação futura desta CHANGE só pode ser considerada semanticamente reconciliada quando demonstrar, no mínimo:

1. um `FINDINGS.yaml` contendo conhecimento positivo e lacunas sem obrigatoriedade artificial de `risk` em todos os itens;
2. reconstrução cega de um R/D/O materialmente equivalente a partir apenas de `SEMANTIC_GIT.md` + FINDINGS + ancestrais explicitamente autorizados;
3. auditoria de um R/D/O manualmente alterado que identifique proposições sustentadas, contraditas, sem sustentação e ambíguas;
4. reinvestigação que faça UPSERT de evidência compatível e sinalize drift para evidência incompatível;
5. preservação integral de findings não examinados/não relacionados;
6. falha determinística para referência promovida órfã ou stale;
7. ausência de novos artefatos persistentes como IES/ESSENCE fora de `FINDINGS.yaml` e R/D/O;
8. reconstrução de um indicador cuja fórmula humana principal apareça em Requirement e cujos componentes sejam definidos nas Decisions sem nomes físicos.

## Fora de escopo

- transformar FINDINGS em autoridade semântica;
- armazenar chain-of-thought ou transcript de investigação;
- copiar integralmente evidence map para `_memory`;
- exigir que todo detalhe físico observado seja persistido;
- criar `IES.yaml`, `ESSENCE.yaml`, `BEHAVIOR_MODEL.yaml` ou equivalente;
- decidir automaticamente que toda divergência entre implementação e R/D/O é nova versão semântica;
- alterar retroativamente o significado histórico da CHANGE-023.
