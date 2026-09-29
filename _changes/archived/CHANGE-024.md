change: CHANGE-024
status: MERGED
base_commit: a49e7004172c33bc76d9ddef0cc1dc26685a1fdd
approved_semantic_commit: 6716e7d76c10e7a97e54ddf321deda1db33bd522
approval_scope:
  - _changes/CHANGE-024.md
reason: Evoluir FINDINGS para preservar conhecimento reconstruível, verificável e atual sem transformar a memória em histórico concorrente ao Git ou em autoridade concorrente ao R/D/O.
namespace: root
branch: change/root/CHANGE-024-reconstructable-memory

# CHANGE-024 - Memória reconstruível e verificável

## Escopo

Evoluir `_memory/FINDINGS.yaml` de uma memória predominantemente orientada a exceções, riscos e lacunas para uma memória reconstruível do **estado atual do conhecimento descoberto** sobre o namespace.

**FINDINGS é um componente nativo do Semantic Git.** O mecanismo FINDINGS — sua finalidade, estrutura, ciclo de vida, regras de evidência, UPSERT, abstração, reconciliação e relação com R/D/O — é definido normativamente por `SEMANTIC_GIT.md`. O que não é autoritativo perante R/D/O é o conteúdo analítico de um `FINDINGS.yaml` específico: ele registra conhecimento descoberto e evidências, não substitui a verdade semântica aprovada em Requirements, Decisions e Operations.

FINDINGS deve permanecer:

- mínimo;
- semanticamente atômico;
- evidenciado;
- reconciliável por UPSERT;
- verificável por humano e LLM;
- suficiente para reconstruir e auditar R/D/O dentro do nível de abstração escolhido;
- analítico e não autoritativo perante R/D/O;
- não histórico por padrão.

A evolução histórica do conhecimento pertence ao Git. FINDINGS só preserva estados históricos quando eles continuam materialmente necessários para compreender, reproduzir, verificar ou auditar a realidade atual.

A mudança não cria IES, ESSENCE.yaml, EVIDENCE_MAP.yaml, BEHAVIOR_MODEL.yaml ou qualquer quarta dimensão semântica persistente.

## Semantic Diff

### REQUIREMENTS

**ADD**

