# Compiled Semantic Context V2

Status: **PROPOSTA DE FORMATO / NÃO IMPLEMENTADO**

## Objetivo

O `compiled.ai.md` deve ser um artefato derivado, compacto e diretamente útil como contexto de IA. Ele não deve explicar o próprio Compiled Semantic Context, reproduzir documentação editorial nem expandir toda a árvore ancestral por padrão.

A regra principal da V2 é:

```text
CSC(target)
=
semântica local do target
+
fechamento transitivo das dependências explícitas externas
```

Não é:

```text
CSC(target)
=
target + todos os ancestrais completos
```

## Fechamento determinístico

1. O conjunto inicial contém todos os nodes `R`, `D` e `O` do namespace alvo.
2. Relações explícitas já reconhecidas pelo índice (`satisfies`, `depends_on`, `references`, `semantic_ref`) são resolvidas.
3. Se uma dessas relações aponta para um node fora do namespace alvo, esse node externo entra no CSC.
4. O processo continua recursivamente apenas pelas dependências explícitas desses nodes externos.
5. `parent_namespace` identifica a estrutura da árvore, mas **não inclui automaticamente o conteúdo inteiro do pai**.
6. Nenhuma similaridade vetorial, LLM ou inferência textual participa da compilação canônica.

Isso significa que uma regra ancestral só ocupa tokens no CSC quando existe uma dependência explicitamente governada que leva até ela.

## Transformações permitidas

O CSC não precisa reproduzir literalmente a formatação dos documentos-fonte. Pode fazer transformações determinísticas que aumentem densidade sem alterar significado:

- remover cabeçalhos editoriais de `REQUIREMENTS.md`, `DECISIONS.md` e `OPERATIONS.md`;
- reunir R/D/O em um único arquivo;
- qualificar IDs externos por namespace;
- converter `Atende R-...` em relação estrutural `D -> R` e remover essa frase redundante do corpo da Decision;
- ordenar nodes e relações de forma estável;
- incluir cada node apenas uma vez;
- listar somente referências irresolvidas que afetem o fechamento.

Não pode:

- resumir texto com IA;
- escolher regras por relevância aparente;
- inferir que uma Operation implementa uma Decision sem referência explícita;
- copiar todos os ancestrais apenas por estarem acima do target;
- inserir notas de design, tutorial ou justificativas arquiteturais no arquivo de runtime.

## Formato Markdown proposto

```markdown
# CSC <namespace>
format: csc-md/2
target: <namespace>
source_commit: <sha>
authority: DERIVED

## Requirements
- R-001 | <texto>

## Decisions
- D-001 -> R-001,R-003 | <texto sem a cláusula Atende já materializada>

## Operations
- O-001 -> D-001 | <texto, se a dependência estiver explícita>
- O-002 | <texto, quando nenhuma dependência estiver explicitamente declarada>

## External Dependencies
- parent/domain:D-004 | <texto>

## Unresolved
- <referência que não pôde ser resolvida>
```

Se `External Dependencies` ou `Unresolved` estiver vazio, a seção pode ser omitida.

## Por que isto é compilação e não concatenação

A compilação V2 executa quatro operações que a leitura direta dos Markdown não oferece de forma pronta:

1. une os três tipos de artefato locais em uma unidade de contexto;
2. resolve relações explícitas e as transforma em estrutura compacta;
3. resolve somente as dependências externas efetivamente referenciadas;
4. remove redundância editorial e relacional já representada estruturalmente.

O resultado é uma representação materializada do subgrafo semântico necessário para o domínio, e não uma publicação alternativa.

## Diferença para PUBLICATION.md

| Dimensão | `PUBLICATION.md` | `compiled.ai.md` V2 |
|---|---|---|
| Consumidor | humano | IA |
| Forma | documento editorial | subgrafo semântico linearizado |
| Cabeçalhos explicativos | úteis | removidos |
| Texto R/D/O | legível/editorial | preservado de forma compacta |
| Relações | podem ficar dentro das frases | extraídas para sintaxe estrutural |
| Herança | pode ser explicada narrativamente | somente dependências explícitas externas são materializadas |
| Ancestral completo | não costuma repetir | também não repete por padrão |
| Proveniência detalhada | opcional | não entra no runtime base; permanece recuperável pelo índice |
| Notas de design | possíveis | proibidas |
| Objetivo | comunicar | minimizar reconstrução + minimizar tokens irrelevantes |

## Consequência importante

Se um domínio depende semanticamente de uma regra ancestral, mas **não existe nenhuma relação explícita que permita chegar a ela**, a V2 não deve compensar isso copiando o ancestral inteiro.

Esse caso revela uma lacuna estrutural do grafo. O compilador deve permanecer conservador.

Assim, o CSC também funciona como teste da qualidade das relações governadas: quanto melhor estiverem explicitadas as dependências reais, mais preciso e compacto será o contexto compilado.

## Arquivo de validação

A simulação concreta da V2 para o domínio real `mop` está em:

`simulations/mop.compiled.ai.v2.md`

Ela usa o conteúdo real da `main`, mas foi montada manualmente para validar o formato. **Ainda não existe compilador implementado nesta branch.**
