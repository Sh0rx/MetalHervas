"""Genera Proveedores/diagrama_proveedores.drawio: MetalHervas -> tipo -> proveedor -> familias.

Lo que MetalHervas trabaja según la nota del tío (Proveedores/Proveedores.jpeg) se marca con una etiqueta
verde «✔ MetalHervas» y borde grueso; lo que no figura en la nota sale en gris y con borde discontinuo.
El texto se corta en líneas midiendo su ancho real con Arial (la fuente de la exportación de draw.io),
así cada caja tiene el alto justo y nada se sale.

Uso: .venv\\Scripts\\python.exe scraping\\build_diagram.py
Exportar a PNG (draw.io Desktop):
  "C:\\Program Files\\draw.io\\draw.io.exe" -x -f png -e -b 20 -s 2 -o Proveedores\\diagrama_proveedores.drawio.png Proveedores\\diagrama_proveedores.drawio
"""
import json
import sys
from html import escape
from pathlib import Path

from PIL import ImageFont

sys.stdout.reconfigure(encoding="utf-8")
PROV = Path(__file__).resolve().parent.parent / "Proveedores"
RAW = PROV / "raw"

FONT = "Arial"
_fonts = {}


def text_w(text: str, size: int, bold: bool = False) -> float:
    key = (size, bold)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", size)
    return _fonts[key].getlength(text)


COLORS = {  # relleno, borde, texto
    "root": ("#37474F", "#263238", "#FFFFFF"),
    "cat": ("#ECEFF1", "#607D8B", "#263238"),
    "gealan": ("#E3F2FD", "#1565C0", "#0D47A1"),
    "aluval": ("#FFF3E0", "#EF6C00", "#BF360C"),
    "extrugasa": ("#E8F5E9", "#2E7D32", "#1B5E20"),
    "sg": ("#F3E5F5", "#7B1FA2", "#4A148C"),
    "off": ("#FAFAFA", "#BDBDBD", "#9E9E9E"),
    "ok": ("#2E7D32", "#1B5E20", "#FFFFFF"),
    "note": ("#E8F5E9", "#2E7D32", "#1B5E20"),
}
COL_W, GAP, LEAF_INDENT, LEAF_GAP = 300, 46, 26, 22
PAD_L, PAD_R, PAD_T, PAD_B, SLACK = 10, 10, 14, 10, 10  # márgenes internos y holgura de medida
TITLE_PX, BODY_PX, LH = 13, 11, 1.3  # tamaños de letra y alto de línea relativo

cells: list[str] = []
_id = [1]


def nid() -> str:
    _id[0] += 1
    return f"n{_id[0]}"


def wrap_words(text: str, width: float, size: int, bold: bool = False) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        cand = f"{cur} {word}" if cur else word
        if cur and text_w(cand, size, bold) > width:
            lines.append(cur)
            cur = word
        else:
            cur = cand
    return lines + ([cur] if cur else [])


def wrap_items(items: list[str], width: float, size: int) -> list[str]:
    """Une los elementos con ' · ' sin pasarse de `width` píxeles; corta por palabras si uno no cabe.
    Un elemento que empieza por '¶' siempre arranca línea nueva."""
    lines, cur = [], ""
    for it in items:
        if it.startswith("¶"):
            it = it[1:]
            if cur:
                lines.append(cur)
                cur = ""
        cand = f"{cur} · {it}" if cur else it
        if text_w(cand, size) <= width:
            cur = cand
            continue
        if cur:
            lines.append(cur)
        parts = wrap_words(it, width, size)
        lines += parts[:-1]
        cur = parts[-1]
    return lines + ([cur] if cur else [])


def cell(x, y, w, h, html, style, cid=None):
    i = cid or nid()
    cells.append(f'<mxCell id="{i}" value="{escape(html, quote=True)}" style="{style}" vertex="1" parent="1">'
                 f'<mxGeometry x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" as="geometry"/></mxCell>')
    return i


def box(x, y, w, h, html, kind, size=12, stroke_w=1.5, align="center", dashed=False):
    fill, stroke, font = COLORS[kind]
    valign = "verticalAlign=middle;" if align == "center" else f"verticalAlign=top;spacingTop={PAD_T - 4};"
    style = (f"rounded=1;whiteSpace=wrap;html=1;arcSize=6;fillColor={fill};strokeColor={stroke};fontColor={font};"
             f"fontFamily={FONT};fontSize={size};align={align};{valign}spacingLeft={PAD_L};spacingRight={PAD_R};"
             f"strokeWidth={stroke_w};" + ("dashed=1;dashPattern=6 4;" if dashed else ""))
    return cell(x, y, w, h, html, style)


