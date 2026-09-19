change: CHANGE-021
status: DRAFT
base_commit: 463bf8c7c6578417e0eba51cfab98c95af2a8222
approved_semantic_commit: null
approval_scope: null
reason: null

# CHANGE-021

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - O Semantic Git deve oferecer um índice semântico global, derivado e reconstruível, capaz de representar deterministicamente os Semantic Namespaces e os principais artefatos governados do repositório sem criar uma nova fonte de verdade.
- **ADD R-B** - O índice deve ser gerado somente a partir de fontes governadas e estruturalmente válidas do repositório, incluindo R/D/O, CHANGEs e `_memory/FINDINGS.yaml` quando presentes, preservando proveniência suficiente para reabrir a fonte original.
- **ADD R-C** - O índice deve representar entidades e relações por estruturas explícitas de `nodes` e `edges`, com identidades estáveis derivadas das identidades canônicas existentes, evitando interpretação probabilística quando a relação puder ser obtida estruturalmente.
- **ADD R-D** - Todo nó indexado deve possuir proveniência mínima com caminho de origem e locator estável; o snapshot do índice deve registrar o commit-fonte do qual foi gerado. O índice não substitui a leitura da fonte autoritativa para conclusões materiais.
- **ADD R-E** - O índice deve ser validável deterministicamente quanto a unicidade de IDs, existência das fontes, integridade de referências, validade dos tipos, existência dos endpoints de cada edge e correspondência com o snapshot-fonte.
- **ADD R-F** - O índice deve apoiar carregamento progressivo de contexto, permitindo que humanos e IAs localizem elementos e relações relevantes antes de abrir os documentos completos, reduzindo leitura desnecessária sem alterar a autoridade semântica.
- **ADD R-G** - A primeira versão deve permanecer tecnicamente simples e portátil: JSON versionado como artefato derivado principal, sem banco de grafos, embeddings, vector database, GraphQL, RDF, SQLite obrigatório ou framework externo de grafo.
- **ADD R-H** - Falha de geração ou validação do índice deve ser tratada como incompatibilidade estrutural/indexador ou estrutura inválida, nunca resolvida por adivinhação da IA.

### DECISIONS

- **ADD D-A** - Criar `_index/SEMANTIC_INDEX.json` no root físico do repositório como artefato derivado global. `_index/` não é Semantic Namespace, não contém R/D/O, não participa de herança e não possui autoridade normativa. Atende R-A e R-G.
- **ADD D-B** - Usar formato JSON com `schema_version`, `source_commit`, `nodes` e `edges`. Nós iniciais incluem `namespace`, `requirement`, `decision`, `operation`, `change` e `finding`. Atende R-C e R-G.
- **ADD D-C** - Usar relações iniciais pequenas e explícitas, como `contains`, `parent_namespace`, `references`, `satisfies`, `implemented_by`, `introduced_by`, `modified_by`, `related_to` e `semantic_ref`, emitindo apenas relações demonstráveis pela estrutura ou referências presentes nas fontes. Atende R-C.
- **ADD D-D** - Para cada nó, registrar `source.path` e `source.locator`; registrar commit-fonte global em `source_commit`. Consultas ao índice devem poder retornar esses locators para posterior abertura da fonte original. Atende R-D e R-F.
- **ADD D-E** - O índice deve ser reconstruído de forma determinística a partir do snapshot do repositório. Sua exclusão não pode causar perda de conhecimento semântico; discrepâncias entre índice e fontes são resolvidas regenerando/validando o índice a partir das fontes. Atende R-A, R-D e R-H.
- **ADD D-F** - O indexador deve depender do padrão documental canônico do Semantic Git e do validador estrutural, preferindo parsing específico e determinístico das estruturas conhecidas a parsing genérico orientado por IA. Atende R-B e R-H.
- **ADD D-G** - A primeira implementação deve usar a biblioteca padrão do Python sempre que possível e não introduzir NetworkX, Neo4j, RDF/SPARQL, LangChain, LlamaIndex, embeddings ou banco vetorial. SQLite e NetworkX permanecem possíveis otimizações futuras derivadas do mesmo JSON, fora do escopo desta CHANGE. Atende R-G.
- **ADD D-H** - O índice pode conter texto resumido/normalizado suficiente para descoberta e consulta, mas respostas materiais devem tratar o índice como roteador de contexto: localizar no índice, reabrir a fonte, então concluir. Atende R-D e R-F.

### OPERATIONS

- **ADD O-A** - Criar `_scripts/semantic_index.py` com comandos `build`, `validate` e `query`, operando a partir do root do repositório e produzindo `_index/SEMANTIC_INDEX.json`.
- **ADD O-B** - Implementar descoberta determinística de Semantic Namespaces por R/D/O canônicos e indexação de Requirements, Decisions e Operations com identidade qualificada pelo namespace e locator original.
- **ADD O-C** - Indexar CHANGEs ativos e arquivados e findings de `_memory/FINDINGS.yaml` quando presentes, preservando estado, namespace controlador e referências explicitamente recuperáveis sem promover findings a autoridade semântica.
- **ADD O-D** - Construir edges somente quando a relação puder ser provada por estrutura, namespace, campo/referência explícita ou convenção canônica do Semantic Git; referências não resolvidas devem falhar validação ou ser reportadas explicitamente, nunca virar edge inventado.
- **ADD O-E** - Validar no mínimo: `schema_version` suportada; `source_commit`; IDs de nós únicos; tipos conhecidos; `source.path` existente; locators necessários; endpoints de edges existentes; ausência de edges duplicados; e consistência básica entre namespace e caminho.
- **ADD O-F** - Integrar a geração/validação ao fluxo estrutural de forma que um repositório estruturalmente válido produza um índice determinístico e um índice inválido não seja silenciosamente aceito.
- **ADD O-G** - Atualizar `AGENTS.md` para orientar IAs a consultar o índice para descoberta, navegação e redução de contexto, mas reabrir a fonte autoritativa antes de sustentar conclusões semânticas materiais.
- **ADD O-H** - Documentar em `README.md` ou documentação operacional equivalente a finalidade de `_index/`, seu caráter derivado/não normativo e os comandos mínimos de build, validate e query.
- **ADD O-I** - Adicionar validações determinísticas cobrindo ao menos: geração idempotente; IDs únicos; edge para endpoint inexistente; source inexistente; namespace pai/filho; R/D/O; CHANGE arquivada; finding com `semantic_refs`; e detecção de índice desatualizado em relação ao snapshot-fonte.
- **ADD O-J** - Não introduzir SQLite, NetworkX, embeddings ou banco de grafos nesta CHANGE; qualquer cache ou análise avançada futura deve ser regenerável a partir de `SEMANTIC_INDEX.json` e das fontes governadas.
