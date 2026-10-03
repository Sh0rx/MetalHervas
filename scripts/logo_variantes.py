"""Cinco variantes de rediseño del logo de Metal Hervás que respetan el original.

Parten de los trazados reales del logo verde (scripts/trace_logo.py → logo-color.svg):
«Metal» caligráfico y las letras de «HERVÁS». Lo nuevo (vigas, línea, placa, soldadura)
se construye con geometría limpia. El único texto añadido («METAL» de la variante 4) se
convierte a trazados con Archivo (OFL), así que ningún SVG depende de fuentes instaladas.

Salida: prototipos/assets/logo/variantes/v{1..5}-{lockup,simbolo}.svg
"""
import math, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import logo_propuestas as lp
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = pathlib.Path("prototipos/assets/logo/variantes"); OUT.mkdir(parents=True, exist_ok=True)
VERDE, NEGRO, ACERO, BLANCO = "#4BA939", "#151515", "#A0A0A0", "#FFFFFF"

g = lp.grupo
METAL = g([11, 12, 13, 15, 16])          # «Metal» caligráfico original
M_SCRIPT = g([11])                       # su «M»
HERVAS = g([0, 1, 2, 3, 4, 5, 6])        # HERVÁS original, con tilde
HERVAS_SIN_TILDE = g([1, 2, 3, 4, 5, 6])
LETRA_H, LETRA_A = g([3]), g([1])

def svg(vb, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="t">'
            f'<title id="t">{title}</title>{body}</svg>')

def poly(pts, fill):
    return f'<polygon fill="{fill}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>'

def rect(x, y, w, h, fill):
    return f'<rect fill="{fill}" x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}"/>'

# ---------- texto → trazados (Archivo, ancho 125, peso 800) ----------
_font = None
def texto(txt, size, x, baseline, tracking=0.0, wdth=125, wght=800):
    global _font
    if _font is None:
        _font = instantiateVariableFont(TTFont("scripts/fonts/Archivo-VF.ttf"), {"wdth": wdth, "wght": wght})
    gs, cmap, upm = _font.getGlyphSet(), _font.getBestCmap(), _font["head"].unitsPerEm
    k = size / upm; pen = SVGPathPen(gs); cx = 0.0
    for ch in txt:
        gn = cmap[ord(ch)]
        gs[gn].draw(TransformPen(pen, (k, 0, 0, -k, x + cx, baseline)))
        cx += gs[gn].width * k + tracking
    return pen.getCommands(), cx - tracking

def cap_height(size):
    texto("H", 1, 0, 0)
    return _font["OS/2"].sCapHeight / _font["head"].unitsPerEm * size

# ---------- viga en alzado: perfil I visto de lado ----------
def viga(x0, y0, largo, canto, ang, ala, c_alma, c_ala):
    """Rectángulo girado `ang` grados alrededor de (x0, y0) (esquina superior izquierda)."""
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    P = lambda s, t: (x0 + ux * s + nx * t, y0 + uy * s + ny * t)
    return (poly([P(0, 0), P(largo, 0), P(largo, canto), P(0, canto)], c_alma)
            + poly([P(0, 0), P(largo, 0), P(largo, ala), P(0, ala)], c_ala)
            + poly([P(0, canto - ala), P(largo, canto - ala), P(largo, canto), P(0, canto)], c_ala))

# =====================================================================
# 1 · FIEL — todo el original, redibujado: la línea en L llega al pilar y cierra la estructura
# =====================================================================
def v1(c):
    t = math.tan(math.radians(22.5)); D = 150; F = 32
    top = lambda x: t * (x - 3240)
    acero = (poly([(2878, 0), (3240, 0), (4600, top(4600)), (4600, top(4600) + D)], c["acero"])
             + rect(4600, 0, 140, 1829, c["acero"])
             + poly([(4740, top(4600)), (5010, top(4600) - t * 270), (5010, top(4600) - t * 270 + D), (4740, top(4600) + D)], c["acero"]))
    oscuro = (poly([(3240 - F / t, 0), (3240, 0), (4600, top(4600)), (4600, top(4600) + F)], c["viga"])
              + poly([(2878, 0), (2878 + F / t, 0), (4600, top(4600) + D - F + 0), (4600, top(4600) + D)], c["viga"])
              + rect(4600, 0, 32, 1829, c["viga"]) + rect(4708, 0, 32, 1829, c["viga"])
              + poly([(4740, top(4600)), (5010, top(4600) - t * 270), (5010, top(4600) - t * 270 + F), (4740, top(4600) + F)], c["viga"])
              + poly([(4740, top(4600) + D - F), (5010, top(4600) - t * 270 + D - F), (5010, top(4600) - t * 270 + D), (4740, top(4600) + D)], c["viga"]))
    linea = rect(78, 1109, 20, 720, c["linea"]) + rect(78, 1809, 4522, 20, c["linea"])
    body = acero + oscuro + linea + f'<g fill="{c["metal"]}">{METAL}</g><g fill="{c["hervas"]}">{HERVAS}</g>'
    return svg("0 0 5040 1840", body, "Metal Hervás — variante 1, Fiel")

