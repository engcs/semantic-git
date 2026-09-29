# FINDINGS — memória reconstruível de conhecimento

> Este documento é explicativo. A fonte normativa do Semantic Git continua sendo [`SEMANTIC_GIT.md`](../SEMANTIC_GIT.md). Em caso de divergência, prevalece a especificação normativa.

## 1. O que é FINDINGS

FINDINGS é um **componente nativo do Semantic Git**. O protocolo define normativamente sua finalidade, estrutura, ciclo de vida, evidência, abstração e reconciliação; este guia apenas explica essa capacidade.

`_memory/FINDINGS.yaml` é a memória analítica materializada de um namespace e seu conteúdo permanece não autoritativo perante R/D/O.

Seu objetivo é preservar o **conjunto mínimo de descobertas materiais necessário para reconstruir, verificar e reavaliar o entendimento semântico atual do namespace sem repetir a investigação original**.

FINDINGS não é o contrato semântico oficial. A autoridade permanece em `REQUIREMENTS.md`, `DECISIONS.md` e `OPERATIONS.md`.

A relação conceitual é:

```text
EVIDÊNCIAS
    ↓
INVESTIGAÇÃO
    ↓
FINDINGS
    ↓
essência reconstruível
    ↓
CHANGE
    ↓
R/D/O
```

E, no sentido de verificação:

```text
R/D/O editado
    ↓
proposições alteradas
    ↓
confronto com FINDINGS
    ↓
sustentado / parcial / contradito /
não sustentado / ambíguo
```

## 2. Princípio fundamental: estado atual, não histórico embutido

FINDINGS representa **o estado atual do conhecimento descoberto sobre o namespace**.

A evolução desse conhecimento pertence ao Git.

```text
Git       = como o conhecimento mudou
FINDINGS  = o que sabemos agora e por que sabemos
R/D/O     = qual significado foi aprovado como verdade
CHANGE    = qual transformação da verdade está sendo proposta
```

Se na V1:

```text
F-001 = A
F-002 = B
```

E na V2:

```text
F-001 = A
F-002 = C
```

O FINDINGS atual deve normalmente conter:

```yaml
- id: F-001
  afirmacao: A

- id: F-002
  afirmacao: C
```

Não deve carregar, por padrão, uma genealogia como:

```yaml
historico:
  V1: B
  V2: C
```

O Git já preserva essa evolução.

## 3. Quando conhecimento histórico permanece no arquivo atual

Uma regra histórica só permanece materializada quando ainda é necessária para compreender, reproduzir, verificar ou auditar alguma realidade atualmente relevante.

Exemplo:

```text
competências de 2025 → ainda interpretadas por V1
competências de 2026 → interpretadas por V2
```

Nesse caso, as duas regras continuam semanticamente necessárias e podem coexistir com aplicabilidade explícita.

A pergunta de retenção é:

> Se eu remover esta regra histórica do FINDINGS atual, ainda consigo compreender, reproduzir e verificar corretamente tudo que o sistema atual precisa suportar?

Se sim, a regra pode ficar apenas no Git.

Se não, ela permanece no FINDINGS atual.

Assim, após V19, o tamanho de FINDINGS deve crescer de acordo com a **complexidade semântica atual**, e não com a quantidade de versões históricas.

## 4. O que deve virar finding

Um finding deve existir quando a descoberta for material para pelo menos uma destas funções:

- reconstruir;
- verificar;
- distinguir;
- delimitar;
- reavaliar;
- reimplementar;
- auditar.

Exemplos típicos:

- propósito;
- fato elementar;
- população;
- elegibilidade;
- componentes semânticos;
- fórmula;
- ordem de agregação;
- temporalidade;
- exclusões;
- invariantes;
- casos-limite;
- exceções;
- convenções;
- diferenças semânticas ainda vigentes;
- incertezas;
- evidência conflitante;
- limites da investigação.

## 5. O que não deve virar finding

FINDINGS não é log de investigação.

Não armazenar apenas porque algo foi observado:

