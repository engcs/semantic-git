change: CHANGE-016
status: MERGED
base_commit: a9afd06f03318635e9cc36d87d8789947d32336b
depends_on:
  - root:CHANGE-014
reason: null

# CHANGE-016

## Semantic Diff

### REQUIREMENTS

- **ADD R-A** - A reconstrução semântica de uma implementação existente deve recuperar o menor contrato de negócio completo capaz de reproduzir seu comportamento sem depender da forma física atual.
- **ADD R-B** - A reconstrução deve distinguir versão semântica de cronologia física e seguir todas as dependências necessárias para fechar o comportamento da versão alvo, sem incorporar regras exclusivas de versões semanticamente posteriores.
- **ADD R-C** - A reconstrução deve traduzir comportamento físico determinístico em significado de domínio quando a interpretação for inequívoca, usando `REVIEW` somente após esgotar as evidências relevantes e restar ambiguidade material.
- **ADD R-D** - A economia da reconstrução deve remover detalhe físico e redundância sem remover conhecimento de negócio necessário à compreensão e à reimplementação fiel do comportamento.

### DECISIONS

- **ADD D-A** - Criar uma skill especializada `semantic-reconstruction`, derivada de `SEMANTIC_GIT.md`, para engenharia reversa semântica de implementações existentes; a `semantic-extraction` permanece como skill genérica. Atende R-A, R-B, R-C e R-D.
- **ADD D-B** - Definir `behavioral closure` como o conjunto de dependências físicas necessário para reconstruir completamente o comportamento semântico da versão alvo. Atende R-A e R-B.
- **ADD D-C** - Permitir síntese semântica determinística de flags, estados, lookups e condições distribuídas quando, após investigação das dependências, não restar interpretação material concorrente. Atende R-C.
- **ADD D-D** - Aplicar dois testes complementares: o contrato deve sobreviver à reimplementação física e, ao mesmo tempo, permitir reconstruir comportamento equivalente sem inventar regras de negócio. Atende R-A e R-D.
- **ADD D-E** - Tratar `REVIEW` como último recurso semântico: conhecimento distribuído, indireto ou codificado não é ambíguo por si só; somente ambiguidade residual após investigação suficiente deve permanecer pendente. Atende R-C.
- **ADD D-F** - Fazer a subtração de herança semanticamente: não redefinir regras ancestrais, mas permitir que Operations registrem o ponto de aplicação de mecanismos herdados quando isso for necessário para reconstruir o fluxo local. Atende R-D.

### OPERATIONS

- **ADD O-A** - Disponibilizar a skill em `.opencode/skills/semantic-reconstruction/SKILL.md`, mantendo `SEMANTIC_GIT.md` como única autoridade normativa.
- **ADD O-B** - Orientar a skill a identificar a versão semântica alvo independentemente do primeiro commit ou primeira aparição física e a percorrer dependências upstream, downstream e compartilhadas até atingir o `behavioral closure`.
- **ADD O-C** - Antes de escrever R/D/O, exigir a reconstrução explícita do propósito, fato elementar, população, medidas, regras de contribuição, temporalidade, validade, recortes, agregação, fórmula e edge cases quando aplicáveis ao domínio investigado.
- **ADD O-D** - Antes de emitir `REVIEW`, exigir investigação das dependências, resolução de aliases, flags, estados, lookups e condições distribuídas, usando `REVIEW` somente quando a evidência relevante estiver esgotada.
- **ADD O-E** - Validar a skill por cenários independentes de reconstrução semântica, comparando os resultados gerados com referências somente após a reconstrução ter sido concluída.
- **ADD O-F** - Manter referências, benchmarks, respostas esperadas e critérios específicos de um domínio fora do contexto fornecido ao agente reconstrutor, para que a validação meça capacidade de reconstrução e não reprodução de um gabarito.
- **ADD O-G** - Registrar na CHANGE apenas evidências genéricas de que o método foi validado, sem persistir respostas esperadas, listas de conceitos-alvo ou qualquer conteúdo que possa contaminar testes cegos futuros.

## Validation Evidence

- A skill `semantic-reconstruction` permanece genérica e independente de qualquer domínio usado durante seu desenvolvimento.
- A implementação contém `behavioral closure`, separação entre versão semântica e cronologia Git, síntese semântica determinística, esgotamento de evidência antes de `REVIEW`, subtração semântica de herança e testes complementares de reconstrução e reimplementação.
- A validação da skill separa geração e avaliação: referências ou respostas esperadas não são disponibilizadas ao agente durante a reconstrução.
- Benchmarks específicos podem ser usados externamente para avaliar a qualidade após a geração, mas seus conteúdos esperados não fazem parte da skill nem desta CHANGE.
- Nenhuma regra de negócio específica de um domínio de teste é necessária para interpretar ou executar a skill.

### Reconciliation Summary

- O Semantic Diff materializa uma skill de reconstrução semântica de propósito geral.
- A skill permanece aplicável a implementações e domínios distintos sem depender de um caso de validação específico.
- A documentação desta CHANGE não contém gabarito, lista de conceitos esperados ou referência semântica específica de um benchmark.

### Merge Evidence

- A skill foi incorporada à `main` e a CHANGE foi arquivada após a incorporação.
