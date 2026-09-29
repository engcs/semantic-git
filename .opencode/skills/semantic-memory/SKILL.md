---
name: semantic-memory
description: Use para ler, criar, reconciliar ou verificar a memória analítica nativa do Semantic Git em _memory/FINDINGS.yaml. Preserva o estado atual do conhecimento descoberto necessário para reconstruir, verificar e reavaliar R/D/O sem transformar FINDINGS em autoridade semântica ou histórico paralelo ao Git.
compatibility: Semantic Git 1.5
---

# Semantic Memory

FINDINGS é uma capacidade nativa do Semantic Git. Esta skill operacionaliza essa capacidade; toda autoridade normativa continua em `SEMANTIC_GIT.md`.

A distinção central é:

```text
R/D/O
= verdade semântica aprovada agora

_memory/FINDINGS.yaml
= estado atual do conhecimento analítico descoberto e suas evidências

Git
= evolução histórica de ambos

fontes originais
= evidência do que fisicamente ou documentalmente existiu
```

O conteúdo de um `FINDINGS.yaml` não possui autoridade sobre R/D/O. A estrutura, o ciclo de vida, as regras de evidência, UPSERT, abstração e reconciliação de FINDINGS são parte do protocolo Semantic Git.

## 1. Objetivo

Preserve o **conjunto mínimo de descobertas materiais, evidenciadas e semanticamente atômicas necessário para reconstruir, verificar e reavaliar o entendimento atual do namespace sem repetir a investigação original**.

Não preserve apenas riscos, exceções e lacunas. Conhecimento positivo pode ser indispensável, por exemplo:

- propósito;
- fato elementar;
- população;
- componentes;
- regras de contribuição;
- temporalidade;
- exclusões;
- fórmulas;
- ordem de agregação;
- recortes;
- invariantes;
- convenções;
- limites de versão;
- exceções e lacunas materiais.

Regra operacional:

```text
não guardar tudo que foi VISTO
+
guardar tudo que foi APRENDIDO e continua material para reconstrução/verificação
```

## 2. Localização

A memória é local ao Semantic Namespace:

```text
<namespace>/
├── REQUIREMENTS.md
├── DECISIONS.md
├── OPERATIONS.md
├── _changes/
└── _memory/
    └── FINDINGS.yaml
```

Nesta versão, `FINDINGS.yaml` é o único arquivo canônico permitido em `_memory/`.

`_memory`:

- não cria Semantic Namespace;
- não é quarta dimensão R/D/O;
- não participa de herança automática;
- não entra na publicação canônica por padrão;
- é versionado por Git;
- só deve existir quando houver ao menos um finding material.

## 3. Estado atual, não histórico embutido

`FINDINGS.yaml` representa o estado atual do conhecimento descoberto. Git preserva a evolução.

Exemplo:

```text
V1: F-002 = B
V2: F-002 = C
```

Se B não for mais necessário para compreender, reproduzir, verificar ou auditar nenhuma realidade atual, o arquivo corrente contém apenas C. O estado B continua recuperável por Git.

Não materialize genealogia como:

```yaml
historico:
  V1: B
  V2: C
  V3: ...
```

apenas porque as versões existiram.

Um estado histórico permanece no arquivo atual somente quando ainda governa realidade material, como dados históricos consultados, replay, auditoria, coexistência por competência ou outra aplicabilidade vigente.

Consequência desejada:

```text
após V19
FINDINGS cresce com a complexidade semântica atual
não com o número de versões passadas
```

## 4. Teste de retenção

Retenha um finding quando:

1. **Materialidade** — sua perda pode prejudicar reconstrução, verificação, distinção, delimitação, reavaliação, reimplementação ou auditoria.
2. **Evidência** — há evidência observada ou inferência sustentada; quando a própria indisponibilidade é material, registre-a como lacuna explícita.
3. **Atomicidade** — a descoberta possui identidade analítica reconhecível e pode evoluir por UPSERT.
4. **Aplicabilidade** — é possível dizer a qual realidade o finding se aplica ou declarar a aplicabilidade como não resolvida.

Risco não é requisito de retenção. `risco` é metadata opcional.

Não retenha apenas porque algo foi observado.

## 5. O que não deve virar memória

Não use `_memory` como:

