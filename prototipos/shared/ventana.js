// Ventana de PVC de dos hojas practicables con el perfil GEALAN S 9000, para el prototipo «Del taller a tu casa».
// Unidades: metros. Interior hacia +Z.
//
// La sección del marco, la hoja, el junquillo, las juntas y los refuerzos sale del plano público de GEALAN
// para el S 9000 («Technische Eigenschaften»), vectorizado con scripts/trazar_perfil_s9000.py en
// shared/perfil-s9000.json. Son de ejemplo: las medidas de la ventana, el encuentro central de las hojas,
// la manilla, las bisagras y el cajón de persiana.
import * as THREE from "three";
import { mergeGeometries } from "three/addons/utils/BufferGeometryUtils.js";

const mm = 0.001;
const ANCHO = 1.2, ALTO = 1.1, CAJON = 0.19, HOLGURA = 0.004;

function forma(pieza, du = 0, dv = 0) {
  const p = (pts) => pts.map(([u, v]) => new THREE.Vector2((u - du) * mm, (v - dv) * mm));
  const s = new THREE.Shape(p(pieza.contorno));
  for (const h of pieza.huecos) s.holes.push(new THREE.Path(p(h)));
  return s;
}

// Barra extruida a lo largo de Z. Con «inglete», los extremos se cortan a 45°: cada punto de la sección
// se acorta tanto como dista del canto exterior (su coordenada y).
function barra(formas, L, inglete) {
  const g = new THREE.ExtrudeGeometry(formas, { depth: L, bevelEnabled: false, curveSegments: 1, steps: 1 });
  if (inglete) {
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) { const y = p.getY(i), z = p.getZ(i); p.setZ(i, y + (z / L) * (L - 2 * y)); }
  }
  return g;
}

// Coloca una barra (sección en x = fondo u, y = distancia al canto exterior) en un lado de un rectángulo
const LADOS = [
  { a: [1, 0], n: [0, 1], o: [-1, -1], largo: "w" },   // abajo
  { a: [0, 1], n: [-1, 0], o: [1, -1], largo: "h" },   // derecha
  { a: [-1, 0], n: [0, -1], o: [1, 1], largo: "w" },   // arriba
  { a: [0, -1], n: [1, 0], o: [-1, 1], largo: "h" },   // izquierda
];
function rectangulo(formas, w, h, uC) {
  const geos = LADOS.map((l) => {
    const L = l.largo === "w" ? w : h, b = barra(formas, L, true), g = b.index ? b.toNonIndexed() : b;
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const u = p.getX(i), v = p.getY(i), z = p.getZ(i);
      p.setXYZ(i, l.o[0] * w / 2 + l.a[0] * z + l.n[0] * v, l.o[1] * h / 2 + l.a[1] * z + l.n[1] * v, u - uC * mm);
    }
    // El cambio de ejes invierte el sentido de las caras: se reordenan para que la normal mire hacia fuera
    if (l.n[0] * l.a[1] - l.n[1] * l.a[0] < 0) {
      for (let i = 0; i < p.count; i += 3) {
        const t = [p.getX(i + 1), p.getY(i + 1), p.getZ(i + 1)];
        p.setXYZ(i + 1, p.getX(i + 2), p.getY(i + 2), p.getZ(i + 2)); p.setXYZ(i + 2, ...t);
      }
    }
    g.deleteAttribute("uv"); g.deleteAttribute("normal"); g.clearGroups();
    return g;
  });
  const m = mergeGeometries(geos); m.computeVertexNormals(); return m;
}

function anillo(w, h, ancho, fondo) {
  const s = new THREE.Shape([new THREE.Vector2(-w / 2, -h / 2), new THREE.Vector2(w / 2, -h / 2), new THREE.Vector2(w / 2, h / 2), new THREE.Vector2(-w / 2, h / 2)]);
  const iw = w / 2 - ancho, ih = h / 2 - ancho;
  s.holes.push(new THREE.Path([new THREE.Vector2(-iw, -ih), new THREE.Vector2(-iw, ih), new THREE.Vector2(iw, ih), new THREE.Vector2(iw, -ih)]));
  const g = new THREE.ExtrudeGeometry(s, { depth: fondo, bevelEnabled: false }); g.translate(0, 0, -fondo / 2); return g;
}

