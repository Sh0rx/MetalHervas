"""Panel único con todas las propuestas de logo numeradas (para enseñárselo a la familia).
Uso: python scripts/tablero_logo_resumen.py <canvas.json leído del artifact> <carpeta raíz de salida>
"""
import json, sys, pathlib
sys.argv, args = sys.argv[:1] + ["_", "_"], sys.argv[1:]   # el módulo extra lee argv al importarse
SRC, ROOT = pathlib.Path(args[0]), pathlib.Path(args[1])
P = ROOT / "project"; P.mkdir(parents=True, exist_ok=True)

import importlib.util
spec = importlib.util.spec_from_file_location("extra", pathlib.Path(__file__).parent / "tablero_logo_extra.py")
src = spec.loader.get_source("extra")
src = src[:src.index("FILES = {")]          # solo helpers y datos, sin escribir nada
ns = {"__file__": str(pathlib.Path(__file__).parent / "tablero_logo_extra.py")}
sys.argv = [sys.argv[0], str(SRC), str(ROOT)]
exec(compile(src, "tablero_logo_extra.py", "exec"), ns)
page, lockup, simbolo, ASP, URL = ns["page"], ns["lockup"], ns["simbolo"], ns["ASP"], ns["URL"]
SANS, DISP, MONO, LABEL = ns["SANS"], ns["DISP"], ns["MONO"], ns["LABEL"]

ASP1 = {"Actual": 5040 / 1980, "A": 5040 / 1860, "B": 1000 / 230, "C": 1330 / 300}
def imp(p, form, h):
    w = h if form == "simbolo" else round(h * ASP1[p])
    return f'<dc-import name="Logo{p}" tone="claro" form="{form}" h="{h}" hint-size="{w}px,{h}px"></dc-import>'
def fit_h(asp, maxw=290, maxh=120):
    return min(maxh, round(maxw / asp))

# (número, nombre, idea, logo grande, icono)
ACTUAL = ("Hoy", "Logo actual", "Como está ahora, con «S.L.» y la viga en perspectiva.",
          f'<img src="/_blob/8bf5ef3042bc58a993a82f50511292ec" alt="Logo actual de Metal Hervás" style="height: {fit_h(ASP1["Actual"])}px; width: auto; display: block">',
          imp("Actual", "simbolo", 48))
R1 = [("1", "Limpieza", "El mismo logo redibujado: sin «S.L.» y con la viga en plano.", imp("A", "horizontal", fit_h(ASP1["A"])), imp("A", "simbolo", 48)),
      ("2", "H de acero", "La H de HERVÁS es la sección de un pilar de acero.", imp("B", "horizontal", fit_h(ASP1["B"])), imp("B", "simbolo", 48)),
      ("3", "Pórtico", "Identidad nueva: pórtico con vidrio y verde oscuro.", imp("C", "horizontal", fit_h(ASP1["C"])), imp("C", "simbolo", 48))]
SETV = ns["SETS"]["V"]; SETE = ns["SETS"]["E"]
nombres_v = ["Fiel", "Tilde de viga", "Placa de fabricante", "Nave", "Firma de taller"]
nombres_e = ["Nudo", "Herencia", "Escuadra", "Tilde-viga moderna", "Línea de corte"]
R2 = [(str(4 + i), nombres_v[i], d, lockup(k, "claro", h=fit_h(ASP[k])), simbolo(k, 48)) for i, (k, _, d) in enumerate(SETV)]
R3 = [(str(9 + i), nombres_e[i], d, lockup(k, "claro", h=fit_h(ASP[k])), simbolo(k, 48)) for i, (k, _, d) in enumerate(SETE)]

def card(num, nombre, idea, grande, icono, ref=False):
    badge_bg, badge_fg = ("#e9ece9", "#545e58") if ref else ("#256a31", "#ffffff")
    return f"""<div style="background: #ffffff; border: 1px solid #d6dbd7; display: flex; flex-direction: column; min-width: 0">
<div style="display: flex; align-items: center; gap: 12px; padding: 16px 18px 0">
<span style="min-width: 40px; height: 40px; padding: 0 8px; box-sizing: border-box; border-radius: 999px; background: {badge_bg}; color: {badge_fg}; font-family: {DISP}; font-stretch: 112%; font-weight: 800; font-size: 18px; display: flex; align-items: center; justify-content: center">{num}</span>
<h3 style="margin: 0; font-family: {DISP}; font-stretch: 112%; font-weight: 800; font-size: 20px; line-height: 1.15">{nombre}</h3>
</div>
<div style="height: 180px; display: flex; align-items: center; justify-content: center; padding: 0 18px">{grande}</div>
<div style="display: flex; align-items: center; gap: 14px; padding: 0 18px 18px; border-top: 1px solid #e9ece9; padding-top: 14px">
<div style="flex-shrink: 0; line-height: 0">{icono}</div>
<p style="margin: 0; font-size: 14px; line-height: 1.45; color: #545e58">{idea}</p>
</div>
</div>"""

def fila(titulo, nota, cards):
    return f"""<section style="display: flex; flex-direction: column; gap: 16px">
<div style="display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap">
<h2 style="margin: 0; font-family: {DISP}; font-stretch: 112%; font-weight: 800; font-size: 26px">{titulo}</h2>
<span style="font-size: 15px; color: #545e58">{nota}</span>
</div>
<div style="display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 24px">{''.join(cards)}</div>
</section>"""

body = f"""<div style="width: 1920px; height: 1640px; box-sizing: border-box; padding: 56px; background: #f5f6f4; color: #141815; font-family: {SANS}; display: flex; flex-direction: column; gap: 40px">
<header style="display: flex; justify-content: space-between; align-items: flex-end; gap: 40px">
<div style="display: flex; flex-direction: column; gap: 10px">
<p style="{LABEL}">Metal Hervás · Logo</p>
<h1 style="margin: 0; font-family: {DISP}; font-stretch: 118%; font-weight: 800; font-size: 52px; line-height: 1">Todas las propuestas</h1>
<p style="margin: 0; font-size: 18px; line-height: 1.5; color: #545e58; max-width: 60ch">Cada tarjeta muestra el logo y, abajo a la izquierda, su icono pequeño (el de la pestaña del navegador o la foto de WhatsApp).</p>
</div>
<div style="background: #e3f3e6; color: #256a31; padding: 18px 24px; font-size: 17px; line-height: 1.45; max-width: 46ch; font-weight: 600">Dime el número de las que más te gusten y qué cambiarías. Se pueden mezclar ideas de varias.</div>
</header>
{fila("Hoy y primera ronda", "Del retoque al cambio completo.", [card(*ACTUAL, ref=True)] + [card(*c) for c in R1])}
{fila("Respetando el original", "Usan las letras del logo de siempre.", [card(*c) for c in R2])}
{fila("Evolución", "Mismo verde y mismo HERVÁS, con letra más actual.", [card(*c) for c in R3])}
</div>"""

(P / "Resumen.dc.html").write_text(page("Todas las propuestas", body, 1920, 1640), encoding="utf-8")
canvas = json.loads(SRC.read_text(encoding="utf-8"))
canvas["boards"]["Resumen.dc.html"] = {"x": -2700, "y": 0, "w": 1920, "h": 1640, "title": "Todas las propuestas"}
if "Resumen.dc.html" not in canvas["order"]:
    canvas["order"].append("Resumen.dc.html")
canvas["launch"] = {"view": "focused", "file": "Resumen.dc.html"}
(P / "canvas.json").write_text(json.dumps(canvas, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok")