- chain-of-thought;
- transcript de sessão;
- lista de todos os arquivos abertos;
- todas as CTEs;
- todos os JOINs;
- todas as colunas físicas;
- dump completo de SQL;
- detalhes físicos semanticamente irrelevantes;
- histórico textual de mudanças;
- duplicação textual do R/D/O.

Regra prática:

> Não preservar tudo que foi visto. Preservar tudo que foi aprendido e continua materialmente útil.

## 6. Atomicidade

Um finding representa uma descoberta semanticamente identificável.

Bom:

```yaml
chave: exec_prog.componente.programado
afirmacao: >
  PROGRAMADO = 1 quando...
```

Ruim:

```yaml
chave: analise_modelo_sql
afirmacao: >
  O arquivo possui várias CTEs, filtros, joins e cálculos...
```

O finding não representa um arquivo, uma sessão ou uma investigação inteira.

## 7. Identidade estável e UPSERT

Cada finding possui uma identidade técnica e uma identidade analítica.

```yaml
id: F-005
chave: exec_prog.componente.programado
```

Mudança de redação não cria novo finding.

Nova evidência da mesma verdade também não.

A regra de UPSERT é:

```text
mesma descoberta + mesma verdade
→ manter finding
→ atualizar evidência se útil

mesma descoberta + evidência melhor
→ manter finding
→ enriquecer evidência / certeza

mudança apenas física
→ manter semântica
→ atualizar evidência se necessário

mudança semântica da realidade
→ atualizar estado atual do conhecimento
→ Git preserva estado anterior
→ avaliar CHANGE no R/D/O

nova descoberta
→ novo F-*
```

Se a versão anterior ainda for materialmente necessária no estado atual, ela pode permanecer como variante ou finding aplicável ao escopo histórico ainda vigente.

## 8. Idioma canônico

As chaves estruturais e enumerações controladas de FINDINGS devem usar PT-BR.

Exemplos:

```yaml
id:
chave:
estado:
tipo:
aplica_se_a:
afirmacao:
evidencias:
certeza:
amostras:
artefato:
linhas:
localizador:
amostra:
trilha_codigo:
semantica:
papel:
expressao:
componentes:
rdo:
disposicao:
dimensoes:
motivo:
risco:
consequencia:
```

Não traduzir identificadores cuja tradução prejudique identidade ou verificabilidade:

```text
PROGRAMACAO_EXECUTADA_ID
DATA_ALTERACAO
V1_VAR1_EXECUTADO
SQL
dbt
Git
RDO
```

Termos técnicos consolidados também podem permanecer literais quando fizer sentido.

## 9. Evidência verificável

Não basta afirmar algo. O humano deve conseguir ler uma amostra que sustente a descoberta e saber onde aprofundar a verificação.

Exemplo:

```yaml
evidencias:
  certeza: comprovada
  amostras:
    - tipo: implementacao
      artefato: modelo_x.sql
      linhas: 120-135
      amostra: |
        CASE
          WHEN PROGRAMACAO_EXECUTADA_ID = 127
          THEN 1
          ELSE 0
        END
      trilha_codigo: models/.../modelo_x.sql:120-135
```

A amostra deve ser curta, suficiente, legível e diretamente relacionada ao finding.

Ela não substitui a fonte original.

Para evidência quantitativa, a amostra pode ser um witness, expressão ou linha representativa.

## 10. Certeza

A certeza descreve a força da evidência, não a importância do finding.

Estados possíveis podem incluir:

```text
comprovada
corroborada
parcial
conflitante
inferida
lacuna_comprovada
nao_resolvida
```

## 11. Risco é opcional

`risco` não é requisito para um finding existir.

Uma fórmula, definição de população ou invariante pode ser material mesmo sem risco associado.

Use `risco` apenas quando a consequência acrescentar informação útil.

## 12. Relação com R/D/O

FINDINGS não copia R/D/O. Ele registra a relação com o contrato.

Exemplo candidato:

```yaml
rdo:
  disposicao: candidato
  dimensoes:
    - requirement
    - decision
```

Exemplo promovido:

