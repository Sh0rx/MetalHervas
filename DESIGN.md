# DESIGN.md — Metal Hervás

> Copia local del Design System publicado en Claude Design: https://claude.ai/artifact/3DZaLvDXRyQ3gG47BAbq5f
> Tokens en `design-system/tokens.json`; estilos de componentes en `design-system/components/bundle.css`; logos en `prototipos/assets/logo/`.
> Si cambia algo, se cambia primero en el Design System publicado y después se copia aquí.

Metal Hervás S.L. es una empresa familiar de Hervás (Cáceres), en el Valle del Ambroz. Hace carpintería de hierro, aluminio y PVC, y estructuras metálicas. Fabrica sus propias ventanas de PVC en su taller. La web tiene una sola misión: que el cliente vea trabajo real bien hecho y llame.

## Contenido y tono

- Habla como alguien del oficio que sabe lo que hace: frases cortas y concretas, en español de España y tuteando al cliente. «Medimos, fabricamos en nuestro taller y montamos.»
- Nombra el producto con su nombre real: «GEALAN S 9000», «ALUPROM 44», «Climalit Plus». Las cifras van con su unidad real: `82,5 mm`, `Uf ≤ 0,89 W/(m²K)`, `34–45 dB`. Nunca se redondea ni se adorna un dato técnico.
- Nada de superlativos vacíos («líderes», «la mejor calidad»), ni signos de exclamación, ni emoji.
- Mayúsculas solo en `label` (antetítulos y chips). Los titulares van en mayúscula inicial: «Fabricamos tus ventanas».
- Los botones empiezan por un verbo: «Pedir presupuesto», «Llamar al 664 40 96 18», «Ver la serie».
- Nunca se inventan datos de la empresa (años, número de obras, pueblos). Si no están confirmados, no se escriben.

## Color

- La marca vive en tres verdes y un acero. `verde` es el verde de «HERVÁS» en el logo; `verde-oscuro`, `verde-medio` y `menta` son la barra y los cuadros del icono «VENTANAS de PVC»; `acero` y `viga` son la estructura de vigas del logo.
- Fondos: `surface` para la página, `surface-raised` para tarjetas y `surface-sunken` para bandas alternas. El texto va en `ink`, y el secundario en `ink-muted`.
- `verde` sobre fondo claro no llega a contraste AA para texto (2,9:1). Úsalo en bloques de color, iconos grandes y titulares de 24px o más sobre fondo oscuro. Los enlaces y el texto verde van en `verde-texto`.
- Botón principal: fondo `accion` con texto `on-accion`. Sobre un relleno verde nunca se escribe en blanco a mano; se usa siempre `on-accion`.
- Los tokens `dir-*` son las paletas secundarias de las cinco direcciones que se están probando para la página inicial (Acero, Luz y vidrio, Oficio, Blueprint y De aquí). El núcleo verde y el logo se mantienen iguales en todas. Cuando se elija la dirección, los `dir-*` que no se usen se retirarán.

## Tipografía

- Titulares en `display` (Archivo, peso 800, ancho expandido). Recuerda a las letras anchas de «HERVÁS» sin imitar el logo. Estilos: `display-xl` para el hero, `display` para secciones y `heading` para tarjetas.
- El texto corrido va en `sans` (IBM Plex Sans): `lead` para entradillas, `body` para el resto (máximo 65 caracteres por línea) y `label` para antetítulos en mayúsculas.
- Los datos técnicos van en `mono` (IBM Plex Mono): `dato` para la cifra destacada de una ficha y `dato-sm` para las filas de una tabla técnica. Activa siempre `font-variant-numeric: tabular-nums`.
- Las tres familias se cargan desde Google Fonts. Archivo se carga con su eje `wdth`.

## Forma, espacio y movimiento

- Los cantos son rectos, como un perfil. Fotos y bloques llevan `radius-none`; botones, campos y tarjetas, `radius-sm`. `radius-pill` solo se usa en los chips de material y en el botón flotante de WhatsApp.
- Las tarjetas se separan con un borde `line`, no con sombra. `shadow-float` existe solo para la barra de contacto fija en el móvil.
- Espaciado de 4 en 4: `space-6` dentro de las tarjetas, `space-8` entre tarjetas y `space-24` entre secciones (64px en móvil). El margen lateral mínimo es `space-4`.
- Foco del teclado: anillo sólido de 2px en `focus` con 2px de separación.
- El movimiento es una mejora progresiva: todo debe leerse con `prefers-reduced-motion` activado y sin WebGL. Cada página tiene un único momento protagonista, como la viga del logo ensamblándose o una ventana que se abre; el resto se mueve poco.

## Imagen

- Solo obras y taller reales de Metal Hervás. Las fotos se mejoran con Google Flow siguiendo `docs/google-flow-prompt.md` del repositorio: se puede corregir la luz, enderezar y limpiar la obra, pero el producto no se toca (ni color, ni número de hojas, ni herrajes, ni apertura).
- Los modelos 3D de productos se construyen con las medidas reales: perfiles IPE normalizados y cortes de sección de las fichas de cada proveedor.
- Las fotos de casas de clientes solo se publican con su permiso, y sin matrículas ni números de calle.

## Logo

- `assets/Logos/logo-color.svg` sobre fondos claros y `logo-negativo.svg` sobre fondos oscuros. `logo-blanco.svg` y `logo-mono.svg` son para fotos y para impresión a una tinta. La submarca «VENTANAS de PVC» va siempre aparte, debajo o en el pie, nunca pegada al logo.
- El logo no se redibuja, no se estira y no se recolorea fuera de estas cuatro variantes. Hay que dejar alrededor un espacio libre igual a la altura de la «H» de «HERVÁS».

## Iconos

- Iconos de trazo de 1,5px y esquinas rectas: [Lucide](https://lucide.dev) (licencia ISC), en `ink` o `verde-texto`. No se usan emoji ni iconos rellenos de colores.

## Contacto

- Ctra. de las Cañadas, s/n · 10700 Hervás (Cáceres) · Tel. 927 47 36 19 · Móvil 664 40 96 18 · metalhervas@gmail.com
