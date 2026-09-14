# Semantic Git — Modelo de Evolução do Conhecimento Semântico

**Versão:** 1.5
**Status:** especificação normativa standalone
**Natureza:** modelo autocontido de gestão e evolução de conhecimento semântico
**Compatibilidade conceitual:** modelo autocontido e independente de especificações externas

---

## 0. Regra de leitura e independência normativa

O Semantic Git 1.5 é **autocontido**.

Para compreender e operar corretamente um repositório governado por esta especificação, não é necessário consultar qualquer versão anterior do protocolo, uma skill, um prompt externo ou outra especificação normativa.

```text
SEMANTIC_GIT.md
= fonte normativa completa do protocolo
```

`AGENTS.md`, skills, CLIs, validadores, manifestos, templates e automações podem orientar ou executar o protocolo, mas não substituem nem modificam esta especificação.

Em caso de divergência:

```text
SEMANTIC_GIT.md
> skill / AGENTS.md / automação / template / manifesto derivado
```

Uma skill pode resumir o procedimento operacional e consultar seções deste documento sob demanda, mas não deve criar uma segunda fonte de verdade.

---

## 1. Propósito

O Semantic Git existe para preservar significado persistente sobre sistemas, negócio e operação por longos períodos sem transformar a documentação em uma estrutura complexa demais para humanos e IAs utilizarem com segurança.

Sua prioridade é permitir responder rapidamente:

- o que é considerado verdade hoje;
- o que está sendo alterado;
- qual transformação semântica foi aprovada;
- o que deixou de valer e o que passou a valer;
- como a transformação foi materializada fisicamente;
- por que e como o estado atual evoluiu;
- como reconstruir estados anteriores quando necessário.

O Semantic Git favorece:

- simplicidade;
- previsibilidade;
- rastreabilidade;
- recuperação de contexto;
- baixo custo cognitivo;
- baixo volume documental;
- uso intensivo do Git para fatos físicos e temporais;
- documentação humana somente para significado relevante e difícil de reconstruir;
- automação de regras determinísticas;
- validação humana para decisões materiais de significado;
- carregamento progressivo de contexto pela IA.

A estrutura não deve armazenar tudo.

Ela deve armazenar apenas conhecimento semântico relevante e difícil de reconstruir adequadamente a partir de artefatos ou histórico técnico.

---

## 2. Domínio governado

O objeto governado pelo Semantic Git é **Semantic Knowledge**: significado persistente sobre o que um sistema, negócio ou operação deve ser, por que determinadas escolhas existem e como o estado vigente é operado.

A materialização física desse significado pode existir em:

- código;
- configuração;
- testes;
- scripts;
- modelos;
- infraestrutura;
- aplicações;
- pipelines;
- procedimentos executáveis;
- outros artefatos técnicos.

Essas materializações não constituem automaticamente novas dimensões semânticas.

O Semantic Git distingue:

```text
significado persistente
≠
materialização física
```

O repositório que governa o significado é chamado **Semantic Repository**.

Os escopos conceituais são chamados **Semantic Namespaces**.

A transformação conceitual é representada por **Semantic Delta / Semantic Diff**.

---

## 3. Conceito central: AS-IS e CHANGE

O Semantic Git separa de forma absoluta:

```text
PRESENTE
≠
TRANSFORMAÇÃO
```

### 3.1. AS-IS

AS-IS representa o conhecimento semântico oficialmente aprovado e vigente em determinado escopo.

No Semantic Repository governante, em fluxo Git corresponde à `main` local:

```text
main
```

Uma `main` remota ou de outro clone não substitui a `main` local governante.

O AS-IS contém somente conhecimento que deve ser entendido como verdadeiro agora.

No Semantic Git, o AS-IS permanente é expresso, conforme aplicável, por:

```text
REQUIREMENTS
DECISIONS
OPERATIONS
```

Artefatos físicos que materializam esse conhecimento não se tornam AS-IS semântico por existirem; eles devem permanecer coerentes com o AS-IS semântico governante.

### 3.2. CHANGE

CHANGE representa uma transformação proposta ou em desenvolvimento.

Uma mudança ainda não é verdade.

Ela é uma hipótese de futuro.

Enquanto não for incorporada ao AS-IS:

```text
branch / CHANGE
= TO-BE em desenvolvimento

main
= AS-IS vigente
```

Se a criação inicial de um namespace for realizada sob o Semantic Git, ela deve
ser governada por um único `CHANGE-INIT`. Se for manual ou externa, ocorre fora
do protocolo: não existe `CHANGE-INIT` nem CHANGE de inicialização, e o estado
pode ser reconhecido como AS-IS de origem. A ausência de `CHANGE-INIT` não
representa uma criação governada sem `CHANGE-INIT`, não prova ferramenta ou
autoria e não exige reconstrução.

A partir da existência do namespace, toda alteração semântica material,
inclusive em `REQUIREMENTS`, `DECISIONS` ou `OPERATIONS`, deve ser governada por
um CHANGE.

Alterações puramente físicas, editoriais, de formatação ou refatorações que preservem integralmente o significado não exigem CHANGE semântico.

Um CHANGE não deve ser tratado como verdade vigente antes do merge.

---

## 4. Ergonomia humano–IA

O humano não deve ser obrigado a conhecer ou preencher corretamente toda a estrutura interna do protocolo.

Ele deve poder começar com uma intenção simples.

Cabe à IA e às automações, quando disponíveis:

- localizar o Semantic Namespace aplicável;
- consultar o AS-IS relevante;
- recuperar Requirements ancestrais aplicáveis;
- consultar Decisions relevantes;
- consultar Operations quando houver impacto operacional;
- pesquisar CHANGEs anteriores quando forem relevantes;
- alocar CHANGE-IDs pela sequência local do namespace controlador;
- resolver CHANGEs por identidade canônica em referências, autorizações e gates;
- validar identidade, caminho e branch antes de criar um CHANGE;
- criar ou ajustar a estrutura do CHANGE;
- preencher metadados determinísticos;
- normalizar referências;
- propor e manter o Semantic Diff;
- executar testes de conformidade;
- resolver vínculos semântico-físicos;
- sinalizar ambiguidades materiais;
- solicitar validação humana quando o significado depender de decisão humana.

A complexidade do protocolo pertence principalmente à IA e às automações.

O humano deve concentrar-se principalmente em:

> expressar intenção e validar significado.

A IA pode corrigir estrutura e inferir fatos determinísticos.

A IA não pode inventar significado, motivo desconhecido, identidade humana ausente ou decisão material humana.

---

## 5. Semantic Namespaces

O Semantic Git é recursivo.

Um Semantic Repository pode possuir uma árvore de namespaces:

```text
root
├── domain
│   ├── operation
│   └── cancelamento
└── apuracao
```

Cada namespace pode conter AS-IS semântico e CHANGEs próprios.

Um namespace novo, se criado manualmente ou externamente, surge fora do
protocolo: não existe `CHANGE-INIT` nem CHANGE de inicialização, e seu estado
pode ser reconhecido como AS-IS de origem sem invalidação ou reconstrução
retroativa. Se criado sob o Semantic Git, deve ser governado por um único
`CHANGE-INIT` localizado no namespace alvo, mesmo que ele não possua AS-IS no
`base_commit`; o namespace pai não precisa de CHANGE.

A raiz não possui autoridade especial apenas por ser raiz.

Ela contém somente conhecimento cujo escopo seja realmente global.

### 5.1. Menor escopo suficiente

Um CHANGE deve viver no menor ancestral comum capaz de conter integralmente tudo o que a transformação pretende alterar.

Exemplo:

```text
operation apenas
→ domain/operation:CHANGE-002

operation + cancelamento
→ domain:CHANGE-002

domain + apuracao
→ root:CHANGE-002
```

Se durante a descoberta a mudança revelar alcance maior, o CHANGE deve subir para o menor namespace que passe a conter integralmente a transformação.

Isso representa evolução da compreensão, não erro do processo.

O escopo do CHANGE não obriga as entidades resultantes a permanecerem nesse mesmo nível.

### 5.2. Herança de contexto

Ao trabalhar em um namespace, a IA deve considerar:

```text
contexto local
+
Requirements aplicáveis dos ancestrais
+
Decisions relevantes
+
Operations relevantes quando aplicável
+
dependências laterais relevantes
```

Não deve carregar indiscriminadamente toda a árvore.

A árvore existe para localização, herança e redução de contexto.

Requirements ancestrais aplicáveis são herdados conceitualmente pelo namespace
descendente. Essa herança:

- não copia o texto do ancestral para o descendente;
- não cria uma segunda entidade semântica por si só;
- mantém o texto e a identidade no namespace de origem;
- exige referência canônica quando uma entidade local depender, especializar ou
  restringir o conceito ancestral.

Uma especialização ou complemento local é uma entidade própria e deve possuir
identidade canônica própria no namespace local. O mesmo ID curto do mesmo tipo
pode existir no ancestral e no descendente, pois as identidades canônicas são
distintas. A herança, sozinha, não exige repetição no arquivo filho nem cria
uma entidade local.

### 5.3. Namespace não é filesystem

O namespace responde:

> onde este significado pertence conceitualmente?

Ele não deve ser derivado automaticamente da estrutura física da implementação.

```text
identidade semântica
≠
caminho físico
```

A estrutura física pode espelhar a árvore semântica quando isso melhorar a navegação, mas reorganização puramente física não deve alterar identidade semântica quando significado e escopo conceitual forem preservados.

---

## 6. Dimensões permanentes do AS-IS

O Semantic Git define três dimensões permanentes canônicas:

```text
REQUIREMENTS
     ↓
DECISIONS
     ↓
OPERATIONS
```

Elas representam sempre o estado semântico vigente do namespace em que vivem.

Nem todo namespace precisa possuir todas as dimensões.

Arquivos vazios não devem ser criados apenas para completar estrutura.

Nenhuma dimensão deve existir apenas para preencher taxonomia.

### 6.1. REQUIREMENTS

REQUIREMENTS responde:

> o que deve ser verdade?

Pode conter:

- objetivos;
- requisitos funcionais;
- requisitos não funcionais;
- regras de negócio;
- restrições;
- contratos;
- invariantes;
- critérios de aceitação;
- comportamentos esperados.

É a dimensão de maior autoridade semântica permanente.

REQUIREMENTS não deve funcionar como histórico, TODO, justificativa arquitetural ou descrição operacional.

### 6.2. DECISIONS

DECISIONS responde:

> como e por que escolhemos satisfazer os Requirements?

Pode registrar:

- escolha arquitetural;
- escolha de tecnologia;
- escolha de fonte;
- algoritmo;
- estratégia de versionamento;
- compatibilidade;
- trade-offs;
- alternativas relevantes descartadas;
- consequências duradouras.

Registrar somente decisões cuja ausência provavelmente faria alguém perguntar no futuro:

> por que fizeram desta forma?

### 6.3. OPERATIONS

OPERATIONS responde:

> como o estado vigente é utilizado, executado, mantido, validado ou recuperado?

Pode conter:

- execução;
- publicação;
- reprocessamento;
- recuperação;
- validação;
- monitoramento;
- dependências operacionais;
- janelas;
- rotinas;
- procedimentos duradouros.

OPERATIONS não é TODO.

### 6.4. Hierarquia semântica

É obrigatório:

```text
REQUIREMENTS
     ↓
DECISIONS
     ↓
OPERATIONS
```

Portanto:

- Decisions não podem contradizer Requirements;
- Operations não podem contradizer Requirements ou Decisions;
- conhecimento local deve respeitar Requirements ancestrais aplicáveis;
- materializações físicas devem permanecer coerentes com o conjunto vigente.

Divergências materiais devem ser sinalizadas, não resolvidas arbitrariamente pela IA.

---

## 7. Identidade semântica, IDs e referências

IDs identificam entidades semânticas.

Eles não identificam versões de texto.

Os prefixos oficiais são:

```text
R-
D-
O-
CHANGE-
```

A identidade canônica é:

```text
<namespace>:<ID local>
```

Exemplos:

```text
root:R-001
domain:R-017
domain/operation:D-003
domain/operation:O-005
domain/operation:CHANGE-014
```

