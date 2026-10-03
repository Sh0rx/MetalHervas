"""Rastrea las webs de los proveedores de MetalHervas y guarda cada página en Markdown.

Uso:
    .venv\\Scripts\\python.exe scraping\\crawl.py [proveedor ...]

Salida: Proveedores/raw/<proveedor>/<slug>.md + _index.json (url, título, PDFs enlazados).
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from urllib.parse import urldefrag, urlparse, unquote

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Proveedores" / "raw"

# Para cada proveedor: URLs semilla, patrones de URL a seguir (regex) y profundidad
# máxima de enlaces a seguir desde las semillas.
SUPPLIERS = {
    "gealan": {
        "seeds": [
            "https://www.gealan.de/es/productos",
            "https://www.gealan.de/es/sistemas",
            "https://www.gealan.de/es/sistemas/s-8000",
            "https://www.gealan.de/es/sistemas/s-9000",
            "https://www.gealan.de/es/sistemas/gealan-linear",
            "https://www.gealan.de/es/sistemas/s-7000",
            "https://www.gealan.de/es/sistemas/gealan-kontur",
            "https://www.gealan.de/es/sistemas/gealan-kubus",
            "https://www.gealan.de/es/sistemas/gealan-smoovio",
            "https://www.gealan.de/es/sistemas/gealan-smoove-multislide",
            "https://www.gealan.de/es/productos/sistemas/sistema-deslizante-74mm-alt",
            "https://www.gealan.de/es/ventanas",
            "https://www.gealan.de/es/puertas-de-casa",
            "https://www.gealan.de/es/elementos-corredera",
            "https://www.gealan.de/es/sistemas-de-ventilacion",
            "https://www.gealan.de/es/soluciones-de-umbral",
            "https://www.gealan.de/es/productos/soluciones",
            "https://www.gealan.de/es/productos/tipos-de-productos",
            "https://www.gealan.de/es/productos/soluciones/barreras-sin-umbral",
            "https://www.gealan.de/es/productos/gealan-comfort",
            "https://www.gealan.de/es/productos/balance",
            "https://www.gealan.de/es/productos/gealan-caire",
            "https://www.gealan.de/es/productos/gealan-caire-smart",
            "https://www.gealan.de/es/productos/gealan-caire-flex",
            "https://www.gealan.de/es/productos/gealan-caire-aereco",
            "https://www.gealan.de/es/productos/window-and-door-technology",
            "https://www.gealan.de/es/productos/window-and-door-technology/gealan-windowfit",
            "https://www.gealan.de/es/lo-mas-destacado-del-producto",
            "https://www.gealan.de/es/superficies",
            "https://www.gealan.de/es/superficies/produktdetail-seite-dekorfolien",
            "https://www.gealan.de/es/gealan-acrylcolor",
            "https://www.gealan.de/es/innovaciones/gealan-acrylcolor",
            "https://www.gealan.de/es/gealan-acrylcolor-metallic",
            "https://www.gealan.de/es/gealan-acrylcolor-base-oscura",
            "https://www.gealan.de/es/designed-for-you",
            "https://www.gealan.de/es/designed-for-you/realwood",
            "https://www.gealan.de/es/innovaciones/aislamiento-termico-ikd",
            "https://www.gealan.de/es/innovaciones/estatica-stv",
            "https://www.gealan.de/es/clientes-privados/ventanas-de-color",
            "https://www.gealan.de/es/mediateca/gealan-productos",
        ],
        "follow": [
            r"^https://www\.gealan\.de/es/(sistemas|productos|superficies|innovaciones|designed-for-you)/",
            r"^https://www\.gealan\.de/es/gealan-acrylcolor",
        ],
        "depth": 1,
    },
    "extrugasa": {
        "seeds": [
            "https://www.extrugasa.com/edificacion",
            "https://www.extrugasa.com/acabados",
            "https://www.extrugasa.com/accesorios",
            "https://www.extrugasa.com/ventanas-hc",
        ],
        "follow": [
            r"^https://www\.extrugasa\.com/(edificacion|edificacion-categoria|acabados|accesorios)(/|$)",
        ],
        # Las fichas de producto vienen del sitemap; profundidad 1 por si hay alguna fuera.
        "sitemap_extra": "extrugasa",
        "depth": 1,
    },
    "saint-gobain": {
        "seeds": [
            "https://www.saint-gobain-glass.es/es/productos-0",
            "https://www.saint-gobain-glass.es/es/climalit-la-solucion-para-tus-ventanas",
            "https://www.saint-gobain-glass.es/es/soluciones-ventanas",
            "https://www.saint-gobain-glass.es/es/soluciones-muro-cortina",
            "https://www.saint-gobain-glass.es/es/soluciones-interiores",
            "https://www.saint-gobain-glass.es/es/sg-acustic",
            "https://www.saint-gobain-glass.es/es/nuevas-epds-de-climalit-plus",
            "https://www.saint-gobain-glass.es/es/servicio-de-reciclaje-climalit-recicla",
        ],
        "follow": [
            r"^https://www\.saint-gobain-glass\.es/es/(productos|soluciones|system-specifications)/",
        ],
        "sitemap_extra": "saint-gobain",
        "depth": 1,
    },
    "climalit": {
        "seeds": ["https://www.climalit.es/"],
        "follow": [r"^https://www\.climalit\.es/"],
        "exclude": [r"/(noticias|blog|news|aviso-legal|politica|cookies|contacto)"],
        "depth": 2,
        "max_pages": 120,
    },
    "aluval": {
        "seeds": [
            "https://aluval.es/productos",
            "https://aluval.es/acabados-y-colores",
            "https://aluval.es/particulares",
            "https://aluval.es/arquitectura-y-contract",
        ],
        "follow": [r"^https://aluval\.es/(es/)?(productos|acabados-y-colores|serie|series)(/|$)"],
        "depth": 3,
        "max_pages": 300,
    },
}

SITEMAP_DIR = Path(__file__).resolve().parent / "sitemaps"

# Abre acordeones/pestañas plegadas para que su contenido entre en el Markdown.
EXPAND_JS = """
document.querySelectorAll('details').forEach(d => d.open = true);
for (const el of document.querySelectorAll('button, [role=button], [role=tab], summary, h2, h3, h4, div, span, a')) {
  if (el.closest('nav, header, footer')) continue;
  const t = (el.textContent || '').trim();
  const accordion = el.getAttribute('aria-expanded') === 'false'
    || /^(Mostrar contenido|Ver más|Leer más|Mostrar más)$/i.test(t);
  if (accordion && t.length < 80) { try { el.click(); } catch (e) {} }
}
"""


def sitemap_urls(name: str) -> list[str]:
    """URLs extra sacadas de los sitemaps guardados en scraping/sitemaps/<name>.txt."""
    f = SITEMAP_DIR / f"{name}.txt"
    if not f.exists():
        return []
    return [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip()]


def norm(url: str) -> str:
    url = urldefrag(url)[0]
    return url.rstrip("/") if urlparse(url).path not in ("", "/") else url


def slugify(url: str) -> str:
    p = urlparse(url)
    s = unquote(p.path).strip("/") or "home"
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s[:150]


def markdown_of(result) -> str:
    md = result.markdown
    return getattr(md, "raw_markdown", None) or str(md or "")


async def crawl_supplier(crawler: AsyncWebCrawler, name: str, cfg: dict) -> None:
    out = OUT / name
    out.mkdir(parents=True, exist_ok=True)
    follow = [re.compile(p) for p in cfg.get("follow", [])]
    exclude = [re.compile(p) for p in cfg.get("exclude", [])]
    max_pages = cfg.get("max_pages", 500)

    run_cfg = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        wait_until="domcontentloaded",
        js_code=EXPAND_JS,
        page_timeout=45000,
        delay_before_return_html=2.0,
        excluded_tags=["script", "style", "noscript"],
        verbose=False,
    )
    sem = asyncio.Semaphore(3)

    async def fetch(url: str):
        async with sem:
            r = None
            for _ in range(3):  # reintenta fallos de carga transitorios
                try:
                    r = await asyncio.wait_for(crawler.arun(url, config=run_cfg), timeout=90)
                except Exception as e:  # timeout o error del navegador
                    r = e
                    continue
                md = markdown_of(r) if r.success else ""
                if r.success and len(md) > 300 and "couldn’t load" not in md:
                    break
                await asyncio.sleep(3)
            return url, r

    seeds = [norm(u) for u in cfg["seeds"] + sitemap_urls(cfg.get("sitemap_extra", ""))]
    seen: set[str] = set()
    frontier = list(dict.fromkeys(seeds))
    index = []

    for depth in range(cfg.get("depth", 0) + 1):
        batch = [u for u in frontier if u not in seen][: max(0, max_pages - len(seen))]
        if not batch:
            break
        seen.update(batch)
        print(f"[{name}] profundidad {depth}: {len(batch)} páginas", flush=True)
        results = await asyncio.gather(*(fetch(u) for u in batch))
        next_frontier = []
        for url, r in results:
            if isinstance(r, Exception):
                print(f"  ✗ {url}: {type(r).__name__} {r}"[:160], flush=True)
                index.append({"url": url, "ok": False, "error": repr(r)[:200]})
                continue
            url = norm(r.url or url)
            if not r.success:
                print(f"  ✗ {url}: {r.error_message[:120] if r.error_message else r.status_code}", flush=True)
                index.append({"url": url, "ok": False, "status": r.status_code})
                continue
            md = markdown_of(r)
            title = (r.metadata or {}).get("title") or ""
            links = (r.links or {}).get("internal", []) + (r.links or {}).get("external", [])
            hrefs = [l.get("href", "") for l in links if l.get("href")]
            pdfs = sorted({h for h in hrefs if ".pdf" in h.lower()})
            slug = slugify(url)
            header = f"<!-- url: {url} -->\n<!-- title: {title} -->\n"
            if pdfs:
                header += "<!-- pdfs:\n" + "\n".join(pdfs) + "\n-->\n"
            (out / f"{slug}.md").write_text(header + "\n" + md, encoding="utf-8")
            index.append({"url": url, "ok": True, "title": title, "file": f"{slug}.md",
                          "depth": depth, "chars": len(md), "pdfs": pdfs})
            print(f"  ✓ {url} ({len(md)} chars)", flush=True)
            for h in hrefs:
                h = norm(h)
                if (h not in seen and any(f.search(h) for f in follow)
                        and not any(e.search(h) for e in exclude)
                        and not re.search(r"\.(pdf|jpe?g|png|webp|svg|zip|dwg|mp4)$", h, re.I)):
                    next_frontier.append(h)
        frontier = list(dict.fromkeys(next_frontier))

    (out / "_index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for i in index if i["ok"])
    print(f"[{name}] terminado: {ok}/{len(index)} páginas guardadas en {out}", flush=True)


async def main(names: list[str]) -> None:
    browser = BrowserConfig(headless=True, verbose=False, viewport_width=1366, viewport_height=900)
    async with AsyncWebCrawler(config=browser) as crawler:
        for name in names:
            await crawl_supplier(crawler, name, SUPPLIERS[name])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(main(sys.argv[1:] or list(SUPPLIERS)))