def v1_simbolo(c):
    return svg("0 0 1100 1100", rect(0, 0, 1100, 1100, c["fondo"]) + f'<g transform="translate(-355 -690)" fill="{c["letra"]}">{LETRA_H}</g>',
               "Metal Hervás — símbolo 1")

# =====================================================================
# 2 · LA TILDE ES UNA VIGA — la tilde de la Á es un tramo de perfil I a 30°
# =====================================================================
def tilde(cx, cy, c, largo=520, canto=200):
    a = math.radians(-30); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    x0 = cx - ux * largo / 2 - nx * canto / 2; y0 = cy - uy * largo / 2 - ny * canto / 2
    return viga(x0, y0, largo, canto, -30, 52, c["acero"], c["viga"])

def v2(c):
    body = (f'<g fill="{c["metal"]}">{METAL}</g><g fill="{c["hervas"]}">{HERVAS_SIN_TILDE}</g>' + tilde(3505, 700, c))
    return svg("0 0 4420 1640", body, "Metal Hervás — variante 2, La tilde es una viga")

def v2_simbolo(c):
    body = (rect(2905, 480, 1200, 1200, c["fondo"]) + f'<g fill="{c["letra"]}">{LETRA_A}</g>' + tilde(3505, 700, c))
    return svg("2905 480 1200 1200", body, "Metal Hervás — símbolo 2")

# =====================================================================
# 3 · PLACA DE FABRICANTE — el logo estampado en una placa remachada
# =====================================================================
def placa(w, h, c, borde=110, aro=30, r_rem=55, ins_rem=230):
    anillo = (f'<path fill="{c["aro"]}" fill-rule="evenodd" d="M{borde} {borde}H{w-borde}V{h-borde}H{borde}Z'
              f'M{borde+aro} {borde+aro}V{h-borde-aro}H{w-borde-aro}V{borde+aro}Z"/>')
    remaches = "".join(f'<circle fill="{c["aro"]}" cx="{x}" cy="{y}" r="{r_rem}"/>'
                       for x in (ins_rem, w - ins_rem) for y in (ins_rem, h - ins_rem))
    return f'<rect fill="{c["placa"]}" width="{w}" height="{h}" rx="{borde * 0.6:g}"/>' + anillo + remaches

def v3(c):
    W, H = 5200, 2090
    body = placa(W, H, c) + (f'<g transform="translate(391 214)"><g fill="{c["metal_placa"]}">{METAL}</g>'
                             f'<g fill="{c["hervas"]}">{HERVAS}</g></g>')
    return svg(f"0 0 {W} {H}", body, "Metal Hervás — variante 3, Placa de fabricante")

def v3_simbolo(c):
    body = placa(1100, 1100, c, borde=70, aro=26, r_rem=40, ins_rem=150) + f'<g transform="translate(-355 -690)" fill="{c["hervas"]}">{LETRA_H}</g>'
    return svg("0 0 1100 1100", body, "Metal Hervás — símbolo 3")

# =====================================================================
# 4 · NAVE — la viga cubre el nombre como una cubierta y lleva «METAL» en el alma
# =====================================================================
def v4(c):
    ang, D = 15, 430
    t = math.tan(math.radians(ang)); x0, y0 = 1250, 10
    colx, colw = 4560, 220
    largo = (colx - x0) / math.cos(math.radians(ang))
    beam = viga(x0, y0, largo, D, ang, 0.1, c["viga"], c["viga"])
    juntas = (viga(x0, y0 + 70, largo, 14, ang, 0.1, c["acero"], c["acero"])
              + viga(x0, y0 + D - 84, largo, 14, ang, 0.1, c["acero"], c["acero"]))
    pilar = rect(colx, 0, colw, 2200, c["viga"]) + rect(colx + 56, 0, 14, 2200, c["acero"]) + rect(colx + colw - 70, 0, 14, 2200, c["acero"])
    size = 240; d, w = texto("METAL", size, 0, 0, tracking=size * 0.28)
    ch = cap_height(size)
    a = math.radians(ang); s0 = 330
    px = x0 + math.cos(a) * s0 - math.sin(a) * (D / 2 + ch / 2)
    py = y0 + math.sin(a) * s0 + math.cos(a) * (D / 2 + ch / 2)
    rotulo = f'<path fill="{c["rotulo"]}" transform="translate({px:.1f} {py:.1f}) rotate({ang})" d="{d}"/>'
    linea = rect(78, 1489, 20, 711, c["linea"]) + rect(78, 2180, colx - 78, 20, c["linea"])
    body = (beam + juntas + pilar + rotulo + linea
            + f'<g transform="translate(0 420)" fill="{c["hervas"]}">{HERVAS}</g>')
    return svg("0 0 4800 2200", body, "Metal Hervás — variante 4, Nave")