def badge(x_right, y_top, text="✔ MetalHervas"):
    w = text_w(text, 10, True) + 18
    style = (f"rounded=1;arcSize=50;html=1;fillColor={COLORS['ok'][0]};strokeColor={COLORS['ok'][1]};"
             f"fontColor=#FFFFFF;fontFamily={FONT};fontSize=10;fontStyle=1;align=center;verticalAlign=middle;")
    return cell(x_right - w - 10, y_top - 10, w, 20, escape(text), style)


def edge(src, dst, color, style_extra, dashed=False):
    cells.append(f'<mxCell id="{nid()}" style="edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=none;html=1;'
                 f'strokeColor={color};strokeWidth=1.5;{"dashed=1;" if dashed else ""}{style_extra}" edge="1" '
                 f'parent="1" source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry"/></mxCell>')


def leaf(x, y, w, title, items, kind, worked, highlight=()):
    """Caja de familia: título en negrita + lista. Devuelve (id, alto)."""
    inner = w - PAD_L - PAD_R - SLACK
    k = kind if worked else "off"
    t_lines = wrap_words(title, inner - (0 if worked else 0), TITLE_PX, True)
    b_lines = wrap_items(items, inner, BODY_PX)
    extra = [] if worked else ["No figura en la nota"]
    h = PAD_T + TITLE_PX * LH * len(t_lines) + 4 + BODY_PX * LH * (len(b_lines) + len(extra)) + PAD_B

    def fmt(line):
        s = escape(line)
        for hl in highlight:  # resalta dentro de la caja lo que la nota nombra expresamente
            s = s.replace(escape(hl), f"<b><u>{escape(hl)}</u></b>")
        return s

    html = (f"<b style='font-size:{TITLE_PX}px'>{'<br>'.join(escape(t) for t in t_lines)}</b>"
            f"<div style='font-size:{BODY_PX}px;margin-top:4px'>{'<br>'.join(fmt(l) for l in b_lines)}"
            + (f"<br><i>{extra[0]}</i>" if extra else "") + "</div>")
    i = box(x, y, w, h, html, k, size=BODY_PX, stroke_w=2.5 if worked else 1.2, align="left", dashed=not worked)
    if worked:
        badge(x + w, y)
    return i, h


def column(col: int, supplier: str, subtitle: str, kind: str, families, top: int):
    """Proveedor arriba y sus familias apiladas debajo, unidas por un 'peine' a la izquierda."""
    x = col * (COL_W + GAP)
    fill, stroke, font = COLORS[kind]
    sup = box(x, top, COL_W, 62,
              f"<b style='font-size:16px'>{escape(supplier)}</b><br>"
              f"<span style='font-size:11px;color:{COLORS['ok'][0]}'><b>{escape(subtitle)}</b></span>",
              kind, size=12, stroke_w=2.5)
    y = top + 62 + 30
    links = []
    for fam in families:
        title, items, worked = fam[:3]
        hl = fam[3] if len(fam) > 3 else ()
        lid, h = leaf(x + LEAF_INDENT, y, COL_W - LEAF_INDENT, title, items, kind, worked, hl)
        links.append((worked, lid))
        y += h + LEAF_GAP
    for worked, lid in sorted(links, key=lambda t: t[0]):  # discontinuas debajo, continuas encima
        edge(sup, lid, stroke if worked else COLORS["off"][1],
             "exitX=0.04;exitY=1;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;", dashed=not worked)
    return sup, x, y


