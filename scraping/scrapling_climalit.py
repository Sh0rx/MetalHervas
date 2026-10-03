"""Completa climalit.es con Scrapling: sitemap en vivo + copias de Internet Archive.

La web en vivo (www.climalit.es) responde 403 "Verifying your browser" (comprobación antibots de Cloudflare)
a cualquier petición automatizada; no se elude. Lo único público es /sitemap.xml, que se usa como lista
completa de URLs. Para cada URL que aún no está en Proveedores/raw/climalit/ se descarga la copia más
reciente de Internet Archive con el Fetcher de Scrapling y se extrae el contenido con sus selectores.

Uso: .venv\\Scripts\\python.exe scraping\\scrapling_climalit.py
Salida: Proveedores/raw/climalit/scrapling/<seccion>/<slug>.md + _index.json
"""
import json
import re
import sys
import time
from pathlib import Path

from markdownify import markdownify
from scrapling.fetchers import Fetcher
from scrapling.parser import Selector

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "Proveedores" / "raw" / "climalit"
OUT = RAW / "scrapling"
SITEMAP = "https://www.climalit.es/sitemap.xml"
SKIP = re.compile(r"/(cookies|aviso-legal|politica-de-privacidad|search-page)$")
DELAY = 2.0  # archive.org devuelve 429 enseguida: ritmo lento


def path_of(url: str) -> str:
    return re.sub(r"^https?://(www\.)?climalit\.es", "", url).rstrip("/") or "/"


def already_have() -> set[str]:
    """Rutas ya recuperadas por fetch_climalit_archive.py."""
    idx = json.loads((RAW / "_index.json").read_text(encoding="utf-8"))
    return {path_of(e["url"]) for e in idx if e.get("ok")}


def archived_paths() -> set[str]:
    """Una sola consulta al índice CDX: rutas de climalit.es con copia HTML válida."""
    cdx = ("https://web.archive.org/cdx/search/cdx?url=climalit.es/*&filter=statuscode:200"
           "&filter=mimetype:text/html&collapse=urlkey&fl=original")
    page = Fetcher.get(cdx, timeout=120, stealthy_headers=False)
    return {path_of(u.split("?")[0]).lower() for u in page.body.decode("utf-8", "replace").split()}


def fetch_archived(path: str):
    """Copia más reciente en Internet Archive (respuesta Scrapling) o None si no está archivada."""
    url = f"https://web.archive.org/web/20261231235959id_/https://climalit.es{path}"
    for attempt in range(4):
        page = Fetcher.get(url, timeout=60, stealthy_headers=False)
        if page.status == 200:
            try:
                page.get_all_text()
                return page
            except UnicodeDecodeError:  # copia con bytes mal codificados: se re-parsea sustituyéndolos
                fixed = Selector(page.body.decode("utf-8", "replace"), url=page.url)
                fixed.status = 200
                return fixed
        if page.status == 404:
            return None
        time.sleep(15 * (attempt + 1))  # 429 / 5xx
    return None


def to_markdown(page) -> str:
    # WordPress (copias antiguas) o Drupal (web actual): primer contenedor de contenido que exista
    for sel in ["article", "main", ".entry-content", "#content", ".site-content", "body"]:
        node = page.css(sel).first
        if node is not None and len(node.get_all_text(strip=True)) > 200:
            break
    html = re.sub(r"<(script|style|noscript|nav|header|footer|form)\b.*?</\1>", "", node.html_content, flags=re.S | re.I)
    md = markdownify(html, heading_style="ATX", strip=["img"])
    return re.sub(r"\n{3,}", "\n\n", md).strip()


def main():
    sm = Fetcher.get(SITEMAP, timeout=30)
    (ROOT / "scraping" / "sitemaps" / "climalit_sitemap_live.xml").write_text(sm.html_content, encoding="utf-8")
    paths = [path_of(u) for u in re.findall(r"<loc>([^<]+)</loc>", sm.html_content)]
    have = already_have()
    todo = [p for p in dict.fromkeys(paths) if p not in have and not SKIP.search(p)]
    print(f"sitemap: {len(paths)} URLs, ya recuperadas {len(paths) - len(todo)}, pendientes {len(todo)}", flush=True)

    archived = archived_paths()
    old_paths = {a.split("/")[-1]: a for a in sorted(archived) if re.match(r"/20\d\d/\d\d/\d\d/", a)}
    index = []
    for i, p in enumerate(todo, 1):
        section = p.strip("/").split("/")[0] if p.count("/") > 1 else "paginas"
        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", p.strip("/").split("/")[-1])[:150]
        dest = OUT / section / f"{slug}.md"
        entry = {"url": f"https://www.climalit.es{p}", "seccion": section}
        if dest.exists():
            index.append({**entry, "ok": True, "file": str(dest.relative_to(RAW)).replace("\\", "/"), "cache": True})
            continue
        # la web nueva movió las noticias de /AAAA/MM/DD/<slug>/ (WordPress) a /news/<slug>
        # el índice CDX no es completo: si no aparece ni con la ruta antigua, se pide igualmente la ruta nueva
        src = p if p.lower() in archived else old_paths.get(p.rstrip("/").split("/")[-1].lower(), p)
        page = None
        if src:
            page = fetch_archived(src)
            time.sleep(DELAY)
        if page is None:
            print(f"  [{i}/{len(todo)}] ✗ sin copia: {p}", flush=True)
            index.append({**entry, "ok": False})
            continue
        snap = page.url
        ts = (re.search(r"/web/(\d{14})", snap) or [None, ""])[1]
        title = (page.css("title::text").get() or "").strip()
        date = page.css('meta[property="article:published_time"]::attr(content)').get() or page.css("time::attr(datetime)").get() or ""
        pdfs = sorted({h for h in page.css("a::attr(href)").getall() if h.lower().endswith(".pdf")})
        md = to_markdown(page)
        header = (f"<!-- url: {entry['url']} -->\n<!-- title: {title} -->\n<!-- publicado: {date} -->\n"
                  f"<!-- archivo: {snap} ({ts[:4]}-{ts[4:6]}-{ts[6:8]}) -->\n")
        if pdfs:
            header += "<!-- pdfs:\n" + "\n".join(pdfs) + "\n-->\n"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(header + "\n" + md, encoding="utf-8")
        index.append({**entry, "ok": True, "title": title, "publicado": date, "file": str(dest.relative_to(RAW)).replace("\\", "/"),
                      "chars": len(md), "pdfs": pdfs, "snapshot": snap, "fecha_copia": ts[:8]})
        print(f"  [{i}/{len(todo)}] ✓ {p} ({len(md)} chars, copia {ts[:8]})", flush=True)

    (OUT / "_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"terminado: {sum(e['ok'] for e in index)}/{len(index)} páginas -> {OUT}")


if __name__ == "__main__":
    main()
