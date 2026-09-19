#!/usr/bin/env python3
"""Build, validate and query deterministic scoped Semantic Git indexes."""
from __future__ import annotations

import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
GENERATOR = {"name": "semantic-git-index", "version": 1}
RDO = {
    "REQUIREMENTS.md": "requirement",
    "DECISIONS.md": "decision",
    "OPERATIONS.md": "operation",
}
PRUNE = {".git", ".opencode", "__pycache__", "_changes", "_memory", "_publications", "_index", "_foundations", "_scripts"}
TRANSPARENT = {"_applications"}
NODE_TYPES = {"namespace", "requirement", "decision", "operation", "change", "finding"}
EDGE_TYPES = {"contains", "parent_namespace", "references", "satisfies", "depends_on", "semantic_ref"}
RDO_ITEM = re.compile(r"^- \*\*([RDO]-\d{3,})\*\* - (.+\S)\s*$")
CANONICAL_REF = re.compile(r"(?<![\w/.-])((?:root|[A-Za-z0-9][\w.-]*(?:/[A-Za-z0-9][\w.-]*)*):(?:[RDO]-\d{3,}|CHANGE-(?:INIT|\d{3,})))")
LOCAL_REF = re.compile(r"(?<![\w:-])([RDO]-\d{3,})(?![\w-])")
CHANGE_ID = re.compile(r"^CHANGE-(?:INIT|\d{3,})$")
COMMIT = re.compile(r"^[0-9a-f]{7,64}$")
FINDING_START = re.compile(r"^  - id:\s*(F-\d{3,})\s*$")
FINDING_FIELD = re.compile(r"^    ([a-z][a-z0-9_]*)\s*:\s*(.*?)\s*$")

class IndexErrorBase(RuntimeError): pass
class StructuralValidationError(IndexErrorBase): pass
class IndexValidationError(IndexErrorBase): pass

def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if check and p.returncode:
        raise IndexErrorBase(p.stderr.strip() or f"git {' '.join(args)} failed")
    return p

def git_root(path: Path) -> Path:
    p = subprocess.run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if p.returncode: raise IndexErrorBase(f"{path} is not inside a Git repository")
    return Path(p.stdout.strip()).resolve()

def rel(root: Path, path: Path) -> str:
    p = path.resolve().relative_to(root.resolve())
    return "." if not p.parts else p.as_posix()

def validate_structure(root: Path) -> None:
    script, spec = root / "_scripts/validate_structure.py", root / "SEMANTIC_GIT.md"
    if not script.is_file() or not spec.is_file():
        raise StructuralValidationError("validate_structure.py and SEMANTIC_GIT.md are required")
    p = subprocess.run([sys.executable, str(script), "--root", str(root), "--spec", str(spec), "--json"], capture_output=True, text=True)
    if p.returncode:
        raise StructuralValidationError(p.stdout.strip() or p.stderr.strip() or "structural validation failed")

def semantic_dirs(root: Path) -> list[Path]:
    root = root.resolve(); anchors = {root}
    for current, dirs, files in os.walk(root, followlinks=False):
        c = Path(current).resolve(); names = set(dirs)
        if any(x in RDO for x in files) or {"_changes", "_memory"} & names: anchors.add(c)
        dirs[:] = [x for x in dirs if x not in PRUNE]
    out = {root}
    for anchor in anchors:
        p = anchor
        while p != root:
            if p.name not in TRANSPARENT: out.add(p)
            p = p.parent
    return sorted(out, key=lambda p: (len(p.parts), p.as_posix()))

def ns_id(root: Path, path: Path) -> str:
    if path.resolve() == root.resolve(): return "root"
    parts = [p for p in path.resolve().relative_to(root.resolve()).parts if p not in TRANSPARENT]
    return "/".join(parts) or "root"

