change: CHANGE-016
status: RECONCILED
base_commit: a9afd06f03318635e9cc36d87d8789947d32336b
approved_semantic_commit: 12f5cedb04dde108723df784416fd322e6a3fada
approval_scope:
  - _changes/CHANGE-016.md
depends_on:
  - root:CHANGE-014
reason: null

# CHANGE-016

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - A reconstrução semântica de uma implementação existente deve recuperar o menor contrato de negócio completo capaz de reproduzir seu comportamento sem depender da forma física atual.
- **ADD R-B** - A reconstrução deve distinguir versão semântica de cronologia física e seguir todas as dependências necessárias para fechar o comportamento da versão alvo, sem incorporar regras exclusivas de versões semanticamente posteriores.
- **ADD R-C** - A reconstrução deve traduzir comportamento físico determinístico em significado de domínio quando a interpretação for inequívoca, usando `REVIEW` somente após esgotar as evidências relevantes e restar ambiguidade material.
- **ADD R-D** - A economia da extração deve remover detalhe físico e redundância sem remover propósito, população, regras de contribuição, temporalidade, recortes, fórmula, agregação ou edge cases necessários à reconstrução.

### DECISIONS

- **ADD D-A** - Criar uma skill especializada `semantic-reconstruction`, derivada de `SEMANTIC_GIT.md`, para engenharia reversa semântica de implementações existentes; a `semantic-extraction` permanece como skill genérica. Atende R-A, R-B, R-C e R-D.
- **ADD D-B** - Definir `behavioral closure` como o conjunto de dependências físicas necessário para reconstruir propósito, fato elementar, população, medidas, regras de contribuição, tempo, recortes, fórmula, agregação e edge cases da versão semântica alvo. Atende R-A e R-B.
- **ADD D-C** - Permitir síntese semântica determinística de flags, estados, lookups e condições distribuídas quando, após investigação das dependências, não restar interpretação material concorrente. Atende R-C.
- **ADD D-D** - Aplicar dois testes complementares: o contrato deve sobreviver à reimplementação física e, ao mesmo tempo, permitir reconstruir comportamento equivalente sem inventar regras de negócio. Atende R-A e R-D.
- **ADD D-E** - Tratar `REVIEW` como último recurso semântico: conhecimento distribuído, indireto ou codificado não é ambíguo por si só; somente ambiguidade residual após investigação suficiente deve permanecer pendente. Atende R-C.
- **ADD D-F** - Fazer a subtração de herança semanticamente: não redefinir regras ancestrais, mas permitir que Operations registrem o ponto de aplicação de mecanismos herdados quando isso for necessário para reconstruir o fluxo local. Atende R-D.

### OPERATIONS

- **ADD O-A** - Disponibilizar a skill em `.opencode/skills/semantic-reconstruction/SKILL.md`, mantendo `SEMANTIC_GIT.md` como única autoridade normativa.
- **ADD O-B** - Orientar a skill a identificar a versão semântica alvo independentemente do primeiro commit ou primeira aparição física e a percorrer upstream, downstream, componentes compartilhados, lookups, macros, regras temporais e camadas de agregação até atingir o behavioral closure.
- **ADD O-C** - Antes de escrever R/D/O, exigir a reconstrução explícita de propósito, fato elementar, população, medidas, contribuição, tempo, validade, recortes, agregação, fórmula e edge cases relevantes.
- **ADD O-D** - Antes de emitir `REVIEW`, exigir resolução de aliases, flags, estados, lookups, condições distribuídas e aplicabilidade por versão, usando `REVIEW` somente quando a evidência relevante estiver esgotada.
- **ADD O-E** - Validar a skill por reexecução da reconstrução do EXEC_PROG-V1 sobre os anexos de implementação fornecidos, comparando o resultado com a referência humana `EXEC_PROG-V1_SEMANTIC-GIT(1).MD` por natureza semântica, cobertura comportamental, abstração física e reconstrutibilidade, sem exigir identidade textual.
- **ADD O-F** - Considerar a validação aprovada somente se o resultado reconstruído recuperar, sem copiar a referência como fonte, os mesmos núcleos semânticos materiais: propósito de aderência, população organizacional elegível, critérios de Executado e Programado, vigência por estado, visões Geral/Obra/ANS, fórmula e denominador zero, fluxo de temporalização e agregação, expurgo e roll-up organizacional.
- **ADD O-G** - Registrar evidências objetivas da validação no próprio CHANGE antes de declarar reconciliação ou conclusão.


