"""Descarga todos los PDFs enlazados desde las páginas rastreadas y genera un índice.

Uso: .venv\\Scripts\\python.exe scraping\\download_pdfs.py
Salida:
  Proveedores/pdfs/<proveedor>/<familia>/<archivo>.pdf   (cada PDF se guarda una sola vez)
  Proveedores/pdfs/pdfs.csv   una fila por producto ↔ PDF (proveedor, familia, producto, tipo, archivo, url…)
Los PDFs ya descargados no se vuelven a bajar. climalit.es se descarga desde Internet Archive.
"""
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "Proveedores" / "raw"
OUT = ROOT / "Proveedores" / "pdfs"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()[:60] or "general"


def index(prov: str) -> list[dict]:
    f = RAW / prov / "_index.json"
    return [e for e in json.loads(f.read_text(encoding="utf-8")) if e.get("ok")] if f.exists() else []


def title_of(prov: str, e: dict) -> str:
    md = (RAW / prov / e["file"]).read_text(encoding="utf-8")
    m = re.search(r"^# (.+)$", md, re.M)
    return (m.group(1) if m else e.get("title", "")).strip(" #")


rows: list[dict] = []  # proveedor, familia, producto, tipo, url, pagina


def add(prov, familia, producto, tipo, url, pagina):
    rows.append(dict(proveedor=prov, familia=familia, producto=producto, tipo=tipo, url=url, pagina=pagina))


# ---- Aluval: series (desde aluval.json) + PDFs de páginas de familia y generales
alu = json.loads((RAW / "aluval.json").read_text(encoding="utf-8"))
seen_alu = set()
for fam in alu.values():
    for s in fam["series"]:
        for p in s["pdfs"]:
            name = unquote(p).lower()
            tipo = "ficha técnica" if "ficha" in name else "catálogo"
            add("aluval", fam["nombre"].strip(), s["nombre"].strip(), tipo, p, s["url"])
            seen_alu.add(p)
for e in index("aluval"):
    for p in e["pdfs"]:
        if p not in seen_alu and "/files/pdf/" in p:
            fam = next((f["nombre"].strip() for k, f in alu.items() if f"/productos/{k}" in e["url"]), "General")
            add("aluval", fam, title_of("aluval", e), "catálogo", p, e["url"])
            seen_alu.add(p)
add("aluval", "General", "Catálogo general", "catálogo", "https://aluval.es/files/pdf/category/catalogo-general.pdf",
    "https://aluval.es/productos")

# ---- Extrugasa: ficha técnica de cada producto (desde extrugasa.json)
ext = json.loads((RAW / "extrugasa.json").read_text(encoding="utf-8"))
for c in ext["categorias"]:
    for p in c["productos"]:
        if p.get("ficha_tecnica"):
            add("extrugasa", c["nombre"], p["nombre"], "ficha técnica", p["ficha_tecnica"], p["url"])

# ---- Gealan, Saint-Gobain, Climalit: PDFs enlazados en cada página
SG_TIPOS = {"catalogo-de-producto": "catálogo", "ficha-tecnica-calumen": "ficha técnica",
            "guias-de-transformacion": "guía de transformación", "guias-y-manuales": "guía / manual",
            "dap": "EPD (declaración ambiental)", "documentacion-sostenibilidad": "sostenibilidad",
            "certificado-saint-gobain-glass": "certificado"}
for prov in ("gealan", "saint-gobain", "climalit"):
    for e in index(prov):
        for p in e["pdfs"]:
            if "/download-documents/" in p:  # duplicado de /documents/ en Saint-Gobain
                continue
            seg = urlparse(p).path.split("/")
            tipo = next((v for k, v in SG_TIPOS.items() if k in seg), "folleto / documento")
            path = urlparse(e["url"]).path.strip("/").split("/")
            familia = {"productos": "Productos", "soluciones": "Soluciones", "system-specifications": "Soluciones",
                       "sistemas": "Sistemas", "innovaciones": "Superficies"}.get(path[1] if len(path) > 1 else "", "General")
            add(prov, familia, title_of(prov, e) or e["url"], tipo, p, e["url"])


# ------------------------------------------------------------------ descarga
def download(url: str, prov: str) -> tuple[bytes | None, str, str]:
    """Devuelve (contenido, nombre de archivo, estado)."""
    real = f"https://web.archive.org/web/20261231235959id_/{url}" if prov == "climalit" else url
    req = urllib.request.Request(quote(real, safe=":/?=&%#()"), headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                cd = r.headers.get("Content-Disposition", "")
                m = re.search(r'filename\*?=(?:UTF-8\'\')?"?([^";]+)', cd)
                name = unquote(m.group(1)) if m else unquote(urlparse(url).path.rsplit("/", 1)[-1])
                if not data.startswith(b"%PDF"):
                    return None, name, f"no es PDF ({r.headers.get('Content-Type')})"
                return data, name, "ok"
        except Exception as ex:
            if getattr(ex, "code", None) in (403, 404, 410):
                return None, "", f"error {ex.code}"
            # 429 = archive.org pide ir más despacio: esperar bastante más antes de reintentar
            time.sleep((60 if getattr(ex, "code", None) == 429 else 3) * (attempt + 1))
            err = repr(ex)[:80]
    return None, "", f"error ({err})"


done: dict[str, dict] = {}  # url -> {archivo, bytes, estado}
manifest = OUT / "_descargas.json"
if manifest.exists():
    done = json.loads(manifest.read_text(encoding="utf-8"))

urls = list(dict.fromkeys((r["proveedor"], r["familia"], r["url"]) for r in rows))
print(f"{len(rows)} filas, {len({u for _, _, u in urls})} PDFs distintos")
for prov, familia, url in urls:
    if url in done and done[url]["estado"] == "ok" and (ROOT / done[url]["archivo"]).exists():
        continue
    if url in done and done[url]["estado"] != "ok" and done[url]["estado"].startswith("error 4"):
        continue
    data, name, estado = download(url, prov)
    rec = {"archivo": "", "bytes": 0, "estado": estado}
    if data:
        name = re.sub(r'[<>:"/\\|?*]+', "_", (name or "documento.pdf").replace("+", " "))
        if not name.lower().endswith(".pdf"):
            name += ".pdf"
        dest = OUT / prov / slug(familia) / name
        if dest.exists() and dest.stat().st_size != len(data):  # mismo nombre, distinto PDF
            dest = dest.with_stem(dest.stem + "_" + str(abs(hash(url)) % 10000))
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        rec.update(archivo=dest.relative_to(ROOT).as_posix(), bytes=len(data))
    done[url] = rec
    print(f"  {'✓' if data else '✗'} {prov:12} {rec['bytes'] // 1024:6} KB  {(rec['archivo'] or url)[-90:]}  {'' if data else estado}", flush=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
    time.sleep(1.5 if prov == "climalit" else 0.4)

with open(OUT / "pdfs.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["proveedor", "familia", "producto", "tipo", "archivo", "kb", "estado", "url", "pagina"])
    w.writeheader()
    for r in rows:
        d = done.get(r["url"], {})
        w.writerow({**r, "archivo": d.get("archivo", ""), "kb": d.get("bytes", 0) // 1024, "estado": d.get("estado", "")})
ok = sum(1 for d in done.values() if d["estado"] == "ok")
mb = sum(d["bytes"] for d in done.values()) / 1e6
print(f"\nPDFs descargados: {ok}/{len(done)} · {mb:.0f} MB · índice: {OUT / 'pdfs.csv'}")
for u, d in done.items():
    if d["estado"] != "ok":
        print("  sin descargar:", d["estado"], u)