def namespaces(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in semantic_dirs(root):
        ident = ns_id(root, path)
        if ident in out and out[ident]["path"] != path:
            raise IndexErrorBase(f"multiple directories resolve to namespace {ident}")
        out[ident] = {"id": ident, "path": path, "rel": rel(root, path)}
    return out

def parent_ns(ident: str, nss: dict[str, Any]) -> str | None:
    if ident == "root": return None
    parts = ident.split("/")
    for n in range(len(parts)-1, 0, -1):
        x = "/".join(parts[:n])
        if x in nss: return x
    return "root" if "root" in nss else None

def edge(edges: list[dict[str,str]], src: str, typ: str, dst: str) -> None:
    e = {"from": src, "type": typ, "to": dst}
    if e not in edges: edges.append(e)

def read(path: Path) -> str: return path.read_text(encoding="utf-8-sig")

def metadata(lines: list[str]) -> tuple[dict[str,str], dict[str,list[str]]]:
    vals: dict[str,str] = {}; lists: dict[str,list[str]] = {}; active = None
    for line in lines:
        if line.startswith("#"): break
        if not line.strip(): continue
        if line.startswith("  - ") and active:
            lists.setdefault(active, []).append(line[4:].strip()); continue
        m = re.fullmatch(r"([a-z][a-z0-9_]*)\s*:\s*(.*?)\s*", line)
        if not m: active = None; continue
        k,v = m.groups()
        if not v and k in {"approval_scope","depends_on"}: lists.setdefault(k, []); active = k
        else: vals[k] = v; active = None
    return vals, lists

def parse_findings(root: Path, ns: dict[str,Any], nodes: dict[str,Any], edges: list[dict[str,str]]) -> None:
    path = ns["path"] / "_memory/FINDINGS.yaml"
    if not path.is_file(): return
    lines = read(path).splitlines(); starts=[]
    for i,line in enumerate(lines):
        m = FINDING_START.fullmatch(line)
        if m: starts.append((i,m.group(1)))
    for pos,(start,fid) in enumerate(starts):
        end = starts[pos+1][0] if pos+1 < len(starts) else len(lines)
        fields: dict[str,str]={}; refs=[]; active=None
        for line in lines[start+1:end]:
            m=FINDING_FIELD.fullmatch(line)
            if m: active=m.group(1); fields[active]=m.group(2).strip('"\''); continue
            if active=="semantic_refs" and re.fullmatch(r"^      -\s+\S.*$", line): refs.append(line.split("-",1)[1].strip().strip('"\''))
        node_id=f"{ns['id']}:{fid}"
        nodes[node_id]={"id":node_id,"type":"finding","namespace":ns["id"],"status":fields.get("status"),"category":fields.get("category"),"text":fields.get("summary", ""),"source":{"path":rel(root,path),"locator":fid}}
        edge(edges,f"namespace:{ns['id']}","contains",node_id)
        for refid in refs: edge(edges,node_id,"semantic_ref",refid)

def refs(text: str, namespace: str, nodes: dict[str,Any]) -> set[str]:
    out=set(CANONICAL_REF.findall(text))
    for short in LOCAL_REF.findall(text):
        full=f"{namespace}:{short}"
        if full in nodes: out.add(full)
    return out

def catalog(root: Path) -> tuple[dict[str,Any],dict[str,Any],list[dict[str,str]]]:
    nss=namespaces(root); nodes: dict[str,Any]={}; edges=[]
    for ns in nss.values():
        nid=f"namespace:{ns['id']}"; nodes[nid]={"id":nid,"type":"namespace","namespace":ns["id"],"source":{"path":ns["rel"],"locator":ns["id"]}}
    for ident in sorted(nss):
        p=parent_ns(ident,nss)
        if p: edge(edges,f"namespace:{ident}","parent_namespace",f"namespace:{p}")
    for ns in sorted(nss.values(), key=lambda x:x["id"]):
        for fname,typ in RDO.items():
            path=ns["path"] / fname
            if not path.is_file(): continue
            for line in read(path).splitlines():
                m=RDO_ITEM.fullmatch(line)
                if not m: continue
                local,text=m.groups(); nid=f"{ns['id']}:{local}"
                if nid in nodes: raise IndexErrorBase(f"duplicate node identity: {nid}")
                nodes[nid]={"id":nid,"type":typ,"namespace":ns["id"],"text":text,"source":{"path":rel(root,path),"locator":local}}
                edge(edges,f"namespace:{ns['id']}","contains",nid)
        chdir=ns["path"] / "_changes"
        paths=[]
        if chdir.is_dir():
            paths += sorted(chdir.glob("CHANGE-*.md")); arc=chdir/"archived"
            if arc.is_dir(): paths += sorted(arc.glob("CHANGE-*.md"))
        for path in paths:
            vals,lists=metadata(read(path).splitlines()); cid=vals.get("change",path.stem)
            if not CHANGE_ID.fullmatch(cid): continue
            nid=f"{ns['id']}:{cid}"; node={"id":nid,"type":"change","namespace":ns["id"],"status":vals.get("status"),"source":{"path":rel(root,path),"locator":cid}}
            if path.parent.name=="archived": node["archived"]=True
            nodes[nid]=node; edge(edges,f"namespace:{ns['id']}","contains",nid)
            for dep in lists.get("depends_on",[]): edge(edges,nid,"depends_on",dep)
        parse_findings(root,ns,nodes,edges)
    for node in [x for x in nodes.values() if x["type"] in {"requirement","decision","operation"}]:
        all_refs=refs(node.get("text",""),node["namespace"],nodes); sat=set()
        if node["type"]=="decision":
            for m in re.finditer(r"\bAtende\s+(.+?)(?:\.|$)",node.get("text",""),re.I): sat |= refs(m.group(1),node["namespace"],nodes)
        for refid in sorted(all_refs):
            if refid==node["id"]: continue
            target=nodes.get(refid); typ="references"
            if refid in sat and target and target["type"]=="requirement": typ="satisfies"
            elif node["type"]=="operation" and target and target["type"] in {"requirement","decision"}: typ="depends_on"
            edge(edges,node["id"],typ,refid)
    return nss,nodes,edges

def resolve_scope(root: Path, value: str | None, nss: dict[str,Any]) -> dict[str,Any]:
    if value in {None,"",".","root"}: return nss["root"]
    p=Path(value).expanduser(); p=(root/p).resolve() if not p.is_absolute() else p.resolve()
    for ns in nss.values():
        if ns["path"]==p: return ns
    raise IndexErrorBase(f"scope directory is not a Semantic Namespace path: {value}")

def in_scope(ident: str, scope: str) -> bool:
    return scope=="root" or ident==scope or ident.startswith(scope+"/")

def external(node: dict[str,Any]) -> dict[str,Any]:
    out={"id":node["id"],"type":node["type"],"namespace":node.get("namespace"),"source":node["source"],"external":True}
    for k in ("status","category"):
        if node.get(k) is not None: out[k]=node[k]
    return out

def fingerprint(root: Path, paths: list[str]) -> str:
    h=hashlib.sha256()
    for rp in sorted(set(paths)):
        p=root if rp=="." else root/rp
        if p.is_dir(): continue
        if not p.is_file(): raise IndexValidationError(f"indexed source does not exist: {rp}")
        blob=git(root,"hash-object","--",str(p)).stdout.strip()
        h.update(rp.encode()); h.update(b"\0"); h.update(blob.encode("ascii")); h.update(b"\n")
    return h.hexdigest()

def build_index(root: Path, scope_value: str|None=None, *, check_structure: bool=True) -> dict[str,Any]:
    root=root.resolve()
    if check_structure: validate_structure(root)
    nss,all_nodes,all_edges=catalog(root); scope=resolve_scope(root,scope_value,nss)
    selected={nid:dict(n) for nid,n in all_nodes.items() if in_scope(n.get("namespace","root"),scope["id"])}
    selected_edges=[]
    changed=True
    while changed:
        changed=False
        for e in all_edges:
            if e["from"] not in selected or selected[e["from"]].get("external"): continue
            if e["to"] not in all_nodes: raise IndexValidationError(f"unresolved reference from {e['from']} to {e['to']}")
            if e["to"] not in selected: selected[e["to"]]=external(all_nodes[e["to"]]); changed=True
            if e not in selected_edges: selected_edges.append(e)
    selected_edges=[e for e in selected_edges if not selected[e["from"]].get("external")]
    source_paths=[n["source"]["path"] for n in selected.values()]
    return {"schema_version":SCHEMA_VERSION,"generator":GENERATOR,"scope":{"identity":scope["id"],"path":scope["rel"]},"source_commit":git(root,"rev-parse","HEAD").stdout.strip(),"source_fingerprint":fingerprint(root,source_paths),"nodes":sorted(selected.values(),key=lambda x:x["id"]),"edges":sorted(selected_edges,key=lambda x:(x["from"],x["type"],x["to"]))}

def index_path(scope: dict[str,Any]) -> Path: return scope["path"] / "_index/SEMANTIC_INDEX.json"

def source_exists(root: Path, source: dict[str,str]) -> bool:
    rp=source.get("path"); return bool(rp) and (root if rp=="." else root/rp).exists()

def validate_payload(root: Path, payload: dict[str,Any], expected: dict[str,Any]|None=None) -> list[str]:
    err=[]
    if payload.get("schema_version")!=SCHEMA_VERSION: err.append("unsupported schema_version")
    if payload.get("generator")!=GENERATOR: err.append("generator metadata does not match this indexer")
    scope=payload.get("scope")
    if not isinstance(scope,dict) or not scope.get("identity") or not scope.get("path"): err.append("scope must contain identity and path")
    commit=payload.get("source_commit")
    if not isinstance(commit,str) or not COMMIT.fullmatch(commit): err.append("source_commit is missing or invalid")
    elif git(root,"cat-file","-e",f"{commit}^{{commit}}",check=False).returncode: err.append("source_commit does not exist")
    elif git(root,"merge-base","--is-ancestor",commit,"HEAD",check=False).returncode: err.append("source_commit is not an ancestor of HEAD")
    if not re.fullmatch(r"[0-9a-f]{64}",str(payload.get("source_fingerprint",""))): err.append("source_fingerprint is missing or invalid")
    nodes=payload.get("nodes") if isinstance(payload.get("nodes"),list) else []; edges=payload.get("edges") if isinstance(payload.get("edges"),list) else []
    if not isinstance(payload.get("nodes"),list): err.append("nodes must be an array")
    if not isinstance(payload.get("edges"),list): err.append("edges must be an array")
    ids=set(); node_map={}
    for n in nodes:
        if not isinstance(n,dict): err.append("every node must be an object"); continue
        nid=n.get("id")
        if not nid: err.append("every node must have id"); continue
        if nid in ids: err.append(f"duplicate node id: {nid}")
        ids.add(nid); node_map[nid]=n
        if n.get("type") not in NODE_TYPES: err.append(f"unknown node type: {nid}")
        src=n.get("source")
        if not isinstance(src,dict) or not src.get("path") or not src.get("locator"): err.append(f"node {nid} must contain source.path and source.locator")
        elif not source_exists(root,src): err.append(f"node {nid} source does not exist: {src.get('path')}")
        if n.get("external") not in {None,True}: err.append(f"node {nid} external marker must be true")
    seen=set()
    for e in edges:
        if not isinstance(e,dict): err.append("every edge must be an object"); continue
        key=(e.get("from"),e.get("type"),e.get("to"))
        if key in seen: err.append(f"duplicate edge: {key}")
        seen.add(key)
        if e.get("type") not in EDGE_TYPES: err.append(f"unknown edge type: {e.get('type')}")
        if e.get("from") not in ids: err.append(f"edge source does not exist: {e.get('from')}")
        if e.get("to") not in ids: err.append(f"edge target does not exist: {e.get('to')}")
        if e.get("from") in node_map and node_map[e["from"]].get("external"): err.append(f"external stub must not originate edges: {e['from']}")
    if isinstance(scope,dict) and scope.get("identity"):
        if f"namespace:{scope['identity']}" not in ids: err.append("scope namespace node is missing")
        p=root if scope.get("path")=="." else root/str(scope.get("path"))
        if not p.exists(): err.append("scope path does not exist")
    if expected is not None:
        if payload.get("source_fingerprint")!=expected.get("source_fingerprint"): err.append("STALE: source_fingerprint does not match current indexed sources")
        a=dict(payload); b=dict(expected); b["source_commit"]=a.get("source_commit")
        if a!=b: err.append("DRIFT: index content does not match deterministic regeneration")
    return err

def write_index(root: Path, scope_value: str|None=None) -> Path:
    payload=build_index(root,scope_value); nss=namespaces(root); scope=resolve_scope(root,scope_value,nss); path=index_path(scope)
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); return path

