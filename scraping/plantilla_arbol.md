# Árbol de productos por proveedor — MetalHervas

> Generado el 2 de octubre de 2026 a partir de las webs oficiales de cada proveedor (rastreo con Crawl4AI).
> Alcance según la nota del tío (`Proveedores/Proveedores.jpeg`). Las series con **★** son las que MetalHervas trabaja expresamente; en Aluval, Extrugasa y Saint-Gobain/Climalit la nota dice «todos los modelos».
> El texto de cada página está guardado en `Proveedores/raw/<proveedor>/`. Para regenerar: `scraping/crawl.py` → `fetch_climalit_archive.py` → `extract_*.py` → `download_pdfs.py` → `build_tree.py`.

## Dónde está todo

| Qué | Dónde |
|---|---|
| Este documento (árbol, fichas, enlaces) | `Proveedores/arbol_productos.md` |
| Diagrama | `Proveedores/diagrama_proveedores.drawio.png` |
| **PDFs descargados** (fichas técnicas, catálogos, guías, EPD…) | `Proveedores/pdfs/<proveedor>/<familia>/` |
| Índice de PDFs: proveedor, familia, producto, tipo, archivo local, URL original | `Proveedores/pdfs/pdfs.csv` (se abre con Excel) |
| **Datos estructurados para la web** | `Proveedores/raw/aluval.json`, `extrugasa.json`, `gealan.json`, `saint-gobain.json` |
| Texto completo de cada página web | `Proveedores/raw/<proveedor>/*.md` (con su URL en la cabecera) |
| HTML original de climalit.es (copias de Internet Archive) | `Proveedores/raw/climalit/_html/` |

{{RESUMEN_PDFS}}

> **Sobre los que faltan:** los dos de Gealan dan error 404 en la propia web de Gealan. Los de climalit.es se piden a Internet Archive: dos no están archivados (404) y dos los frena su límite de peticiones (429). El folleto de Climalit y el manual REcircula sí están descargados, porque Saint-Gobain publica los mismos documentos (`pdfs/saint-gobain/soluciones/Folleto Climalit.pdf` y `pdfs/saint-gobain/general/Manual REcircula 2025.pdf`). Para reintentar más adelante basta con volver a ejecutar `scraping/download_pdfs.py`, que solo baja lo que falte.

## Vista general

```
MetalHervas
├── VENTANAS PVC
│   └── GEALAN (marca de perfiles de PVC, grupo VEKA)
│       ├── ★ S 8000 (S 8000 IQ) ······ 74 mm · ventanas y puertas
│       ├── ★ S 9000 (S 9000 IQ) ······ 82,5 mm · ventanas, puertas, elevadora
│       │   └── variantes: GEALAN-FUTURA®, GEALAN-LUMAXX®
│       ├── ★ GEALAN-LINEAR® ·········· 74 mm · ventanas, puertas, correderas
│       │   └── ★ LINEAR acrylcolor® · variantes: LUMAXX®, hoja enrasada, marco empotrado
│       ├── ★ Gama de colores
│       │   ├── GEALAN-acrylcolor® (estándar · ampliada · bajo pedido · metálicos · base oscura)
│       │   ├── Láminas decorativas (estándar · madera · RealWood · lisas · mate · metálicas)
│       │   └── Revestimiento de aluminio (carcasas, todos los RAL)
│       ├── Otros sistemas: GEALAN-KONTUR®, GEALAN-KUBUS®, SMOOVE multislide, Corredera 74 mm, SMOOVIO®
│       └── Complementos: umbrales, ventilación GEALAN-CAIRE®, windowfit, Hafen-City-Fenster®, STV®, IKD®, BALANCE
│
├── VENTANAS ALUMINIO
│   ├── ALUVAL (sistemas ALUPROM, Picanya, Valencia)
{{ARBOL_ALUVAL}}
│   │   └── Acabados y colores (lacados estándar, texturados, efecto madera)
│   │
│   └── EXTRUGASA (sistemas de edificación)
{{ARBOL_EXTRUGASA}}
│
└── ACRISTALAMIENTO
    └── SAINT-GOBAIN GLASS · marca CLIMALIT®
        ├── Gamas de climalit.es: Climalit Basic® · Climalit Plus® · Climalit ORAÉ®
        ├── CLIMALIT® / CLIMALIT PLUS® (doble y triple acristalamiento para ventana)
        │   ├── Baja emisividad: PLANITHERM® XN, ECLAZ®
        │   └── Control solar + baja emisividad: PLANITHERM® 4S, PLANISTAR® ONE, COOL-LITE® XTREME 61/29
        ├── CLIMALIT ORAÉ® (baja huella de carbono): PLANISTAR® ONE ORAÉ®, ECLAZ® ZEN ORAÉ®, COOL-LITE® XTREME ORAÉ®
        ├── Muro cortina / no residencial: COOL-LITE® SKN, COOL-LITE® XTREME, COOL-LITE® ST/STB, COOL-LITE® K
        ├── Seguridad y acústica: STADIP®, STADIP® PROTECT, STADIP® SILENCE
        ├── Vidrios especiales: PRIVA-LITE®, SageGlass®, VISION-LITE®, 4BIRD®
        └── Interiorismo: DECORGLASS®/MASTERGLASS®, MASTER-SOFT®, PLANILAQUE® EVOLUTION, MIRALITE® PURE, MIRASTAR®
```

