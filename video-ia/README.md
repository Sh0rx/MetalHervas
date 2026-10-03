# Vídeo con IA · «Del taller a tu casa»

Kit para generar el recorrido animado de la web con **Google Flow** (imágenes clave) y **Seedance 2.5 vía APIMart** (vídeo). La web hace avanzar el vídeo con el scroll y, al final, la ventana «sale» de la casa y pasa a ser un modelo 3D (despiece, galería de obras y presupuesto). Plan completo: `C:\Users\Jorge\.claude\plans\en-relacion-con-la-robust-kettle.md`.

## El recorrido

Cinco clips encadenados: el **último fotograma de cada clip es el primero del siguiente**. El orden vive en `clips.json`.

| Clip | Qué pasa | Primer fotograma | Último fotograma |
|---|---|---|---|
| 0 · El taller | Avanzamos entre las ventanas recién hechas y entramos en el vidrio de una | **K0** · taller (foto real) | **KV** · vidrio con luz desenfocada |
| 1 · Llegamos a casa | La luz se enfoca y aparece la habitación con la ventana instalada | **KV** | **K1** · ventana cerrada (foto real) |
| A · Se abre | Nos acercamos y las dos hojas se abren | **K1** | **K2** · ventana abierta (foto real) |
| B · Salimos | Cruzamos la ventana y salimos al valle | **K2** | **K3** · el valle al anochecer |
| C · Giro de 180º | Nos damos la vuelta y miramos la casa: la ventana, de frente | **K3** | **K4** · fachada con la ventana abierta |

Después del clip C la web funde a la ventana en 3D (Three.js), con la cámara alineada a K4.

**KV es el truco que une taller y casa:** las ventanas del taller son blancas y la de la casa es antracita. Si pidiéramos a la IA ir de una a otra, «transformaría» la ventana. Con un fotograma intermedio de puro vidrio y luz, el cambio es un corte invisible y no se inventa producto.

Así el producto es **real en los fotogramas clave**: la IA solo rellena el movimiento entre ellos.

**Prueba con fachada inventada.** Para la primera prueba K3 (valle) y K4 (fachada) los genera la IA. Si el recorrido gusta, se sustituyen por fotos reales (ver «Lo ideal» abajo) y se regeneran solo los clips B y C. Mientras sean inventadas, la web lo dice.

## 1 · Fotos de partida

| Clave | Archivo | Origen |
|---|---|---|
| K0 | `../prototipos/assets/fotos/taller-ventanas-pvc-blancas.webp` (original en `recursos-multimedia/`) | Taller: filas de ventanas GEALAN blancas con cajón de persiana, puente grúa |
| KV | — | Se genera en Flow (o se saca de K0, ver abajo) |
| K1 | `fuentes/ventana-cerrada.jpg` | GEALAN de dos hojas, antracita, con cajón de persiana, cerrada (2048 × 1536) |
| K2 | `fuentes/ventana-abierta.jpg` | Ventana de dos hojas abierta de par en par (1536 × 2048, vertical) |
| K3 | — (provisional, IA) | Más adelante: foto real del valle desde Hervás al anochecer |
| K4 | — (provisional, IA), con `../prototipos/assets/fotos/chalet-travertino-fachada.webp` de referencia de estilo | Más adelante: foto real de la misma ventana desde fuera |

Las claves terminadas se guardan en `claves/` con estos nombres: `k0-16x9.jpg`, `kv-16x9.jpg`, `k1-16x9.jpg`, `k2-16x9.jpg`, `k3-16x9.jpg`, `k4-16x9.jpg` (y luego las `-9x16`). **Primero solo 16:9**; el formato móvil cuando el recorrido guste.

**Lo ideal**, si la familia puede, son 3 fotos nuevas hechas a la hora azul (unos 20 minutos después de ponerse el sol), con el móvil apoyado y sin moverlo entre las dos primeras:

