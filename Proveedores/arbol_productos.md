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

**PDFs descargados**

| Proveedor | PDFs distintos | Descargados | Tamaño | Sin descargar |
|---|---|---|---|---|
| aluval | 103 | 103 | 744 MB | — |
| extrugasa | 56 | 56 | 31 MB | — |
| gealan | 3 | 1 | 1 MB | [Warum-GEALAN-acrylcolor_GB_small.pdf](https://www.gealan.de/getContentAsset/b2d0eb50-7de8-4a36-9b5d-bdd814654202/3300e2ea-3bab-45bc-a62a-dc94db8eac24/Warum-GEALAN-acrylcolor_GB_small.pdf?language=en) (error 404)<br>[GEALAN-LINEAR-B2C-E.pdf](https://www.gealan.de/getContentAsset/e93e268f-4920-420a-a440-07ed3c491cf0/3300e2ea-3bab-45bc-a62a-dc94db8eac24/GEALAN-LINEAR-B2C-E.pdf?language=es) (error 404) |
| saint-gobain | 39 | 39 | 120 MB | — |
| climalit | 5 | 1 | 1 MB | [folleto-climalit-2022.pdf](https://climalit.es/wp-content/uploads/2022/11/folleto-climalit-2022.pdf) (error (<HTTPError 429: 'Too Many Requests'>))<br>[manual-recircula-2025.pdf](https://climalit.es/wp-content/uploads/2025/11/manual-recircula-2025.pdf) (error 404)<br>[sg-triptico-climalit-plus-2021-oct21.pdf](https://climalit.es/wp-content/uploads/2021/12/sg-triptico-climalit-plus-2021-oct21.pdf) (error (<HTTPError 429: 'Too Many Requests'>))<br>[triptico-climalit-ecologico-act.pdf](https://climalit.es/wp-content/uploads/2023/06/triptico-climalit-ecologico-act.pdf) (error 404) |

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
│   │   ├── Series Practicables (3)
│   │   │   └── ALUPROM 22, ALUPROM 28, SERIE 40x20
│   │   ├── Series Correderas – Elevables (7)
│   │   │   └── ALUPROM 14, ALUPROM 15, ALUPROM 18, ALUPROM 21, ALUPROM 24, ALUPROM 30, ALUPROM 40
│   │   ├── Series Practicables RPT Canal Europeo (8)
│   │   │   └── ALUPROM 25, ALUPROM 34 HO, ALUPROM 35 HO, ALUPROM 36, ALUPROM 38, ALUPROM 43, ALUPROM 44, ALUPROM 46
│   │   ├── Series Practicables RPT Canal 16 (7)
│   │   │   └── ALUPROM 25 C16, ALUPROM 34 HO C16, ALUPROM 35 HO C16, ALUPROM 36 C16, ALUPROM 38 C16, ALUPROM 44 C16, ALUPROM 46 C16
│   │   ├── Series Correderas - Elevables RPT (5)
│   │   │   └── ALUPROM 17, ALUPROM 20, ALUPROM 31, ALUPROM 41, ALUPROM 42
│   │   ├── Fachadas Ligeras (1)
│   │   │   └── ALUPROM 54
│   │   ├── Series Mallorquinas (3)
│   │   │   └── SISTEMAS ALUVAL, MALLORQUINA 4020, MALLORQUINA ESTÁNDAR
│   │   ├── Sistemas de Barandillas (4)
│   │   │   └── BARANDILLA TRADICIONAL, ALUPROM 50, CLASS VISION, CLASS JULIET
│   │   ├── Protección solar y cerramientos exteriores (5)
│   │   │   └── JALOUSIE, TECHO MÓVIL, CELOSÍAS FIJAS CLIPADAS, CELOSÍAS, DIVISORIA Y 100
│   │   ├── Guías y Lamas de seguridad (11)
│   │   │   └── PS-30, PS-78, ECO-100, ECO-80, GUÍAS, PS-4, LAMAS, PS-15, PS-40, PS-10, PS-100
│   │   ├── Mosquiteras (10)
│   │   │   └── Aludark R33, Aludark P42, Aludark R42, Mosquiclass, Corredera Curva, Corredera Recta, Mosquitera fija, R33, R42, P42
│   │   ├── Sistemas Tradicionales (6)
│   │   │   └── VITRINA, FORROS, PREMARCOS OBRA, MÁMPARA OFICINA, LUMINOSOS, NORMALIZADOS
│   │   └── Acabados y colores (lacados estándar, texturados, efecto madera)
│   │
│   └── EXTRUGASA (sistemas de edificación)
│       ├── Cerramiento exterior (3)
│       │   └── XM-40, Celosías y lamas de ventilación, Cerrajería
│       ├── Control solar (4)
│       │   └── Lama ala de avión, Lama en “C”, Lama rectangular, XM-40
│       ├── Fachada ventilada (3)
│       │   └── TS-200, TS-300, TS-700
│       ├── Interiorismo (2)
│       │   └── XM-40, Mamparas
│       ├── Muro cortina (5)
│       │   └── EXAP-50 SG, EXAP-50 TP, EXAP-50 TH TV, EXAP-50 FT, EXAP UNITIZED
│       ├── Perfiles normalizados (1)
│       │   └── Perfiles normalizados
│       ├── Perfiles complementarios (6)
│       │   └── Premarcos, Albardillas, Dinteles, Alargaderas, Guías, Tapajuntas
│       ├── Sistema de barandillas (3)
│       │   └── XR-Handrail, XR-Frame Glass, XR-Glass
│       ├── Sistema de puertas (4)
│       │   └── XP-80+ HI, V-8000 40, V-8000 45, XD-70
│       ├── Sistema de ventanas practicables (22)
│       │   └── XP-70+ HI, XP-70 Compaq+ HI, XP-70 HO+, XP-70 HO+ HI, XP-80 Compaq HI, XP-80 HI, XP-80 HO HI, XP-80+ HI, V-8000 40, V-8000 45, XP-50, XP-60, XP-60+, XP-60 HO, XP-70, XP-70+, XP-70 Compaq, XP-70 Compaq+, XP-70 Compaq HI, XP-70 HI, XP-70 HO, XP-70 HO HI
│       ├── Sistema de carpintería de ventanas y puertas (7)
│       │   └── XS-110, XS-150, XS-160 HI, XS-170, G-90, XD-70, Perimetral 70
│       ├── Sistemas de ventana corredera (8)
│       │   └── XS-60, XS-100, XS-110, XS-150, XS-160 HI, G-90, XS-170, Perimetral 70
│       ├── Acabados (6)
│       │   └── Anodizado natural, Efecto madera embero, Efecto madera nogal, Lacado Blanco, Aluminio lacado RAL, Lacado textura negro
│       └── Accesorios (5)
│           └── Manilla puerta practicable Essence door, Manilla Essence Square practicable, Manilla Essence Essence Round practicable, Manilla correderas Essence acodada, Manilla correderas Essence con escudo
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

### Series Practicables

Funcionalidad y elegancia en cada apertura. [Web](https://aluval.es/productos/series-practicables)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [ALUPROM 22](https://aluval.es/productos/series-practicables/aluprom-22) | Serie abatible de cámara europea · Marcos de 45mm y de 52mm de ancho · Acristalamiento: junquillos desde 9 hasta 38mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura oscilo paralela, Pivotante, Batiente, Proyectante, Plegable en 3, 4, 5, 6, 7 u 8 hojas | [Aluprom 22 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2022%20Catalogo.pdf) · [Catálogo Series Abatibles](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Abatibles.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas22(22).pdf) |
| [ALUPROM 28](https://aluval.es/productos/series-practicables/aluprom-28) | Serie abatible de cámara europea · Marcos de 40mm de ancho · Acristalamiento: junquillos de hueco desde 4 hasta 32,8mm | — | [Aluprom 28 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2028%20Catalogo.pdf) · [Catálogo Series Abatibles](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Abatibles.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas28(28).pdf) |
| [SERIE 40x20](https://aluval.es/productos/series-practicables/serie-40x20) | Serie abatible 4020, 4040 · Marcos de 40mm · Acristalamiento: junquillos de hueco 9mm, 16mm y 21mm | Fijo, Practicable, Practicable de apertura exterior, Batiente, Pivotante | [Aluprom 4020 Catalogo](https://aluval.es/files/pdf/category/Aluprom%204020%20Catalogo.pdf) · [Catálogo Series Abatibles](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Abatibles.pdf) |

### Series Correderas – Elevables

Diseño y amplitud en movimiento. Las series correderas y elevables de Aluval permiten abrir espacios con suavidad y ligereza, ofreciendo grandes superficies acristaladas sin renunciar al aislamiento ni a la seguridad. [Web](https://aluval.es/productos/series-correderas)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [ALUPROM 14](https://aluval.es/productos/series-correderas/aluprom-14) | Serie corredera de corte recto · Marco de 72mm con carril de rodadura ancho · Acristalamiento: hojas de hueco de 12mm y 21mm | Corredera 2, 3, 4y 6 hojas | [Aluprom 14 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2014%20Catalogo.pdf) · [Catálogo Series Correderas](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Correderas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2014(14).pdf) |
| [ALUPROM 15](https://aluval.es/productos/series-correderas/aluprom-15) | Serie corredera perimetral · Marcos de 60mm con carril de rodadura ancho · Acristalamiento: hojas de hueco de 10mm y 19mm | Corredera 2, 3, 4 y 6 hojas | [Aluprom 15 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2015%20Catalogo.pdf) · [Catálogo Series Correderas](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Correderas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2015(15).pdf) |
| [ALUPROM 18](https://aluval.es/productos/series-correderas/aluprom-18) | Serie corredera perimetral · Marcos de 53, 70 y 90mm. con carril de rodadura ancho · Acristalamiento: hojas de hueco de 10mm, 20mm y 24mm | Corredera 2, 3, 4 y 6 hojas | [Aluprom 18 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2018%20Catalogo.pdf) · [Catálogo Series Correderas](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Correderas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2018(18).pdf) |
| [ALUPROM 21](https://aluval.es/productos/series-correderas/aluprom-21) | Serie corredera de corte recto · Marcos de 60mm con carril de rodadura ancho · Acristalamiento: hojas de hueco de 10, 16 y 19mm | Corredera 2, 3, 4 y 6 hojas | [Aluprom 21 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2021%20Catalogo.pdf) · [Catálogo Series Correderas](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Correderas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2021(21).pdf) |
| [ALUPROM 24](https://aluval.es/productos/series-correderas/aluprom-24) | Serie corredera de corte recto · Marcos de 77mm con carril de rodadura ancho · Acristalamiento: hojas de hueco de 12, 19 y 24mm | Corredera 2, 3, 4 y 6 hojas | [Aluprom 24 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2024%20Catalogo.pdf) · [Catálogo Series Correderas](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Correderas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2024(24).pdf) |
| [ALUPROM 30](https://aluval.es/productos/series-correderas/aluprom-30) | Serie corredera elevable con marco de 80mm · Acristalamiento de hasta 33mm · Altura de hojas de 65mm y de 74mm para correderas elevables | Corredera elevable 1, 2, 3, 4 y 6 hojas, Corredera 1, 2, 3, 4 y 6 hojas | [Aluprom 30 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2030%20Catalogo.pdf) · [Catálogo Series Correderas](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Correderas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2030(30).pdf) |
| [ALUPROM 40](https://aluval.es/productos/series-correderas/aluprom-40) | Serie corredera elevable con marco perimetral a inglete o con corte recto y hojas perimetrales · Marcos de 100 mm. con carril de rodadura ancho · Acristalamiento junquillos desde 9,5 hasta 29,5mm | Corredera elevable 1, 2, 3, 4 y 6 hojas, Corredera 1, 2, 3, 4 y 6 hojas | [Aluprom 40 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2040%20Catalogo.pdf) · [Catálogo Series Correderas](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20Series%20Correderas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2040(40).pdf) |

### Series Practicables RPT Canal Europeo

Máxima eficiencia y diseño en cada detalle. [Web](https://aluval.es/productos/series-practicables-rpt-canal-europeo)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [ALUPROM 25](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-25) | Serie abatible rotura puente térmico de cámara europea · Marcos para puerta y ventana de 45mm · Acristalamiento: junquillos de hueco desde 9mm hasta 37,8mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilo-batiente, Apertura oscilo paralela, Batiente, Proyectante, Plegable en 3, 4, 5, 6 ó 7 hojas | [Aluprom 25 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2025%20Catalogo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2025(525).pdf) |
| [ALUPROM 34 HO](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-34) | Serie abatible con rotura de puente térmico con diseño de “hoja oculta” y de cámara europea · Marcos de 54 con resalte hasta ancho total de 61,3 · Acristalamiento variable mediante gomas EPDM; huecos para acristalamientos de 14, 16, 18, 20, 22 y 24mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Batiente, Proyectante | [Aluprom 34 HO Catalogo](https://aluval.es/files/pdf/category/Aluprom%2034%20HO%20Catalogo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2034(534).pdf) |
| [ALUPROM 35 HO](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-35-ho) | Serie abatible con rotura de puente térmico con diseño de “hoja oculta” y de cámara europea · Marco de 77 con resalte hasta ancho total de 84,5mm · Doble escuadra en marcos y hojas | Fijo, Practicable, Apertura oscilobatiente, Batiente | [Aluprom 35 HO Catalogo](https://aluval.es/files/pdf/category/Aluprom%2035%20HO%20Catalogo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2035(535).pdf) |
| [ALUPROM 36](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-36) | Serie abatible con rotura puente térmico de cámara europea · Marcos de 54mm · Acristalamiento: junquillos de hueco desde 12,8 hasta 47mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura osciloparalela, Batiente, Proyectante, Plegable en 3, 4, 5, 6 ó 7 hojas | [Aluprom 36 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2036%20Catalogo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2036(536).pdf) |
| [ALUPROM 38](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-38) | Serie abatible con rotura de puente térmico de cámara europea · Marcos de 58mm · Acristalamiento junquillo desde 16,8 hasta 50,8mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilo batiente, Apertura oscilo paralela, Batiente, Proyectante, Pivotante, Plegable en 3, 4, 5, 6 ó 7 hojas | [Aluprom 38 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2038%20Catalogo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2038(38).pdf) |
| [ALUPROM 43](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-43) | Serie abatible con rotura de puente térmico con diseño de “hoja oculta” y con cámara europea · Marcos de 67 mm con resalte hasta ancho total de 74,5 · Doble escuadra en marcos y hojas | — | [Aluprom 43 HO Catálogo](https://aluval.es/files/pdf/category/Aluprom%2043%20HO%20Cat%C3%A1logo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas43(543).pdf) |
| [ALUPROM 44](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-44) | — | — | [Aluprom 44 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2044%20Catalogo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2044(544).pdf) |
| [ALUPROM 46](https://aluval.es/productos/series-practicables-rpt-canal-europeo/aluprom-46) | Serie abatible con rotura de puente térmico de cámara europea · Marcos de 77,2mm · Doble escuadra en marcos y hojas | — | [Aluprom 46 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2046%20Catalogo.pdf) · [Series Practicables RPT CE](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20CE.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2046(546).pdf) |

### Series Practicables RPT Canal 16

Prestaciones superiores para proyectos que exigen más. [Web](https://aluval.es/productos/series-practicables-rpt-canal-16)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [ALUPROM 25 C16](https://aluval.es/productos/series-practicables-rpt-canal-16/aluprom-25c16) | Serie abatible rotura de puente térmico con cámara para herraje de canal 16 con eje de 13 · Marco de 45mm de ancho · Acristalamiento: Junquillos desde 9 hasta 37,8mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura osciloparalela, Batiente, Proyectante | [Aluprom 25 C16 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2025%20C16%20Catalogo.pdf) · [Series Practicables RPT C16](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20C16.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2025(10011).pdf) |
| [ALUPROM 34 HO C16](https://aluval.es/productos/series-practicables-rpt-canal-16/aluprom-34hoc16) | Serie abatible con rotura de puente térmico con diseño de “hoja oculta” con cámara para herraje de canal 16 con eje de 13 · Marcos de 54 con resalte hasta ancho total de 61,3 · Acristalamiento variable mediante gomas EPDM; huecos para acristalamientos de 16, 18, 20, 22, 24 y 26mm | Fijo, Practicable, Apertura oscilobatiente, Batiente | [Aluprom 34 C16 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2034%20C16%20Catalogo.pdf) · [Series Practicables RPT C16](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20C16.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2034(10010).pdf) |
| [ALUPROM 35 HO C16](https://aluval.es/productos/series-practicables-rpt-canal-16/aluprom-35hoc16) | Serie abatible con rotura de puente térmico con diseño de “hoja oculta” con cámara para herraje de canal 16 con eje de 13mm · Marcos de 77 con resalte hasta ancho total de 84,5mm · Doble escuadra en marcos y hojas | Fijo, Practicable, Apertura oscilobatiente, Batiente | [Aluprom 35 HO C16 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2035%20HO%20C16%20Catalogo.pdf) · [Series Practicables RPT C16](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20C16.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2035(10009).pdf) |
| [ALUPROM 36 C16](https://aluval.es/productos/series-practicables-rpt-canal-16/aluprom-36c16) | Serie abatible con rotura de puente térmico con cámara para herraje de canal 16 con eje de 13 · Marcos de 54mm de ancho · Acristalamiento: junquillos de hueco desde 12,8 hasta 46,8mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura osciloparalela, Batiente, Proyectante, Plegable en 3, 4, 5, 6 ó 7 hojas | [Aluprom 36 C16 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2036%20C16%20Catalogo.pdf) · [Series Practicables RPT C16](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20C16.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2036(10008).pdf) |
| [ALUPROM 38 C16](https://aluval.es/productos/series-practicables-rpt-canal-16/aluprom-38-c16) | Serie abatible rotura de puente térmico con cámara para herraje de canal 16 con eje de 13 · Marco de 58mm de ancho · Acristalamiento Junquillos desde 16,8 hasta 50,8mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura oscilo-paralela, Batiente, Proyectante, Plegable en 3, 4, 5, 6 ó 7 hojas | [Aluprom 38 C16 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2038%20C16%20Catalogo.pdf) · [Series Practicables RPT C16](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20C16.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2038(38999).pdf) |
| [ALUPROM 44 C16](https://aluval.es/productos/series-practicables-rpt-canal-16/aluprom-44c16) | Serie abatible rotura de puente térmico con cámara para herraje de canal 16 con eje de 13 · Marco de 67mm de ancho · Acristalamiento junquillos desde 26 hasta 60mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura oscilo paralela, Batiente, Proyectante, Plegable en 3, 4, 5, 6 ó 7 hojas | [Aluprom 44 C16 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2044%20C16%20Catalogo.pdf) · [Series Practicables RPT C16](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20C16.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2044(10005).pdf) |
| [ALUPROM 46 C16](https://aluval.es/productos/series-practicables-rpt-canal-16/aluprom-46-c16) | Serie abatible rotura de puente térmico con cámara para herraje de canal 16 con eje de 13 · Marco de 77mm de ancho · Acristalamiento Junquillos desde 36 hasta 70mm | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura osciloparalela, Batiente, Proyectante, Plegable en 3, 4, 5, 6 ó 7 hojas | [Aluprom 46 C16 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2046%20C16%20Catalogo.pdf) · [Series Practicables RPT C16](https://aluval.es/files/pdf/category/Series%20Practicables%20RPT%20C16.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2046(10004).pdf) |

### Series Correderas - Elevables RPT

Grandes aperturas con el máximo confort. Las correderas y elevables con rotura de puente térmico de Aluval permiten disfrutar de amplias superficies acristaladas con excelente aislamiento térmico y acústico. [Web](https://aluval.es/productos/series-correderas-rpt)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [ALUPROM 17](https://aluval.es/productos/series-correderas-rpt/aluprom-17) | Serie corredera perimetral con rotura puente térmico · Marco de 70mm con carril de rodadura ancho · Acristalamiento: hojas de hueco de 24mm | Corredera 2, 3, 4 y 6 hojas | [Aluprom 17 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2017%20Catalogo.pdf) · [Series Correderas - Elevables RPT](https://aluval.es/files/pdf/category/Series%20Correderas%20-%20Elevables%20RPT.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2017(10017).pdf) |
| [ALUPROM 20](https://aluval.es/productos/series-correderas-rpt/aluprom-20) | Serie corredera con diseño minimalista y rotura de puente térmico y con marcos de 155 mm · Acristalamiento desde 33 hasta 43 mm · Posibilidad de realización de hojas a inglete con una sección central de tan solo 35mm | — | [Aluprom 20 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2020%20Catalogo.pdf) · [Series Correderas - Elevables RPT](https://aluval.es/files/pdf/category/Series%20Correderas%20-%20Elevables%20RPT.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas20(20).pdf) |
| [ALUPROM 31](https://aluval.es/productos/series-correderas-rpt/aluprom-31) | Serie corredera / elevable con rotura de puente térmico con marco de 80mm · Acristalamiento de hasta 33mm · Altura de hojas de 65mm y de 74mm para correderas elevables | — | [Aluprom 31 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2031%20Catalogo.pdf) · [Series Correderas - Elevables RPT](https://aluval.es/files/pdf/category/Series%20Correderas%20-%20Elevables%20RPT.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2031(31).pdf) |
| [ALUPROM 41](https://aluval.es/productos/series-correderas-rpt/aluprom-41) | Serie corredera elevable con rotura de puente térmico · Marcos de 100 mm con carril de rodadura ancho · Anchura de hoja 45mm | Corredera 1, 2, 3, 4 y 6 hojas, Corredera elevable de 1, 2 y 4 hojas, Corredera elevable 1 hoja y fijo integrado con el mismo marco, Corredera 2 hojas y fijo integrado en el mismo marco, Corredera de 4 hojas con dos hojas centrales elevables y fijos exteriores, Corredera de 6 hojas con dos hojas centrales elevables y fijos exteriores | [Aluprom 41 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2041%20Catalogo.pdf) · [Series Correderas - Elevables RPT](https://aluval.es/files/pdf/category/Series%20Correderas%20-%20Elevables%20RPT.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2041(10015).pdf) |
| [ALUPROM 42](https://aluval.es/productos/series-correderas-rpt/aluprom-42) | Serie corredera elevable con rotura de puente térmico · Marcos de 130 mm. con carril de rodadura ancho · Anchura de hoja 54mm | Corredera 1, 2 , 3 , 4 y 6 hojas, Corredera elevable de 1, 2 y 4 hojas, Corredera elevable 1 hoja y fijo integrado con el mismo marco, Corredera 2 y 3 hojas con fijo integrado en el mismo marco, Corredera de 4 hojas con dos hojas centrales elevables y fijos exteriores, Corredera de 6 hojas con dos hojas centrales elevables y fijos exteriores | [Aluprom 42 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2042%20Catalogo.pdf) · [Series Correderas - Elevables RPT](https://aluval.es/files/pdf/category/Series%20Correderas%20-%20Elevables%20RPT.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2042(10014).pdf) |

### Fachadas Ligeras

Transparencia, innovación y diseño en cada proyecto. [Web](https://aluval.es/productos/fachadas-ligeras)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [ALUPROM 54](https://aluval.es/productos/fachadas-ligeras/aluprom-54) | Muro cortina con montantes desde 45mm hasta 200mm · Ancho de montantes de 54mm · Corte en recto y montaje mediante piezas regulables | — | [Aluprom 54 Catalogo(3504)](https://aluval.es/files/pdf/category/Aluprom%2054%20Catalogo(3504).pdf) · [Aluprom 54 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2054%20Catalogo.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicast_54(54).pdf) |

### Series Mallorquinas

Tradición y modernidad en perfecta armonía. [Web](https://aluval.es/productos/series-mallorquinas)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [SISTEMAS ALUVAL](https://aluval.es/productos/series-mallorquinas/sistemas-aluval) | — | — | [Series Mallorquinas](https://aluval.es/files/pdf/category/Series%20Mallorquinas.pdf) · [Sistemas Aluval](https://aluval.es/files/pdf/category/Sistemas%20Aluval.pdf) |
| [MALLORQUINA 4020](https://aluval.es/productos/series-mallorquinas/mallorquina-4020) | Persianas tipo mallorquinas · Marcos de 40mm de ancho · Lama fija y graduable | Fijo, Practicable, Practicable de apertura exterior, Batiente, Proyectante | [Mallorquina 4020](https://aluval.es/files/pdf/category/Mallorquina%204020.pdf) · [Series Mallorquinas](https://aluval.es/files/pdf/category/Series%20Mallorquinas.pdf) |
| [MALLORQUINA ESTÁNDAR](https://aluval.es/productos/series-mallorquinas/mallorquina-estandar) | Persianas tipo mallorquinas · Marcos de 40mm de ancho · Lama fija y graduable | Fijo, Practicable, Practicable de apertura exterior, Apertura oscilobatiente, Apertura oscilo paralela, Batiente, Proyectante, Plegable en 3, 4, 5, 6, 7 u 8 hojas | [Mallorquina Estándar](https://aluval.es/files/pdf/category/Mallorquina%20Est%C3%A1ndar.pdf) · [Series Mallorquinas](https://aluval.es/files/pdf/category/Series%20Mallorquinas.pdf) |

### Sistemas de Barandillas

Seguridad y diseño en perfecta sintonía. Los sistemas de barandillas de Aluval combinan resistencia, estética y fácil instalación para adaptarse a todo tipo de espacios. [Web](https://aluval.es/productos/sistemas-de-barandillas)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [BARANDILLA TRADICIONAL](https://aluval.es/productos/sistemas-de-barandillas/barandilla-tradicional) | Barandilla tradicional basada en U de 40x24 · Corte en recto y montaje mediante piezas regulables · Gran variedad de soluciones y herrajes para su montaje | — | [Barandilla tradicional catalogo](https://aluval.es/files/pdf/category/Barandilla%20tradicional%20catalogo.pdf) · [Sistemas de Barandillas](https://aluval.es/files/pdf/category/Sistemas%20de%20Barandillas.pdf) |
| [ALUPROM 50](https://aluval.es/productos/sistemas-de-barandillas/aluprom-50) | Barandilla basada en U de 51x21mm con y sin portavidrios · Perfil forma U para integrar vidrio · Corte en recto y montaje mediante piezas regulables | — | [Aluprom 50 Catalogo](https://aluval.es/files/pdf/category/Aluprom%2050%20Catalogo.pdf) · [Sistemas de Barandillas](https://aluval.es/files/pdf/category/Sistemas%20de%20Barandillas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%2050(55).pdf) |
| [CLASS VISION](https://aluval.es/productos/sistemas-de-barandillas/class-vision) | Barandilla basada en un perfil U base de 122x46mm o de 122x81mm · Diseño minimalista · Sistema de montaje sencillo y limpio | — | [Class Visión Catalogo](https://aluval.es/files/pdf/category/Class%20Visi%C3%B3n%20Catalogo.pdf) · [Sistemas de Barandillas](https://aluval.es/files/pdf/category/Sistemas%20de%20Barandillas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%20CLASS_VISON(4000).pdf) |
| [CLASS JULIET](https://aluval.es/productos/sistemas-de-barandillas/class-juliet) | Barandilla basada en dos guías laterales que soportan el vidrio con unos tapones inferiores de aluminio · Diseño minimalista · Sistema de montaje sencillo y limpio | — | [Class Juliet Catalogo](https://aluval.es/files/pdf/category/Class%20Juliet%20Catalogo.pdf) · [Sistemas de Barandillas](https://aluval.es/files/pdf/category/Sistemas%20de%20Barandillas.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%20CLASS_JULIET(5000).pdf) |

### Protección solar y cerramientos exteriores

Confort y eficiencia durante todo el año. [Web](https://aluval.es/productos/proteccion-solar-y-cerramientos-exteriores)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [JALOUSIE](https://aluval.es/productos/proteccion-solar-y-cerramientos-exteriores/jalousie) | Sistema de celosía con baldas proyectantes · Debido a su entramado de perfiles horizontales aporta un plus de seguridad al hueco · Control de la ventilación de una forma sencilla y gradual | — | [Jalousie Catalogo](https://aluval.es/files/pdf/category/Jalousie%20Catalogo.pdf) · [Protección Solar y Cerramientos Exteriores](https://aluval.es/files/pdf/category/Protecci%C3%B3n%20Solar%20y%20Cerramientos%20Exteriores.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%20JALOUSIE(61).pdf) |
| [TECHO MÓVIL](https://aluval.es/productos/proteccion-solar-y-cerramientos-exteriores/techo-movil) | Sistema de techo móvil con policarbonato o panel de 16mm de gran versatilidad y fácil montaje · Pendiente prevista de 10° · Ancho de placa máximo recomendado de 1250mm | — | [Protección Solar y Cerramientos Exteriores](https://aluval.es/files/pdf/category/Protecci%C3%B3n%20Solar%20y%20Cerramientos%20Exteriores.pdf) · [Techo móvil Catalogo](https://aluval.es/files/pdf/category/Techo%20m%C3%B3vil%20Catalogo.pdf) |
| [CELOSÍAS FIJAS CLIPADAS](https://aluval.es/productos/proteccion-solar-y-cerramientos-exteriores/celosias-fijas-clipadas) | — | — | [Celosías fijas clipadas Catalogo](https://aluval.es/files/pdf/category/Celos%C3%ADas%20fijas%20clipadas%20Catalogo.pdf) · [Protección Solar y Cerramientos Exteriores](https://aluval.es/files/pdf/category/Protecci%C3%B3n%20Solar%20y%20Cerramientos%20Exteriores.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_fichas_tecnicas%20CELOSIAS%20FIJAS%20CLIPADAS(5101).pdf) |
| [CELOSÍAS](https://aluval.es/productos/proteccion-solar-y-cerramientos-exteriores/celosias) | Lamas orientables o fijas en aluminio de extrusión · Pesos 8,5Kg/m2 (lama de 120mm), 10,5Kg/m2 (lama de 210mm) y 12,8Kg/m2 (lama de 300mm) · Diseños elípticos de 120x20mm, 210x30mm y de 300x40mm | — | [Celosías Catalogo](https://aluval.es/files/pdf/category/Celos%C3%ADas%20Catalogo.pdf) · [Protección Solar y Cerramientos Exteriores](https://aluval.es/files/pdf/category/Protecci%C3%B3n%20Solar%20y%20Cerramientos%20Exteriores.pdf) · [Ficha técnica](https://aluval.es/files/pdf/category/aluval_ficha_tecnica_lama_ovalada(5102).pdf) |
| [DIVISORIA Y 100](https://aluval.es/productos/proteccion-solar-y-cerramientos-exteriores/divisoria-y-100) | Lama fija en aluminio de extrusión · Nº de lamas por metro: 11 con paso referencia 8000272 · Peso por m2: 8.283 Kg | — | [Protección Solar y Cerramientos Exteriores](https://aluval.es/files/pdf/category/Protecci%C3%B3n%20Solar%20y%20Cerramientos%20Exteriores.pdf) · [Techo móvil Catalogo](https://aluval.es/files/pdf/category/Techo%20m%C3%B3vil%20Catalogo.pdf) |

### Guías y Lamas de seguridad

Protección reforzada con diseño Aluval. Nuestras guías y lamas de seguridad garantizan resistencia, durabilidad y confianza frente a intentos de intrusión. [Web](https://aluval.es/productos/guias-y-lamas-de-seguridad)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [PS-30](https://aluval.es/productos/guias-y-lamas-de-seguridad/ps-30) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [PS-78](https://aluval.es/productos/guias-y-lamas-de-seguridad/ps-78) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) |
| [ECO-100](https://aluval.es/productos/guias-y-lamas-de-seguridad/eco-100) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [ECO-80](https://aluval.es/productos/guias-y-lamas-de-seguridad/eco-80) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [GUÍAS](https://aluval.es/productos/guias-y-lamas-de-seguridad/guias) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [GUÍAS Catálogo](https://aluval.es/files/pdf/category/GU%C3%8DAS%20Cat%C3%A1logo.pdf) |
| [PS-4](https://aluval.es/productos/guias-y-lamas-de-seguridad/ps-4) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [LAMAS](https://aluval.es/productos/guias-y-lamas-de-seguridad/lamas) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [PS-15](https://aluval.es/productos/guias-y-lamas-de-seguridad/ps-15) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [PS-40](https://aluval.es/productos/guias-y-lamas-de-seguridad/ps-40) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [PS-10](https://aluval.es/productos/guias-y-lamas-de-seguridad/ps-10) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |
| [PS-100](https://aluval.es/productos/guias-y-lamas-de-seguridad/ps-100) | — | — | [CatalogoEspecificoDeGuias](https://aluval.es/files/pdf/category/CatalogoEspecificoDeGuias.pdf) · [Catálogo específico de guías](https://aluval.es/files/pdf/category/Cat%C3%A1logo%20espec%C3%ADfico%20de%20gu%C3%ADas.pdf) |

### Mosquiteras

Protección eficiente con innovación en cada detalle. [Web](https://aluval.es/productos/mosquiteras)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [Aludark R33](https://aluval.es/productos/mosquiteras/aludark-r33) | El sistema oscurecedor alu-dark es un sistema enrollable de tejido para interior y exterior técnico Black out, el cual impide el paso de luz · El nuevo oscurecedor se encuentra disponible en una amplia gama de colores bajo pedido y de forma permanente en color negro · Las dimensiones máximas que ofrece el sistema son 120 cm x 170 cm | — | [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [Aludark P42](https://aluval.es/productos/mosquiteras/aludark-p42) | — | — | [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [Aludark R42](https://aluval.es/productos/mosquiteras/aludark-r42) | — | — | [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [Mosquiclass](https://aluval.es/productos/mosquiteras/mosquiclass) | Mosquiclass es la primera mosquitera automontable sin guía inferior para puertas y ventanas · Su sistema flexiform, consigue ajustar la tela a la guía sin que permanezca fija a los cuatro laterales, impidiendo posibles roturas · Mediante un innovador sistema reel, la mosquitera se articula a través de un movimiento horizontal que recoge la guía en los carriles internos adaptables | — | [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [Corredera Curva](https://aluval.es/productos/mosquiteras/corte-recto-curvo) | — | — | [Mosquitera Corredera Curva - 2020](https://aluval.es/files/pdf/category/Mosquitera%20Corredera%20Curva%20-%202020.pdf) · [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [Corredera Recta](https://aluval.es/productos/mosquiteras/corte-recto-lisa) | — | — | [Mosquitera Corredera Recta - 2020](https://aluval.es/files/pdf/category/Mosquitera%20Corredera%20Recta%20-%202020.pdf) · [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [Mosquitera fija](https://aluval.es/productos/mosquiteras/fija) | — | — | [Mosquitera Fija - 2020](https://aluval.es/files/pdf/category/Mosquitera%20Fija%20-%202020.pdf) · [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [R33](https://aluval.es/productos/mosquiteras/r33) | — | — | [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [R42](https://aluval.es/productos/mosquiteras/r42) | — | — | [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |
| [P42](https://aluval.es/productos/mosquiteras/p42) | El P42 es un sistema enrollable de tejido termosoldable de malla de 1,8x1,6 en color gris para interior y exterior , el cuál permite el paso de luz · Presentable en medidas 170 cm x 170 cm. y 230 cm x 170 cm. En un cajón de 42 mm | — | [Mosquiteras](https://aluval.es/files/pdf/category/Mosquiteras.pdf) |

### Sistemas Tradicionales

La esencia del aluminio en soluciones de siempre. [Web](https://aluval.es/productos/sistemas-tradicionales)

| Serie | Características principales | Aperturas | Documentos |
|---|---|---|---|
| [VITRINA](https://aluval.es/productos/sistemas-tradicionales/vitrina) | — | — | [Vitrinas](https://aluval.es/files/pdf/category/Vitrinas.pdf) |
| [FORROS](https://aluval.es/productos/sistemas-tradicionales/forros) | — | — | [Forros](https://aluval.es/files/pdf/category/Forros.pdf) |
| [PREMARCOS OBRA](https://aluval.es/productos/sistemas-tradicionales/premarcos-obra) | — | — | [Premarcos de obra Catalogo](https://aluval.es/files/pdf/category/Premarcos%20de%20obra%20Catalogo.pdf) · [Premarcos obra - Esquema](https://aluval.es/files/pdf/category/Premarcos%20obra%20-%20Esquema.pdf) |
| [MÁMPARA OFICINA](https://aluval.es/productos/sistemas-tradicionales/mampara-oficina) | — | — | [Mampara Oficina - Esquema](https://aluval.es/files/pdf/category/Mampara%20Oficina%20-%20Esquema.pdf) · [Mampara oficina](https://aluval.es/files/pdf/category/Mampara%20oficina.pdf) |
| [LUMINOSOS](https://aluval.es/productos/sistemas-tradicionales/luminosos) | — | — | [Luminosos y Chapas](https://aluval.es/files/pdf/category/Luminosos%20y%20Chapas.pdf) |
| [NORMALIZADOS](https://aluval.es/productos/sistemas-tradicionales/normalizados) | — | — | [Normalizados Catalogo](https://aluval.es/files/pdf/category/Normalizados%20Catalogo.pdf) |

### Acabados y colores Aluval

[Web](https://aluval.es/acabados-y-colores) · Lacado para arquitectura, licencia nº 482.

- **Lacados estándar**: 1013 blanco perla · 1015 marfil claro · 3005 rojo vino · 5010 azul genciana · 5013 azul cobalto · 6005 verde musgo · 6009 verde abeto · 7011 gris hierro · 7012 gris basalto · 7016 gris antracita · 7022 gris sombra · 7035 gris luminoso · 8007 pardo corzo · 8014 sepia · 8017 chocolate · 9010 blanco puro · 9011 negro grafito
- **Lacados texturados**: 7016 · 6009 · 8019 · 9016 · 7033 texturados · Noir 200
- **Efecto madera**: Pino 202 · Pino · Roble 202 · Roble · Acacia 202 · Acacia · Raíz · Nogal · Castaño · Teka liso · Golden dorado · Golden dorado oscuro · Nogal texturado oscuro · Roble golden texturado · Nogal siena · Teka texturado · Embero claro · Embero oscuro · Embero · Embero 639 · Cerezo · Cerezo texturado · Pino texturado · Pino envejecido texturado · Nogal andaluz · Siena texturizado 2

---

## 3. Ventanas de aluminio — EXTRUGASA

Web: <https://www.extrugasa.com/edificacion> · Todas las series de la web (área de Edificación).

> La web pone algunos productos en varias categorías; aquí aparecen en todas ellas. Las series XP que la web solo muestra en la 2.ª página de *practicables* se han añadido a esa categoría. Los manuales, BIM, CAD y ensayos completos están en la intranet de Extrugasa.

### Cerramiento exterior

| Producto | Descripción | Ficha |
|---|---|---|
| [XM-40](https://www.extrugasa.com/edificacion/xm-40) | El sistema de aluminio multifunción XM-40, brinda la posibilidad de diseñar un sistema plegable, practicable o corredera, además dispone de multitud de herrajes y perfiles para poder… | [PDF](https://www.extrugasa.com/?jet_download=78793551dddd9f62f0048e4e2e5ca2918aa5c40a) |
| [Celosías y lamas de ventilación](https://www.extrugasa.com/edificacion/celosias-y-lamas-ventilacion) | Sistema de aluminio extruido de celosías y lamas de ventilación, usadas en cerramientos exteriores e interiores, para la ocultación de muros, protección solar, separación de espacios. | [PDF](https://www.extrugasa.com/?jet_download=cb471e6155c879b7f7d2bad0b696a1874d467aa5) |
| [Cerrajería](https://www.extrugasa.com/edificacion/cerrajeria) | La serie de cerrajerías dispone de multitud de soluciones para viviendas unifamiliares, locales comerciales, naves industriales, etc. | [PDF](https://www.extrugasa.com/?jet_download=d446cc22c16e25142c317826c60c7bd01b308b3e) |

### Control solar

| Producto | Descripción | Ficha |
|---|---|---|
| [Lama ala de avión](https://www.extrugasa.com/edificacion/ala-de-avion) | Sistema de lama para control solar que permiten la atenuación de radiación solar para mejorar la eficiencia energética. | [PDF](https://www.extrugasa.com/?jet_download=50f2ba97533b0524829b240e7483c1149372d60e) |
| [Lama en “C”](https://www.extrugasa.com/edificacion/perfil-en-c) | Sistema de protección solar en aluminio tipo C que permiten la atenuación de radiación solar para mejorar la eficiencia energética. | [PDF](https://www.extrugasa.com/?jet_download=0f7192bfb0da45ac6c650d8d019caa3cf0242adb) |
| [Lama rectangular](https://www.extrugasa.com/edificacion/perfil-rectangular) | Sistema de protección solar en aluminio de tipo rectangular que permiten la atenuación de radiación solar para ahorros energéticos en interiores. | [PDF](https://www.extrugasa.com/?jet_download=e89c670005b9ef9bf709cba87ba008c8807eae4c) |
| [XM-40](https://www.extrugasa.com/edificacion/xm-40) | El sistema de aluminio multifunción XM-40, brinda la posibilidad de diseñar un sistema plegable, practicable o corredera, además dispone de multitud de herrajes y perfiles para poder… | [PDF](https://www.extrugasa.com/?jet_download=78793551dddd9f62f0048e4e2e5ca2918aa5c40a) |

### Fachada ventilada

| Producto | Descripción | Ficha |
|---|---|---|
| [TS-200](https://www.extrugasa.com/edificacion/ts-200) | Sistema de fachada ventilada en aluminio de fijación oculta con tornillos, abrazadera y perfil guía sobre subestructura de aluminio. | [PDF](https://www.extrugasa.com/?jet_download=28b117ae9ef8139fc799b8dd29c049092082bf07) |
| [TS-300](https://www.extrugasa.com/edificacion/ts-300) | El método de fijación TS-300 es especialmente indicado para el cerramiento de grandes superficies de fachadas con modulaciones horizontales. | [PDF](https://www.extrugasa.com/?jet_download=caa1c46ad7452f73a8a3051d6ecc12f4308d361c) |
| [TS-700](https://www.extrugasa.com/edificacion/ts-700) | — | [PDF](https://www.extrugasa.com/?jet_download=7f7021a92af8184bb3bd8a687a1ecc6124518651) |

### Interiorismo

| Producto | Descripción | Ficha |
|---|---|---|
| [XM-40](https://www.extrugasa.com/edificacion/xm-40) | El sistema de aluminio multifunción XM-40, brinda la posibilidad de diseñar un sistema plegable, practicable o corredera, además dispone de multitud de herrajes y perfiles para poder… | [PDF](https://www.extrugasa.com/?jet_download=78793551dddd9f62f0048e4e2e5ca2918aa5c40a) |
| [Mamparas](https://www.extrugasa.com/edificacion/mamparas) | Sistema en aluminio diseñado para generar divisiones interiores para oficinas y versátil en forma y estructura, pues su variedad en perfiles permite diferenciar espacios en oficinas… | [PDF](https://www.extrugasa.com/?jet_download=5f9db7cb99e08d6cc145baf0504a5775d1678e58) |

### Muro cortina

| Producto | Descripción | Ficha |
|---|---|---|
| [EXAP-50 SG](https://www.extrugasa.com/edificacion/exap-sg) | Fachada ligera EXAP-50 SG, con posibilidad de diferentes vistas exteriores: vidrio estructural. | [PDF](https://www.extrugasa.com/?jet_download=e4a4821ffaf37ecda5ed2b853f099e0fb910dcfd) |
| [EXAP-50 TP](https://www.extrugasa.com/edificacion/exap-50-tp) | EXAP-TP, fachada ligera estructural de vidrio visto, con posibilidad de diferentes vistas exteriores: vidrio estructural. | [PDF](https://www.extrugasa.com/?jet_download=c8f94b22f144ba056e9f1a09dce176f97f8c839a) |
| [EXAP-50 TH TV](https://www.extrugasa.com/edificacion/exap-50-th-tv) | EXAP-50 TH TV es la opción ideal para fachadas ligeras con posibilidad de diferentes vistas exteriores: trama horizontal, trama vertical. | [PDF](https://www.extrugasa.com/?jet_download=a0be6c2fb5c7bfb9dbc3fa185b7803bde3bde2d0) |
| [EXAP-50 FT](https://www.extrugasa.com/edificacion/exap-50-ft) | — | [PDF](https://www.extrugasa.com/?jet_download=bca5e4a4ea14628ce0f9bbdab46a6129d9512d93) |
| [EXAP UNITIZED](https://www.extrugasa.com/edificacion/exap-unitized) | Con este sistema de fachada ligera de tipo modular, se mantiene la estanqueidad en grandes movimientos como sismos o dilatación, permitiendo la construcción de edificios de gran altura. | [PDF](https://www.extrugasa.com/?jet_download=778e7305b6955eaee466c5fd1cc80f1c21f8c139) |

### Perfiles normalizados

| Producto | Descripción | Ficha |
|---|---|---|
| [Perfiles normalizados](https://www.extrugasa.com/edificacion/perfiles-normalizados) | Las infinitas posibilidades del aluminio, combinadas con sus características como la ligereza, dureza, durabilidad y tratamientos superficiales, hacen que los perfiles normalizados sean… | [PDF](https://www.extrugasa.com/?jet_download=37cc7a4cf2b0ae133603dc0fe05239a9a6923e5c) |

### Perfiles complementarios

| Producto | Descripción | Ficha |
|---|---|---|
| [Premarcos](https://www.extrugasa.com/edificacion/premarcos) | Perfil de aluminio complementario para ventanas y puertas. | [PDF](https://www.extrugasa.com/?jet_download=df92e9b6cb1797eee97a2e0e7d65b9107c6dc288) |
| [Albardillas](https://www.extrugasa.com/edificacion/albardillas) | Elemento de aluminio instalado en la parte superior de un muro para resguardarlo de la lluvia y de otras condiciones climáticas. | [PDF](https://www.extrugasa.com/?jet_download=55d8ce575787d81f8c349009711de3cf4e79473a) |
| [Dinteles](https://www.extrugasa.com/edificacion/dinteles) | Perfil complementario para ventanas con persiana. | [PDF](https://www.extrugasa.com/?jet_download=32dbca92f8a202f39e8daa37c5539ca6323ebdac) |
| [Alargaderas](https://www.extrugasa.com/edificacion/alargadera) | Perfil complementario para ventanas. | [PDF](https://www.extrugasa.com/?jet_download=a93a3535643fb65f7e6751f3df845dc20555f5e9) |
| [Guías](https://www.extrugasa.com/edificacion/guias) | Guías de aluminio para ventanas con persiana. | [PDF](https://www.extrugasa.com/?jet_download=811e509e9cf0943f2d88e29207bbc81a37f74daa) |
| [Tapajuntas](https://www.extrugasa.com/edificacion/tapajuntas) | Tapajuntas de aluminio para sistemas de ventanas y puertas. | [PDF](https://www.extrugasa.com/?jet_download=47bc12665a541cd433c8167961f22d75984f7d31) |

### Sistema de barandillas

| Producto | Descripción | Ficha |
|---|---|---|
| [XR-Handrail](https://www.extrugasa.com/edificacion/xr-handrail) | Sistema para barandillas y pasamanos que permite crear diferentes opciones, tanto para interiores como para exteriores, en tramos rectos y de escalera. | [PDF](https://www.extrugasa.com/?jet_download=3a0a83d3cd60c7b075a7de2beffc753524b33941) |
| [XR-Frame Glass](https://www.extrugasa.com/edificacion/xr-frame-glass) | Sistema minimalista con instalación en el exterior de la ventana mediante fijaciones ocultas. | [PDF](https://www.extrugasa.com/?jet_download=9b61ee8d735f2d2790ad8a9b2efbab98b0089202) |
| [XR-Glass](https://www.extrugasa.com/edificacion/xr-glass) | Sistema de barandilla de regulación patentada, de perfil de aluminio en “U”, ala vertical y lateral, soporta cargas pesadas y proporciona transparencia, permitiendo visibilidad plena. | [PDF](https://www.extrugasa.com/?jet_download=b2b48668e9dc28a0f00ddf6c72d8d05f35e9695f) |

### Sistema de puertas

| Serie | Descripción | Uf (W/m²K) | Uw (W/m²K) | Acústica Rw | Aire / Agua / Viento | Ficha |
|---|---|---|---|---|---|---|
| [XP-80+ HI](https://www.extrugasa.com/edificacion/xp-80-c16-hi) | Sistema de ventana practicable de 80 mm de canal 16 presenta una RPT de 44 mm y su aislamiento térmico HI en cámara garantiza las mejores prestaciones térmicas y acústicas. | 0,87 | ≥ 0,71 | 48 (-1;-4) dB | Clase 4 / E1950 / C5 | [PDF](https://www.extrugasa.com/?jet_download=ecbd2b235397d949b3a67f7a351d8285099e42a2) |
| [V-8000 40](https://www.extrugasa.com/edificacion/v-8000-40) | Sistema practicable sin RPT de reducido tamaño con 40 mm de marco. | 6,2 | ≥ 3,06 | 41 (-1:-5) dB | Clase 3 / 9A / C4 | [PDF](https://www.extrugasa.com/?jet_download=9e1804b0f27b8ff7598c2da18dfca9c9e34c0873) |
| [V-8000 45](https://www.extrugasa.com/edificacion/v-8000-45) | Sistema practicable sin RPT de reducido tamaño con 40 mm de marco. | 6,2 | — | 41 (-1:-5) dB | Clase 3 / E750 / C4 | [PDF](https://www.extrugasa.com/?jet_download=19722c01dc67c48cba6c1efda9b109eff65c8202) |
| [XD-70](https://www.extrugasa.com/edificacion/xd-70) | El sistema de puertas de aluminio XD-70 ha sido diseñado para satisfacer las exigencias de cualquier proyecto en términos de aislamiento, seguridad y diseño. | — | — | — | — / — / — | [PDF](https://www.extrugasa.com/?jet_download=dce47feb62d9f7e74b55025b8dfcfd144b9ab687) |

### Sistema de ventanas practicables

| Serie | Descripción | Uf (W/m²K) | Uw (W/m²K) | Acústica Rw | Aire / Agua / Viento | Ficha |
|---|---|---|---|---|---|---|
| [XP-70+ HI](https://www.extrugasa.com/edificacion/xp-70-c16-hi) | Sistema de ventana practicable de 70 mm de canal 16 cuenta con una RPT de 34 mm y un aislamiento térmico HI en cámara, resulta un sistema de ventanas óptimo. | 1,3 | ≥ 0,8 | 48 (-1;-4) dB | Clase 4 / E1500 / C5 | [PDF](https://www.extrugasa.com/?jet_download=c7b8909357b75b3963062aadefa31aab1a4a938a) |
| [XP-70 Compaq+ HI](https://www.extrugasa.com/edificacion/xp-70-compaq-c16-hi) | Sistema de ventana practicable de 70 mm de canal 16 cuenta con una RPT de 34 mm y un aislamiento térmico HI en cámara, resulta un sistema de ventanas óptimo. | 1,7 | ≥ 0,90 | 48 (-1;-4) dB | Clase 4 / E3000 / C5 | [PDF](https://www.extrugasa.com/?jet_download=52f5b6c6678dcf9c4f2f742ee3caade66c06b70f) |
| [XP-70 HO+](https://www.extrugasa.com/edificacion/xp-70-ho-c16) | Sistema de ventana practicable de 70 mm de canal 16 que permite su instalación en todo tipo de proyectos conservando un diseño minimalista. | 1,9 | ≥ 0,86 | 48 (-1;-4) dB | Clase 4 / E2550 / C5 | [PDF](https://www.extrugasa.com/?jet_download=dd78aaa51b801429acc4d349c2bd75f210b59b80) |
| [XP-70 HO+ HI](https://www.extrugasa.com/edificacion/xp-70-ho-c16-hi) | Sistema de ventana practicable de 70 mm de canal 16 con una RPT de 34 mm y un aislamiento térmico HI en cámara, consigue un valor Uf de 1,5 W/m2K, resulta en una solución ideal con máximas… | 1,5 | ≥ 0,83 | 48 (-1;-4) dB | Clase 4 / E2550 / C5 | [PDF](https://www.extrugasa.com/?jet_download=4536355deb04dc0132cb037f685cc48db4f2b9d9) |
| [XP-80 Compaq HI](https://www.extrugasa.com/edificacion/xp-80-compaq-hi) | Sistema de ventana practicable de 80 mm de canal europeo que cuenta con una RPT de 44 mm y un aislamiento térmico HI en cámara que ofrece las mejores prestaciones térmicas y acústicas. | 1,2 | ≥ 0,83 | 48 (-1;-4) dB | Clase 4 / E2400 / C5 | [PDF](https://www.extrugasa.com/?jet_download=aa4e6f0b6bbba7af7fb93f0c2841f318de227e39) |
| [XP-80 HI](https://www.extrugasa.com/edificacion/xp-80-hi-passivhaus) | Sistema de ventana practicable de 80 mm de canal europeo que cuenta con una RPT de 44 mm y un aislamiento térmico HI en cámara que ofrece las mejores prestaciones térmicas y acústicas. | 0,87 | ≥ 0,70 | 48 (-1;-4) dB | Clase 4 / E2100 / C5 | [PDF](https://www.extrugasa.com/?jet_download=aa151fd9ee2716897df8e6443f79f550c9e3693a) |
| [XP-80 HO HI](https://www.extrugasa.com/edificacion/xp-80-ho-hi) | Sistema de ventana practicable de 80 mm de canal europeo que posibilita las máximas prestaciones térmicas sin renunciar al diseño, manteniendo una estética limpia entre aperturas y fijos. | 1,1 | ≥ 0,72 | 48 (-1;-4) dB | Clase 4 / E1650 / C5 | [PDF](https://www.extrugasa.com/?jet_download=f8aba8cc2b59a83628d1435b7a4ed34e8d2347ea) |
| [XP-80+ HI](https://www.extrugasa.com/edificacion/xp-80-c16-hi) | Sistema de ventana practicable de 80 mm de canal 16 presenta una RPT de 44 mm y su aislamiento térmico HI en cámara garantiza las mejores prestaciones térmicas y acústicas. | 0,87 | ≥ 0,71 | 48 (-1;-4) dB | Clase 4 / E1950 / C5 | [PDF](https://www.extrugasa.com/?jet_download=ecbd2b235397d949b3a67f7a351d8285099e42a2) |
| [V-8000 40](https://www.extrugasa.com/edificacion/v-8000-40) | Sistema practicable sin RPT de reducido tamaño con 40 mm de marco. | 6,2 | ≥ 3,06 | 41 (-1:-5) dB | Clase 3 / 9A / C4 | [PDF](https://www.extrugasa.com/?jet_download=9e1804b0f27b8ff7598c2da18dfca9c9e34c0873) |
| [V-8000 45](https://www.extrugasa.com/edificacion/v-8000-45) | Sistema practicable sin RPT de reducido tamaño con 40 mm de marco. | 6,2 | — | 41 (-1:-5) dB | Clase 3 / E750 / C4 | [PDF](https://www.extrugasa.com/?jet_download=19722c01dc67c48cba6c1efda9b109eff65c8202) |
| [XP-50](https://www.extrugasa.com/edificacion/xp-50) | Sistema de ventana practicable de 50 mm de canal europeo diseñado para lograr las mejores prestaciones con la mínima sección. | — | ≥ 1,1 | — | Clase 4 / E1950 / C5 | [PDF](https://www.extrugasa.com/?jet_download=fa41dc60047ded1086b774bbbefde60183dc5f56) |
| [XP-60](https://www.extrugasa.com/edificacion/xp-60) | Sistema de ventana practicable de 60 mm de canal europeo diseñado que gracias a su doble escuadra permite realizar todos los cerramientos de ventanas y puertas. | 2,4 | ≥ 1,1 | 48 (-1:-4) dB | Clase 4 / E2250 / C5 | [PDF](https://www.extrugasa.com/?jet_download=b1193e33399714109165a93c3ee2999f118bba3e) |
| [XP-60+](https://www.extrugasa.com/edificacion/xp-60-c16) | Sistema de ventana practicable de 60 mm de canal 16 que debido a su doble escuadra se pueden realizar todos los cerramientos de ventanas y puertas con las mayores garantías. | 2,4 | ≥ 1,1 | 48 (-1;-4) dB | Clase 4 / E300 / C5 | [PDF](https://www.extrugasa.com/?jet_download=58b56a3a6ea42aedbb9a82288b4108d8205778c5) |
| [XP-60 HO](https://www.extrugasa.com/edificacion/xp-60-ho) | Sistema de ventana practicable de hoja oculta de 60 mm de canal europeo con el que se consigue mayor superficie de vidrio en la mínima sección constructiva. | 3,4 | ≥ 1,8 | 45 (-1;-4) dB | Clase 4 / E2100 / C5 | [PDF](https://www.extrugasa.com/?jet_download=f95578062f71107e0131cab18a25b4e98ee6663f) |
| [XP-70](https://www.extrugasa.com/edificacion/xp-70) | Sistema de ventana practicable de 70 mm de canal europeo, cuenta con una RPT de 34 mm que garantiza un excelente comportamiento térmico y acústico. | 1,9 | ≥ 1,0 | 48 (-1;-4) dB | Clase 4 / E3000 / C5 | [PDF](https://www.extrugasa.com/?jet_download=e9c38787842252b2106988473940cd72a0c14f8e) |
| [XP-70+](https://www.extrugasa.com/edificacion/xp-70-c16) | Sistema de ventana practicable de 70 mm de canal 16 que gracias a su RPT de 34 mm permite un excelente comportamiento térmico y acústico. | 1,9 | ≥ 1,0 | 46 (-1;-4) dB | Clase 4 / E1500 / C5 | [PDF](https://www.extrugasa.com/?jet_download=85b3b355f7f2bc729ac28ef8dc4c5252197a3cfd) |
| [XP-70 Compaq](https://www.extrugasa.com/edificacion/xp-70-compaq) | Sistema de ventana practicable de 70 mm de canal europeo, cuenta con una RPT de 34 mm que garantiza un excelente comportamiento térmico y acústico. | 2 | ≥ 0,97 | 48 (-1;-4) dB | Clase 4 / E1950 / C5 | [PDF](https://www.extrugasa.com/?jet_download=bf9e53b5618bbc209769243703c03a90d77b5e7e) |
| [XP-70 Compaq+](https://www.extrugasa.com/edificacion/xp-70-compaq-c16) | Sistema de ventana practicable de 70 mm de canal 16 que gracias a su RPT de 34 mm permite un excelente comportamiento térmico y acústico. | 2,1 | ≥ 0,97 | 48 (-1;-4) dB | Clase 4 / E3000 / C5 | [PDF](https://www.extrugasa.com/?jet_download=2940be0f5153ed1fd7540e0411e508cdd123bf67) |
| [XP-70 Compaq HI](https://www.extrugasa.com/edificacion/xp-70-compaq-hi) | Sistema de ventana practicable de 70 mm de canal europeo, cuenta con una RPT de 34 mm y un aislamiento térmico HI en cámara, lo que da como resultado mayores prestaciones. | 1,7 | ≥ 0,9 | 48 (-1;-4) dB | Clase 4 / E1950 / C5 | [PDF](https://www.extrugasa.com/?jet_download=782f6e22541caefd78662f76298b849f253ad060) |
| [XP-70 HI](https://www.extrugasa.com/edificacion/xp-70-hi) | Sistema de ventana practicable de 70 mm de canal europeo, cuenta con una RPT de 34 mm y un aislamiento térmico HI en cámara, lo que da como resultado mayores prestaciones. | 1,3 | ≥ 0,8 | 48 (-1;-4) dB | Clase 4 / E3000 / C5 | [PDF](https://www.extrugasa.com/?jet_download=80721534f5ba136f612d59fbf5c7d5a6480592a1) |
| [XP-70 HO](https://www.extrugasa.com/edificacion/xp-70-ho) | Sistema de ventana practicable de 70 mm de canal europeo que puede usarse en todo tipo de proyectos manteniendo un diseño minimalista. | 1,9 | ≥ 0,87 | 48 (-1;-4) dB | Clase 4 / E2400 / C5 | [PDF](https://www.extrugasa.com/?jet_download=f4930fc294131af751bf8bfe07b6f61a0ac9fb76) |
| [XP-70 HO HI](https://www.extrugasa.com/edificacion/xp-70-ho-hi) | Sistema de ventana practicable con una sección de 70 mm en hoja oculta y RPT de 34 mm. | 1,5 | ≥ 0,83 | 48 (-1;-4) dB | Clase 4 / E2400 / C5 | [PDF](https://www.extrugasa.com/?jet_download=3ea88df6064b479d4e978ab4f447497e92eda15f) |

### Sistema de carpintería de ventanas y puertas

| Serie | Descripción | Uf (W/m²K) | Uw (W/m²K) | Acústica Rw | Aire / Agua / Viento | Ficha |
|---|---|---|---|---|---|---|
| [XS-110](https://www.extrugasa.com/edificacion/xs-110) | El sistema de ventana corredera con su doble posibilidad de apertura, elevable o en línea, permite dar solución tanto a pequeños huecos como a grandes y pesados ventanales. | 3,6 | ≥ 1,2 | 38 (-1;-3) dB | Clase 3 / 6A / C5 | [PDF](https://www.extrugasa.com/?jet_download=b6507a002f341622ed22f9db1d4eb735addd6be9) |
| [XS-150](https://www.extrugasa.com/edificacion/xs-150) | El sistema de ventana corredera de 150 mm, diseñado para balconeras y con un innovador sistema de cierre, consigue las máximas prestaciones en permeabilidad y estanqueidad. | 3,7 | ≥ 1,0 | 40 (-1;-1) dB | Clase 4 / E1650 / C2 | [PDF](https://www.extrugasa.com/?jet_download=b43bb040955ba2fb539d29cc14d2a12aec764898) |
| [XS-160 HI](https://www.extrugasa.com/edificacion/xs-160-hi) | El sistema XS-160 HI ha sido diseñado para garantizar las máximas prestaciones en los ambientes más severos permitiendo triples acristalamientos. | 2,0 | ≥ 0,9 | 43 (-1;-3) dB | Clase 4 / 8A / C4 | [PDF](https://www.extrugasa.com/?jet_download=d6a8602f4e08ec537bdf84d7d9ceacedc5764692) |
| [XS-170](https://www.extrugasa.com/edificacion/xs-170) | — | 2,9 | ≥ 0,8 | 34 (-1;-3) dB | Clase 3 / 9A / C3 | [PDF](https://www.extrugasa.com/?jet_download=69e78ea9adb391d70a7b43388eb0bd2d042cfd02) |
| [G-90](https://www.extrugasa.com/edificacion/g-90) | Sistema corredera en línea sin RPT con corte a 90a que se caracteriza por su adaptación a cualquier solución constructiva planteada. | 6,6 | ≥ 3,18 | 34 (-1;-3) dB | Clase 3 / 5A / C2 | [PDF](https://www.extrugasa.com/?jet_download=82cdd68c480a466a5d8f981d3e9b00ed762c5600) |
| [XD-70](https://www.extrugasa.com/edificacion/xd-70) | El sistema de puertas de aluminio XD-70 ha sido diseñado para satisfacer las exigencias de cualquier proyecto en términos de aislamiento, seguridad y diseño. | — | — | — | — / — / — | [PDF](https://www.extrugasa.com/?jet_download=dce47feb62d9f7e74b55025b8dfcfd144b9ab687) |
| [Perimetral 70](https://www.extrugasa.com/edificacion/perimetral-70) | Sistema corredera en línea sin RPT y corte a 45 º de montaje y diseño sencillo. | 6,6 | ≥ 2,65 | 42 (-1;-3) dB | Clase 3 / 5A / C2 | [PDF](https://www.extrugasa.com/?jet_download=f999f4be79af08a6066240a142ac01d275d7b27d) |

### Sistemas de ventana corredera

| Serie | Descripción | Uf (W/m²K) | Uw (W/m²K) | Acústica Rw | Aire / Agua / Viento | Ficha |
|---|---|---|---|---|---|---|
| [XS-60](https://www.extrugasa.com/edificacion/xs-60) | El sistema de ventana corredera está diseñado para dar una solución minimalista y funcional en los proyectos de edificación. | 3,7 | ≥ 1,6 | 34 (-1;-3) dB | Clase 4 / 8A / — | [PDF](https://www.extrugasa.com/?jet_download=dba3d3d72a611541a2ba133cd992496726b4cfda) |
| [XS-100](https://www.extrugasa.com/edificacion/xs-100) | — | 6,7 | ≥ 1,9 | 35 (-2;-5) dB | Clase 3 / 7A / C5 | [PDF](https://www.extrugasa.com/?jet_download=e4b5ae5fa83fad5e89ad8e6bc8ecb1827ff5c631) |
| [XS-110](https://www.extrugasa.com/edificacion/xs-110) | El sistema de ventana corredera con su doble posibilidad de apertura, elevable o en línea, permite dar solución tanto a pequeños huecos como a grandes y pesados ventanales. | 3,6 | ≥ 1,2 | 38 (-1;-3) dB | Clase 3 / 6A / C5 | [PDF](https://www.extrugasa.com/?jet_download=b6507a002f341622ed22f9db1d4eb735addd6be9) |
| [XS-150](https://www.extrugasa.com/edificacion/xs-150) | El sistema de ventana corredera de 150 mm, diseñado para balconeras y con un innovador sistema de cierre, consigue las máximas prestaciones en permeabilidad y estanqueidad. | 3,7 | ≥ 1,0 | 40 (-1;-1) dB | Clase 4 / E1650 / C2 | [PDF](https://www.extrugasa.com/?jet_download=b43bb040955ba2fb539d29cc14d2a12aec764898) |
| [XS-160 HI](https://www.extrugasa.com/edificacion/xs-160-hi) | El sistema XS-160 HI ha sido diseñado para garantizar las máximas prestaciones en los ambientes más severos permitiendo triples acristalamientos. | 2,0 | ≥ 0,9 | 43 (-1;-3) dB | Clase 4 / 8A / C4 | [PDF](https://www.extrugasa.com/?jet_download=d6a8602f4e08ec537bdf84d7d9ceacedc5764692) |
| [G-90](https://www.extrugasa.com/edificacion/g-90) | Sistema corredera en línea sin RPT con corte a 90a que se caracteriza por su adaptación a cualquier solución constructiva planteada. | 6,6 | ≥ 3,18 | 34 (-1;-3) dB | Clase 3 / 5A / C2 | [PDF](https://www.extrugasa.com/?jet_download=82cdd68c480a466a5d8f981d3e9b00ed762c5600) |
| [XS-170](https://www.extrugasa.com/edificacion/xs-170) | — | 2,9 | ≥ 0,8 | 34 (-1;-3) dB | Clase 3 / 9A / C3 | [PDF](https://www.extrugasa.com/?jet_download=69e78ea9adb391d70a7b43388eb0bd2d042cfd02) |
| [Perimetral 70](https://www.extrugasa.com/edificacion/perimetral-70) | Sistema corredera en línea sin RPT y corte a 45 º de montaje y diseño sencillo. | 6,6 | ≥ 2,65 | 42 (-1;-3) dB | Clase 3 / 5A / C2 | [PDF](https://www.extrugasa.com/?jet_download=f999f4be79af08a6066240a142ac01d275d7b27d) |

### Acabados

- [Anodizado natural](https://www.extrugasa.com/acabados/acabado-aluminio-anodizado-natural)
- [Efecto madera embero](https://www.extrugasa.com/acabados/efecto-madera-embero)
- [Efecto madera nogal](https://www.extrugasa.com/acabados/efecto-madera-nogal)
- [Lacado Blanco](https://www.extrugasa.com/acabados/lacado-blanco)
- [Aluminio lacado RAL](https://www.extrugasa.com/acabados/lacado-ral)
- [Lacado textura negro](https://www.extrugasa.com/acabados/lacado-textura-negro)

### Accesorios (manillas)

- [Manilla puerta practicable Essence door](https://www.extrugasa.com/accesorios/accesorio-3)
- [Manilla Essence Square practicable](https://www.extrugasa.com/accesorios/manilla-essence)
- [Manilla Essence Essence Round practicable](https://www.extrugasa.com/accesorios/manilla-essence-2)
- [Manilla correderas Essence acodada](https://www.extrugasa.com/accesorios/manilla-ventana-corredera-1)
- [Manilla correderas Essence con escudo](https://www.extrugasa.com/accesorios/manilla-ventana-corredera-2)

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

**Páginas recuperadas de climalit.es** (31, texto en `raw/climalit/`):

[Climalit®](https://web.archive.org/web/20260522123735id_/https://climalit.es/) · [Productos](https://web.archive.org/web/20260516113117id_/https://climalit.es/productos/) · [Climalit Plus. Un nivel superior de aislamiento térmico](https://web.archive.org/web/20260522123753id_/https://climalit.es/climalit-plus/) · [Climalit Plus®](https://web.archive.org/web/20260516084541id_/https://climalit.es/descubre-climalit-plus/) · [Climalit ORAÉ®](https://web.archive.org/web/20260316083446id_/https://climalit.es/orae/) · [Soluciones vivienda tipo](https://web.archive.org/web/20260516111434id_/https://climalit.es/soluciones-vivienda-tipo/) · [Preguntas frecuentes](https://web.archive.org/web/20260516075906id_/https://climalit.es/preguntas-frecuentes/) · [Huella de carbono](https://web.archive.org/web/20260522123751id_/https://climalit.es/huella-de-carbono/) · [Sostenibilidad](https://web.archive.org/web/20260522123750id_/https://climalit.es/compromiso-climalit/) · [Climalit recicla](https://web.archive.org/web/20260607194713id_/https://climalit.es/climalit-recicla/) · [Cambia tus ventanas con el lider del sector](https://web.archive.org/web/20260607201406id_/https://climalit.es/cambia-tus-ventanas/) · [Climalit Plus®](https://web.archive.org/web/20260522123739id_/https://climalit.es/desarrollo-sostenible/) · [Fabricantes](https://web.archive.org/web/20260607203826id_/https://climalit.es/fabricantes/) · [La instalación de las ventanas también cuenta](https://web.archive.org/web/20260607194936id_/https://climalit.es/instaladores/) · [Acceso auditorio sobre sostenibilidad](https://web.archive.org/web/20260522123735id_/https://climalit.es/sostenibilidad/auditorio/) · [Beneficios de los cristales Climalit Plus](https://web.archive.org/web/20260412231625id_/https://climalit.es/video-sgg/) · [Ponte en contacto con Climalit y garantízate los mejores vidrios](https://web.archive.org/web/20260607194316id_/https://climalit.es/contacto/) · [Descubre nuestras webinars &#8211; Academy](https://web.archive.org/web/20260410222929id_/https://climalit.es/sostenibilidad/descubre-academy/) · [Solicitud Expert](https://web.archive.org/web/20260412232037id_/https://climalit.es/solicitud-expert/) · [Luz sin calor](https://web.archive.org/web/20260412225448id_/https://climalit.es/luz-sin-calor/) · [Aislamiento térmico](https://web.archive.org/web/20260607192404id_/https://climalit.es/aislamiento-termico/) · [Productos](https://web.archive.org/web/20240912103635id_/https://climalit.es/productos/) · [CLIMALIT recicla](https://web.archive.org/web/20260412232223id_/https://www.climalit.es/sostenibilidad/circularidad/climalitrecicla/) · [ICPE Login](https://web.archive.org/web/20260607202231id_/https://climalit.es/icpe-login/) · [Descubre nuestras ventanas sostenibles](https://web.archive.org/web/20260516075151id_/https://climalit.es/sostenibilidad/) · [Interior del auditorio sostenible I Climalit](https://web.archive.org/web/20241006203544id_/https://climalit.es/sostenibilidad/interior-auditorio/) · [Silencio](https://web.archive.org/web/20231202123833id_/https://climalit.es/beneficios/silencio/) · [Aislamiento térmico](https://web.archive.org/web/20231202105609id_/https://climalit.es/beneficios/aislamiento-termico/) · [Ahorro](https://web.archive.org/web/20230605011211id_/https://climalit.es/beneficios/ahorro-2/) · [Seguridad](https://web.archive.org/web/20231202120124id_/https://climalit.es/beneficios/seguridad/) · [Luz sin calor](https://web.archive.org/web/20231202115253id_/https://climalit.es/beneficios/luz-sin-calor/)

**PDFs de climalit.es**

- [sg-triptico-climalit-plus-2021-oct21.pdf](https://web.archive.org/web/2026/https://climalit.es/wp-content/uploads/2021/12/sg-triptico-climalit-plus-2021-oct21.pdf) · —
- [folleto-climalit-2022.pdf](https://web.archive.org/web/2026/https://climalit.es/wp-content/uploads/2022/11/folleto-climalit-2022.pdf) · —
- [triptico-climalit-ecologico-usuario-def_comp.pdf](https://web.archive.org/web/2026/https://climalit.es/wp-content/uploads/2022/11/triptico-climalit-ecologico-usuario-def_comp.pdf) · [PDF local](pdfs/climalit/general/triptico-climalit-ecologico-usuario-def_comp.pdf)
- [triptico-climalit-ecologico-act.pdf](https://web.archive.org/web/2026/https://climalit.es/wp-content/uploads/2023/06/triptico-climalit-ecologico-act.pdf) · —
- [manual-recircula-2025.pdf](https://web.archive.org/web/2026/https://climalit.es/wp-content/uploads/2025/11/manual-recircula-2025.pdf) · —

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

| Producto | Grupo | Documento | Local |
|---|---|---|---|
| [CLIMALIT ORAÉ ®](https://www.saint-gobain-glass.es/es/productos/climalit-orae) | CLIMALIT ORAÉ® (baja huella de carbono) | [catálogo: climalit-orae-2025-1.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/climalit-orae-2025-1.pdf) | [PDF local](pdfs/saint-gobain/productos/Climalit%20ORAE%202025_1.pdf) |
| ″ |  | [ficha técnica: ficha-tcnica-climalit-ecolgico.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-climalit-ecolgico.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20t%C3%A9cnica%20Climalit%20Ecol%C3%B3gico.pdf) |
| [COOL-LITE® SKN ORAÉ®](https://www.saint-gobain-glass.es/es/productos/cool-liter-skn-oraer) | CLIMALIT ORAÉ® (baja huella de carbono) | [catálogo: cool-lite-skn-orae.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/cool-lite-skn-orae.pdf) | [PDF local](pdfs/saint-gobain/productos/COOL-LITE%20SKN%20ORAE.pdf) |
| ″ |  | [guía de transformación: guias-de-transformacion-cool-lite-skn-xtreme.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guias-de-transformacion-cool-lite-skn-xtreme.pdf) | [PDF local](pdfs/saint-gobain/productos/Guias%20de%20Transformacion_COOL%20LITE%20SKN%20XTREME.pdf) |
| [COOL-LITE® XTREME ORAÉ®](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-orae) | CLIMALIT ORAÉ® (baja huella de carbono) | [catálogo: cool-lite-xtreme-orae.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/cool-lite-xtreme-orae.pdf) | [PDF local](pdfs/saint-gobain/productos/COOL-LITE%20XTREME%20ORAE.pdf) |
| ″ |  | [EPD (declaración ambiental): epd-orae-4mm.pdf](https://www.saint-gobain-glass.es/es/documents/dap/epd-orae-4mm.pdf) | [PDF local](pdfs/saint-gobain/productos/EPD%20ORAE%20-%204mm.pdf) |
| ″ |  | [sostenibilidad: declaracin-de-contenido-reciclado-2026-orae.pdf](https://www.saint-gobain-glass.es/es/documents/documentacion-sostenibilidad/declaracin-de-contenido-reciclado-2026-orae.pdf) | [PDF local](pdfs/saint-gobain/productos/Declaraci%C3%B3n%20de%20Contenido%20Reciclado%202026%20ORAE.pdf) |
| ″ |  | [ficha técnica: ficha-tcnica-climalit-ecolgico.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-climalit-ecolgico.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20t%C3%A9cnica%20Climalit%20Ecol%C3%B3gico.pdf) |
| ″ |  | [guía de transformación: guias-de-transformacion-planiclear-orae-diamant-parsol.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guias-de-transformacion-planiclear-orae-diamant-parsol.pdf) | [PDF local](pdfs/saint-gobain/productos/Guias%20de%20Transformacion_PLANICLEAR%2C%20ORAE%2C%20DIAMANT%2C%20PARSOL.pdf) |
| [ECLAZ® ZEN ORAÉ®](https://www.saint-gobain-glass.es/es/productos/eclaz-zen-orae) | CLIMALIT ORAÉ® (baja huella de carbono) | [guía / manual: af-sg-diptico-eclaz-zen-orae-v7.pdf](https://www.saint-gobain-glass.es/es/documents/guias-y-manuales/af-sg-diptico-eclaz-zen-orae-v7.pdf) | [PDF local](pdfs/saint-gobain/productos/AF%20SG%20Diptico%20Eclaz%20Zen%20Orae%20v7.pdf) |
| [PLANISTAR® ONE ORAÉ®](https://www.saint-gobain-glass.es/es/productos/planistar-one-orae) | CLIMALIT ORAÉ® (baja huella de carbono) | [ficha técnica: 6-ora-16-air-6-ora-planistar-one-f2-.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/6-ora-16-air-6-ora-planistar-one-f2-.pdf) | [PDF local](pdfs/saint-gobain/productos/6%20ORA%C3%89%20%2816%20AIR%29%206%20ORA%C3%89_PLANISTAR%20ONE%20F2%20.pdf) |
| ″ |  | [ficha técnica: 6-ora-16-argon-90-6-ora-planistar-one-f2-.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/6-ora-16-argon-90-6-ora-planistar-one-f2-.pdf) | [PDF local](pdfs/saint-gobain/productos/6%20ORA%C3%89%20%2816%20Argon%2090%29%206%20ORA%C3%89_PLANISTAR%20ONE%20F2%20.pdf) |
| [COOL-LITE® XTREME 61/29 Y 61/29 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-6129-y-cool-lite-xtreme-6129-ll) | CLIMALIT® / CLIMALIT PLUS® — vidrio para ventana | [catálogo: separata-cool-lite-xtreme-61-29-ii-def.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/separata-cool-lite-xtreme-61-29-ii-def.pdf) | [PDF local](pdfs/saint-gobain/productos/Separata%20COOL-LITE_XTREME_61_29_II%20def.pdf) |
| ″ |  | [ficha técnica: ficha-tcnica-cool-lite-xtreme-61-29.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-cool-lite-xtreme-61-29.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Cool%20Lite%20Xtreme%2061-29.pdf) |
| [ECLAZ®](https://www.saint-gobain-glass.es/es/productos/eclazr) | CLIMALIT® / CLIMALIT PLUS® — vidrio para ventana | [catálogo: eclaz-hoja.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/eclaz-hoja.pdf) | [PDF local](pdfs/saint-gobain/productos/ECLAZ%20HOJA.pdf) |
| [PLANISTAR® ONE](https://www.saint-gobain-glass.es/es/productos/planistar-one) | CLIMALIT® / CLIMALIT PLUS® — vidrio para ventana | [catálogo: diptico-planistar-one.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-planistar-one.pdf) | [PDF local](pdfs/saint-gobain/productos/Diptico%20PLANISTAR%20ONE.pdf) |
| ″ |  | [ficha técnica: 6-ora-16-air-6-ora-planistar-one-f2-.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/6-ora-16-air-6-ora-planistar-one-f2-.pdf) | [PDF local](pdfs/saint-gobain/productos/6%20ORA%C3%89%20%2816%20AIR%29%206%20ORA%C3%89_PLANISTAR%20ONE%20F2%20.pdf) |
| ″ |  | [guía de transformación: guas-de-transformacion-planitherm-planistar.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guas-de-transformacion-planitherm-planistar.pdf) | [PDF local](pdfs/saint-gobain/productos/Gu%C3%ADas%20de%20Transformacion_PLANITHERM%20%26%20PLANISTAR.pdf) |
| [PLANITHERM® 4S](https://www.saint-gobain-glass.es/es/productos/planitherm-4s) | CLIMALIT® / CLIMALIT PLUS® — vidrio para ventana | [catálogo: diptico-planitherm-4s.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-planitherm-4s.pdf) | [PDF local](pdfs/saint-gobain/productos/Diptico%20PLANITHERM%204S.pdf) |
| ″ |  | [ficha técnica: ficha-tcnica-planitherm-4s-3.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-planitherm-4s-3.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Planitherm%204S%20%283%29.pdf) |
| ″ |  | [guía de transformación: guas-de-transformacion-planitherm-planistar.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guas-de-transformacion-planitherm-planistar.pdf) | [PDF local](pdfs/saint-gobain/productos/Gu%C3%ADas%20de%20Transformacion_PLANITHERM%20%26%20PLANISTAR.pdf) |
| [PLANITHERM® XN](https://www.saint-gobain-glass.es/es/productos/planitherm-xn) | CLIMALIT® / CLIMALIT PLUS® — vidrio para ventana | [catálogo: diptico-planitherm-xn.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-planitherm-xn.pdf) | [PDF local](pdfs/saint-gobain/productos/Diptico%20PLANITHERM%20XN.pdf) |
| ″ |  | [ficha técnica: ficha-tcnica-planitherm-xn.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-planitherm-xn.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Planitherm%20XN.pdf) |
| ″ |  | [guía de transformación: guas-de-transformacion-planitherm-planistar.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guas-de-transformacion-planitherm-planistar.pdf) | [PDF local](pdfs/saint-gobain/productos/Gu%C3%ADas%20de%20Transformacion_PLANITHERM%20%26%20PLANISTAR.pdf) |
| [COOL-LITE® K](https://www.saint-gobain-glass.es/es/productos/cool-liter-k) | Control solar para muro cortina / no residencial | [guía de transformación: guas-de-transformacion-cool-lite-k.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guas-de-transformacion-cool-lite-k.pdf) | [PDF local](pdfs/saint-gobain/productos/Gu%C3%ADas%20de%20Transformacion_COOL-LITE%20K.pdf) |
| [COOL-LITE® SKN](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn) | Control solar para muro cortina / no residencial | [catálogo: cool-lite-skn-orae.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/cool-lite-skn-orae.pdf) | [PDF local](pdfs/saint-gobain/productos/COOL-LITE%20SKN%20ORAE.pdf) |
| ″ |  | [guía de transformación: guias-de-transformacion-cool-lite-skn-xtreme.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guias-de-transformacion-cool-lite-skn-xtreme.pdf) | [PDF local](pdfs/saint-gobain/productos/Guias%20de%20Transformacion_COOL%20LITE%20SKN%20XTREME.pdf) |
| [COOL-LITE® SKN 144 ll](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-144-ll) | Control solar para muro cortina / no residencial | [ficha técnica: ficha-tcnica-cool-lite-skn-144-ii.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-cool-lite-skn-144-ii.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Cool-Lite%20SKN%20144%20II.pdf) |
| [COOL-LITE® SKN 155/155 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-155-cool-lite-skn-155-II) | Control solar para muro cortina / no residencial | [catálogo: cool-lite-skn-orae.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/cool-lite-skn-orae.pdf) | [PDF local](pdfs/saint-gobain/productos/COOL-LITE%20SKN%20ORAE.pdf) |
| ″ |  | [guía / manual: lo-esencial-2026.pdf](https://www.saint-gobain-glass.es/es/documents/guias-y-manuales/lo-esencial-2026.pdf) | [PDF local](pdfs/saint-gobain/productos/Lo%20Esencial%202026.pdf) |
| [COOL-LITE® SKN 165/165 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-165-y-cool-lite-skn-165-II) | Control solar para muro cortina / no residencial | [ficha técnica: ficha-tcnica-cool-lite-skn-165.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-cool-lite-skn-165.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Cool%20Lite%20SKN%20165.pdf) |
| [COOL-LITE® SKN 176/176 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-176-y-cool-lite-skn-176-II) | Control solar para muro cortina / no residencial | [ficha técnica: ficha-tcnica-cool-lite-skn-176.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-cool-lite-skn-176.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Cool-Lite%20SKN%20176.pdf) |
| [COOL-LITE® SKN 183/183 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-skn-183-y-cool-lite-skn-183-II) | Control solar para muro cortina / no residencial | [catálogo: cool-lite-skn-183ii-ok.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/cool-lite-skn-183ii-ok.pdf) | [PDF local](pdfs/saint-gobain/productos/COOL-LITE-SKN-183II-OK.pdf) |
| ″ |  | [ficha técnica: ficha-tcnica-cool-lite-skn-183.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-cool-lite-skn-183.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Cool-Lite%20SKN%20183.pdf) |
| [COOL-LITE® ST - COOL-LITE® STB](https://www.saint-gobain-glass.es/es/productos/cool-lite-st-y-cool-lite-stb) | Control solar para muro cortina / no residencial | [guía de transformación: guas-de-transformacion-cool-lite-st.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guas-de-transformacion-cool-lite-st.pdf) | [PDF local](pdfs/saint-gobain/productos/Gu%C3%ADas%20de%20Transformacion_COOL-LITE%20ST.pdf) |
| [COOL-LITE® XTREME](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme) | Control solar para muro cortina / no residencial | [guía de transformación: guias-de-transformacion-cool-lite-skn-xtreme.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guias-de-transformacion-cool-lite-skn-xtreme.pdf) | [PDF local](pdfs/saint-gobain/productos/Guias%20de%20Transformacion_COOL%20LITE%20SKN%20XTREME.pdf) |
| [COOL-LITE® XTREME 51/23 & 51/23 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-51/23%20%26%2051/23-ll) | Control solar para muro cortina / no residencial | [ficha técnica: cool-lite-xtreme-orae-product-datasheet-esp-2025.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/cool-lite-xtreme-orae-product-datasheet-esp-2025.pdf) | [PDF local](pdfs/saint-gobain/productos/COOL-LITE%20XTREME%20ORAE%20Product%20Datasheet%20ESP%202025.pdf) |
| [COOL-LITE® XTREME 70/33 Y 70/33 II](https://www.saint-gobain-glass.es/es/productos/cool-lite-xtreme-7033-y-7033-ll) | Control solar para muro cortina / no residencial | [ficha técnica: ficha-tcnica-cool-lite-xtreme-70-33.pdf](https://www.saint-gobain-glass.es/es/documents/ficha-tecnica-calumen/ficha-tcnica-cool-lite-xtreme-70-33.pdf) | [PDF local](pdfs/saint-gobain/productos/Ficha%20T%C3%A9cnica%20Cool%20Lite%20Xtreme%2070-33.pdf) |
| [STADIP® & STADIP® SILENCE](https://www.saint-gobain-glass.es/es/productos/stadip-stadip-silence) | Seguridad y acústica | [catálogo: diptico-stadip-silence.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/diptico-stadip-silence.pdf) | [PDF local](pdfs/saint-gobain/productos/Diptico%20STADIP%20SILENCE.pdf) |
| ″ |  | [guía de transformación: guas-de-transformacion-stadip.pdf](https://www.saint-gobain-glass.es/es/documents/guias-de-transformacion/guas-de-transformacion-stadip.pdf) | [PDF local](pdfs/saint-gobain/productos/Gu%C3%ADas%20de%20Transformacion_STADIP.pdf) |
| [4BIRD®](https://www.saint-gobain-glass.es/es/productos/4birdr) | Vidrios especiales | sin PDFs en la web | — |
| [PRIVA-LITE®](https://www.saint-gobain-glass.es/es/productos/priva-liter) | Vidrios especiales | sin PDFs en la web | — |
| [SAGEGLASS®](https://www.saint-gobain-glass.es/es/productos/sageglassr) | Vidrios especiales | [catálogo: comfort-and-sustainability-with-sageglass-mkt-096.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/comfort-and-sustainability-with-sageglass-mkt-096.pdf) | [PDF local](pdfs/saint-gobain/productos/comfort_and_sustainability_with_sageglass_mkt_096.pdf) |
| [VISION-LITE®](https://www.saint-gobain-glass.es/es/productos/vision-liter) | Vidrios especiales | sin PDFs en la web | — |
| [DECORGLASS® Y MASTERGLASS®](https://www.saint-gobain-glass.es/es/productos/decorglass-y-masterglass) | Interiorismo y decoración | [certificado: decorglass-masterglass.pdf](https://www.saint-gobain-glass.es/es/documents/certificado-saint-gobain-glass/decorglass-masterglass.pdf) | [PDF local](pdfs/saint-gobain/productos/DECORGLASS%20%26%20MASTERGLASS.pdf) |
| [MASTER-SOFT®](https://www.saint-gobain-glass.es/es/productos/master-soft) | Interiorismo y decoración | sin PDFs en la web | — |
| [MIRALITE® PURE](https://www.saint-gobain-glass.es/es/productos/miralite-pure) | Interiorismo y decoración | [catálogo: colas-y-cintas-miralite-pure-2026-marzo.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/colas-y-cintas-miralite-pure-2026-marzo.pdf) | [PDF local](pdfs/saint-gobain/productos/Colas%20y%20cintas%20Miralite%20Pure%202026%20Marzo.pdf) |
| [MIRASTAR®](https://www.saint-gobain-glass.es/es/productos/mirastar) | Interiorismo y decoración | sin PDFs en la web | — |
| [PLANILAQUE® EVOLUTION](https://www.saint-gobain-glass.es/es/productos/planilaquer-evolution) | Interiorismo y decoración | [catálogo: hoja-planilaque-evolution-2018-4.pdf](https://www.saint-gobain-glass.es/es/documents/catalogo-de-producto/hoja-planilaque-evolution-2018-4.pdf) | [PDF local](pdfs/saint-gobain/productos/Hoja%20Planilaque%20Evolution%202018%204.pdf) |

Otros documentos (páginas de soluciones):

- [folleto-climalit.pdf](https://www.saint-gobain-glass.es/es/documents/guias-y-manuales/folleto-climalit.pdf) (SOLUCIONES DE CONTROL SOLAR Y BAJA EMISIVIDAD) · [PDF local](pdfs/saint-gobain/soluciones/Folleto%20Climalit.pdf)
- [folleto-climalit.pdf](https://www.saint-gobain-glass.es/es/documents/guias-y-manuales/folleto-climalit.pdf) (SOLUCIONES DE BAJA EMISIVIDAD) · [PDF local](pdfs/saint-gobain/soluciones/Folleto%20Climalit.pdf)
