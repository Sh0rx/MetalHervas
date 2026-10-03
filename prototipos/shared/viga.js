// Perfiles de acero con sus medidas reales y el «nudo» del logo de Metal Hervás
// (pilar + dintel inclinado + ménsula, unidos con chapa de testa atornillada).
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
// para que un dintel inclinado apoye a plomo contra el pilar. Colores por vértice: alas oscuras, alma clara,
// como en el logo (alas negras, alma gris).
export function barra(p, largo, { corteIni = 0, corteFin = 0, alas = 0x2a2f33, alma = 0x767c82 } = {}) {
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
    envMapIntensity: 0.8,
  });
}

export function entorno(renderer, scene) {
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  pm.dispose();
}

// Orienta una barra (extruida en +Z con el canto en Y) a lo largo de la dirección d dentro del plano XY
function orientar(obj, d) {
  const z = d.clone().normalize(), y = new THREE.Vector3(-z.y, z.x, 0);
  if (y.y < 0) y.negate();
  const x = new THREE.Vector3().crossVectors(y, z);
  obj.quaternion.setFromRotationMatrix(new THREE.Matrix4().makeBasis(x, y, z));
}

// El nudo del logo. Devuelve el grupo y sus piezas (con su posición final guardada en userData.fin)
// para poder animar el montaje.
export function nudo({ perfil = "IPE 300", altoPilar = 4.4, alturaNudo = 3.95, largoDintel = 3.8,
                      largoMensula = 0.95, pendiente = THREE.MathUtils.degToRad(20) } = {}) {
  const p = PERFILES[perfil], mat = aceroMaterial(), h = p.h / 1000, b = p.b / 1000;
  const chapa = 0.02, grupo = new THREE.Group(), piezas = {};

  // Pilar: alas perpendiculares a X, de modo que dintel y ménsula atornillan a sus caras
  const pilar = new THREE.Mesh(barra(p, altoPilar), mat);
  pilar.rotation.x = -Math.PI / 2; pilar.rotation.z = Math.PI / 2;
  piezas.pilar = pilar;

  const tan = Math.tan(pendiente);
  // Dintel: sube hacia la izquierda desde la cara del pilar, corte a plomo en el nudo
  const dintel = new THREE.Mesh(barra(p, largoDintel, { corteIni: pendiente }), mat);
  orientar(dintel, new THREE.Vector3(-Math.cos(pendiente), Math.sin(pendiente), 0));
  dintel.position.set(-h / 2 - chapa, alturaNudo, 0);
  piezas.dintel = dintel;

  // Ménsula (vuelo) al otro lado, en la prolongación del dintel
  const yM = alturaNudo - (h + 2 * chapa) * tan;
  const mensula = new THREE.Mesh(barra(p, largoMensula, { corteIni: -pendiente }), mat);
  orientar(mensula, new THREE.Vector3(Math.cos(pendiente), -Math.sin(pendiente), 0));
  mensula.position.set(h / 2 + chapa, yM, 0);
  piezas.mensula = mensula;

  // Chapas de testa y tornillos M20 (cabeza hexagonal)
  const altoChapa = h / Math.cos(pendiente) + 0.08;
  const chapaGeo = new THREE.BoxGeometry(chapa, altoChapa, b + 0.02);
  const chapaMat = new THREE.MeshPhysicalMaterial({ color: 0x8d9296, metalness: 0.9, roughness: 0.42 });
  const tornMat = new THREE.MeshPhysicalMaterial({ color: 0xc4c8cb, metalness: 1, roughness: 0.28 });
  const cabeza = new THREE.CylinderGeometry(0.017, 0.017, 0.013, 6);
  const union = (x, y, lado) => {
    const g = new THREE.Group();
    g.add(new THREE.Mesh(chapaGeo, chapaMat));
    for (const dy of [-0.3, 0, 0.3]) for (const dz of [-0.048, 0.048]) {
      const t = new THREE.Mesh(cabeza, tornMat);
      t.rotation.z = Math.PI / 2; t.position.set(lado * (chapa / 2 + 0.0065), dy * altoChapa * 0.9, dz);
      g.add(t);
    }
    g.position.set(x, y, 0);
    return g;
  };
  piezas.unionDintel = union(-h / 2 - chapa / 2, alturaNudo, -1);
  piezas.unionMensula = union(h / 2 + chapa / 2, yM, 1);

  for (const k in piezas) {
    const o = piezas[k];
    o.userData.fin = { pos: o.position.clone(), quat: o.quaternion.clone() };
    grupo.add(o);
  }
  return { grupo, piezas, centro: new THREE.Vector3(-1.1, 3.1, 0) };
}
