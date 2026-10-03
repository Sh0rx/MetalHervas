"""Genera clips con Seedance 2.5 en APIMart a partir de un primer y un último fotograma.

La clave se lee de la variable de entorno APIMART_API_KEY (no se guarda en ningún archivo).
  PowerShell:  $env:APIMART_API_KEY = "…"
  Bash:        export APIMART_API_KEY=…

Uso:
  python scripts/seedance.py clip --primero K1.png --ultimo K2.png --prompt video-ia/prompts/clip-a.txt --nombre clip-a-16x9 --borrador
  python scripts/seedance.py final --borrador-id <task_id> --nombre clip-a-16x9
  python scripts/seedance.py estado <task_id>

Cada trabajo deja su registro (petición, respuesta y coste) en video-ia/salidas/<nombre>.json y el vídeo en <nombre>.mp4.
Documentación: https://docs.apimart.ai/en/api-reference/videos/seedance-2-5/generation
"""
import argparse, json, mimetypes, os, pathlib, sys, time, urllib.error, urllib.request, uuid

API = "https://api.apimart.ai/v1"
SALIDAS = pathlib.Path(__file__).resolve().parent.parent / "video-ia" / "salidas"


def clave():
    k = os.environ.get("APIMART_API_KEY")
    if not k:
        sys.exit("Falta la variable de entorno APIMART_API_KEY.")
    return k


def peticion(metodo, ruta, cuerpo=None, cabeceras=None):
    req = urllib.request.Request(API + ruta, data=cuerpo, method=metodo,
                                 headers={"Authorization": f"Bearer {clave()}", **(cabeceras or {})})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.exit(f"APIMart respondió {e.code}: {e.read().decode('utf-8', 'replace')[:800]}")


def subir(ruta_imagen):
    """Sube una imagen y devuelve su URL pública (APIMart la guarda 72 horas)."""
    p = pathlib.Path(ruta_imagen)
    limite = uuid.uuid4().hex
    tipo = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
    cuerpo = (f"--{limite}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{p.name}\"\r\n"
              f"Content-Type: {tipo}\r\n\r\n").encode() + p.read_bytes() + f"\r\n--{limite}--\r\n".encode()
    r = peticion("POST", "/uploads/images", cuerpo, {"Content-Type": f"multipart/form-data; boundary={limite}"})
    url = r.get("url") or (r.get("data") or {}).get("url")
    if not url:
        sys.exit(f"No vino la URL de la imagen subida: {r}")
    print(f"  subida {p.name} → {url}")
    return url


def lanzar(cuerpo):
    r = peticion("POST", "/videos/generations", json.dumps(cuerpo).encode(), {"Content-Type": "application/json"})
    try:
        return r["data"][0]["task_id"], r
    except (KeyError, IndexError, TypeError):
        sys.exit(f"Respuesta inesperada al lanzar: {r}")


def urls_mp4(x):
    """Busca las URL de vídeo en la respuesta, venga como venga anidada."""
    if isinstance(x, str):
        return [x] if x.startswith("http") and (".mp4" in x or ".mov" in x) else []
    if isinstance(x, dict):
        return [u for v in x.values() for u in urls_mp4(v)]
    if isinstance(x, list):
        return [u for v in x for u in urls_mp4(v)]
    return []


def esperar(task_id, cada=10):
    print(f"  tarea {task_id}: esperando…")
    while True:
        r = peticion("GET", f"/tasks/{task_id}")
        d = r.get("data", r)
        estado = d.get("status") if isinstance(d, dict) else None
        if estado == "completed":
            return r
        if estado == "failed":
            sys.exit(f"La tarea falló: {json.dumps(r, ensure_ascii=False)[:800]}")
        print(f"    {estado} …")
        time.sleep(cada)


def guardar(nombre, cuerpo, lanzado, final):
    SALIDAS.mkdir(parents=True, exist_ok=True)
    (SALIDAS / f"{nombre}.json").write_text(json.dumps({"peticion": cuerpo, "lanzado": lanzado, "resultado": final},
                                                       ensure_ascii=False, indent=1), encoding="utf-8")
    urls = urls_mp4(final)
    if not urls:
        print("  Terminado, pero no encuentro la URL del vídeo; mira el .json.")
        return
    destino = SALIDAS / f"{nombre}.mp4"
    urllib.request.urlretrieve(urls[0], destino)
    d = final.get("data", {}) if isinstance(final, dict) else {}
    print(f"  vídeo → {destino}   coste: {d.get('cost', '¿?')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    c = sub.add_parser("clip", help="clip entre un primer y un último fotograma")
    c.add_argument("--primero", required=True); c.add_argument("--ultimo", required=True)
    c.add_argument("--prompt", required=True, help="archivo de texto con el prompt")
    c.add_argument("--nombre", required=True); c.add_argument("--duracion", type=int, default=6)
    c.add_argument("--borrador", action="store_true", help="borrador barato a 480p")
    c.add_argument("--semilla", type=int)
    f = sub.add_parser("final", help="versión 1080p de un borrador que ha convencido")
    f.add_argument("--borrador-id", required=True); f.add_argument("--nombre", required=True)
    f.add_argument("--prompt", help="opcional: el mismo prompt del borrador")
    e = sub.add_parser("estado", help="consulta una tarea"); e.add_argument("task_id")
    a = ap.parse_args()

    if a.orden == "estado":
        print(json.dumps(peticion("GET", f"/tasks/{a.task_id}"), ensure_ascii=False, indent=1))
        return
    if a.orden == "clip":
        cuerpo = {"model": "seedance-2.5", "prompt": pathlib.Path(a.prompt).read_text(encoding="utf-8").strip(),
                  "image_with_roles": [{"url": subir(a.primero), "role": "first_frame"},
                                       {"url": subir(a.ultimo), "role": "last_frame"}],
                  "size": "adaptive", "duration": a.duracion, "generate_audio": False, "watermark": False,
                  "return_last_frame": True}
        cuerpo.update({"draft": True, "resolution": "480p"} if a.borrador else {"resolution": "1080p"})
        if a.semilla is not None:
            cuerpo["seed"] = a.semilla
        nombre = a.nombre + ("-borrador" if a.borrador else "")
    else:
        cuerpo = {"model": "seedance-2.5", "draft_task_id": a.borrador_id, "resolution": "1080p",
                  "generate_audio": False, "watermark": False, "return_last_frame": True}
        if a.prompt:
            cuerpo["prompt"] = pathlib.Path(a.prompt).read_text(encoding="utf-8").strip()
        nombre = a.nombre + "-1080p"
    task_id, lanzado = lanzar(cuerpo)
    print(f"  lanzada: {task_id}")
    guardar(nombre, cuerpo, lanzado, esperar(task_id))


if __name__ == "__main__":
    main()
