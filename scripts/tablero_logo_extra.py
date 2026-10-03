"""Añade al tablero «Logo Metal Hervás: propuestas» las variantes fieles (V1–V5), la prueba de
favicon con el nudo pilar-viga y las propuestas evolutivas (E1–E5), cada una con sus aplicaciones.
Uso: python scripts/tablero_logo_extra.py <canvas.json leído del artifact> <carpeta raíz de salida>
"""
import json, re, sys, pathlib, datetime

SRC_CANVAS, ROOT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
P = ROOT / "project"; P.mkdir(parents=True, exist_ok=True)
LOGO = pathlib.Path("prototipos/assets/logo")

BLOB = {  # urls devueltas al subir los assets al tablero
 "v1-lockup-color": "80d81d5d6b36b90591b3d00b4c532df9", "v1-lockup-negativo": "a4acc33a3021aa731cd5e85a49fd1f9b", "v1-simbolo-color": "1fc38537c8860d0a7969e3c004c96f0b",
 "v2-lockup-color": "ed0da47b61c20a5f3deb5663ae35f767", "v2-lockup-negativo": "adab9abd8a4d507eab9aca4043e5c645", "v2-simbolo-color": "54f584e7e96f99fa54f6c4355d033796",
 "v3-lockup-color": "1257cf9cb5fc79f06b0283c9be09c52e", "v3-lockup-negativo": "f29e2a12f2a06d78f89507a11c7202e5", "v3-simbolo-color": "2d54b3a47a48e38cf8ebaff6a44a2f40",
 "v4-lockup-color": "793f72d475752ea1b4d590f9f96e676c", "v4-lockup-negativo": "d519b913cd61ebce2816374d28eaa388", "v4-simbolo-color": "12b4c0909f756a8bdae25550d7f59f45",
 "v5-lockup-color": "bf4bd1a994dd84cbda8ba94dd4dbae9f", "v5-lockup-negativo": "82f00ae30239eb9064e0dd2a6f85173d", "v5-simbolo-color": "ba31aa9243849087d4d4f56b4afa1808",
 "nudo-a": "b390b17946b73f34d12b929457ddcfde", "nudo-b": "d359040a7b75ab5e3dd61e4b6ff59698", "nudo-c": "bccf872a030ad0b8eefaa7a62f3cd222",
 "e1-lockup-color": "3f6381d0e962f207ee1f39994ee1702b", "e1-lockup-negativo": "428635726ed3cc6d6f6401ae267d602c", "e1-simbolo-color": "df2b818eea30c8b720014232d513fe92",
 "e2-lockup-color": "fc3685a7ec37a7efbd3c2f6fd9cb6a42", "e2-lockup-negativo": "0803c52b76733f08ec2cbfc57c3ad6d4", "e2-simbolo-color": "e8c30c6dfd9ddfa9a24a56d27f1cf48a",
 "e3-lockup-color": "db84b3d3090a45575e59c091c9621dc2", "e3-lockup-negativo": "d8abf23123d6f9478322be468196905f", "e3-simbolo-color": "2be6119ac47d899cf9a0b25e81503d14",
 "e4-lockup-color": "ba6a13a4b3845cb5e364ed094232cebe", "e4-lockup-negativo": "c08d7fa15c3c63f422722b2271b2fae8", "e4-simbolo-color": "2d89f3e5da94f260c8bb1ecdd17fc991",
 "e5-lockup-color": "885c9f0f020572403dd2ce1883a54956", "e5-lockup-negativo": "124bd1e5ad6945735002895b9a31ff73", "e5-simbolo-color": "b5af650ed7fe8027787dc0eee2706fa6",
 "pvc": "d87b64420897e635064390892e528868",
}
URL = lambda k: f"/_blob/{BLOB[k]}"

def aspect(path):
    vb = re.search(r'viewBox="([^"]+)"', path.read_text(encoding="utf-8")).group(1).split()
    return float(vb[2]) / float(vb[3])

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900'
         '&amp;family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet">')
SANS = "'IBM Plex Sans', 'Segoe UI', sans-serif"; DISP = "Archivo, 'Arial Black', sans-serif"; MONO = "'IBM Plex Mono', Consolas, monospace"
LABEL = f"font-family: {SANS}; font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #545e58; margin: 0"

