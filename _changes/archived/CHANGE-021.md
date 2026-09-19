change: CHANGE-021
status: MERGED
base_commit: 463bf8c7c6578417e0eba51cfab98c95af2a8222
approved_semantic_commit: 38841a94a4f850bb32c2786794f43690de07f3aa
approval_scope:
  - _changes/CHANGE-021.md
reason: null

# CHANGE-021

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - O Semantic Git deve oferecer um índice semântico derivado e reconstruível em qualquer Semantic Namespace, capaz de representar deterministicamente o conhecimento pertencente ao namespace escolhido e aos seus descendentes sem criar uma nova fonte de verdade; `root` é apenas o caso de maior escopo e, por isso, enxerga toda a árvore semântica.
- **ADD R-B** - Cada índice deve ser gerado somente a partir de fontes governadas e estruturalmente válidas do repositório, incluindo R/D/O, CHANGEs e `_memory/FINDINGS.yaml` quando presentes no escopo, preservando proveniência suficiente para reabrir a fonte original.
- **ADD R-C** - O índice deve representar entidades e relações por estruturas explícitas de `nodes` e `edges`, com identidades estáveis derivadas das identidades canônicas existentes, evitando interpretação probabilística quando a relação puder ser obtida estruturalmente.
- **ADD R-D** - Todo nó indexado deve possuir proveniência mínima com caminho de origem e locator estável; o snapshot do índice deve registrar o escopo, o commit-fonte e uma impressão determinística das fontes utilizadas. O índice não substitui a leitura da fonte autoritativa para conclusões materiais.
- **ADD R-E** - O índice deve ser validável deterministicamente quanto a unicidade de IDs, existência das fontes, integridade de referências, validade dos tipos, existência dos endpoints de cada edge, coerência de escopo e correspondência com o snapshot-fonte.
- **ADD R-F** - O índice deve apoiar carregamento progressivo de contexto, permitindo que humanos e IAs localizem elementos e relações relevantes antes de abrir os documentos completos, reduzindo leitura desnecessária sem alterar a autoridade semântica.
- **ADD R-G** - Um índice local deve permanecer pequeno: contém o namespace solicitado e seus descendentes, podendo incluir apenas stubs externos mínimos para entidades explicitamente referenciadas fora do escopo, suficientes para navegação e reabertura da fonte, sem importar indiscriminadamente o conteúdo dos ancestrais ou de namespaces irmãos.
- **ADD R-H** - A primeira versão deve permanecer tecnicamente simples e portátil: JSON versionado como artefato derivado principal, sem banco de grafos, embeddings, vector database, GraphQL, RDF, SQLite obrigatório ou framework externo de grafo.
- **ADD R-I** - Falha de geração ou validação do índice deve ser tratada como incompatibilidade estrutural/indexador ou estrutura inválida, nunca resolvida por adivinhação da IA.

### DECISIONS

- **ADD D-A** - Definir `_index/SEMANTIC_INDEX.json` como artefato derivado opcional do Semantic Namespace em cujo diretório documental ele é gerado. `_index/` não é Semantic Namespace, não contém R/D/O, não participa de herança e não possui autoridade normativa. No root físico do Semantic Repository, `_index/SEMANTIC_INDEX.json` representa o índice de `root`; em um namespace descendente, `<namespace-dir>/_index/SEMANTIC_INDEX.json` representa aquele escopo. Atende R-A e R-H.
- **ADD D-B** - Usar formato JSON com, no mínimo, `schema_version`, `scope`, `source_commit`, `source_fingerprint`, `nodes` e `edges`. `scope` registra identidade canônica e caminho do namespace indexado. Nós iniciais incluem `namespace`, `requirement`, `decision`, `operation`, `change` e `finding`. Atende R-C, R-D e R-H.
- **ADD D-C** - Considerar in-scope o namespace solicitado e todos os seus descendentes semânticos. O índice de `root` contém toda a árvore; índices descendentes não devem copiar a árvore inteira nem o conteúdo integral dos ancestrais. Atende R-A, R-F e R-G.
- **ADD D-D** - Quando uma relação explícita partir de um nó in-scope para entidade fora do escopo, incluir somente um nó externo mínimo, marcado como externo, com identidade, tipo e proveniência necessárias para resolver a referência. Não expandir transitivamente o conteúdo externo por padrão. Atende R-F e R-G.
- **ADD D-E** - Usar relações iniciais pequenas e explícitas, como `contains`, `parent_namespace`, `references`, `satisfies`, `depends_on` e `semantic_ref`, emitindo apenas relações demonstráveis pela estrutura ou referências presentes nas fontes. Relações adicionais só devem ser emitidas quando houver evidência determinística equivalente. Atende R-C.
- **ADD D-F** - Para cada nó, registrar `source.path` e `source.locator`; registrar no snapshot `source_commit` e `source_fingerprint`. Consultas ao índice devem retornar esses locators para posterior abertura da fonte original. Atende R-D e R-F.
- **ADD D-G** - O índice deve ser reconstruído de forma determinística a partir das mesmas fontes e do mesmo escopo. Sua exclusão não pode causar perda de conhecimento semântico; discrepâncias entre índice e fontes são resolvidas regenerando/validando o índice a partir das fontes. Atende R-A, R-D e R-I.
- **ADD D-H** - O indexador deve depender do padrão documental canônico do Semantic Git e do validador estrutural, preferindo parsing específico e determinístico das estruturas conhecidas a parsing genérico orientado por IA. Atende R-B e R-I.
- **ADD D-I** - A primeira implementação deve usar a biblioteca padrão do Python sempre que possível e não introduzir NetworkX, Neo4j, RDF/SPARQL, LangChain, LlamaIndex, embeddings ou banco vetorial. SQLite e NetworkX permanecem possíveis otimizações futuras derivadas do mesmo JSON, fora do escopo desta CHANGE. Atende R-H.
- **ADD D-J** - O índice pode conter texto resumido/normalizado suficiente para descoberta e consulta, mas respostas materiais devem tratá-lo como roteador de contexto: localizar no índice, reabrir a fonte, então concluir. Atende R-D e R-F.

