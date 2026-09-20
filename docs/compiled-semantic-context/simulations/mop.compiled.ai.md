# COMPILED SEMANTIC CONTEXT

> **SIMULATION** — artefato derivado para validar o formato do Compiled Semantic Context. Não é fonte de verdade e não deve ser editado manualmente.

## Metadata

```yaml
artifact: compiled-semantic-context
target_namespace: mop
scope_depth: 1
authority: DERIVED
source_ref: main
source_commit_at_simulation_start: ae1ea2c39f379d605037118bd249da05072bc146
compiler_status: NOT_IMPLEMENTED
simulation: true
```

## Reading Contract

- O conteúdo R/D/O abaixo é reproduzido dos arquivos governados do domínio `mop`.
- O CSC não cria requisitos, decisões ou operações.
- Relações só são apresentadas como resolvidas quando estão explicitamente representadas na fonte.
- Ausência de uma relação compilada não significa ausência de relação conceitual; significa apenas que a simulação não a inferiu.
- Em caso de divergência, os arquivos governados do Semantic-Git prevalecem.

## Effective Scope Chain

```text
mop  [TARGET]
```

Não há namespace ancestral de aplicação a materializar neste exemplo.

---

# Scope: mop

## Requirements

### mop:R-001
Identificar inequivocamente cada série por indicador, visão, grão temporal e versão da regra de negócio.

### mop:R-002
Organizar o detalhe e os resultados por competência, preservando a data de referência, a data de apuração e, quando aplicável, a data de congelamento.

### mop:R-003
Disponibilizar resultados consistentes nos níveis organizacionais aplicáveis, incluindo contrato, regional e distribuidora.

### mop:R-004
Distinguir a apuração recalculável da fotografia histórica preservada.

### mop:R-005
Permitir a apuração paralela de diferentes versões, preservando a identidade, o estado e a origem de cada resultado.

### mop:R-006
Permitir expurgos de negócio sem remover a ocorrência original nem perder a justificativa da exceção.

### mop:R-007
Permitir reconciliar o resultado do indicador com suas medidas componentes, incluindo eventuais suplementos, e com as ocorrências consideradas ou desconsideradas na apuração.

### mop:R-008
Tratar cada visão como um recorte explícito das ocorrências que podem participar da apuração.

### mop:R-009
Proteger os resultados históricos contra recálculo ou substituição silenciosa.

## Decisions

### mop:D-001
Estruturar cada indicador nas etapas fato detalhado, KPI fato, catálogo e KPI final. Atende R-007 e R-009.

### mop:D-002
Identificar a série por uma chave CCIO composta pelo indicador base, visão, grão temporal e versão. Atende R-001.

### mop:D-003
Usar o grão mensal como padrão de publicação, permitindo que cada indicador defina outros grãos temporais, preservando as datas de referência, apuração e congelamento. Atende R-002.

### mop:D-004
Preservar as ocorrências no menor grão do indicador, agregá-las inicialmente no nível contrato e consolidar as medidas nos níveis regional e distribuidora. Atende R-003 e R-007.

### mop:D-005
Manter fatos e resultados nas apurações `VIVA` e `CONGELADA` e reuni-los no catálogo do indicador. Atende R-004 e R-009.

### mop:D-006
Apurar versões em paralelo e incorporar versão, status da versão e origem à identidade de cada resultado. Atende R-005.

### mop:D-007
Incorporar a visão à identidade da série como recorte da população apurada. Atende R-008.

### mop:D-008
Dar precedência ao controle manual de expurgo e zerar a contribuição da linha sem removê-la do detalhe. Atende R-006.

### mop:D-009
Compor medidas auditáveis no KPI fato a partir de valores base e, quando aplicável, suplementos, preservando separadamente sua origem e seu grão antes de calcular a fórmula específica no KPI final. Atende R-007.

## Operations

### mop:O-001
Cada indicador define sua unidade elementar no menor grão disponível, preservando o dia e a equipe quando fizerem parte da ocorrência.

### mop:O-002
Cada unidade recebe uma data de referência, da qual são derivadas as competências temporais necessárias à apuração.

### mop:O-003
Cada unidade é situada na hierarquia organizacional formada por equipe, contrato, regional e distribuidora.

