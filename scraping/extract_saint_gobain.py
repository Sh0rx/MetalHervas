"""Extrae los productos y soluciones de Saint-Gobain Glass (+ páginas de Climalit) a Proveedores/raw/saint-gobain.json.

Uso: .venv\\Scripts\\python.exe scraping\\extract_saint_gobain.py
Según la nota del tío, MetalHervas trabaja «todos los modelos» de Climalit / Saint-Gobain.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAW = Path(__file__).resolve().parent.parent / "Proveedores" / "raw"
SG = RAW / "saint-gobain"

GRUPOS = [  # (grupo, función que decide por nombre) — mismo orden que en arbol_productos.md
    ("CLIMALIT ORAÉ® (baja huella de carbono)", lambda n: "ORA" in n),
    ("CLIMALIT® / CLIMALIT PLUS® — vidrio para ventana",
     lambda n: any(k in n for k in ("PLANITHERM", "PLANISTAR", "ECLAZ", "61/29"))),
    ("Control solar para muro cortina / no residencial", lambda n: "COOL-LITE" in n),
    ("Seguridad y acústica", lambda n: "STADIP" in n),
    ("Vidrios especiales", lambda n: any(k in n for k in ("PRIVA", "SAGE", "VISION", "4BIRD"))),
    ("Interiorismo y decoración", lambda n: any(k in n for k in ("DECOR", "MASTER", "PLANILAQUE", "MIRA"))),
]
DOC_TIPOS = {"catalogo-de-producto": "catálogo", "ficha-tecnica-calumen": "ficha técnica",
             "guias-de-transformacion": "guía de transformación", "guias-y-manuales": "guía / manual",
             "dap": "EPD (declaración ambiental)", "documentacion-sostenibilidad": "sostenibilidad",
             "certificado-saint-gobain-glass": "certificado"}
KEYS = ["TL", "RLe", "RLi", "g", "Ug", "selectividad"]


def sections(md: str) -> dict[str, str]:
    out, cur = {}, None
    for line in md.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            cur = m.group(1).strip("* ")
            out[cur] = ""
        elif cur:
            out[cur] += line + "\n"
    return out


def clean(txt: str) -> str:
    txt = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", txt)
    txt = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", txt)
    txt = re.sub(r"\*\*|__", "", txt)
    return re.sub(r"[ \t]+", " ", txt).strip()


def bullets(txt: str) -> list[str]:
    return [clean(l.lstrip(" *-•")) for l in txt.splitlines() if l.strip().startswith(("*", "-", "•")) and clean(l.lstrip(" *-•"))]


def tabla(txt: str) -> list[dict]:
    """Tabla 'Información Técnica': filas de valores por configuración de acristalamiento."""
    filas, config = [], ""
    for line in txt.splitlines():
        if not line.strip().startswith("|") or "---" in line or "Producto" in line:
            continue
        cells = [clean(c) for c in line.strip().strip("|").split("|")]
        cells = [c for c in cells if c]
        if len(cells) == 1:
            config = cells[0]
        elif len(cells) >= 7:
            filas.append({"configuracion": config, "producto": cells[0], **dict(zip(KEYS, cells[1:7]))})
    return filas


def doc_tipo(url: str) -> str:
    return next((v for k, v in DOC_TIPOS.items() if f"/{k}/" in url), "documento")


idx = [e for e in json.loads((SG / "_index.json").read_text(encoding="utf-8")) if e.get("ok")]
productos, soluciones, paginas = [], [], []
for e in idx:
    md = (SG / e["file"]).read_text(encoding="utf-8")
    h1 = re.search(r"^#\s+(.+)$", md, re.M)
    nombre = clean(h1.group(1)) if h1 else e["title"]
    secs = sections(md)
    pdfs = [{"tipo": doc_tipo(p), "url": p} for p in e["pdfs"] if "/download-documents/" not in p]
    desc = clean(secs.get("Descripción", ""))
    if "/productos/" in e["url"]:
        up = nombre.upper()
        grupo = next((g for g, f in GRUPOS if f(up)), "Otros")
        tecnica = next((tabla(v) for k, v in secs.items() if k.startswith("Información Técnica")), [])
        productos.append({
            "nombre": nombre, "url": e["url"], "grupo": grupo, "trabaja_metalhervas": True,
            "descripcion": desc.split("\n")[0] if desc else "",
            "descripcion_completa": desc,
            "aplicaciones": clean(secs.get("Aplicaciones", "")),
            "beneficios": bullets(secs.get("Beneficios", "")),
            "caracteristicas": clean(next((v for k, v in secs.items() if k.startswith("Características")), "")),
            "prestaciones": tecnica,
            "documentos": pdfs,
        })
    elif "/soluciones" in e["url"] or "/system-specifications/" in e["url"]:
        listed = re.findall(r"###\s+\[([^\]]+)\]\((https://www\.saint-gobain-glass\.es/es/productos/[^)]+)\)", md)
        soluciones.append({"nombre": nombre, "url": e["url"], "descripcion": clean(md.split(h1.group(0), 1)[1])[:600] if h1 else "",
                           "productos": [{"nombre": clean(n), "url": u} for n, u in listed], "documentos": pdfs})
    else:
        paginas.append({"nombre": nombre, "url": e["url"], "documentos": pdfs})

# Climalit (copias de Internet Archive de climalit.es)
climalit = []
CL = RAW / "climalit"
if (CL / "_index.json").exists():
    for e in json.loads((CL / "_index.json").read_text(encoding="utf-8")):
        if e.get("ok"):
            climalit.append({"titulo": e["title"], "url": e["url"], "copia_archive_org": e["snapshot"],
                             "fecha_copia": e["fecha_copia"], "archivo_md": f"climalit/{e['file']}",
                             "documentos": [{"tipo": "folleto / documento", "url": p} for p in e["pdfs"]]})

orden = [g for g, _ in GRUPOS] + ["Otros"]
productos.sort(key=lambda p: (orden.index(p["grupo"]), p["nombre"]))
out = {"proveedor": "Saint-Gobain Glass · CLIMALIT®", "web": "https://www.saint-gobain-glass.es/es",
       "alcance_nota": "Climalit / Saint-Gobain: todos los modelos",
       "productos": productos, "soluciones": soluciones, "otras_paginas": paginas, "climalit_es": climalit}
(RAW / "saint-gobain.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for g in orden:
    ps = [p for p in productos if p["grupo"] == g]
    if ps:
        print(f"\n## {g} ({len(ps)})")
        for p in ps:
            print(f"  - {p['nombre']}: {len(p['prestaciones'])} filas técnicas, {len(p['documentos'])} PDFs | {p['descripcion'][:90]}")
print(f"\nsoluciones: {len(soluciones)} · otras páginas: {len(paginas)} · páginas climalit.es: {len(climalit)}")