1. Una ventana vuestra ya terminada, cerrada, desde dentro, con la luz de la habitación encendida.
2. **La misma ventana, desde el mismo sitio**, con las dos hojas abiertas.
3. El valle desde esa ventana o desde un balcón de Hervás.
4. **La misma ventana desde fuera**, de frente, con las hojas abiertas y la luz de dentro encendida.
5. En el taller, una ventana antracita terminada, de pie, con la cámara a la altura de los ojos.

Con eso K1 y K2 son la misma habitación, K4 es la casa real y la transición sale mucho más limpia. Con las fotos actuales también funciona, pero son dos habitaciones distintas y la IA tiene que «fundirlas».

## 2 · Google Flow: profesionalizar las claves

Reglas, las mismas de `docs/google-flow-prompt.md`: **la ventana no se toca** (color, número de hojas, herrajes, cajón de persiana, proporciones). Se puede cambiar la luz y limpiar la escena. **Excepción consciente:** aquí cambiamos la hora del día a la hora azul. Es ambientación, no producto.

Cada clave hará falta en **dos formatos**: **16:9** (ordenador) y **9:16** (móvil); empieza solo por 16:9. Seedance exige que el primer y el último fotograma de un clip tengan la misma proporción. Al ampliar el encuadre, que Flow añada solo pared, techo y suelo, nunca más ventana.

### K0 · el taller (sobre `taller-ventanas-pvc-blancas`)

```
Edit this photo. It is a real photo of our window workshop: rows of newly made white PVC windows with roller-shutter boxes standing on the floor, with their protective film on. Keep every window exactly as it is: same frames, sashes, handles, shutter boxes, film, proportions, number and positions. Do not add, remove or move any window.
Remove only the cardboard boxes, plastic and packing waste in the foreground; keep the red floor, the overhead crane and the roof structure. Hide the phone number printed on the crane. Light: warm late-afternoon light, clean and gentle, slight haze in the air.
Photorealistic photography, 24 mm lens, eye level, straight verticals; the nearest window is the main subject.
Extend the frame to 16:9 by adding only floor, roof and wall.
```

### KV · el vidrio (nueva, con K0 y K1 como referencias)

```
Extreme close-up through a clean pane of double glazing: the glass fills the entire frame, no frame edges visible. Soft, out-of-focus light and gentle reflections: warm workshop amber on the left blending into cool blue-hour light on the right. Photorealistic macro photography, very shallow depth of field, no objects, no text. 16:9.
```

Si Flow lo complica, vale un recorte muy desenfocado de K0:
`ffmpeg -i claves/k0-16x9.png -vf "crop=iw/3:ih/3,scale=1920:1080,gblur=sigma=60" claves/kv-16x9.png`

**Orden en Flow: K3 (valle) primero**, porque K1 y K2 lo usan como vista exterior; así las tres claves cuentan con el mismo paisaje. Después K1, K2, K0, KV y K4.

### K1 · ventana cerrada (sobre `ventana-cerrada.jpg`, con K3 como referencia del exterior)

```
Edit this photo. Keep the window exactly as it is: two-leaf anthracite grey PVC window with a roller-shutter box above, same frame and sash widths, same glass division, same proportions and position. The window has exactly ONE handle in total, in the centre where the two sashes meet; keep it exactly there and do not add any other handle. Do not add or remove any part of the window.
Replace everything seen through the glass with the landscape of the reference image (the valley at blue hour), softly out of focus: no buildings, no walls, no construction site outside.
Light: blue hour just after sunset; warm light from an unseen ceiling lamp gently lights the room. Remove the protective film, printed logos and stickers from frame and glass. Clean the walls of dust, cables and plaster marks; keep the room empty, no furniture, no people, no text.
Photorealistic architectural interior photography, 24 mm lens, straight verticals, eye level, centered on the window.
Extend the frame to [16:9 | 9:16] by adding only wall, ceiling and floor around the window.
```

### K2 · ventana abierta (sobre **K1 terminada**, con `ventana-abierta.jpg` como referencia de cómo es la hoja abierta)