IDs curtos são locais ao namespace. A identidade de qualquer entidade é a
combinação do namespace canônico com o ID local. O mesmo ID curto pode existir
em namespaces distintos sem representar a mesma entidade:

```text
domain:R-001
≠
domain/child:R-001

root:CHANGE-004
≠
domain:CHANGE-004
```

Identidades canônicas são hierárquicas e inequívocas.

### 7.1. Referências

São permitidas:

- referências absolutas;
- referências relativas resolvíveis;
- referências curtas quando o contexto for inequivocamente suficiente.

Referências ambíguas não podem ser resolvidas por adivinhação.

Toda referência deve ser normalizável para uma identidade canônica.

Quando a referência atravessar a fronteira de um namespace, a forma persistida
deve ser a identidade canônica completa (`namespace:ID`). Referências curtas
podem ser usadas somente para entidades do namespace local quando forem
inequivocamente resolvíveis. Uma referência curta não deve procurar entidade em
namespace ancestral, descendente ou irmão. Referências persistidas que
identifiquem CHANGE devem usar a identidade canônica quando a forma curta puder
designar mais de um CHANGE.
Dependências e entradas de gates devem sempre usar a identidade canônica.
Autorizações seguem as regras mais estritas da seção 13.8.

Exemplo de referência absoluta:

```text
domain:D-004 → domain:R-017
domain/child:D-001 → domain:R-001
```

### 7.2. IDs oficiais

IDs oficiais:

- são monotônicos por tipo dentro do namespace que os controla;
- não precisam formar sequência contínua;
- não devem ser renumerados por conveniência;
- não devem ser reutilizados dentro do namespace após remoção;
- devem permanecer estáveis enquanto identidade e escopo conceitual forem preservados;
- devem ser atribuídos de forma exclusiva e atômica.

Para entidades semânticas permanentes `R-`, `D-` e `O-`, a unicidade é
verificada por tipo dentro do namespace controlador. Um ID curto do mesmo tipo
não pode ser duplicado nem reutilizado, inclusive após remoção, dentro desse
mesmo namespace.

O mesmo ID curto do mesmo tipo pode existir em namespaces distintos, inclusive
entre ancestral e descendente ou entre namespaces irmãos, porque suas
identidades canônicas são distintas. A alocação R/D/O consulta o AS-IS, o
histórico e alocações concorrentes do próprio namespace controlador; não reserva
nem consome números em ancestrais, descendentes ou irmãos.

Para `CHANGE-`, a sequência é local e independente em cada Semantic Namespace.
A alocação consulta os CHANGEs ativos, arquivados e históricos do próprio
namespace, sem reservar ou consumir números em ancestrais, descendentes ou
irmãos. CHANGE-IDs curtos iguais em namespaces distintos são válidos; sua
unicidade é determinada pela identidade canônica `<namespace>:<CHANGE-ID>`.
Reutilizar um CHANGE-ID ativo, arquivado ou histórico no mesmo namespace produz
`FAIL`.

Em uma criação inicial governada, o único CHANGE de inicialização é
`CHANGE-INIT`, identificador especial, único por identidade canônica do
namespace e não reutilizável. Ele não consome a sequência numérica de CHANGE-IDs;
portanto, a primeira evolução normal do namespace usa `CHANGE-001`.

Se o namespace já possuir AS-IS sem registro de `CHANGE-INIT`, ele é tratado,
para fins do protocolo, como origem estabelecida fora de uma criação governada.
Isso não permite inferir ou registrar ferramenta ou autoria; a primeira evolução
governada usa `CHANGE-001`.

### 7.3. IDs locais de construção

Novas entidades ainda em construção dentro de um CHANGE podem utilizar aliases locais:

```text
R-A
D-A
O-A
```

Aliases locais:

- existem somente dentro do CHANGE;
- evitam consumir IDs oficiais prematuramente;
- não são identidades oficiais;
- não devem permanecer no AS-IS;
- devem ser promovidos antes da incorporação conforme a política de promoção.

A promoção de entidades R/D/O deve verificar duplicidade, reutilização e
alocações concorrentes somente no namespace semântico de destino e no
respectivo tipo. A existência do mesmo ID curto em namespace ancestral,
descendente ou irmão não bloqueia a promoção.

### 7.4. Preservação de identidade

MODIFY exige preservação razoável da identidade semântica.

Pergunta de controle:

> depois da mudança, ainda estamos falando essencialmente da mesma entidade?

Se a resposta for não, utilizar REMOVE + ADD.

---

## 8. CHANGE como unidade de evolução

CHANGE é a unidade lógica de transformação semântica do Semantic Git.

Um único CHANGE pode materializar-se em um ou vários repositórios físicos.

Um Merge Request físico não é equivalente ao CHANGE.

### 8.1. Contrato mínimo

Em fluxo Git, todo CHANGE material deve possuir no mínimo:

```yaml
change: CHANGE-014
status: DRAFT
base_commit: 71ac982
reason: null
```

O namespace é determinado pelo escopo em que o CHANGE vive. A identidade do
exemplo é `<namespace do documento>:CHANGE-014`; o campo curto não constitui
uma chave global.

`CHANGE-INIT` é o único valor permitido para o campo `change` de um CHANGE que
governe a criação inicial de um namespace sob o Semantic Git. Nesse caso, o
namespace alvo pode estar ausente do AS-IS registrado no `base_commit`, pois o
CHANGE cria seu primeiro AS-IS. Criação manual ou externa ocorre fora do
protocolo e não gera CHANGE de inicialização. Antes da aprovação, deve ser
validado que o alvo não possui AS-IS no `base_commit` e que sua branch adiciona
o primeiro AS-IS sem alterar Requirements, Decisions, Operations ou outro AS-IS
ancestral. A ausência do alvo não exige CHANGE no namespace pai. `CHANGE-INIT`
segue o fluxo normal de branch, aprovação, implementação, RECONCILIATION,
pre-merge recheck, merge e arquivamento.

Dependências excepcionais podem ser declaradas:

```yaml
depends_on:
  - domain:CHANGE-021
```

`depends_on` deve ser omitido quando não houver dependência real. Cada item deve
usar a identidade canônica completa, inclusive para dependência no mesmo
namespace. Autodependências e ciclos são comparados por identidade canônica,
nunca apenas pelo CHANGE-ID curto.

`reason` é opcional.

Se o motivo for desconhecido, a IA não deve inventá-lo.

### 8.2. Coesão

Um CHANGE deve conter, em geral, o conjunto coerente de alterações necessário para realizar uma transformação.

Não fragmentar artificialmente uma única transformação apenas para criar dependências entre CHANGEs.

### 8.3. CHANGE não é AS-IS

Conteúdo de CHANGE representa TO-BE.

Mesmo quando aprovado, um CHANGE ainda não é verdade vigente até sua incorporação ao AS-IS.

---

## 9. Semantic Delta e Semantic Diff

Todo CHANGE semântico material deve possuir delta explícito.

O **Semantic Delta** representa a transformação conceitual pretendida.

Sua forma concreta preferencial é o **Semantic Diff**.

O Semantic Diff deve separar, conforme aplicável:

```text
REQUIREMENTS
DECISIONS
OPERATIONS
```

Cada dimensão pode utilizar:

```text
ADD
MODIFY
REMOVE
NONE
```

### 9.1. ADD

```text
ADD
= nasce uma verdade ou identidade semântica nova
```

ADD contém somente conteúdo novo.

### 9.2. REMOVE

```text
REMOVE
= uma verdade ou identidade semântica vigente deixa de existir
```

O ID oficial removido não pode ser reutilizado no mesmo namespace controlador e no mesmo tipo.

### 9.3. MODIFY

```text
MODIFY
= a identidade permanece, mas parte de seu significado muda
```

MODIFY deve mostrar:

1. contexto original suficiente;
2. menor fragmento que deixa de valer;
3. fragmento que passa a valer.

Forma canônica:

```text
MODIFY R-021

"A competência anterior deve ser congelada após o dia 10."

- dia 10
+ dia 15
```

Não inventar campos intermediários que não existam no conhecimento original.

### 9.4. REMOVE + ADD

Quando a identidade anterior deixa conceitualmente de existir e outra nasce, utilizar:

```text
REMOVE + ADD
```

Não usar MODIFY apenas porque algum texto mudou.

### 9.5. NONE

NONE indica explicitamente que uma dimensão não sofre alteração semântica naquele CHANGE.

NONE não é motivo para criar CHANGE vazio.

### 9.6. Regra de representação

> não explicar o delta quando é possível mostrar o próprio delta.

Preferir texto original e `- / +` a paráfrases ou categorias inventadas.

### 9.7. Evolução do Semantic Diff

Enquanto o CHANGE estiver aberto, o Semantic Diff representa a melhor compreensão atual do futuro desejado.

Se a compreensão mudar, o Semantic Diff deve ser atualizado.

A aprovação humana não congela a capacidade de aprender; ela congela qual contrato semântico está aprovado naquele momento.

Mudança material posterior exige nova aprovação.

---

## 10. Semantic Diff não é Git Diff

```text
Semantic Diff
= o que mudou no significado

Git Diff
= o que mudou fisicamente
```

É permitido:

```text
Git Diff ≠ 0
Semantic Diff = NONE
```

quando a diferença física preservar integralmente o significado.

A correspondência não precisa ser linha a linha.

Ela precisa ser semanticamente coerente.

Git fornece fatos físicos.

Semantic Diff explicita transformação de significado.

---

## 11. PRD, SPEC e TODO

PRD, SPEC e TODO são instrumentos opcionais do CHANGE.

Não são dimensões permanentes obrigatórias do AS-IS.

Funcionam como andaimes temporários da transformação.

### 11.1. PRD

PRD pode ser utilizado para explorar:

- problema;
- objetivo;
- contexto;
- restrições;
- resultado esperado.

É particularmente útil para descobrir e formular mudança de Requirements.

Conhecimento duradouro oriundo de PRD deve ser consolidado, quando aplicável, em:

```text
REQUIREMENTS
```

### 11.2. SPEC

SPEC descreve como a transformação será realizada.

Pode conter:

- desenho técnico;
- componentes afetados;
- migração;
- compatibilidade;
- estratégia de testes;
- detalhes relevantes de execução.

Escolhas estruturais duradouras surgidas na SPEC devem ser consolidadas, quando aplicável, em:

```text
DECISIONS
```

### 11.3. TODO

TODO representa trabalho pendente do CHANGE.

Deve ser concreto, verificável e temporário.

Procedimentos que continuarem válidos após a mudança devem ser consolidados, quando aplicável, em:

```text
OPERATIONS
```

TODO não deve virar documentação permanente apenas porque foi utilizado durante a execução.

### 11.4. Regra de consolidação

```text
PRD                  ───→ REQUIREMENTS
SPEC                 ───→ DECISIONS
TODO / execução      ───→ OPERATIONS
```

A seta significa:

> extrair e consolidar somente o conhecimento que continuará válido.

Não significa copiar o documento temporário integralmente.

---

## 12. Evolução interna e snapshots

Um CHANGE aberto pode evoluir.

Hipóteses podem ser ampliadas, reduzidas, divididas, reformuladas ou descartadas antes da conclusão.

Nada historicamente relevante pode tornar-se irrecuperável.

No mínimo devem existir:

```text
snapshot inicial
+
snapshot final
```

Snapshots intermediários devem ser preservados quando sua perda prejudicar a reconstrução futura, por exemplo:

- mudança relevante de escopo;
- reformulação material do Semantic Diff;
- alteração substancial de PRD ou SPEC;
- abandono de uma linha de solução relevante;
- marco importante em mudança longa ou complexa.

Rascunhos efêmeros não precisam ser preservados individualmente.

A IA pode decidir os momentos apropriados para snapshots intermediários sem exigir aprovação humana para cada marco histórico.

A estratégia Git não pode tornar os snapshots obrigatórios irrecuperáveis por squash, exclusão de branch ou limpeza de referências.

Snapshots são garantia histórica do CHANGE, não uma dimensão permanente de conhecimento.

---

## 13. Máquina de estados

Estados canônicos:

```text
DRAFT
  ↓
APPROVED
  ↓
IN_PROGRESS
  ↓
RECONCILED
  ↓
MERGED
```

Estado terminal alternativo:

```text
ABANDONED
```

### 13.1. DRAFT

O CHANGE existe, mas seu contrato semântico ainda não está aprovado.

Neste estado:

- o Semantic Diff pode evoluir;
- novas entidades podem nascer ou ser descartadas;
- PRD pode ou não existir;
- SPEC pode ou não existir;
- TODO pode ou não existir;
- nada deve ser tratado como semanticamente aprovado.

### 13.2. APPROVED

O humano aprovou o contrato semântico exato registrado pelas âncoras de aprovação.

A aprovação responde:

> é esta a transformação que queremos realizar?

Ela é distinta da aprovação de MR e do ato de merge.

### 13.3. IN_PROGRESS

A transformação aprovada está sendo executada.

Código, configuração, testes, documentação, PRD, SPEC e TODO podem evoluir desde que permaneçam coerentes com o contrato semântico aprovado.

### 13.4. RECONCILED

A execução foi confrontada com:

- Semantic Diff aprovado;
- estado final semântico;
- Git Diff(s);
- AS-IS aplicável;
- referências;
- hierarquia R/D/O;
- demais invariantes obrigatórias.

Não há pendências impeditivas observadas naquele estado.

RECONCILED não congela `main`.

### 13.5. MERGED

O CHANGE foi incorporado à `main`.

O TO-BE aprovado tornou-se parte do novo AS-IS.

MERGED é terminal.

Após a incorporação, a conclusão operacional do CHANGE exige seu arquivamento
no caminho canônico definido na seção 21. O estado `MERGED` somente deve ser
registrado depois que o movimento tiver sido concluído e validado.

Uma mudança posterior que desfaça ou altere esse resultado exige novo CHANGE.

### 13.6. ABANDONED

O CHANGE foi explicitamente encerrado sem incorporação ao AS-IS.

Pode ocorrer a partir de qualquer estado anterior a MERGED.

Não existe:

```text
MERGED → ABANDONED
```

### 13.7. Alteração material após aprovação

Se o contrato semântico aprovado sofrer alteração material:

```text
APPROVED
IN_PROGRESS
RECONCILED
    ↓
DRAFT
```

Nova validação humana é obrigatória.

Quando a alteração material ocorrer antes de `MERGED` e permanecer dentro do
mesmo escopo semântico:

- o mesmo `CHANGE-ID` deve ser mantido;
- a mesma branch exclusiva deve ser mantida;
- o estado deve retornar a `DRAFT`;
- o `base_commit` original deve ser preservado;
- o Semantic Diff deve ser atualizado com o novo delta;
- a aprovação anterior continua recuperável no histórico Git;
- a nova aprovação deve registrar um novo `approved_semantic_commit`.

Esse ciclo não cria outra branch nem outro CHANGE. Um novo CHANGE somente é
necessário quando a transformação for independente ou quando o escopo tiver
ultrapassado materialmente o contrato original.

Se o problema for somente de execução, sem alteração material do contrato:

```text
RECONCILED → IN_PROGRESS
```

O estado deve decorrer de condições objetivas, não de escolha arbitrária da IA.

### 13.8. Gates de capacidade e autorização

Estado de CHANGE e autorização operacional são conceitos distintos. Nenhum
estado, por si só, autoriza merge, criação de tag ou push.

Enquanto o CHANGE estiver em `DRAFT`, a IA pode somente:

- ler contexto e materializações;
- sintetizar intenção e Semantic Diff;
- analisar gaps, conflitos e impactos;
- escrever ou atualizar a própria CHANGE em elaboração.

Em `DRAFT`, a IA não pode alocar agentes de implementação nem editar
`SEMANTIC_GIT.md`, R/D/O, materializações físicas ou arquivos fora da CHANGE.

`APPROVED` confirma somente o contrato semântico exato. A execução exige:

1. `approved_semantic_commit` existente;
2. `approval_scope` resolvido;
3. preflight de recursos, branch, escopo e drift aprovado;
4. autorização explícita de implementação, identificando a CHANGE por sua
   identidade canônica;
5. transição explícita para `IN_PROGRESS`.

Uma aprovação semântica deve identificar a CHANGE por sua identidade canônica.
Para autorizar também a execução, o humano deve dizer, por exemplo:

```text
Aprovo e autorizo a implementação de domain:CHANGE-014.
```

Uma autorização que use apenas CHANGE-ID curto ou que não possa ser vinculada
inequivocamente à identidade canônica produz `IMPLEMENTATION_BLOCKED`.

Somente `IN_PROGRESS` permite implementação, limitada ao escopo aprovado.
`RECONCILED` permite validação e correções de execução autorizadas, mas não
autoriza merge.

As autorizações abaixo são independentes:

```text
semantic approval
    ≠ implementation authorization
    ≠ merge authorization
    ≠ tag/release authorization
    ≠ push/publication authorization
```

Uma autorização de merge somente existe quando o humano identificar a identidade
canônica da CHANGE, a branch globalmente única de origem e a `main` de destino
em uma instrução explícita, por exemplo:

```text
Faça o merge de domain:CHANGE-014 da branch
`change/domain/CHANGE-014-slug` na `main`.
```

"Aprovado", "faça", "pode seguir" ou equivalentes não autorizam merge, tag,
release ou push quando não identificarem explicitamente a operação. Na dúvida,
a IA deve produzir `MERGE_BLOCKED`, `RELEASE_BLOCKED` ou
`PUBLICATION_BLOCKED`, conforme o caso.

---

## 14. Aprovação semântica e âncoras Git

### 14.1. `base_commit`

Todo CHANGE criado em fluxo Git deve registrar o commit imutável que representa o AS-IS físico de origem:

```yaml
base_commit: 71ac982
```

`base_commit` responde:

> de qual estado físico esta transformação partiu?

### 14.2. `approved_semantic_commit`

Quando o humano aprovar o contrato semântico, deve ser registrado o commit que contém a versão exata aprovada:

```yaml
approved_semantic_commit: b18f3a1
```

Em uma nova aprovação do mesmo CHANGE antes de `MERGED`, o novo snapshot
aprovado substitui o `approved_semantic_commit` vigente como referência atual.
O valor anterior não deve ser apagado do histórico Git. O `base_commit` não
muda enquanto a transformação continuar no mesmo escopo semântico.

### 14.3. `approval_scope`

A aprovação deve registrar os documentos efetivamente aprovados:

```yaml
approval_scope:
  - path/to/CHANGE-014.md
```

Assim:

```text
base_commit
= de onde a transformação partiu

approved_semantic_commit + approval_scope
= exatamente qual transformação semântica foi aprovada
```

O metadado que registra o hash pode existir em commit posterior ao snapshot aprovado.

Não criar hash autorreferente.

Não é necessário criar hash semântico adicional quando commit + Git diff forem suficientes.

### 14.4. Identidade do aprovador

A identidade do aprovador não é obrigatória no núcleo do Semantic Git.

Projetos podem ativar auditoria automática de identidade Git.

A IA nunca deve inventar identidade ausente.

### 14.5. Drift após aprovação

Mudança material no conteúdo abrangido por:

```text
approved_semantic_commit + approval_scope
```

exige retorno a DRAFT e nova aprovação humana.

Alterações exclusivamente técnicas, editoriais, de TODO, evidência, formatação ou metadados de aprovação não invalidam automaticamente a aprovação quando preservarem integralmente o significado aprovado.

---

## 15. Fluxo de uma mudança

```text
AS-IS do namespace relevante, quando existente
ou ausência do AS-IS do namespace-alvo em `CHANGE-INIT`
  ↓
necessidade percebida
  ↓
menor escopo suficiente
  ↓
branch exclusiva do CHANGE
  ↓
CHANGE / DRAFT
  ↓
base_commit
  ↓
proposta e análise de gaps
  ↓
PRD, se necessário
  ↓
primeira formulação coerente
  ↓
snapshot inicial
  ↓
Semantic Delta / Semantic Diff
  ↓
validação humana do significado
  ↓
approved_semantic_commit + approval_scope
  ↓
APPROVED
  ↓
SPEC, se necessária
  ↓
TODO, se necessário
  ↓
IN_PROGRESS
  ↓
execução
  ↓
snapshots intermediários, quando necessários
  ↓
validação
  ↓
RECONCILIATION
  ↓
RECONCILED
  ↓
promoção de IDs locais conforme política
  ↓
pre-merge recheck
  ↓
snapshot final recuperável
  ↓
merge
  ↓
arquivamento pós-merge obrigatório
  ↓
MERGED
  ↓
novo AS-IS
```

Para toda transformação semântica material, a branch exclusiva e globalmente
única no repositório deve existir antes da criação ou evolução do CHANGE. Para
novos CHANGEs, a convenção operacional é:

```text
change/<namespace-key>/<CHANGE-ID>-<slug-curto>
```

`root` é o `namespace-key` reservado ao namespace raiz. Para os demais
namespaces, `namespace-key` é a representação reversível do namespace canônico
em um único componente de ref Git: bytes UTF-8 que não sejam letras ASCII
minúsculas, algarismos ou hífen são codificados como `%HH`, com hexadecimal
maiúsculo. Assim, `domain/operation` torna-se
`domain%2Foperation`. O namespace decodificado da branch deve
corresponder ao namespace controlador da identidade canônica do CHANGE.

O `slug-curto` deve usar somente caracteres ASCII minúsculos, algarismos e
hífens. O namespace representado na branch é redundância operacional
verificável: não define nem substitui o namespace documental, o escopo ou a
identidade semântica.

Antes de criar um CHANGE, devem ser validados atomicamente: a inexistência da
identidade canônica no namespace controlador, a disponibilidade do caminho
ativo local e a unicidade global da branch Git. A alocação do próximo CHANGE-ID
consulta somente CHANGEs ativos, arquivados e recuperáveis no histórico desse
namespace; números de outros namespaces não participam da alocação.

CHANGE-IDs e nomes de branches estabelecidos antes do Semantic Git 1.4 são
preservados sem renumeração ou migração retroativa obrigatória. A branch
`change/CHANGE-004-change-ids-locais`, usada para introduzir esta regra, também
é preservada. A nova convenção aplica-se apenas a CHANGEs criados depois desta
mudança.

O fluxo resumido obrigatório é:

```text
branch exclusiva
    ↓
CHANGE / DRAFT
    ↓
proposta e análise de gaps
    ↓
validação humana
    ↓
implementação definitiva
    ↓
RECONCILIATION
    ↓
merge
    ↓
arquivamento pós-merge obrigatório
    ↓
MERGED
```

A proposta e a análise de gaps podem ser ajustadas ou descartadas antes da
validação. Elas não são implementação definitiva e não podem ser tratadas como
AS-IS. A implementação definitiva somente começa depois da validação humana do
contrato semântico exato. A branch mantém `main` como AS-IS durante todo o
período anterior ao merge.

### 15.1. Novo ciclo antes do merge

Se uma alteração material for identificada em `APPROVED`, `IN_PROGRESS` ou
`RECONCILED`, e o CHANGE ainda não tiver sido incorporado à `main`, o fluxo é:

```text
CHANGE RECONCILED
    ↓ alteração material identificada
mesma branch + mesmo CHANGE / DRAFT
    ↓
Semantic Diff atualizado
    ↓
proposta e análise de gaps
    ↓
nova validação humana
    ↓
novo approved_semantic_commit
    ↓
implementar somente o novo delta
    ↓
RECONCILIATION completa
    ↓
RECONCILED
```

O ciclo anterior não deve ser apagado nem reescrito. A nova reconciliação deve
verificar o contrato completo, embora a implementação física se limite ao
delta aprovado no novo ciclo.

A presença de PRD, SPEC ou TODO é opcional.

As condições semânticas e de reconciliação não são opcionais quando aplicáveis.

### 15.2. Transação de incorporação local

A incorporação autorizada deve ser tratada como uma transação única. A IA deve:

1. capturar o `HEAD` exato da branch candidata e o `HEAD` exato da `main`;
2. confirmar a autorização explícita de merge para esses alvos;
3. iniciar a integração sem finalizar o commit de merge;
4. mover a CHANGE com `git mv` para o diretório `changes/archived/` do
   namespace controlador;
