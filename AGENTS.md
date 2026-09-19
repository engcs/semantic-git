# Agent Instructions

## Authority

`SEMANTIC_GIT.md` é a fonte normativa deste repositório. Este arquivo orienta a
operação de agentes, mas não cria, substitui ou modifica regras normativas.

Em caso de divergência, prevalece `SEMANTIC_GIT.md`.

## Mandatory Execution Protocol

Toda tarefa deve aplicar o protocolo operacional da seção 24.4 de
`SEMANTIC_GIT.md` antes de qualquer escrita governada.

A ordem mínima é:

```text
intenção
→ namespace e AS-IS
→ CHANGE e estado
→ autorização aplicável
→ preflight objetivo
→ ações permitidas
→ execução limitada
→ autoauditoria
→ evidências
→ próximo gate
```

Não pule etapas porque a solicitação parece simples. Uma etapa pode ser marcada
como não aplicável quando houver evidência suficiente para isso.

Condição obrigatória que não puder ser verificada não deve ser presumida como
válida. Use `REVIEW`, `FAIL`, `IMPLEMENTATION_BLOCKED`, `MERGE_BLOCKED`,
`RELEASE_BLOCKED` ou `PUBLICATION_BLOCKED`, conforme `SEMANTIC_GIT.md`.

Antes de declarar `RECONCILED`, `READY`, `PASS` ou outro resultado de sucesso,
apresente as evidências mínimas previstas na seção 24.4. O status escrito no
arquivo nunca substitui a verificação das condições que o sustentam.

## Human CHANGE Summary

Ao criar um CHANGE ou apresentá-lo pela primeira vez ao humano, forneça antes
dos detalhes extensos um resumo sintético em linguagem natural que diga o que a
mudança pretende fazer e seu efeito principal.

Prefira um ou dois períodos corridos. Não transforme o resumo em lista do
Semantic Diff nem repita item a item Requirements, Decisions ou Operations.
Use bullets somente quando eles realmente tornarem a compreensão mais clara.

Esse resumo é uma saída de interação humano–IA. Ele não cria campo canônico no
CHANGE, não substitui o Semantic Diff e não deve ser tratado como nova fonte de
verdade.

## Analytical Memory

`_memory/FINDINGS.yaml`, quando existir em um Semantic Namespace, contém memória
analítica versionada e não normativa. Ela preserva somente achados materiais que
seriam caros ou perigosos de redescobrir, como exceções físicas, riscos de
reimplementação, lacunas de evidência e significados ainda não resolvidos.

Regras operacionais:

- `_memory` não é R/D/O, não cria verdade semântica e não substitui evidência original;
- mantenha separação de estado entre R/D/O e `_memory`: um finding ativo não deve duplicar conhecimento já adequadamente representado no R/D/O vigente;
- após promoção, a regra autoritativa deve viver somente em R/D/O; o finding pode permanecer como `promoted` apenas para preservar proveniência, evidência histórica, risco anterior e `semantic_refs`, sem funcionar como segunda cópia normativa da regra;
- não carregue `_memory` no bootstrap normal apenas porque o arquivo existe;
- consulte memória sob demanda em reconstrução, reimplementação, revisão conceitual, debug, análise de risco, investigação de `REVIEW` ou origem de uma regra;
- quando o humano perguntar pelos riscos conhecidos de um domínio ou namespace, consulte os findings relevantes e apresente os riscos analíticos conhecidos, suas consequências, evidências e estados; não transforme isso em um inventário genérico de riscos de negócio sem evidência;
- ausência de findings de risco não prova ausência de risco; diga apenas que não há riscos analíticos registrados ou recuperados no escopo consultado;
- use a skill `semantic-memory` para criar, ler, reconciliar ou atualizar findings;
- faça upsert por identidade estável `F-*`; não use append cego nem substituição cega;
- não remova finding existente apenas porque a execução atual não o reencontrou;
- criação ou upsert de `_memory/FINDINGS.yaml` é escrita analítica permitida durante investigação em `DRAFT` quando limitada à memória não normativa do namespace aplicável;
- a exceção de escrita em `DRAFT` não autoriza editar R/D/O, `SEMANTIC_GIT.md`, materializações físicas ou qualquer outro arquivo de implementação;
- a atualização de memória, por si só, não exige CHANGE semântico; promoção de finding ou mudança de significado continua sujeita ao fluxo normal de CHANGE e aprovação;
- um finding só pode virar R/D/O por CHANGE, revisão e aprovação normal do Semantic Git;
- `_memory` não entra em publicação canônica por padrão.

