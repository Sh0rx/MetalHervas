"""Genera los artboards (.dc.html) del tablero «Logo Metal Hervás: propuestas» en Claude Design.
Uso: python scripts/tablero_logo.py <carpeta raíz de salida>
"""
import json, sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import logo_propuestas as lp

ROOT = pathlib.Path(sys.argv[1]); P = ROOT / "project"; P.mkdir(parents=True, exist_ok=True)

BLOB = {"color": "/_blob/8bf5ef3042bc58a993a82f50511292ec", "negativo": "/_blob/c74534a14dc3b9c32986e23667af852a",
        "pvc": "/_blob/d87b64420897e635064390892e528868"}
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900'
         '&amp;family=IBM+Plex+Mono:wght@400;500&amp;family=IBM+Plex+Sans:wght@400;600;700&amp;display=swap" rel="stylesheet">')
ASPECT = {"Actual": 5040 / 1980, "A": 5040 / 1860, "B": 1000 / 230, "C": 1330 / 300}
SANS = "'IBM Plex Sans', 'Segoe UI', sans-serif"
DISP = "Archivo, 'Arial Black', sans-serif"
MONO = "'IBM Plex Mono', Consolas, monospace"

def page(title, body, props, logic):
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
<script type="text/x-dc" data-dc-script data-props='{json.dumps(props, ensure_ascii=False)}'>
class Component extends DCLogic {{
{logic}
}}
</script>
</body>
</html>
"""

LOGO_PROPS = {"tone": {"editor": "enum", "options": ["claro", "oscuro"], "default": "claro"},
              "form": {"editor": "enum", "options": ["horizontal", "simbolo"], "default": "horizontal"},
              "h": {"editor": "int", "min": 12, "max": 400, "default": 120}}

def logo_logic(colores, tile):
    return f"""renderVals() {{
const tone = this.props.tone ?? 'claro';
const form = this.props.form ?? 'horizontal';
const h = Number(this.props.h ?? 120);
const C = {json.dumps(colores)};
return {{ c: C[tone] || C.claro, t: {json.dumps(tile)}, hpx: h + 'px', esH: form !== 'simbolo', esS: form === 'simbolo' }};
}}"""

def logo_file(nombre, horizontal_svg, tile_svg, colores, tile, w_prev):
    body = f"""<div style="display: inline-block; line-height: 0; font-family: {SANS}; color: #141815">
