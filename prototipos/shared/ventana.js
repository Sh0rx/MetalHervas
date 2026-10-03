// Ventana de PVC de dos hojas practicables, antracita, con cajón de persiana, para el prototipo
// «Del taller a tu casa». Unidades: metros. Interior hacia +Z.
//
// MODELO PROVISIONAL: las medidas de los perfiles son genéricas. Cuando llegue la sección real del
// sistema GEALAN (DXF o PDF técnico), se sustituyen marcoRect() y las constantes de abajo por la
// extrusión de esa sección. Hasta entonces la web lo indica junto al modelo.
import * as THREE from "three";

const M = {
  ancho: 1.2, alto: 1.1,            // hueco de la ventana
  caraMarco: 0.062, fondoMarco: 0.074,
  caraHoja: 0.078, fondoHoja: 0.074, solape: 0.012,
  vidrio: 0.004, camara: 0.016,     // composición de ejemplo 4/16/4
  cajon: 0.19,
};

// Marco rectangular extruido: contorno exterior menos el hueco, con un bisel pequeño para que la luz dibuje los cantos.
function marcoRect(w, h, cara, fondo) {
  const s = new THREE.Shape();
  s.moveTo(-w / 2, -h / 2); s.lineTo(w / 2, -h / 2); s.lineTo(w / 2, h / 2); s.lineTo(-w / 2, h / 2); s.closePath();
  const iw = w / 2 - cara, ih = h / 2 - cara, hueco = new THREE.Path();
  hueco.moveTo(-iw, -ih); hueco.lineTo(-iw, ih); hueco.lineTo(iw, ih); hueco.lineTo(iw, -ih); hueco.closePath();
  s.holes.push(hueco);
  const g = new THREE.ExtrudeGeometry(s, { depth: fondo - 0.004, bevelEnabled: true, bevelThickness: 0.002, bevelSize: 0.0015, bevelSegments: 2 });
  g.translate(0, 0, -fondo / 2 + 0.002);
  return g;
}