- **R-A** - FINDINGS deve preservar o conjunto mínimo de descobertas materiais necessário para reconstruir, verificar e reavaliar o entendimento semântico atual do namespace sem repetir a investigação original e sem competir com R/D/O.
- **R-B** - Conhecimento positivo necessário à reconstrução — como propósito, população, componentes, fórmulas, agregação e invariantes — pode permanecer em FINDINGS mesmo sem risco, exceção ou lacuna associados.
- **R-C** - Cada finding deve representar uma unidade analítica semanticamente identificável e estável, adequada a UPSERT; um finding não representa arquivo, sessão, CTE, JOIN ou resumo indiscriminado da investigação.
- **R-D** - FINDINGS deve permitir derivar uma essência transitória contendo, quando aplicável, propósito, fato elementar, população, componentes, regras de contribuição, temporalidade, exclusões, agregação, fórmulas, invariantes, versões materialmente vigentes, exceções, convenções e limites da reconstrução.
- **R-E** - Toda proposição material introduzida ou modificada em R/D/O deve poder ser confrontada com FINDINGS aplicáveis, conhecimento ancestral aplicável ou decisão humana governada explícita; ausência de sustentação, contradição, cobertura parcial ou ambiguidade deve permanecer visível.
- **R-F** - Todo finding material aplicável deve possuir disposição conhecida perante o contrato semântico, como candidato, promovido, parcialmente representado, revisão, não promovido, não semântico, herdado ou equivalente normativamente definido.
- **R-G** - Reinvestigação deve reconciliar FINDINGS por UPSERT: evidência compatível enriquece o finding existente; evidência materialmente incompatível produz drift/review explícito; nova identidade material produz novo finding.
- **R-H** - A transformação FINDINGS → R/D/O é semanticamente reversível, não textualmente reversível: o conhecimento promovido deve poder ser reconstruído e justificado sem exigir igualdade textual entre artefatos.
- **R-I** - Alterações materiais em R/D/O devem permitir localizar seletivamente findings relacionados e classificá-los quanto a coerência, cobertura, contradição, ambiguidade, obsolescência de evidência ou reabertura, preservando findings não relacionados.
- **R-J** - Um CHANGE não pode alcançar `RECONCILED` com referência promovida órfã, finding material afetado sem disposição reconciliada ou contradição material entre R/D/O e FINDINGS aplicáveis sem resolução humana governada.
- **R-K** - Quando um Requirement define o significado de um indicador calculável, ele pode expressar a fórmula semântica principal usando componentes semanticamente legíveis e estáveis; Decisions definem esses componentes e suas convenções, e Operations materializam o comportamento físico.
- **R-L** - O schema canônico de FINDINGS deve usar chaves e vocabulário estrutural em PT-BR, preservando literais técnicos sem tradução quando traduzi-los prejudicar identidade ou verificabilidade.
- **R-M** - Cada finding material deve preservar evidência mínima verificável: ao menos uma amostra curta de trecho, linha, expressão, witness, registro ou resultado, acompanhada de proveniência/localizador suficiente para reabrir a fonte original quando disponível.
- **R-N** - FINDINGS deve admitir `nivel_abstracao` de `0.0` a `1.0`, em passos de `0.1`, com padrão `0.7`. O nível controla granularidade e compressão, não a verdade considerada correta.
- **R-O** - `0.0` deve maximizar materialização observável sem armazenar chain-of-thought; `0.7` deve equilibrar reconstruibilidade, auditabilidade, legibilidade e custo de contexto; `1.0` deve maximizar síntese semântica, podendo perder detalhe de reimplementação e rastreabilidade fina de forma explícita.
- **R-P** - FINDINGS deve representar o **estado atual do conhecimento descoberto**, não o histórico interno de como cada proposição evoluiu. A história de alterações dos findings pertence ao Git.
- **R-Q** - Um estado histórico só deve permanecer materializado no FINDINGS atual quando ainda for necessário para compreender, reproduzir, verificar ou auditar alguma realidade atualmente relevante. A existência passada de uma proposição, por si só, não justifica sua retenção.
- **R-R** - O repositório deve fornecer documentação autocontida, legível por humano e LLM, explicando a filosofia, estrutura, evidência, abstração, evolução entre versões, UPSERT e verificação RDO↔FINDINGS, sem criar fonte normativa concorrente a `SEMANTIC_GIT.md`.
- **R-S** - Quando R/D/O novo ou editado não for sustentado pelos findings atuais, o protocolo deve distinguir ausência de evidência de evidência contraditória e permitir investigação dirigida à proposição alterada, procurando confirmação, refutação e interpretações concorrentes.
- **R-T** - FINDINGS deve ser tratado como capacidade nativa do Semantic Git: sua estrutura, ciclo de vida, regras de reconciliação, abstração e papel na verificação são normativos no protocolo, embora o conteúdo de cada `FINDINGS.yaml` permaneça memória analítica não autoritativa perante R/D/O.

### DECISIONS

**ADD**