### OPERATIONS

- **ADD O-A** - Alterar `SEMANTIC_GIT.md` para reconhecer `_index/` como diretório auxiliar reservado e derivado de um Semantic Namespace, definir o caráter scoped/reconstruível do índice, sua não autoridade, progressive disclosure e a regra de que `root` é apenas o maior escopo.
- **ADD O-B** - Criar `_scripts/semantic_index.py` com comandos `build`, `validate` e `query`, permitindo selecionar o namespace por diretório documental e produzindo `<namespace-dir>/_index/SEMANTIC_INDEX.json`; quando o diretório for a raiz do Semantic Repository, produzir o índice de `root`.
- **ADD O-C** - Implementar descoberta determinística de Semantic Namespaces por R/D/O canônicos e diretórios auxiliares locais permitidos, respeitando diretórios reservados de organização e produzindo identidades canônicas coerentes com o namespace controlador.
- **ADD O-D** - Indexar Requirements, Decisions e Operations com identidade qualificada pelo namespace e locator original; indexar CHANGEs ativos e arquivados e findings de `_memory/FINDINGS.yaml` quando presentes, preservando estado e referências explicitamente recuperáveis sem promover findings a autoridade semântica.
- **ADD O-E** - Construir edges somente quando a relação puder ser provada por estrutura, namespace, campo/referência explícita ou convenção canônica do Semantic Git; referências fora do escopo devem gerar stubs externos mínimos e referências não resolvidas devem falhar validação ou ser reportadas explicitamente, nunca virar edge inventado.
- **ADD O-F** - Validar no mínimo: `schema_version` suportada; identidade e caminho de `scope`; `source_commit`; `source_fingerprint`; IDs de nós únicos; tipos conhecidos; `source.path` existente; locators necessários; endpoints de edges existentes; ausência de edges duplicados; coerência namespace/caminho; e marcação correta de nós externos.
- **ADD O-G** - Fazer `build` e `validate` dependerem de validação estrutural bem-sucedida do Semantic Repository e garantir geração determinística/idempotente para o mesmo escopo e snapshot-fonte. Um índice inválido ou stale não deve ser silenciosamente aceito.
- **ADD O-H** - Atualizar `AGENTS.md` para orientar IAs a preferir o índice do menor escopo suficiente para descoberta, navegação e redução de contexto, subir seletivamente para referências externas/ancestrais quando necessário e reabrir a fonte autoritativa antes de sustentar conclusões semânticas materiais.
- **ADD O-I** - Atualizar `README.md` com a finalidade de `_index/`, seu caráter derivado/não normativo, a relação entre índices locais e o índice de `root` e os comandos mínimos de `build`, `validate` e `query`.
- **ADD O-J** - Adicionar validações determinísticas cobrindo ao menos: geração idempotente; IDs únicos; edge para endpoint inexistente; source inexistente; namespace pai/filho; escopo descendente sem importar irmãos; stub para referência externa; R/D/O; CHANGE arquivada; finding com `semantic_refs`; e detecção de índice desatualizado em relação às fontes.
- **ADD O-K** - Materializar e validar o índice de `root` desta versão como demonstração canônica, sem exigir que índices de todos os namespaces sejam mantidos simultaneamente; índices descendentes devem poder ser gerados sob demanda pelo mesmo comando.
- **ADD O-L** - Não introduzir SQLite, NetworkX, embeddings ou banco de grafos nesta CHANGE; qualquer cache ou análise avançada futura deve ser regenerável a partir de `SEMANTIC_INDEX.json` e das fontes governadas.

## Validation Evidence

- O validator estrutural passou sem exigir alteração retroativa de CHANGEs arquivadas.
- CHANGEs arquivadas preservam integralmente seu conteúdo histórico; campos de aprovação modernos ausentes não são fabricados retroativamente.
- Metadados modernos presentes em arquivos históricos continuam sendo validados quanto à forma.
- A suíte `test_semantic_index.py` passou com fixture de CHANGE arquivada legada sem `approved_semantic_commit`/`approval_scope`.
- As fixtures determinísticas de revisão matemática permanecem válidas.
- O índice de `root` foi materializado, validado e consultado com sucesso.

### Reconciliation Summary

- O índice scoped está implementado em JSON, com `nodes`, `edges`, proveniência, `source_commit`, `source_fingerprint`, stubs externos e comandos `build`, `validate` e `query`.
- A validação estrutural é pré-condição do índice, mas respeita a imutabilidade histórica: evolução do validator não autoriza reescrita de CHANGE arquivada.
- O índice de `root` é apenas o maior escopo; índices descendentes permanecem reproduzíveis sob demanda.
