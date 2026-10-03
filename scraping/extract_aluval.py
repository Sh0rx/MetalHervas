"""Extrae familia -> serie -> ficha de las páginas de Aluval rastreadas (Proveedores/raw/aluval.json)."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAW = Path(__file__).resolve().parent.parent / "Proveedores" / "raw" / "aluval"
idx = json.loads((RAW / "_index.json").read_text(encoding="utf-8"))


def ficha(md):
    """Bloque plegable 'Características técnicas' -> {SUBAPARTADO: [líneas]}."""
    m = re.search(r"^### Características técnicas\s*\n(.*?)(?=^### |\Z)", md, re.S | re.M)
    secs, cur = {}, "DESCRIPCIÓN"
    for l in (m.group(1) if m else "").splitlines():
        l = l.strip()
        if not l or l in ("Ocultar contenido", "Mostrar contenido"):
            continue
        if l.startswith("## "):
            cur = l[3:].strip().upper()
            continue
        secs.setdefault(cur, []).append(l.lstrip("-*· ").strip())
    return secs


def descripcion(md, h1):
    body = md.split(f"# {h1}", 1)[1]
    for l in body.splitlines():
        l = l.strip()
        if len(l) > 80 and not l.startswith(("*", "[", "!", "#")):
            return l
    return ""


out = {}
for e in idx:
    m = re.match(r"https://aluval\.es/productos/([^/]+)(?:/([^/]+))?$", e["url"])
    if not m or not e["ok"]:
        continue
    md = (RAW / e["file"]).read_text(encoding="utf-8")
    h1 = re.search(r"^# (.+)$", md, re.M).group(1).strip()
    fam, serie = m.groups()
    d = out.setdefault(fam, {"series": []})
    if serie is None:
        d.update(nombre=h1, url=e["url"], descripcion=descripcion(md, h1))
    else:
        f = ficha(md)
        d["series"].append({
            "nombre": h1,
            "url": e["url"],
            "caracteristicas": f.get("CARACTERÍSTICAS TÉCNICAS") or f.get("DESCRIPCIÓN", []),
            "aperturas": f.get("APERTURAS POSIBLES", []),
            "ficha": f,
            "pdfs": [p for p in e["pdfs"] if "/files/pdf/" in p],
        })

(RAW.parent / "aluval.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for d in out.values():
    print(f"\n## {d.get('nombre')} — {d.get('descripcion', '')[:160]}")
    for s in d["series"]:
        print(f"  - {s['nombre']}: {' | '.join(s['caracteristicas'][:3])[:220]} || AP: {', '.join(s['aperturas'])[:100]} || secs {list(s['ficha'])}")
