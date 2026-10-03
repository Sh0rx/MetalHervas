"""Vectoriza la sección del sistema GEALAN S 9000 (marco + hoja) del plano público de gealan.de.

Fuente: Proveedores/pdfs/gealan/sistemas/S9000-technische-eigenschaften_14592.png (764 × 832 px).
Escala con las cotas del propio plano: fondo del marco 82,5 mm (x 240,5 → 559,5 px) y altura vista
total 118 mm (y 707,5 → 251,5 px) → 3,866 px/mm en los dos ejes.

Coordenadas de salida, en mm:
  u = fondo, desde la cara exterior del marco (0) hacia el interior (82,5; la hoja llega a 101).
  v = distancia desde el canto exterior del marco (0, contra la pared) hacia el centro de la ventana.

Salida: prototipos/shared/perfil-s9000.json (+ una imagen de control en el scratchpad si se pasa --control).
El PVC del plano es blanco con contorno negro: cada perfil es una única región blanca «en red» y sus
cámaras son regiones cerradas dentro. Los refuerzos de acero van rayados y las juntas, en negro.
"""
import argparse, json, pathlib, sys
import cv2, numpy as np

RAIZ = pathlib.Path(__file__).resolve().parent.parent
PLANO = RAIZ / "Proveedores/pdfs/gealan/sistemas/S9000-technische-eigenschaften_14592.png"
SALIDA = RAIZ / "prototipos/shared/perfil-s9000.json"
K = (559.5 - 240.5) / 82.5            # px por mm
X0, Y0 = 240.5, 707.5                  # origen: cara exterior del marco, canto exterior
RECORTE = (236, 200, 640, 711)         # x0, y0, x1, y1: solo el perfil, sin cotas


def a_mm(pts, ox, oy):
    return [[round((x + ox - X0) / K, 2), round((Y0 - (y + oy)) / K, 2)] for x, y in pts]