def validate_index(root: Path, scope_value: str|None=None) -> tuple[Path,list[str]]:
    validate_structure(root); nss=namespaces(root); scope=resolve_scope(root,scope_value,nss); path=index_path(scope)
    if not path.is_file(): return path,["MISSING: index file does not exist"]
    try: payload=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as e: return path,[f"INVALID: {e}"]
    expected=build_index(root,scope["rel"],check_structure=False)
    return path,validate_payload(root,payload,expected)

def query_index(root: Path, scope_value: str|None, node_id: str|None, text: str|None, node_type: str|None) -> dict[str,Any]:
    path,errors=validate_index(root,scope_value)
    if errors: raise IndexValidationError("; ".join(errors))
    data=json.loads(path.read_text(encoding="utf-8")); matches=data["nodes"]
    if node_id: matches=[n for n in matches if n["id"]==node_id]
    else:
        if node_type: matches=[n for n in matches if n["type"]==node_type]
        if text:
            q=text.casefold(); matches=[n for n in matches if q in n["id"].casefold() or q in str(n.get("text","")).casefold() or q in str(n.get("category","")).casefold()]
    mids={n["id"] for n in matches}; es=[e for e in data["edges"] if e["from"] in mids or e["to"] in mids]; ids=mids|{e["from"] for e in es}|{e["to"] for e in es}
    return {"scope":data["scope"],"matches":matches,"related_nodes":[n for n in data["nodes"] if n["id"] in ids],"edges":es}

def args() -> argparse.Namespace:
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--root",default="."); sub=p.add_subparsers(dest="command",required=True)
    for name in ("build","validate"):
        q=sub.add_parser(name); q.add_argument("--scope",default=".")
    q=sub.add_parser("query"); q.add_argument("--scope",default="."); q.add_argument("--id",dest="node_id"); q.add_argument("--text"); q.add_argument("--type",choices=sorted(NODE_TYPES))
    return p.parse_args()

def main() -> int:
    a=args()
    try:
        root=git_root(Path(a.root).expanduser().resolve())
        if a.command=="build": print(f"BUILT {rel(root,write_index(root,a.scope))}"); return 0
        if a.command=="validate":
            path,errors=validate_index(root,a.scope)
            if errors:
                print(f"FAIL {rel(root,path)}"); [print(f"- {x}") for x in errors]; return 1
            print(f"PASS {rel(root,path)}"); return 0
        print(json.dumps(query_index(root,a.scope,a.node_id,a.text,a.type),ensure_ascii=False,indent=2)); return 0
    except IndexErrorBase as e: print(f"FAIL: {e}",file=sys.stderr); return 1

if __name__=="__main__": sys.exit(main())