- **D-A** - Definir FINDINGS como memória estruturada da descoberta necessária à reconstrução e verificação do contrato; R/D/O permanece a verdade semântica aprovada, Git preserva evolução histórica e fontes originais preservam evidência física.
- **D-B** - Manter `FINDINGS.yaml` como único arquivo canônico de `_memory`; não criar artefato persistente intermediário de essência.
- **D-C** - Tornar `risco` opcional. Retenção depende de materialidade para reconstrução, verificação, distinção, delimitação, reavaliação, reimplementação ou auditoria.
- **D-D** - Usar identidade estável por `id` e `chave` analítica; mudança de redação ou evidência não cria novo finding.
- **D-E** - Preservar somente estrutura suficiente para declarar a descoberta, sua evidência, papel semântico/analítico, aplicabilidade e disposição perante R/D/O.
- **D-F** - Tratar essência reconstruída como projeção transitória: `fontes → investigação → UPSERT FINDINGS → essência derivada → CHANGE/RDO`.
- **D-G** - No sentido inverso, tratar RDO→FINDINGS como verificação, não como geração de memória: `RDO editado → proposições → confronto com FINDINGS`.
- **D-H** - Classificar confronto no mínimo em equivalentes de `SUSTENTADO`, `PARCIAL`, `CONTRADITO`, `NAO_SUSTENTADO`, `AMBIGUO` e `EVIDENCIA_DESATUALIZADA`.
- **D-I** - Em `NAO_SUSTENTADO`, oferecer investigação dirigida ou manutenção explícita em REVIEW; em `CONTRADITO`, permitir reinvestigação da realidade, revisão da edição ou tratamento como TO-BE deliberado por CHANGE.
- **D-J** - Investigação dirigida deve testar a hipótese e também procurar evidência capaz de refutá-la ou revelar interpretação concorrente.
- **D-K** - Para indicadores calculáveis, preservar nos findings componentes semânticos e relação matemática necessários para recuperar a melhor leitura humana da fórmula.
- **D-L** - Padronizar chaves estruturais e enumerações controladas em PT-BR; nomes de arquivo, caminhos, código, identificadores, SQL, dbt, Git, RDO e termos técnicos consolidados podem permanecer literais.
- **D-M** - Estruturar evidência com `amostras`; cada amostra deve incluir tipo, artefato/fonte, localizador quando disponível e trecho mínimo legível ou witness equivalente.
- **D-N** - Definir escala de abstração: `0.0` máxima granularidade observável; `0.7` padrão equilibrado; `1.0` máxima síntese. Níveis intermediários ajustam granularidade sem autorizar invenção ou ocultação de incerteza material.
- **D-O** - Ao investigar uma nova versão, comparar a nova evidência com FINDINGS atuais: proposição igual mantém finding; evidência melhor faz UPSERT; mudança física sem mudança de significado mantém semântica; mudança semântica atualiza o conhecimento atual e pode exigir CHANGE no R/D/O; nova proposição cria novo finding.
- **D-P** - Mudança semântica da mesma identidade atualiza o finding corrente; o estado anterior fica no Git. Se o estado anterior ainda governar dados, reprocessamentos, auditoria ou outra realidade atual, ele permanece materializado com aplicabilidade explícita.
- **D-Q** - FINDINGS não deve crescer proporcionalmente ao número de versões históricas. Depois de V19, deve conter prioritariamente o conhecimento necessário ao estado atual, mais variantes históricas ainda materialmente vigentes.
- **D-R** - Criar `docs/FINDINGS.md` como guia explicativo autocontido. O documento deve declarar explicitamente que `SEMANTIC_GIT.md` continua normativo e prevalece em caso de divergência.
- **D-S** - Tratar `docs/FINDINGS.md` como guia didático de uma capacidade nativa do Semantic Git, e não como definição externa do mecanismo: toda regra necessária para operar FINDINGS deve permanecer derivável de `SEMANTIC_GIT.md`.

### OPERATIONS

**ADD**

- **O-A** - Atualizar a seção normativa de memória em `SEMANTIC_GIT.md` para refletir o modelo reconstruível, verificável e orientado a estado atual.
- **O-B** - Evoluir schema e validador de `FINDINGS.yaml` para findings positivos, `risco` opcional, PT-BR, amostras verificáveis, `nivel_abstracao`, identidade e relações R/D/O.
- **O-C** - Atualizar `semantic-memory` e `semantic-reconstruction` para materializar por UPSERT o conjunto mínimo de descobertas necessário à reconstrução e verificação, não apenas riscos, exceções e gaps.
- **O-D** - Implementar auditoria FINDINGS→RDO para detectar findings materiais sem disposição conhecida.
- **O-E** - Implementar auditoria RDO→FINDINGS para classificar sustentação, cobertura, contradição, ambiguidade e evidência desatualizada.
- **O-F** - Integrar ao gate de `RECONCILED` validação de referências órfãs/stale e reconciliação seletiva de findings materialmente afetados.
- **O-G** - Fazer `semantic-git validate` falhar para referência promovida inexistente sem depender exclusivamente da construção separada do índice.
- **O-H** - Expor `nivel_abstracao` de `0.0` a `1.0` em passos de `0.1`, padrão `0.7`, e testar materializações `0.0`, `0.7` e `1.0` sobre a mesma evidência.
- **O-I** - Adicionar teste cego em fixture semelhante a EXEC_PROG: protocolo + FINDINGS devem permitir reconstruir R/D/O materialmente equivalente sem reler implementação.
- **O-J** - Adicionar mutações de R/D/O que produzam sustentado, contradito, não sustentado e ambíguo.
- **O-K** - Adicionar teste de reinvestigação em que evidência compatível atualize finding existente e evidência incompatível exponha drift sem sobrescrita silenciosa.
- **O-L** - Adicionar teste de evolução V1→V2 em que proposição inalterada não duplica finding, proposição alterada atualiza estado corrente e Git preserva o estado anterior.
- **O-M** - Adicionar teste de retenção histórica em que regra antiga seja removida do FINDINGS atual quando deixar de ser necessária e preservada quando ainda governar realidade atual.
- **O-N** - Adicionar teste multiversão que demonstre que V1…V19 não geram histórico embutido por inércia; o tamanho da memória deve acompanhar complexidade semântica atual, não contagem de versões.
- **O-O** - Criar e manter `docs/FINDINGS.md` com definição, estado atual versus história, retenção histórica, atomicidade, UPSERT, evidência verificável, PT-BR, RDO↔FINDINGS, investigação dirigida, evolução entre versões, abstração, cadeias de decisão e invariantes.
- **O-P** - Adicionar referência a `docs/FINDINGS.md` no `README.md`, deixando claro que é guia explicativo e não fonte normativa.
- **O-Q** - Não criar IES, ESSENCE.yaml, EVIDENCE_MAP.yaml, BEHAVIOR_MODEL.yaml ou qualquer novo arquivo canônico de memória.
- **O-R** - Atualizar `SEMANTIC_GIT.md` e as skills para declarar explicitamente FINDINGS como capacidade nativa do protocolo, separando a normatividade do mecanismo da não autoridade do conteúdo analítico perante R/D/O.

