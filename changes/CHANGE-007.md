change: CHANGE-007
status: RECONCILED
base_commit: 55434c50f6f7855bba6e50972a70ed1b358e69d7
approved_semantic_commit: 278a2887a7c7c2038c25f9b8d085566977a0ff35
approval_scope:
  - changes/CHANGE-007.md
reason: null

# CHANGE-007

## Semantic Diff

### REQUIREMENTS

- **ADD** - O Semantic Repository deve poder validar de forma deterministica a estrutura documental e os caminhos de CHANGE antes da interpretacao semantica.

### DECISIONS

- **ADD** - Disponibilizar `scripts/validate_structure.py` como validador somente leitura, sem dependencia de IA e sem correcao automatica.
- **ADD** - Separar a raiz validada (`--root`) da fonte normativa (`--spec`), permitindo que o core e o repositorio de dominio estejam em pastas ou repositorios diferentes.
- **ADD** - Produzir resultado legivel por humanos e JSON, com diagnostico por regra, caminho e linha quando aplicavel.

### OPERATIONS

- **ADD** - Executar o validador contra a raiz do Semantic Repository antes de interpretar ou reorganizar seus documentos.
- **ADD** - Validar somente regras estruturais deterministicas de nomes, documentos R/D/O, IDs correntes, caminhos de CHANGE e contrato minimo de CHANGE.
- **ADD** - Manter fora do validador estrutural a interpretacao semantica, a reconciliacao, os gates de implementacao e merge e a resolucao de materializacoes externas.
