"""Extrae los sistemas, superficies y complementos de Gealan a Proveedores/raw/gealan.json.

Uso: .venv\\Scripts\\python.exe scraping\\extract_gealan.py (antes: dedupe.py gealan, para tener _clean/)
Las especificaciones salen de la tabla técnica de cada página; las paletas de colores van transcritas a mano
de las páginas de acrylcolor® y láminas decorativas porque la web las pinta como texto pegado.
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RAW = Path(__file__).resolve().parent.parent / "Proveedores" / "raw"
G = RAW / "gealan"
BASE = "https://www.gealan.de/es/"

# (slug de página, nombre, nombre en la nota del tío o None si no la trabaja)
SISTEMAS = [
    ("sistemas/s-8000", "S 8000", "S 8000 IQ"),
    ("sistemas/s-9000", "S 9000", "S 9000 IQ"),
    ("sistemas/gealan-linear", "GEALAN-LINEAR®", "Linear (y Linear acrylcolor)"),
    ("sistemas/gealan-kontur", "GEALAN-KONTUR®", None),
    ("sistemas/gealan-kubus", "GEALAN-KUBUS®", None),
    ("sistemas/gealan-smoove-multislide", "GEALAN-SMOOVE multislide", None),
    ("productos/sistemas/sistema-deslizante-74mm-alt", "Corredera 74 mm", None),
    ("sistemas/gealan-smoovio", "GEALAN-SMOOVIO®", None),
]
COMPLEMENTOS = [
    ("productos/soluciones/barreras-sin-umbral", "Umbral estándar", "Umbral"),
    ("productos/gealan-comfort", "GEALAN-COMFORT®", "Umbral"),
    ("sistemas-de-ventilacion", "GEALAN-CAIRE® flex", "Ventilación"),
    ("productos/window-and-door-technology/gealan-windowfit", "GEALAN-windowfit", "Montaje"),
    ("productos/gealan-hafen-city", "Hafen-City-Fenster®", "Acústica"),
    ("innovaciones/estatica-stv", "STV®", "Tecnología"),
    ("innovaciones/aislamiento-termico-ikd", "IKD®", "Tecnología"),
]
COLORES = {
    "trabaja_metalhervas": True,
    "acrylcolor": {
        "url": BASE + "innovaciones/gealan-acrylcolor",
        "descripcion": "Capa de PMMA coextruida sobre el PVC: no se pela, resiste arañazos y luz; acabado mate sedoso. "
                       "Disponible en KUBUS, LINEAR, KONTUR y S 9000 (paleta según sistema).",
        "estandar": ["RAL 7015 gris pizarra", "RAL 7016 gris antracita", "RAL 7022 gris umbra", "RAL 7039 gris cuarzo",
                     "RAL 7040 gris ventana", "RAL 8014 marrón sepia", "RAL 9005 negro profundo", "DB 703",
                     "Plata (similar a RAL 9007)"],
        "ampliada": ["RAL 8022 pardo negruzco", "RAL 9006 aluminio blanco", "Bronce", "RAL 1019 beige agrisado",
                     "RAL 1035 beige perlado", "RAL 7006 gris beige", "RAL 7021 gris negruzco", "RAL 7038 gris ágata",
                     "RAL 9016 blanco tráfico"],
        "bajo_pedido": ["RAL " + c for c in "8023 9001 9002 9010 8000 8001 8003 8011 8012 8017 7032 7033 7035 7036 7037 "
                        "7043 7012 7013 7023 7024 7030 7031 7000 7001 7003 7004 7010 7011 5011 5014 6005 6009 6015 6021 "
                        "1015 3004 3011 5002 5005 5007 1001 1013 1014".split()] + ["Oro"],
        "metalicos": {"url": BASE + "gealan-acrylcolor-metallic",
                      "colores": ["Bronce", "Oro", "Beige perla RAL 1035", "Aluminio blanco RAL 9006",
                                  "Plata (≈ RAL 9007)", "Mica de hierro DB 703"]},
        "base_oscura": {"url": BASE + "gealan-acrylcolor-base-oscura",
                        "exterior": ["RAL 7016", "RAL 9005", "DB 703"],
                        "interior": ["Antracita liso RAL 7016", "Antracita mate RAL 7016", "Antracita graneado RAL 7016",
                                     "Antracita RealWood RAL 7016", "Negro Ulti-Matt", "Alux DB703"]},
    },
    "laminas_decorativas": {
        "url": BASE + "superficies/produktdetail-seite-dekorfolien",
        "estandar": ["Roble dorado", "Nogal", "Caoba", "RAL 7001 gris plata", "RAL 7039 gris cuarzo",
                     "RAL 7012 gris basalto", "RAL 7016 liso gris antracita", "Marrón chocolate"],
        "madera": ["Roble Sheffield claro", "AnTEAK", "Oregón", "Abeto Douglas veteado", "Nuez", "Meranti",
                   "Roble rústico", "Roble oscuro", "Roble negro", "Roble claro", "Pino negro", "Winchester XA"],
        "realwood": ["Woodec Sheffield Oak concrete", "Weissbach Oak", "Woodec Turner Oak toffee",
                     "Woodec Turner Oak malt", "Ginger Oak", "Honey Oak", "RealWood RAL 9010", "RealWood RAL 7016"],
        "lisas": ["RAL 9003 blanco brillante", "RAL 9010 blanco puro", "RAL 9001 blanco crema", "RAL 7035 gris luminoso",
                  "RAL 7023 gris hormigón", "RAL 5011 azul acero", "RAL 8022 pardo negruzco", "RAL 3011 rojo pardo",
                  "RAL 3005 rojo vino", "RAL 6005 verde musgo", "RAL 6009 verde abeto", "Verde monumento"],
        "mate": ["RAL 7012 gris basalto liso", "RAL 7016 antracita mate", "RAL 7021 gris negro liso",
                 "RAL 9010 blanco puro mate", "RAL 9001 blanco crema mate", "RAL 7039 Smooth Quartz Grey",
                 "RAL 7022 gris umbra mate"],
        "metalicas": ["DB 703", "Bronce", "Cepillado metálico latón", "Cepillado metálico plata"],
    },
    "revestimiento_aluminio": "Carcasas exteriores de aluminio en todos los sistemas y cualquier color RAL",
}


def clean(t: str) -> str:
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    return re.sub(r"\s+", " ", t.replace("**", "")).strip()


def load(slug: str) -> tuple[str, str, dict]:
    url = BASE + slug
    e = next(x for x in json.loads((G / "_index.json").read_text(encoding="utf-8")) if x["url"] == url)
    return (G / e["file"]).read_text(encoding="utf-8"), (G / "_clean" / e["file"]).read_text(encoding="utf-8"), e


def specs(md: str) -> dict[str, str]:
    m = re.search(r"^##\s+(Características técnicas|Especificaciones técnicas|Propiedades técnicas)\s*\n(.*?)(?=^##\s|\Z)",
                  md, re.S | re.M)
    out = {}
    for line in (m.group(2) if m else "").splitlines():
        cells = [clean(c) for c in line.strip().strip("|").split("|")]
        cells = [c for c in cells if c]
        if len(cells) == 2 and "---" not in line:
            out[cells[0]] = cells[1]
    return out


def intro(clean_md: str, nombre: str) -> str:
    """Primera frase larga tras el título (las páginas repiten el título dos veces)."""
    lines = [l.strip() for l in clean_md.splitlines()]
    for l in lines:
        if (len(l) > 80 and not l.startswith(("[", "!", "*", "#", "|", "<", "http"))
                and "](http" not in l and l.count(" ") > 8):
            return clean(l)
    return ""


def variantes(md: str) -> dict[str, str]:
    """Bloques 'Título corto' + párrafo bajo '## Variantes…' / '## La versatilidad…'."""
    m = re.search(r"^##\s+(Variantes|La versatilidad)[^\n]*\n(.*?)(?=^##\s|\Z)", md, re.S | re.M)
    out, lines = {}, [l.strip() for l in (m.group(2) if m else "").splitlines() if l.strip()]
    for a, b in zip(lines, lines[1:]):
        if len(a) < 40 and not a.startswith(("!", "[", "|")) and len(b) > 80:
            out[clean(a)] = clean(b)
    return out


sistemas = []
for slug, nombre, nota in SISTEMAS:
    md, cmd, e = load(slug)
    sistemas.append({"nombre": nombre, "nombre_en_nota": nota, "trabaja_metalhervas": nota is not None,
                     "url": e["url"], "descripcion": intro(cmd, nombre), "especificaciones": specs(md),
                     "variantes": variantes(md),
                     "documentos": [{"tipo": "folleto", "url": p} for p in e["pdfs"]]})
complementos = []
for slug, nombre, tipo in COMPLEMENTOS:
    md, cmd, e = load(slug)
    complementos.append({"nombre": nombre, "tipo": tipo, "trabaja_metalhervas": False, "url": e["url"],
                         "descripcion": intro(cmd, nombre)})
_, _, acr = load("innovaciones/gealan-acrylcolor")
COLORES["acrylcolor"]["documentos"] = [{"tipo": "folleto", "url": p} for p in acr["pdfs"]]

out = {"proveedor": "GEALAN", "web": BASE, "alcance_nota": "S 8000 IQ, S 9000 IQ, Linear, Linear acrylcolor y gama de colores",
       "aviso": "La web ya no usa el sufijo «IQ»: S 8000 IQ = S 8000 y S 9000 IQ = S 9000. Fichas técnicas completas en myGEALAN (acceso privado).",
       "sistemas": sistemas, "colores": COLORES, "complementos": complementos}
(RAW / "gealan.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for s in sistemas:
    print(f"{'★' if s['trabaja_metalhervas'] else ' '} {s['nombre']:26} specs {len(s['especificaciones'])} · variantes {list(s['variantes'])[:5]} · {s['descripcion'][:70]}")
for c in complementos:
    print(f"  {c['nombre']:26} {c['descripcion'][:80]}")