Se parte de K1 y no de la foto abierta: así K1 y K2 tienen el mismo encuadre, la misma habitación y el mismo valle, y solo cambia la posición de las hojas. La foto abierta es real (hoja, bisagras y grosor del perfil) y sirve de referencia. Abrir las dos hojas es un uso normal de esta ventana, no un cambio del producto.

```
Edit this photo. Change only one thing: open the window. Both sashes swing inward into the room and open fully and symmetrically, each rotated about 90 degrees on its outer hinges, mirror images of each other, both standing perpendicular to the wall at the same angle. The left sash carries the single handle on its free edge and is opened exactly as far as the right sash. The right sash has no handle.
Keep everything else exactly as it is: same camera position and framing, same room, same light, same roller-shutter box, same anthracite grey colour, same frame and sash profile widths, same glass. The window still has exactly ONE handle in total; do not add any other handle or hardware. The reference image shows how one of these sashes really looks when open (thickness, hinges, colour): match it.
Through the open window the same valley at blue hour stays visible, softly out of focus. No people, no text, no reflections of people.
Photorealistic architectural interior photography, 16:9.
```

**Si sigue saliendo una segunda manilla:** genera otra vez y, en la variante buena, borra la de sobra con la edición por zonas de Flow (selecciona solo la manilla y pide `remove this handle, keep the sash profile intact`).

### K3 · el valle

**Provisional (prueba), generada:**

```
Photorealistic open landscape photograph at blue hour: the Ambroz valley in northern Cáceres, Spain, seen from about six metres above the ground, camera floating in the open air. Green chestnut and oak hills, a small village of stone houses with clay-tile roofs below with its first lights on, mountains on the horizon with the last warm light in the sky. Calm, natural colours.
Pure landscape only: no window, no window frame, no glass, no wall, no railing, no balcony, no interior, nothing in the foreground framing the view. No people, no text. 16:9.
```

**Definitiva, sobre la foto real del valle:**

```
Improve this landscape photo only in light and colour: blue hour, the last warm light on the horizon, first lights in the village below. Do not add buildings, roads or mountains. Photorealistic, natural colours, no text.
Reframe to [16:9 | 9:16].
```

### K4 · la ventana desde fuera (provisional, generada; con K2 y `chalet-travertino-fachada` como referencias)

```
Exterior view at blue hour of a modern two-storey house with a cream travertine stone facade, like the second reference image. The camera floats at first-floor height, straight in front of one window, centred, frontal, straight verticals. The window is the same as in the first reference image, seen from outside: two-leaf anthracite grey PVC casement window, both sashes open inward, roller shutter fully raised so only its thin guides and slot show, slim travertine sill. Warm lamp light in the empty room behind. Same proportions as the reference window. No people, no text, no other windows in the centre of the frame.
Photorealistic architectural photography, 35 mm lens. 16:9.
```

Revisa especialmente que tenga **dos hojas**, que abran **hacia dentro** y que el color sea el mismo antracita.

**Revisión antes de seguir** (lado a lado con la foto original):
- La ventana tiene las mismas hojas, herrajes, cajón y color.
- No se ha añadido nada a la ventana.
- No hay matrículas, números de calle ni caras.

## 3 · Seedance 2.5: los clips

Modelo `seedance-2.5` en APIMart. Primer y último fotograma con `image_with_roles` (`first_frame` y `last_frame`). La proporción tiene que ser `adaptive`: sale la de las imágenes.

| Ajuste | Valor | Por qué |
|---|---|---|
| `duration` | 6 s | Unos 150 fotogramas por tramo: suficiente para un scroll suave |
| `generate_audio` | `false` | La web no lleva sonido |
| `watermark` | `false` | Se avisa en la web con un texto (abajo) |
| Borrador | `draft: true` (480p) | Primero se prueba el movimiento barato |
| Final | `draft_task_id` → 1080p | Solo del borrador que convenza |
| `return_last_frame` | `true` | Para encadenar clips si hace falta |

Los prompts están en `prompts/` (`clip-0.txt`, `clip-1.txt`, `clip-a.txt`, `clip-b.txt`, `clip-c.txt`). Los de los clips A y B:

### Clip A · se abre (K1 → K2)

```
Slow, steady dolly-in toward the window at eye level, as if gently walking closer. The two sashes swing inward and open fully, smoothly, from the closed position to the open position. The window keeps its exact shape, colour and handles at all times. Blue hour light, warm lamp light inside. One continuous shot, no cuts, no camera shake, no people, no text. Photorealistic.
```

### Clip B · salimos (K2 → K3)

```
The camera keeps gliding forward at the same speed, passes through the open window between the two sashes, and flies out into the evening air over the valley, rising slightly and ending on the view of the valley at blue hour. One continuous shot, no cuts, smooth and calm, no people, no text. Photorealistic.
```

### Con el script

`scripts/seedance.py` sube las imágenes a APIMart, lanza el trabajo, espera el resultado y descarga el vídeo a `video-ia/salidas/`. La clave se lee de la variable de entorno `APIMART_API_KEY`; no se escribe en ningún archivo.

Todos los borradores de golpe (se salta los clips a los que les falte alguna clave), y luego el final de los que convenzan:

```bash
python scripts/seedance.py lote --formato 16x9 --borrador
python scripts/seedance.py lote --formato 16x9 --borrador --solo clip-c
python scripts/seedance.py final --borrador-id <task_id del borrador> --nombre clip-c-16x9
```

Un clip suelto, a mano:

```bash
python scripts/seedance.py clip --primero video-ia/claves/k1-16x9.png --ultimo video-ia/claves/k2-16x9.png --prompt video-ia/prompts/clip-a.txt --nombre clip-a-16x9 --borrador
```

**Plan B:** si Seedance no resuelve bien el giro de 180º (clip C), probar ese clip con Veo en Google Flow, que también acepta primer y último fotograma.

### De los clips a la web

`scripts/secuencia.py` toma los clips en el orden de `clips.json` (el final 1080p, o el borrador si aún no hay final), mide las costuras entre clips y saca los fotogramas WebP que la web pinta al hacer scroll, en `prototipos/assets/recorrido/<formato>/` con su `manifest.json`.

```bash
python scripts/secuencia.py --formato 16x9
```

Una costura por debajo de ~0,85 de SSIM se notará como un salto: repetir ese clip o igualar color en DaVinci Resolve.

## 4 · Coste aproximado

Precios de APIMart a 17-09-2026, por segundo de vídeo; el coste real lo devuelve cada tarea.

| Paso | Cálculo | Coste |
|---|---|---|
| Borrador de 6 s (480p) | 6 × 0,096 $ | ≈ 0,58 $ |
| Final de 6 s (1080p) | 6 × 0,385 $ | ≈ 2,31 $ |
| Recorrido en 16:9: 5 clips, unos 3 borradores por clip y 1 final | 5 × (3 × 0,58 + 2,31) | **≈ 20 $** |
| Lo mismo en 9:16 (cuando guste) | — | ≈ 20 $ |

## 5 · Revisión de cada clip

- [ ] La ventana nunca cambia de forma, de color ni de número de hojas, y no aparecen herrajes nuevos.
- [ ] Las hojas abren hacia dentro, como en la realidad.
- [ ] No hay cortes ni saltos: el scroll tiene que poder ir adelante y atrás.
- [ ] No hay personas, texto ni marcas de agua.
- [ ] El último fotograma de cada clip encaja con el primero del siguiente (`secuencia.py` lo mide).
- [ ] Clip 0: las ventanas del taller no se convierten en otra cosa antes de llegar al vidrio.
- [ ] Clip C: el giro es suave y termina de frente, con la ventana centrada.

## 6 · Aviso en la web

El vídeo está generado con IA a partir de fotos reales. Para no confundir al cliente, el pie de la web llevará:

> «Animación creada con IA a partir de fotos de nuestras obras.»

Mientras K3 y K4 sean inventadas, se añade: «El paisaje y la fachada exterior son recreaciones.»

Las fotos de casas de clientes solo se publican con su permiso.