export function crearVentana() {
  const pvc = new THREE.MeshStandardMaterial({ color: 0x353a3e, roughness: 0.48, metalness: 0.05 });   // antracita
  const junta = new THREE.MeshStandardMaterial({ color: 0x111213, roughness: 0.9 });
  const acero = new THREE.MeshStandardMaterial({ color: 0xa9adb0, roughness: 0.35, metalness: 0.85 });
  const aluminio = new THREE.MeshStandardMaterial({ color: 0x8e9396, roughness: 0.4, metalness: 0.7 });
  const cristal = new THREE.MeshPhysicalMaterial({ color: 0xdfe9ea, roughness: 0.04, metalness: 0, transmission: 0.92,
    thickness: 0.004, ior: 1.5, transparent: true, opacity: 0.35, side: THREE.DoubleSide, depthWrite: false });
  const herraje = new THREE.MeshStandardMaterial({ color: 0x2b2f32, roughness: 0.32, metalness: 0.6 });

  const ventana = new THREE.Group();
  const piezas = {};        // grupos que se separan en el despiece
  const anclas = {};        // puntos donde la web coloca las etiquetas

  // Marco fijo
  const marco = new THREE.Mesh(marcoRect(M.ancho, M.alto, M.caraMarco, M.fondoMarco), pvc);
  ventana.add(marco); piezas.marco = marco;
  anclas.marco = new THREE.Object3D(); anclas.marco.position.set(-M.ancho / 2 + 0.02, -M.alto * 0.3, 0.04); marco.add(anclas.marco);

  // Cajón de persiana, por encima del marco y enrasado con el interior
  const pvcCajon = pvc.clone(); pvcCajon.transparent = true;
  const cajon = new THREE.Mesh(new THREE.BoxGeometry(M.ancho + 0.02, M.cajon, 0.2), pvcCajon);
  cajon.position.set(0, M.alto / 2 + M.cajon / 2, 0.06);
  ventana.add(cajon); piezas.cajon = cajon;
  anclas.cajon = new THREE.Object3D(); anclas.cajon.position.set(M.ancho * 0.3, 0, 0.1); cajon.add(anclas.cajon);

  // Hojas: cada una cuelga de un pivote en su canto exterior
  const luzW = M.ancho - 2 * M.caraMarco + 2 * M.solape, luzH = M.alto - 2 * M.caraMarco + 2 * M.solape;
  const hojaW = luzW / 2, hojaH = luzH;
  const hojas = [];
  for (const lado of [-1, 1]) {           // -1 izquierda (lleva la manilla), +1 derecha
    const pivote = new THREE.Group();
    pivote.position.set(lado * luzW / 2, 0, M.fondoHoja * 0.25);
    ventana.add(pivote);

    const hoja = new THREE.Group();       // origen en el centro de la hoja
    hoja.position.x = -lado * hojaW / 2;
    pivote.add(hoja);

    const perfil = new THREE.Mesh(marcoRect(hojaW, hojaH, M.caraHoja, M.fondoHoja), pvc);
    hoja.add(perfil);

    // Refuerzo de acero galvanizado dentro del perfil (solo se ve en el despiece)
    const refuerzo = new THREE.Mesh(marcoRect(hojaW - 0.03, hojaH - 0.03, 0.022, 0.03), acero);
    refuerzo.visible = false; hoja.add(refuerzo);

    // Junta perimetral
    const juntaM = new THREE.Mesh(marcoRect(hojaW - 2 * M.caraHoja + 0.012, hojaH - 2 * M.caraHoja + 0.012, 0.008, 0.01), junta);
    juntaM.position.z = 0.03; hoja.add(juntaM);

    // Doble acristalamiento: dos lunas y el perfil separador entre ellas
    const vw = hojaW - 2 * M.caraHoja + 0.02, vh = hojaH - 2 * M.caraHoja + 0.02;
    const vidrio = new THREE.Group(); hoja.add(vidrio);
    const lunaExt = new THREE.Mesh(new THREE.BoxGeometry(vw, vh, M.vidrio), cristal); lunaExt.position.z = -(M.camara + M.vidrio) / 2;
    const lunaInt = new THREE.Mesh(new THREE.BoxGeometry(vw, vh, M.vidrio), cristal); lunaInt.position.z = (M.camara + M.vidrio) / 2;
    const separador = new THREE.Mesh(marcoRect(vw - 0.004, vh - 0.004, 0.012, M.camara), aluminio);
    vidrio.add(lunaExt, lunaInt, separador);

    // Bisagras en el canto exterior
    for (const y of [-hojaH / 2 + 0.12, hojaH / 2 - 0.12]) {
      const b = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.008, 0.09, 16), herraje);
      b.position.set(lado * (hojaW / 2 + 0.002), y, M.fondoHoja / 2); perfil.add(b);
    }

    const h = { lado, pivote, hoja, perfil, refuerzo, junta: juntaM, vidrio, lunaExt, lunaInt, separador };
    hojas.push(h);
  }

  // Manilla en el canto libre de la hoja izquierda, cara interior: roseta + palanca que gira 90°
  const izq = hojas[0];
  const manilla = new THREE.Group();
  manilla.position.set(hojaW / 2 - M.caraHoja / 2, 0, M.fondoHoja / 2 + 0.004);
  const roseta = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.085, 0.012), herraje);
  const palanca = new THREE.Group(); palanca.position.z = 0.012;
  const cuello = new THREE.Mesh(new THREE.CylinderGeometry(0.009, 0.009, 0.04, 16), herraje); cuello.rotation.x = Math.PI / 2; cuello.position.z = 0.014;
  const brazo = new THREE.Mesh(new THREE.BoxGeometry(0.02, 0.13, 0.018), herraje); brazo.position.set(0, -0.06, 0.03);
  palanca.add(cuello, brazo); manilla.add(roseta, palanca);
  izq.hoja.add(manilla);
  anclas.manilla = new THREE.Object3D(); anclas.manilla.position.set(0, -0.13, 0.04); manilla.add(anclas.manilla);

  anclas.perfil = new THREE.Object3D(); anclas.perfil.position.set(hojaW / 2 - 0.04, hojaH / 2 - 0.04, 0.04); hojas[1].hoja.add(anclas.perfil);
  anclas.refuerzo = new THREE.Object3D(); anclas.refuerzo.position.set(-hojaW / 2 + 0.01, hojaH * 0.3, 0); hojas[1].refuerzo.add(anclas.refuerzo);
  anclas.junta = new THREE.Object3D(); anclas.junta.position.set(hojaW / 2 - M.caraHoja, hojaH * 0.02, 0); hojas[1].junta.add(anclas.junta);
  anclas.vidrio = new THREE.Object3D(); anclas.vidrio.position.set(0.1, hojaH * 0.22, 0); hojas[1].vidrio.add(anclas.vidrio);

  ventana.position.y = -M.cajon / 2;      // centra el conjunto (hueco + cajón)

  // Estado: abrir 0–1 (0 cerrada, 1 a 90°), manilla 0–1 (0 abajo, 1 horizontal), despiece 0–1
  function estado({ abrir = 0, manilla: m = 0, despiece: e = 0 }) {
    const a = abrir * Math.PI / 2 * 0.95;
    for (const h of hojas) {
      h.pivote.rotation.y = h.lado < 0 ? -a : a;
      // Despiece hacia el interior (+Z): refuerzo, perfil, junta y lunas en capas
      h.refuerzo.visible = e > 0.01;
      h.refuerzo.position.z = e * 0.16;
      h.perfil.position.z = e * 0.3;
      h.junta.position.z = 0.03 + e * 0.44;
      h.lunaExt.position.z = -(M.camara + M.vidrio) / 2 + e * 0.56;
      h.separador.position.z = e * 0.66;
      h.lunaInt.position.z = (M.camara + M.vidrio) / 2 + e * 0.76;
    }
    manilla.position.z = M.fondoHoja / 2 + 0.004 + e * 0.92;
    palanca.rotation.z = m * Math.PI / 2;
    cajon.position.y = M.alto / 2 + M.cajon / 2 + e * 0.22;
  }
  estado({});

  // Visto desde fuera el cajón queda detrás de la fachada: se oculta y aparece al girar hacia dentro
  function cajonVisible(f) { pvcCajon.opacity = f; cajon.visible = f > 0.02; pvcCajon.depthWrite = f > 0.98; }

  return { grupo: ventana, estado, anclas, hojas, cajonVisible, medidas: { ...M, hojaW, hojaH, total: M.alto + M.cajon } };
}
