# Agent Instructions

## Authority

`SEMANTIC_GIT.md` é a fonte normativa deste repositório. Este arquivo orienta a
operação de agentes, mas não cria, substitui ou modifica regras normativas.

## Context Loading

Ao iniciar uma tarefa:

1. identifique o escopo conceitual da solicitação;
2. consulte em `SEMANTIC_GIT.md` somente as regras necessárias;
3. consulte `transformations/IES_RDO_Transform.md` quando a tarefa envolver IES e RDO;
4. consulte `applications/mop/foundations/` quando a tarefa envolver as premissas semânticas dos indicadores MOP;
5. consulte `applications/mop/` quando a tarefa envolver a aplicação MOP;
6. siga exclusivamente o padrão documental canônico da seção 23.3 de `SEMANTIC_GIT.md`;
7. expanda o contexto apenas quando dependências ou conflitos exigirem.

## Semantic Work

- diferencie AS-IS, CHANGE e materialização física;
- trate Requirements, Decisions e Operations como dimensões distintas;
- não invente intenção, justificativa, identidade ou decisão humana;
- preserve identidade, referências e histórico;
- governe alterações semânticas materiais por CHANGE;
- valide a coerência entre significado, documentação e materialização;
- prefira validações determinísticas quando a regra puder ser verificada por estrutura, Git ou referência;
- sinalize ambiguidades materiais para revisão humana.

## Repository Scope

Quando existir, `README.md` contém somente orientação essencial. A aplicação MOP
é um contexto de uso do Semantic Git, não uma substituição da especificação.
Conhecimento específico de outras aplicações deve permanecer em seus namespaces
ou repositórios próprios.