def v4_simbolo(c):
    largo = 1000 / math.cos(math.radians(15))
    body = (rect(0, 0, 1100, 1100, c["fondo"])
            + viga(40, 60, largo, 160, 15, 0.1, c["viga"], c["viga"])
            + f'<g transform="translate(-173.8 -229.2) scale(0.8)" fill="{c["letra"]}">{LETRA_H}</g>')
    return svg("0 0 1100 1100", body, "Metal Hervás — símbolo 4")

# =====================================================================
# 5 · FIRMA DE TALLER — la línea se convierte en un cordón de soldadura
# =====================================================================
def cordon(x0, x1, y, alto=130, paso=110, r=60):
    base = y + alto; cresta = y + 50
    d = f"M{x0} {base}V{cresta}"
    x = x0
    while x + paso <= x1:
        d += f"A{r} {r} 0 0 1 {x + paso} {cresta}"; x += paso
    return d + f"V{base}Z"

def v5(c):
    body = (f'<g fill="{c["metal"]}">{METAL}</g><g fill="{c["hervas"]}">{HERVAS}</g>'
            f'<path fill="{c["cordon"]}" d="{cordon(560, 4420, 1690)}"/>')
    return svg("0 0 4440 1820", body, "Metal Hervás — variante 5, Firma de taller")

def v5_simbolo(c):
    body = (rect(0, 0, 1100, 1100, c["fondo"]) + f'<g transform="translate(160 110) scale(0.86)" fill="{c["letra"]}"><g transform="translate(-29 -36)">{M_SCRIPT}</g></g>'
            f'<path fill="{c["letra"]}" d="{cordon(165, 935, 860, alto=140, paso=110, r=60)}"/>')
    return svg("0 0 1100 1100", body, "Metal Hervás — símbolo 5")

# ---------- colores ----------
CLARO = dict(metal=NEGRO, hervas=VERDE, linea=NEGRO, viga=NEGRO, acero=ACERO, cordon=NEGRO, rotulo=BLANCO,
             placa=NEGRO, aro=ACERO, metal_placa=BLANCO)
OSCURO = dict(metal=BLANCO, hervas=VERDE, linea=BLANCO, viga="#E6E6E6", acero="#7A7A7A", cordon=BLANCO, rotulo=NEGRO,
              placa="#232826", aro="#8C8C8C", metal_placa=BLANCO)
NEGRO1 = dict(metal="#000", hervas="#000", linea="#000", viga="#000", acero="#000", cordon="#000", rotulo="#FFF",
              placa="#000", aro="#FFF", metal_placa="#FFF")
SIMB = {1: dict(fondo=VERDE, letra=BLANCO), 2: dict(fondo=VERDE, letra=BLANCO, viga=NEGRO, acero=ACERO),
        3: dict(placa=NEGRO, aro=ACERO, hervas=VERDE), 4: dict(fondo=VERDE, viga=NEGRO, letra=BLANCO), 5: dict(fondo=VERDE, letra=BLANCO)}
SIMB_NEGRO = {1: dict(fondo="#FFF", letra="#000"), 2: dict(fondo="#FFF", letra="#000", viga="#000", acero="#000"),
              3: dict(placa="#000", aro="#FFF", hervas="#FFF"), 4: dict(fondo="#FFF", viga="#000", letra="#000"), 5: dict(fondo="#FFF", letra="#000")}

LOCK = {1: v1, 2: v2, 3: v3, 4: v4, 5: v5}
SYM = {1: v1_simbolo, 2: v2_simbolo, 3: v3_simbolo, 4: v4_simbolo, 5: v5_simbolo}

if __name__ == "__main__":
    for n in LOCK:
        for tono, col in (("color", CLARO), ("negativo", OSCURO), ("negro", NEGRO1)):
            (OUT / f"v{n}-lockup-{tono}.svg").write_text(LOCK[n](col), encoding="utf-8")
        (OUT / f"v{n}-simbolo-color.svg").write_text(SYM[n](SIMB[n]), encoding="utf-8")
        (OUT / f"v{n}-simbolo-negro.svg").write_text(SYM[n](SIMB_NEGRO[n]), encoding="utf-8")
    print(sorted(p.name for p in OUT.glob("*.svg")))
