"""Propuestas de logo A, B y C para Metal Hervás.

Genera SVG sueltos en prototipos/assets/logo/propuestas/ y un JSON con las piezas
que usan los artboards del tablero de Claude Design.

- A · Limpieza: los trazados originales del logo verde (scripts/trace_logo.py) sin «S.L.»,
  sin restos grises dentro de las letras y con la viga redibujada en plano.
- B · Evolución: símbolo = sección real de un perfil HD 400 × 1086 (ArcelorMittal) girada,
  que se lee como una H. Wordmark METAL / HERVÁS en Archivo expandida.
- C · Rebranding: símbolo de marco (ventana / pórtico) y wordmark en minúsculas,
  con el verde oscuro como color principal.
"""
import json, re, pathlib

LOGO = pathlib.Path("prototipos/assets/logo")
OUT = LOGO / "propuestas"; OUT.mkdir(exist_ok=True)

# ---------- A · piezas del logo trazado ----------
src = (LOGO / "logo-color.svg").read_text(encoding="utf-8")
paths = re.findall(r'<path fill="([^"]+)" transform="translate\(([^ ]+) ([^)]+)\)" d="([^"]*)"', src)
def grupo(idx):
    return "".join(f'<path transform="translate({paths[i][1]} {paths[i][2]})" d="{paths[i][3]}"/>' for i in idx)
A_METAL = grupo([11, 12, 13, 15, 16])
A_HERVAS = grupo([0, 1, 2, 3, 4, 5, 6])
A_LINEA = grupo([18])
# Viga en plano (coordenadas del trazado, 5040 × 1980): pilar, viga inclinada y ménsula
A_ACERO = ('<rect x="4600" y="0" width="140" height="1840"/>'
           '<polygon points="3240,0 3500,0 4600,500 4600,660"/>'
           '<polygon points="4740,560 5010,470 5010,610 4740,700"/>')
A_VIGA = ('<rect x="4600" y="0" width="34" height="1840"/><rect x="4706" y="0" width="34" height="1840"/>'
          '<polygon points="3240,0 3420,0 4600,520 4600,560"/>'
          '<polygon points="4740,560 5010,470 5010,500 4740,590"/>')
A_VB = "0 0 5040 1860"

def svg_a(c):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{A_VB}">'
            f'<g fill="{c["acero"]}">{A_ACERO}</g><g fill="{c["viga"]}">{A_VIGA}</g>'
            f'<g fill="{c["linea"]}">{A_LINEA}</g><g fill="{c["metal"]}">{A_METAL}</g>'
            f'<g fill="{c["hervas"]}">{A_HERVAS}</g></svg>')

# ---------- B · sección HD 400 × 1086 girada (h 569, b 454, tw 78, tf 125, r 15) ----------
def seccion_h(x0, y0, alto):
    s = alto / 454
    W, H, tf, tw, r = 569 * s, 454 * s, 125 * s, 78 * s, 15 * s
    yw1, yw2 = (H - tw) / 2, (H + tw) / 2
    f = lambda v: f"{v:.2f}"
    return (f"M{f(x0)} {f(y0)}H{f(x0+tf)}V{f(y0+yw1-r)}A{f(r)} {f(r)} 0 0 0 {f(x0+tf+r)} {f(y0+yw1)}"
            f"H{f(x0+W-tf-r)}A{f(r)} {f(r)} 0 0 0 {f(x0+W-tf)} {f(y0+yw1-r)}V{f(y0)}H{f(x0+W)}V{f(y0+H)}"
            f"H{f(x0+W-tf)}V{f(y0+yw2+r)}A{f(r)} {f(r)} 0 0 0 {f(x0+W-tf-r)} {f(y0+yw2)}"
            f"H{f(x0+tf+r)}A{f(r)} {f(r)} 0 0 0 {f(x0+tf)} {f(y0+yw2+r)}V{f(y0+H)}H{f(x0)}Z"), W

# La sección hace de «H» de HERVÁS: misma altura que las mayúsculas de Archivo 800 a 190px (131 u.)
B_CAP = 131
B_SIM, B_SIM_W = seccion_h(0, 270 - B_CAP, B_CAP)
FONT = "Archivo, 'Arial Black', sans-serif"
B_VB = "0 50 1000 230"

