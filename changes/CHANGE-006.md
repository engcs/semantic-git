change: CHANGE-006
status: IN_PROGRESS
base_commit: 871dbab5edf3674ab76b734c0ef28a6edcea303c
approved_semantic_commit: 11dbd56345aedc3ef3bb6a96e07f055ebd4482c7
approval_scope:
  - changes/CHANGE-006.md
reason: null

# CHANGE-006

## Semantic Diff

### REQUIREMENTS

- **MODIFY** - A unicidade de IDs permanentes `R-`, `D-` e `O-` deve ser determinada pela identidade canônica `<namespace>:<ID local>`, com unicidade do ID curto exigida somente dentro do namespace controlador e do mesmo tipo.
- **MODIFY** - O mesmo ID curto `R-`, `D-` ou `O-` pode existir em namespaces distintos, inclusive entre ancestral e descendente e entre namespaces irmãos, sem representar colisão de identidade.
- **PRESERVE** - Dentro do mesmo namespace e do mesmo tipo, IDs oficiais permanecem estáveis, monotônicos, não reutilizáveis após remoção e devem ser alocados de forma exclusiva e atômica.
- **PRESERVE** - Referências persistidas que atravessem namespaces devem usar a identidade canônica completa; referências curtas locais continuam permitidas quando inequivocamente resolvíveis.
- **PRESERVE** - As regras de identidade e alocação de `CHANGE-ID` permanecem locais ao namespace e não sofrem alteração.

### DECISIONS

- **MODIFY** - Remover a reserva artificial de números R/D/O ao longo da cadeia ancestral: a alocação deve consultar somente o namespace de destino/controlador para colisão do ID curto, sem consumir números usados por ancestrais, descendentes ou irmãos.
- **MODIFY** - A promoção de aliases locais R/D/O deve verificar colisão somente no namespace semântico de destino e no mesmo tipo.
- **MODIFY** - Colisão estrutural de R/D/O existe quando a mesma identidade canônica é duplicada; reutilização do mesmo ID curto em outro namespace não produz `FAIL`.
- **PRESERVE** - Herança conceitual não copia entidade ancestral. Uma especialização ou complemento local é entidade própria, mesmo quando utiliza o mesmo ID curto de uma entidade ancestral.
- **PRESERVE** - Não renumerar namespaces descendentes apenas para evitar igualdade numérica com ancestrais.

### OPERATIONS

- **MODIFY** - Validadores determinísticos devem rejeitar duplicidade R/D/O no mesmo namespace e tipo, mas aceitar o mesmo ID curto em pai/filho e entre irmãos.
- **MODIFY** - Testes de promoção/alocação devem comprovar que colisões são avaliadas no namespace de destino e que alocação concorrente continua exclusiva e atômica localmente.
- **MODIFY** - Testes referenciais devem comprovar que referência entre namespaces exige identidade canônica completa e que referência curta local permanece válida quando inequívoca.
- **PRESERVE** - Testes de `CHANGE-ID` devem continuar validando as regras atuais sem alteração.

## Acceptance Criteria

- `domain:R-001` e `domain/child:R-001` são identidades válidas e distintas.
- `domain/child:D-001 -> domain:R-001` é referência cruzada válida pela forma canônica completa.
- Duplicidade do mesmo `R-`, `D-` ou `O-` dentro do mesmo namespace e tipo produz `FAIL`.
- Mesmo ID curto R/D/O em namespaces irmãos é válido.
- Nenhuma regra normativa restante reserva IDs R/D/O usados por ancestrais.
- Um namespace descendente pode iniciar suas próprias sequências R/D/O em `R-001`, `D-001` e `O-001` sem renumeração motivada apenas pela ancestralidade.