def contornos(mascara, ox, oy, eps=0.7, min_area=12):
    """Contorno exterior y huecos de una máscara, simplificados, en mm."""
    cs, jer = cv2.findContours(mascara, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    piezas = []
    if jer is None:
        return piezas
    for i, c in enumerate(cs):
        if jer[0][i][3] != -1 or cv2.contourArea(c) < min_area:
            continue
        huecos = []
        h = jer[0][i][2]
        while h != -1:
            if cv2.contourArea(cs[h]) >= min_area:
                huecos.append(a_mm(cv2.approxPolyDP(cs[h], eps, True)[:, 0, :], ox, oy))
            h = jer[0][h][0]
        piezas.append({"contorno": a_mm(cv2.approxPolyDP(c, eps, True)[:, 0, :], ox, oy), "huecos": huecos})
    return piezas


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--control", help="ruta de una imagen de control")
    a = ap.parse_args()
    im = cv2.imread(str(PLANO), cv2.IMREAD_GRAYSCALE)
    if im is None:
        sys.exit(f"No encuentro {PLANO}")
    x0, y0, x1, y1 = RECORTE
    c = im[y0:y1, x0:x1]
    negro = (c < 150).astype(np.uint8)
    blanco = 1 - negro
    n, lab, st, cen = cv2.connectedComponentsWithStats(blanco, connectivity=4)
    dt = cv2.distanceTransform(blanco, cv2.DIST_L2, 3)
    H, W = c.shape
    k3 = np.ones((3, 3), np.uint8)

    def comp_en(px, py):
        return lab[py - y0, px - x0]

    def region(i, crecer=1):
        """La región blanca más su contorno negro (crecer px)."""
        return cv2.dilate((lab == i).astype(np.uint8), k3, iterations=crecer)

    # Las redes de PVC: las dos regiones grandes y finas (grosor de pared < 8 px)
    redes = sorted([i for i in range(1, n) if st[i][4] > 5000 and dt[lab == i].max() < 8], key=lambda i: -st[i][4])
    if len(redes) < 2:
        sys.exit("No encuentro las dos redes de PVC (marco y hoja).")
    marco_i, hoja_i = sorted(redes[:2], key=lambda i: -cen[i][1])   # el marco es el de abajo

    def perfil(i):
        m = region(i, 2)
        # Rellena las cámaras cerradas dentro de la red para tener el contorno con sus huecos
        return m

    marco_m, hoja_m = perfil(marco_i), perfil(hoja_i)

    # Junquillo: la red fina suelta arriba a la derecha (sujeta el vidrio por dentro)
    junqs = [i for i in range(1, n) if st[i][0] > 300 and st[i][1] < 180 and st[i][4] > 800 and dt[lab == i].max() < 5]
    if not junqs:
        sys.exit("No encuentro el junquillo.")
    junq_m = region(max(junqs, key=lambda i: st[i][4]), 2)

    # Refuerzos de acero: el hueco de la red que contiene el rayado, menos el vacío interior del tubo
    def refuerzo(red_m, px_vacio, py_vacio):
        vacio = lab == comp_en(px_vacio, py_vacio)
        cs, jer = cv2.findContours(red_m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        vy, vx = py_vacio - y0, px_vacio - x0
        for j, cc in enumerate(cs):
            if jer[0][j][3] != -1 and cv2.pointPolygonTest(cc, (vx, vy), False) > 0:
                hueco = np.zeros_like(red_m); cv2.drawContours(hueco, [cc], -1, 1, -1)
                hueco = cv2.erode(hueco, k3, iterations=1)
                # El acero es el rayado: trazos negros y los huecos pequeños entre ellos, no el aire de la cámara
                pequenos = np.isin(lab, [q for q in range(1, n) if st[q][4] < 90]).astype(np.uint8)
                rayado = cv2.morphologyEx(((negro | pequenos) & hueco).astype(np.uint8), cv2.MORPH_CLOSE, k3, iterations=2)
                return (rayado & hueco & (1 - cv2.dilate(vacio.astype(np.uint8), k3, iterations=1))).astype(np.uint8)
        return None
    acero_marco = refuerzo(marco_m, 450, 620)
    acero_hoja = refuerzo(hoja_m, 500, 410)

    # Manchas negras que sobreviven a quitar las líneas finas. Son juntas si tocan el aire (el galce entre
    # marco y hoja, o el exterior); si solo tocan cámaras, son tabiques gruesos del propio perfil.
    manchas = cv2.morphologyEx(negro, cv2.MORPH_OPEN, k3, iterations=2)
    def huecos_de(m):
        cs, jer = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        h = np.zeros_like(m)
        for j, cc in enumerate(cs):
            if jer[0][j][3] != -1: cv2.drawContours(h, [cc], -1, 1, -1)
        return h
    camaras = huecos_de(marco_m) | huecos_de(hoja_m) | huecos_de(junq_m)
    nm, labm = cv2.connectedComponents(manchas, connectivity=8)
    juntas_m = np.zeros_like(manchas)
    for j in range(1, nm):
        mj = (labm == j).astype(np.uint8)
        anillo = cv2.dilate(mj, k3, iterations=3) & blanco & (1 - mj)
        if (anillo & (1 - camaras) & (1 - marco_m) & (1 - hoja_m)).sum() > 3:
            juntas_m |= mj
        elif (mj & (marco_m | hoja_m)).sum() or (anillo & camaras).sum():
            # tabique grueso: pasa a formar parte del perfil que lo rodea
            if (cv2.dilate(mj, k3, iterations=3) & hoja_m).sum() > (cv2.dilate(mj, k3, iterations=3) & marco_m).sum(): hoja_m |= mj
            else: marco_m |= mj
    # La junta central del marco va dibujada en contorno (blanca por dentro): región alargada de unos 45 × 90 px
    centrales = [i for i in range(1, n) if 35 <= st[i][2] <= 55 and 80 <= st[i][3] <= 100 and dt[lab == i].max() < 6]
    junta_central = region(centrales[0], 2) if centrales else None
    if junta_central is not None:
        juntas_m |= junta_central
    # Fuera de las juntas, lo que es de los aceros (el rayado) no cuenta
    for acero in (acero_marco, acero_hoja):
        if acero is not None:
            juntas_m &= (1 - cv2.dilate(acero, k3, iterations=2))

    datos = {
        "fuente": "GEALAN S 9000, plano «Technische Eigenschaften» de gealan.de (sección de marco y hoja). Vectorizado con scripts/trazar_perfil_s9000.py.",
        "unidades": "mm; u = fondo desde la cara exterior del marco, v = desde el canto exterior del marco hacia el centro",
        "cotas": {"fondo_marco": 82.5, "fondo_total": 101, "visto_marco": 70, "visto_total": 118, "alto_hoja": 82, "hoja_sobre_marco": 48},
        "marco": contornos(marco_m, x0, y0),
        "hoja": contornos(hoja_m, x0, y0),
        "junquillo": contornos(junq_m, x0, y0),
        "acero_marco": contornos(acero_marco, x0, y0) if acero_marco is not None else [],
        "acero_hoja": contornos(acero_hoja, x0, y0) if acero_hoja is not None else [],
        "juntas": contornos(juntas_m.astype(np.uint8), x0, y0, eps=0.5, min_area=8),
        "vidrio": {"u0": round((382 - X0) / K, 1), "u1": round((552 - X0) / K, 1), "borde_v": round((Y0 - 332) / K, 1),
                    "composicion": "triple, 4/16/4/16/4 (como en el plano)"},
    }
    SALIDA.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
    resumen = {k: (len(v) if isinstance(v, list) else "") for k, v in datos.items() if isinstance(v, list)}
    print("Escrito", SALIDA, resumen, f"{SALIDA.stat().st_size / 1024:.0f} kB")

    if a.control:
        vis = cv2.cvtColor(c, cv2.COLOR_GRAY2BGR)
        capas = [(marco_m, (60, 160, 60)), (hoja_m, (200, 120, 40)), (junq_m, (40, 200, 220)),
                 (acero_marco, (40, 40, 220)), (acero_hoja, (40, 40, 220)), (juntas_m, (200, 40, 200))]
        for m, col in capas:
            if m is None: continue
            capa = np.zeros_like(vis); capa[m > 0] = col
            vis = cv2.addWeighted(vis, 1, capa, 0.55, 0)
        cv2.imwrite(a.control, cv2.resize(vis, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST))


if __name__ == "__main__":
    main()
