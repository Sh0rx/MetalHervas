"""Convierte los clips de Seedance en la secuencia de fotogramas que la web avanza con el scroll.

Lee el orden de video-ia/clips.json, toma de video-ia/salidas/ el final 1080p de cada clip
(o el borrador si aún no hay final) y deja los fotogramas WebP y un manifest.json en
prototipos/assets/recorrido/<formato>/. También mide cuánto se parecen las costuras
(último fotograma de un clip contra el primero del siguiente) y, si una costura no encaja
(SSIM por debajo de --umbral), funde los últimos fotogramas de un clip con los primeros del siguiente.

Uso:
  python scripts/secuencia.py --formato 16x9
  python scripts/secuencia.py --formato 9x16 --fps 15 --ancho 720
  python scripts/secuencia.py --formato 16x9 --solo-costuras
"""
import argparse, json, pathlib, re, shutil, subprocess, sys, tempfile
from PIL import Image

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDAS = RAIZ / "video-ia" / "salidas"
DESTINO = RAIZ / "prototipos" / "assets" / "recorrido"


def ffmpeg(*args):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *map(str, args)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg falló: {r.stderr[-800:]}")
    return r.stderr


def video_de(nombre, formato):
    for sufijo in ("-1080p", "-borrador"):
        p = SALIDAS / f"{nombre}-{formato}{sufijo}.mp4"
        if p.exists():
            return p, sufijo.strip("-")
    return None, None


def fotograma(video, cual, destino):
    """Saca el primer o el último fotograma de un vídeo a PNG."""
    if cual == "primero":
        ffmpeg("-i", video, "-frames:v", 1, destino)
    else:
        ffmpeg("-sseof", -0.1, "-i", video, "-update", 1, destino)


def ssim(a, b):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", a, "-i", b, "-lavfi",
                        "[0:v][1:v]scale2ref[x][y];[x][y]ssim", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"All:([\d.]+)", r.stderr)
    return float(m.group(1)) if m else None


def fundir(carpeta_a, nombres_a, carpeta_b, cuadros_b, n, calidad):
    """Mezcla los últimos n fotogramas del clip anterior con los n primeros del siguiente."""
    n = min(n, len(nombres_a), len(cuadros_b))
    for j in range(n):
        destino = carpeta_a / nombres_a[len(nombres_a) - n + j]
        t = (j + 1) / (n + 1)
        with Image.open(destino) as x, Image.open(cuadros_b[j]) as y:
            Image.blend(x.convert("RGB"), y.convert("RGB").resize(x.size), t).save(destino, "WEBP", quality=calidad)


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # la consola de Windows no es UTF-8 por defecto
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--formato", default="16x9", choices=["16x9", "9x16"])
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--ancho", type=int, help="ancho en px (por defecto 1600 en 16x9 y 720 en 9x16)")
    ap.add_argument("--calidad", type=int, default=72, help="calidad WebP 0–100")
    ap.add_argument("--solo-costuras", action="store_true")
    ap.add_argument("--umbral", type=float, default=0.7, help="por debajo de este SSIM la costura se funde")
    ap.add_argument("--fundido", type=int, default=12, help="fotogramas del fundido en las costuras que no encajan")
    a = ap.parse_args()
    ancho = a.ancho or (1600 if a.formato == "16x9" else 720)

    clips = json.loads((RAIZ / "video-ia" / "clips.json").read_text(encoding="utf-8"))["clips"]
    videos = []
    for c in clips:
        v, calidad = video_de(c["nombre"], a.formato)
        if not v:
            print(f"- {c['nombre']}: todavía no hay vídeo; la secuencia se corta aquí.")
            break
        print(f"- {c['nombre']}: {v.name} ({calidad})")
        videos.append((c, v, calidad))
    if not videos:
        sys.exit("No hay ningún clip en video-ia/salidas/.")

    costuras = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        print(f"Costuras (SSIM; 1 = idénticos; por debajo de {a.umbral} se funden):")
        for (c1, v1, _), (c2, v2, _) in zip(videos, videos[1:]):
            fotograma(v1, "ultimo", tmp / "a.png"); fotograma(v2, "primero", tmp / "b.png")
            costuras.append(ssim(tmp / "a.png", tmp / "b.png"))
            print(f"  {c1['nombre']} → {c2['nombre']}: {costuras[-1]}" + ("  → fundido" if (costuras[-1] or 0) < a.umbral else ""))
    if a.solo_costuras:
        return

    salida = DESTINO / a.formato
    if salida.exists():
        shutil.rmtree(salida)
    tramos = []
    for i, (c, v, calidad) in enumerate(videos):
        carpeta = salida / c["nombre"]; carpeta.mkdir(parents=True)
        ffmpeg("-i", v, "-vf", f"fps={a.fps},scale={ancho}:-2:flags=lanczos",
               "-c:v", "libwebp", "-quality", a.calidad, "-compression_level", 6, carpeta / "%04d.webp")
        cuadros = sorted(carpeta.glob("*.webp"))
        if i > 0 and cuadros:  # el primero repite el último del clip anterior
            cuadros[0].unlink(); cuadros = cuadros[1:]
        if i > 0 and (costuras[i - 1] or 0) < a.umbral:
            fundir(salida / videos[i - 1][0]["nombre"], tramos[-1]["cuadros"], carpeta, cuadros, a.fundido, a.calidad)
            for q in cuadros[:a.fundido]:
                q.unlink()
            cuadros = cuadros[a.fundido:]
        peso = sum(p.stat().st_size for p in cuadros)
        tramos.append({"nombre": c["nombre"], "tramo": c["tramo"], "calidad": calidad,
                       "carpeta": f"{c['nombre']}/", "cuadros": [p.name for p in cuadros]})
        print(f"  {c['nombre']}: {len(cuadros)} fotogramas, {peso / 1e6:.1f} MB")
    (salida / "manifest.json").write_text(json.dumps({"formato": a.formato, "fps": a.fps, "ancho": ancho,
                                                      "tramos": tramos}, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
    total = sum(p.stat().st_size for p in salida.rglob("*.webp"))
    print(f"Secuencia → {salida}  ({sum(len(t['cuadros']) for t in tramos)} fotogramas, {total / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