```yaml
rdo:
  disposicao: promovido
  referencias:
    - mop/programacao/exec_prog:R-001
    - mop/programacao/exec_prog:D-003
```

Outras disposições podem incluir:

```text
representado_parcialmente
revisao
nao_promovido
nao_semantico
herdado
superseded
```

## 13. FINDINGS → RDO

Os findings devem conter conhecimento suficiente para reconstruir a essência necessária ao contrato.

```text
propósito
+ população
+ componentes
+ fórmula
+ agregação
+ exclusões
+ invariantes
    ↓
síntese semântica
    ↓
R/D/O
```

A reversibilidade é semântica, não textual.

## 14. RDO → FINDINGS significa verificação

Não significa gerar findings a partir do RDO.

Quando um humano edita R/D/O, a LLM deve decompor a mudança em proposições e confrontá-las com o conhecimento preservado.

Resultados esperados:

```text
SUSTENTADO
PARCIAL
CONTRADITO
NAO_SUSTENTADO
AMBIGUO
EVIDENCIA_DESATUALIZADA
```

`NAO_SUSTENTADO` não significa falso. Significa que a memória atual não contém evidência suficiente.

`CONTRADITO` significa que existe evidência preservada materialmente incompatível com a proposição.

## 15. Investigação dirigida

Quando uma edição não for sustentada ou estiver contradita, o protocolo pode iniciar uma investigação especificamente orientada à hipótese alterada.

A busca deve procurar:

```text
evidência favorável
+
evidência contrária
+
interpretações concorrentes
```

Não deve ser uma busca apenas confirmatória.

Depois:

```text
nova evidência
    ↓
UPSERT FINDINGS
    ↓
reavaliar R/D/O
```

## 16. Evolução entre versões

Ao investigar uma nova versão, a LLM parte de:

```text
FINDINGS atuais
+
RDO atual
+
nova evidência
```

Para cada proposição:

```text
igual?
→ mantém

evidência melhor?
→ UPSERT

mudança só física?
→ mantém significado

mudança semântica?
→ atualiza conhecimento atual
→ Git preserva versão anterior
→ avaliar CHANGE no R/D/O

não verificável?
→ não inventar

nova?
→ novo finding
```

O arquivo atual não deve acumular V1, V2, V3 ... V19 apenas porque essas versões existiram.

## 17. Nível de abstração

FINDINGS admite:

```yaml
nivel_abstracao: 0.7
```

Faixa:

```text
0.0 a 1.0
```

Passo:

```text
0.1
```

Padrão:

```text
0.7
```

### 0.0

Máxima materialização observável. Preserva mais detalhes físicos, condições intermediárias, exceções, relações técnicas, amostras e limites.

Não armazena chain-of-thought.

### 0.7

Padrão recomendado. Preserva o conhecimento necessário para reconstrução e verificação, comprimindo detalhes físicos redundantes.

Busca equilíbrio entre:

```text
reconstruibilidade
auditabilidade
legibilidade
custo de contexto
```

### 1.0

Máxima síntese semântica.

Pode reduzir capacidade de reimplementação precisa, detalhe de borda e rastreabilidade fina. Essa perda é intencional e deve permanecer visível.

A abstração altera quanto conhecimento intermediário é materializado, não qual verdade é considerada correta.

## 18. Estrutura proposta

```yaml
esquema: semantic-git-achados-v2
espaco_semantico: mop/programacao/exec_prog
autoridade: memoria_analitica_nao_autoritativa
nivel_abstracao: 0.7

alvo:
  assunto: EXEC_PROG
  versao_semantica: V1

achados:
  - id: F-005
    chave: exec_prog.componente.programado
    estado: ativo
    tipo: fato_semantico

    aplica_se_a:
      versao_semantica: V1

    afirmacao: >
      PROGRAMADO = 1 quando a programação pertence
      à população elegível e satisfaz as condições admitidas.

    evidencias:
      certeza: comprovada
      amostras:
        - tipo: implementacao
          artefato: modelo.sql
          linhas: 140-165
          amostra: |
            ...
          trilha_codigo: models/.../modelo.sql:140-165

    semantica:
      papel: definicao_componente
      estado: candidato
      conceito: PROGRAMADO
      dominio_valores: [0, 1]

    rdo:
      disposicao: candidato
      dimensoes:
        - decision
        - operation
```

