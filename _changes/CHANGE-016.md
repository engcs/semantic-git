change: CHANGE-016
status: IN_PROGRESS
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