- chain-of-thought;
- transcrição de sessão;
- log de passos;
- evidence map completo;
- inventário de todos os arquivos, JOINs, CTEs e campos;
- TODO;
- cópia textual de R/D/O;
- cópia de CHANGE;
- histórico V1…Vn embutido por inércia;
- substituto da fonte original;
- local oculto para tornar regra semântica autoritativa sem CHANGE.

FINDINGS registra o que foi aprendido, não o processo mental usado para chegar lá.

## 6. Schema canônico PT-BR

Use chaves estruturais em PT-BR. Preserve literais técnicos quando traduzi-los prejudicar identidade ou verificabilidade, como Git, SQL, dbt, RDO, nomes de arquivo, campos, modelos e código.

Forma recomendada:

```yaml
esquema: semantic-git-achados-v2
espaco_semantico: domain/example
autoridade: memoria_analitica_nao_autoritativa
nivel_abstracao: 0.7

alvo:
  assunto: EXEMPLO
  versao_semantica: atual

achados:
  - id: F-001
    chave: example.componente.programado
    estado: ativo
    tipo: fato_semantico

    aplica_se_a:
      versao_semantica: atual

    afirmacao: >
      PROGRAMADO representa ...

    evidencias:
      certeza: comprovada
      amostras:
        - tipo: implementacao
          artefato: modelo.sql
          localizador: linhas 120-135
          amostra: |
            CASE ... END

    semantica:
      papel: definicao_componente
      estado: candidato
      conceito: PROGRAMADO

    rdo:
      disposicao: candidato
      dimensoes:
        - decision
        - operation

    risco:
      consequencia: >
        Opcional: consequência material de esquecer o finding.
```

Campos canônicos mínimos de um finding material:

```text
id
chave
estado
tipo
aplica_se_a
afirmacao
evidencias
semantica
rdo
```

`risco` é opcional.

Use, no mínimo, estes estados de ciclo de vida:

```text
ativo
resolvido
substituido
promovido
```

`F-*` permanece identidade analítica local; não é ID R/D/O.

## 7. Evidência verificável

Todo finding material deve permitir inspeção humana sem exigir fé no resumo da IA.

Em `evidencias.amostras`, preserve ao menos uma amostra curta e diretamente ligada à afirmação:

- trecho de código;
- linha documental;
- expressão;
- witness matemático;
- registro representativo;
- resultado de teste;
- trecho curto de reconstrução que documenta prova ou lacuna.

Cada amostra deve indicar, quando disponível:

```text
tipo
artefato/fonte
localizador
amostra ou witness
trilha de origem
```

A amostra não substitui a fonte. Não copie arquivos ou consultas inteiras quando um trecho mínimo + localizador for suficiente.

Quando nenhuma amostra puder existir porque a própria evidência está indisponível, isso só é válido se o finding for precisamente a lacuna e a indisponibilidade estiver explícita.

## 8. Nível de abstração

A materialização usa:

```yaml
nivel_abstracao: 0.7
```

Valores válidos: `0.0` a `1.0`, em passos de `0.1`. Padrão operacional: `0.7`.

### 0.0

Máxima granularidade observável. Preserve mais detalhes físicos, condições intermediárias, witnesses e separação de achados. Ainda assim, não grave chain-of-thought nem dump indiscriminado.

### 0.7

Padrão equilibrado. Preserve tudo que é necessário para reconstrução e verificação sem carregar detalhe físico redundante.

### 1.0

Máxima síntese semântica. Findings correlatos podem ser fundidos quando a essência continuar correta. Pode haver perda intencional de detalhe fino de reimplementação, mas nunca ocultação de incerteza material ou invenção.

A abstração altera granularidade, não a verdade sustentada pela evidência.

## 9. Identidade e atomicidade

Use:

```yaml
id: F-005
chave: exec_prog.componente.programado
```

`id` é a identidade técnica estável do finding.

`chave` representa sua identidade analítica para UPSERT.

Não crie novo ID porque:

- a redação melhorou;
- uma nova fonte confirmou a mesma verdade;
- a certeza aumentou;
- a implementação foi refatorada sem mudar significado.

Novo `F-*` só cabe quando existe nova proposição materialmente distinta.

## 10. UPSERT e evolução

Sempre reconcilie a nova investigação com a memória existente.