## Validation Evidence

- A implementação foi limitada a `.opencode/skills/semantic-reconstruction/SKILL.md` e a esta CHANGE; `SEMANTIC_GIT.md`, R/D/O e a skill genérica `semantic-extraction` não foram alterados.
- A skill mantém `SEMANTIC_GIT.md` como única autoridade normativa e implementa explicitamente behavioral closure, separação entre versão semântica e cronologia Git, síntese semântica determinística, REVIEW após esgotamento de evidência, subtração semântica de herança e os testes complementares de reconstrução e reimplementação.
- A validação do EXEC_PROG-V1 carregou primeiro o R/D/O ancestral de `mop` e `mop/programacao` e usou os anexos de implementação como fonte do domínio; a referência humana foi usada somente depois da reconstrução, como alvo de comparação.
- A investigação seguiu o behavioral closure da V1 através das camadas de programação, elegibilidade organizacional, apontamento/tempestividade, KPI fato, cálculo final e consolidação, isolando regras V1 de acréscimos semanticamente posteriores.
- A reconstrução independente recuperou 6 Requirements e 6 Decisions da mesma natureza semântica da referência e 11 Operations semanticamente equivalentes, mais comprimidas que as 14 Operations da referência.
- A matriz de cobertura validou 21/21 núcleos materiais exigidos por O-F: propósito de aderência; universo elegível; Executado e tempestividade; Programado por situação; vigência por estado; visões; fórmula; denominador zero; empreiteira ativa; existência de equipe ativa; equipe ativa na competência; apontamento positivo; ausência de data de alteração; programação elementar; dia de referência; competência semanal/mensal; expurgo; agregação mensal direta; soma separada das componentes; acumulado; e roll-up contrato → regional → distribuidora.
- A comparação não exigiu identidade textual: as diferenças remanescentes são principalmente compressão de Operations e formulação. O comportamento aceito para Programado foi recuperado; parte dos rótulos humanos dos códigos físicos depende de mapeamentos não materializados estaticamente no conjunto analisado, sem comprometer a natureza semântica central validada.
- O resultado passa os testes de reimplementação e reconstrução: não depende de SQL/dbt/tabelas/campos para ser compreendido e preserva conhecimento suficiente para reimplementar o comportamento sem redescobrir as regras materiais validadas.
- A `main` permanece exatamente em `a9afd06f03318635e9cc36d87d8789947d32336b`, idêntica ao `base_commit`; não há drift desde a criação da CHANGE.
- A dependência `root:CHANGE-014` está arquivada na `main` com status `MERGED`.
- O Git Diff da branch permanece restrito a `_changes/CHANGE-016.md` e `.opencode/skills/semantic-reconstruction/SKILL.md`; nenhum arquivo fora do escopo aprovado foi modificado.

### Reconciliation Summary

- O Semantic Diff aprovado em `approved_semantic_commit: 12f5cedb04dde108723df784416fd322e6a3fada` está materializado pela nova skill.
- A validação específica do EXEC_PROG-V1 atingiu o critério de proximidade por natureza semântica definido em O-E/O-F, sem usar a referência como fonte de reconstrução.
- Não há drift da `main`, conflito com `root:CHANGE-014` ou alteração de R/D/O/SEMANTIC_GIT.
- Não foi identificado FAIL ou REVIEW impeditivo para a implementação da skill.
