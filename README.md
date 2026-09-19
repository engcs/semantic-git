# Semantic Git

Especificação standalone de governança semântica.

A fonte normativa é [`SEMANTIC_GIT.md`](SEMANTIC_GIT.md).

## Publicação de namespace

Cada namespace é publicado separadamente. O valor de `--root` é o diretório do
namespace que será compilado; a ferramenta lê somente `README.md` e os arquivos
`REQUIREMENTS.md`, `DECISIONS.md` e `OPERATIONS.md` diretamente nesse diretório.
Namespaces descendentes não são incorporados automaticamente.

Use o gerador do core:

```powershell
python _scripts\build_publication.py build --root "path\to\namespace" --spec "path\to\SEMANTIC_GIT.md" --pdf --json
python _scripts\build_publication.py status --root "path\to\namespace" --spec "path\to\SEMANTIC_GIT.md" --json
```

`build` valida a estrutura antes de gerar os artefatos em
`<namespace>/_publications/`:

- `PUBLICATION.md`: publicação textual derivada;
- `PUBLICATION.pdf`: apresentação visual derivada;
- `PUBLICATION.manifest.json`: hashes das fontes e dos artefatos.

`PUBLICATION.*` não é fonte semântica e não deve ser editado manualmente. O
comando `status` informa `CURRENT`, `MISSING`, `STALE`, `DRIFT` ou `INVALID`.
Publicar é uma operação derivada e não autoriza aprovação, merge, tag ou push.

## Índice semântico

`_index/SEMANTIC_INDEX.json` é um artefato derivado, reconstruível e não
normativo usado para descoberta, navegação e carregamento progressivo de
contexto. Ele nunca substitui R/D/O, CHANGE, `_memory` nem a fonte original de
uma conclusão material.

O índice é scoped por Semantic Namespace. O índice de `root` enxerga toda a
árvore; um índice descendente contém apenas o namespace escolhido e seus
descendentes, além de stubs externos mínimos quando uma referência precisa
apontar para fora do escopo. Não é necessário manter todos os índices
materializados simultaneamente.

Use o mesmo CLI em qualquer nível:

```powershell
# root
python _scripts\semantic_index.py build --scope .
python _scripts\semantic_index.py validate --scope .
python _scripts\semantic_index.py query --scope . --id "mop:D-001"

# namespace descendente
python _scripts\semantic_index.py build --scope "_applications\mop"
python _scripts\semantic_index.py validate --scope "_applications\mop"
python _scripts\semantic_index.py query --scope "_applications\mop" --type decision
```

`build` e `validate` exigem que a validação estrutural do Semantic Repository
passe. O JSON registra `scope`, `source_commit`, `source_fingerprint`, `nodes` e
`edges`. Se as fontes mudarem, o índice deve ser regenerado; discrepância é
`STALE`/`DRIFT`, não algo que a IA deva adivinhar ou reparar semanticamente.

Cristian Sousa — eng.cristiansousa@gmail.com
