# IES ↔ RDO — Transformação orientada pela Matriz de Conhecimento do Produto

Este documento define a transformação de Intent, Experience e Solution (IES)
em Requirements, Decisions e Operations (RDO). O texto pode ser utilizado como
método de análise, instrução para uma IA ou critério de revisão semântica.

Você deve estruturar o conhecimento de um produto em três pilares:

- **Requirements — Requisitos**
- **Decisions — Decisões**
- **Operations — Operação**

Entretanto, não produza esses pilares de forma isolada ou meramente documental.

Antes e durante a construção do RDO, raciocine sobre o produto pela **Matriz de Conhecimento do Produto**, considerando simultaneamente duas perspectivas:

| Camada do Produto ↓ / Natureza do Conhecimento → | Requirements | Decisions | Operations |
|---|---|---|---|
| **Intent** | O que precisa ser verdadeiro para cumprir o propósito | Escolhas que delimitam ou preservam o propósito | Condições operacionais que afetam o propósito |
| **Experience** | Comportamentos e qualidades esperados | Escolhas de produto/design que moldam a experiência | Como a experiência se comporta na prática |
| **Solution** | Restrições e propriedades que a solução deve satisfazer | Escolhas concretas de design/arquitetura | Como a solução é realizada, executada e mantida |

## Direção das transformações

Este documento define duas transformações complementares, e não apenas uma
classificação em uma única direção:

```text
IES -> RDO
RDO -> IES
```

### IES -> RDO

Parte-se das perspectivas de Intent, Experience e Solution para descobrir,
classificar e relacionar Requirements, Decisions e Operations. O resultado deve
preservar o significado, registrar lacunas e evitar que decisões de solução
sejam confundidas com requisitos.

### RDO -> IES

Parte-se do RDO vigente para reconstruir a intenção do produto, a experiência
esperada e a solução que está sendo governada. Essa transformação inversa é um
teste de reconstruibilidade: não deve inventar intenção, experiência ou
justificativas que não estejam sustentadas pelo RDO.

### Critério de ida e volta

As duas direções devem ser semanticamente coerentes:

```text
IES -> RDO -> IES'
RDO -> IES -> RDO'

IES' ≈ IES
RDO' ≈ RDO
```

O símbolo `≈` representa equivalência semântica, não igualdade textual. Uma
diferença material na volta indica lacuna, ambiguidade ou perda de significado
e deve ser tratada antes de considerar o conhecimento completo.

## Objetivo

Construir um conjunto de **Requirements, Decisions e Operations semanticamente completo**, de modo que um humano ou outra IA consiga, a partir somente desses três pilares:

1. compreender a **intenção** do produto;
2. reconstruir a **experiência desejada**;
3. compreender a **solução vigente**;
4. gerar um PRD adequado sem precisar inventar informações relevantes.

O RDO não está completo apenas porque existem documentos nas três categorias.

Ele está completo quando consegue representar inequivocamente o produto.

---

# 1. Pense primeiro no produto

Antes de classificar qualquer informação como Requirement, Decision ou Operation, forme internamente uma visão do produto segundo:

## Intent

Determine:

- qual problema está sendo resolvido;
- para quem;
- por que ele importa;
- qual resultado se pretende produzir;
- quais princípios não devem ser perdidos.

## Experience

Determine:

- o que deve acontecer para o usuário ou consumidor do produto;
- quais comportamentos são esperados;
- quais qualidades precisam ser percebidas;
- quais fluxos ou resultados são essenciais;
- o que caracteriza uma experiência correta ou incorreta.

## Solution

Determine:

- qual solução concreta existe ou está sendo proposta;
- quais componentes relevantes a constituem;
- quais restrições condicionam sua construção;
- como ela satisfaz a intenção e a experiência.

Não crie necessariamente documentos chamados Intent, Experience ou Solution.

Essas três dimensões funcionam como **perspectiva de produto usada para validar o RDO**.

---

# 2. Construa os Requirements

Requirements descrevem:

> **O que precisa ser verdadeiro.**

Um Requirement não deve registrar uma escolha simplesmente porque ela é a implementação atual.

Registre como Requirement:

- necessidades;
- comportamentos obrigatórios;
- propriedades esperadas;
- restrições reais;
- invariantes;
- critérios de aceitação;
- condições de sucesso;
- necessidades de experiência;
- requisitos técnicos quando realmente forem restrições do problema.

Sempre que possível, escreva requisitos independentes da solução.

Exemplo:

**Bom**

> O usuário deve conseguir utilizar as funções essenciais sem conexão com a internet.

**Evitar**

> O sistema deve utilizar banco SQLite local.

A segunda afirmação provavelmente é uma Decision, salvo se SQLite for uma restrição externa obrigatória.

---

# 3. Construa as Decisions

Decisions descrevem:

> **O que foi escolhido para satisfazer os requisitos e por quê.**

Toda decisão relevante deve indicar:

- contexto;
- requisito(s) que motivaram a decisão;
- escolha adotada;
- justificativa;
- alternativas relevantes consideradas, quando existirem;
- consequências e trade-offs conhecidos;
- estado da decisão: proposta, aceita, substituída ou descartada.

Decisions devem preservar o **racional** que não poderia ser reconstruído apenas observando a solução pronta.

Uma decisão não deve ser artificialmente convertida em Requirement apenas porque já está implementada.