```text
nova observação
→ localizar finding semanticamente equivalente
→ comparar significado e aplicabilidade
→ UPSERT ou novo finding
```

Casos:

### Mesma verdade, mesma identidade

Mantenha o mesmo finding. Acrescente ou atualize evidência quando útil.

### Evidência melhor

Mantenha o mesmo finding. Atualize `evidencias`, certeza e amostras somente no grau sustentado.

### Mudança apenas física

Mantenha a semântica. Atualize evidência se o localizador físico mudou.

### Mudança semântica da mesma identidade atual

Atualize o finding corrente para representar a realidade atual. Git preserva o estado anterior.

Se a regra anterior ainda governar realidade atual, preserve-a como variante materialmente aplicável em finding separado ou estrutura de aplicabilidade adequada; não a retenha apenas por nostalgia histórica.

### Evidência materialmente incompatível

Não sobrescreva silenciosamente. Produza drift/review explícito, preserve a evidência conflitante e reavalie a realidade aplicável.

### Nova proposição

Crie novo `F-*`.

### Finding não reencontrado

Não o apague automaticamente. Ausência de redescoberta não prova falsidade ou irrelevância.

## 11. Relação com R/D/O

FINDINGS e R/D/O têm responsabilidades diferentes:

```text
FINDINGS
= o que foi descoberto + por que acreditamos

R/D/O
= o que foi aprovado como verdade semântica
```

A relação é referencial, não espelho textual.

Exemplo após promoção:

```yaml
rdo:
  disposicao: promovido
  referencias:
    - domain/example:R-001
    - domain/example:D-004
```

Referências persistidas devem usar identidade R/D/O canônica completa.

## 12. FINDINGS → RDO: reconstrução

O conjunto de findings aplicáveis deve permitir sintetizar a essência necessária ao contrato sem reler toda a implementação.

Ao reconstruir, derive quando sustentado:

- propósito;
- fato elementar;
- população;
- componentes;
- regras de contribuição;
- temporalidade;
- exclusões;
- agregação;
- fórmula;
- invariantes;
- casos-limite;
- aplicabilidade atual.

A transformação é semântica, não textual. Não mapeie mecanicamente um finding para um item R/D/O.

Todo finding material deve possuir disposição compreensível perante o contrato: promovido, candidato, parcialmente representado, revisão, não promovido, não semântico, herdado ou equivalente governado.

## 13. RDO → FINDINGS: verificação

Quando R/D/O for criado ou editado:

1. decomponha a alteração em proposições materiais;
2. localize findings aplicáveis e conhecimento ancestral relevante;
3. compare significado;
4. classifique cada proposição.

Use no mínimo:

```text
SUSTENTADO
PARCIAL
CONTRADITO
NAO_SUSTENTADO
AMBIGUO
EVIDENCIA_DESATUALIZADA
```

`NAO_SUSTENTADO` significa ausência de prova suficiente no conhecimento preservado; não significa automaticamente falso.

`CONTRADITO` significa que existe evidência preservada materialmente incompatível.

Não transforme FINDINGS em autoridade automática. Uma divergência pode significar:

- edição incorreta do R/D/O;
- findings antigos;
- implementação alterada;
- nova versão semântica;
- TO-BE deliberado.

## 14. Investigação dirigida

Quando uma edição ficar `NAO_SUSTENTADO` ou `CONTRADITO`, ofereça investigação dirigida à hipótese.

A investigação deve buscar:

```text
evidência favorável
+
evidência capaz de refutar
+
interpretações concorrentes
```

Depois:

```text
nova evidência
→ UPSERT FINDINGS
→ reexecutar verificação RDO↔FINDINGS
```

Se não surgir sustentação suficiente, mantenha a proposição explicitamente em REVIEW/não sustentada. Não aceite por ausência de oposição.

Se a intenção for TO-BE deliberada, a divergência pode ser legítima, mas deve ser governada pelo CHANGE aplicável.

## 15. Promoção e reconciliação inversa

Um finding pode tornar-se conhecimento semântico durável somente pelo fluxo normal:

```text
finding
→ compreensão/evidência
→ CHANGE
→ revisão semântica
→ aprovação humana
→ R/D/O
```

Depois da promoção, FINDINGS continua não autoritativo perante R/D/O, mas pode preservar a descoberta, evidência e referências necessárias para futura verificação.

