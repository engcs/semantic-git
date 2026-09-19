change: CHANGE-019
status: MERGED
base_commit: 7735ce340df437329054dda4181559ea3e6cc3eb
approved_semantic_commit: 4ca35f8dceb9ec379bfe7a7463f51a0bfd79d05b
approval_scope:
  - _changes/CHANGE-019.md
depends_on:
  - root:CHANGE-017
reason: null

# CHANGE-019

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - Um Semantic Namespace deve poder manter memória analítica versionada para preservar achados materialmente relevantes cuja perda aumentaria risco ou custo de redescoberta, mas que não devam compor o R/D/O vigente.
- **ADD R-B** - A memória analítica deve permanecer explicitamente não normativa: não cria verdade semântica, não substitui evidência original, não participa de herança semântica e não pode promover conteúdo para R/D/O fora do fluxo normal de CHANGE e aprovação humana.
- **ADD R-C** - A memória deve ser local ao namespace e fisicamente organizada em `_memory/`, ao lado de diretórios auxiliares como `_changes/` e `_publications/`, sem criar novo Semantic Namespace.
- **ADD R-D** - Achados de memória devem ser estruturados, rastreáveis e atualizáveis por identidade estável, preservando ao menos o que foi observado, evidência/proveniência, risco ou consequência material, estado atual e situação semântica.
- **ADD R-E** - Reexecuções das skills não devem produzir append cego nem substituição cega da memória existente; achados semanticamente equivalentes devem ser reconciliados por upsert, e informação existente não deve desaparecer apenas porque uma execução posterior não a reencontrou.
- **ADD R-F** - `_memory` deve seguir progressive disclosure: não é carregado no bootstrap normal do namespace nem incluído em publicação por padrão, mas deve ser consultável quando a tarefa envolver reconstrução, reimplementação, revisão conceitual, risco, debug, investigação de `REVIEW` ou origem de uma regra.
- **ADD R-G** - As skills `semantic-extraction`, `semantic-reconstruction` e `semantic-conceptual-review` devem conhecer a memória analítica e usar uma capacidade transversal `semantic-memory` quando encontrarem ou revisarem achados que atendam aos critérios de retenção.
- **ADD R-H** - A manutenção de `_memory` que preserve apenas achados analíticos não normativos deve poder ocorrer durante investigação autorizada, inclusive enquanto o CHANGE relacionado estiver em `DRAFT`, sem ser tratada como implementação semântica ou alteração do AS-IS; essa permissão não se estende a R/D/O nem às materializações físicas.

### DECISIONS

- **ADD D-A** - Definir `_memory/FINDINGS.yaml` como representação canônica opcional da memória analítica de um namespace. O diretório e o arquivo só devem existir quando houver ao menos um finding material; não criar memória vazia apenas para completar estrutura. Atende R-A, R-C e R-F.
- **ADD D-B** - Definir finding como conhecimento observado ou inferência sustentada que seja material, caro ou arriscado de redescobrir e inadequado ao R/D/O vigente. Exemplos incluem exceções físicas hardcoded, riscos de reimplementação, lacunas de evidência, artefatos históricos e significado ainda não resolvido. Atende R-A e R-B.
- **ADD D-C** - Identificar findings por IDs locais estáveis `F-001`, `F-002`, ... dentro do namespace. O ID identifica o achado analítico, não cria identidade semântica R/D/O nem referência normativa. Atende R-D.
- **ADD D-D** - Manter cada finding como estado atual, usando no mínimo `active`, `resolved`, `superseded` ou `promoted`. O histórico de alterações do finding pertence ao Git; `FINDINGS.yaml` não deve duplicar esse histórico como log append-only. Atende R-D e R-E.
- **ADD D-E** - Exigir em cada finding, no mínimo, `id`, `status`, `category`, `summary`, `evidence`, `risk` e `semantic_status`; permitir proveniência de skill e referências físicas quando disponíveis. A ausência de significado semântico conhecido deve ser representada explicitamente, não preenchida por invenção. Atende R-B e R-D.
- **ADD D-F** - Tratar `semantic-memory` como skill transversal de leitura, classificação, upsert, resolução, supersessão e marcação de promoção de findings. Ela não constitui uma quarta etapa obrigatória do pipeline semântico e não decide sozinha que um finding virou R/D/O. Atende R-G.
- **ADD D-G** - Fazer `semantic-reconstruction` atuar como principal produtora de findings físicos; permitir que `semantic-extraction` registre achados materiais vindos de fontes humanas; permitir que `semantic-conceptual-review` funda duplicatas, reclassifique, resolva ou proponha promoção, sempre preservando a ausência de autoridade normativa da memória. Atende R-G.
- **ADD D-H** - Um finding que passe a representar conhecimento semântico durável deve entrar em CHANGE normal e ser aprovado antes de aparecer em R/D/O; após a promoção, o finding pode permanecer com `status: promoted` e referência ao item semântico resultante para preservar proveniência. Atende R-B e R-D.
- **ADD D-I** - Tratar criação ou upsert de `_memory/FINDINGS.yaml` como escrita analítica permitida em `DRAFT` quando derivada da investigação em curso e limitada à memória não normativa do namespace aplicável. A atualização de memória, por si só, não exige CHANGE semântico; qualquer promoção de finding ou mudança de significado continua sujeita ao fluxo normal de CHANGE e aprovação. Atende R-B, R-G e R-H.

### OPERATIONS

- **ADD O-A** - Alterar `SEMANTIC_GIT.md` para reconhecer `_memory/` como diretório auxiliar reservado local ao namespace, definir `FINDINGS.yaml`, sua não autoridade, política de carregamento sob demanda, relação com publicação e regras estruturais mínimas.
- **ADD O-B** - Criar `.opencode/skills/semantic-memory/SKILL.md` com critérios de retenção, leitura seletiva, deduplicação/upsert, estados, proveniência, risco, resolução e promoção governada.
- **ADD O-C** - Ajustar `semantic-extraction` para aplicar `semantic-memory` quando uma fonte humana contiver achado material que não deva entrar no contrato persistente, evitando transformar a memória em cópia da evidência.
- **ADD O-D** - Ajustar `semantic-reconstruction` para consultar memória relevante no início de investigações compatíveis e registrar/reconciliar exceções físicas, lacunas e riscos materiais que não devam ser comprimidos para R/D/O.
- **ADD O-E** - Ajustar `semantic-conceptual-review` para usar findings como contexto não normativo, confrontá-los com evidência original e atualizar sua classificação quando a revisão resolver, fundir, superseder ou identificar candidato a promoção.
- **ADD O-F** - Atualizar `AGENTS.md` para orientar o uso de `_memory` por progressive disclosure e deixar explícito que memória não é fonte de verdade, não deve ser carregada indiscriminadamente e não substitui o fluxo de CHANGE.
- **ADD O-G** - Adicionar validações determinísticas para aceitar `_memory/FINDINGS.yaml` sem tratá-lo como novo R/D/O, rejeitar memória vazia quando criada apenas estruturalmente, validar unicidade de `F-*` dentro do namespace e impedir que `_memory` seja incluído como AS-IS semântico ou publicação canônica.
- **ADD O-H** - Não criar `_memory/` vazio em namespaces sem findings. Quando um finding real for registrado, criar o diretório local e o `FINDINGS.yaml` correspondente naquele namespace.
- **ADD O-I** - Ajustar `SEMANTIC_GIT.md`, `AGENTS.md` e `semantic-memory` para explicitar a exceção de escrita analítica em `DRAFT`, mantendo proibidas edições de R/D/O e materializações físicas antes da aprovação semântica aplicável.
