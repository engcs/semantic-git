# Fundação semântica de indicadores

## Anexo pré-ontológico da aplicação MOP

Este documento é uma fundação específica do MOP. Ele não pertence ao núcleo
do Semantic Git nem pretende ser uma ontologia formal.

Este documento estabelece uma terminologia precisa para diferenciar **fatos**, **séries de dados**, **agregações**, **valores agregados**, **indicadores**, **apurações** e **resultados**, evitando ambiguidades conceituais.

Considere, como referência, um indicador definido por:

\[
x_t = \frac{a_t}{b_t}
\]

em que:

\[
a_t = \sum A_t
\]

\[
b_t = \sum B_t
\]

e \(t\) representa o período de referência.

---

## 1. Fato

Um **fato** é uma ocorrência individual registrada pelo sistema, associada a um contexto e, normalmente, a um instante ou período.

Exemplo:

```text
evento 1 → valor A = 10 → janeiro
evento 2 → valor A = 20 → janeiro
evento 3 → valor A = 15 → fevereiro
```

O fato é a unidade observacional. Ele ainda não é uma agregação nem um resultado de indicador.

---

## 2. Série de dados

Uma **série de dados** é um conjunto ordenado ou indexado de valores de uma mesma variável ao longo de uma dimensão de referência.

Quando a dimensão é o tempo:

\[
S = [s_1, s_2, \ldots, s_n]
\]

De maneira mais rigorosa:

\[
S = \{(t_1,s_1),(t_2,s_2),\ldots,(t_n,s_n)\}
\]

Assim, uma série precisa ter:

- uma variável;
- uma dimensão de indexação;
- os valores observados nessa dimensão.

Exemplo:

\[
A = [A_{jan}, A_{fev}, A_{mar}, \ldots]
\]

**Importante:** série não significa necessariamente dado agregado. Podem existir séries de observações brutas ou séries agregadas.

---

## 3. Série base ou série de entrada

Uma **série de entrada** é uma série utilizada como insumo para o cálculo de outra série ou indicador.

No caso:

\[
X_t = \frac{\sum A_t}{\sum B_t}
\]

A e B são as séries de entrada de X.

Portanto:

\[
A = [A_1,A_2,\ldots,A_n]
\]

\[
B = [B_1,B_2,\ldots,B_n]
\]

são dependências do indicador X.

---

## 4. Agregação

Uma **agregação** é uma operação que reduz um conjunto de observações a um valor representativo dentro de determinado contexto.

Exemplos:

\[
SUM(A_t)
\]

\[
COUNT(A_t)
\]

\[
AVG(A_t)
\]

Se em janeiro existem:

\[
A_1 = [10,20,30]
\]

então:

\[
SUM(A_1) = 60
\]

A agregação é a **operação**. O valor 60 é o **valor agregado**.

---

## 5. Valor agregado

Um **valor agregado** é o valor produzido por uma operação de agregação sobre os dados de determinado contexto.

Para distinguir claramente observações e agregações, podemos usar:

\[
a_t = \sum A_t
\]

\[
b_t = \sum B_t
\]

Assim:

- \(A_t\) = conjunto de observações de A no período \(t\);
- \(a_t\) = valor agregado dessas observações;
- \(B_t\) = conjunto de observações de B no período \(t\);
- \(b_t\) = valor agregado dessas observações.

A expressão do indicador pode então ser escrita de maneira mais rigorosa:

\[
x_t = \frac{a_t}{b_t}
\]

---

## 6. Indicador

Um **indicador** é uma definição formal de uma medida derivada, composta por:

- variáveis de entrada;
- regra de cálculo;
- contexto ou dimensão de apuração.

Por exemplo:

\[
X_t = \frac{\sum A_t}{\sum B_t}
\]

é a definição do indicador X.

O indicador, enquanto definição, não é um número específico.

Ele estabelece a regra que determina como os resultados serão produzidos.

---

## 7. Regra de apuração

A **regra de apuração** é a expressão ou procedimento que transforma os dados de entrada no valor do indicador.

No exemplo:

\[
f(A_t,B_t) =
\frac{\sum A_t}{\sum B_t}
\]

é a regra de apuração.

Podemos representar:

\[
x_t = f(A_t,B_t)
\]

---

## 8. Apuração

Uma **apuração** é a execução da regra de um indicador para um contexto determinado.

Exemplo:

> Apuração de X para janeiro de 2026.

Se:

\[
a_{jan} = 80
\]

e:

\[
b_{jan} = 100
\]

a apuração executa:

\[
x_{jan} = \frac{80}{100}
\]

A apuração é, portanto, o **processo**, não o valor produzido.

---

## 9. Resultado

Um **resultado** é o valor produzido por uma apuração.

No exemplo:

\[
x_{jan} = 0,8
\]

ou:

\[
x_{jan} = 80\%
\]

**80% é o resultado da apuração de X para janeiro.**

Portanto:

- **apuração** = processo;
- **resultado** = saída do processo.

---

## 10. Indicador apurado

Um **indicador apurado** é uma instância do indicador para um contexto específico, acompanhada de seu resultado.

Pode ser representado como:

