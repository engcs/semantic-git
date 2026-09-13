change: CHANGE-004
status: RECONCILED
base_commit: ff0433d98f4edd8813b81d1c68a6882a25302476
approved_semantic_commit: c7a54dfdc6f32c0c5906c621887d55b7596ec966
approval_scope:
  - SEMANTIC_GIT.md
  - changes/CHANGE-004.md
reason: null

# CHANGE-004

## Semantic Diff

### REQUIREMENTS

- **MODIFY** - Restringir a proteção contra colisão de ID entre namespaces ancestrais e descendentes às entidades semânticas permanentes R/D/O.

  ```text
  - IDs oficiais não podem reutilizar, em namespace descendente, ID oficial do mesmo tipo já utilizado por qualquer namespace ancestral.
  + IDs oficiais R-, D- e O- não podem colidir com ID do mesmo tipo na cadeia ancestral aplicável; essa proteção não se aplica a CHANGE-.
  ```

- **ADD** - Exigir que cada Semantic Namespace controle uma sequência local independente de CHANGE-IDs, sem reservar ou consumir números em namespaces ancestrais, descendentes ou irmãos.
- **ADD** - Permitir que namespaces distintos possuam o mesmo CHANGE-ID curto, preservando como identidade inequívoca a forma `<namespace>:<CHANGE-ID>`.
- **ADD** - Exigir que referências persistidas, dependências, autorizações e gates que identifiquem CHANGE utilizem sua identidade canônica quando a forma curta puder ser ambígua.
- **ADD** - Exigir que a branch Git de um CHANGE seja globalmente única no repositório, ainda que CHANGE-IDs locais se repitam.

### DECISIONS

- **MODIFY** - Separar a política de alocação de IDs oficiais em proteção ancestral para R/D/O e sequência estritamente local para CHANGE.
- **ADD** - Usar `change/<namespace-key>/<CHANGE-ID>-<slug-curto>` como convenção de branch, com `root` reservado para a raiz e representação reversível e compatível com Git para os demais namespaces.
- **ADD** - Tratar o namespace representado na branch como redundância operacional verificável, sem torná-lo fonte de autoridade para escopo ou identidade semântica.
- **ADD** - Resolver dependências entre CHANGEs por identidade canônica completa e detectar ciclos por `<namespace>:<CHANGE-ID>`, nunca apenas pelo ID curto.
- **MODIFY** - Tornar os caminhos ativo e arquivado relativos ao diretório documental do Semantic Namespace controlador.

  ```text
  - changes/<CHANGE-ID>.md
  + <namespace-dir>/changes/<CHANGE-ID>.md

  - changes/archived/<CHANGE-ID>.md
  + <namespace-dir>/changes/archived/<CHANGE-ID>.md
  ```

- **MODIFY** - Resolver a relocação de `approval_scope` pela identidade canônica e pelo namespace de origem, nunca por busca global de basename ou CHANGE-ID curto.
- **ADD** - Exigir identidade canônica em autorizações semântica, de implementação e de merge; no merge, exigir também branch globalmente única e destino.
- **ADD** - Preservar os CHANGE-IDs e nomes de branches historicamente estabelecidos antes desta mudança, sem renumeração ou migração retroativa obrigatória.
- **ADD** - Identificar a especificação resultante como Semantic Git v1.4.

### OPERATIONS

- **ADD** - Alocar o próximo CHANGE-ID consultando CHANGEs ativos, arquivados e históricos do mesmo namespace, sem consultar números de outros namespaces.
- **ADD** - Continuar verificando colisões na cadeia ancestral durante criação e promoção de IDs R/D/O.
- **ADD** - Validar atomicamente a unicidade da identidade canônica, do caminho local e da branch Git antes de criar um CHANGE.
- **ADD** - Aplicar a convenção de branch com namespace aos novos CHANGEs criados após esta mudança, preservando branches preexistentes e a branch desta própria transformação.
- **ADD** - Arquivar cada CHANGE no diretório `changes/archived/` do namespace que controla sua identidade.
- **ADD** - Resolver índices, referências, dependências, aprovações e gates por identidade canônica de CHANGE.
- **ADD** - Produzir `FAIL` para reutilização de CHANGE-ID no mesmo namespace, `IMPLEMENTATION_BLOCKED` para autorização ambígua e `MERGE_BLOCKED` para branch, identidade ou destino não identificados inequivocamente.