### mop:O-004
A unidade é relacionada às demais entidades necessárias para receber suas classificações de negócio.

### mop:O-005
As classificações determinam a população apurada e a contribuição individual para cada medida do indicador.

### mop:O-006
Ocorrências expurgadas permanecem no detalhe e na auditoria, mas deixam de contribuir para as medidas agregadas.

### mop:O-007
As contribuições são inicialmente preservadas no menor grão temporal e organizacional necessário ao indicador.

### mop:O-008
As contribuições no menor grão do indicador são consolidadas no período e no nível organizacional definidos para publicação.

### mop:O-009
No nível contrato, as unidades são agrupadas por competência, visão, versão e demais dimensões próprias do indicador.

### mop:O-010
Quando uma medida prevê suplementos, eles são associados aos valores base no mesmo grão antes da agregação do período, preservando separadamente sua origem.

### mop:O-011
As medidas do nível contrato são posteriormente consolidadas nos níveis regional e distribuidora.

### mop:O-012
Os valores acumulados são obtidos pela soma temporal das medidas dentro de cada série e nível organizacional.

### mop:O-013
A fórmula específica do indicador é aplicada às medidas já agregadas para produzir os resultados do período e acumulado.

---

# Explicit Relationships

As relações abaixo podem ser extraídas deterministicamente da sintaxe explícita `Atende R-...` das Decisions.

```yaml
relations:
  - source: mop:D-001
    predicate: satisfies
    target: mop:R-007
  - source: mop:D-001
    predicate: satisfies
    target: mop:R-009
  - source: mop:D-002
    predicate: satisfies
    target: mop:R-001
  - source: mop:D-003
    predicate: satisfies
    target: mop:R-002
  - source: mop:D-004
    predicate: satisfies
    target: mop:R-003
  - source: mop:D-004
    predicate: satisfies
    target: mop:R-007
  - source: mop:D-005
    predicate: satisfies
    target: mop:R-004
  - source: mop:D-005
    predicate: satisfies
    target: mop:R-009
  - source: mop:D-006
    predicate: satisfies
    target: mop:R-005
  - source: mop:D-007
    predicate: satisfies
    target: mop:R-008
  - source: mop:D-008
    predicate: satisfies
    target: mop:R-006
  - source: mop:D-009
    predicate: satisfies
    target: mop:R-007
```

## Deliberately Not Inferred

A simulação **não** cria relações `Operation -> Decision`, embora algumas possam parecer semanticamente evidentes para um leitor. No estado atual do conteúdo, as Operations de `mop` não usam uma sintaxe equivalente a `Executa D-...` em seus textos.

Exemplo do que não deve ser produzido por um compilador puramente determinístico:

```text
mop:O-006 --executes--> mop:D-008   # NÃO INFERIR
```

Uma camada posterior de IA poderia sugerir essa relação, mas ela não pertence ao CSC canônico enquanto não estiver explicitamente governada.

---

# Unresolved References

```yaml
unresolved_references: []
```

Nesta simulação, todas as referências `Atende R-...` materializadas acima possuem alvo local identificável.

---

# Provenance

```yaml
sources:
  requirements:
    namespace: mop
    path: _applications/mop/REQUIREMENTS.md
  decisions:
    namespace: mop
    path: _applications/mop/DECISIONS.md
  operations:
    namespace: mop
    path: _applications/mop/OPERATIONS.md
  semantic_index:
    path: _index/SEMANTIC_INDEX.json
```

## Source Entity Map

```text
mop:R-* -> _applications/mop/REQUIREMENTS.md
mop:D-* -> _applications/mop/DECISIONS.md
mop:O-* -> _applications/mop/OPERATIONS.md
```

---

# Compilation Notes

Este arquivo mostra a forma mais simples do CSC: domínio de profundidade 1. Não há herança de namespace a expandir.

O ganho sobre uma simples concatenação dos três Markdown está em quatro elementos adicionais e determinísticos:

1. IDs qualificados pelo namespace;
2. contrato explícito de leitura para IA;
3. relações estruturadas já declaradas na fonte;
4. proveniência e referências irresolvidas em formato explícito.
