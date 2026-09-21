change: CHANGE-022
status: IN_PROGRESS
base_commit: ae1ea2c39f379d605037118bd249da05072bc146
approved_semantic_commit: 87349c0c1b856505bb55b147315363f99d7cb8cc
approval_scope:
  - _changes/CHANGE-022.md
reason: null

# CHANGE-022

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - Cada Semantic Namespace com conhecimento local efetivo deve poder gerar exatamente um `compiled.ai.md` derivado, reconstruível e não autoritativo, destinado a concentrar o conhecimento do domínio em uma representação determinística única para consumo por IA e outras projeções.
- **ADD R-B** - O `compiled.ai.md` deve atuar como concatenador enriquecedor: preservar integralmente os blocos-fonte locais usados hoje pela publicação (`README.md`, `REQUIREMENTS.md`, `DECISIONS.md`, `OPERATIONS.md`, quando presentes), acrescentando identidade, relações e proveniência sem resumir, parafrasear ou reinterpretar seu conteúdo.
- **ADD R-C** - Cada bloco-fonte do compilado deve ser endereçável e reversível, com metadados determinísticos suficientes para extração independente e verificação de integridade, permitindo reconstruir exatamente os mesmos textos que alimentam a publicação atual.
- **ADD R-D** - O compilado deve enriquecer os R/D/O locais com as relações explícitas já recuperáveis deterministicamente pelo Semantic Git, incluindo `satisfies`, `depends_on`, `references` e `semantic_ref`, sem utilizar IA, embeddings, similaridade vetorial ou inferência semântica probabilística.
- **ADD R-E** - Dependências externas só podem ser materializadas quando alcançadas transitivamente por relações explícitas a partir dos R/D/O locais; namespaces ancestrais, irmãos ou outros domínios não devem ser copiados integralmente apenas por posição estrutural.
- **ADD R-F** - A compilação deve ser determinística: para as mesmas fontes comprometidas, mesma versão do compilador e mesmo indexador, a saída deve ser idêntica byte a byte; timestamps de execução, UUIDs aleatórios, ordem de filesystem ou qualquer outra fonte de não determinismo são proibidos.
- **ADD R-G** - O compilado deve ser validável por regeneração exata e deve recusar fontes sem commit ou divergentes do snapshot comprometido, preservando um `source_commit`, fingerprint das fontes e hashes dos geradores envolvidos.
- **ADD R-H** - A projeção de publicação extraída do `compiled.ai.md` deve ser exatamente igual ao Markdown que o `build_publication.py` atual produz a partir das mesmas fontes; a introdução do compilado não pode alterar conteúdo, ordem ou formatação da publicação existente.
- **ADD R-I** - A publicação deve manter um caminho de contingência explícito que concatene diretamente `README.md` e R/D/O pelo publicador atual quando o `compiled.ai.md` não puder ser usado, garantindo que a geração de `PUBLICATION.md` e PDF permaneça possível sem depender do compilador.

### DECISIONS

- **ADD D-A** - Definir `<namespace-dir>/compiled.ai.md` como único artefato compilado por domínio. O arquivo é derivado, regenerável e não substitui R/D/O como fonte governada. Atende R-A e R-G.
- **ADD D-B** - Estruturar o arquivo em quatro regiões determinísticas: metadados mínimos; `Source Blocks` lossless; `Semantic Index` compacto para unidades locais; e, quando necessário, `External Semantic Units` e `Unresolved References`. Atende R-B, R-C, R-D e R-E.
- **ADD D-C** - Preservar os blocos-fonte locais literalmente, apenas normalizando UTF-8/line endings de modo compatível com a publicação atual; cada bloco registra `path`, comprimento e SHA-256 e pode ser extraído sem depender das demais regiões do compilado. Atende R-B e R-C.
- **ADD D-D** - Representar cada R/D/O local no índice embutido por ID canônico, tipo, locator de origem e relações de entrada/saída. O texto não é duplicado nessa região porque permanece nos `Source Blocks`. Atende R-C e R-D.
- **ADD D-E** - Calcular o fechamento externo somente seguindo arestas explícitas `satisfies`, `depends_on`, `references` e `semantic_ref` a partir dos nodes selecionados; apenas R/D/O externos efetivamente alcançados são materializados com texto e proveniência. Atende R-D e R-E.
- **ADD D-F** - Basear a compilação no mesmo parser/grafo determinístico já implementado por `_scripts/semantic_index.py`, sem transformar o `SEMANTIC_INDEX.json` materializado em nova fonte de verdade. Atende R-D, R-E e R-F.
- **ADD D-G** - Registrar no cabeçalho `source_commit`, `source_fingerprint`, versão e hash do compilador e hash do indexador; `source_commit` corresponde ao último commit que contém o snapshot atual das fontes efetivamente usadas, de modo que commitar o próprio artefato derivado não o torne stale por si só. Atende R-F e R-G.
- **ADD D-H** - Disponibilizar uma projeção determinística de publicação que extrai os `Source Blocks` do compilado e reutiliza o renderer atual de `build_publication.py`; sua igualdade byte a byte com a publicação atual é uma invariável testada. Atende R-H.
- **ADD D-I** - Manter `_scripts/build_publication.py` com seu caminho direto atual como contingência operacional independente do compilador. O fluxo normal pode projetar a publicação a partir de `compiled.ai.md`, enquanto o operador pode, em emergência, executar o publicador direto atual para gerar Markdown/PDF a partir de `README.md` e R/D/O. Os dois caminhos reutilizam a mesma lógica editorial e não existe fallback automático silencioso. Atende R-H e R-I.

