"""Genera Proveedores/arbol_productos.md a partir de la plantilla y los JSON extraídos.

Uso: .venv\\Scripts\\python.exe scraping\\build_tree.py
(antes: crawl.py -> extract_aluval.py / extract_extrugasa.py)
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, unquote

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PROV = HERE.parent / "Proveedores"
RAW = PROV / "raw"


def url(u: str) -> str:
    return quote(u, safe=":/()?=&%#")


def cell(s: str) -> str:
    return s.replace("|", "/").replace("\n", " ").strip()


def first_sentence(s: str, n: int = 190) -> str:
    s = s.strip()
    m = re.match(r"(.{40,}?[.;])\s", s + " ")
    s = m.group(1) if m else s
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def ge(v: str) -> str:
    """'0,83 ≥' / '≥0,83' -> '≥ 0,83' (la web los escribe de varias formas)."""
    v = v.replace("W/m²k", "").replace("*", "").strip()
    return f"≥ {v.replace('≥', '').strip()}" if "≥" in v else v or "—"


def clean_ap(a: str) -> str:
    return a.strip(" .-").replace("  ", " ")


# ---------------------------------------------------------------- Aluval
def aluval() -> tuple[str, str]:
    data = json.loads((RAW / "aluval.json").read_text(encoding="utf-8"))
    tree, body = [], []
    for fam in data.values():
        series = fam["series"]
        tree.append(f"│   │   ├── {fam['nombre'].strip()} ({len(series)})")
        tree.append("│   │   │   └── " + ", ".join(s["nombre"].strip() for s in series))
        body.append(f"### {fam['nombre'].strip()}\n")
        if fam.get("descripcion"):
            body.append(f"{first_sentence(fam['descripcion'], 260)} [Web]({url(fam['url'])})\n")
        body.append("| Serie | Características principales | Aperturas | Documentos |")
        body.append("|---|---|---|---|")
        for s in series:
            car = " · ".join(cell(c.rstrip(".")) for c in s["caracteristicas"][:3]) or "—"
            ap = ", ".join(clean_ap(a) for a in s["aperturas"] if not a.startswith(("!", "Buscar"))) or "—"
            docs = []
            for p in s["pdfs"]:
                name = unquote(p.rsplit("/", 1)[-1]).rsplit(".", 1)[0]
                label = "Ficha técnica" if "ficha" in name.lower() else name.strip()
                docs.append(f"[{label}]({url(p)})")
            body.append(f"| [{s['nombre'].strip()}]({url(s['url'])}) | {car} | {cell(ap)} | {' · '.join(docs) or '—'} |")
        body.append("")
    return "\n".join(tree), "\n".join(body)


# ------------------------------------------------------------- Extrugasa
def extrugasa() -> tuple[str, str]:
    data = json.loads((RAW / "extrugasa.json").read_text(encoding="utf-8"))
    tree, body = [], []
    for cat in data["categorias"]:
        prods = cat["productos"]
        tree.append(f"│       ├── {cat['nombre']} ({len(prods)})")
        tree.append("│       │   └── " + ", ".join(p["nombre"] for p in prods))
        body.append(f"### {cat['nombre']}\n")
        tecnica = any(p["ensayos"] for p in prods)
        if tecnica:
            body.append("| Serie | Descripción | Uf (W/m²K) | Uw (W/m²K) | Acústica Rw | Aire / Agua / Viento | Ficha |")
            body.append("|---|---|---|---|---|---|---|")
        else:
            body.append("| Producto | Descripción | Ficha |")
            body.append("|---|---|---|")
        for p in prods:
            e = p["ensayos"]
            name = f"[{p['nombre']}]({url(p['url'])})"
            desc = cell(first_sentence(p["descripcion"])) or "—"
            ficha = f"[PDF]({p['ficha_tecnica']})" if p.get("ficha_tecnica") else "—"
            if tecnica:
                uf = cell(ge(e.get("Transmitancia térmica Uf", "")))
                uw = cell(ge(e.get("Transmitancia térmica Uw", "")))
                rw = cell(e.get("Aislamiento acústico Rw (C;Ctr)", "—"))
                aav = " / ".join(e.get(k, "—") for k in ("Permeabilidad al aire", "Estanqueidad al agua", "Resistencia al viento"))
                body.append(f"| {name} | {desc} | {uf} | {uw} | {rw} dB | {cell(aav)} | {ficha} |".replace("— dB", "—"))
            else:
                body.append(f"| {name} | {desc} | {ficha} |")
        body.append("")
    tree.append(f"│       ├── Acabados ({len(data['acabados'])})")
    tree.append("│       │   └── " + ", ".join(a["nombre"] for a in data["acabados"]))
    tree.append(f"│       └── Accesorios ({len(data['accesorios'])})")
    tree.append("│           └── " + ", ".join(a["nombre"] for a in data["accesorios"]))
    body.append("### Acabados\n")
    body += [f"- [{a['nombre']}]({url(a['url'])})" for a in data["acabados"]]
    body.append("\n### Accesorios (manillas)\n")
    body += [f"- [{a['nombre']}]({url(a['url'])})" for a in data["accesorios"]]
    body.append("")
    return "\n".join(tree), "\n".join(body)


# ------------------------------------------------------- PDFs descargados
MANIFEST = PROV / "pdfs" / "_descargas.json"
DESCARGAS = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}


def local(u: str) -> str:
    """Enlace relativo (desde Proveedores/) a la copia descargada, o '—'."""
    d = DESCARGAS.get(u, {})
    if d.get("estado") != "ok":
        return "—"
    rel = d["archivo"].removeprefix("Proveedores/")
    return f"[PDF local]({quote(rel)})"


def resumen_pdfs() -> str:
    import csv
    f = PROV / "pdfs" / "pdfs.csv"
    if not f.exists():
        return ""
    rows = list(csv.DictReader(f.open(encoding="utf-8-sig")))
    out = ["| Proveedor | PDFs distintos | Descargados | Tamaño | Sin descargar |", "|---|---|---|---|---|"]
    for prov in dict.fromkeys(r["proveedor"] for r in rows):
        urls = {r["url"] for r in rows if r["proveedor"] == prov}
        ok = [u for u in urls if DESCARGAS.get(u, {}).get("estado") == "ok"]
        mb = sum(DESCARGAS[u]["bytes"] for u in ok) / 1e6
        bad = [f"[{unquote(u.rsplit('/', 1)[-1].split('?')[0])}]({url(u)}) ({DESCARGAS.get(u, {}).get('estado', 'pendiente')})"
               for u in urls if u not in ok]
        out.append(f"| {prov} | {len(urls)} | {len(ok)} | {mb:.0f} MB | {'<br>'.join(bad) or '—'} |")
    return "**PDFs descargados**\n\n" + "\n".join(out)


def climalit_paginas() -> str:
    f = RAW / "climalit" / "_index.json"
    if not f.exists():
        return ""
    idx = [e for e in json.loads(f.read_text(encoding="utf-8")) if e.get("ok")]
    pdfs = sorted({p for e in idx for p in e["pdfs"]})
    out = [f"**Páginas recuperadas de climalit.es** ({len(idx)}, texto en `raw/climalit/`):",
           "", " · ".join(f"[{cell(e['title'].split('|')[0].split(' - ')[0]) or e['url']}]({url(e['snapshot'])})"
                          for e in idx), "", "**PDFs de climalit.es**", ""]
    out += [f"- [{unquote(p.rsplit('/', 1)[-1])}](https://web.archive.org/web/2026/{url(p)}) · {local(p)}" for p in pdfs]
    return "\n".join(out)


def docs_sg() -> str:
    f = RAW / "saint-gobain.json"
    if not f.exists():
        return ""
    data = json.loads(f.read_text(encoding="utf-8"))
    out = ["| Producto | Grupo | Documento | Local |", "|---|---|---|---|"]
    for p in data["productos"]:
        if not p["documentos"]:
            out.append(f"| [{cell(p['nombre'])}]({url(p['url'])}) | {p['grupo']} | sin PDFs en la web | — |")
        for k, d in enumerate(p["documentos"]):
            name = cell(f"[{p['nombre']}]({url(p['url'])})") if k == 0 else "″"
            label = f"{d['tipo']}: {unquote(d['url'].rsplit('/', 1)[-1])}"
            out.append(f"| {name} | {p['grupo'] if k == 0 else ''} | [{cell(label)}]({url(d['url'])}) | {local(d['url'])} |")
    docs_sol = [(s, d) for s in data["soluciones"] for d in s["documentos"]]
    if docs_sol:
        out += ["", "Otros documentos (páginas de soluciones):", ""]
        out += [f"- [{unquote(d['url'].rsplit('/', 1)[-1])}]({url(d['url'])}) ({cell(s['nombre'])}) · {local(d['url'])}"
                for s, d in docs_sol]
    return "\n".join(out)


tpl = (HERE / "plantilla_arbol.md").read_text(encoding="utf-8")
a_tree, a_body = aluval()
e_tree, e_body = extrugasa()
doc = (tpl.replace("{{ARBOL_ALUVAL}}", a_tree).replace("{{ALUVAL}}", a_body)
          .replace("{{ARBOL_EXTRUGASA}}", e_tree).replace("{{EXTRUGASA}}", e_body)
          .replace("{{RESUMEN_PDFS}}", resumen_pdfs()).replace("{{CLIMALIT_PAGINAS}}", climalit_paginas())
          .replace("{{DOCS_SG}}", docs_sg()))
assert "{{" not in doc, "queda algún hueco de la plantilla sin rellenar"
(PROV / "arbol_productos.md").write_text(doc, encoding="utf-8")
print("OK ->", PROV / "arbol_productos.md", len(doc), "caracteres")
