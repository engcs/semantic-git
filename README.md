# Semantic Git

Metamodelo de Governança Semântica com Base Proto-Ontológica - Uma forma de
extrair a essência semântica de qualquer coisa, versioná-la e apresentá-la de
modo claro.

## Propósito

Este repositório separa três camadas:

- `SEMANTIC_GIT.md`: especificação normativa oficial do Semantic Git;
- `transformations/IES_RDO_Transform.md`: transformação bidirecional entre Intent, Experience, Solution e Requirements, Decisions, Operations;
- `applications/mop/`: aplicação de referência do Semantic Git ao framework MOP, incluindo suas premissas específicas de indicadores.

O repositório não é uma implementação dbt nem um executor. Ele define como
conhecimento e mudanças devem ser representados e governados.

## Fonte normativa

`SEMANTIC_GIT.md` é a fonte normativa oficial desta distribuição. A cópia foi mantida
standalone na versão 1.0 para que o modelo possa ser compreendido sem depender de outro
repositório, prompt ou automação.

Não manter uma segunda cópia concorrente da especificação. Alterações
normativas devem ser feitas em `SEMANTIC_GIT.md`, registradas no Git e identificadas
pela versão correspondente.

## Relação entre os artefatos

```text
IES
  ⇄ transformação semântica
RDO
  ↓ governança pelo Semantic Git
Semantic Repository
  ↓ materialização
código, configuração, testes e operações
```

## Escopo

Esta distribuição contém o modelo, a transformação, o vocabulário formal e a
aplicação MOP. Conhecimento corporativo específico, mapeamentos
físicos, caminhos locais, dados, arquivos compactados e implementações externas
não fazem parte deste repositório.

## Status

Semantic Git v1.0, com o MOP como aplicação de referência. A automação de
validação determinística e a integração com
materializações físicas podem ser adicionadas em mudanças posteriores.

Cristian Sousa — eng.cristiansousa@gmail.com
