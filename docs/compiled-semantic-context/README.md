# Compiled Semantic Context

Status: **SIMULATION / DESIGN STUDY**

Este diretório explora um artefato derivado do Semantic-Git chamado **Compiled Semantic Context** (CSC).

O CSC é uma visão determinística, redundante de propósito e orientada ao consumo por IA. Ele não substitui Requirements, Decisions, Operations, CHANGE, índice semântico ou publicação. A fonte de verdade permanece nos artefatos governados do Semantic-Git.

## Ideia central

Um domínio humano deve continuar organizado para leitura, manutenção e governança. O CSC existe para evitar que uma IA precise navegar manualmente por vários arquivos e níveis de herança antes de responder sobre um domínio.

O compilador não interpreta linguagem natural para decidir o que parece relevante. Ele só pode materializar o que for recuperável por regras estruturais e referências explícitas.

Em termos conceituais:

```text
Semantic-Git governado
        |
        | compilação determinística
        v
Compiled Semantic Context
        |
        | seleção posterior para uma pergunta
        v
Prompt / contexto de IA
```

## O que a compilação pode fazer deterministicamente

- identificar o namespace alvo;
- percorrer a cadeia de namespaces ancestrais definida pela estrutura do repositório;
- copiar, sem paráfrase, R/D/O dos escopos incluídos;
- preservar IDs qualificados por namespace;
- resolver referências explícitas, como `Atende R-...`, quando não houver ambiguidade;
- materializar relações já disponíveis no índice semântico;
- registrar origem de cada entidade;
- listar referências que não puderam ser resolvidas;
- registrar o commit/fingerprint usado como fonte;
- ordenar o conteúdo de forma estável.

## O que a compilação não deve fazer

- inferir que duas frases têm o mesmo significado;
- inventar relações D -> O não declaradas;
- escolher ancestrais por "relevância semântica";
- resumir, reescrever ou melhorar R/D/O;
- criar glossário por interpretação;
- corrigir lacunas do domínio;
- transformar inferência de LLM em verdade compilada.

Esses pontos podem existir em uma camada posterior de análise por IA, mas não no compilador determinístico.

## Publicação Markdown x Compiled Semantic Context

| Dimensão | `PUBLICATION.md` | `compiled.ai.md` / CSC |
|---|---|---|
| Consumidor principal | Humano | IA |
| Objetivo | Comunicar e publicar o conhecimento do domínio | Entregar contexto semanticamente fechado por regras estruturais |
| Natureza | Visão de apresentação | Artefato intermediário de contexto |
| Fonte de verdade | Não | Não |
| Derivado do Semantic-Git | Sim | Sim |
| Otimização principal | Legibilidade | Explicitude e reconstrução |
| R/D/O locais | Sim | Sim |
| R/D/O ancestrais | Evita repetir quando a herança basta | Materializa a cadeia ancestral conforme regra de compilação |
| Herança | Pode ser apenas declarada | É expandida no artefato |
| Redundância | Evitada quando prejudica a leitura | Aceita intencionalmente |
| IDs qualificados | Conforme necessidade editorial | Preferencialmente sempre |
| Relações explícitas | Podem aparecer integradas ao texto | Devem ganhar uma seção estruturada adicional |
| Relações inferidas | Não | Não |
| Proveniência por entidade | Secundária | Parte do contrato |
| Referências irresolvidas | Podem ser apresentadas editorialmente | Devem ser enumeradas mecanicamente |
| Histórico completo | Não é o objetivo | Não é o objetivo |
| Paráfrase/resumo | Permitidos pela estratégia de publicação | Evitados na compilação base |
| Tamanho | Conciso para leitura | Completo dentro do fechamento definido |
| Uso como entrada de LLM | Possível | Projetado para isso |
| Edição manual | Não recomendada se gerada | Proibida: deve ser regenerável |

Resumo:

```text
PUBLICATION.md = "mostre este domínio para uma pessoa"
compiled.ai.md = "entregue à IA o fechamento estrutural deste domínio"
```

## Contrato mínimo proposto do CSC

```markdown
# COMPILED SEMANTIC CONTEXT

## Metadata
- target_namespace
- source_commit
- source_fingerprint
- compiler_version
- generated
- authority: DERIVED

## Reading Contract
- artefato derivado
- sem inferências novas
- fontes governadas continuam autoritativas

## Effective Scope Chain
- ancestor 0
- ancestor 1
- target

## Scope: <ancestor>
### Requirements
### Decisions
### Operations

## Scope: <target>
### Requirements
### Decisions
### Operations

## Explicit Relationships
- source
- predicate
- target
- evidence/origin

## Unresolved References

## Provenance
```

## Regra de fechamento proposta

Para um namespace alvo `A/B/C`, a forma mais simples e auditável de compilação é:

```text
A
A/B
A/B/C
```

O compilador materializa os R/D/O existentes em cada namespace da cadeia. Ele não tenta decidir quais entidades ancestrais "parecem" relevantes.

Essa estratégia favorece determinismo e auditabilidade. Uma otimização futura de tokens deve acontecer **depois** da compilação, em outro estágio, e não alterar o CSC canônico.

## Relações explícitas

A compilação pode aproveitar o `SEMANTIC_INDEX.json` e a sintaxe governada já reconhecida pelo Semantic-Git. Quando uma relação não estiver representada explicitamente, ela deve permanecer ausente.

Exemplo:

```text
mop:D-002 --atende--> mop:R-001
```

é compilável se essa relação estiver representada pelo índice/regra estrutural.

Já uma relação do tipo:

```text
mop:O-009 --executa--> mop:D-004
```

não deve ser criada apenas porque um modelo ou humano considera a relação semanticamente plausível.

## Simulações incluídas

- `simulations/mop.compiled.ai.md`: compilação concreta do único domínio atualmente materializado em `_applications` na `main` (`mop`).
- `simulations/child-domain.compiled.ai.md`: forma estrutural para um domínio filho, sem introduzir conhecimento de negócio inexistente na `main`.
- `simulations/grandchild-domain.compiled.ai.md`: forma estrutural para um domínio com dois níveis ancestrais, representando o caso de uso discutido para domínios mais profundos.

Os dois últimos arquivos são deliberadamente estruturais: os placeholders evitam transformar uma simulação em AS-IS não aprovado.

## Decisão ainda aberta

Esta branch não implementa um compilador. Ela serve para validar primeiro:

1. se o artefato faz sentido;
2. qual deve ser o contrato do arquivo;
3. quanta redundância ancestral é aceitável;
4. quais relações podem ser resolvidas deterministicamente;
5. como o CSC deve se distinguir da publicação humana.
