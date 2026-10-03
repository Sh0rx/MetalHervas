# Google Flow — plantilla para mejorar fotos de obras sin alterar el producto

**Regla de oro:** la foto puede verse mejor, pero el producto tiene que ser exactamente el mismo. Si un cliente ve la foto y luego la ventana real, no puede notar ninguna diferencia.

## Prompt base (copiar tal cual y añadir debajo la línea «Esta foto»)

```
Retoque fotográfico profesional de una obra real de carpintería (ventanas, puertas,
cerramientos, barandillas o estructuras metálicas). Es una foto de un trabajo real que
se va a mostrar a clientes: NO se puede inventar ni modificar nada del producto.

PERMITIDO:
- Corregir exposición, balance de blancos, contraste y nitidez.
- Enderezar verticales y corregir la perspectiva de la cámara.
- Mejorar el cielo y la luz ambiente de forma natural (luz de día suave, sin dramatismo).
- Limpiar suciedad temporal de obra (escombros, herramientas, cubos, plásticos, cintas,
  andamios que tapen la vista) SOLO si no tocan ni tapan el producto.
- Ocultar o difuminar matrículas, caras de personas ajenas, números de calle y
  cualquier dato que identifique la dirección.

PROHIBIDO (el resultado no vale si se incumple cualquiera):
- Cambiar el color, el acabado, la textura o el brillo de los perfiles, puertas,
  vidrios, herrajes o barandillas.
- Cambiar el número de hojas, la división de vidrios, el tipo de apertura, la forma,
  el tamaño o las proporciones de cualquier elemento.
- Añadir, quitar o mover ventanas, puertas, manillas, persianas, rejas, barrotes,
  tornillos, soldaduras o cualquier elemento constructivo.
- Añadir muebles, plantas, personas, coches, decoración o arquitectura que no existan.
- Cambiar la fachada, los materiales del edificio o el entorno de forma reconocible.
- Estilo de render 3D, ilustración o «perfección» artificial: tiene que seguir siendo
  una fotografía real.

Mantén la misma composición y el mismo encuadre (como mucho, recorte ligero).
```

## Línea específica por foto (ejemplos)

- `Esta foto: fachada de travertino con ventanas y puerta de aluminio antracita. Quitar el andamio del primer plano y la valla de obra; cielo despejado de tarde.`
- `Esta foto: interior del taller fabricando ventanas de PVC blancas. Solo luz y nitidez; no ordenar ni quitar nada del taller.`
- `Esta foto: barandilla de forja en escalera. Corregir la perspectiva y el balance de blancos.`

## Control de calidad (antes de publicar)

1. Guardar el original y la versión de Flow **juntos**, con el mismo nombre:
   - `IMG_1234.jpg` → original
   - `IMG_1234.flow.jpg` → versión de Flow
2. Compararlas lado a lado al 100 % de zoom, mirando el producto: color del perfil, hojas, manillas, junquillos, soldaduras.
3. Si algo del producto ha cambiado, **se descarta** y se repite con una línea «Esta foto» más restrictiva.
4. Mantener el mismo «look» en toda la galería: misma temperatura de color y mismo contraste. Conviene procesar cada obra en una sola tanda.
5. Las fotos de casas de clientes solo se publican con su consentimiento.