## 19. Cadeia de decisão operacional da LLM

Isto é um procedimento auditável; não é armazenamento de chain-of-thought.

```text
1. O que exatamente foi aprendido?
        ↓
2. É material para reconstrução, verificação ou auditoria?
   não → descartar
   sim → continuar
        ↓
3. Já existe finding semanticamente equivalente?
   não → novo F-*
   sim → continuar
        ↓
4. A nova evidência confirma a mesma verdade?
   sim → UPSERT de evidência
   não → continuar
        ↓
5. É apenas mudança física?
   sim → manter semântica
   não → continuar
        ↓
6. A realidade semanticamente mudou?
   sim → atualizar conhecimento atual
       → Git preserva estado anterior
       → avaliar CHANGE no R/D/O
        ↓
7. O estado anterior ainda é necessário hoje?
   sim → preservar aplicabilidade necessária
   não → deixar história no Git
        ↓
8. Há evidência suficiente?
   não → registrar lacuna/ambiguidade
        ↓
9. Qual é a disposição perante R/D/O?
```

## 20. Cadeia de verificação de R/D/O editado

```text
RDO original
    ↓
edição humana
    ↓
RDO'
    ↓
extrair proposições alteradas
    ↓
localizar findings relacionados
    ↓
comparar
```

Para cada proposição:

```text
findings confirmam?         → SUSTENTADO
confirmam parcialmente?     → PARCIAL
há evidência incompatível?  → CONTRADITO
não há evidência?           → NAO_SUSTENTADO
há interpretações rivais?   → AMBIGUO
```

Depois:

```text
SUSTENTADO
→ pode prosseguir

PARCIAL / AMBIGUO
→ revisão ou investigação dirigida

NAO_SUSTENTADO
→ investigar ou declarar ausência de evidência

CONTRADITO
→ reinvestigar a realidade,
  rever a edição,
  ou tratar como TO-BE deliberado
```

## 21. Invariantes

### 21.1 Sem conhecimento silenciosamente perdido

Descoberta material não desaparece sem substituição, resolução, perda de aplicabilidade, decisão explícita ou preservação histórica pelo Git.

### 21.2 Sem R/D/O material silenciosamente sem sustentação

Toda proposição material de R/D/O deve ser justificável por FINDINGS, conhecimento ancestral aplicável ou decisão humana governada explícita.

### 21.3 Sem finding material sem disposição conhecida

Todo finding material deve possuir situação compreensível em relação ao contrato.

### 21.4 Reconstruibilidade

O conjunto atual de findings, dentro do nível de abstração escolhido, deve permitir recuperar o entendimento semântico correspondente.

### 21.5 Evidência recuperável

Toda afirmação material deve possuir evidência suficientemente localizável para inspeção humana ou nova investigação.

## 22. Princípio de conservação de conhecimento

O Semantic Git deve conservar conhecimento material sem confundir conhecimento com história.

```text
Git      conserva a evolução
FINDINGS conserva o conhecimento atual descoberto
R/D/O    conserva a verdade aprovada
CHANGE   conserva a transformação proposta
```

## 23. Teste final de qualidade

Um bom FINDINGS deve permitir responder positivamente:

1. Uma nova LLM, recebendo o protocolo, FINDINGS atual e ancestrais autorizados, consegue reconstruir o significado sem reler toda a implementação?
2. Um humano consegue inspecionar evidências mínimas que sustentam as principais descobertas?
3. Se o R/D/O for editado, a LLM consegue distinguir sustentação, contradição, ausência de evidência e ambiguidade?
4. Ao surgir uma nova versão, a LLM consegue reconciliar o novo comportamento sem transformar FINDINGS em um histórico crescente V1…V19?
5. O Git continua suficiente para reconstruir a evolução que não precisa permanecer materializada no estado atual?

Se sim, FINDINGS está cumprindo sua função.