As skills `semantic-extraction`, `semantic-reconstruction` e
`semantic-conceptual-review` devem conhecer essa capacidade transversal e
aplicá-la somente quando um achado satisfizer os critérios de retenção de
`semantic-memory`.

## Mathematical Review

Use `semantic-mathematical-review` quando a tarefa pedir gaps matemáticos,
indeterminações, inconsistências quantitativas, casos de fronteira, divisão por
zero, sobreposição/lacuna de regras por casos, ordem de agregação, precisão ou
incompatibilidade dimensional. Também use a skill quando uma reconstrução ou
revisão conceitual encontrar fórmula, limite, função ou agregação material cujo
comportamento total e único ainda não esteja demonstrado.

A skill matemática é transversal e analítica. Ela deve separar sempre:

```text
comportamento matemático
≠ comportamento físico da engine
≠ regra semântica governada
```

Regras operacionais:

- identifique o domínio admissível antes de concluir que uma expressão é total ou inválida;
- prefira prova determinística, verificação simbólica, teste de fronteira ou contraexemplo concreto quando possível;
- um único witness válido pode demonstrar que uma regra não é total, única ou equivalente;
- não transforme `NULL`, erro, infinito, overflow, arredondamento ou fallback de uma engine em regra de negócio automaticamente;
- quando R/D/O já definir de forma única um caso matematicamente especial, comportamento físico diferente é divergência da materialização, não nova indeterminação semântica;
- quando mais de uma convenção semanticamente plausível puder fechar o gap, mantenha `REVIEW` ou finding analítico; não invente a resolução;
- execute a skill sob demanda, não como etapa obrigatória de todo pipeline semântico;
- não crie `_memory` porque a skill foi executada; somente findings matemáticos materiais e caros/perigosos de redescobrir podem ser preservados via `semantic-memory`;
- findings matemáticos continuam sendo findings normais em `_memory/FINDINGS.yaml`; não crie `MATHEMATICS.yaml` separado para esse fim;
- quando útil para leitura por máquina, um finding matemático pode incluir bloco opcional `mathematics:` com expressão, condição de domínio, witness/prova, resultado semântico esperado, comportamento observado e classificação;
- use categorias de finding que deixem sua natureza clara, como `mathematical_contradiction`, `mathematical_indeterminacy`, `mathematical_boundary_gap`, `mathematical_overlap`, `mathematical_aggregation_order`, `mathematical_precision` ou `mathematical_dimension`;
- se a regra autoritativa já estiver em R/D/O, o finding não deve duplicá-la como segunda fonte de verdade; registre apenas a inconsistência, evidência, risco e proveniência necessários.

Quando o humano perguntar por "gaps matemáticos", "inconsistências matemáticas" ou
"situações de indeterminação", a IA deve acionar essa skill explicitamente e
apresentar, para cada caso material, a regra afetada, domínio/condição, prova ou
contraexemplo, consequência, classificação e situação semântica.

## Context Loading

Ao iniciar uma tarefa:

1. identifique o escopo conceitual da solicitação;
2. consulte primeiro as seções 24.4 e 13.8 de `SEMANTIC_GIT.md` quando houver possibilidade de escrita, transição ou autorização;
3. consulte em `SEMANTIC_GIT.md` somente as demais regras necessárias;
4. consulte `_foundations/transformations/IES-RDO-TRANSFORMATION.md` quando a tarefa envolver IES e RDO;
5. consulte `_applications/mop/_foundations/` quando a tarefa envolver as premissas semânticas dos indicadores MOP;
6. consulte `_applications/mop/` quando a tarefa envolver a aplicação MOP;
7. siga exclusivamente o padrão documental canônico da seção 23.3 de `SEMANTIC_GIT.md`;
8. consulte `_memory/FINDINGS.yaml` do namespace somente quando a natureza da tarefa tornar a memória analítica materialmente relevante;
9. expanda o contexto apenas quando dependências, conflitos, findings ou evidências exigirem.

## Preflight Before Writing

Antes de editar qualquer arquivo fora de uma CHANGE em elaboração, determine e
verifique, conforme aplicável:

- Semantic Namespace controlador;
- identidade canônica da CHANGE;
- branch corrente e branch esperada;
- estado efetivo da CHANGE;
- `base_commit`;
- `approved_semantic_commit` e `approval_scope` quando exigidos;
- autorização humana correspondente à ação pretendida;
- escopo de escrita permitido;
- drift material conhecido;
- dependências ou conflitos que possam bloquear a ação.

