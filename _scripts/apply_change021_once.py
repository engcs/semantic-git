#!/usr/bin/env python3
"""One-shot applicator for approved root:CHANGE-021; removed after successful application."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SECTION_33 = r'''## 33. Índice semântico derivado

O Semantic Git permite materializar um **índice semântico derivado** para reduzir
o custo de descoberta, navegação e carregamento de contexto sem criar uma nova
fonte de verdade.

O índice responde:

> onde está o conhecimento relevante deste escopo e quais relações determinísticas permitem navegar até suas fontes?

Ele é infraestrutura reconstruível, não AS-IS semântico.

```text
R/D/O + CHANGE + _memory + estrutura do namespace
                    ↓
              índice derivado
                    ↓
       descoberta / navegação / contexto
                    ↓
             reabertura da fonte
```

### 33.1. Localização e natureza

Quando materializado, o índice de um Semantic Namespace fica em:

```text
<namespace-dir>/_index/SEMANTIC_INDEX.json
```

Para `root`, `<namespace-dir>` é a raiz do Semantic Repository. Para um namespace
descendente, o diretório `_index/` fica no próprio diretório documental desse
namespace.

`_index/`:

- é auxiliar e derivado;
- não é Semantic Namespace;
- não cria dimensão adicional de R/D/O;
- não participa de herança semântica;
- não possui autoridade normativa;
- pode ser apagado e reconstruído sem perda de conhecimento semântico;
- não deve ser editado manualmente como forma de alterar significado.

A autorização de `_index/SEMANTIC_INDEX.json` nesta seção é uma exceção auxiliar
ao bloqueio de novos tipos documentais da seção 23.3. Ela não cria novo tipo de
documento permanente do AS-IS.

### 33.2. Escopo recursivo

O índice é reproduzível em qualquer Semantic Namespace.

Para um namespace `N`, o escopo do índice é:

```text
N
+
descendentes semânticos de N
+
stubs externos mínimos exigidos por referências explícitas
```

`root` não possui um tipo especial de índice. Ele é apenas o maior escopo e,
por isso, seu índice pode representar toda a árvore semântica do repositório.

Um índice descendente não deve importar indiscriminadamente o conteúdo completo
de ancestrais, irmãos ou outros ramos. Quanto menor o escopo suficiente, menor
deve permanecer o contexto necessário para trabalhar nele.

A existência de índice em um nível não exige que índices sejam materializados em
todos os demais níveis. O mesmo mecanismo deve ser capaz de reconstruí-los sob
demanda.

### 33.3. Representação mínima

A representação canônica derivada desta versão é JSON e deve conter, no mínimo:

```text
schema_version
scope
source_commit
source_fingerprint
nodes
edges
```

`scope` identifica o Semantic Namespace representado e seu caminho documental.
`source_commit` ancora o snapshot Git usado pela geração e
`source_fingerprint` fornece uma impressão determinística das fontes efetivamente
indexadas.

Os tipos iniciais de nó são:

```text
namespace
requirement
decision
operation
change
finding
```

As relações iniciais podem incluir:

```text
contains
parent_namespace
references
satisfies
depends_on
semantic_ref
```

Uma implementação pode acrescentar relação derivada somente quando ela puder ser
provada deterministicamente pela estrutura, identidade, referência explícita ou
outra convenção normativa do Semantic Git. A IA não deve inventar arestas para
preencher o grafo.

### 33.4. Identidade e proveniência

Entidades R/D/O e CHANGE preservam suas identidades canônicas existentes. Nós de
namespace devem preservar a identidade do namespace. Findings podem receber uma
identidade técnica qualificada para indexação, mas isso não transforma `F-*` em
identidade semântica normativa.

Todo nó deve permitir reabrir sua fonte por, no mínimo:

```text
source.path
source.locator
```

O índice pode conter texto resumido ou normalizado para descoberta, mas esse
texto não substitui o documento governado. Para sustentar conclusão semântica
material, a IA ou ferramenta deve reabrir a fonte apontada pelo índice.

### 33.5. Referências externas ao escopo

Quando um nó dentro do escopo referencia explicitamente uma entidade fora dele,
o índice local pode incluir um **stub externo mínimo**.

O stub deve:

- preservar a identidade da entidade referenciada;
- registrar tipo e proveniência suficientes para reabrir a fonte;
- ser marcado explicitamente como externo;
- não provocar expansão transitiva automática do namespace externo;
- não originar novas relações como se seu conteúdo estivesse carregado no escopo local.

Assim, um índice local sabe **onde continuar a navegação** sem carregar toda a
árvore ancestral ou lateral.

### 33.6. Geração determinística e autoridade

O índice deve ser gerado a partir de fontes governadas e estruturalmente válidas.
Quando uma propriedade puder ser obtida por parser, identidade, caminho,
referência ou Git, sua geração deve ser determinística e não depender de
interpretação probabilística da IA.

A autoridade permanece nas fontes:

```text
R/D/O
= verdade semântica vigente

CHANGE
= transformação governada / histórico semântico

_memory
= memória analítica não normativa

_index
= mapa derivado para descoberta

Git
= fatos físicos e temporais
```

Em caso de divergência entre índice e fonte, corrigir ou regenerar o índice. O
índice nunca prevalece sobre a fonte governada.

### 33.7. Progressive disclosure

Quando existir um índice válido e atual, humanos, IAs e ferramentas devem poder
usá-lo como roteador de contexto:

```text
pergunta / tarefa
→ menor escopo suficiente
→ índice desse escopo
→ poucos nós e relações relevantes
→ fontes apontadas
→ expansão seletiva somente quando necessária
```

Não carregar o índice de `root` por padrão quando um índice descendente suficiente
resolver a descoberta. Referências externas ou requisitos ancestrais podem levar
a IA a subir seletivamente de escopo ou abrir diretamente a fonte indicada.

O índice não altera as regras de herança, autoridade ou bootstrap; apenas reduz o
custo de localizar o contexto que essas regras exigem.

### 33.8. Freshness e validação

Uma implementação determinística deve validar, no mínimo:

- versão de schema suportada;
- identidade e caminho do `scope`;
- `source_commit` existente e aplicável;
- `source_fingerprint` bem formado e compatível com as fontes atuais;
- unicidade dos IDs de nós;
- tipos de nó e de relação conhecidos;
- existência de `source.path` e `source.locator` exigidos;
- existência física das fontes apontadas;
- existência de ambos os endpoints de cada edge;
- ausência de edges duplicados;
- coerência entre namespace, identidade e caminho;
- marcação correta de stubs externos;
- ausência de relações originadas de stub externo como se ele estivesse carregado;
- equivalência entre o índice materializado e sua regeneração determinística.

Índice ausente quando solicitado pode ser reconstruído. Índice inválido,
`STALE`, `DRIFT`, referência órfã ou fonte inexistente produz `FAIL` para a
operação que depender dele. A IA não deve preencher a lacuna por adivinhação.

### 33.9. Implementação portátil

A representação primária desta versão permanece um JSON simples. SQLite,
NetworkX, banco de grafos, RDF, embeddings, vector database ou outra camada de
consulta podem existir futuramente como otimização derivada, mas não constituem
autoridade adicional e devem continuar regeneráveis a partir das fontes
governadas e, quando aplicável, do JSON derivado.

O núcleo do índice não deve depender dessas tecnologias para preservar sua
portabilidade e verificabilidade.

### 33.10. Invariantes do índice semântico

São invariantes adicionais:

1. Todo índice pertence a exatamente um escopo de Semantic Namespace.
2. `root` é somente o maior escopo, não um tipo especial de índice.
3. O escopo inclui o namespace escolhido e seus descendentes semânticos.
4. Conteúdo externo ao escopo só é incluído como stub mínimo quando uma referência explícita o exigir.
5. Stub externo não causa expansão transitiva automática nem origina relações locais derivadas de conteúdo não carregado.
6. `_index` não é AS-IS semântico, memória analítica, namespace ou dimensão R/D/O.
7. Todo nó indexado possui proveniência suficiente para reabrir a fonte.
8. Conclusão semântica material deve consultar a fonte, não apenas o índice.
9. O índice deve ser reconstruível deterministicamente e sua remoção não pode causar perda de conhecimento semântico.
10. Índice desatualizado ou estruturalmente inválido não pode ser aceito silenciosamente.
11. O índice deve favorecer o menor escopo suficiente e progressive disclosure.
12. Relações não demonstráveis deterministicamente não devem ser inventadas pela IA.
13. A representação JSON derivada não impede caches ou grafos futuros, mas nenhuma otimização se torna nova fonte de verdade.
14. Não é obrigatório materializar simultaneamente índices de todos os namespaces.
'''


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one patch anchor in {path}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def patch_spec() -> None:
    path = ROOT / "SEMANTIC_GIT.md"
    text = path.read_text(encoding="utf-8")
    if "## 33. Índice semântico derivado" in text:
        return

    publication = '''`_publications/` é reservado para publicações derivadas rastreadas, como
`REFERENCE.md` e seu manifesto. Uma publicação é regenerável e não é fonte de
verdade semântica, mesmo quando for mantida no Git como entregável.
'''
    replace_once(path, publication, publication + '''\n`_index/` é reservado para índices semânticos derivados e reconstruíveis do
namespace em cujo diretório é materializado. Ele não é AS-IS, não cria novo
namespace e não substitui as fontes governadas; suas regras estão na seção 33.
''')

    bootstrap = '''Não carregar indiscriminadamente toda a árvore nem toda a especificação quando o ambiente oferecer acesso seletivo confiável às regras necessárias.
'''
    replace_once(path, bootstrap, '''Quando existir índice semântico válido e atual no menor escopo suficiente, a IA
pode utilizá-lo primeiro para localizar entidades, relações e fontes relevantes,
sem tratá-lo como autoridade e reabrindo a fonte antes de qualquer conclusão
semântica material.

''' + bootstrap)

    invariant = '''116. A criação ou atualização de `_memory/FINDINGS.yaml` durante investigação em `DRAFT` é escrita analítica permitida quando limitada à memória não normativa da seção 32; ela não constitui implementação, não autoriza R/D/O ou materializações físicas e, por si só, não exige CHANGE semântico separado.
'''
    replace_once(path, invariant, invariant + '''117. `_index/SEMANTIC_INDEX.json` é artefato derivado, reconstruível e não normativo do Semantic Namespace em cujo diretório é materializado.
118. O índice pode ser reproduzido em qualquer namespace; `root` é apenas o caso de maior escopo.
119. Um índice contém seu scope e descendentes, sem importar indiscriminadamente ancestrais ou irmãos.
120. Referência explícita fora do escopo pode produzir somente stub externo mínimo e terminal.
121. Todo nó indexado deve preservar proveniência suficiente para reabrir a fonte governada.
122. O índice é roteador de contexto e não pode substituir a fonte em conclusão semântica material.
123. Índice inválido, stale, drifted, com endpoint órfão ou source inexistente não pode ser silenciosamente aceito.
124. Remover o índice não pode causar perda de conhecimento semântico; sua reconstrução determinística deve ser possível a partir das fontes.
''')

    final = '''---\n\n# Fim da especificação Semantic Git v1.5 Standalone'''
    replace_once(path, final, '''---\n\n''' + SECTION_33 + '''\n---\n\n# Fim da especificação Semantic Git v1.5 Standalone''')


def patch_validator() -> None:
    path = ROOT / "_scripts/validate_structure.py"
    text = path.read_text(encoding="utf-8")
    if "INDEX_FILENAME = \"SEMANTIC_INDEX.json\"" in text:
        return

    replace_once(path,
        'FINDING_FIELD_RE = re.compile(r"^    ([a-z][a-z0-9_]*)\\s*:\\s*(.*?)\\s*$")\n',
        'FINDING_FIELD_RE = re.compile(r"^    ([a-z][a-z0-9_]*)\\s*:\\s*(.*?)\\s*$")\n'
        'INDEX_FILENAME = "SEMANTIC_INDEX.json"\n'
        'INDEX_NODE_TYPES = {"namespace", "requirement", "decision", "operation", "change", "finding"}\n'
        'INDEX_EDGE_TYPES = {"contains", "parent_namespace", "references", "satisfies", "depends_on", "semantic_ref"}\n')

    replace_once(path,
        '        self.memory_count = 0\n        self.rdo_ids:',
        '        self.memory_count = 0\n        self.index_count = 0\n        self.rdo_ids:')

    replace_once(path,
        '            if path.name.casefold() in {"_memory", "memory"}:\n                self.validate_memory_directory(path)\n\n        self.validate_local_configuration()\n',
        '            if path.name.casefold() in {"_memory", "memory"}:\n                self.validate_memory_directory(path)\n'
        '            if path.name.casefold() in {"_index", "index"}:\n                self.validate_index_directory(path)\n\n'
        '        self.validate_local_configuration()\n')

    replace_once(path,
        '            if path.name.casefold() == "findings.yaml":\n                if path.name != "FINDINGS.yaml":\n                    self.add("MEMORY_FILENAME", path, "analytical memory must use the exact name FINDINGS.yaml")\n                if path.parent.name != "_memory":\n                    self.add("MEMORY_PATH", path, "FINDINGS.yaml is valid only inside a namespace _memory directory")\n',
        '            if path.name.casefold() == "findings.yaml":\n                if path.name != "FINDINGS.yaml":\n                    self.add("MEMORY_FILENAME", path, "analytical memory must use the exact name FINDINGS.yaml")\n                if path.parent.name != "_memory":\n                    self.add("MEMORY_PATH", path, "FINDINGS.yaml is valid only inside a namespace _memory directory")\n\n'
        '            if path.name.casefold() == INDEX_FILENAME.casefold():\n                if path.name != INDEX_FILENAME:\n                    self.add("INDEX_FILENAME", path, f"semantic index must use the exact name {INDEX_FILENAME}")\n'
        '                if path.parent.name != "_index":\n                    self.add("INDEX_PATH", path, f"{INDEX_FILENAME} is valid only inside a namespace _index directory")\n')

    marker = '    def validate_local_configuration(self) -> None:\n'
    method = '''    def validate_index_directory(self, index_dir: Path) -> None:
        if index_dir.name != "_index":
            self.add("INDEX_DIRECTORY", index_dir, "the semantic index directory must be named exactly _index")

        entries = list(index_dir.iterdir())
        if not entries:
            self.add("INDEX_EMPTY", index_dir, "_index must not exist without SEMANTIC_INDEX.json")
            return
        for entry in entries:
            if entry.is_dir():
                self.add("INDEX_PATH", entry, "_index may contain only SEMANTIC_INDEX.json")
            elif entry.name != INDEX_FILENAME:
                self.add("INDEX_PATH", entry, "_index may contain only the canonical SEMANTIC_INDEX.json file")

        index_file = index_dir / INDEX_FILENAME
        if not index_file.is_file():
            self.add("INDEX_FILE", index_dir, "_index must contain SEMANTIC_INDEX.json")
            return

        self.index_count += 1
        try:
            payload = json.loads(index_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            self.add("INDEX_JSON", index_file, f"semantic index is not valid UTF-8 JSON: {error}")
            return

        if payload.get("schema_version") != 1:
            self.add("INDEX_SCHEMA", index_file, "semantic index schema_version must be 1")
        scope = payload.get("scope")
        if not isinstance(scope, dict) or not scope.get("identity") or not scope.get("path"):
            self.add("INDEX_SCOPE", index_file, "semantic index scope must contain identity and path")
        source_commit = payload.get("source_commit")
        if not isinstance(source_commit, str) or not COMMIT_RE.fullmatch(source_commit):
            self.add("INDEX_SOURCE", index_file, "semantic index source_commit must be a Git commit identifier")
        fingerprint = payload.get("source_fingerprint")
        if not isinstance(fingerprint, str) or re.fullmatch(r"[0-9a-f]{64}", fingerprint) is None:
            self.add("INDEX_SOURCE", index_file, "semantic index source_fingerprint must be a SHA-256 hex string")

        nodes = payload.get("nodes")
        edges = payload.get("edges")
        if not isinstance(nodes, list):
            self.add("INDEX_NODES", index_file, "semantic index nodes must be an array")
            nodes = []
        if not isinstance(edges, list):
            self.add("INDEX_EDGES", index_file, "semantic index edges must be an array")
            edges = []

        ids: set[str] = set()
        node_map: dict[str, dict[str, Any]] = {}
        for node in nodes:
            if not isinstance(node, dict):
                self.add("INDEX_NODES", index_file, "every semantic index node must be an object")
                continue
            node_id = node.get("id")
            if not isinstance(node_id, str) or not node_id:
                self.add("INDEX_NODES", index_file, "every semantic index node must have a non-empty id")
                continue
            if node_id in ids:
                self.add("INDEX_NODE_DUPLICATE", index_file, f"semantic index node id is duplicated: {node_id}")
            ids.add(node_id)
            node_map[node_id] = node
            if node.get("type") not in INDEX_NODE_TYPES:
                self.add("INDEX_NODE_TYPE", index_file, f"semantic index node has unknown type: {node_id}")
            source = node.get("source")
            if not isinstance(source, dict) or not source.get("path") or not source.get("locator"):
                self.add("INDEX_SOURCE", index_file, f"semantic index node lacks source.path/source.locator: {node_id}")
            else:
                source_path = self.root if source["path"] == "." else self.root / str(source["path"])
                if not source_path.exists():
                    self.add("INDEX_SOURCE", index_file, f"semantic index node source does not exist: {source['path']}")
            if node.get("external") not in {None, True}:
                self.add("INDEX_EXTERNAL", index_file, f"external marker must be true when present: {node_id}")

        seen_edges: set[tuple[Any, Any, Any]] = set()
        for relation in edges:
            if not isinstance(relation, dict):
                self.add("INDEX_EDGES", index_file, "every semantic index edge must be an object")
                continue
            key = (relation.get("from"), relation.get("type"), relation.get("to"))
            if key in seen_edges:
                self.add("INDEX_EDGE_DUPLICATE", index_file, f"semantic index edge is duplicated: {key}")
            seen_edges.add(key)
            if relation.get("type") not in INDEX_EDGE_TYPES:
                self.add("INDEX_EDGE_TYPE", index_file, f"semantic index edge has unknown type: {relation.get('type')}")
            if relation.get("from") not in ids:
                self.add("INDEX_ENDPOINT", index_file, f"semantic index edge source does not exist: {relation.get('from')}")
            if relation.get("to") not in ids:
                self.add("INDEX_ENDPOINT", index_file, f"semantic index edge target does not exist: {relation.get('to')}")
            origin = node_map.get(str(relation.get("from")))
            if origin is not None and origin.get("external") is True:
                self.add("INDEX_EXTERNAL", index_file, f"external stub must not originate edges: {relation.get('from')}")

'''
    replace_once(path, marker, method + marker)

    replace_once(path,
        '            "memory_files": self.memory_count,\n            "findings": self.findings,\n',
        '            "memory_files": self.memory_count,\n            "index_files": self.index_count,\n            "findings": self.findings,\n')
    replace_once(path,
        '            f"{self.change_count} CHANGE files and {self.memory_count} memory files"\n',
        '            f"{self.change_count} CHANGE files, {self.memory_count} memory files and "\n'
        '            f"{self.index_count} semantic index files"\n')


def reconcile_change() -> None:
    path = ROOT / "_changes/CHANGE-021.md"
    text = path.read_text(encoding="utf-8")
    if "status: RECONCILED" in text:
        return
    if "status: IN_PROGRESS" not in text:
        raise SystemExit("CHANGE-021 is not IN_PROGRESS")
    path.write_text(text.replace("status: IN_PROGRESS", "status: RECONCILED", 1), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["patch", "reconcile"])
    args = parser.parse_args()
    if args.action == "patch":
        patch_spec()
        patch_validator()
    else:
        reconcile_change()


if __name__ == "__main__":
    main()
