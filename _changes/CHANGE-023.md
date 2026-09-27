change: CHANGE-023
status: IN_PROGRESS
base_commit: 7979573be557ed65c74b6afecd07724af4e250c0
approved_semantic_commit: cf222109e114960196c33a1b08e6b12f3cd30e78
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
- **ADD R-G** - Correções ou complementos materiais fornecidos pelo humano durante uma investigação devem poder ser preservados em `_memory/FINDINGS.yaml` como memória analítica, sem se tornarem verdade semântica autoritativa apenas por terem sido declarados na interação.
- **ADD R-H** - Quando uma correção ou complemento humano se referir ao mesmo achado analítico já existente, a identidade `F-*` deve ser preservada e o finding existente deve ser reconciliado por upsert; mudança de redação, aumento de precisão ou correção do entendimento não deve criar novo finding por si só.
- **ADD R-I** - Incerteza, ressalva ou interpretação concorrente expressa pelo humano deve permanecer explicitamente não resolvida quando material; a interação não pode converter dúvida em certeza nem escolher silenciosamente uma interpretação concorrente.
- **ADD R-J** - Uma declaração humana de que determinado entendimento deve ser tratado como regra autoritativa pode motivar promoção semântica, mas não pode pular o fluxo normal de CHANGE, revisão, aprovação e incorporação em R/D/O. Quando a correção afetar finding já promovido, a relação com o R/D/O vigente deve ser reconciliada antes de qualquer alteração autoritativa.
- **ADD R-K** - `_memory` deve registrar somente a síntese material da correção ou complemento e sua proveniência analítica suficiente, sem armazenar transcrição integral da conversa, chain-of-thought ou dump da interação.

### DECISIONS

- **ADD D-A** - Tratar `_memory/` como contêiner reservado e extensível de memória analítica do namespace, mantendo `FINDINGS.yaml` como único arquivo canônico permitido nesta versão. Novos arquivos dentro de `_memory` exigem mudança normativa futura do protocolo. Atende R-A e R-B.
- **ADD D-B** - Definir a separação de responsabilidades como `R/D/O = memória do conhecimento autoritativo` e `_memory/FINDINGS.yaml = memória da descoberta`, incluindo evidência, risco, interpretação analítica e relação com o conhecimento promovido. Atende R-A e R-C.
- **ADD D-C** - Findings promovidos devem poder registrar referências canônicas às entidades R/D/O resultantes, preservando evidência e risco sem copiar a formulação normativa correspondente. Atende R-C.
- **ADD D-D** - Introduzir reconciliação inversa `R/D/O → findings`: ao modificar, remover ou substituir R/D/O, localizar findings promovidos que referenciem as entidades afetadas e exigir sua reconciliação antes de `RECONCILED`. Atende R-D.
- **ADD D-E** - A reconciliação deve ser seletiva e orientada por referências explícitas ou relações determinísticas disponíveis no índice; ausência de relação com a mudança não autoriza alterar finding existente. Atende R-E.
- **ADD D-F** - Para cada finding afetado, aplicar um resultado explícito entre: preservar `promoted`; atualizar `semantic_refs`; marcar `resolved`; marcar `superseded`; ou retornar a `active` com estado semântico não resolvido quando a nova verdade reabrir a questão analítica. Atende R-F.
- **ADD D-G** - Tratar correção ou complemento humano como nova evidência analítica sobre o finding aplicável. Se a identidade do achado for preservada, reconciliar o mesmo `F-*`; criar novo finding somente quando a questão analítica for materialmente distinta. Atende R-G e R-H.
- **ADD D-H** - Registrar a origem humana da correção de forma concisa na proveniência do finding e ajustar certeza, risco ou `semantic_status` somente na medida sustentada pelo que foi explicitamente esclarecido; não armazenar a conversa como transcrição. Atende R-G, R-I e R-K.
- **ADD D-I** - Quando o humano expressar dúvida, hipótese ou interpretação concorrente, preservar estado não resolvido e produzir `REVIEW` quando a distinção for material para uma decisão ou promoção posterior. Atende R-I.
- **ADD D-J** - Quando o humano declarar intenção normativa, separar retenção analítica de promoção: `_memory` pode ser atualizada imediatamente quando cabível, mas R/D/O somente pode mudar pelo CHANGE aplicável e seus gates. Se o finding já estiver `promoted` e a correção tornar sua relação com `semantic_refs` potencialmente incompatível, a questão deve ser reaberta e reconciliada. Atende R-J.