---

## 1. Ventanas de PVC — GEALAN

Web: <https://www.gealan.de/es> · Marca alemana de perfiles de PVC (grupo VEKA).

> **Sobre los nombres «S 8000 IQ» y «S 9000 IQ»:** la web actual los llama simplemente **S 8000** y **S 9000**. La antigua dirección `/sistemas/s-8000-iq` todavía existe, pero da error. Son las mismas plataformas.

### ★ S 8000 (S 8000 IQ)

Sistema económico y optimizado en material para ventanas y puertas. [Web](https://www.gealan.de/es/sistemas/s-8000)

| Dato | Valor |
|---|---|
| Profundidad | 74 mm · versiones de 5 cámaras (más estabilidad) o 6 cámaras (más aislamiento) |
| Solape | Marco 18/20 mm · Hoja 18/20 mm |
| Vidrio máximo | 48 mm con junta · 50 mm con pegado STV® |
| Uf | hasta 1,2 W/m²K |
| Tipos | Ventanas · Puertas de entrada |
| Ensayos | Agua 9A · Aire clase 4 · Viento C5/B5 · Impacto clase 4 · Acústica 34–47 dB |
| Acabados | Blanco · láminas decorativas · BALANCE (núcleo reciclado) · también versión de base oscura con acrylcolor |

### ★ S 9000 (S 9000 IQ)

Sistema combinado para ventanas, puertas de entrada y elevadoras correderas. Su rasgo estético es la inclinación de 15°. [Web](https://www.gealan.de/es/sistemas/s-9000)

| Dato | Valor |
|---|---|
| Profundidad | 82,5 mm |
| Solape | Marco 26 mm · Hoja 18 mm + 26 mm |
| Vidrio máximo | 56 mm con sellado · 58 mm con STV® |
| Uf | hasta 0,89 W/m²K |
| Tipos | Ventanas · Puertas de entrada (clásica y con hoja superpuesta) · Elevadora corredera |
| Ensayos | Agua 9A · Aire clase 4 · Viento C5/B5 · Impacto clase 2 · Acústica 34–45 dB |
| Acabados | Blanco · GEALAN-acrylcolor® · láminas decorativas · carcasas de aluminio · BALANCE |

- **GEALAN-FUTURA®**: combinación de perfiles del S 9000 apta para casa pasiva (ift WA-15/2) con perfiles y refuerzos de acero estándar. Uf 0,89 W/m²K y disponible en color.
- **GEALAN-LUMAXX®**: variante de perfil estrecho con más superficie de vidrio y monostulp simétrico apoyado.
- Umbral **GEALAN-COMFORT®**: umbral cero, a ras de suelo, para todos los marcos del S 9000.

### ★ GEALAN-LINEAR®

El sistema más versátil de Gealan, de diseño recto, para ventanas, puertas de entrada y correderas. [Web](https://www.gealan.de/es/sistemas/gealan-linear) · El folleto en PDF que enlaza la web da error 404 a fecha de hoy.

| Dato | Valor |
|---|---|
| Profundidad | 74 mm |
| Solape | Marco 26 mm · Hoja 18 mm |
| Vidrio máximo | 48 mm con junta · 50 mm con STV® |
| Uf | hasta 1,0 W/m²K |
| Tipos | Ventanas · Puertas de entrada · Soluciones correderas |
| Ensayos | Agua 9A · Aire clase 4 · Viento C5/B5 · Impacto clase 3 · Acústica 34–47 dB |
| Acabados | Blanco · **GEALAN-acrylcolor®** · láminas decorativas · revestimiento de aluminio · BALANCE |

- **★ LINEAR con acrylcolor®**: la superficie de color premium aplicada al Linear. Las paletas de acrylcolor® cambian según el sistema; la del Linear está en el [resumen de colores acrylcolor® (PDF)](https://www.gealan.de/getContentAsset/56a73eb0-8bde-4a27-82b0-ab48dab152dd/dfc3d011-8f63-43f6-9ed8-4b444333a1d0/GEALAN-acrylcolor-Lieferklassen-Ansicht.pdf?language=en).
- **GEALAN-LUMAXX®**: vistas más estrechas, con monodeslizante de solo 100 mm de anchura.
- **Hoja enrasada** y **marco empotrado**: marco y hoja quedan en el mismo plano y solo se ve una junta fina.

### ★ Gama de colores Gealan

**GEALAN-acrylcolor®**: capa de PMMA (vidrio acrílico) coextruida sobre el PVC. No se pela, resiste arañazos y no pierde color con la luz. Acabado mate sedoso cepillado. [Web](https://www.gealan.de/es/innovaciones/gealan-acrylcolor) · Disponible en KUBUS, LINEAR, KONTUR y S 9000. El folleto «Warum GEALAN-acrylcolor» que enlaza la web también da error 404.

- **Paleta estándar**: RAL 7015 gris pizarra · RAL 7016 gris antracita · RAL 7022 gris umbra · RAL 7039 gris cuarzo · RAL 7040 gris ventana · RAL 8014 marrón sepia · RAL 9005 negro profundo · DB 703 · Plata (similar a RAL 9007)
- **Paleta ampliada**: RAL 8022 pardo negruzco · RAL 9006 aluminio blanco · Bronce · RAL 1019 beige agrisado · RAL 1035 beige perlado · RAL 7006 gris beige · RAL 7021 gris negruzco · RAL 7038 gris ágata · RAL 9016 blanco tráfico
- **Bajo pedido (proyectos)**: RAL 8023, 9001, 9002, 9010, Oro, 8000, 8001, 8003, 8011, 8012, 8017, 7032, 7033, 7035, 7036, 7037, 7043, 7012, 7013, 7023, 7024, 7030, 7031, 7000, 7001, 7003, 7004, 7010, 7011, 5011, 5014, 6005, 6009, 6015, 6021, 1015, 3004, 3011, 5002, 5005, 5007, 1001, 1013, 1014
- **Metálicos** (exclusivos de Gealan): Bronce · Oro · Beige perla RAL 1035 · Aluminio blanco RAL 9006 · Plata (≈ RAL 9007) · Mica de hierro DB 703. [Web](https://www.gealan.de/es/gealan-acrylcolor-metallic)
- **Base oscura** (perfil gris oscuro en todo el contorno, en todos los sistemas): exterior acrylcolor RAL 7016, RAL 9005 o DB 703; interior con 6 láminas a juego (antracita liso, mate, graneado y RealWood, Negro Ulti-Matt, Alux DB703). [Web](https://www.gealan.de/es/gealan-acrylcolor-base-oscura)

**Láminas decorativas**: válidas por dentro y por fuera, en todos los sistemas. La disponibilidad depende del sistema y del distribuidor. [Web](https://www.gealan.de/es/superficies/produktdetail-seite-dekorfolien)

- **Estándar y Standard plus**: Roble dorado · Nogal · Caoba · RAL 7001 gris plata · RAL 7039 gris cuarzo · RAL 7012 gris basalto · RAL 7016 liso gris antracita · Marrón chocolate
- **Madera** (fuera de estándar): Roble Sheffield claro · AnTEAK · Oregón · Abeto Douglas veteado · Nuez · Meranti · Roble rústico · Roble oscuro · Roble negro · Roble claro · Pino negro · Winchester XA
- **RealWood** (veta en relieve): Woodec Sheffield Oak concrete · Weissbach Oak · Woodec Turner Oak toffee · Woodec Turner Oak malt · Ginger Oak · Honey Oak · RealWood RAL 9010 · RealWood RAL 7016
- **Lisas de grano**: RAL 9003 blanco brillante · RAL 9010 blanco puro · RAL 9001 blanco crema · RAL 7035 gris luminoso · RAL 7023 gris hormigón · RAL 5011 azul acero · RAL 8022 pardo negruzco · RAL 3011 rojo pardo · RAL 3005 rojo vino · RAL 6005 verde musgo · RAL 6009 verde abeto · Verde monumento
- **Lisas / mate**: RAL 7012 gris basalto liso · RAL 7016 antracita mate · RAL 7021 gris negro liso · RAL 9010 blanco puro mate · RAL 9001 blanco crema mate · RAL 7039 Smooth Quartz Grey · RAL 7022 gris umbra mate
- **Efecto metálico**: DB 703 · Bronce · Cepillado metálico latón · Cepillado metálico plata

**Revestimiento de aluminio**: carcasas exteriores de aluminio, disponibles en todos los sistemas y en cualquier color RAL.

### Otros sistemas Gealan (no figuran en la nota)

| Sistema | Profundidad | Uf | Uso | Web |
|---|---|---|---|---|
| GEALAN-KONTUR® | 82,5 mm | hasta 0,97 | Premium, con opción de aluminio y fabricación automatizable; acústica 36–49 dB | [Web](https://www.gealan.de/es/sistemas/gealan-kontur) |
| GEALAN-KUBUS® | 82,5 mm | hasta 0,88 | Ventana de diseño, casi todo vidrio y apta para casa pasiva; hojas de hasta 2,50 m | [Web](https://www.gealan.de/es/sistemas/gealan-kubus) |
| GEALAN-SMOOVE multislide | 74 mm | — | Correderas de 2 o 3 carriles, umbral de 20/27,5 mm, monostulp de 47 mm | [Web](https://www.gealan.de/es/sistemas/gealan-smoove-multislide) |
| Corredera 74 mm | 74 / hoja 48 mm | 2,1–2,3 | Corredera hasta 6000 × 2500 mm (3 carriles), hojas de hasta 120 kg | [Web](https://www.gealan.de/es/productos/sistemas/sistema-deslizante-74mm-alt) |
| GEALAN-SMOOVIO® | — | — | Corredera de alta estanqueidad que ocupa poco espacio | [Web](https://www.gealan.de/es/sistemas/gealan-smoovio) |

### Complementos y tecnologías Gealan

- **Umbrales**: [umbral estándar](https://www.gealan.de/es/productos/soluciones/barreras-sin-umbral) de 20 mm para todos los sistemas de 74 y 82,5 mm · [GEALAN-COMFORT®](https://www.gealan.de/es/productos/gealan-comfort), umbral cero para el S 9000.
- **Ventilación**: [GEALAN-CAIRE® flex](https://www.gealan.de/es/sistemas-de-ventilacion), aireador pasivo en el galce que sirve para cualquier ventana de PVC. Variantes CAIRE® smart y CAIRE® aereco.
- **[GEALAN-windowfit](https://www.gealan.de/es/productos/window-and-door-technology/gealan-windowfit)**: perfiles de conexión y accesorios de montaje (Blaugelb).
- **[Hafen-City-Fenster®](https://www.gealan.de/es/productos/gealan-hafen-city)**: ventana de alto aislamiento acústico, hasta 63 dB.
- **Tecnologías**: [STV®](https://www.gealan.de/es/innovaciones/estatica-stv), acristalamiento pegado en seco para elementos grandes · [IKD®](https://www.gealan.de/es/innovaciones/aislamiento-termico-ikd), espuma aislante dentro de las cámaras · **BALANCE**, perfil con núcleo reciclado.
- **Documentación técnica** (fichas, textos de licitación, perfiles): en el área privada **myGEALAN**, que requiere acceso.

---

## 2. Ventanas de aluminio — ALUVAL

Web: <https://aluval.es> · [Catálogo general (PDF)](https://aluval.es/files/pdf/category/catalogo-general.pdf) · Todas las series de la web.

> Las fichas de *Guías y lamas de seguridad*, varias *Mosquiteras* y *Sistemas tradicionales* no tienen texto en la web: su información está solo en los PDFs enlazados.

{{ALUVAL}}
### Acabados y colores Aluval

[Web](https://aluval.es/acabados-y-colores) · Lacado para arquitectura, licencia nº 482.

- **Lacados estándar**: 1013 blanco perla · 1015 marfil claro · 3005 rojo vino · 5010 azul genciana · 5013 azul cobalto · 6005 verde musgo · 6009 verde abeto · 7011 gris hierro · 7012 gris basalto · 7016 gris antracita · 7022 gris sombra · 7035 gris luminoso · 8007 pardo corzo · 8014 sepia · 8017 chocolate · 9010 blanco puro · 9011 negro grafito
- **Lacados texturados**: 7016 · 6009 · 8019 · 9016 · 7033 texturados · Noir 200
- **Efecto madera**: Pino 202 · Pino · Roble 202 · Roble · Acacia 202 · Acacia · Raíz · Nogal · Castaño · Teka liso · Golden dorado · Golden dorado oscuro · Nogal texturado oscuro · Roble golden texturado · Nogal siena · Teka texturado · Embero claro · Embero oscuro · Embero · Embero 639 · Cerezo · Cerezo texturado · Pino texturado · Pino envejecido texturado · Nogal andaluz · Siena texturizado 2

---

## 3. Ventanas de aluminio — EXTRUGASA

Web: <https://www.extrugasa.com/edificacion> · Todas las series de la web (área de Edificación).

> La web pone algunos productos en varias categorías; aquí aparecen en todas ellas. Las series XP que la web solo muestra en la 2.ª página de *practicables* se han añadido a esa categoría. Los manuales, BIM, CAD y ensayos completos están en la intranet de Extrugasa.

{{EXTRUGASA}}
---

## 4. Acristalamiento — SAINT-GOBAIN GLASS · CLIMALIT®

Web: <https://www.saint-gobain-glass.es/es> · CLIMALIT® es la marca de doble y triple acristalamiento aislante de Saint-Gobain, fabricada por la red **CLIMALIT Partners**.

> `climalit.es` tiene una protección antibots (Cloudflare) que no se ha intentado eludir. Su contenido se ha recuperado de las **copias públicas de Internet Archive** (marzo–junio de 2026); el resto sale de saint-gobain-glass.es, donde está la misma gama.

### Lo que explica climalit.es (copia de Internet Archive, mayo 2026)

Climalit® es la marca de doble y triple acristalamiento. La web la divide en **tres gamas**:

- **Climalit Basic®**: las soluciones más sencillas, sin vidrio de capa.
- **Climalit Plus®**: integra un vidrio con capa que añade aislamiento térmico y/o control solar; responde al Código Técnico de la Edificación.
- **Climalit ORAÉ®**: la misma eficiencia con baja huella de carbono, gracias al vidrio ORAÉ®.

Los productos que presenta para ventana de vivienda son estos. [Productos (copia)](https://web.archive.org/web/20260516000000/https://climalit.es/productos/)

| Beneficio | Producto | Para qué | Combinación recomendada |
|---|---|---|---|
| Aislamiento térmico | PLANITHERM® 4S (cara 2) | Aislamiento y control solar; climas cálidos, todo el año | STADIP / STADIP SILENCE PLANITHERM 4S |
| Aislamiento térmico | PLANITHERM® XN (cara 3) | Aísla hasta 3 veces más; climas fríos, ahorro en calefacción | STADIP / STADIP SILENCE PLANITHERM XN |
| Luz sin calor | PLANISTAR® ONE (cara 2) | Aislamiento reforzado, control solar y mucha luz; zonas soleadas | STADIP / STADIP SILENCE PLANISTAR ONE |
| Luz sin calor | COOL-LITE XTREME® 61/29 (cara 2) | Control solar extremo, aspecto neutro y baja reflexión | STADIP SILENCE COOL-LITE XTREME 61/29 |
| Silencio | STADIP SILENCE® | Aislamiento acústico (PVB Silence) y seguridad | — |
| Seguridad | STADIP PROTECT® | Doble acristalamiento laminado anti-impactos | — |

Todas las soluciones Climalit Plus® y Climalit ORAÉ® contribuyen además al **ahorro** en las facturas.

{{CLIMALIT_PAGINAS}}

### CLIMALIT® y CLIMALIT PLUS® — acristalamiento para ventana

CLIMALIT PLUS® lleva un vidrio de capa que aísla hasta 3 veces más que un doble acristalamiento básico. [Web](https://www.saint-gobain-glass.es/es/climalit-la-solucion-para-tus-ventanas)

| Vidrio de capa | Función | Datos clave (doble acristalamiento) | Orientación recomendada | Web / PDF |
|---|---|---|---|---|
| PLANITHERM® XN | Baja emisividad | TL 81 % · Ug 1,1 W/m²K (argón) | Norte / baja radiación solar | [Web](https://www.saint-gobain-glass.es/es/productos/planitherm-xn) · [PDF](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-planitherm-xn.pdf) |
| ECLAZ® | Baja emisividad, muy transparente | TL 83 % · g 0,71 · Ug 1,1 (triple: Ug 0,6) | Máxima luz natural | [Web](https://www.saint-gobain-glass.es/es/productos/eclazr) |
| PLANITHERM® 4S | Control solar + baja emisividad | g 0,42 · Ug 1,0 | Sur, este, oeste | [Web](https://www.saint-gobain-glass.es/es/productos/planitherm-4s) · [PDF](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-planitherm-4s.pdf) |
| PLANISTAR® ONE | Control solar + baja emisividad, alta selectividad | g 0,38 · Ug 1,0 | Sur, este, oeste (radiación directa) | [Web](https://www.saint-gobain-glass.es/es/productos/planistar-one) · [PDF](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-planistar-one.pdf) |
| COOL-LITE® XTREME 61/29 (II) | Extrema selectividad | TL 61 % · g 0,29 | Grandes superficies acristaladas | [Web](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-6129-y-cool-lite-xtreme-6129-ll) |

### CLIMALIT ORAÉ® — baja huella de carbono

Doble y triple acristalamiento hecho sobre vidrio ORAÉ®, con un 35–40 % menos de huella de carbono. Lleva intercalario warm-edge y argón. [Web](https://www.saint-gobain-glass.es/es/productos/climalit-orae) · [Catálogo PDF](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/climalit-orae-2025-1.pdf)

- [PLANISTAR® ONE ORAÉ®](https://www.saint-gobain-glass.es/es/productos/planistar-one-orae): control solar + baja emisividad
- [ECLAZ® ZEN ORAÉ®](https://www.saint-gobain-glass.es/es/productos/eclaz-zen-orae): baja emisividad, Ug 1,0 en doble y 0,5 en triple, TL cercana al 80 %
- [COOL-LITE® XTREME ORAÉ®](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-orae) · [COOL-LITE® SKN ORAÉ®](https://www.saint-gobain-glass.es/es/productos/cool-liter-skn-oraer)

### Control solar para muro cortina y obra no residencial

- **[COOL-LITE® SKN](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn)**: [SKN 144 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-144-ll) · [SKN 155 / 155 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-155-cool-lite-skn-155-II) · [SKN 165 / 165 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-165-y-cool-lite-skn-165-II) · [SKN 176 / 176 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-176-y-cool-lite-skn-176-II) · [SKN 183 / 183 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-183-y-cool-lite-skn-183-II)
- **[COOL-LITE® XTREME](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme)** (extrema selectividad, estética neutra): [51/23 & 51/23 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-51/23%20%26%2051/23-ll) · [61/29 & 61/29 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-6129-y-cool-lite-xtreme-6129-ll) · [70/33 & 70/33 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-7033-y-7033-ll)
- **[COOL-LITE® ST / STB](https://www.saint-gobain-glass.es/es/productos/cool-lite-st-y-cool-lite-stb)** · **[COOL-LITE® K](https://www.saint-gobain-glass.es/es/productos/cool-liter-k)**: control solar selectivo y baja emisividad

### Seguridad y acústica

- **[STADIP® / STADIP® PROTECT / STADIP® SILENCE](https://www.saint-gobain-glass.es/es/productos/stadip-stadip-silence)**: vidrio laminado de seguridad. SILENCE usa PVB acústico (más aislamiento al ruido con la misma seguridad). [PDF](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-stadip-silence.pdf)

### Vidrios especiales

- [PRIVA-LITE®](https://www.saint-gobain-glass.es/es/productos/priva-liter): pasa de translúcido a transparente con corriente eléctrica
- [SageGlass®](https://www.saint-gobain-glass.es/es/productos/sageglassr): vidrio electrocrómico inteligente
- [VISION-LITE®](https://www.saint-gobain-glass.es/es/productos/vision-liter): antirreflejo
- [4BIRD®](https://www.saint-gobain-glass.es/es/productos/4birdr): evita choques de aves, combinado con COOL-LITE®

### Interiorismo y decoración

- [DECORGLASS® y MASTERGLASS®](https://www.saint-gobain-glass.es/es/productos/decorglass-y-masterglass) · [MASTER-SOFT®](https://www.saint-gobain-glass.es/es/productos/master-soft): vidrios impresos
- [PLANILAQUE® EVOLUTION](https://www.saint-gobain-glass.es/es/productos/planilaquer-evolution): vidrio lacado blanco o negro
- [MIRALITE® PURE](https://www.saint-gobain-glass.es/es/productos/miralite-pure) · [MIRASTAR®](https://www.saint-gobain-glass.es/es/productos/mirastar): espejos

### Servicios

- [CLIMALIT® Recicla](https://www.saint-gobain-glass.es/es/servicio-de-reciclaje-climalit-recicla): recogida y reciclaje de vidrio

### Documentación de cada producto Saint-Gobain

Todos los PDFs enlazados en la web de Saint-Gobain Glass. La columna «Local» abre la copia descargada.

{{DOCS_SG}}
