"""Cinco propuestas EVOLUTIVAS del logo de Metal Hervás (línea de la propuesta B).

Se mantienen el verde #4BA939 y «HERVÁS» en mayúsculas anchas; la letra pasa a Archivo
(ancho 125) convertida a trazados; cada propuesta añade una idea propia:
  E1 Nudo         · símbolo = el cruce pilar-viga del logo original
  E2 Herencia     · «Metal» caligráfico original como acento sobre HERVÁS moderno
  E3 Escuadra     · une la marca con la submarca VENTANAS de PVC (escuadra + cuadros)
  E4 Tilde-viga   · la tilde de la Á es un tramo de perfil I
  E5 Línea de corte · un corte horizontal atraviesa las letras y sigue como línea de nivel
Salida: prototipos/assets/logo/evolucion/e{1..5}-{lockup-color,lockup-negativo,simbolo-color}.svg
"""
import math, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import logo_propuestas as lp
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

OUT = pathlib.Path("prototipos/assets/logo/evolucion"); OUT.mkdir(parents=True, exist_ok=True)
VERDE, OSCURO, MEDIO, MENTA, NEGRO, ACERO, BLANCO = "#4BA939", "#256A31", "#28A360", "#87D2A9", "#151515", "#A0A0A0", "#FFFFFF"

_fonts = {}
def font(wght, wdth=125):
    k = (wght, wdth)
    if k not in _fonts:
        _fonts[k] = instantiateVariableFont(TTFont("scripts/fonts/Archivo-VF.ttf"), {"wdth": wdth, "wght": wght})
    return _fonts[k]

def texto(txt, size, x, base, tracking=0.0, wght=800):
    """Devuelve (d, ancho, posiciones x de cada letra)."""
    f = font(wght); gs, cmap, upm = f.getGlyphSet(), f.getBestCmap(), f["head"].unitsPerEm
    k = size / upm; pen = SVGPathPen(gs); cx = 0.0; xs = []
    for ch in txt:
        gn = cmap[ord(ch)]; xs.append(x + cx)
        gs[gn].draw(TransformPen(pen, (k, 0, 0, -k, x + cx, base)))
        cx += gs[gn].width * k + tracking
    return pen.getCommands(), cx - tracking, xs

def cap(size, wght=800):
    f = font(wght); return f["OS/2"].sCapHeight / f["head"].unitsPerEm * size

def poly(pts, fill):
    return f'<polygon fill="{fill}" points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>'
def rect(x, y, w, h, fill):
    return f'<rect fill="{fill}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/>'
