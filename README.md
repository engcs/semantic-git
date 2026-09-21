# Semantic Git

Especificação standalone de governança semântica.

A fonte normativa é [`SEMANTIC_GIT.md`](SEMANTIC_GIT.md).

## CLI canônica

O Semantic Git possui um único ponto de entrada público:

```powershell
python _scripts\semantic_git.py <capacidade> ...
```

Os demais scripts em `_scripts/` são implementação interna. A interface pública
não garante compatibilidade com a execução direta desses scripts.

### Regra de localização

O repositório é descoberto automaticamente a partir do diretório atual.
Normalmente não é necessário informar onde está o Semantic Repository.

```text
onde estou?
→ Semantic Git descobre o repositório automaticamente

qual domínio quero operar?
→ --namespace

quero operar outro Semantic Repository?
→ --root
```

`--root` é somente um override opcional e deve apontar para a raiz do Semantic
Repository. `--namespace` identifica o Semantic Namespace alvo. Se
`--namespace` for omitido, o alvo é o namespace `root`.

Exemplos:

```powershell
# validar o Semantic Repository atual
python _scripts\semantic_git.py validate

# operar o namespace root
python _scripts\semantic_git.py index build

# operar um namespace descendente
python _scripts\semantic_git.py index build --namespace "_applications\mop"

# operar explicitamente outro Semantic Repository
python _scripts\semantic_git.py --root "D:\repos\outro-semantic-repo" index build --namespace "_applications\mop"
```

## Mapa de capacidades

O catálogo legível por humano ou IA pode ser consultado diretamente:

```powershell
python _scripts\semantic_git.py capabilities
python _scripts\semantic_git.py capabilities --json
```

Rotas atuais:

```text
semantic-git://
├── validate/structure
├── publication/{build,status}
├── index/{build,validate,query}
├── compiled/{build,validate,publication}
└── skills/{extraction,reconstruction,conceptual-review,mathematical-review,memory}
```

## Validação estrutural

```powershell
python _scripts\semantic_git.py validate
python _scripts\semantic_git.py validate --json
```

A validação opera sobre o Semantic Repository inteiro.

## Publicação de namespace

Cada namespace é publicado separadamente. O publicador lê somente `README.md`
e os arquivos `REQUIREMENTS.md`, `DECISIONS.md` e `OPERATIONS.md` diretamente no
namespace selecionado. Namespaces descendentes não são incorporados
automaticamente.

```powershell
# namespace root
python _scripts\semantic_git.py publication build
python _scripts\semantic_git.py publication status

# namespace específico
python _scripts\semantic_git.py publication build --namespace "_applications\mop" --pdf
python _scripts\semantic_git.py publication status --namespace "_applications\mop" --json
```

`build` gera em `<namespace>/_publications/`:

- `PUBLICATION.md`;
- `PUBLICATION.manifest.json`;
- `PUBLICATION.pdf`, quando `--pdf` for solicitado.

`PUBLICATION.*` é derivado e não deve ser editado manualmente. `status` informa
`CURRENT`, `MISSING`, `STALE`, `DRIFT` ou `INVALID`.

## Índice semântico

`_index/SEMANTIC_INDEX.json` é derivado, reconstruível e não normativo. É usado
para descoberta, navegação e carregamento progressivo de contexto.

```powershell
python _scripts\semantic_git.py index build
python _scripts\semantic_git.py index validate
python _scripts\semantic_git.py index query --id "mop:D-001"

python _scripts\semantic_git.py index build --namespace "_applications\mop"
python _scripts\semantic_git.py index query --namespace "_applications\mop" --type decision
```

## Compiled Semantic Context

`compiled.ai.md` concentra deterministicamente o conhecimento efetivo de um
namespace para consumo por IA e outras projeções, sem substituir R/D/O como
fonte governada.

```powershell
python _scripts\semantic_git.py compiled build --namespace "_applications\mop"
python _scripts\semantic_git.py compiled validate --namespace "_applications\mop"
python _scripts\semantic_git.py compiled publication --namespace "_applications\mop"
```

Sem `--namespace`, esses comandos operam sobre o namespace `root`.

## Skills

As capacidades agênticas atuais ficam em `.opencode/skills/`:

- `semantic-extraction` — conhecimento humano já expresso → candidato R/D/O;
- `semantic-reconstruction` — implementação existente → significado de negócio;
- `semantic-conceptual-review` — revisão conceitual sênior de R/D/O candidato;
- `semantic-mathematical-review` — análise de regras quantitativas e gaps matemáticos;
- `semantic-memory` — gestão de `_memory/FINDINGS.yaml` sem criar autoridade normativa.

As skills são capacidades cognitivas; os comandos da CLI são capacidades
determinísticas.

Cristian Sousa — eng.cristiansousa@gmail.com
