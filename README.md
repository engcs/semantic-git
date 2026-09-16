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

Cristian Sousa — eng.cristiansousa@gmail.com