---

# 4. Construa as Operations

Operations descrevem:

> **Como as decisões e requisitos se manifestam e permanecem válidos na realidade.**

Inclua apenas conhecimento operacional relevante, como:

- comportamento em execução;
- processos necessários;
- atualização;
- sincronização;
- execução;
- validação;
- monitoramento;
- recuperação;
- manutenção;
- migração;
- rollback;
- rotinas e procedimentos essenciais.

Uma Operation deve estar ligada a pelo menos uma Decision, Requirement ou ambos quando essa relação existir.

Não transforme Operations em um depósito indiscriminado de procedimentos.

---

# 5. Preserve rastreabilidade

Sempre que possível, explicite relações como:

```text
Requirement
    ↓ addressed_by
Decision
    ↓ realized_by
Operation
```

Mas não force uma cadeia 1:1.

São válidas estruturas como:

```text
R1 ─┬─ D1 ── O1
    │
    └─ D2 ─┬─ O2
            └─ O3
```

e:

```text
D1
 ↓ consequence
R4
 ↓ addressed_by
D5
```

Uma Decision pode gerar consequências que revelem novos Requirements.

Uma descoberta operacional pode exigir revisão de uma Decision.

O modelo deve representar essas relações, e não esconder a causalidade.

---

# 6. Use a matriz como teste de cobertura

Após construir o RDO, avalie mentalmente as nove interseções:

| | Requirement | Decision | Operation |
|---|---|---|---|
| Intent | ? | ? | ? |
| Experience | ? | ? | ? |
| Solution | ? | ? | ? |

Uma célula pode legitimamente não possuir conteúdo.

**Não invente informações apenas para preencher a matriz.**

Entretanto, uma célula vazia deve provocar a pergunta:

> Há conhecimento relevante ausente ou essa interseção realmente não se aplica?

Identifique gaps quando houver informação necessária para compreender o produto que ainda não esteja representada.

---

# 7. Execute o teste PRD

Ao final, simule a reconstrução de um PRD usando exclusivamente o RDO produzido.

Esse PRD hipotético deve permitir explicar claramente:

## Intenção
- problema;
- usuário ou consumidor;
- necessidade;
- objetivo;
- resultado esperado.

## Experiência
- comportamento esperado;
- capacidades essenciais;
- qualidades;
- restrições percebidas;
- critérios de sucesso.

## Solução
- solução vigente;
- decisões relevantes que determinam sua forma;
- principais restrições;
- comportamento operacional necessário.

Não é obrigatório gerar o PRD completo, salvo solicitação explícita.

O objetivo é verificar sua **reconstruibilidade**.

---

# 8. Critério de fechamento semântico

Considere o trabalho incompleto se a reconstrução do PRD exigir que você:

- invente intenção;
- suponha experiência importante;
- deduza arbitrariamente por que determinada decisão foi tomada;
- confunda implementação histórica com requisito;
- descubra comportamento operacional essencial que não está documentado;
- acrescente conhecimento relevante que não existe no RDO.

O critério desejado é:

```text
RDO
 ↓
PRD reconstruído
 ↓
interpretação novamente como RDO
 ↓
RDO semanticamente equivalente ao original
```

Não se exige igualdade textual.

Exige-se **equivalência semântica**.

---

# 9. Evite estes erros

Não:

- transforme toda implementação em Requirement;
- registre decisões sem requisito, problema ou contexto correspondente;
- registre apenas o estado atual e perca o racional das escolhas;
- misture Requirement, Decision e Operation na mesma afirmação;
- crie documentação apenas para preencher categorias;
- duplique a mesma verdade em diversos lugares sem necessidade;
- invente informações para tornar a estrutura aparentemente completa;
- trate RDO como sequência temporal obrigatória;
- confunda consequência de uma decisão com Operation;
- use o PRD como fonte paralela de verdade quando o RDO for a estrutura canônica.

---

# 10. Forma de trabalho

Para cada nova informação recebida:

1. compreenda seu significado no produto;
2. identifique se ela afeta Intent, Experience ou Solution;
3. classifique sua natureza como Requirement, Decision ou Operation;
4. identifique relações com elementos existentes;
5. detecte contradições, lacunas ou decisões implícitas;
6. atualize o RDO;
7. valide se a definição global do produto continua reconstruível.

Quando uma informação estiver ambígua entre Requirement e Decision, pergunte:

> Isso precisa necessariamente ser verdadeiro ou foi uma escolha feita para atingir algo que precisa ser verdadeiro?

Quando estiver ambígua entre Decision e Operation, pergunte:

> Isto descreve uma escolha ou descreve como essa escolha funciona na prática?

---

# Resultado esperado

O resultado final deve ser um RDO no qual:

- Requirements expressem as verdades necessárias;
- Decisions preservem as escolhas e seus motivos;
- Operations expressem sua realização prática;
- as relações entre os elementos sejam rastreáveis;
- Intent, Experience e Solution possam ser reconstruídos;
- um PRD adequado possa ser derivado sem invenção relevante.

**O RDO é a representação estruturada do conhecimento.
O PRD é uma possível projeção desse conhecimento sob a perspectiva do produto.
A Matriz de Conhecimento do Produto é o recurso usado para verificar se as duas visões permanecem semanticamente coerentes.**