# ------------------------------------------------------------------ datos
# (título, elementos, ¿lo trabaja MetalHervas según la nota?, [textos a resaltar dentro])
gealan = [
    ("S 8000 IQ (en la web: S 8000)", ["74 mm", "5 o 6 cámaras", "Uf ≤ 1,2", "vidrio hasta 50 mm", "ventanas y puertas"], True),
    ("S 9000 IQ (en la web: S 9000)", ["82,5 mm", "Uf ≤ 0,89", "ventanas, puertas, elevadora", "variantes FUTURA® y LUMAXX®"], True),
    ("GEALAN-LINEAR®", ["74 mm", "Uf ≤ 1,0", "ventanas, puertas, correderas", "LINEAR acrylcolor®",
                        "LUMAXX®", "hoja enrasada", "marco empotrado"], True, ("LINEAR acrylcolor®",)),
    ("Gama de colores", ["acrylcolor®: estándar (9)", "ampliada (9)", "bajo pedido (44 RAL)", "metálicos (6)",
                         "base oscura", "láminas decorativas: estándar, madera, RealWood, lisas, mate y metálicas",
                         "revestimiento de aluminio RAL"], True),
    ("Otros sistemas Gealan", ["KONTUR®", "KUBUS®", "SMOOVE multislide", "Corredera 74 mm", "SMOOVIO®"], False),
    ("Complementos Gealan", ["Umbral estándar", "COMFORT®", "CAIRE® (ventilación)", "windowfit",
                             "Hafen-City-Fenster®", "STV®", "IKD®", "BALANCE"], False),
]

aluval_data = json.loads((RAW / "aluval.json").read_text(encoding="utf-8"))
aluval = [(f"{f['nombre'].strip()} ({len(f['series'])})", [s["nombre"].strip() for s in f["series"]], True)
          for f in aluval_data.values()]
aluval.append(("Acabados y colores", ["17 lacados RAL estándar", "6 texturados", "26 efectos madera"], True))

ext = json.loads((RAW / "extrugasa.json").read_text(encoding="utf-8"))
extrugasa = [(f"{c['nombre']} ({len(c['productos'])})", [p["nombre"] for p in c["productos"]], True)
             for c in ext["categorias"]]
extrugasa.append((f"Acabados ({len(ext['acabados'])})", [a["nombre"] for a in ext["acabados"]], True))
extrugasa.append((f"Accesorios ({len(ext['accesorios'])})", ["Manillas Essence: puerta", "Square", "Round",
                                                               "corredera acodada", "corredera con escudo"], True))

# Gamas Climalit tal como las presenta climalit.es (copia de Internet Archive, mayo 2026); «¶» = nueva línea
sg = [
    ("Climalit Basic®", ["Doble y triple acristalamiento", "sin vidrio de capa (la solución más sencilla)"], True),
    ("Climalit Plus® (vidrio con capa)", ["¶Aislamiento térmico: PLANITHERM® 4S", "PLANITHERM® XN",
                                         "¶Luz sin calor: PLANISTAR® ONE", "COOL-LITE® XTREME 61/29",
                                         "¶Silencio: STADIP® SILENCE", "¶Seguridad: STADIP® PROTECT",
                                         "¶Baja emisividad: ECLAZ®"], True),
    ("Climalit ORAÉ® (baja huella de carbono)", ["−35/40 % de CO₂", "¶PLANISTAR® ONE ORAÉ®", "ECLAZ® ZEN ORAÉ®",
                                                 "COOL-LITE® XTREME ORAÉ®"], True),
    ("Muro cortina / no residencial", ["COOL-LITE® SKN 144–183", "COOL-LITE® XTREME 51/23, 61/29 y 70/33",
                                       "COOL-LITE® ST/STB", "COOL-LITE® K"], True),
    ("Vidrio laminado (seguridad y acústica)", ["STADIP®", "STADIP® PROTECT", "STADIP® SILENCE"], True),
    ("Vidrios especiales", ["PRIVA-LITE®", "SageGlass®", "VISION-LITE®", "4BIRD®"], True),
    ("Interiorismo", ["DECORGLASS®", "MASTERGLASS®", "MASTER-SOFT®", "PLANILAQUE® EVOLUTION", "MIRALITE® PURE",
                      "MIRASTAR®"], True),
]

# ------------------------------------------------------------------ layout
ROOT_Y, CAT_Y, SUP_Y = 20, 210, 320
cols = [("GEALAN", "✔ Solo las series marcadas", "gealan", gealan),
        ("ALUVAL", "✔ Todos los modelos", "aluval", aluval),
        ("EXTRUGASA", "✔ Todos los modelos", "extrugasa", extrugasa),
        ("SAINT-GOBAIN · CLIMALIT®", "✔ Todos los modelos", "sg", sg)]
sups, bottoms = [], []
for k, (name, sub, kind, fams) in enumerate(cols):
    sid, x, bottom = column(k, name, sub, kind, fams, SUP_Y)
    sups.append((sid, x))
    bottoms.append(bottom)
TOTAL_W = sups[-1][1] + COL_W


def center(*col_idx):
    xs = [sups[c][1] for c in col_idx]
    return (min(xs) + max(xs) + COL_W) / 2


