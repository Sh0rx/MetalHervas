"""Extrae categoría -> producto -> ficha de las páginas de Extrugasa (Proveedores/raw/extrugasa.json)."""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAW = Path(__file__).resolve().parent.parent / "Proveedores" / "raw" / "extrugasa"
idx = {e["url"]: e for e in json.loads((RAW / "_index.json").read_text(encoding="utf-8")) if e["ok"]}
PROD = re.compile(r"https://www\.extrugasa\.com/edificacion/([a-z0-9-]+)\)?")
ENSAYOS = ["Permeabilidad al aire", "Estanqueidad al agua", "Resistencia al viento",
           "Transmitancia térmica Uf", "Transmitancia térmica Uw", "Aislamiento acústico Rw (C;Ctr)"]


def main_content(md):
    """Desde el primer H1 (se salta cookies y menús repetidos)."""
    m = re.search(r"^# .+$", md, re.M)
    return md[m.start():] if m else md


def lines(txt):
    return [l.strip() for l in txt.splitlines() if l.strip()]


def producto(url):
    e = idx[url]
    md = main_content((RAW / e["file"]).read_text(encoding="utf-8"))
    ls = lines(md)
    nombre = ls[0].lstrip("# ").strip()
    desc = ls[1] if len(ls) > 1 and not ls[1].startswith(("[", "!", "#", "Descargables")) else ""
    ensayos = {}
    for k in ENSAYOS:
        if k in ls:
            i = ls.index(k)
            ensayos[k] = ls[i + 2] if i + 2 < len(ls) else ""
    car = {}
    m = re.search(r"^## Características técnicas\s*\n(.*?)(?=^## )", md, re.S | re.M)
    if m:
        cur = None
        for l in lines(m.group(1)):
            if l.startswith("* "):
                cur = l[2:].strip()
                car.setdefault(cur, [])
            elif cur and l.rstrip() not in car[cur]:
                car[cur].append(l.rstrip())
    pdf = re.search(r"\[Ficha técnica\]\((https://[^)]+)\)", md)
    return {"nombre": nombre, "url": url, "descripcion": desc, "ensayos": ensayos,
            "caracteristicas": {k: " / ".join(v) for k, v in car.items()},
            "ficha_tecnica": pdf.group(1) if pdf else None}


def categoria(url):
    md = main_content((RAW / idx[url]["file"]).read_text(encoding="utf-8"))
    ls = lines(md)
    nombre = ls[0].lstrip("# ").strip()
    prods = []
    for slug in PROD.findall(md):
        u = f"https://www.extrugasa.com/edificacion/{slug}"
        if u in idx and u not in prods:
            prods.append(u)
    return nombre, prods


out = {"categorias": [], "sin_categoria": [], "acabados": [], "accesorios": []}
asignados = set()
for url in sorted(u for u in idx if "/edificacion-categoria/" in u and "?" not in u):
    nombre, prods = categoria(url)
    out["categorias"].append({"nombre": nombre, "url": url, "productos": [producto(p) for p in prods]})
    asignados.update(prods)
for url in sorted(u for u in idx if re.match(r"https://www\.extrugasa\.com/edificacion/[^/]+$", u)):
    if url not in asignados:
        out["sin_categoria"].append(producto(url))
# La categoría "practicables" pagina por AJAX y el rastreo solo ve la 1ª página:
# las series XP sueltas son todas practicables según su propia descripción.
pract = next(c for c in out["categorias"] if c["url"].endswith("sistema-ventanas-practicables"))
for prod in [x for x in out["sin_categoria"] if "ventana practicable" in x["descripcion"]]:
    pract["productos"].append(prod)
    out["sin_categoria"].remove(prod)
for key, pat in (("acabados", "/acabados/"), ("accesorios", "/accesorios/")):
    for url in sorted(u for u in idx if pat in u):
        ls = lines(main_content((RAW / idx[url]["file"]).read_text(encoding="utf-8")))
        out[key].append({"nombre": ls[0].lstrip("# "), "url": url, "descripcion": ls[1] if len(ls) > 1 else ""})

(RAW.parent / "extrugasa.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for c in out["categorias"]:
    print(f"\n## {c['nombre']} ({len(c['productos'])})")
    for p in c["productos"]:
        print(f"  - {p['nombre']}: {p['descripcion'][:150]} | Uw {p['ensayos'].get('Transmitancia térmica Uw', '-')}")
print("\n## SIN CATEGORÍA:", [p["nombre"] for p in out["sin_categoria"]])
print("## ACABADOS:", [a["nombre"] for a in out["acabados"]])
print("## ACCESORIOS:", [a["nombre"] for a in out["accesorios"]])