\[
(X,t,x_t)
\]

Exemplo:

```text
Indicador: X
Período: janeiro/2026
Resultado: 80%
```

Assim:

- **indicador** = definição;
- **indicador apurado** = definição aplicada a determinado contexto, produzindo um resultado.

---

## 11. Série de resultados

Uma **série de resultados** é o conjunto ordenado dos resultados das sucessivas apurações de um indicador.

Se:

\[
x_1 = 80\%
\]

\[
x_2 = 85\%
\]

\[
x_3 = 77\%
\]

então:

\[
X = [x_1,x_2,x_3,\ldots,x_n]
\]

é a série de resultados do indicador X.

De forma mais rigorosa:

\[
X = \{(t_1,x_1),(t_2,x_2),\ldots,(t_n,x_n)\}
\]

---

## 12. Relação entre os conceitos

A estrutura conceitual completa pode ser representada como:

```text
Fatos
  ↓
Séries de entrada
  ↓
Agregações
  ↓
Valores agregados
  ↓
Regra do indicador
  ↓
Apuração
  ↓
Resultado
  ↓
Série de resultados
```

Aplicando ao exemplo:

\[
A_t \xrightarrow{SUM} a_t
\]

\[
B_t \xrightarrow{SUM} b_t
\]

\[
x_t = \frac{a_t}{b_t}
\]

e:

\[
X = [x_1,x_2,\ldots,x_n]
\]

Portanto:

- **A e B** = séries de entrada do indicador;
- **\(a_t\) e \(b_t\)** = valores agregados de A e B no período \(t\);
- **\(X_t = a_t/b_t\)** = definição da apuração de X para cada período;
- **\(x_t\)** = resultado de uma apuração;
- **\(X = [x_1,\ldots,x_n]\)** = série de resultados do indicador.

---

## 13. Distinção entre apuração periódica e apuração consolidada

A série de resultados mensais:

\[
X = [x_1,x_2,\ldots,x_{12}]
\]

não deve ser confundida com uma única apuração consolidada do período inteiro.

Por exemplo, uma apuração anual poderia ser:

\[
x_{ano} =
\frac{\sum_{t=1}^{12} a_t}
     {\sum_{t=1}^{12} b_t}
\]

Esse valor é diferente da simples média dos resultados mensais:

\[
\frac{x_1+x_2+\cdots+x_{12}}{12}
\]

Em geral:

\[
\frac{\sum_{t=1}^{12} a_t}
     {\sum_{t=1}^{12} b_t}
\neq
\frac{x_1+x_2+\cdots+x_{12}}{12}
\]

porque cada período pode possuir denominadores diferentes e, portanto, pesos diferentes.

---

## 14. Convenção recomendada de notação

Para evitar que a letra X represente simultaneamente a definição do indicador e sua série de resultados, recomenda-se separar explicitamente os conceitos.

### Definição do indicador

\[
I_X
\]

representa o **indicador enquanto definição**.

### Resultado de uma apuração

\[
x_t
\]

representa o **resultado do indicador no período \(t\)**.

### Série de resultados

\[
S_X = [x_1,x_2,\ldots,x_n]
\]

representa a **série de resultados do indicador X**.

Dessa forma:

\[
I_X(A_t,B_t) \rightarrow x_t
\]

e, após sucessivas apurações:

\[
S_X = [x_1,x_2,\ldots,x_n]
\]

Essa convenção elimina a ambiguidade entre:

- o indicador enquanto definição;
- uma apuração específica;
- o resultado dessa apuração;
- a série histórica dos resultados.

---

## 15. Glossário resumido

| Termo | Definição |
|---|---|
| **Fato** | Ocorrência individual registrada pelo sistema. |
| **Série de dados** | Conjunto de valores de uma mesma variável indexados por uma dimensão. |
| **Série de entrada** | Série utilizada como insumo para o cálculo de um indicador. |
| **Agregação** | Operação que resume um conjunto de observações. |
| **Valor agregado** | Valor produzido por uma agregação. |
| **Indicador** | Definição formal de uma medida derivada. |
| **Regra de apuração** | Regra que transforma dados de entrada no valor do indicador. |
| **Apuração** | Execução da regra do indicador em determinado contexto. |
| **Resultado** | Valor produzido por uma apuração. |
| **Indicador apurado** | Instância de um indicador aplicada a um contexto específico e associada a seu resultado. |
| **Série de resultados** | Conjunto indexado dos resultados das sucessivas apurações de um indicador. |

---

## Síntese formal

A relação entre os conceitos pode ser sintetizada por:

\[
A_t \xrightarrow{agregação} a_t
\]

\[
B_t \xrightarrow{agregação} b_t
\]

\[
I_X(a_t,b_t) \xrightarrow{apuração} x_t
\]

\[
S_X = [x_1,x_2,\ldots,x_n]
\]

Em palavras:

> **Fatos geram dados; dados podem constituir séries; séries alimentam agregações; valores agregados são submetidos à regra de um indicador; a execução dessa regra é uma apuração; cada apuração produz um resultado; e o conjunto indexado desses resultados forma a série de resultados do indicador.**
