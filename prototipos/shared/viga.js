// Perfiles de acero con sus medidas reales y el «nudo»: esquina de pórtico con pilar y dos vigas
// a 90° (las aristas de un cubo), unidas con chapas de testa atornilladas.
// Lo comparten los prototipos Acero, Oficio y Blueprint. Unidades: metros.
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";

// Perfiles IPE según UNE-EN 10365 (mm): canto h, ala b, alma tw, ala tf, radio de acuerdo r
export const PERFILES = {
  "IPE 200": { h: 200, b: 100, tw: 5.6, tf: 8.5, r: 12 },
  "IPE 300": { h: 300, b: 150, tw: 7.1, tf: 10.7, r: 15 },
  "HEB 200": { h: 200, b: 200, tw: 9, tf: 15, r: 18 },
};

// Sección en doble T con los cuatro radios de acuerdo entre alma y alas
export function seccionI(p) {
  const m = 0.001, h = p.h * m, b = p.b * m, tw = p.tw * m, tf = p.tf * m, r = p.r * m;
  const H = h / 2, B = b / 2, W = tw / 2, s = new THREE.Shape();
  s.moveTo(-B, -H); s.lineTo(B, -H); s.lineTo(B, -H + tf); s.lineTo(W + r, -H + tf);
  s.absarc(W + r, -H + tf + r, r, -Math.PI / 2, -Math.PI, true);
  s.lineTo(W, H - tf - r);
  s.absarc(W + r, H - tf - r, r, Math.PI, Math.PI / 2, true);
  s.lineTo(B, H - tf); s.lineTo(B, H); s.lineTo(-B, H); s.lineTo(-B, H - tf); s.lineTo(-W - r, H - tf);
  s.absarc(-W - r, H - tf - r, r, Math.PI / 2, 0, true);
  s.lineTo(-W, -H + tf + r);
  s.absarc(-W - r, -H + tf + r, r, 0, -Math.PI / 2, true);
  s.lineTo(-B, -H + tf);
  return s;
}

// Barra extruida a lo largo de +Z. corteIni/corteFin: ángulo (rad) del corte respecto al corte recto,
// para que una viga inclinada apoye a plomo contra el pilar. Colores por vértice: alas oscuras y alma gris,
// los dos tonos de la viga del logo.
export function barra(p, largo, { corteIni = 0, corteFin = 0, alas = 0x26292c, alma = 0x9a9fa3 } = {}) {
  const g = new THREE.ExtrudeGeometry(seccionI(p), { depth: largo, bevelEnabled: false, curveSegments: 6 });
  const pos = g.attributes.position, col = new Float32Array(pos.count * 3);
  const cA = new THREE.Color(alas), cW = new THREE.Color(alma), c = new THREE.Color();
  const H = p.h / 2000, tf = p.tf / 1000, r = p.r / 1000;
  for (let i = 0; i < pos.count; i++) {
    const y = pos.getY(i), z = pos.getZ(i);
    if (z < 1e-6) pos.setZ(i, y * Math.tan(corteIni));
    else if (z > largo - 1e-6) pos.setZ(i, largo - y * Math.tan(corteFin));
    // 0 en el alma, 1 en las alas; transición suave a lo largo del radio de acuerdo
    const t = THREE.MathUtils.smoothstep(Math.abs(y), H - tf - r, H - tf);
    c.copy(cW).lerp(cA, t); col.set([c.r, c.g, c.b], i * 3);
  }
  g.setAttribute("color", new THREE.BufferAttribute(col, 3));
  g.computeVertexNormals();
  return g;
}

export function aceroMaterial() {
  return new THREE.MeshPhysicalMaterial({
    vertexColors: true, metalness: 0.85, roughness: 0.4, clearcoat: 0.2, clearcoatRoughness: 0.45,
    envMapIntensity: 0.4,
  });
}

export function entorno(renderer, scene) {
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  pm.dispose();
}

