"""Logo actual de Metal Hervás sin «S.L.»: idéntico al trazado del logo verde, solo se quitan
las letras S.L. (trazados 19–22) y se recorta el hueco que dejan abajo.
Salida: prototipos/assets/logo/sin-sl/logo-{color,negativo,blanco,mono}.svg y simbolo-color.svg
"""
import pathlib, re

SRC = pathlib.Path("prototipos/assets/logo")
OUT = SRC / "sin-sl"; OUT.mkdir(exist_ok=True)
SL = {19, 20, 21, 22}            # «S», «.», «L», «.» bajo la línea (ver scripts/trace_logo.py)
VB = "0 0 5040 1860"             # la línea en L acaba en y≈1829; antes el lienzo bajaba a 1980 por «S.L.»

for v in ("color", "negativo", "blanco", "mono"):
    s = (SRC / f"logo-{v}.svg").read_text(encoding="utf-8")
    paths = re.findall(r'<path [^>]*/>', s)
    assert len(paths) == 33, (v, len(paths))
    cuerpo = "".join(p for i, p in enumerate(paths) if i not in SL)
    head = re.sub(r'viewBox="[^"]+"', f'viewBox="{VB}"', s[:s.index("<path")])
    (OUT / f"logo-{v}.svg").write_text(head + cuerpo + "</svg>", encoding="utf-8")

# icono: el logo entero centrado en un cuadrado blanco (igual que hoy, no tiene símbolo propio)
color = (OUT / "logo-color.svg").read_text(encoding="utf-8")
inner = color[color.index("<path"):color.rindex("</svg>")]
pad = (5040 - 1860) / 2
(OUT / "simbolo-color.svg").write_text(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-pad - 120:.0f} 5040 5280"><rect x="0" y="{-pad - 120:.0f}" width="5040" height="5280" fill="#FFFFFF"/>{inner}</svg>',
    encoding="utf-8")
print(sorted(p.name for p in OUT.iterdir()))