def svg_b(c):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{B_VB}">'
            f'<text x="2" y="110" fill="{c["metal"]}" '
            f'style="font-family:{FONT};font-stretch:125%;font-weight:600;font-size:50px;letter-spacing:15px">METAL</text>'
            f'<path fill="{c["simbolo"]}" d="{B_SIM}"/>'
            f'<text x="{B_SIM_W + 10:.0f}" y="270" fill="{c["hervas"]}" '
            f'style="font-family:{FONT};font-stretch:125%;font-weight:800;font-size:190px;letter-spacing:-2px">ERVÁS</text>'
            f'</svg>')

def tile_b(c):
    d, w = seccion_h(0, 0, 100)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="{c["fondo"]}"/>'
            f'<path transform="translate({(200-w)/2:.2f} 50)" fill="{c["simbolo"]}" d="{d}"/></svg>')

# ---------- C · marco ----------
def portico(x0, y0, L):
    """Pórtico: dos pilares y una viga (estructura) con un vidrio dentro (ventana). Base abierta, sobre el suelo."""
    k = L / 240
    r = lambda x, y, w, h: f"M{x0+x*k:.2f} {y0+y*k:.2f}h{w*k:.2f}v{h*k:.2f}h{-w*k:.2f}Z"
    estructura = r(0, 0, 240, 46) + r(0, 46, 46, 194) + r(194, 46, 46, 194)
    vidrio = r(66, 66, 108, 174)
    return estructura, vidrio

C_MARCO, C_PANE = portico(0, 30, 240)

def svg_c(c):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1330 300">'
            f'<path fill="{c["marco"]}" d="{C_MARCO}"/><path fill="{c["pane"]}" d="{C_PANE}"/>'
            f'<text x="292" y="270" '
            f'style="font-family:{FONT};font-stretch:100%;font-weight:700;font-size:168px;letter-spacing:-3px">'
            f'<tspan fill="{c["metal"]}">metal </tspan><tspan fill="{c["hervas"]}">hervás</tspan></text></svg>')

def tile_c(c):
    m, p = portico(44, 40, 112)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect width="200" height="200" fill="{c["fondo"]}"/>'
            f'<path fill="{c["marco"]}" d="{m}"/><path fill="{c["pane"]}" d="{p}"/></svg>')

COL = {
    "A": {"claro": dict(metal="#111111", hervas="#4BA939", linea="#111111", viga="#151515", acero="#A0A0A0"),
          "oscuro": dict(metal="#FFFFFF", hervas="#4BA939", linea="#FFFFFF", viga="#E6E6E6", acero="#7A7A7A")},
    "B": {"claro": dict(simbolo="#151515", metal="#151515", hervas="#4BA939"),
          "oscuro": dict(simbolo="#FFFFFF", metal="#FFFFFF", hervas="#4BA939"),
          "tile": dict(fondo="#4BA939", simbolo="#151515")},
    "C": {"claro": dict(marco="#256A31", pane="#87D2A9", metal="#141815", hervas="#256A31"),
          "oscuro": dict(marco="#87D2A9", pane="#4BA939", metal="#FFFFFF", hervas="#87D2A9"),
          "tile": dict(fondo="#256A31", marco="#FFFFFF", pane="#87D2A9")},
}

if __name__ == "__main__":
    files = {
        "A-claro.svg": svg_a(COL["A"]["claro"]), "A-oscuro.svg": svg_a(COL["A"]["oscuro"]),
        "B-claro.svg": svg_b(COL["B"]["claro"]), "B-oscuro.svg": svg_b(COL["B"]["oscuro"]), "B-simbolo.svg": tile_b(COL["B"]["tile"]),
        "C-claro.svg": svg_c(COL["C"]["claro"]), "C-oscuro.svg": svg_c(COL["C"]["oscuro"]), "C-simbolo.svg": tile_c(COL["C"]["tile"]),
    }
    for n, s in files.items():
        (OUT / n).write_text(s, encoding="utf-8"); print(n, len(s) // 1024, "KB")
    json.dump({"B_VB": B_VB, "B_CAP": B_CAP, "A_VB": A_VB, "A_METAL": A_METAL, "A_HERVAS": A_HERVAS, "A_LINEA": A_LINEA, "A_ACERO": A_ACERO,
               "A_VIGA": A_VIGA, "B_SIM": B_SIM, "B_SIM_W": B_SIM_W, "C_MARCO": C_MARCO, "C_PANE": C_PANE},
              open(OUT / "piezas.json", "w", encoding="utf-8"))