// Orienta una barra (extruida en +Z con el canto en Y) a lo largo de la dirección d, con el alma vertical
function orientar(obj, d) {
  const z = d.clone().normalize();
  const x = new THREE.Vector3().crossVectors(new THREE.Vector3(0, 1, 0), z).normalize();
  const y = new THREE.Vector3().crossVectors(z, x);
  obj.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, y, z));
}

// El nudo: esquina de un pórtico en la que pilar y dos vigas forman las tres aristas de un cubo.
//  · Pilar vertical, con las alas perpendiculares a X.
//  · Viga 1 hacia −X, atornillada con chapa de testa al ala del pilar.
//  · Viga 2 hacia +Z, atornillada con chapa de testa al alma del pilar (entre sus alas).
//  · El pilar sigue por encima del nudo, como en el logo.
// Devuelve el grupo y sus piezas, con su posición final en userData.fin para animar el montaje.
export function nudo({ perfil = "IPE 300", alturaNudo = 3.6, largoViga = 3.2, sobrePilar = 1.2 } = {}) {
  const p = PERFILES[perfil], mat = aceroMaterial(), h = p.h / 1000, b = p.b / 1000, tw = p.tw / 1000;
  const chapa = 0.02, grupo = new THREE.Group(), piezas = {};
  const arriba = alturaNudo + h / 2;            // cara superior de las vigas

  // Pilar: Z de la extrusión → Y; canto (Y) → X. Como en el logo, sigue por encima de las vigas
  // En el logo el pilar se ve al revés que las vigas: cara del ala gris y costado (alma) en negro
  const pilar = new THREE.Mesh(barra(p, arriba + sobrePilar, { alas: 0x9a9fa3, alma: 0x26292c }), mat);
  pilar.rotation.x = -Math.PI / 2; pilar.rotation.z = Math.PI / 2;
  piezas.pilar = pilar;

  const viga1 = new THREE.Mesh(barra(p, largoViga), mat);
  orientar(viga1, new THREE.Vector3(-1, 0, 0));
  viga1.position.set(-h / 2 - chapa, alturaNudo, 0);
  piezas.viga1 = viga1;

  const viga2 = new THREE.Mesh(barra(p, largoViga), mat);
  orientar(viga2, new THREE.Vector3(0, 0, 1));
  viga2.position.set(0, alturaNudo, tw / 2 + chapa);
  piezas.viga2 = viga2;

  // Chapas de testa con 6 tornillos M20 (cabeza hexagonal), del lado de la viga
  const chapaMat = new THREE.MeshPhysicalMaterial({ color: 0x8d9296, metalness: 0.9, roughness: 0.42 });
  const tornMat = new THREE.MeshPhysicalMaterial({ color: 0xc4c8cb, metalness: 1, roughness: 0.28 });
  const cabeza = new THREE.CylinderGeometry(0.017, 0.017, 0.013, 6);
  const altoChapa = h + 0.06;
  const union = (ancho) => {          // chapa en el plano YZ local, tornillos hacia −X local
    const g = new THREE.Group();
    g.add(new THREE.Mesh(new THREE.BoxGeometry(chapa, altoChapa, ancho), chapaMat));
    for (const dy of [-0.108, 0, 0.108]) for (const dz of [-0.048, 0.048]) {
      const t = new THREE.Mesh(cabeza, tornMat);
      t.rotation.z = Math.PI / 2; t.position.set(-(chapa / 2 + 0.0065), dy, dz);
      g.add(t);
    }
    return g;
  };
  piezas.union1 = union(b + 0.02);
  piezas.union1.position.set(-h / 2 - chapa / 2, alturaNudo, 0);
  piezas.union2 = union(b + 0.02);      // cabe entre las alas del pilar (luz libre h − 2·tf)
  piezas.union2.rotation.y = Math.PI / 2;  // −X local → +Z
  piezas.union2.position.set(0, alturaNudo, tw / 2 + chapa / 2);

  for (const k in piezas) {
    const o = piezas[k];
    o.userData.fin = { pos: o.position.clone(), quat: o.quaternion.clone() };
    grupo.add(o);
  }
  return { grupo, piezas, esquina: new THREE.Vector3(0, alturaNudo, 0), largoViga };
}
