"""Quita de cada .md de un proveedor las líneas repetidas en muchas páginas (menús, pies, cookies).
Uso: python scraping/dedupe.py <proveedor> [umbral=0.4]  -> Proveedores/raw/<proveedor>/_clean/*.md"""
import collections, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
name = sys.argv[1]; thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.4
d = Path(__file__).resolve().parent.parent / "Proveedores" / "raw" / name
files = sorted(d.glob("*.md"))
cnt = collections.Counter()
for f in files:
    cnt.update({l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip()})
common = {l for l, c in cnt.items() if c > thr * len(files) and not l.startswith("<!--")}
out = d / "_clean"; out.mkdir(exist_ok=True)
for f in files:
    ls = [l for l in f.read_text(encoding="utf-8").splitlines() if l.strip() and l.strip() not in common]
    (out / f.name).write_text("\n".join(ls), encoding="utf-8")
print(f"{len(files)} ficheros, {len(common)} líneas comunes eliminadas -> {out}")
