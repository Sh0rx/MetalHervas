"""Recupera climalit.es desde Internet Archive (Wayback Machine).

climalit.es tiene una comprobación antibots de Cloudflare que no se debe eludir; Internet Archive guarda
copias públicas de la web, así que se usa la copia más reciente de cada página. Cada .md lleva en la
cabecera la URL original, la copia usada y su fecha.

Uso: .venv\\Scripts\\python.exe scraping\\fetch_climalit_archive.py
Salida: Proveedores/raw/climalit/<slug>.md + _index.json (mismo formato que crawl.py)
"""
import asyncio
import json
import re
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urldefrag

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Proveedores" / "raw" / "climalit"
UA = "Mozilla/5.0 (MetalHervas catalog research; contacto: propietario del proyecto)"

# Páginas del menú de la copia de mayo de 2026 relacionadas con producto
SEEDS = [
    "https://climalit.es/", "https://climalit.es/productos/", "https://climalit.es/climalit-plus/",
    "https://climalit.es/descubre-climalit-plus/", "https://climalit.es/orae/", "https://climalit.es/ecologico/",
    "https://climalit.es/soluciones-vivienda-tipo/", "https://climalit.es/preguntas-frecuentes/",
    "https://climalit.es/huella-de-carbono/", "https://climalit.es/compromiso-climalit/",
    "https://climalit.es/climalit-recicla/", "https://climalit.es/cambia-tus-ventanas/",
    "https://climalit.es/desarrollo-sostenible/", "https://climalit.es/fabricantes/",
    "https://climalit.es/instaladores/",
]
EXCLUDE = re.compile(r"/(blog|actualidad|eventos?|feed|wp-|tienda|carrito|product|producto-tag|user|login|registro|"
                     r"team|node|comments|politica|aviso-legal|cookies|mi-cuenta|gestor|zona-privada|search|"
                     r"climalizate|sostenibilidad/registro|xmlrpc|forms)", re.I)
MAX_DEPTH, MAX_PAGES = 2, 80


def norm(u: str) -> str:
    u = urldefrag(u)[0].split("?")[0]
    u = re.sub(r"^https?://(www\.)?climalit\.es", "https://climalit.es", u)
    return u if u.endswith("/") or "." in u.rsplit("/", 1)[-1] else u + "/"


def fetch(url: str) -> tuple[str, str] | None:
    """Devuelve (html original, url de la copia) de la copia más reciente, o None."""
    req = urllib.request.Request(f"https://web.archive.org/web/20261231235959id_/{url}", headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace"), r.geturl()
        except Exception as e:  # 404 = no archivada; otros: reintento
            if getattr(e, "code", None) == 404:
                return None
            time.sleep(5 * (attempt + 1))
    return None


def slugify(url: str) -> str:
    s = url.replace("https://climalit.es", "").strip("/") or "home"
    return re.sub(r"[^A-Za-z0-9._-]+", "_", s)[:150]


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    seen, index = set(), []
    frontier = [norm(u) for u in SEEDS]
    cfg = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, excluded_tags=["script", "style", "noscript", "header", "footer", "nav"], verbose=False)
    async with AsyncWebCrawler(config=BrowserConfig(headless=True, verbose=False)) as crawler:
        for depth in range(MAX_DEPTH + 1):
            nxt = []
            for url in frontier:
                if url in seen or len(seen) >= MAX_PAGES:
                    continue
                seen.add(url)
                cache = OUT / "_html" / f"{slugify(url)}.html"
                if cache.exists():  # copia ya descargada: no se vuelve a pedir a archive.org
                    first, html_c = cache.read_text(encoding="utf-8").split("\n", 1)
                    got = (html_c, first[5:-4])  # primera línea: <!-- url de la copia -->
                else:
                    got = fetch(url)
                    time.sleep(1.5)  # ritmo amable con archive.org
                    if got:
                        cache.parent.mkdir(parents=True, exist_ok=True)
                        cache.write_text(f"<!-- {got[1]} -->\n{got[0]}", encoding="utf-8")
                if not got:
                    print(f"  ✗ sin copia: {url}", flush=True)
                    index.append({"url": url, "ok": False})
                    continue
                html, snap = got
                ts = re.search(r"/web/(\d{14})", snap)
                ts = ts.group(1) if ts else ""
                hrefs = {norm(urljoin(url, h)) for h in re.findall(r'href=["\']([^"\'#]+)', html)}
                pdfs = sorted({urldefrag(urljoin(url, h))[0] for h in re.findall(r'href=["\']([^"\']+\.pdf)', html, re.I)})
                # rutas relativas -> absolutas (si no, el conversor las resuelve contra el HTML entero)
                html_abs = re.sub(r"""(src|href)=(["'])(?!https?:|data:|mailto:|tel:|#|javascript:)/?""",
                                  lambda m: f"{m.group(1)}={m.group(2)}https://climalit.es/", html)
                r = await crawler.arun(url="raw:" + html_abs, config=cfg)
                md = r.markdown.raw_markdown if r.success else ""
                title = (re.search(r"<title>([^<]*)", html) or [None, ""])[1].strip()
                slug = slugify(url)
                header = f"<!-- url: {url} -->\n<!-- title: {title} -->\n<!-- archivo: {snap} ({ts[:4]}-{ts[4:6]}-{ts[6:8]}) -->\n"
                if pdfs:
                    header += "<!-- pdfs:\n" + "\n".join(pdfs) + "\n-->\n"
                (OUT / f"{slug}.md").write_text(header + "\n" + md, encoding="utf-8")
                index.append({"url": url, "ok": True, "title": title, "file": f"{slug}.md", "depth": depth,
                              "chars": len(md), "pdfs": pdfs, "snapshot": snap, "fecha_copia": ts[:8]})
                print(f"  ✓ {url} ({len(md)} chars, copia {ts[:8]}, {len(pdfs)} PDFs)", flush=True)
                nxt += [h for h in hrefs if h.startswith("https://climalit.es/") and not EXCLUDE.search(h)
                        and not re.search(r"\.(pdf|jpe?g|png|webp|svg|css|js|xml|zip|ico)/?$", h, re.I)
                        and not re.search(r"/20\d\d/", h)]
            frontier = list(dict.fromkeys(nxt))
    (OUT / "_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"terminado: {sum(e['ok'] for e in index)}/{len(index)} páginas -> {OUT}")


if __name__ == "__main__":
    asyncio.run(main())