5. atualizar o estado para `MERGED` somente no resultado integrado;
6. validar o AS-IS final, a ausência da origem e a integridade do histórico;
7. criar um único merge commit que contenha toda a transação.

Qualquer falha antes do merge commit final deve abortar a integração e produzir
`MERGE_BLOCKED`. Não é permitido deixar uma integração parcialmente finalizada,
uma CHANGE `MERGED` ativa ou um arquivo arquivado sem o merge correspondente.

Push, tag e release são posteriores e independentes dessa transação.

---

## 16. RECONCILIATION semântica

Antes de qualquer CHANGE ser incorporado ao AS-IS, RECONCILIATION é obrigatória.

Confrontar explicitamente:

```text
Semantic Diff aprovado
          ↕
estado final semântico
          ↕
Git Diff(s) da implementação
          ↕
AS-IS semântico atual
          ↕
integridade entre R / D / O
          ↕
integridade referencial
```

Em `CHANGE-INIT`, a ausência de AS-IS no namespace alvo é ausência de
predecessor e não deve ser materializada como arquivo, entidade ou baseline
vazio. A reconciliação confronta o Semantic Diff aprovado com o primeiro AS-IS
adicionado e valida que não há alterações nos AS-IS ancestrais.

Pergunta central:

> tudo o que foi realmente alterado está corretamente representado pelo CHANGE e continua compatível com o AS-IS no qual será incorporado?

A reconciliação deve detectar tanto:

```text
mudança declarada mas não materializada
```

quanto:

```text
mudança materializada mas não declarada
```

### 16.1. Integridade R / D / O

Verificar, conforme aplicável:

- Requirement removido ainda referenciado por Decision ou Operation;
- Decision incompatível com Requirement vigente;
- Operation incompatível com Requirement ou Decision;
- Requirement ancestral aplicável violado;
- conhecimento duradouro de PRD/SPEC/TODO não consolidado quando necessário;
- implementação que materializa significado diferente do aprovado.

### 16.2. Integridade referencial

Verificar:

- referências órfãs;
- referências curtas ambíguas;
- referências relativas irresolvíveis;
- entidades removidas ainda referenciadas;
- dependências semanticamente incompatíveis;
- aliases locais ainda não resolvidos no momento em que deveriam estar promovidos;
- referências cujo namespace semântico mudou sem reconciliação;
- MODIFY utilizado sem preservação razoável de identidade.

Exemplo:

```text
domain:D-004 → domain:R-017
```

Se o CHANGE fizer:

```text
  REMOVE domain:R-017
```

a reconciliação deve detectar que `domain:D-004` ficaria com referência inválida ou semanticamente inconsistente.

Um MODIFY não obriga automaticamente a alteração de todos os dependentes.

A IA deve verificar se eles continuam compatíveis.

### 16.3. Verificação do contrato aprovado

A reconciliação deve verificar se o conteúdo semântico executado continua correspondendo ao snapshot aprovado por:

```text
approved_semantic_commit
+
approval_scope
```

O Git fornece a fotografia exata do conteúdo aprovado e das alterações posteriores.

A IA deve interpretar o diff posterior e decidir se houve drift semântico material.

Se houver, o CHANGE retorna a DRAFT.

### 16.4. AS-IS de origem

O Semantic Diff final deve corresponder à diferença entre:

```text
AS-IS semântico de origem
↕
novo AS-IS proposto
```

Não basta que o Semantic Diff descreva a intenção atual se ele já não representar corretamente a transformação desde a origem relevante.

### 16.5. Concorrência entre CHANGEs

Se `main` avançar após `base_commit`, o CHANGE não se torna automaticamente inválido.

A IA deve avaliar se o avanço interfere no conhecimento relevante.

A árvore de namespaces é indicador inicial de sobreposição, não prova suficiente.

Conflito material com mais de uma interpretação válida exige decisão humana.

### 16.6. Múltiplos CHANGEs candidatos

Antes do primeiro merge de uma mesma janela, analisar conjuntamente os CHANGEs candidatos quando houver possibilidade de sobreposição.

```text
CHANGE-A ─┐
CHANGE-B ─┼─→ análise de conflito semântico
CHANGE-C ─┘
```

A ordem de merge deve ser considerada quando puder alterar o resultado.

A IA deve informar ao humano quando a ordem de incorporação puder produzir resultados semanticamente diferentes.

---

## 17. Pre-merge recheck

RECONCILED significa que a mudança estava coerente com o AS-IS observado durante a reconciliação.

Isso não congela `main`.

Imediatamente antes do merge:

```text
1. observar HEAD(main)
2. verificar se corresponde ao AS-IS avaliado
3. se mudou, reavaliar impacto
4. repetir até que o merge ocorra contra o estado validado
```

Se o avanço da main for:

```text
irrelevante
→ seguir

relevante apenas à execução
→ ajustar, retornar a IN_PROGRESS quando necessário e reconciliar

material ao contrato semântico
→ retornar a DRAFT e solicitar nova aprovação
```

Git fornece o fato de que o mundo mudou.

A IA interpreta o impacto semântico dessa mudança.

O pre-merge recheck é obrigatório.

Quando o recheck for aprovado, registrar o conjunto de entrada do gate:

```text
main_head
candidate_head
base_commit
approved_semantic_commit
approval_scope
final_snapshot
```

Esse conjunto é imutável para a tentativa de incorporação. Qualquer mudança
em uma dessas entradas, na branch candidata ou na `main`, invalida o resultado
e exige novo recheck. `READY` confirma somente o conjunto capturado; não
autoriza merge.

---

## 18. Promoção de IDs locais

Entidades locais que sobreviverão devem receber IDs oficiais antes de entrar no AS-IS.

Modos suportados:

```text
pre_merge
reconciliation
```

Apenas um modo pode estar ativo por projeto.

Padrão:

```text
pre_merge
```

Configuração:

```yaml
id_promotion:
  mode: pre_merge
```

### 18.1. Modo `pre_merge`

A promoção ocorre depois de RECONCILED e antes do merge.

Esse é o modo padrão porque evita consumir IDs oficiais antes de a identidade estar efetivamente prestes a entrar no AS-IS.

### 18.2. Modo `reconciliation`

A promoção ocorre dentro da própria RECONCILIATION.

É apropriado quando validações finais, integrações ou regras de integridade precisam trabalhar com IDs oficiais antes de declarar RECONCILED.

### 18.3. Regras comuns

Independentemente do modo:

1. identificar entidades locais que sobreviverão;
2. determinar o namespace semântico de destino;
3. determinar o tipo R, D ou O;
4. atribuir o próximo ID oficial daquele tipo dentro do namespace de destino;
5. alocar IDs de forma exclusiva e atômica;
6. impedir duplicidade ou reutilização de IDs R/D/O no mesmo namespace de
   destino e tipo, inclusive entre CHANGEs concorrentes;
7. substituir aliases locais;
8. atualizar dependências e referências;
9. atualizar o Semantic Diff final;
10. verificar novamente a integridade;
11. garantir que o CHANGE arquivado utilize IDs oficiais resolvíveis.

Exemplo:

```text
R-A → domain:R-028
R-B → apuracao:R-011
```

O histórico oficial não deve depender do conhecimento de aliases locais.

### 18.4. Exclusividade da política

Não é permitido decidir o modo individualmente em cada CHANGE.

O modo é política do projeto/repositório.

Nunca usar os dois simultaneamente.

---

## 19. Fechamento de CHANGE

Um CHANGE somente pode chegar a RECONCILED quando:

- Semantic Diff está atualizado;
- o contrato semântico atual corresponde ao snapshot aprovado;
- o escopo do CHANGE contém integralmente a transformação;
- Requirements afetados estão coerentes;
- Requirements ancestrais aplicáveis foram respeitados;
- Decisions necessárias foram persistidas;
- Operations necessárias foram atualizadas;
- conhecimento duradouro surgido em PRD, SPEC ou TODO foi consolidado quando aplicável;
- materializações físicas estão coerentes com o estado proposto;
- testes necessários foram concluídos;
- documentação vigente representa o novo estado proposto;
- IDs locais sobreviventes foram promovidos no momento definido pela política, quando aplicável;
- referências foram reconciliadas;
- não existem referências órfãs ou ambíguas;
- Semantic Diff e Git Diff(s) são compatíveis;
- conflitos concorrentes relevantes foram tratados;
- dependências explícitas foram satisfeitas;
- o Semantic Diff final representa a diferença entre o AS-IS de origem e o novo AS-IS proposto;
- a suíte obrigatória não contém FAIL nem REVIEW impeditivo.

O campo `reason` pode permanecer vazio.

Sua ausência não bloqueia fechamento.

Depois de RECONCILED, o pre-merge recheck continua obrigatório.

Imediatamente antes da incorporação deve existir snapshot final recuperável representando o estado efetivamente levado ao merge.

A estratégia Git deve preservar também o snapshot inicial e snapshots intermediários historicamente relevantes.

Somente depois da incorporação à `main` o CHANGE passa a:

```text
MERGED
```

---

## 20. Relação com Git

Git deve ser utilizado intensivamente.

```text
main
= AS-IS aprovado

branch
= TO-BE em desenvolvimento

git diff
= Git Diff / mudança física

CHANGE
= transformação semântica situada em namespace

Semantic Diff
= significado que nasceu, deixou de valer ou mudou

Merge Request
= processo de revisão e aprovação operacional da incorporação

merge
= transformação aprovada do TO-BE em novo AS-IS

Git history
= evolução física e temporal
```

No Semantic Repository governante, a `main` local é a referência oficial do
AS-IS. Um merge concluído nessa `main` incorpora semanticamente a transformação
e não depende de push para ser vigente.

`origin/main` e outras referências remotas são réplicas ou destinos de
publicação. `git push` transmite commits e referências já existentes, mas não
aprova, não reconcilia, não incorpora e não altera o AS-IS local.

Tags são marcadores de versão. Criar tag exige autorização explícita separada
e não é consequência automática de aprovação, reconciliação ou merge.

Push e criação de tag não podem ser executados pela IA sem autorização textual
explícita que identifique a operação, a referência e o destino. Falha de push
não desfaz nem invalida o AS-IS local já incorporado.

Git fornece fatos físicos e temporais.

Documentos explicitam significado.

Semantic Namespace resolve identidade contextual.

A IA interpreta contexto, impacto, coerência e conflito.

---

## 21. Histórico e reversão

CHANGEs concluídos não devem ser apagados definitivamente.

Podem ser preservados por recurso que garanta recuperação histórica. Para
CHANGEs com estado `MERGED`, este repositório adota adicionalmente o
arquivamento físico obrigatório:

```text
<namespace-dir>/changes/<CHANGE-ID>.md
                   ↓ merge confirmado
<namespace-dir>/changes/archived/<CHANGE-ID>.md
```

Os caminhos são relativos ao diretório documental do Semantic Namespace que
controla a identidade. Para `root`, `<namespace-dir>` é a raiz do Semantic
Repository; para `domain/operation`, por exemplo, é `domain/operation/`.

O movimento deve ser executado pela IA com `git mv`, nunca por cópia. O conteúdo
semântico, a identidade, os IDs, as referências e o histórico devem ser
preservados. A atualização do campo de estado para `MERGED` é metadado de
ciclo e somente pode ocorrer depois que o destino existir, a origem não existir
mais e a integridade do movimento tiver sido validada.

O diretório `changes/` de cada namespace é reservado para seus CHANGEs não
incorporados. Uma CHANGE `MERGED` encontrada no caminho ativo de seu namespace
produz `FAIL`. Não existe um novo estado `ARCHIVED`.

Uma referência de `approval_scope` ao arquivo ativo de uma CHANGE continua
resolvível após a relocação canônica para o `changes/archived/` do mesmo
namespace. A resolução usa a identidade canônica e o namespace de origem do
caminho aprovado; nunca busca globalmente por basename ou CHANGE-ID curto. A
relocação histórica não constitui drift semântico e não exige nova aprovação.

