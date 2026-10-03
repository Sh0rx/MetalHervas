"""Exporta a WebP optimizado las fotos elegidas para los prototipos.
Uso: python scripts/export_fotos.py <index.json de las hojas de contacto>
"""
import json, sys, pathlib
from PIL import Image, ImageOps
import pillow_heif; pillow_heif.register_heif_opener()

ROOT = pathlib.Path("recursos-multimedia/ordenado")
OUT = pathlib.Path("prototipos/assets/fotos"); OUT.mkdir(parents=True, exist_ok=True)
idx = json.load(open(sys.argv[1]))

SELECCION = {  # nombre destino: (carpeta, índice en la hoja de contacto)
    "chalet-travertino-fachada": ("viviendas__chalet-travertino", 1),
    "chalet-travertino-trasera": ("viviendas__chalet-travertino", 6),
    "chalet-travertino-entrada": ("viviendas__chalet-travertino", 9),
    "chalet-travertino-porche": ("viviendas__chalet-travertino", 12),
    "chalet-gris-jardin": ("viviendas__chalet-gris-piscina", 8),
    "puerta-antracita-acristalada": ("puertas-entrada__aluminio-antracita", 23),
    "puerta-antracita-diagonal": ("puertas-entrada__aluminio-antracita", 8),
    "porche-plegable-madera": ("cerramientos__cortina-cristal-porche-vigas", 16),
    "porche-plegable-interior": ("cerramientos__cortina-cristal-porche-vigas", 14),
    "pabellon-cristal-negro": ("cerramientos__pabellon-cristal-negro", 0),
    "terraza-plegable": ("cerramientos__terraza-plegable-blanca", 20),
    "barandilla-vidrio-escalera": ("barandillas-y-escaleras__edificio-blanco-escalera-cristal", 16),
    "taller-ventanas-pvc-rojas": ("taller__taller-fabricacion-ventanas", 6),
    "taller-ventanas-pvc-blancas": ("taller__taller-fabricacion-ventanas", 16),
    "taller-soldador": ("taller__taller-fabricacion-ventanas", 15),
    "soldadura-nocturna": ("naves-y-estructuras__soldadura-nocturna", 7),
    "soldadura-pilares": ("naves-y-estructuras__soldadura-nocturna", 3),
    "nave-estructura-arriostrada": ("naves-y-estructuras__nave-patatas-1-montaje-estructura", 28),
    "nave-cerchas-cielo": ("naves-y-estructuras__nave-patatas-1-montaje-estructura", 14),
    "nave-grua-montaje": ("naves-y-estructuras__nave-patatas-1-montaje-estructura", 9),
    "nave-terminada": ("naves-y-estructuras__nave-patatas-2-terminada", 18),
    "sede-camiones-rotulo": ("vehiculos__furgoneta-y-camion-metal-hervas", 3),
    "equipo-puerta": ("personas__equipo", 0),
}
for nombre, (hoja, i) in SELECCION.items():
    cat, sub = hoja.split("__")
    src = ROOT / cat / sub / idx[hoja][i]
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((2000, 2000), Image.LANCZOS)
    dst = OUT / f"{nombre}.webp"
    im.save(dst, "WEBP", quality=78, method=6)
    print(f"{nombre:32s} {im.size[0]}x{im.size[1]} {dst.stat().st_size//1024:4d} KB  <- {src.name}")