### OPERATIONS

- **ADD O-A** - Atualizar a seção normativa de memória analítica para declarar explicitamente `_memory` como contêiner do que foi descoberto e `FINDINGS.yaml` como arquivo padrão canônico da versão atual, deixando extensões futuras reservadas a alteração normativa posterior.
- **ADD O-B** - Formalizar no schema de finding promovido um campo de referências semânticas canônicas, suficiente para localizar as entidades R/D/O às quais a descoberta foi promovida sem duplicar seu texto normativo.
- **ADD O-C** - Integrar ao fluxo de `RECONCILIATION` uma verificação determinística de findings promovidos que apontem para R/D/O afetado pelo Semantic Diff do CHANGE.
- **ADD O-D** - Bloquear `RECONCILED` quando houver finding promovido semanticamente afetado cuja relação com o novo R/D/O não tenha sido reconciliada.
- **ADD O-E** - Atualizar o validador estrutural e a skill de memória para aceitar e validar as referências semânticas de findings promovidos e para preservar findings não relacionados.
- **ADD O-F** - Adicionar testes cobrindo: finding promovido que permanece válido após MODIFY; referência que precisa ser atualizada após REMOVE + ADD; finding que volta a `active`; finding resolvido ou superseded; bloqueio de reconciliação quando finding afetado permanece stale; e não alteração de finding não relacionado.
- **ADD O-G** - Não introduzir nesta CHANGE arquivos adicionais dentro de `_memory`; a implementação deve apenas tornar explícita a extensibilidade futura e manter `FINDINGS.yaml` como padrão único atual.
- **ADD O-H** - Atualizar o fluxo operacional da memória para que uma correção ou complemento humano procure primeiro um finding semanticamente equivalente e faça upsert do mesmo `F-*` quando a identidade for preservada, criando novo `F-*` somente para achado realmente distinto.
- **ADD O-I** - Ao registrar correção humana, persistir somente a síntese material, a proveniência de que o esclarecimento foi fornecido pelo humano e os ajustes de certeza, risco ou estado efetivamente sustentados pela interação; não persistir transcrição integral nem raciocínio interno.
- **ADD O-J** - Quando a formulação humana permanecer incerta, conflitante ou condicionada, manter o finding como não resolvido e impedir sua promoção silenciosa para verdade autoritativa.
- **ADD O-K** - Quando houver intenção explícita de tornar a correção regra autoritativa, encaminhar a alteração pelo CHANGE aplicável; em `DRAFT`, limitar a escrita definitiva a `_memory/FINDINGS.yaml` e à própria CHANGE conforme permitido, sem editar R/D/O antes da aprovação e autorização correspondentes.
- **ADD O-L** - Quando uma correção humana atingir finding `promoted`, verificar `semantic_refs`; se a correção puder tornar o R/D/O vigente incompatível com a descoberta atual, reabrir a questão analítica e exigir reconciliação antes de qualquer nova promoção ou conclusão que dependa dessa relação.
- **ADD O-M** - Adicionar testes cobrindo: correção humana atualiza finding equivalente; preservação do `F-*`; registro de proveniência; complemento não autoritativo não modifica R/D/O; declaração normativa não contorna CHANGE; dúvida permanece não resolvida/`REVIEW`; correção contraditória não sobrescreve silenciosamente certeza anterior; conversa não é armazenada como dump; correção de finding promovido detecta necessidade de reconciliação; e findings não relacionados permanecem intactos.