A única exceção pré-aprovação é a manutenção de `_memory/FINDINGS.yaml` durante
investigação em `DRAFT`, quando a escrita satisfizer integralmente os critérios
da memória analítica e não materializar significado aprovado nem implementação.

Verifique fatos decidíveis por Git, filesystem, identidade, caminho, metadados ou
referência antes de interpretação semântica. Não substitua ausência de evidência
por inferência.

## Semantic Work

- diferencie AS-IS, CHANGE, memória analítica e materialização física;
- trate Requirements, Decisions e Operations como dimensões distintas;
- não invente intenção, justificativa, identidade ou decisão humana;
- preserve identidade, referências e histórico;
- governe alterações semânticas materiais por CHANGE;
- valide a coerência entre significado, documentação e materialização;
- retenha em `_memory` somente achados não normativos que sejam materialmente caros ou perigosos de esquecer;
- evite duplicação de significado entre R/D/O e findings ativos; depois de promoção, mantenha na memória somente a proveniência analítica necessária;
- use `_memory` como mapa dos riscos analíticos conhecidos quando a tarefa pedir fragilidades, exceções, lacunas ou riscos conhecidos do namespace;
- use `semantic-mathematical-review` quando fórmulas ou regras quantitativas materiais precisarem de prova de totalidade, unicidade, fronteira, agregação, precisão ou dimensão;
- nunca use `_memory` para contornar governança semântica;
- prefira validações determinísticas quando a regra puder ser verificada por estrutura, Git, matemática ou referência;
- sinalize ambiguidades materiais para revisão humana;
- execute somente ações compatíveis com o estado, a autorização e o escopo confirmados no preflight.

## Self-Audit Before Completion

Antes de concluir uma tarefa governada, confronte o que foi executado com o que
era permitido e declarado. Verifique, conforme aplicável:

- Semantic Diff aprovado versus resultado produzido;
- Git Diff versus transformação declarada;
- Requirements, Decisions e Operations afetados;
- Requirements ancestrais aplicáveis;
- integridade de referências e aliases;
- escopo aprovado versus arquivos efetivamente alterados;
- drift da `main` ou do contrato aprovado;
- dependências e CHANGEs concorrentes relevantes;
- integridade de `_memory/FINDINGS.yaml` quando a tarefa o tiver criado ou alterado;
- ausência de finding ativo que simplesmente replique conhecimento já autoritativo em R/D/O;
- ausência de promoção implícita de finding para R/D/O;
- para revisão matemática, distinção explícita entre gap semântico, matemática pura e divergência de materialização;
- presença de `FAIL` ou `REVIEW` impeditivo.

Se uma verificação necessária não puder ser concluída, não declare sucesso.

## Evidence Report

Ao concluir um gate ou tarefa governada, produza um resumo de evidências contendo,
quando aplicável:

```text
result:
change:
branch:
state:
base_commit:
approved_semantic_commit:
approval_scope:
checked:
  - <fato verificado + fonte da evidência>
pending:
  - <condição não resolvida>
next_gate:
```

Para pre-merge, inclua também `main_head`, `candidate_head` e o snapshot final.
Campos não aplicáveis podem ser omitidos. Campos obrigatórios não verificados não
podem ser preenchidos por suposição.

## Repository Scope

Quando existir, `README.md` contém somente orientação essencial. A aplicação MOP
é um contexto de uso do Semantic Git, não uma substituição da especificação.
Conhecimento específico de outras aplicações deve permanecer em seus namespaces
ou repositórios próprios.

`_memory/` é auxiliar e local ao namespace. Não cria subdomínio, não participa de
herança automática e não deve ser interpretado como uma quarta dimensão do
AS-IS.

## Publication Operation

Quando a solicitação envolver publicação:

1. determine explicitamente o diretório do namespace solicitado;
2. não inclua namespaces descendentes automaticamente;
3. não inclua `_memory/` na publicação canônica por padrão;
4. execute `_scripts/build_publication.py build` com `--root` e `--spec`;
5. use `--pdf` quando a publicação PDF for solicitada;
6. confirme o resultado com `build_publication.py status`;
7. trate `PUBLICATION.*` como artefatos derivados, nunca como fonte semântica;
8. não interprete publicação como autorização de aprovação, merge, tag ou push.

Exemplo genérico:

```powershell
python _scripts\build_publication.py build --root "path\to\namespace" --spec "path\to\SEMANTIC_GIT.md" --pdf --json
python _scripts\build_publication.py status --root "path\to\namespace" --spec "path\to\SEMANTIC_GIT.md" --json
```