<sc-if value="{{{{esH}}}}" hint-placeholder-val="{{{{ true }}}}">
<div style="height: {{{{hpx}}}}">{horizontal_svg}</div>
</sc-if>
<sc-if value="{{{{esS}}}}" hint-placeholder-val="{{{{ false }}}}">
<div style="height: {{{{hpx}}}}; width: {{{{hpx}}}}">{tile_svg}</div>
</sc-if>
</div>"""
    props = dict(LOGO_PROPS); props["$preview"] = {"width": w_prev, "height": 120}
    return page(nombre, body, props, logo_logic(colores, tile))

SVGSTYLE = 'style="height: 100%; width: auto; display: block"'
SQSTYLE = 'style="height: 100%; width: 100%; display: block"'

# ---- Actual: el logo de hoy (imagen); como «símbolo» no tiene otra cosa que el logo entero encogido
actual = f"""<div style="display: inline-block; line-height: 0">
<sc-if value="{{{{esH}}}}" hint-placeholder-val="{{{{ true }}}}">
<sc-if value="{{{{claro}}}}" hint-placeholder-val="{{{{ true }}}}"><img src="{BLOB['color']}" alt="Logo actual de Metal Hervás" style="height: {{{{hpx}}}}; width: auto; display: block"></sc-if>
<sc-if value="{{{{oscuro}}}}" hint-placeholder-val="{{{{ false }}}}"><img src="{BLOB['negativo']}" alt="Logo actual de Metal Hervás en negativo" style="height: {{{{hpx}}}}; width: auto; display: block"></sc-if>
</sc-if>
<sc-if value="{{{{esS}}}}" hint-placeholder-val="{{{{ false }}}}">
<div style="height: {{{{hpx}}}}; width: {{{{hpx}}}}; background: #ffffff; display: flex; align-items: center; justify-content: center"><img src="{BLOB['color']}" alt="Logo actual reducido" style="width: 94%; height: auto; display: block"></div>
</sc-if>
</div>"""
actual_logic = """renderVals() {
const tone = this.props.tone ?? 'claro';
const form = this.props.form ?? 'horizontal';
const h = Number(this.props.h ?? 120);
return { hpx: h + 'px', esH: form !== 'simbolo', esS: form === 'simbolo', claro: tone !== 'oscuro', oscuro: tone === 'oscuro' };
}"""
props_actual = dict(LOGO_PROPS); props_actual["$preview"] = {"width": 320, "height": 120}

# ---- A
A_H = lp.grupo([3])
a_svg = (f'<svg viewBox="{lp.A_VB}" {SVGSTYLE} role="img" aria-label="Metal Hervás, propuesta A">'
         f'<g fill="{{{{c.acero}}}}">{lp.A_ACERO}</g><g fill="{{{{c.viga}}}}">{lp.A_VIGA}</g>'
         f'<g fill="{{{{c.linea}}}}">{lp.A_LINEA}</g><g fill="{{{{c.metal}}}}">{lp.A_METAL}</g>'
         f'<g fill="{{{{c.hervas}}}}">{lp.A_HERVAS}</g></svg>')
a_tile = (f'<svg viewBox="0 0 1100 1100" {SQSTYLE} role="img" aria-label="Icono A">'
          f'<rect width="1100" height="1100" fill="{{{{t.fondo}}}}"></rect>'
          f'<g transform="translate(-355 -690)" fill="{{{{t.letra}}}}">{A_H}</g></svg>')
# ---- B
b_svg = (f'<svg viewBox="{lp.B_VB}" {SVGSTYLE} role="img" aria-label="Metal Hervás, propuesta B">'
         f'<text x="2" y="110" fill="{{{{c.metal}}}}" style="font-family: {DISP}; font-stretch: 125%; font-weight: 600; font-size: 50px; letter-spacing: 15px">METAL</text>'
         f'<path fill="{{{{c.simbolo}}}}" d="{lp.B_SIM}"></path>'
         f'<text x="{lp.B_SIM_W + 10:.0f}" y="270" fill="{{{{c.hervas}}}}" style="font-family: {DISP}; font-stretch: 125%; font-weight: 800; font-size: 190px; letter-spacing: -2px">ERVÁS</text></svg>')
b_tile_d, b_tile_w = lp.seccion_h(0, 0, 100)
b_tile = (f'<svg viewBox="0 0 200 200" {SQSTYLE} role="img" aria-label="Icono B: sección de viga en H">'
          f'<rect width="200" height="200" fill="{{{{t.fondo}}}}"></rect>'
          f'<path transform="translate({(200 - b_tile_w) / 2:.2f} 50)" fill="{{{{t.simbolo}}}}" d="{b_tile_d}"></path></svg>')
# ---- C
c_svg = (f'<svg viewBox="0 0 1330 300" {SVGSTYLE} role="img" aria-label="Metal Hervás, propuesta C">'
         f'<path fill="{{{{c.marco}}}}" d="{lp.C_MARCO}"></path><path fill="{{{{c.pane}}}}" d="{lp.C_PANE}"></path>'
         f'<text x="292" y="270" style="font-family: {DISP}; font-stretch: 100%; font-weight: 700; font-size: 168px; letter-spacing: -3px">'
         f'<tspan fill="{{{{c.metal}}}}">metal </tspan><tspan fill="{{{{c.hervas}}}}">hervás</tspan></text></svg>')
c_m, c_p = lp.portico(44, 40, 112)
c_tile = (f'<svg viewBox="0 0 200 200" {SQSTYLE} role="img" aria-label="Icono C: pórtico con vidrio">'
          f'<rect width="200" height="200" fill="{{{{t.fondo}}}}"></rect>'
          f'<path fill="{{{{t.marco}}}}" d="{c_m}"></path><path fill="{{{{t.pane}}}}" d="{c_p}"></path></svg>')

FILES = {}
FILES["LogoActual.dc.html"] = page("Logo actual", actual, props_actual, actual_logic)
FILES["LogoA.dc.html"] = logo_file("Logo A", a_svg, a_tile, lp.COL["A"], {"fondo": "#4BA939", "letra": "#FFFFFF"}, 330)
FILES["LogoB.dc.html"] = logo_file("Logo B", b_svg, b_tile, {k: v for k, v in lp.COL["B"].items() if k != "tile"}, lp.COL["B"]["tile"], 520)
FILES["LogoC.dc.html"] = logo_file("Logo C", c_svg, c_tile, {k: v for k, v in lp.COL["C"].items() if k != "tile"}, lp.COL["C"]["tile"], 540)

def imp(p, tone="claro", form="horizontal", h=60):
    w = h if form == "simbolo" else round(h * ASPECT[p])
    return f'<dc-import name="Logo{p}" tone="{tone}" form="{form}" h="{h}" hint-size="{w}px,{h}px"></dc-import>'

LABEL = f"font-family: {SANS}; font-size: 13px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #545e58; margin: 0"

# ---------- Main: comparativa ----------
PROP = [("Actual", "Actual", "Como está hoy, con «S.L.» y la viga en perspectiva.", False),
        ("A", "A · Limpieza", "El mismo logo redibujado: sin «S.L.», viga en plano, trazo limpio.", False),
        ("B", "B · Evolución", "La H de HERVÁS es la sección de un pilar de acero. Se mantienen el verde y el nombre.", True),
        ("C", "C · Rebranding", "Identidad nueva: un pórtico con vidrio, letra en minúscula y verde oscuro.", False)]

def h_for(p, target_w):
    return max(16, round(target_w / ASPECT[p]))

cols = []
for p, titulo, desc, rec in PROP:
    chip = ('<span style="font-family: ' + SANS + '; font-size: 12px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; '
            'color: #256a31; background: #e3f3e6; padding: 4px 10px; border-radius: 999px">Recomendada</span>') if rec else ""
    cols.append(f"""<div style="display: flex; flex-direction: column; gap: 16px; min-width: 0">