CAT_W = 230
cat_pvc = box(center(0) - CAT_W / 2, CAT_Y, CAT_W, 46, "<b>Ventanas PVC</b>", "cat", size=15)
cat_alu = box(center(1, 2) - CAT_W / 2, CAT_Y, CAT_W, 46, "<b>Ventanas aluminio</b>", "cat", size=15)
cat_vid = box(center(3) - CAT_W / 2, CAT_Y, CAT_W, 46, "<b>Acristalamiento</b>", "cat", size=15)
root = box(center(0, 3) - 140, ROOT_Y + 30, 280, 70,
           "<b style='font-size:22px'>MetalHervas</b><br><span style='font-size:12px'>Proveedores y productos</span>",
           "root", size=12)

down = "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"
for c in (cat_pvc, cat_alu, cat_vid):
    edge(root, c, COLORS["cat"][1], down)
edge(cat_pvc, sups[0][0], COLORS["gealan"][1], down)
edge(cat_alu, sups[1][0], COLORS["aluval"][1], down)
edge(cat_alu, sups[2][0], COLORS["extrugasa"][1], down)
edge(cat_vid, sups[3][0], COLORS["sg"][1], down)

# Recuadro con la nota del tío (arriba a la izquierda)
note_lines = [
    "<b style='font-size:13px'>✔ Lo que trabaja MetalHervas (nota del tío)</b>",
    "<b>PVC · Gealan:</b> S 8000 IQ · S 9000 IQ · Linear · Linear acrylcolor · gama de colores",
    "<b>Aluminio:</b> Aluval y Extrugasa → todos los modelos",
    "<b>Acristalamiento:</b> Climalit / Saint-Gobain → todos los modelos",
]
NOTE_W = 360
note_body = wrap_words("PVC · Gealan: S 8000 IQ · S 9000 IQ · Linear · Linear acrylcolor · gama de colores",
                       NOTE_W - PAD_L - PAD_R - SLACK, 11)
note_h = PAD_T + 13 * LH + 4 + 11 * LH * (len(note_body) + 2) + PAD_B + 6
box(0, ROOT_Y, NOTE_W, note_h, note_lines[0] + "<div style='font-size:11px;margin-top:4px'>"
    + "<br>".join(note_lines[1:]) + "</div>", "note", size=11, stroke_w=2, align="left")

# Leyenda (bajo la columna de Saint-Gobain, que es la más corta) con muestras reales
LEG_W = 300
lx, ly = TOTAL_W - LEG_W, bottoms[3] + 30
box(lx, ly, LEG_W, 150, "<b style='font-size:13px'>Leyenda</b>", "cat", size=11, stroke_w=1, align="left")
sw_on = box(lx + 12, ly + 56, 110, 32, "Serie", "gealan", size=11, stroke_w=2.5)
badge(lx + 12 + 110, ly + 56)
cell(lx + 132, ly + 55, LEG_W - 140, 34, "<b>Trabaja MetalHervas</b> según la nota",
     f"text;html=1;whiteSpace=wrap;fontFamily={FONT};fontSize=11;fontColor=#263238;verticalAlign=middle;")
box(lx + 12, ly + 104, 110, 32, "Serie", "off", size=11, stroke_w=1.2, dashed=True)
cell(lx + 132, ly + 103, LEG_W - 140, 34, "No figura en la nota (solo informativo)",
     f"text;html=1;whiteSpace=wrap;fontFamily={FONT};fontSize=11;fontColor=#263238;verticalAlign=middle;")

cell(0, max(bottoms) + 4, TOTAL_W, 20,
     "Fuente: webs oficiales de cada proveedor (octubre 2026) y climalit.es vía Internet Archive (mayo 2026) · "
     "datos técnicos, enlaces y PDFs en Proveedores/arbol_productos.md y Proveedores/pdfs/",
     f"text;html=1;fontFamily={FONT};fontSize=10;fontColor=#78909C;align=left;verticalAlign=middle;")

xml = ('<mxfile><diagram name="Proveedores" id="prov"><mxGraphModel adaptiveColors="auto" grid="0"><root>'
       '<mxCell id="0"/><mxCell id="1" parent="0"/>' + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>")
out = PROV / "diagrama_proveedores.drawio"
out.write_text(xml, encoding="utf-8")
print("OK ->", out, "| alto columnas:", [round(b) for b in bottoms])