def page(title, body, w, h):
    props = json.dumps({"$preview": {"width": w, "height": h}})
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
body{{margin:0}}
a{{color:#256a31}}a:hover{{color:#141815}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{props}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""

# ---------- catálogo de propuestas ----------
SETS = {
 "V": [("v1", "1 · Fiel", "El original redibujado: la línea en L llega al pilar y cierra la estructura."),
       ("v2", "2 · La tilde es una viga", "La tilde de la Á es un tramo de viga de acero."),
       ("v3", "3 · Placa de fabricante", "El logo estampado en una placa remachada, como la de una máquina."),
       ("v4", "4 · Nave", "La viga cubre el nombre como una cubierta y lleva METAL escrito."),
       ("v5", "5 · Firma de taller", "La línea se convierte en un cordón de soldadura bajo HERVÁS.")],
 "E": [("e1", "E1 · Nudo", "El cruce pilar-viga del logo original pasa a ser el símbolo."),
       ("e2", "E2 · Herencia", "«Metal» caligráfico de siempre como acento sobre un HERVÁS moderno."),
       ("e3", "E3 · Escuadra", "Une la marca con la submarca de PVC: escuadra verde y cuadros de ventana."),
       ("e4", "E4 · Tilde-viga", "La tilde de la Á es un perfil de acero, con la letra moderna."),
       ("e5", "E5 · Línea de corte", "Un corte limpio atraviesa las letras, como chapa cortada a plasma.")],
}
FOLDER = {"V": "variantes", "E": "evolucion"}
ASP = {k: aspect(LOGO / FOLDER[s] / f"{k}-lockup-color.svg") for s in SETS for k, _, _ in SETS[s]}

def lockup(k, tone, w=None, h=None):
    if h is None: h = round(w / ASP[k])
    tono = "color" if tone == "claro" else "negativo"
    return f'<img src="{URL(f"{k}-lockup-{tono}")}" alt="Logo Metal Hervás, propuesta {k.upper()}" style="height: {h}px; width: auto; display: block">'

def simbolo(k, s):
    return f'<img src="{URL(f"{k}-simbolo-color")}" alt="Icono {k.upper()}" style="width: {s}px; height: {s}px; display: block">'

def comparativa(set_key, titulo, eyebrow):
    cols = []
    for k, nombre, desc in SETS[set_key]:
        sizes = "".join(f'<div style="display: flex; flex-direction: column; gap: 8px; align-items: center">{simbolo(k, s)}'
                        f'<span style="font-family: {MONO}; font-size: 12px; color: #545e58">{s} px</span></div>' for s in (64, 32, 16))
        cols.append(f"""<div style="display: flex; flex-direction: column; gap: 16px; min-width: 0">
<h2 style="margin: 0; font-family: {DISP}; font-stretch: 112%; font-weight: 800; font-size: 22px; line-height: 1.15; color: #141815; min-height: 52px">{nombre}</h2>
<p style="margin: 0; font-family: {SANS}; font-size: 15px; line-height: 1.5; color: #545e58; min-height: 68px">{desc}</p>
<div style="height: 190px; background: #ffffff; border: 1px solid #d6dbd7; display: flex; align-items: center; justify-content: center">{lockup(k, "claro", w=280)}</div>
<div style="height: 190px; background: #0f1211; display: flex; align-items: center; justify-content: center">{lockup(k, "oscuro", w=280)}</div>
<div style="display: flex; align-items: flex-end; gap: 22px; padding-top: 8px">{sizes}</div>
</div>""")
    body = f"""<div style="width: 1920px; height: 900px; box-sizing: border-box; padding: 56px 48px; background: #f5f6f4; color: #141815; font-family: {SANS}; display: flex; flex-direction: column; gap: 40px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{LABEL}">{eyebrow}</p>
<h1 style="margin: 0; font-family: {DISP}; font-stretch: 118%; font-weight: 800; font-size: 44px; line-height: 1">{titulo}</h1>
</div>
<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 28px">
{''.join(cols)}
</div>
</div>"""
    return page(titulo, body, 1920, 900)

def submarcas(set_key, k):
    if set_key == "V":
        return (f'<img src="{URL("pvc")}" alt="Submarca Ventanas de PVC" style="width: 420px; height: auto; display: block">', "Se mantiene la submarca actual.")
    f = f"font-family: {DISP}; font-stretch: 125%; font-weight: 800; font-size: 22px; letter-spacing: 0.02em; text-transform: uppercase; color: #141815"
    filas = "".join(f'<div style="display: flex; align-items: center; gap: 16px">{simbolo(k, 44)}<span style="{f}">{t}</span></div>'
                    for t in ("Ventanas de PVC", "Estructuras metálicas", "Cerrajería"))
    return filas, "Misma letra e icono para cada línea de negocio."

def aplic(set_key, k, titulo):
    sub, nota = submarcas(set_key, k)
    body = f"""<div style="width: 1600px; height: 980px; position: relative; overflow: hidden; background: #f5f6f4; color: #141815; font-family: {SANS}">
<h1 style="position: absolute; left: 48px; top: 28px; margin: 0; font-family: {DISP}; font-stretch: 118%; font-weight: 800; font-size: 32px">{titulo}, en uso</h1>
<div style="position: absolute; left: 48px; top: 96px; width: 1504px; height: 88px; box-sizing: border-box; background: #ffffff; border: 1px solid #d6dbd7; display: flex; align-items: center; gap: 40px; padding: 0 32px">
{lockup(k, "claro", h=min(64, round(240 / ASP[k])))}
<nav style="display: flex; gap: 28px; font-size: 16px; font-weight: 600; flex-grow: 1">
<a href="#" style="color: #141815; text-decoration: none">Ventanas</a><a href="#" style="color: #141815; text-decoration: none">Aluminio</a><a href="#" style="color: #141815; text-decoration: none">Estructuras</a><a href="#" style="color: #141815; text-decoration: none">Trabajos</a><a href="#" style="color: #141815; text-decoration: none">Contacto</a>
</nav>
<a href="#" style="background: #256a31; color: #ffffff; text-decoration: none; font-weight: 600; font-size: 16px; padding: 14px 24px; border-radius: 2px">Pedir presupuesto</a>
</div>
<div style="position: absolute; left: 48px; top: 200px; width: 1504px; height: 112px; box-sizing: border-box; background: #0f1211; display: flex; align-items: center; gap: 48px; padding: 0 32px">
{lockup(k, "oscuro", h=min(72, round(220 / ASP[k])))}
<span style="color: #a3ada7; font-size: 15px; flex-grow: 1">Ctra. de las Cañadas, s/n · 10700 Hervás (Cáceres)</span>
<span style="color: #ffffff; font-family: {MONO}; font-size: 18px">664 40 96 18</span>
</div>
<p style="{LABEL}; position: absolute; left: 48px; top: 348px">Pestaña del navegador</p>
<div style="position: absolute; left: 48px; top: 380px; width: 420px; height: 280px; box-sizing: border-box; background: #ffffff; border: 1px solid #d6dbd7; display: flex; flex-direction: column">
<div style="height: 52px; background: #dfe3e0; display: flex; align-items: flex-end; padding: 0 12px">
<div style="height: 40px; width: 300px; background: #ffffff; border-radius: 10px 10px 0 0; display: flex; align-items: center; gap: 10px; padding: 0 14px; box-sizing: border-box">
{simbolo(k, 16)}<span style="font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">Metal Hervás · Carpintería en Hervás</span>
</div>
</div>
<div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; gap: 40px">
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px">{simbolo(k, 16)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">16 px</span></div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px">{simbolo(k, 32)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">32 px</span></div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px">{simbolo(k, 96)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">96 px</span></div>
</div>
</div>
<p style="{LABEL}; position: absolute; left: 508px; top: 348px">Foto de perfil</p>
<div style="position: absolute; left: 508px; top: 380px; width: 200px; display: flex; flex-direction: column; align-items: center; gap: 14px">
<div style="width: 180px; height: 180px; border-radius: 50%; overflow: hidden; border: 1px solid #d6dbd7; line-height: 0">{simbolo(k, 180)}</div>
<span style="font-size: 14px; color: #545e58; text-align: center">WhatsApp, Instagram, Google</span>
</div>
<p style="{LABEL}; position: absolute; left: 748px; top: 348px">Furgoneta</p>
<div style="position: absolute; left: 748px; top: 380px; width: 804px; height: 280px">
<svg viewBox="0 0 804 280" style="position: absolute; inset: 0; width: 804px; height: 280px" aria-hidden="true">
<ellipse cx="400" cy="262" rx="380" ry="10" fill="#d6dbd7"></ellipse>
<path d="M24 60 Q24 30 54 30 H560 Q600 30 630 60 L700 130 Q770 140 776 180 V226 Q776 240 762 240 H38 Q24 240 24 226 Z" fill="#ffffff" stroke="#b9c0bb" stroke-width="2"></path>
<path d="M584 46 H612 Q622 46 632 58 L684 120 H584 Z" fill="#2c3330"></path>
<line x1="572" y1="36" x2="572" y2="238" stroke="#d6dbd7" stroke-width="2"></line>
<line x1="380" y1="36" x2="380" y2="238" stroke="#d6dbd7" stroke-width="2"></line>
<circle cx="170" cy="240" r="40" fill="#1b1b1b"></circle><circle cx="170" cy="240" r="16" fill="#9a9a9a"></circle>
<circle cx="640" cy="240" r="40" fill="#1b1b1b"></circle><circle cx="640" cy="240" r="16" fill="#9a9a9a"></circle>
</svg>
<div style="position: absolute; left: 56px; top: 64px; display: flex; flex-direction: column; gap: 14px">
{lockup(k, "claro", h=min(110, round(300 / ASP[k])))}
<span style="font-family: {MONO}; font-size: 22px; font-weight: 500; color: #141815">664 40 96 18</span>
</div>
</div>
<p style="{LABEL}; position: absolute; left: 48px; top: 690px">Rótulo de la nave</p>
<div style="position: absolute; left: 48px; top: 722px; width: 880px; height: 230px; overflow: hidden; background: repeating-linear-gradient(90deg, #c9ced0 0px, #c9ced0 22px, #b8bec0 22px, #b8bec0 24px)">
<div style="position: absolute; left: 180px; top: 22px; width: 520px; height: 112px; background: #ffffff; display: flex; align-items: center; justify-content: center">{lockup(k, "claro", h=min(92, round(420 / ASP[k])))}</div>
<div style="position: absolute; left: 330px; top: 150px; width: 220px; height: 80px; background: repeating-linear-gradient(180deg, #e3e6e4 0px, #e3e6e4 18px, #cdd2cf 18px, #cdd2cf 20px)"></div>
</div>
<p style="{LABEL}; position: absolute; left: 968px; top: 690px">Submarcas · {nota}</p>
<div style="position: absolute; left: 968px; top: 722px; width: 584px; height: 230px; box-sizing: border-box; background: #ffffff; border: 1px solid #d6dbd7; padding: 24px 32px; display: flex; flex-direction: column; justify-content: center; gap: 18px">
{sub}
</div>
</div>"""
    return page(f"{titulo} en uso", body, 1600, 980)

def favicon_board():
    filas = [("nudo-a", "Negro sobre verde", "Recomendado: a 16 px se sigue leyendo el cruce."),
             ("nudo-b", "Bitono, como el original", "Solo a partir de 64 px: en pequeño se vuelve gris y fino."),
             ("nudo-c", "Cruce ampliado", "Más rotundo, pero casi simétrico: empieza a parecer un árbol.")]
    rows = ""
    for key, nombre, nota in filas:
        img = lambda s: f'<img src="{URL(key)}" alt="Favicon {nombre}" style="width: {s}px; height: {s}px; display: block">'
        sizes = "".join(f'<div style="display: flex; flex-direction: column; align-items: center; gap: 8px">{img(s)}'
                        f'<span style="font-family: {MONO}; font-size: 12px; color: #545e58">{s} px</span></div>' for s in (128, 64, 32, 16))
        rows += f"""<div style="display: flex; align-items: center; gap: 40px; background: #ffffff; border: 1px solid #d6dbd7; padding: 20px 28px">
<div style="width: 260px; display: flex; flex-direction: column; gap: 6px"><strong style="font-size: 18px">{nombre}</strong><span style="font-size: 14px; line-height: 1.45; color: #545e58">{nota}</span></div>
<div style="display: flex; align-items: flex-end; gap: 28px">{sizes}</div>
<div style="height: 40px; width: 300px; background: #dfe3e0; display: flex; align-items: flex-end; padding: 0 10px; margin-left: auto">
<div style="height: 32px; width: 270px; background: #ffffff; border-radius: 8px 8px 0 0; display: flex; align-items: center; gap: 8px; padding: 0 12px; box-sizing: border-box">{img(16)}<span style="font-size: 13px; white-space: nowrap">Metal Hervás · Carpintería</span></div>
</div>
</div>"""
    body = f"""<div style="width: 1500px; height: 760px; box-sizing: border-box; padding: 48px; background: #f5f6f4; color: #141815; font-family: {SANS}; display: flex; flex-direction: column; gap: 20px">
<p style="{LABEL}">Favicon</p>
<h1 style="margin: 0 0 12px; font-family: {DISP}; font-stretch: 118%; font-weight: 800; font-size: 36px; line-height: 1">El cruce pilar-viga del logo original</h1>
{rows}
</div>"""
    return page("Favicon: el cruce pilar-viga", body, 1500, 760)

FILES = {"Fieles.dc.html": comparativa("V", "Cinco variantes que respetan el original", "Metal Hervás · Segunda ronda"),
         "FaviconNudo.dc.html": favicon_board(),
         "Evolucion.dc.html": comparativa("E", "Cinco propuestas evolutivas", "Metal Hervás · Tercera ronda")}
for s in SETS:
    for k, nombre, _ in SETS[s]:
        FILES[f"Aplic{k.upper()}.dc.html"] = aplic(s, k, nombre)
for n, txt in FILES.items():
    (P / n).write_text(txt, encoding="utf-8")

# ---------- índice: el leído del artifact + los artboards nuevos ----------
canvas = json.loads(SRC_CANVAS.read_text(encoding="utf-8"))
boards, order, notes = canvas["boards"], canvas["order"], canvas.setdefault("notes", {})
def add(name, x, y, w, h, title):
    boards[name] = {"x": x, "y": y, "w": w, "h": h, "title": title}
    if name not in order: order.append(name)
Y2 = 3800
add("Fieles.dc.html", 0, Y2, 1920, 900, "Variantes fieles · comparativa")
y = Y2 + 900 + 120
for i, (k, nombre, _) in enumerate(SETS["V"]):
    add(f"Aplic{k.upper()}.dc.html", 0 if i % 2 == 0 else 1680, y, 1600, 980, f"{nombre} · en uso")
    if i % 2 == 1: y += 980 + 120
add("FaviconNudo.dc.html", 1680, y, 1500, 760, "Favicon: el cruce pilar-viga")
Y3 = y + 980 + 120 + 300
add("Evolucion.dc.html", 0, Y3, 1920, 900, "Evolutivas · comparativa")
y = Y3 + 900 + 120
for i, (k, nombre, _) in enumerate(SETS["E"]):
    add(f"Aplic{k.upper()}.dc.html", 0 if i % 2 == 0 else 1680, y, 1600, 980, f"{nombre} · en uso")
    if i % 2 == 1: y += 980 + 120
notes["t1"] = {"x": 0, "y": -300, "text": "Primera ronda · limpieza, evolución y rebranding", "kind": "title1", "maxW": 3280}
notes["t2"] = {"x": 0, "y": Y2 - 300, "text": "Segunda ronda · variantes que respetan el original", "kind": "title1", "maxW": 3280}
notes["t3"] = {"x": 0, "y": Y3 - 300, "text": "Tercera ronda · propuestas evolutivas", "kind": "title1", "maxW": 3280}
notes["n2"] = {"x": -560, "y": Y2, "w": 460, "fill": "yellow", "size": "m",
               "text": "Todas usan las letras reales del logo actual («Metal» y «HERVÁS»). Cada una conserva una combinación distinta de: la caligrafía, la estructura de vigas, la línea en L y el verde."}
notes["n3"] = {"x": -560, "y": Y3, "w": 460, "fill": "yellow", "size": "m",
               "text": "En la línea de la propuesta B: mismo verde y HERVÁS en mayúsculas anchas, letra moderna (Archivo) y submarcas unificadas, cada una con una idea propia."}
(P / "canvas.json").write_text(json.dumps(canvas, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(FILES), "artboards nuevos ·", len(boards), "en total")