Se o arquivamento pós-merge falhar, a IA deve produzir `FAIL` e não declarar o
fluxo concluído. O tratamento obrigatório de `ABANDONED` permanece limitado à
preservação histórica geral desta seção.

O AS-IS atual deve ser compreensível sem leitura obrigatória de CHANGEs históricos.

Para entender o presente, deve bastar consultar:

```text
REQUIREMENTS
DECISIONS
OPERATIONS
```

mais as materializações vigentes quando necessário.

Quando alguém perguntar como uma entidade evoluiu, CHANGEs são a primeira fonte da evolução semântica.

Quando alguém perguntar qual era literalmente o conteúdo físico, Git é a fonte adequada.

Um CHANGE MERGED não deve ser reescrito para fingir que nunca existiu.

Reversão material deve ser representada por novo CHANGE.

`git revert` não substitui CHANGE quando o significado for alterado.

Mudança material ocorrida fora do fluxo normal deve ser regularizada por CHANGE de reconciliação quando o AS-IS documental deixar de representar a realidade oficial.

---

## 22. Semantic Repository e materializações externas

O Semantic Repository representa a estrutura de conhecimento semântico governada pelo Semantic Git.

As materializações podem estar:

- no próprio repositório;
- em outro repositório Git;
- distribuídas entre vários repositórios independentes.

A árvore semântica não deve ser redesenhada para reproduzir a topologia física da implementação.

```text
estrutura semântica
≠
estrutura física
```

A relação é associação, não composição física.

Não exigir Git aninhado ou submodules apenas para reproduzir a árvore semântica.

### 22.1. Configuração autoritativa

O arquivo padrão é:

```text
.semantic-repo.yaml
```

Ele é versionado e representa a autoridade compartilhada para navegação:

```text
semântico → físico
```

Exemplo:

```yaml
sources:
  domain/indicator:
    repo: git@example.com:org/implementation.git
    branch: main
    path: models/indicadores/example_framework
```

Um namespace pode apontar para vários repositórios de implementação.

Um repositório físico pode materializar vários namespaces.

`branch` deve ser sempre informada e identifica a referência padrão compartilhada para investigação do vínculo. Ela não deve ser inferida a partir do clone local, da branch corrente ou da configuração padrão do repositório remoto.

`path` é ponto recomendado de investigação, não fronteira rígida, salvo regra explícita do projeto.

### 22.2. Configuração local opcional

A localização dos clones na máquina não é conhecimento compartilhado.

Quando necessária, usar:

```text
.semantic-repo.local.yaml
```

Ele pode mapear identidades remotas e branches para caminhos locais, inclusive quando o mesmo repositório possuir várias worktrees.

A configuração local pode disponibilizar branches adicionais, mas não deve redefinir silenciosamente a `branch` padrão declarada em `.semantic-repo.yaml`.

Não deve ser versionado.

A ausência desse arquivo não impede compreensão dos vínculos remotos.

### 22.3. Semantic Link

Repositórios de implementação podem utilizar:

```text
semantic-link.yaml
```

para criar vínculo de retorno:

```text
implementação → semântica
```

Na raiz do repositório físico:

```yaml
semantic_repo: git@example.com:org/semantic.git
```

Em áreas físicas relevantes:

```yaml
    semantic_ref: domain/indicator
```

Quando ambos se aplicarem:

```yaml
semantic_repo: git@example.com:org/semantic.git
    semantic_ref: domain/indicator
```

Marcadores internos:

- são opcionais;
- devem permanecer escassos;
- aplicam-se aos descendentes até marcador mais específico;
- utilizam o marcador aplicável mais próximo.

### 22.4. Relação bidirecional e autoridade

```text
                 SEMANTIC REPOSITORY
                        │
                .semantic-repo.yaml
                        │
                        ├──────────────► IMPLEMENTATION REPO
                        │                       │
                        ◄──────────── semantic-link.yaml
```

O vínculo é bidirecional.

A autoridade do mapeamento é assimétrica:

```text
.semantic-repo.yaml
= autoridade semântico → físico

semantic-link.yaml
= vínculo/back-link físico → semântico
```

Divergências devem ser sinalizadas.

O link físico não deve substituir silenciosamente a autoridade do Semantic Repository.

### 22.5. Independência das identidades

Preservar separadamente:

```text
identidade semântica
identidade remota do repositório físico
caminho local da máquina
```

Nenhuma deve ser inferida automaticamente a partir das outras sem regra explícita.

---

## 23. Estrutura física mínima standalone

Um Semantic Repository governado pelo Semantic Git pode começar com:

```text
semantic-knowledge/
├── .git/
├── README.md                 # opcional
├── AGENTS.md
├── SEMANTIC_GIT.md
├── .semantic-repo.yaml
└── .gitignore
```

`SEMANTIC_GIT.md` é a única especificação normativa necessária.

Nenhuma especificação externa é requerida.

A árvore semântica surge sob demanda.

Exemplo quando houver conhecimento real:

```text
semantic-knowledge/
└── domain/
    └── indicator/
        ├── REQUIREMENTS.md
        ├── DECISIONS.md
        ├── OPERATIONS.md
        └── changes/
```

Nenhum arquivo R/D/O precisa existir vazio.

Quando usada, `.semantic-repo.local.yaml` deve constar no `.gitignore`.

Artefatos derivados por ferramentas, como manifestos, caches e logs, não constituem conhecimento oficial e devem ser regeneráveis.

### 23.1. Papel de `AGENTS.md`

`AGENTS.md` é uma interface operacional para agentes.

Ele pode instruir a IA a utilizar o Semantic Git e uma skill associada, mas não deve duplicar toda a especificação.

Sua ausência não altera as regras normativas do Semantic Git, embora um projeto possa torná-lo obrigatório por convenção local.

### 23.2. Papel de skills

Uma skill do Semantic Git é opcional.

Quando existir, deve:

- resumir o procedimento operacional;
- orientar progressive disclosure;
- indicar quando consultar seções específicas de `SEMANTIC_GIT.md`;
- nunca substituir a fonte normativa;
- declarar compatibilidade com a versão do Semantic Git.

O funcionamento semântico do padrão não pode depender de regras existentes somente na skill.

### 23.3. Padrão documental canônico

O padrão documental usado pela aplicação MOP é o padrão global do Semantic Git
para documentos permanentes de Semantic Namespaces. Nenhum padrão alternativo
é válido.

#### Nomes canônicos

Os nomes físicos são sensíveis a maiúsculas e minúsculas e são exatamente:

```text
README.md          opcional
REQUIREMENTS.md    quando houver Requirements no namespace
DECISIONS.md       quando houver Decisions no namespace
OPERATIONS.md      quando houver Operations no namespace
```

Não são válidos nomes singulares, nomes em minúsculas, variações de grafia,
arquivos duplicados ou novos arquivos permanentes para representar uma dessas
dimensões. Não são válidos novos tipos de documento permanente dentro de um
Semantic Namespace. Um novo tipo só pode existir após alteração normativa
explícita desta especificação.

A ausência de `README.md` é válida e não deve provocar sua criação. A ausência
de um arquivo R/D/O também é válida quando a dimensão não se aplica. Arquivos
R/D/O vazios não são válidos.

Documentos de infraestrutura desta especificação, instruções operacionais de
agentes e artefatos de CHANGE autorizados possuem regras próprias e não criam
um padrão alternativo para o AS-IS de um namespace. Documentos auxiliares de
uma aplicação somente podem existir fora desse AS-IS canônico e não autorizam
a criação de novos tipos permanentes.

#### `README.md`

Quando existir, `README.md` deve conter somente o essencial para identificar o
namespace e compreender seu propósito ou escopo. Pode conter links diretos de
orientação quando forem indispensáveis.

`README.md` não é dimensão semântica e não pode conter Requirements, Decisions,
Operations, IDs, histórico, procedimentos operacionais ou regras concorrentes.
Não deve receber seções, tabelas, metadados ou conteúdo explicativo que não
seja necessário para essa orientação mínima.

#### Arquivos R/D/O

Cada arquivo R/D/O deve possuir exatamente esta estrutura, nesta ordem:

```markdown
# Requirements - <nome do namespace>

## Cabeçalho

<resumo curto do escopo>

## Corpo

- **R-001** - <texto do Requirement>
```

Para `DECISIONS.md`, usar `Decisions` e o prefixo `D-`. Para `OPERATIONS.md`,
usar `Operations` e o prefixo `O-`.

O arquivo deve conter um único título de nível 1, um único `## Cabeçalho` e um
único `## Corpo`, nessa ordem. O `Cabeçalho` é um resumo do conteúdo do
namespace e não cria entidade ou ID. O `Corpo` contém somente uma lista direta
de itens, com um item por entidade:

```text
- **R-001** - texto
- **R-002** - texto
```

O ID deve usar o prefixo correspondente e pelo menos três algarismos decimais.
IDs oficiais permanecem estáveis e não podem ser alterados apenas para adequar
formatação. Não são válidos frontmatter, tabelas, listas aninhadas, seções
adicionais ou outro formato de item dentro desses arquivos.

O conteúdo de cada item deve respeitar sua dimensão: Requirement expressa o
que deve ser verdade; Decision expressa uma escolha duradoura; Operation
expressa comportamento ou procedimento operacional duradouro. Relações com
outras entidades devem permanecer no próprio item, por referências resolvíveis,
sem criar seções ou arquivos auxiliares.

Ao reorganizar um documento, a IA pode ordenar itens ou sintetizar o
`Cabeçalho` somente quando isso preservar integralmente significado, identidade,
referências e histórico. Não pode criar conteúdo para completar o formato.

A IA também pode sintetizar a redação de um item quando a formulação resultante
for semanticamente equivalente ao conhecimento sustentado por fontes canônicas,
intenção humana explícita ou CHANGE em análise. Sintetizar significa condensar
ou relacionar significado existente; não significa inventar requisito, escolha,
operação, justificativa, identidade ou decisão humana. Uma síntese materialmente
ambígua deve produzir `REVIEW`.

A validação estrutural dos nomes, seções, itens, IDs e referências é
determinística. A IA é usada somente para classificação, equivalência,
relação e síntese semântica quando a estrutura não for suficiente. A IA não
pode converter `FAIL` estrutural em resultado válido.

#### Regra de bloqueio

Nome de arquivo não canônico, arquivo R/D/O com estrutura diferente, seção
adicional, item fora do formato, ID R/D/O duplicado ou reutilizado no mesmo
namespace e tipo, referência persistida entre namespaces sem identidade canônica
completa, referência não resolvível ou novo tipo de documento permanente deve
produzir `FAIL`. A existência do mesmo ID curto R/D/O em namespace distinto não
é colisão. A IA não deve corrigir esse caso inventando uma convenção; deve
interromper a operação e informar a violação.

---

## 24. Bootstrap esperado da IA

O bootstrap deve ser suficiente para operar sem uma especificação externa.

### 24.1. Ao iniciar no Semantic Repository

A IA deve:

1. descobrir a raiz Git;
2. ler `SEMANTIC_GIT.md` ou, quando uma skill compatível já fornecer o procedimento operacional, carregar deste documento somente as seções normativas necessárias sob demanda;
3. ler `.semantic-repo.yaml`;
4. determinar o Semantic Namespace atual;
5. carregar REQUIREMENTS locais;
6. subir pelos ancestrais para recuperar Requirements aplicáveis;
7. consultar DECISIONS relevantes;
8. consultar OPERATIONS quando houver impacto operacional;
9. identificar CHANGE ativo aplicável quando existir;
10. expandir lateralmente somente quando dependências ou conflitos exigirem;
11. pesquisar CHANGEs históricos somente quando forem relevantes à pergunta ou transformação.

Não carregar indiscriminadamente toda a árvore nem toda a especificação quando o ambiente oferecer acesso seletivo confiável às regras necessárias.

Ao entrar em um namespace, a IA deve aplicar o padrão documental da seção
23.3 antes de interpretar ou reorganizar seu conteúdo. `README.md` é opcional.
Arquivos permanentes desconhecidos ou estruturas alternativas são violações
estruturais e não devem ser convertidos automaticamente para um novo padrão.

### 24.2. Ao iniciar em implementação governada

A IA deve:

1. descobrir a raiz Git física;
2. procurar `semantic-link.yaml` na raiz e, quando necessário, nos ancestrais físicos relevantes;
3. resolver `semantic_repo` e `semantic_ref`;
4. consultar o Semantic Repository antes de realizar escrita governada;
5. carregar o AS-IS semântico aplicável;
6. vincular alterações semânticas materiais a um CHANGE;
7. reconciliar a implementação com o contrato semântico antes de concluir.

### 24.3. Progressive disclosure

O contexto operacional preferencial é:

```text
namespace local
+
Requirements ancestrais aplicáveis
+
Decisions relevantes
+
Operations relevantes
+
CHANGE ativo
+
dependências laterais somente quando necessárias
```

A IA deve buscar mais contexto quando necessário, não antecipadamente por padrão.

---

## 25. Testes de conformidade

O Semantic Git adota o princípio:

> toda regra determinística do padrão deve, sempre que possível, existir como teste executável e não apenas como instrução para humanos ou IAs.

Estados importantes devem decorrer de condições verificáveis, e não apenas de campos declarados.

### 25.1. Classes de teste

Uma implementação de testes Semantic Git deve suportar, conceitualmente:

```text
STRUCTURAL
IDENTITY / REFERENCE
LIFECYCLE
GIT / HISTORY
LINK / INTEGRATION
RECONCILIATION
SEMANTIC
```

#### Structural

Exemplos:

- formato válido de CHANGE;
- `CHANGE-INIT` válido no contrato somente para criação inicial governada;
- status canônico;
- política de promoção válida;
- configurações obrigatórias quando aplicáveis;
- estrutura de arquivos válida quando presente;
- nomes canônicos de documentos;
- `README.md` ausente ou mínimo quando presente;
- estrutura exata de `REQUIREMENTS.md`, `DECISIONS.md` e `OPERATIONS.md`;
- ausência de arquivos R/D/O vazios;
- rejeição de seções, formatos de item e tipos documentais não previstos;
- nome válido e globalmente único da branch exclusiva do CHANGE;
- correspondência entre o `namespace-key` reversível da branch e o namespace
  controlador, sem usá-lo como fonte de autoridade;
- caminho ativo e caminho canônico de arquivamento relativos ao namespace
  controlador para CHANGEs `MERGED`;
- ausência de CHANGE `MERGED` no diretório ativo `changes/`;
- ausência de cópia simultânea da mesma CHANGE em local ativo e arquivado.

#### Identity / Reference

Exemplos:

- identidade canônica única;
- ID R/D/O não duplicado nem reutilizado no mesmo namespace e tipo;
- mesmo ID curto R/D/O aceito entre ancestral e descendente;
- mesmo ID curto R/D/O aceito entre namespaces irmãos;
- CHANGE-ID não reutilizado no mesmo namespace;
- CHANGE-IDs curtos iguais aceitos em namespaces distintos;
- próximo CHANGE-ID calculado somente sobre o histórico local do namespace;
- único CHANGE-INIT por namespace e não reutilizado;
- `CHANGE-INIT` não consome a sequência numérica e a primeira evolução normal
  usa `CHANGE-001`;
- AS-IS de origem sem registro de `CHANGE-INIT` usa `CHANGE-001` na primeira
  evolução governada, sem inferir sua proveniência;
- referências absolutas válidas;
- referências relativas resolvíveis;
- referência curta local válida quando inequivocamente resolvível;
- referência persistida entre namespaces exige identidade canônica completa;
- ausência de referências órfãs;
- dependências entre CHANGEs e detecção de ciclos resolvidas por identidade
  canônica completa;
- aliases locais resolvidos antes da incorporação;
- alocação atômica sem colisão.

#### Lifecycle

Exemplos:

- campos exigidos pelo estado presentes;
- CHANGE MERGED não tratado como ativo;
- APPROVED possui âncora de aprovação;
- alteração material após aprovação retorna a DRAFT;
- alteração material pré-merge permanece na mesma CHANGE e branch quando o escopo não muda;
- `CHANGE-INIT` percorre o fluxo normal de CHANGE;
- DRAFT não aloca recursos de implementação;
- aprovação semântica não autoriza merge, tag ou push;
- aprovação e autorização de implementação identificam a CHANGE por identidade
  canônica;
- autorização ambígua de implementação produz `IMPLEMENTATION_BLOCKED`;
- ABANDONED não tratado como candidato a merge.

#### Git / History

Exemplos:

- `base_commit` existe;
- `approved_semantic_commit` existe;
- `approval_scope` existe no commit indicado;
- branch do CHANGE existe e parte do `base_commit`;
- `CHANGE-INIT` pode iniciar namespace ausente do AS-IS em `base_commit` sem
  CHANGE no namespace pai;
- `base_commit` permanece estável em novo ciclo do mesmo CHANGE;
- novo snapshot de aprovação está ancorado sem apagar aprovações anteriores;
- `approval_scope` continua resolvível após relocação canônica da CHANGE;
- relocação de `approval_scope` é resolvida pela identidade canônica e pelo
  namespace de origem, sem busca global por basename ou ID curto;
- conjunto de entrada do pre-merge permanece imutável durante a transação;
- merge usa a branch e a `main` capturadas pelo gate;
- implementação definitiva não foi incorporada antes da validação humana;
- snapshots mínimos continuam recuperáveis;
- pre-merge recheck observa a `main` atual;
- movimento pós-merge preserva conteúdo semântico, identidade e histórico;
- branches anteriores ao Semantic Git 1.4 e a branch desta transformação são
  aceitas sem migração retroativa.

#### Link / Integration

Exemplos:

- `.semantic-repo.yaml` bem formado;
- `semantic-link.yaml` resolvível;
- divergência entre autoridade e back-link detectada;
- configuração local não versionada;
- nenhum Git aninhado criado apenas para reproduzir a árvore semântica.

#### Reconciliation

Exemplos:

- Semantic Diff compatível com Git Diff(s);
- transformação declarada foi materializada;
- transformação material não declarada foi classificada;
- conflitos concorrentes tratados;
- dependências satisfeitas;
- integridade referencial final válida;
- em `CHANGE-INIT`, a ausência de predecessor não é materializada como arquivo,
  entidade ou baseline vazio;
- `CHANGE-INIT` confronta o Semantic Diff aprovado com o primeiro AS-IS adicionado
  e não altera AS-IS ancestral;
- contrato atual corresponde ao aprovado.

#### Semantic

Exemplos canônicos:

```text
decision_respects_requirements
operation_respects_requirements
operation_respects_decisions
child_respects_ancestor_requirements
child_does_not_duplicate_ancestor_text
rdo_id_is_unique_within_namespace_and_type
rdo_id_is_not_reused_within_namespace
rdo_id_may_repeat_between_ancestor_and_descendant
rdo_id_may_repeat_between_siblings
cross_namespace_reference_requires_canonical_identity
local_short_reference_resolves_within_namespace
semantic_diff_source_matches_asis
semantic_diff_matches_approved_contract
modify_preserves_semantic_identity
removed_entity_has_no_live_semantic_dependents
semantic_namespace_resolves
governed_namespace_initialization_requires_single_change_init
external_namespace_initialization_has_no_initial_change
absence_of_change_init_is_not_governed_initialization_without_init
absence_of_change_init_does_not_infer_provenance
post_initial_namespace_material_change_requires_change
change_init_is_unique_per_namespace
change_init_does_not_consume_numeric_sequence
established_asis_without_initial_change_starts_at_change_001
change_init_target_may_be_absent_from_base_commit
change_init_does_not_require_parent_change
change_init_does_not_modify_ancestor_asis
semantic_reference_unambiguous
change_identity_is_namespace_qualified
change_id_sequence_is_namespace_local
change_id_may_repeat_across_namespaces
change_dependency_cycle_uses_canonical_identity
change_branch_is_globally_unique
change_branch_namespace_key_matches_controller
change_paths_are_relative_to_controller_namespace
change_approval_scope_relocation_uses_origin_namespace
implementation_matches_semantic_contract
implementation_gate_blocks_unapproved
implementation_gate_blocks_ambiguous_change_identity
merge_authorization_is_explicit
merge_gate_identifies_canonical_change_branch_and_destination
merge_transaction_is_atomic
local_main_is_authoritative
publication_is_not_incorporation
```

### 25.2. Determinístico antes de interpretativo

Quando uma regra puder ser decidida por estrutura, identidade, Git ou referência, o teste deve ser determinístico.

A IA deve ser utilizada somente onde a pergunta depender de significado.

Exemplo:

```text
D-004 referencia R-017 removido
→ FAIL determinístico
```

Já:

```text
D-004 ainda respeita o significado de R-017 após MODIFY?
→ teste semântico por IA
```

### 25.3. Resultados canônicos

```text
PASS
WARN
REVIEW
FAIL
IMPLEMENTATION_BLOCKED
MERGE_BLOCKED
RELEASE_BLOCKED
PUBLICATION_BLOCKED
```

- `PASS`: conformidade confirmada;
- `WARN`: condição não impeditiva que merece atenção;
- `REVIEW`: julgamento humano ou semântico é necessário antes de avançar;
- `FAIL`: invariante violada.
- `IMPLEMENTATION_BLOCKED`: recursos de implementação não podem ser alocados;
- `MERGE_BLOCKED`: incorporação local não está autorizada ou não é segura;
- `RELEASE_BLOCKED`: tag ou release não está autorizado;
- `PUBLICATION_BLOCKED`: push ou publicação não está autorizado.

`FAIL` bloqueia avanço.

`REVIEW` bloqueia transições que dependam daquela decisão até resolução.

`WARN` não bloqueia por padrão.

Quando houver mais de uma interpretação material plausível:

```text
REVIEW
```

A IA não deve decidir arbitrariamente.

### 25.4. RECONCILED como consequência

RECONCILED não deve ser apenas um status escrito manualmente.

Ele deve corresponder à aprovação da suíte obrigatória de reconciliação do projeto, sem FAIL e sem REVIEW impeditivo.

### 25.5. Gate de implementação

Antes de transicionar para `IN_PROGRESS`, a IA deve confirmar:

- identidade canônica da CHANGE em `APPROVED`;
- `approved_semantic_commit` e `approval_scope` válidos;
- branch correta e `base_commit` preservado;
- recursos de implementação disponíveis;
- ausência de drift material;
- escopo de escrita limitado ao contrato aprovado.

Se uma condição falhar, produzir `IMPLEMENTATION_BLOCKED` e não alocar agente
de implementação nem editar arquivos fora da CHANGE permitida em `DRAFT`.
Identidade curta ou ambígua na autorização também produz
`IMPLEMENTATION_BLOCKED`.

### 25.6. Gate de pre-merge

Antes do merge deve existir um gate que confirme:

- CHANGE continua reconciliado;
- `main` observada continua válida;
- promoção de IDs foi concluída conforme a política;
- referências permanecem íntegras;
- nenhuma nova incompatibilidade foi introduzida;
- autorização textual explícita identifica a identidade canônica da CHANGE, a
  branch globalmente única de origem e a `main` de destino;
- `main_head`, `candidate_head`, `base_commit`, `approved_semantic_commit`,
  `approval_scope` e snapshot final correspondem ao conjunto capturado;
- a transação de merge pode conter arquivamento, estado `MERGED` e resultado
  final sem duplicidade.

O resultado operacional pode ser:

```text
READY
```

ou:

```text
BLOCKED
```

READY não é novo estado do CHANGE.

É apenas resultado do gate imediatamente anterior ao merge.

`READY` não autoriza merge. Sem autorização textual explícita, produzir
`MERGE_BLOCKED`. Identidade, branch ou destino ausente, ambíguo ou inconsistente
também produz `MERGE_BLOCKED`.

### 25.7. Manifesto derivado

Ferramentas podem compilar o Semantic Repository para um manifesto derivado contendo:

- identidades;
- namespaces;
- relações;
- CHANGEs;
- vínculos;
- materializações.

Esse manifesto:

- não é fonte de verdade;
- não deve ser editado manualmente;
- deve ser regenerável;
- pode acelerar testes e navegação.

---

## 26. Comportamento esperado da IA

A IA deve:

- permitir que o humano expresse intenção sem conhecer o contrato interno do CHANGE;
- distinguir presente de transformação;
- localizar o menor Semantic Namespace suficiente;
- distinguir a criação inicial manual ou externa, que ocorre fora do protocolo e
  não gera `CHANGE-INIT` nem CHANGE de inicialização, da criação inicial sob o
  Semantic Git, que deve ser governada por um único `CHANGE-INIT`;
- não interpretar a ausência de `CHANGE-INIT` como criação governada sem
  `CHANGE-INIT`, nem inferir ferramenta ou autoria ou exigir reconstrução;
- tratar namespace já estabelecido sem registro de `CHANGE-INIT` como AS-IS de
  origem fora de uma criação governada e alocar `CHANGE-001` para sua primeira
  evolução governada, sem inferir ou registrar sua proveniência;
- exigir CHANGE para toda alteração semântica material posterior à existência do
  namespace, inclusive em REQUIREMENTS, DECISIONS e OPERATIONS;
- elevar o escopo do CHANGE quando a compreensão revelar impacto maior;
- respeitar Requirements ancestrais aplicáveis;
- consultar REQUIREMENTS antes de propor mudança;
- consultar DECISIONS antes de reinventar soluções;
- consultar OPERATIONS quando houver impacto operacional;
- expandir para namespaces irmãos apenas quando dependências ou conflitos tornarem isso relevante;
- pesquisar CHANGEs anteriores quando forem relevantes;
- preservar identidade canônica;
- resolver identidade como `namespace:ID`;
- alocar CHANGE-ID por sequência estritamente local, consultando CHANGEs ativos,
  arquivados e históricos somente no namespace controlador;
- manter `CHANGE-INIT` único por namespace, sem consumir `CHANGE-001`, permitir o
  alvo ausente do `base_commit` sem CHANGE no pai e aplicar o fluxo normal;
- aceitar CHANGE-ID curto repetido em namespaces distintos e rejeitar sua
  reutilização dentro do mesmo namespace;
- resolver índices, referências persistidas ambíguas, dependências, aprovações,
  autorizações e gates de CHANGE por identidade canônica;
- aceitar referências relativas quando úteis, mas normalizá-las para identidade absoluta durante validação;
- não adivinhar referências ambíguas;
- utilizar CHANGE para alterações semânticas materiais posteriores à existência
  do namespace;
- capturar `base_commit` ao criar CHANGE em fluxo Git;
- limitar em `DRAFT` os recursos a leitura, síntese, análise de gaps e escrita na própria CHANGE;
- executar o preflight de implementação antes de alocar qualquer agente de escrita;
- manter status coerente com a máquina de estados;
- produzir Semantic Diff explícito;
- separar ADD, MODIFY, REMOVE e NONE;
- verificar preservação de identidade antes de MODIFY;
- preferir REMOVE + ADD quando uma identidade for substituída;
- utilizar texto original sempre que possível;
- mostrar o menor fragmento necessário em `- / +`;
- atualizar o Semantic Diff quando a compreensão evoluir;
- utilizar aliases locais para novas entidades quando apropriado;
- obedecer à política de promoção de IDs;
- preservar snapshots históricos relevantes;
- registrar `approved_semantic_commit` e `approval_scope` após aprovação;
- nunca inventar `reason` nem identidade de aprovador;
- consolidar conhecimento duradouro de PRD/SPEC/TODO em R/D/O quando aplicável;
- reconciliar Semantic Diff, Git Diff(s), AS-IS e snapshot aprovado;
- verificar integridade referencial mesmo quando não houver promoção de IDs;
- detectar referências órfãs, ambíguas, relativas irresolvíveis e dependências semanticamente incompatíveis;
- analisar concorrência semântica entre CHANGEs;
- considerar a ordem de merge quando puder alterar resultado;
- executar testes determinísticos antes de julgamento semântico por IA;
- aplicar exclusivamente o padrão documental canônico da seção 23.3;
- tratar `README.md` como opcional e mínimo;
- herdar Requirements ancestrais sem copiar texto ou identidade;
- verificar duplicidade, reutilização e alocação concorrente de IDs R/D/O
  somente no namespace controlador e no respectivo tipo;
- bloquear padrões documentais não previstos antes de sintetizar conteúdo;
- criar branch exclusiva antes de criar ou evoluir CHANGE semântico material;
- validar atomicamente identidade canônica, caminho local e unicidade global da
  branch antes de criar um CHANGE;
- aplicar `change/<namespace-key>/<CHANGE-ID>-<slug-curto>` apenas a novos
  CHANGEs e preservar CHANGE-IDs e branches historicamente estabelecidos;
- manter proposta e análise de gaps como TO-BE até a validação humana;
- iniciar implementação definitiva somente após a validação humana;
- separar aprovação semântica de autorização de implementação, merge, tag e push;
- exigir autorização textual explícita para merge, tag e push;
- tratar a `main` local governante como AS-IS oficial e push como publicação;
- capturar e preservar o conjunto imutável de entradas do pre-merge;
- executar a incorporação em transação única com arquivamento e `MERGED`;
- reabrir o mesmo CHANGE e manter a mesma branch quando houver alteração material antes de `MERGED` dentro do mesmo escopo;
- preservar o `base_commit` e os snapshots anteriores durante novo ciclo;
- atualizar o `approved_semantic_commit` somente após nova validação;
- implementar somente o delta do novo ciclo e executar nova RECONCILIATION completa;
- após merge confirmado, arquivar automaticamente toda CHANGE `MERGED` no
  `changes/archived/` de seu namespace controlador usando `git mv`;
- migrar CHANGEs `MERGED` existentes para o caminho canônico quando a regra de arquivamento entrar em vigor;
- atualizar o estado para `MERGED` somente depois de validar o movimento pós-merge;
- produzir `FAIL` quando o arquivamento obrigatório não puder ser concluído;
- produzir `IMPLEMENTATION_BLOCKED`, `MERGE_BLOCKED`, `RELEASE_BLOCKED` ou `PUBLICATION_BLOCKED` quando o gate correspondente falhar;
- sinalizar contradições e conflitos;
- executar pre-merge recheck;
- manter o AS-IS limpo;
- usar Git para fatos físicos e temporais;
- usar documentos para significado persistente;
- carregar contexto progressivamente, evitando leitura indiscriminada.

---

## 27. O que a IA não deve fazer

A IA não deve:

- exigir do humano metadados determinísticos que possa derivar;
- inventar motivo ou identidade humana;
- inventar decisão semântica apenas para completar estrutura;
- tratar CHANGE-ID curto como identidade global;
- consultar números de CHANGE de namespaces ancestrais, descendentes ou irmãos
  para alocar a sequência local;
- criar ou aceitar nomes, seções, formatos ou tipos documentais alternativos;
- criar `README.md` apenas para completar a estrutura;
- copiar para um filho o texto ou a identidade canônica de uma entidade ancestral;
- executar implementação definitiva antes da validação humana do CHANGE;
- alocar agente de implementação em `DRAFT`;
- editar arquivos fora da CHANGE em `DRAFT`;
- interpretar aprovação semântica como autorização de merge, tag ou push;
- executar merge sem identificar explicitamente a identidade canônica da
  CHANGE, a branch globalmente única de origem e o destino;
- criar tag ou executar push automaticamente após merge;
- continuar uma transação de merge após mudança no conjunto de entradas capturado;
- usar o nome da branch para inferir namespace ou escopo semântico;
- resolver dependência, aprovação, autorização, gate ou relocação de
  `approval_scope` por busca global de CHANGE-ID curto ou basename;
- criar outra branch ou CHANGE para alteração do mesmo escopo antes de `MERGED`;
- resetar o `base_commit` ou apagar âncora de aprovação anterior em novo ciclo;
- implementar a alteração material antes da nova aprovação;
- deixar CHANGE `MERGED` no `changes/` ativo de seu namespace após o merge;
- copiar uma CHANGE para o arquivo histórico em vez de usar `git mv`;
- perguntar se deve executar arquivamento obrigatório já definido na especificação;
- definir `ARCHIVED` como novo estado;
- criar Operation sem conteúdo operacional duradouro;
- tratar branch ou CHANGE em desenvolvimento como AS-IS;
- resolver conflito material arbitrariamente;
- assumir que toda mudança pertence à raiz;
- manter CHANGE em escopo estreito quando o impacto se ampliou;
- confundir caminho físico com Semantic Namespace;
- derivar namespace automaticamente da topologia de implementação;
- reutilizar IDs oficiais no mesmo namespace e tipo ou renumerá-los por conveniência;
- promover entidade no namespace errado;
- usar MODIFY quando uma identidade foi substituída;
- transformar todo Git Diff em Semantic Diff;
- criar CHANGE para mudança sem impacto semântico;
- interpretar a ausência de `CHANGE-INIT` como criação governada sem
  `CHANGE-INIT`, prova de ferramenta ou autoria, ou motivo para reconstrução;
- registrar CHANGE de inicialização para criação manual ou externa, ou governar
  criação inicial sob o Semantic Git sem o único `CHANGE-INIT` exigido;
- criar mais de um `CHANGE-INIT` para a mesma identidade canônica de namespace;
- materializar a ausência de predecessor de `CHANGE-INIT` como arquivo, entidade
  ou baseline vazio;
- criar arquivos R/D/O vazios apenas para preencher estrutura;
- transformar PRD, SPEC ou TODO em documentação permanente por inércia;
- perder snapshots obrigatórios por estratégia Git;
- duplicar o mesmo significado em múltiplos lugares sem necessidade;
- criar árvores profundas sem necessidade;
- criar links físicos indiscriminadamente;
- tratar `semantic-link.yaml` como fonte concorrente de verdade;
- considerar testes físicos suficientes para declarar RECONCILED;
- definir RECONCILED manualmente quando a suíte obrigatória não estiver satisfeita;
- declarar MERGED antes da incorporação real ao AS-IS;
- tratar uma skill, manifesto ou AGENTS como autoridade superior ao Semantic Git;
- carregar indiscriminadamente toda a árvore ou todo o histórico quando não forem necessários.

---

## 28. Regra de ouro

A pergunta permanente é:

> esta informação descreve o que é verdade agora ou descreve uma transformação em andamento?

Se descreve o presente:

```text
AS-IS
→ REQUIREMENTS / DECISIONS / OPERATIONS
```

Se descreve transformação:

```text
CHANGE
```

Se descreve alteração física:

```text
Git Diff
```

Se descreve trabalho futuro:

```text
TODO
```

Se descreve problema, intenção e resultado esperado temporariamente:

```text
PRD
```

Se descreve plano técnico temporário da transformação:

```text
SPEC
```

Se algo descoberto nesses artefatos continuar verdadeiro após a mudança, consolidá-lo no AS-IS permanente apropriado.

---

## 29. Modelo mental final

```text
                         MAIN
                          │
                     AS-IS vigente
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
  REQUIREMENTS        DECISIONS        OPERATIONS
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                  materializações
                          │
                     necessidade
                          ↓
                        CHANGE
                         DRAFT
                           │
                   somente análise e gaps
                           │
                      base_commit
                          │
                   PRD opcional
                          │
                  snapshot inicial
                          │
                   Semantic Diff
                          │
               ADD / MODIFY /
               REMOVE / NONE
                          │
                          ↓
                  validação humana
                          ↓
             approved_semantic_commit
                  + approval_scope
                          ↓
                        APPROVED
                           ↓
                  gate de implementação
                           ↓
                     SPEC opcional
                          ↓
                    TODO opcional
                          ↓
                    IN_PROGRESS
                          ↓
                      execução
                          ↓
                snapshots intermediários
                  quando necessários
                          ↓
                   RECONCILIATION
                          │
               Semantic Diff aprovado
                          ↕
                    Git Diff(s)
                          ↕
                     AS-IS atual
                          ↕
                integridade R / D / O
                          ↕
                integridade referencial
                          ↓
                     RECONCILED
                          ↓
                  promoção de IDs
                 conforme a política
                          ↓
                  PRE-MERGE RECHECK
                           ↓
                autorização explícita de merge
                           ↓
                     snapshot final
                           ↓
                 transação de incorporação
               + arquivamento + MERGED
                           ↓
                   merge commit local
                           ↓
                      novo AS-IS
```