## Critérios de aceitação semântica

A implementação só pode ser considerada reconciliada quando demonstrar, no mínimo:

1. FINDINGS com conhecimento positivo e lacunas sem `risco` artificial obrigatório;
2. reconstrução cega de R/D/O materialmente equivalente usando protocolo + FINDINGS + ancestrais autorizados;
3. auditoria de R/D/O editado distinguindo sustentado, parcial, contradito, não sustentado e ambíguo;
4. reinvestigação com UPSERT de evidência compatível e drift para evidência incompatível;
5. preservação de findings não afetados;
6. falha determinística para referência promovida órfã;
7. chaves estruturais em PT-BR com exceções técnicas delimitadas;
8. ao menos uma amostra verificável por finding material, salvo quando a própria indisponibilidade for a lacuna registrada;
9. materializações `0.0`, `0.7` e `1.0` da mesma evidência sem alteração de fatos sustentados;
10. fórmula humana principal de indicador podendo aparecer em Requirement, com componentes definidos em Decisions e materialização em Operations;
11. V1→V2 com finding inalterado não duplicado e finding semanticamente alterado representando apenas o estado atual quando o anterior não for mais materialmente necessário;
12. estado histórico preservado no arquivo apenas quando ainda necessário à realidade atual;
13. cenário V1…V19 sem genealogia embutida por versão e com Git suficiente para recuperar a evolução descartada do estado corrente;
14. `docs/FINDINGS.md` autocontido, referenciado pelo `README.md` e explicitamente subordinado a `SEMANTIC_GIT.md`;
15. `SEMANTIC_GIT.md` definindo FINDINGS como capacidade nativa do protocolo, enquanto cada `FINDINGS.yaml` permanece memória analítica não autoritativa perante R/D/O.

## Reconciliação final

A implementação foi reconciliada em 2026-09-29 após validação humana explícita do resultado funcional e do experimento de reconstrução do EXEC_PROG.

Evidências de fechamento:

- o responsável humano declarou a implementação aprovada e validada e autorizou a conclusão da reconciliação;
- o teste de reconstrução do EXEC_PROG foi revisado pelo humano e aceito como evidência suficiente para este CHANGE; ressalvas metodológicas identificadas durante a revisão foram conhecidas e não foram consideradas bloqueantes pela autoridade humana;
- `python _scripts/semantic_git.py validate --json` retornou `PASS` no estado implementado;
- a suíte completa `_scripts/test_*.py` executou com sucesso, incluindo schema PT-BR, `risco` opcional, amostra verificável, referência promovida órfã, índice e reconciliação;
- a branch permaneceu sem commits pendentes da `main` no recheck de reconciliação;
- não foram criados IES, `ESSENCE.yaml`, `EVIDENCE_MAP.yaml`, `BEHAVIOR_MODEL.yaml` ou nova dimensão semântica persistente;
- o escopo implementado permanece limitado à especificação, documentação, skills, validação, índice, reconciliação e testes de FINDINGS previstos por esta CHANGE.

Resultado: os critérios de aceitação foram considerados satisfeitos ou explicitamente resolvidos por validação humana governada, permitindo a transição para `RECONCILED`.

## Fora de escopo

- transformar o conteúdo de FINDINGS em autoridade semântica sobre R/D/O;
- armazenar chain-of-thought ou transcript de investigação;
- copiar integralmente evidence map para `_memory`;
- manter histórico V1…Vn dentro de cada finding apenas porque versões existiram;
- exigir persistência de todo detalhe físico fora de níveis de abstração que o justifiquem;
- criar quarta dimensão semântica persistente;
- decidir automaticamente que toda divergência entre implementação e R/D/O é nova versão semântica;
- alterar retroativamente o significado histórico da CHANGE-023.
