change: CHANGE-023
status: RECONCILED
base_commit: 7979573be557ed65c74b6afecd07724af4e250c0
approved_semantic_commit: d9960df0ed1de58b26142ca04b6232d2fe0d5157
approval_scope:
  - _changes/CHANGE-023.md
reason: null

# CHANGE-023

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - `_memory` deve preservar o que foi descoberto durante investigação quando esse conhecimento analítico for material, caro ou perigoso de redescobrir, sem competir com R/D/O como fonte semântica autoritativa.
- **ADD R-B** - `FINDINGS.yaml` deve permanecer o arquivo canônico padrão da memória analítica nesta versão do protocolo; `_memory` é o contêiner conceitual e poderá receber outros tipos de arquivo somente por evolução normativa futura explícita, sem exigir que tais extensões existam hoje.
- **ADD R-C** - Um finding promovido a R/D/O pode permanecer na memória para preservar descoberta, evidência, risco e proveniência, mas não deve duplicar o texto normativo do R/D/O; a sincronização entre memória e AS-IS deve ser referencial, não textual.
- **ADD R-D** - Toda alteração material em R/D/O que modifique, remova ou substitua uma entidade referenciada por finding promovido deve reconciliar os findings afetados antes que o CHANGE possa alcançar `RECONCILED`.
- **ADD R-E** - A reconciliação de memória deve preservar findings não relacionados e deve atualizar somente os findings semanticamente afetados pela mudança, evitando reescrita global, append cego ou substituição integral de `_memory`.
- **ADD R-F** - A reconciliação de um finding afetado deve resultar em um estado analítico coerente com a nova realidade: permanecer promovido, atualizar suas referências semânticas, tornar-se resolvido ou superseded, ou voltar a `active` quando a questão analítica deixar de estar plenamente coberta pelo R/D/O vigente.

### DECISIONS

- **ADD D-A** - Tratar `_memory/` como contêiner reservado e extensível de memória analítica do namespace, mantendo `FINDINGS.yaml` como único arquivo canônico permitido nesta versão. Novos arquivos dentro de `_memory` exigem mudança normativa futura do protocolo. Atende R-A e R-B.
- **ADD D-B** - Definir a separação de responsabilidades como `R/D/O = memória do conhecimento autoritativo` e `_memory/FINDINGS.yaml = memória da descoberta`, incluindo evidência, risco, interpretação analítica e relação com o conhecimento promovido. Atende R-A e R-C.
- **ADD D-C** - Findings promovidos devem poder registrar referências canônicas às entidades R/D/O resultantes, preservando evidência e risco sem copiar a formulação normativa correspondente. Atende R-C.
- **ADD D-D** - Introduzir reconciliação inversa `R/D/O → findings`: ao modificar, remover ou substituir R/D/O, localizar findings promovidos que referenciem as entidades afetadas e exigir sua reconciliação antes de `RECONCILED`. Atende R-D.
- **ADD D-E** - A reconciliação deve ser seletiva e orientada por referências explícitas ou relações determinísticas disponíveis no índice; ausência de relação com a mudança não autoriza alterar finding existente. Atende R-E.
- **ADD D-F** - Para cada finding afetado, aplicar um resultado explícito entre: preservar `promoted`; atualizar `semantic_refs`; marcar `resolved`; marcar `superseded`; ou retornar a `active` com estado semântico não resolvido quando a nova verdade reabrir a questão analítica. Atende R-F.

### OPERATIONS

- **ADD O-A** - Atualizar a seção normativa de memória analítica para declarar explicitamente `_memory` como contêiner do que foi descoberto e `FINDINGS.yaml` como arquivo padrão canônico da versão atual, deixando extensões futuras reservadas a alteração normativa posterior.
- **ADD O-B** - Formalizar no schema de finding promovido um campo de referências semânticas canônicas, suficiente para localizar as entidades R/D/O às quais a descoberta foi promovida sem duplicar seu texto normativo.
- **ADD O-C** - Integrar ao fluxo de `RECONCILIATION` uma verificação determinística de findings promovidos que apontem para R/D/O afetado pelo Semantic Diff do CHANGE.
- **ADD O-D** - Bloquear `RECONCILED` quando houver finding promovido semanticamente afetado cuja relação com o novo R/D/O não tenha sido reconciliada.
- **ADD O-E** - Atualizar o validador estrutural e a skill de memória para aceitar e validar as referências semânticas de findings promovidos e para preservar findings não relacionados.
- **ADD O-F** - Adicionar testes cobrindo: finding promovido que permanece válido após MODIFY; referência que precisa ser atualizada após REMOVE + ADD; finding que volta a `active`; finding resolvido ou superseded; bloqueio de reconciliação quando finding afetado permanece stale; e não alteração de finding não relacionado.
- **ADD O-G** - Não introduzir nesta CHANGE arquivos adicionais dentro de `_memory`; a implementação deve apenas tornar explícita a extensibilidade futura e manter `FINDINGS.yaml` como padrão único atual.

## Validation Evidence

- `SEMANTIC_GIT.md` foi atualizado para definir `_memory` como memória da descoberta, manter `FINDINGS.yaml` como único arquivo canônico atual e reservar extensões futuras a evolução normativa explícita.
- A seção de promoção passou a exigir reconciliação inversa seletiva `R/D/O → findings` quando entidades referenciadas por findings promovidos forem materialmente modificadas, removidas ou substituídas.
- O gate de fechamento de CHANGE passou a exigir reconciliação dos findings promovidos relacionados a R/D/O afetado antes de `RECONCILED`.
- `.opencode/skills/semantic-memory/SKILL.md` foi alinhada ao contrato normativo e explicita o fluxo de reconciliação inversa e a preservação de findings não relacionados.
- `_scripts/_internal/validate_structure.py` passou a validar forma canônica e duplicidade de `semantic_refs` quando presentes.
- `_scripts/_internal/memory_reconciliation.py` localiza deterministicamente R/D/O afetado pelo Semantic Diff e findings `promoted` ligados por `semantic_ref`, reutilizando a relação já produzida pelo índice semântico.
- `_scripts/test_memory_reconciliation.py` cobre MODIFY com finding promovido, atualização de referência após REMOVE+ADD, retorno a `active`, estados `resolved`/`superseded`, preservação de finding não relacionado, referências canônicas e a superfície atual de `_memory`.
- A validação final foi executada no GitHub Actions, run `36255673864`, em Python 3.12: testes direcionados, validação estrutural e descoberta completa de testes em `_scripts` concluíram com sucesso.
- Os workflows e o aplicador temporários usados somente para executar a validação remota foram removidos da branch após a execução.

## Reconciliation Summary

- O contrato implementado corresponde ao snapshot aprovado em `d9960df0ed1de58b26142ca04b6232d2fe0d5157`; não houve alteração material posterior do Semantic Diff aprovado.
- `root:CHANGE-023` adiciona somente novas regras ao protocolo e não modifica, remove ou substitui entidade R/D/O existente; portanto, o conjunto de findings promovidos impactados pela própria CHANGE é vazio.
- A implementação mantém uma única autoridade textual: R/D/O contém o conhecimento normativo e `_memory/FINDINGS.yaml` preserva descoberta, evidência, risco e referências à autoridade.
- Nenhum novo arquivo permanente foi introduzido dentro de `_memory`; `FINDINGS.yaml` permanece o único arquivo canônico permitido nesta versão.
- O diff final foi revisado após a remoção dos artefatos temporários e contém apenas protocolo, skill, CHANGE, validador, mecanismo determinístico de descoberta de impacto e seus testes.
