change: CHANGE-010
status: DRAFT
base_commit: 3749b5bbbda46c2f63746f57094ead71fc19ec0d
operation: SEMANTIC_BASELINE_RESET
reason: null

# CHANGE-010

## Semantic Diff

### REQUIREMENTS

- **ADD** - O Semantic Git deve permitir, de forma excepcional, o reset de uma baseline semântica mediante aprovações humanas explícitas.
- **ADD** - O reset deve revisar as referências internas do repositório antes de substituir a baseline vigente.
- **ADD** - O reset deve preservar o histórico Git, mas pode invalidar referências externas à baseline anterior.
- **ADD** - O risco de ruptura em documentos externos, publicados ou impressos deve ser aceito explicitamente antes da execução.

### DECISIONS

- **ADD** - O reset mantém a identidade do namespace e reinicia as sequências locais de Requirements, Decisions e Operations em `001`, sem criar época ou identidade adicional.
- **ADD** - Entidades da baseline anterior permanecem recuperáveis pelo histórico Git, mas não são automaticamente remapeadas, aliasadas ou preservadas como referências válidas na baseline nova.
- **ADD** - Referências internas devem ser tratadas antes do reset; referências externas são consideradas potencialmente não resolvíveis após a substituição da baseline.
- **ADD** - O reset exige duas aprovações independentes: uma para o novo conteúdo e o reinício dos IDs, e outra para a possível perda de referências externas.
- **ADD** - A segunda aprovação deve confirmar claramente que documentos externos, inclusive publicados ou impressos, podem continuar apontando para conceitos que não existem mais na baseline vigente.

### OPERATIONS

- **ADD** - Executar o reset somente por uma CHANGE específica, em branch exclusiva, com captura da baseline anterior e da nova baseline.
- **ADD** - Auditar referências internas em R/D/O, CHANGEs, `approval_scope`, manifests e publicações rastreadas, classificando cada ocorrência como atualizada, removida, histórica ou não resolvida.
- **ADD** - Bloquear a execução enquanto houver referência interna não tratada; não afirmar que referências externas foram localizadas ou preservadas.
- **ADD** - Registrar separadamente a aprovação do novo RDO e a confirmação do risco de ruptura externa, incluindo o texto explícito de aceitação.
- **ADD** - Substituir o R/D/O vigente pelo conteúdo aprovado, reiniciar os IDs locais e preservar o estado anterior somente no histórico Git, sem cópia de compatibilidade automática.
- **ADD** - Executar validação estrutural, revisão semântica e RECONCILIATION antes de concluir o reset.
- **ADD** - Manter o reset como operação excepcional, sem torná-lo uma consequência automática de qualquer alteração de R/D/O.