<div style="display: flex; align-items: center; gap: 12px; min-height: 28px">
<h2 style="margin: 0; font-family: {DISP}; font-stretch: 118%; font-weight: 800; font-size: 26px; color: #141815">{titulo}</h2>{chip}
</div>
<p style="margin: 0; font-family: {SANS}; font-size: 15px; line-height: 1.5; color: #545e58; min-height: 68px">{desc}</p>
<div style="height: 200px; background: #ffffff; border: 1px solid #d6dbd7; display: flex; align-items: center; justify-content: center">{imp(p, "claro", "horizontal", h_for(p, 300))}</div>
<div style="height: 200px; background: #0f1211; display: flex; align-items: center; justify-content: center">{imp(p, "oscuro", "horizontal", h_for(p, 300))}</div>
<div style="display: flex; align-items: flex-end; gap: 24px; padding-top: 8px">
<div style="display: flex; flex-direction: column; gap: 8px; align-items: center">{imp(p, "claro", "simbolo", 64)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">64 px</span></div>
<div style="display: flex; flex-direction: column; gap: 8px; align-items: center">{imp(p, "claro", "simbolo", 32)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">32 px</span></div>
<div style="display: flex; flex-direction: column; gap: 8px; align-items: center">{imp(p, "claro", "simbolo", 16)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">16 px</span></div>
</div>
</div>""")

main_body = f"""<div style="width: 1600px; height: 900px; box-sizing: border-box; padding: 56px 48px; background: #f5f6f4; color: #141815; font-family: {SANS}; display: flex; flex-direction: column; gap: 40px">
<div style="display: flex; flex-direction: column; gap: 8px">
<p style="{LABEL}">Metal Hervás · Logo</p>
<h1 style="margin: 0; font-family: {DISP}; font-stretch: 118%; font-weight: 800; font-size: 44px; line-height: 1">Cuatro caminos para el logo</h1>
</div>
<div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 32px">
{''.join(cols)}
</div>
</div>"""
FILES["Main.dc.html"] = page("Comparativa de logos", main_body, {"$preview": {"width": 1600, "height": 900}}, "renderVals() { return {}; }")

# ---------- Aplicaciones ----------
SUB = {
    "Actual": f'<img src="{BLOB["pvc"]}" alt="Submarca Ventanas de PVC actual" style="width: 420px; height: auto; display: block">',
    "A": f'<img src="{BLOB["pvc"]}" alt="Submarca Ventanas de PVC" style="width: 420px; height: auto; display: block">',
}
def fila_sub(p, texto, color, fuente):
    return (f'<div style="display: flex; align-items: center; gap: 16px">{imp(p, "claro", "simbolo", 44)}'
            f'<span style="{fuente}; color: {color}">{texto}</span></div>')
FB = f"font-family: {DISP}; font-stretch: 125%; font-weight: 800; font-size: 22px; letter-spacing: 0.02em; text-transform: uppercase"
FC = f"font-family: {DISP}; font-stretch: 100%; font-weight: 700; font-size: 28px; letter-spacing: -0.01em"
SUB["B"] = "".join(fila_sub("B", t, "#141815", FB) for t in ["Ventanas de PVC", "Estructuras metálicas", "Cerrajería"])
SUB["C"] = "".join(fila_sub("C", t, "#256a31", FC) for t in ["ventanas de pvc", "estructuras metálicas", "cerrajería"])
SUBNOTA = {"Actual": "Tipografía y verdes distintos a los del logo.", "A": "Sin cambios en la limpieza.",
           "B": "Misma familia de letra y mismo icono para cada línea de negocio.", "C": "Misma familia de letra y mismo icono para cada línea de negocio."}

def aplic(p, titulo):
    hh = h_for(p, 230 if p in ("Actual", "A") else 250)
    van_h = h_for(p, 300)
    nave_h = h_for(p, 380)
    body = f"""<div style="width: 1600px; height: 980px; position: relative; overflow: hidden; background: #f5f6f4; color: #141815; font-family: {SANS}">
<h1 style="position: absolute; left: 48px; top: 28px; margin: 0; font-family: {DISP}; font-stretch: 118%; font-weight: 800; font-size: 32px">{titulo}, en uso</h1>
<div style="position: absolute; left: 48px; top: 96px; width: 1504px; height: 88px; box-sizing: border-box; background: #ffffff; border: 1px solid #d6dbd7; display: flex; align-items: center; gap: 40px; padding: 0 32px">
{imp(p, "claro", "horizontal", hh if p in ("Actual", "A") else h_for(p, 220))}
<nav style="display: flex; gap: 28px; font-size: 16px; font-weight: 600; flex-grow: 1">
<a href="#" style="color: #141815; text-decoration: none">Ventanas</a><a href="#" style="color: #141815; text-decoration: none">Aluminio</a><a href="#" style="color: #141815; text-decoration: none">Estructuras</a><a href="#" style="color: #141815; text-decoration: none">Trabajos</a><a href="#" style="color: #141815; text-decoration: none">Contacto</a>
</nav>
<a href="#" style="background: #256a31; color: #ffffff; text-decoration: none; font-weight: 600; font-size: 16px; padding: 14px 24px; border-radius: 2px">Pedir presupuesto</a>
</div>
<div style="position: absolute; left: 48px; top: 200px; width: 1504px; height: 112px; box-sizing: border-box; background: #0f1211; display: flex; align-items: center; gap: 48px; padding: 0 32px">
{imp(p, "oscuro", "horizontal", h_for(p, 200))}
<span style="color: #a3ada7; font-size: 15px; flex-grow: 1">Ctra. de las Cañadas, s/n · 10700 Hervás (Cáceres)</span>
<span style="color: #ffffff; font-family: {MONO}; font-size: 18px">664 40 96 18</span>
</div>

<p style="{LABEL}; position: absolute; left: 48px; top: 348px">Pestaña del navegador</p>
<div style="position: absolute; left: 48px; top: 380px; width: 420px; height: 280px; box-sizing: border-box; background: #ffffff; border: 1px solid #d6dbd7; display: flex; flex-direction: column">
<div style="height: 52px; background: #dfe3e0; display: flex; align-items: flex-end; padding: 0 12px">
<div style="height: 40px; width: 300px; background: #ffffff; border-radius: 10px 10px 0 0; display: flex; align-items: center; gap: 10px; padding: 0 14px; box-sizing: border-box">
{imp(p, "claro", "simbolo", 16)}<span style="font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">Metal Hervás · Carpintería en Hervás</span>
</div>
</div>
<div style="flex-grow: 1; display: flex; align-items: center; justify-content: center; gap: 40px">
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px">{imp(p, "claro", "simbolo", 16)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">16 px</span></div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px">{imp(p, "claro", "simbolo", 32)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">32 px</span></div>
<div style="display: flex; flex-direction: column; align-items: center; gap: 10px">{imp(p, "claro", "simbolo", 96)}<span style="font-family: {MONO}; font-size: 12px; color: #545e58">96 px</span></div>
</div>
</div>

<p style="{LABEL}; position: absolute; left: 508px; top: 348px">Foto de perfil</p>
<div style="position: absolute; left: 508px; top: 380px; width: 200px; display: flex; flex-direction: column; align-items: center; gap: 14px">
<div style="width: 180px; height: 180px; border-radius: 50%; overflow: hidden; border: 1px solid #d6dbd7; line-height: 0">{imp(p, "claro", "simbolo", 180)}</div>
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
<div style="position: absolute; left: 56px; top: 74px; display: flex; flex-direction: column; gap: 16px">
{imp(p, "claro", "horizontal", van_h)}
<span style="font-family: {MONO}; font-size: 22px; font-weight: 500; color: #141815">664 40 96 18</span>
</div>
</div>

<p style="{LABEL}; position: absolute; left: 48px; top: 690px">Rótulo de la nave</p>
<div style="position: absolute; left: 48px; top: 722px; width: 880px; height: 230px; overflow: hidden; background: repeating-linear-gradient(90deg, #c9ced0 0px, #c9ced0 22px, #b8bec0 22px, #b8bec0 24px)">
<div style="position: absolute; left: 180px; top: 22px; width: 520px; height: 112px; background: #ffffff; display: flex; align-items: center; justify-content: center">{imp(p, "claro", "horizontal", min(92, nave_h))}</div>
<div style="position: absolute; left: 330px; top: 150px; width: 220px; height: 80px; background: repeating-linear-gradient(180deg, #e3e6e4 0px, #e3e6e4 18px, #cdd2cf 18px, #cdd2cf 20px)"></div>
</div>

<p style="{LABEL}; position: absolute; left: 968px; top: 690px">Submarcas · {SUBNOTA[p]}</p>
<div style="position: absolute; left: 968px; top: 722px; width: 584px; height: 230px; box-sizing: border-box; background: #ffffff; border: 1px solid #d6dbd7; padding: 24px 32px; display: flex; flex-direction: column; justify-content: center; gap: 18px">
{SUB[p]}
</div>
</div>"""
    return page(f"{titulo} en uso", body, {"$preview": {"width": 1600, "height": 980}}, "renderVals() { return {}; }")

for p, titulo, _, _ in PROP:
    FILES[f"Aplic{p}.dc.html"] = aplic(p, titulo)

for n, s in FILES.items():
    (P / n).write_text(s, encoding="utf-8")
    print(n, len(s) // 1024, "KB")

# ---------- índice ----------
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
boards = {"Main.dc.html": {"x": 0, "y": 0, "w": 1600, "h": 900, "title": "Comparativa"}}
y = 900 + 120
for i, (p, titulo, _, _) in enumerate(PROP):
    x = 0 if i % 2 == 0 else 1680
    if i == 2: y += 980 + 120
    boards[f"Aplic{p}.dc.html"] = {"x": x, "y": y, "w": 1600, "h": 980, "title": f"{titulo} · en uso"}
y += 980 + 120
x = 0
for p, w in [("Actual", 320), ("A", 330), ("B", 520), ("C", 540)]:
    boards[f"Logo{p}.dc.html"] = {"x": x, "y": y, "w": w, "h": 120, "title": f"Componente logo {p}"}
    x += w + 80
canvas = {"v": 3, "createdOnFiles": {"v": 1, "at": now}, "title": "Logo Metal Hervás: propuestas",
          "launch": {"view": "canvas"}, "pages": [], "boards": boards, "order": list(boards),
          "notes": {
              "guia": {"x": -560, "y": 0, "w": 460, "fill": "green", "size": "m",
                       "text": "Cómo leer el tablero:\n\n1. Arriba, la comparativa: cada logo sobre claro, sobre oscuro y como icono pequeño.\n2. Debajo, cada opción aplicada a la web, la pestaña del navegador, el perfil de WhatsApp, la furgoneta y el rótulo de la nave.\n\nDeja un comentario en la opción que más te guste (o en lo que cambiarías)."},
              "seccion": {"x": -560, "y": 1020, "w": 460, "fill": "yellow", "size": "m",
                          "text": "La «H» de la propuesta B no es una letra dibujada: es la sección real de un pilar de acero HD 400 × 1086 (ArcelorMittal), girada. Por eso tiene los redondeos interiores entre alma y alas."}},
          "designSystems": [{"title": "Metal Hervás", "namespace": "metalhervas",
                             "artifact": "https://claude.ai/artifact/3DZaLvDXRyQ3gG47BAbq5f",
                             "version": "1790996051-eea8", "copiedAt": now}]}
(P / "canvas.json").write_text(json.dumps(canvas, ensure_ascii=False, indent=1), encoding="utf-8")
print("canvas.json", list(boards))