No vínculo com implementação externa:

```text
                 SEMANTIC REPOSITORY
                        │
                .semantic-repo.yaml
                        │
                        ├──────────────► IMPLEMENTATION REPO
                        │                       │
                        ◄──────────── semantic-link.yaml
```

A relação é bidirecional.

A autoridade do mapeamento é assimétrica e permanece no Semantic Repository.

Em termos simples:

```text
AS-IS
= verdade vigente

Semantic Namespace
= contexto conceitual onde conhecimento e mudanças pertencem

namespace:ID
= identidade canônica e inequívoca

REQUIREMENTS
= o que deve ser verdade

DECISIONS
= como e por que escolhemos satisfazer os Requirements

OPERATIONS
= como o estado vigente é operado e mantido

CHANGE
= hipótese de nova verdade no menor escopo suficiente

base_commit
= estado físico de origem da transformação

Semantic Diff
= exatamente o que deixa de ser verdade e o que passa a ser verdade

approved_semantic_commit + approval_scope
= snapshot exato do significado aprovado

Git Diff
= exatamente o que mudou fisicamente

RECONCILIATION
= prova de coerência entre intenção aprovada, execução física,
  referências, R/D/O e AS-IS observado

PRE-MERGE RECHECK
= verificação de que a reconciliação continua válida diante da main atual

Merge
= transformação do TO-BE aprovado em novo AS-IS
```

A divisão de responsabilidades é:

```text
Git
→ garante fatos físicos e temporais

Documentos R/D/O + CHANGE
→ explicitam significado

Semantic Namespace
→ resolve contexto e identidade

IA
→ interpreta intenção, impacto, coerência e conflito

Testes determinísticos
→ garantem fatos e invariantes verificáveis por testes determinísticos

Humano
→ valida decisões materiais de significado
```

---

## 30. Invariantes normativas

1. O Semantic Git 1.5 é autocontido e não depende de uma especificação externa para interpretação normativa.
2. `SEMANTIC_GIT.md` é a fonte normativa completa do protocolo.
3. AS-IS e CHANGE são conceitos distintos.
4. AS-IS contém somente conhecimento semântico vigente.
5. REQUIREMENTS, DECISIONS e OPERATIONS são as dimensões permanentes canônicas do AS-IS.
6. REQUIREMENTS é a maior autoridade semântica permanente.
7. DECISIONS não podem contradizer REQUIREMENTS.
8. OPERATIONS não podem contradizer REQUIREMENTS ou DECISIONS.
9. Toda alteração semântica material posterior à existência de um namespace,
   inclusive em REQUIREMENTS, DECISIONS ou OPERATIONS, deve ser governada por
   CHANGE.
10. CHANGE vive no menor Semantic Namespace suficiente.
11. Identidade canônica é namespace + ID local.
12. R-, D- e O- são prefixos oficiais das entidades permanentes.
13. IDs oficiais R/D/O não são duplicados nem reutilizados dentro do mesmo namespace e tipo, nem renumerados por conveniência.
14. IDs oficiais devem ser alocados de forma exclusiva e atômica dentro do namespace controlador.
15. MODIFY exige preservação razoável de identidade.
16. Quando a identidade muda materialmente, usar REMOVE + ADD.
17. Semantic Diff deve separar R/D/O conforme aplicável.
18. Semantic Diff representa mudança de significado, não mudança física.
19. Semantic Diff e Git Diff são conceitos diferentes.
20. Git Diff pode existir com Semantic Diff = NONE.
21. Aprovação humana referencia conteúdo semântico exato e recuperável por `approved_semantic_commit + approval_scope`.
22. Drift material do contrato aprovado exige nova aprovação.
23. PRD duradouro consolida-se em REQUIREMENTS quando aplicável.
24. SPEC duradoura consolida-se em DECISIONS quando aplicável.
25. Procedimento duradouro surgido em TODO/execução consolida-se em OPERATIONS quando aplicável.
26. Snapshots historicamente relevantes não podem se tornar irrecuperáveis.
27. RECONCILIATION é obrigatória antes da incorporação.
28. RECONCILIATION deve provar coerência entre Semantic Diff aprovado, AS-IS semântico, R/D/O e todas as materializações físicas relevantes.
29. RECONCILED deve ser consequência de conformidade, não simples declaração.
30. RECONCILED não congela `main`.
31. Pre-merge recheck é obrigatório.
32. MERGED somente existe após incorporação efetiva ao AS-IS.
33. Reversão material de CHANGE MERGED exige novo CHANGE.
34. Estrutura semântica não deve ser moldada para reproduzir estrutura física.
35. `.semantic-repo.yaml` é a autoridade compartilhada do vínculo semântico → físico.
36. `semantic-link.yaml` cria o vínculo físico → semântico sem se tornar fonte concorrente de verdade.
37. Configuração local de clones não deve ser versionada.
38. Regras determinísticas devem, sempre que possível, ser testadas automaticamente.
39. Testes semânticos por IA só devem ser usados quando regras determinísticas não forem suficientes.
40. Ambiguidade material com múltiplas interpretações plausíveis deve produzir REVIEW, não decisão arbitrária da IA.
41. A IA deve carregar somente contexto suficiente e expandi-lo progressivamente quando necessário.
42. O AS-IS atual deve permanecer compreensível sem leitura obrigatória do histórico de CHANGEs.
43. Skill, AGENTS, validator, template e manifesto derivado não podem conter regras normativas indispensáveis ausentes de `SEMANTIC_GIT.md`.
44. Os nomes canônicos dos documentos permanentes são `README.md`, `REQUIREMENTS.md`, `DECISIONS.md` e `OPERATIONS.md`.
45. `README.md` é opcional e deve conter somente orientação essencial.
46. Cada arquivo R/D/O deve seguir exatamente a estrutura documental canônica do Semantic Git.
47. Nenhum novo tipo de documento permanente é válido dentro de um Semantic Namespace sem alteração normativa desta especificação.
48. Requirements ancestrais aplicáveis são herdados sem cópia textual para o namespace descendente.
49. Para R/D/O, a unicidade e a não reutilização são determinadas por namespace canônico e por tipo; o mesmo ID curto pode existir em namespaces distintos, inclusive entre ancestral e descendente ou entre irmãos. As regras locais de CHANGE-ID permanecem independentes e inalteradas.
50. Nome, estrutura, tipo documental, item, ID ou referência inválidos produzem `FAIL` estrutural ou referencial.
51. A IA não pode criar convenção alternativa para contornar uma violação do padrão canônico.
52. Todo CHANGE semântico material deve possuir branch exclusiva antes de sua criação ou evolução.
53. Novas branches de CHANGE devem seguir `change/<namespace-key>/<CHANGE-ID>-<slug-curto>` e ser globalmente únicas no repositório.
54. Proposta e análise de gaps permanecem TO-BE até a validação humana.
55. Implementação definitiva somente pode começar após a validação humana do contrato semântico exato.
56. `main` permanece AS-IS até a incorporação do CHANGE.
57. Alteração material antes de `MERGED`, dentro do mesmo escopo, retorna o mesmo CHANGE à `DRAFT`.
58. Novo ciclo pré-merge mantém o mesmo CHANGE-ID, a mesma branch e o mesmo `base_commit`.
59. Novo ciclo pré-merge exige novo snapshot e nova validação humana.
60. Aprovação anterior permanece recuperável no histórico Git.
61. Implementação de novo ciclo pré-merge limita-se ao delta aprovado, com RECONCILIATION completa.
62. Escopo independente ou materialmente ampliado exige novo CHANGE.
63. Toda CHANGE `MERGED` deve estar em `<namespace-dir>/changes/archived/<CHANGE-ID>.md` no namespace controlador.
64. A IA deve executar o arquivamento pós-merge sem solicitar autorização adicional.
65. O arquivamento obrigatório usa `git mv` e preserva conteúdo semântico, identidade e histórico.
66. `MERGED` somente pode ser registrado após o arquivamento pós-merge ser validado.
67. CHANGE `MERGED` em `changes/` ativo ou duplicada entre ativo e arquivado produz `FAIL`.
68. A relocação canônica da CHANGE não exige nova aprovação quando não altera seu significado.
69. `DRAFT` não pode alocar recursos de implementação nem editar arquivos fora da própria CHANGE.
70. Aprovação semântica não autoriza implementação, merge, tag, release ou push por inferência.
71. A `main` local do Semantic Repository governante é o AS-IS oficial.
72. Push é publicação ou replicação e não altera o AS-IS local.
73. Merge exige autorização textual explícita que identifique a identidade canônica da CHANGE, a branch globalmente única de origem e o destino.
74. O gate de merge deve capturar entradas imutáveis e invalidar-se quando qualquer uma mudar.
75. Incorporação, arquivamento e estado `MERGED` devem compor uma única transação local final.
76. Tag, release e push exigem autorizações textuais independentes.
77. Implementação definitiva somente pode ocorrer após aprovação semântica registrada e preflight de implementação.
78. Cada Semantic Namespace controla uma sequência local independente de CHANGE-IDs.
79. CHANGE-ID não pode ser reutilizado no mesmo namespace, mas pode repetir-se em namespaces distintos.
80. A identidade inequívoca de uma CHANGE é `<namespace>:<CHANGE-ID>`.
81. Dependências, aprovações, autorizações e gates de CHANGE usam identidade canônica; ambiguidade bloqueia a operação aplicável.
82. Dependências e ciclos entre CHANGEs são resolvidos por identidade canônica completa, nunca apenas por CHANGE-ID curto.
83. Caminhos ativo e arquivado de CHANGE são relativos ao diretório documental do namespace controlador.
84. A relocação de `approval_scope` é resolvida pela identidade canônica e pelo namespace de origem, nunca por busca global de basename ou ID curto.
85. O namespace codificado na branch é redundância verificável e não fonte de autoridade semântica.
86. CHANGE-IDs e branches anteriores ao Semantic Git 1.4, inclusive a branch desta transformação, permanecem válidos sem migração retroativa obrigatória.
87. A criação inicial manual ou externa ocorre fora do protocolo, sem `CHANGE-INIT` nem CHANGE de inicialização, e seu estado pode ser reconhecido como AS-IS de origem.
88. Se a criação inicial for realizada sob o Semantic Git, ela deve ser governada por um único `CHANGE-INIT`.
89. A ausência de `CHANGE-INIT` não representa criação governada sem `CHANGE-INIT`, não prova ferramenta ou autoria e não exige reconstrução.
90. `CHANGE-INIT` é único por namespace, não consome `CHANGE-001` e segue o fluxo normal de CHANGE.
91. `CHANGE-INIT` pode estar no caminho do namespace alvo mesmo quando ele estiver ausente do AS-IS do `base_commit`; o namespace pai não precisa de CHANGE.
92. Em `CHANGE-INIT`, a ausência de predecessor não deve ser materializada como arquivo, entidade ou baseline vazio; a RECONCILIATION confronta o Semantic Diff aprovado com o primeiro AS-IS adicionado e valida a ausência de alterações ancestrais.

---

## 31. Requisitos de standalone

Uma distribuição só pode declarar conformidade com **Semantic Git 1.5 Standalone** se:

1. possuir uma cópia íntegra desta especificação em `SEMANTIC_GIT.md` ou referência imutável equivalente acessível ao agente e às ferramentas;
2. nenhuma regra necessária para interpretar R/D/O, CHANGE, Semantic Diff, estados, aprovação, reconciliação, IDs, vínculos ou testes depender exclusivamente de outra especificação;
3. qualquer skill ou `AGENTS.md` puder ser removido sem alterar o significado normativo do protocolo;
4. qualquer manifesto ou cache puder ser regenerado a partir das fontes oficiais;
5. a operação semântica puder ser reconstruída a partir de `SEMANTIC_GIT.md`, do Semantic Repository, do Git e das materializações vinculadas.

O objetivo do modo standalone é:

```text
uma especificação normativa
+
contexto carregado sob demanda
+
automações verificáveis
```

sem cadeia obrigatória de herança documental em runtime.

---

# Fim da especificação Semantic Git v1.5 Standalone