Quando um CHANGE modificar, remover ou substituir R/D/O referenciado por finding promovido:

- localize somente findings relacionados;
- preserve findings não relacionados;
- reconcilie referência e disposição;
- reabra a questão quando a mudança tornar a evidência incompatível;
- não permita `RECONCILED` com referência órfã ou finding afetado não examinado.

## 16. Correções humanas

Correção humana material é evidência analítica, não autoridade semântica automática.

Fluxo:

```text
clarificação humana
→ localizar finding equivalente
→ preservar F-* quando identidade continua
→ atualizar afirmação/evidência na medida sustentada
→ preservar incerteza
→ CHANGE se houver promoção material a R/D/O
```

Armazene síntese material, não transcript da conversa ou raciocínio interno.

## 17. Relação com semantic-reconstruction

Reconstrução é a principal produtora de FINDINGS.

Ela deve:

1. construir fechamento comportamental suficiente;
2. formar evidence map e modelo semântico de trabalho;
3. UPSERT no FINDINGS o conjunto mínimo de descobertas necessário à reconstrução/verificação futura;
4. produzir candidato R/D/O por síntese e subtração de herança;
5. preservar incerteza sem inventar significado.

Não copie evidence map inteiro para FINDINGS. Converta evidência em descobertas atômicas e amostras mínimas verificáveis.

## 18. Fórmulas

Quando um indicador calculável tiver uma relação matemática que expressa diretamente seu significado, preserve nos findings:

- componentes semânticos;
- relação matemática principal;
- ordem de agregação quando material;
- convenções e casos-limite relevantes;
- evidência verificável.

A fórmula humana principal pode sustentar Requirement. Decisions definem componentes e convenções. Operations descrevem materialização física.

Prefira:

```text
EXEC_PROG = EXECUTADO / PROGRAMADO
```

a uma fórmula expressa somente por aliases, colunas ou variáveis físicas.

## 19. Cadeia de decisão operacional

Para cada descoberta:

```text
1. O que foi aprendido?
2. É material para reconstrução/verificação?
   não → descartar
   sim → continuar
3. Há evidência verificável?
   não → investigar ou registrar lacuna explícita
4. Já existe finding equivalente?
   sim → comparar significado
   não → novo F-*
5. Mesma verdade?
   sim → UPSERT evidência
6. Só mudou implementação?
   sim → manter semântica
7. Mudou significado?
   sim → atualizar estado atual + verificar impacto no R/D/O
8. Estado anterior ainda é material hoje?
   sim → preservar aplicabilidade histórica vigente
   não → Git é suficiente
9. Há conflito material?
   sim → REVIEW/drift, nunca overwrite silencioso
10. Qual é a disposição perante R/D/O?
```

## 20. Invariantes

Antes de concluir uma operação de memória, verifique:

1. nenhum conhecimento material desapareceu silenciosamente;
2. nenhum finding foi criado apenas como log;
3. cada finding material possui evidência verificável ou lacuna explícita;
4. risco não foi inventado para justificar retenção;
5. findings não examinados permanecem intactos;
6. R/D/O material novo não foi aceito silenciosamente sem sustentação, ancestral aplicável ou decisão humana governada;
7. todo finding material possui disposição perante R/D/O;
8. referências promovidas existem e são canônicas;
9. Git, e não o arquivo atual, carrega a genealogia descartada;
10. `nivel_abstracao` controla compressão, não verdade;
11. nenhuma chain-of-thought foi materializada;
12. FINDINGS continua parte nativa do Semantic Git sem tornar seu conteúdo autoridade sobre R/D/O.

## 21. Resultado esperado

Uma boa memória deve permitir responder positivamente:

> Uma nova LLM, recebendo o protocolo, FINDINGS atual e ancestrais autorizados, consegue reconstruir o significado do namespace sem reler toda a implementação?

> Se o humano editar materialmente R/D/O, a LLM consegue apontar o que é sustentado, contradito, não sustentado ou ambíguo e reabrir investigação quando necessário?

> Se surgir V2, V3 ou V19, a LLM consegue atualizar o estado atual do conhecimento sem transformar FINDINGS em histórico crescente por versão?

Se não, a memória está incompleta, excessivamente abstrata ou mal reconciliada.
