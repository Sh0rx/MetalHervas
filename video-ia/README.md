# Vídeo con IA · prueba de los tramos 1 y 2

Kit para generar los dos primeros tramos de la web animada con **Google Flow** (imágenes clave) y **Seedance 2.5 vía APIMart** (vídeo). La web luego hace avanzar el vídeo con el scroll.

## La idea, ajustada a las fotos que tenemos

Tenemos fotos reales de ventanas vuestras **desde dentro** (con el film de GEALAN y las etiquetas de Climalit todavía puestos), pero no desde fuera. Por eso la prueba empieza dentro y sale fuera:

| Tramo | Qué pasa | Primer fotograma | Último fotograma |
|---|---|---|---|
| 1 · La ventana | Habitación a la hora azul; nos acercamos y la ventana se abre | **K1** · ventana cerrada (foto real) | **K2** · ventana abierta (foto real) |
| 2 · Salimos | Cruzamos la ventana y salimos al valle al anochecer | **K2** | **K3** · el Valle del Ambroz al anochecer |

Así el producto es **real en los fotogramas clave**: la IA solo rellena el movimiento entre ellos. Es lo que más reduce el riesgo de que invente la ventana.

## 1 · Fotos de partida

| Clave | Archivo | Origen |
|---|---|---|
| K1 | `fuentes/ventana-cerrada.jpg` | GEALAN de dos hojas, antracita, con cajón de persiana, cerrada (2048 × 1536) |
| K2 | `fuentes/ventana-abierta.jpg` | Ventana de dos hojas abierta de par en par (1536 × 2048, vertical) |
| K3 | **falta** | Una foto real del valle desde Hervás al anochecer, hecha con el móvil |

**Lo ideal**, si la familia puede, son 3 fotos nuevas hechas a la hora azul (unos 20 minutos después de ponerse el sol), con el móvil apoyado y sin moverlo entre las dos primeras:

1. Una ventana vuestra ya terminada, cerrada, desde dentro, con la luz de la habitación encendida.
2. **La misma ventana, desde el mismo sitio**, con las dos hojas abiertas.
3. El valle desde una ventana o un balcón de Hervás.

Con eso K1 y K2 son la misma habitación y la transición sale mucho más limpia. Con las fotos actuales también funciona, pero son dos habitaciones distintas y la IA tiene que «fundirlas».

## 2 · Google Flow: profesionalizar las claves

Reglas, las mismas de `docs/google-flow-prompt.md`: **la ventana no se toca** (color, número de hojas, herrajes, cajón de persiana, proporciones). Se puede cambiar la luz y limpiar la escena. **Excepción consciente:** aquí cambiamos la hora del día a la hora azul. Es ambientación, no producto.

Haz cada clave en **dos formatos**: **16:9** (ordenador) y **9:16** (móvil). Seedance exige que el primer y el último fotograma de un clip tengan la misma proporción. Al ampliar el encuadre, que Flow añada solo pared, techo y suelo, nunca más ventana.

### K1 · ventana cerrada (sobre `ventana-cerrada.jpg`)

```
Edit this photo. Keep the window exactly as it is: two-leaf anthracite grey PVC window with a roller-shutter box above, same frame and sash widths, same central handle, same glass division, same proportions and position. Do not add or remove any part of the window.
Change only light and cleanliness: blue hour just after sunset, deep blue sky outside, the exterior softly out of focus. Warm light from an unseen ceiling lamp gently lights the room. Remove the protective film, printed logos and stickers from frame and glass. Clean the walls of dust, cables and plaster marks; keep the room empty, no furniture, no people, no text.
Photorealistic architectural interior photography, 24 mm lens, straight verticals, eye level, centered on the window.
Extend the frame to [16:9 | 9:16] by adding only wall, ceiling and floor around the window.
```

### K2 · ventana abierta (sobre `ventana-abierta.jpg`, con K1 como imagen de referencia)

```
Edit this photo. Keep the window exactly as it is: two-leaf anthracite grey PVC window, both sashes open inward at their exact current angles, same handles, same frame, same roller-shutter box. Do not change the window.
Match the light, colour and room of the reference image: blue hour just after sunset, warm interior light, clean empty room. Remove protective film, logos and stickers. The view outside: evening sky over soft hills, out of focus.
Photorealistic architectural interior photography, 24 mm lens, straight verticals, eye level, same camera height and distance as the reference.
Extend the frame to [16:9 | 9:16] with only wall, ceiling and floor.
```

### K3 · el valle (sobre la foto real del valle)

```
Improve this landscape photo only in light and colour: blue hour, the last warm light on the horizon, first lights in the village below. Do not add buildings, roads or mountains. Photorealistic, natural colours, no text.
Reframe to [16:9 | 9:16].
```

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

### Clip A · tramo 1 (K1 → K2)

```
Slow, steady dolly-in toward the window at eye level, as if gently walking closer. The two sashes swing inward and open fully, smoothly, from the closed position to the open position. The window keeps its exact shape, colour and handles at all times. Blue hour light, warm lamp light inside. One continuous shot, no cuts, no camera shake, no people, no text. Photorealistic.
```

### Clip B · tramo 2 (K2 → K3)

```
The camera keeps gliding forward at the same speed, passes through the open window between the two sashes, and flies out into the evening air over the valley, rising slightly and ending on the view of the valley at blue hour. One continuous shot, no cuts, smooth and calm, no people, no text. Photorealistic.
```

### Con el script

`scripts/seedance.py` sube las imágenes a APIMart, lanza el trabajo, espera el resultado y descarga el vídeo a `video-ia/salidas/`. La clave se lee de la variable de entorno `APIMART_API_KEY`; no se escribe en ningún archivo.

```bash
python scripts/seedance.py clip --primero video-ia/claves/k1-16x9.png --ultimo video-ia/claves/k2-16x9.png --prompt video-ia/prompts/clip-a.txt --nombre clip-a-16x9 --borrador
python scripts/seedance.py final --borrador-id <task_id del borrador> --nombre clip-a-16x9
```

## 4 · Coste aproximado

Precios de APIMart a 17-09-2026, por segundo de vídeo; el coste real lo devuelve cada tarea.

| Paso | Cálculo | Coste |
|---|---|---|
| Borrador de 6 s (480p) | 6 × 0,096 $ | ≈ 0,58 $ |
| Final de 6 s (1080p) | 6 × 0,385 $ | ≈ 2,31 $ |
| Prueba completa: 2 clips × 2 formatos, unos 3 borradores por clip y 1 final | — | **≈ 16 $** |

## 5 · Revisión de cada clip

- [ ] La ventana nunca cambia de forma, de color ni de número de hojas, y no aparecen herrajes nuevos.
- [ ] Las hojas abren hacia dentro, como en la realidad.
- [ ] No hay cortes ni saltos: el scroll tiene que poder ir adelante y atrás.
- [ ] No hay personas, texto ni marcas de agua.
- [ ] El último fotograma del clip A encaja con el primero del clip B.

## 6 · Aviso en la web

El vídeo está generado con IA a partir de fotos reales. Para no confundir al cliente, el pie de la web llevará:

> «Animación creada con IA a partir de fotos de nuestras obras.»

Las fotos de casas de clientes solo se publican con su permiso.
