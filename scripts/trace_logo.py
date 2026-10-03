"""Vectoriza el logo verde actual de MetalHervás (IMG_0564.JPG) por capas de color.

Cada píxel se asigna al color de marca más cercano, se genera una máscara por color,
se amplía ×3 y se calca con vtracer. Resultado: SVG con colores planos exactos.
Uso: python scripts/trace_logo.py
"""
import re, pathlib, tempfile
import numpy as np
from PIL import Image, ImageFilter
import vtracer

SRC = "recursos-multimedia/ordenado/documentos-y-logos/logos-y-cartelería/IMG_0564.JPG"
OUT = pathlib.Path("prototipos/assets/logo")
SCALE = 3

PALETA = {  # colores muestreados del propio JPG
    "blanco": (255, 255, 255),
    "verde": (0x4B, 0xA9, 0x39),
    "negro": (0, 0, 0),
    "gris": (0xA0, 0xA0, 0xA0),
    "verde_oscuro": (0x25, 0x6A, 0x31),
    "verde_medio": (0x28, 0xA3, 0x60),
    "menta": (0x87, 0xD2, 0xA9),
}
HEX = {k: "#%02X%02X%02X" % v for k, v in PALETA.items()}

def capas(box, usar):
    im = Image.open(SRC).convert("RGB").crop(box)
    im = im.resize((im.width * SCALE, im.height * SCALE), Image.LANCZOS)
    a = np.asarray(im).astype(np.int32)
    nombres = [n for n in PALETA if n in usar]
    cols = np.array([PALETA[n] for n in nombres])
    dist = ((a[:, :, None, :] - cols[None, None]) ** 2).sum(-1)
    idx = dist.argmin(-1)
    return im.size, {n: idx == i for i, n in enumerate(nombres) if n != "blanco"}

def calcar(mask):
    img = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
    with tempfile.TemporaryDirectory() as t:
        p, o = f"{t}/m.png", f"{t}/m.svg"
        img.save(p)
        vtracer.convert_image_to_svg_py(p, o, colormode="binary", mode="spline",
                                        filter_speckle=12, corner_threshold=60,
                                        length_threshold=4.0, splice_threshold=45,
                                        path_precision=2)
        svg = open(o).read()
    return re.findall(r'<path d="([^"]*)"[^>]*transform="translate\(([^,]+),([^)]+)\)"', svg)

def construir(nombre, box, colores, titulo, usar=tuple(PALETA)):
    (w, h), mascaras = capas(box, usar)
    partes = []
    for capa, mask in mascaras.items():
        if mask.sum() < 50:
            continue
        fill = colores.get(capa, HEX[capa])
        if fill is None:
            continue
        for d, tx, ty in calcar(mask):
            partes.append(f'<path fill="{fill}" transform="translate({tx} {ty})" d="{d}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="{titulo}"><title>{titulo}</title>' + "".join(partes) + "</svg>")
    (OUT / nombre).write_text(svg, encoding="utf-8")
    print(nombre, f"{w}x{h}", len(partes), "trazados", len(svg) // 1024, "KB")

LOGO_BOX = (120, 0, 1800, 660)        # Metal HERVÁS S.L. + estructura
LOGO_COLS = ("blanco", "verde", "negro", "gris")
PVC_BOX = (255, 700, 1665, 935)        # submarca VENTANAS de PVC
T = "Metal Hervás S.L."
construir("logo-color.svg", LOGO_BOX, {}, T, LOGO_COLS)
construir("logo-negativo.svg", LOGO_BOX, {"negro": "#FFFFFF", "gris": "#8C8C8C"}, T, LOGO_COLS)
construir("logo-blanco.svg", LOGO_BOX, {"negro": "#FFFFFF", "verde": "#FFFFFF", "gris": "#9A9A9A"}, T, LOGO_COLS)
construir("logo-mono.svg", LOGO_BOX, {"verde": "#000000", "gris": "#8A8A8A"}, T, LOGO_COLS)
construir("ventanas-pvc-color.svg", PVC_BOX, {}, "Ventanas de PVC")
construir("ventanas-pvc-negativo.svg", PVC_BOX, {"negro": "#FFFFFF"}, "Ventanas de PVC")