### OPERATIONS

- **ADD O-A** - Criar `_scripts/compile_semantic_context.py` com comandos `build`, `validate` e `publication`, aceitando `--scope` para selecionar o Semantic Namespace e usando `<scope>/compiled.ai.md` como saída padrão.
- **ADD O-B** - Fazer `build` validar a estrutura do Semantic Repository, descobrir o namespace pelo mesmo mecanismo do indexador, carregar `README.md` e R/D/O locais em ordem estável e recusar namespace sem R/D/O local.
- **ADD O-C** - Implementar blocos de fonte reversíveis delimitados por marcadores determinísticos, contendo conteúdo original, comprimento e SHA-256, e implementar extração que valide comprimento, terminador, checksum e duplicidade de caminho.
- **ADD O-D** - Construir o índice embutido a partir dos nodes e edges do indexador, listar relações de entrada e saída de forma estável e materializar apenas dependências externas R/D/O alcançáveis pelas relações permitidas.
- **ADD O-E** - Detectar referências explícitas cujo endpoint não exista e registrá-las em `Unresolved References`, sem procurar substitutos semanticamente semelhantes.
- **ADD O-F** - Calcular fingerprint determinístico sobre fontes, nodes externos e edges selecionados; rejeitar fontes locais ou externas que não estejam comprometidas em `HEAD` ou que divirjam do blob comprometido.
- **ADD O-G** - Fazer `validate` regenerar o arquivo integralmente em memória e comparar o resultado byte a byte com o `compiled.ai.md` materializado, reportando `MISSING`, `INVALID` ou `DRIFT` quando aplicável.
- **ADD O-H** - Fazer o comando `publication` extrair os blocos-fonte e chamar o renderer Markdown atual de `build_publication.py`, sem introduzir nova lógica editorial.
- **ADD O-I** - Criar `_scripts/test_compiled_context.py` cobrindo pelo menos: determinismo byte a byte; extração lossless dos inputs da publicação; igualdade exata da projeção com a publicação atual; enriquecimento de relações; fechamento transitivo de dependência externa explícita; estabilidade após commit apenas do artefato derivado; detecção de drift; e rejeição de fonte sem commit/dirty.
- **ADD O-J** - Não alterar nesta CHANGE o conteúdo editorial atual de `PUBLICATION.md`; qualquer geração via compiled ou via fontes diretas deve produzir exatamente a mesma concatenação e formatação já existente.
- **ADD O-K** - Preservar sem dependência do compilador o comando direto atual de `_scripts/build_publication.py`, incluindo sua capacidade existente de gerar `PUBLICATION.pdf`, como caminho de contingência operacional.
- **ADD O-L** - Manter como teste permanente a invariável `publication(compiled) == publication(direct)` byte a byte, de forma que a existência do caminho de contingência não crie uma segunda semântica editorial.

## Validation Evidence

- Implementação inicial do compilador e suíte foram preparadas para execução determinística sem dependências externas além da biblioteca padrão e dos scripts já existentes do repositório.
- Uma fixture local equivalente às interfaces atuais do indexador/publicador executou 7 testes com sucesso, cobrindo determinismo, extração lossless, compatibilidade da publicação, fechamento transitivo de relações externas, estabilidade do artefato derivado, drift e fonte dirty.
- `_scripts/build_publication.py` permanece inalterado nesta CHANGE e, portanto, conserva o caminho direto existente de concatenação de `README.md` + R/D/O e geração de PDF sem depender de `compiled.ai.md`.
- `_scripts/test_compiled_context.py` contém a invariável que compara a projeção do compiled com `build_publication.render_publication(...)` e exige igualdade exata.