def svg(vb, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="t"><title id="t">{title}</title>{body}</svg>'

# ---------- bloque de palabra común: METAL espaciado sobre HERVÁS ----------
HS, MS = 220, 86                  # cuerpo de HERVÁS y de METAL
HB = 300                          # línea base de HERVÁS
HCAP = cap(HS); HTOP = HB - HCAP
MB = HTOP - 46                    # línea base de METAL
MTOP = MB - cap(MS, 600)

def palabra(x, c, sin_tilde=False):
    dm, wm, _ = texto("METAL", MS, x + 4, MB, tracking=MS * 0.38, wght=600)
    dh, wh, xs = texto("HERVAS" if sin_tilde else "HERVÁS", HS, x, HB, tracking=-3)
    return (f'<path fill="{c["metal"]}" d="{dm}"/><path fill="{c["hervas"]}" d="{dh}"/>'), wh, xs

# ---------- el nudo del original (pilar + viga + ménsula), en un cuadro de 256 ----------
def nudo(c, fill_key="viga"):
    t = math.tan(math.radians(22.5)); colx, colw, yj, D = 150, 44, 96, 44
    f = c[fill_key]
    return (rect(colx, -10, colw, 276, f) + poly([(0, yj - t * colx), (colx, yj), (colx, yj + D), (0, yj - t * colx + D)], f)
            + poly([(colx + colw, yj), (256, yj - t * (256 - colx - colw)), (256, yj - t * (256 - colx - colw) + D * .8), (colx + colw, yj + D * .8)], f))

def viga_I(cx, cy, largo, canto, ang, ala, c):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    x0 = cx - ux * largo / 2 - nx * canto / 2; y0 = cy - uy * largo / 2 - ny * canto / 2
    P = lambda s, q: (x0 + ux * s + nx * q, y0 + uy * s + ny * q)
    return (poly([P(0, 0), P(largo, 0), P(largo, canto), P(0, canto)], c["acero"])
            + poly([P(0, 0), P(largo, 0), P(largo, ala), P(0, ala)], c["viga"])
            + poly([P(0, canto - ala), P(largo, canto - ala), P(largo, canto), P(0, canto)], c["viga"]))

# =========================== E1 · NUDO ===========================
def e1(c):
    T = HB - MTOP; tile = (f'<g transform="translate(0 {MTOP:.1f}) scale({T/256:.4f})">'
                           f'<rect width="256" height="256" fill="{c["tile"]}"/>{nudo(c)}</g>')
    w, wh, _ = palabra(T + 60, c)
    return svg(f"-10 {MTOP-10:.0f} {T+60+wh+20:.0f} {T+20:.0f}", tile + w, "Metal Hervás — E1 Nudo")
def e1_sim(c):
    return svg("0 0 256 256", f'<rect width="256" height="256" fill="{c["tile"]}"/>' + nudo(c), "Símbolo E1")

# =========================== E2 · HERENCIA ===========================
METAL_SCRIPT = lp.grupo([11, 12, 13, 15, 16])
def e2(c):
    dh, wh, _ = texto("HERVÁS", HS, 0, HB, tracking=-3)
    k = (wh * 0.47) / 2173            # «Metal» ocupa el 47 % del ancho de HERVÁS
    sx, sy = -29 * k - 6, HTOP - 856 * k - 6   # su base pisa ligeramente la cabeza de HERVÁS
    script = f'<g transform="translate({sx:.1f} {sy:.1f}) scale({k:.5f})" fill="{c["metal"]}">{METAL_SCRIPT}</g>'
    linea = rect(-40, HB + 34, wh + 40, 10, c["metal"]) + rect(-40, HTOP + 40, 10, HB + 44 - HTOP - 40, c["metal"])
    top = sy + 36 * k
    body = linea + f'<path fill="{c["hervas"]}" d="{dh}"/>' + script
    return svg(f"-60 {top-20:.0f} {wh+80:.0f} {HB+64-top:.0f}", body, "Metal Hervás — E2 Herencia")
M_SCRIPT = lp.grupo([11])
def e2_sim(c):
    return svg("0 0 256 256", f'<rect width="256" height="256" fill="{c["tile"]}"/>'
               f'<g transform="translate(38 30) scale(0.215)" fill="{c["tile_ink"]}"><g transform="translate(-29 -36)">{M_SCRIPT}</g></g>'
               + rect(30, 214, 196, 12, c["tile_ink"]), "Símbolo E2")

# =========================== E3 · ESCUADRA ===========================
def cuadros(x, y, s, gap, c):
    return (rect(x, y, s, s, c["menta"]) + rect(x, y + s + gap, s, s, c["menta"])
            + rect(x + s + gap, y, s, s, c["medio"]) + rect(x + s + gap, y + s + gap, s, s, c["medio"]))
def e3(c):
    T = HB - MTOP; s = (T - 40) / 2 * 0.62; g = s * 0.14; bar = s * 0.42
    x0 = 0; xq = x0; yq = HB - (2 * s + g)
    xb = xq + 2 * s + g + g * 2                       # montante de la escuadra
    escuadra = (rect(x0, MTOP, xb + bar - x0, bar, c["oscuro"]) + rect(xb, MTOP, bar, HB - MTOP + bar * 0 , c["oscuro"]))
    w, wh, _ = palabra(xb + bar + 50, c)
    base = rect(xb, HB + 30, (xb + bar + 50 + wh) - xb, bar, c["oscuro"])
    body = escuadra + base + cuadros(xq, yq + 0, s, g, c) + w
    return svg(f"-10 {MTOP-10:.0f} {xb+bar+50+wh+20:.0f} {HB+30+bar-MTOP+20:.0f}", body, "Metal Hervás — E3 Escuadra")
def e3_sim(c):
    s, g, bar = 70, 10, 24
    body = (f'<rect width="256" height="256" fill="{c["tile"]}"/>'
            + rect(36, 36, 2 * s + g + 14 + bar, bar, c["oscuro"]) + rect(36 + 2 * s + g + 14, 36, bar, 184, c["oscuro"])
            + cuadros(36, 70, s, g, c))
    return svg("0 0 256 256", body, "Símbolo E3")

# =========================== E4 · TILDE-VIGA ===========================
def e4(c):
    w, wh, xs = palabra(0, c, sin_tilde=True)
    _, wa, _ = texto("A", HS, 0, 0)
    cx = xs[4] + wa / 2 + 14; cy = HTOP - 44
    body = w + viga_I(cx, cy, 150, 60, -30, 16, c)
    top = min(MTOP, cy - 80)
    return svg(f"-10 {top-10:.0f} {wh+20:.0f} {HB-top+20:.0f}", body, "Metal Hervás — E4 Tilde-viga")
def e4_sim(c):
    da, wa, _ = texto("A", 150, 0, 0)
    x = (256 - wa) / 2; base = 222
    body = (f'<rect width="256" height="256" fill="{c["tile"]}"/><path fill="{c["tile_ink"]}" transform="translate({x:.1f} {base})" d="{da}"/>'
            + viga_I(128 + 10, base - cap(150) - 40, 120, 44, -30, 12, c))
    return svg("0 0 256 256", body, "Símbolo E4")

# =========================== E5 · LÍNEA DE CORTE ===========================
def e5(c, uid):
    w, wh, _ = palabra(0, c)
    yc = HTOP + HCAP * 0.30; gap = 16
    clip = (f'<clipPath id="corte{uid}"><path clip-rule="evenodd" d="M-200 -200H{wh+400}V{yc:.1f}H-200Z'
            f'M-200 {yc+gap:.1f}H{wh+400}V{HB+200}H-200Z"/></clipPath>')
    linea = rect(-120, yc + gap / 2 - 4, 90, 8, c["metal"]) + rect(wh + 30, yc + gap / 2 - 4, 90, 8, c["metal"])
    body = f'<defs>{clip}</defs><g clip-path="url(#corte{uid})">{w}</g>' + linea
    return svg(f"-130 {MTOP-10:.0f} {wh+260:.0f} {HB-MTOP+20:.0f}", body, "Metal Hervás — E5 Línea de corte")
def e5_sim(c):
    dh, wh, _ = texto("H", 170, 0, 0)
    x = (256 - wh) / 2; base = 128 + cap(170) / 2; yc = 128 - cap(170) * 0.22
    body = (f'<defs><clipPath id="cs"><path clip-rule="evenodd" d="M0 0H256V{yc}H0ZM0 {yc+14}H256V256H0Z"/></clipPath></defs>'
            f'<rect width="256" height="256" fill="{c["tile"]}"/><g clip-path="url(#cs)"><path fill="{c["tile_ink"]}" transform="translate({x:.1f} {base:.1f})" d="{dh}"/></g>'
            + rect(14, yc + 3, x - 26, 8, c["tile_ink"]) + rect(x + wh + 12, yc + 3, 256 - (x + wh + 12) - 14, 8, c["tile_ink"]))
    return svg("0 0 256 256", body, "Símbolo E5")

CLARO = dict(metal=NEGRO, hervas=VERDE, viga=NEGRO, acero=ACERO, tile=VERDE, tile_ink=BLANCO, oscuro=OSCURO, medio=MEDIO, menta=MENTA)
NEG = dict(metal=BLANCO, hervas=VERDE, viga="#E6E6E6", acero="#7A7A7A", tile=VERDE, tile_ink=BLANCO, oscuro=MENTA, medio=MEDIO, menta="#4BA939")
SIM = {1: dict(CLARO), 2: dict(CLARO), 3: dict(CLARO, tile=BLANCO), 4: dict(CLARO), 5: dict(CLARO)}

if __name__ == "__main__":
    LOCK = {1: e1, 2: e2, 3: e3, 4: e4, 5: lambda c: e5(c, "a" if c is CLARO else "b")}
    SYMS = {1: e1_sim, 2: e2_sim, 3: e3_sim, 4: e4_sim, 5: e5_sim}
    for n in LOCK:
        (OUT / f"e{n}-lockup-color.svg").write_text(LOCK[n](CLARO), encoding="utf-8")
        (OUT / f"e{n}-lockup-negativo.svg").write_text(LOCK[n](NEG), encoding="utf-8")
        (OUT / f"e{n}-simbolo-color.svg").write_text(SYMS[n](SIM[n]), encoding="utf-8")
    print(sorted(p.name for p in OUT.glob("*.svg")))
