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

## Context Loading

Ao iniciar uma tarefa:

1. identifique o escopo conceitual da solicitação;
2. consulte primeiro as seções 24.4 e 13.8 de `SEMANTIC_GIT.md` quando houver possibilidade de escrita, transição ou autorização;
3. consulte em `SEMANTIC_GIT.md` somente as demais regras necessárias;
4. consulte `_foundations/transformations/IES-RDO-TRANSFORMATION.md` quando a tarefa envolver IES e RDO;
5. consulte `_applications/mop/_foundations/` quando a tarefa envolver as premissas semânticas dos indicadores MOP;
6. consulte `_applications/mop/` quando a tarefa envolver a aplicação MOP;
7. siga exclusivamente o padrão documental canônico da seção 23.3 de `SEMANTIC_GIT.md`;
8. expanda o contexto apenas quando dependências ou conflitos exigirem.

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

Verifique fatos decidíveis por Git, filesystem, identidade, caminho, metadados ou
referência antes de interpretação semântica. Não substitua ausência de evidência
por inferência.

## Semantic Work

- diferencie AS-IS, CHANGE e materialização física;
- trate Requirements, Decisions e Operations como dimensões distintas;
- não invente intenção, justificativa, identidade ou decisão humana;
- preserve identidade, referências e histórico;
- governe alterações semânticas materiais por CHANGE;
- valide a coerência entre significado, documentação e materialização;
- prefira validações determinísticas quando a regra puder ser verificada por estrutura, Git ou referência;
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

## Publication Operation

Quando a solicitação envolver publicação:

1. determine explicitamente o diretório do namespace solicitado;
2. não inclua namespaces descendentes automaticamente;
3. execute `_scripts/build_publication.py build` com `--root` e `--spec`;
4. use `--pdf` quando a publicação PDF for solicitada;
5. confirme o resultado com `build_publication.py status`;
6. trate `PUBLICATION.*` como artefatos derivados, nunca como fonte semântica;
7. não interprete publicação como autorização de aprovação, merge, tag ou push.

Exemplo genérico:

```powershell
python _scripts\build_publication.py build --root "path\to\namespace" --spec "path\to\SEMANTIC_GIT.md" --pdf --json
python _scripts\build_publication.py status --root "path\to\namespace" --spec "path\to\SEMANTIC_GIT.md" --json
```