export function crearVentana(perfil) {
  const pvc = new THREE.MeshStandardMaterial({ color: 0x33383c, roughness: 0.5, metalness: 0.05 });          // RAL 7016 antracita
  const nucleo = new THREE.MeshStandardMaterial({ color: 0xe9eaea, roughness: 0.65 });                       // PVC del interior del perfil
  const goma = new THREE.MeshStandardMaterial({ color: 0x141516, roughness: 0.9 });
  const acero = new THREE.MeshStandardMaterial({ color: 0xb4b8bb, roughness: 0.3, metalness: 0.9 });
  const aluminio = new THREE.MeshStandardMaterial({ color: 0x8e9396, roughness: 0.4, metalness: 0.7 });
  const cristal = new THREE.MeshPhysicalMaterial({ color: 0xdfe9ea, roughness: 0.04, metalness: 0, transmission: 0.9,
    thickness: 0.004, ior: 1.5, transparent: true, opacity: 0.3, side: THREE.DoubleSide, depthWrite: false });
  const herraje = new THREE.MeshStandardMaterial({ color: 0x2b2f32, roughness: 0.32, metalness: 0.6 });

  const uC = perfil.cotas.fondo_marco / 2;                   // el centro del marco queda en z = 0
  const vS0 = Math.min(...perfil.hoja[0].contorno.map((p) => p[1]));   // canto exterior de la hoja (desde el del marco)
  const g = perfil.vidrio;
  const ventana = new THREE.Group();
  const anclas = {};

  // Juntas: las del galce de la hoja van con la hoja; la central, con el marco
  const centro = (pz) => pz.contorno.reduce((s, p) => [s[0] + p[0], s[1] + p[1]], [0, 0]).map((x) => x / pz.contorno.length);
  const juntasHoja = perfil.juntas.filter((j) => { const [u, v] = centro(j); return v > 72 || u > perfil.cotas.fondo_marco; });
  const juntasMarco = perfil.juntas.filter((j) => !juntasHoja.includes(j));

  // ── Ventana montada ──
  const marco = new THREE.Mesh(rectangulo(perfil.marco.map((p) => forma(p)), ANCHO, ALTO, uC), pvc);
  const juntasM = new THREE.Mesh(rectangulo(juntasMarco.map((p) => forma(p)), ANCHO, ALTO, uC), goma);
  ventana.add(marco, juntasM);

  const pvcCajon = pvc.clone(); pvcCajon.transparent = true;
  const cajon = new THREE.Mesh(new THREE.BoxGeometry(ANCHO + 0.02, CAJON, 0.2), pvcCajon);
  cajon.position.set(0, ALTO / 2 + CAJON / 2, 0.065); ventana.add(cajon);

  const hojaW = (ANCHO - 2 * vS0 * mm - HOLGURA) / 2, hojaH = ALTO - 2 * vS0 * mm;
  const formasHoja = [...perfil.hoja, ...perfil.junquillo].map((p) => forma(p, 0, vS0));
  const geoHoja = rectangulo(formasHoja, hojaW, hojaH, uC);
  const geoJuntasHoja = rectangulo(juntasHoja.map((p) => forma(p, 0, vS0)), hojaW, hojaH, uC);
  const borde = (g.borde_v - vS0) * mm, vw = hojaW - 2 * borde, vh = hojaH - 2 * borde;
  const zHoja = (perfil.cotas.fondo_total - uC) * mm, zBisagra = zHoja - 0.012;
  const hojas = [];
  for (const lado of [-1, 1]) {            // -1 izquierda (hoja principal, con la manilla), +1 derecha
    const pivote = new THREE.Group();
    pivote.position.set(lado * (ANCHO / 2 - vS0 * mm), 0, zBisagra); ventana.add(pivote);
    const hoja = new THREE.Group(); hoja.position.set(-lado * hojaW / 2, 0, -zBisagra); pivote.add(hoja);
    hoja.add(new THREE.Mesh(geoHoja, pvc), new THREE.Mesh(geoJuntasHoja, goma));
    // Triple acristalamiento con sus dos separadores
    const lunas = [];
    for (let i = 0; i < 3; i++) {
      const luna = new THREE.Mesh(new THREE.BoxGeometry(vw, vh, 0.004), cristal);
      luna.position.z = (g.u0 + 2 + i * 20 - uC) * mm; hoja.add(luna); lunas.push(luna);
    }
    for (let i = 0; i < 2; i++) {
      const sep = new THREE.Mesh(anillo(vw - 0.002, vh - 0.002, 0.012, 0.016), aluminio);
      sep.position.z = (g.u0 + 12 + i * 20 - uC) * mm; hoja.add(sep);
    }
    for (const y of [-hojaH / 2 + 0.12, hojaH / 2 - 0.12]) {
      const b = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.09, 16), herraje);
      b.position.set(lado * (hojaW / 2 + 0.003), y, zBisagra); hoja.add(b);
    }
    hojas.push({ lado, pivote, hoja, lunaInt: lunas[2], vw, vh });
  }

  // Hoja principal: tapajuntas del encuentro central (de ejemplo) y manilla que gira 90°
  const izq = hojas[0].hoja;
  const tapa = new THREE.Mesh(new THREE.BoxGeometry(0.034, hojaH - 0.03, 0.006), pvc);
  tapa.position.set(hojaW / 2 + HOLGURA / 2, 0, zHoja + 0.003); izq.add(tapa);
  const manilla = new THREE.Group(); manilla.position.set(hojaW / 2 - 0.012, 0, zHoja + 0.006);
  const roseta = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.085, 0.012), herraje);
  const palanca = new THREE.Group(); palanca.position.z = 0.012;
  const cuello = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.04, 16), herraje); cuello.rotation.x = Math.PI / 2; cuello.position.z = 0.014;
  const brazo = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.13, 0.018), herraje); brazo.position.set(0, -0.06, 0.03);
  palanca.add(cuello, brazo); manilla.add(roseta, palanca); izq.add(manilla);

  // ── Trozo de perfil cortado para «Pieza a pieza», metido en el travesaño de abajo ──
  // Mismo plano que el travesaño (sección en Y–Z, largo a lo largo de X); en la cara del corte se ve el PVC blanco.
  const L = 0.2;
  const muestra = new THREE.Group(); muestra.position.set(0, -ALTO / 2, 0); muestra.rotation.y = -Math.PI / 2; ventana.add(muestra);
  const matMuestra = { pvc: pvc.clone(), nucleo: nucleo.clone(), goma: goma.clone(), acero: acero.clone(), cristal: cristal.clone(), aluminio: aluminio.clone() };
  const pieza = (formas, mats, recto = true) => {
    const ge = barra(formas, L, false); ge.translate(-uC * mm, 0, -L / 2);
    return new THREE.Mesh(ge, mats);
  };
  const caraBlanca = [matMuestra.nucleo, matMuestra.pvc];      // grupo 0: tapas del corte; grupo 1: caras del perfil
  const partes = {
    marco: pieza(perfil.marco.map((p) => forma(p)), caraBlanca),
    juntaCentral: pieza(juntasMarco.map((p) => forma(p)), matMuestra.goma),
    hoja: pieza(perfil.hoja.map((p) => forma(p)), caraBlanca),
    juntasHoja: pieza(juntasHoja.map((p) => forma(p)), matMuestra.goma),
    junquillo: pieza(perfil.junquillo.map((p) => forma(p)), caraBlanca),
    aceroMarco: pieza(perfil.acero_marco.map((p) => forma(p)), matMuestra.acero),
    aceroHoja: pieza(perfil.acero_hoja.map((p) => forma(p)), matMuestra.acero),
  };
  const vidrio = new THREE.Group();
  for (let i = 0; i < 3; i++) {
    const luna = new THREE.Mesh(new THREE.BoxGeometry(0.004, 0.075, L), matMuestra.cristal);
    luna.position.set((g.u0 + 2 + i * 20 - uC) * mm, (g.borde_v + 37.5) * mm, 0); vidrio.add(luna);
    if (i < 2) { const sep = new THREE.Mesh(new THREE.BoxGeometry(0.016, 0.012, L), matMuestra.aluminio);
      sep.position.set((g.u0 + 12 + i * 20 - uC) * mm, (g.borde_v + 6) * mm, 0); vidrio.add(sep); }
  }
  partes.vidrio = vidrio;
  for (const k in partes) muestra.add(partes[k]);
  const ancla = (padre, u, v, z = L / 2) => { const o = new THREE.Object3D(); o.position.set((u - uC) * mm, v * mm, z); padre.add(o); return o; };
  anclas.marco = ancla(partes.marco, 8, 28);
  anclas.aceroMarco = ancla(partes.aceroMarco, 48, 12);
  anclas.juntaCentral = ancla(partes.juntaCentral, 30, 52);
  anclas.hoja = ancla(partes.hoja, 30, 100);
  anclas.aceroHoja = ancla(partes.aceroHoja, 58, 92);
  anclas.junquillo = ancla(partes.junquillo, 97, 110);
  anclas.vidrio = ancla(vidrio, g.u0 + 22, g.borde_v + 60);
  const centroMuestra = new THREE.Object3D(); centroMuestra.position.set(0, 75 * mm, 0.03); muestra.add(centroMuestra);

  ventana.position.y = -CAJON / 2;      // centra el conjunto (hueco + cajón)

  // Estado de la ventana: abrir 0–1 (0 cerrada, 1 a 90°), manilla 0–1 (0 abajo, 1 horizontal)
  function estado({ abrir = 0, manilla: m = 0 }) {
    const a = abrir * Math.PI / 2 * 0.95;
    for (const h of hojas) h.pivote.rotation.y = h.lado < 0 ? -a : a;
    palanca.rotation.z = m * Math.PI / 2;
  }
  // Visibilidad (0–1) de la ventana montada y del trozo de perfil; separa 0–1 abre el trozo en sus piezas
  const matsVentana = [pvc, goma, aluminio, herraje];
  function fundir(mats, o) { for (const x of mats) { x.transparent = o < 0.999; x.opacity = o; x.depthWrite = o > 0.5; } }
  function vistas({ ventana: ov = 1, muestra: om = 0, separa = 0 }) {
    fundir(matsVentana, ov); cristal.opacity = 0.3 * ov; pvcCajon.opacity = Math.min(pvcCajon.opacity, ov);
    for (const h of hojas) h.hoja.visible = ov > 0.01; marco.visible = juntasM.visible = ov > 0.01;
    fundir([matMuestra.pvc, matMuestra.nucleo, matMuestra.goma, matMuestra.acero, matMuestra.aluminio], om); matMuestra.cristal.opacity = 0.35 * om;
    muestra.visible = om > 0.01;
    const s = separa;
    partes.hoja.position.set(0, s * 0.045, 0); partes.juntasHoja.position.copy(partes.hoja.position);
    partes.junquillo.position.set(s * 0.035, s * 0.06, 0);
    vidrio.position.set(0, s * 0.11, 0);
    partes.aceroMarco.position.set(0, 0, s * 0.11); partes.aceroHoja.position.set(0, s * 0.045, s * 0.09);
    partes.juntaCentral.position.set(-s * 0.02, s * 0.018, 0);
  }
  function cajonVisible(f) { pvcCajon.opacity = f; cajon.visible = f > 0.02; pvcCajon.depthWrite = f > 0.98; }
  estado({}); vistas({});

  return { grupo: ventana, estado, vistas, cajonVisible, anclas, hojas, centroMuestra,
    medidas: { ancho: ANCHO, alto: ALTO, cajon: CAJON, hojaW, hojaH, vw, vh } };
}
