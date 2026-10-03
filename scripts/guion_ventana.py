"""Genera el guion «A través de la ventana» como diapositivas del tipo Slides (project/…)."""
import json, pathlib

R = pathlib.Path(__file__).parent
S = R / "project" / "slides"; S.mkdir(parents=True, exist_ok=True)

SANS = "font-family:'IBM Plex Sans', Arial, sans-serif"
DISP = "font-family:'Archivo', Arial, sans-serif"
MONO = "font-family:'IBM Plex Mono', 'Courier New', monospace"
INK, MUTED, VT, LINE, TINTE, BG, DARK = "#141815", "#545e58", "#256a31", "#d6dbd7", "#e3f3e6", "#f5f6f4", "#0f1211"

FOTOS = {"chalet": "/_blob/d9c3c3cc4081e7cd9de660b0c51317ac", "nave": "/_blob/aaa582e1cf1a05bffef26fe5c22442e4",
         "pabellon": "/_blob/ff19d2c74664d6492a60232c192eaf84", "porche": "/_blob/8c0addad6ccf7635e354d97c562c28c3"}

ORDER = ["portada", "idea", "tramo1", "tramo2", "tramo3", "tramo4", "tramo5", "tramo6", "estilo", "falta", "siguiente"]
TRAMOS = [("Fuera, al anochecer", "0–15 %"), ("La ventana se abre", "15–30 %"), ("Dentro: el taller", "30–48 %"),
          ("El banco de trabajo", "48–62 %"), ("Ventanas a nuestras obras", "62–80 %"), ("Salida al valle", "80–100 %")]

# ── Viñetas en SVG (estilo maqueta; sin texto dentro) ─────────────────────────────────────────
SVG = {}
SVG[1] = '''<svg aria-label="Casa del valle en maqueta al anochecer, con una ventana encendida y la ruta de la cámara hacia ella" width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16222b"/><stop offset="1" stop-color="#3d4a52"/></linearGradient>
<radialGradient id="brillo"><stop offset="0" stop-color="#f3d9a0" stop-opacity="0.6"/><stop offset="1" stop-color="#f3d9a0" stop-opacity="0"/></radialGradient>
<marker id="p" orient="auto" markerWidth="6" markerHeight="6" refX="3" refY="3"><path d="M0 0 L6 3 L0 6 Z" fill="#4ba939"/></marker></defs>
<rect width="900" height="560" fill="url(#cielo)"/>
<circle cx="120" cy="70" r="1.8" fill="#ffffff" opacity="0.7"/><circle cx="260" cy="40" r="1.4" fill="#ffffff" opacity="0.6"/><circle cx="700" cy="60" r="1.6" fill="#ffffff" opacity="0.7"/><circle cx="820" cy="120" r="1.2" fill="#ffffff" opacity="0.5"/><circle cx="420" cy="90" r="1.2" fill="#ffffff" opacity="0.5"/>
<path d="M0 360 C 150 300 300 340 450 300 S 760 280 900 330 L900 560 L0 560 Z" fill="#26332e"/>
<path d="M0 430 C 220 390 420 430 620 400 S 820 390 900 410 L900 560 L0 560 Z" fill="#1e2925"/>
<rect x="0" y="458" width="900" height="102" fill="#1a221f"/>
<polygon points="630,250 720,214 720,424 630,460" fill="#a69e90"/>
<rect x="330" y="250" width="300" height="210" fill="#c9c0b1"/>
<polygon points="314,254 480,168 646,254" fill="#3b4148"/>
<polygon points="480,168 570,132 736,216 646,254" fill="#2f343a"/>
<rect x="362" y="296" width="62" height="82" fill="#2a3238" stroke="#e9ece9" stroke-width="5"/>
<rect x="436" y="370" width="50" height="90" fill="#6b3f24"/>
<circle cx="556" cy="334" r="110" fill="url(#brillo)"/>
<rect x="520" y="288" width="72" height="92" fill="#f3d9a0" stroke="#f5f6f4" stroke-width="6"/>
<line x1="556" y1="291" x2="556" y2="377" stroke="#f5f6f4" stroke-width="3"/>
<path d="M90 540 C 220 520 380 470 545 352" fill="none" stroke="#4ba939" stroke-width="4" stroke-dasharray="14 10" marker-end="url(#p)"/>
<circle cx="90" cy="540" r="9" fill="#4ba939"/>
</svg>'''

SVG[2] = '''<svg aria-label="Ventana de PVC abriéndose en oscilobatiente con luz detrás, y un esquema del corte de un perfil multicámara" width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="dentro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d9a0"/><stop offset="1" stop-color="#d49a57"/></linearGradient></defs>
<rect width="900" height="560" fill="#24201d"/>
<rect x="190" y="50" width="400" height="460" fill="url(#dentro)"/>
<rect x="176" y="36" width="428" height="488" fill="none" stroke="#eef0ee" stroke-width="28"/>
<polygon points="166,120 614,120 590,510 190,510" fill="#dfeee5" fill-opacity="0.22" stroke="#f5f6f4" stroke-width="16" stroke-linejoin="round"/>
<line x1="176" y1="524" x2="604" y2="524" stroke="#4ba939" stroke-width="10"/>
<path d="M604 300 L 652 300" stroke="#87d2a9" stroke-width="3" stroke-dasharray="8 6"/>
<rect x="652" y="150" width="228" height="290" fill="#f5f6f4" stroke="#545e58" stroke-width="2"/>
<rect x="732" y="164" width="7" height="44" fill="#87d2a9"/><rect x="772" y="164" width="7" height="44" fill="#87d2a9"/>
<rect x="690" y="206" width="152" height="170" fill="#fbfbf8" stroke="#141815" stroke-width="4"/>
<line x1="722" y1="206" x2="722" y2="376" stroke="#141815" stroke-width="3"/>
<line x1="766" y1="206" x2="766" y2="376" stroke="#141815" stroke-width="3"/>
<line x1="810" y1="206" x2="810" y2="376" stroke="#141815" stroke-width="3"/>
<line x1="722" y1="262" x2="810" y2="262" stroke="#141815" stroke-width="3"/>
<line x1="722" y1="320" x2="810" y2="320" stroke="#141815" stroke-width="3"/>
<rect x="730" y="272" width="72" height="40" fill="#9a9fa3"/>
<line x1="690" y1="408" x2="842" y2="408" stroke="#256a31" stroke-width="3"/>
<line x1="690" y1="396" x2="690" y2="420" stroke="#256a31" stroke-width="3"/><line x1="842" y1="396" x2="842" y2="420" stroke="#256a31" stroke-width="3"/>
</svg>'''

SVG[3] = '''<svg aria-label="Interior de la nave del taller en perspectiva, con pilares y vigas de acero, un punto de soldadura con chispas y el nudo del logo marcado en verde" width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="chispa"><stop offset="0" stop-color="#ffffff"/><stop offset="0.2" stop-color="#f2a33a" stop-opacity="0.8"/><stop offset="1" stop-color="#f2a33a" stop-opacity="0"/></radialGradient>
<marker id="p3" orient="auto" markerWidth="6" markerHeight="6" refX="3" refY="3"><path d="M0 0 L6 3 L0 6 Z" fill="#4ba939"/></marker></defs>
<polygon points="0,0 900,0 700,120 340,120" fill="#b9bec0"/>
<polygon points="0,0 340,120 340,330 0,560" fill="#cfd3d0"/>
<polygon points="900,0 700,120 700,330 900,560" fill="#c4c9c6"/>
<rect x="340" y="120" width="360" height="210" fill="#e9ece9"/>
<polygon points="0,560 900,560 700,330 340,330" fill="#d9d4ca"/>
<rect x="470" y="170" width="120" height="80" fill="#1b1f22" stroke="#f5f6f4" stroke-width="5"/>
<circle cx="510" cy="225" r="26" fill="url(#chispa)"/>
<line x1="85" y1="44" x2="815" y2="44" stroke="#2a2f33" stroke-width="26"/>
<line x1="210" y1="96" x2="690" y2="96" stroke="#2a2f33" stroke-width="16"/>
<line x1="300" y1="130" x2="600" y2="130" stroke="#2a2f33" stroke-width="9"/>
<rect x="66" y="30" width="38" height="520" fill="#2a2f33"/><rect x="81" y="30" width="8" height="520" fill="#9a9fa3"/>
<rect x="198" y="88" width="24" height="360" fill="#2a2f33"/><rect x="207" y="88" width="6" height="360" fill="#9a9fa3"/>
<rect x="796" y="30" width="38" height="520" fill="#2a2f33"/><rect x="811" y="30" width="8" height="520" fill="#9a9fa3"/>
<rect x="678" y="88" width="24" height="360" fill="#2a2f33"/><rect x="687" y="88" width="6" height="360" fill="#9a9fa3"/>
<circle cx="812" cy="48" r="52" fill="none" stroke="#4ba939" stroke-width="4" stroke-dasharray="10 7"/>
<circle cx="262" cy="470" r="70" fill="url(#chispa)"/>
<line x1="262" y1="470" x2="226" y2="430" stroke="#f2a33a" stroke-width="2"/><line x1="262" y1="470" x2="300" y2="436" stroke="#f2a33a" stroke-width="2"/><line x1="262" y1="470" x2="240" y2="420" stroke="#f2a33a" stroke-width="2"/><line x1="262" y1="470" x2="318" y2="452" stroke="#f2a33a" stroke-width="2"/>
<path d="M450 556 C 470 470 560 330 760 120" fill="none" stroke="#4ba939" stroke-width="4" stroke-dasharray="14 10" marker-end="url(#p3)"/>
</svg>'''

SVG[4] = '''<svg aria-label="Banco de trabajo de castaño con cuatro piezas en corte: viga de hierro, perfil de aluminio con rotura de puente térmico, perfil de PVC multicámara y doble acristalamiento" width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg">
<rect width="900" height="560" fill="#e9ece9"/>
<polygon points="90,0 170,0 230,330 30,330" fill="#ffffff" opacity="0.35"/>
<polygon points="290,0 370,0 430,330 230,330" fill="#ffffff" opacity="0.35"/>
<polygon points="480,0 560,0 640,330 420,330" fill="#ffffff" opacity="0.75"/>
<polygon points="690,0 770,0 820,330 640,330" fill="#ffffff" opacity="0.35"/>
<polygon points="60,330 840,330 900,470 0,470" fill="#6b3f24"/>
<rect x="0" y="470" width="900" height="40" fill="#55321d"/>
<rect x="40" y="510" width="34" height="50" fill="#3d2414"/><rect x="826" y="510" width="34" height="50" fill="#3d2414"/>
<rect x="84" y="216" width="104" height="16" fill="#2a2f33"/><rect x="131" y="232" width="10" height="78" fill="#9a9fa3"/><rect x="84" y="310" width="104" height="16" fill="#2a2f33"/>
<rect x="284" y="226" width="104" height="98" fill="none" stroke="#8d9296" stroke-width="7"/>
<rect x="328" y="226" width="16" height="98" fill="#141815"/>
<line x1="284" y1="262" x2="328" y2="262" stroke="#8d9296" stroke-width="4"/><line x1="344" y1="290" x2="388" y2="290" stroke="#8d9296" stroke-width="4"/>
<rect x="476" y="214" width="120" height="110" fill="#fbfbf8" stroke="#545e58" stroke-width="4"/>
<line x1="506" y1="214" x2="506" y2="324" stroke="#545e58" stroke-width="3"/><line x1="566" y1="214" x2="566" y2="324" stroke="#545e58" stroke-width="3"/>
<line x1="506" y1="252" x2="566" y2="252" stroke="#545e58" stroke-width="3"/><line x1="506" y1="292" x2="566" y2="292" stroke="#545e58" stroke-width="3"/>
<rect x="512" y="258" width="48" height="28" fill="#9a9fa3"/>
<line x1="476" y1="340" x2="596" y2="340" stroke="#4ba939" stroke-width="6"/>
<rect x="700" y="196" width="8" height="128" fill="#87d2a9"/><rect x="734" y="196" width="8" height="128" fill="#87d2a9"/>
<rect x="708" y="306" width="26" height="14" fill="#9a9fa3"/><rect x="708" y="320" width="26" height="4" fill="#26292c"/>
</svg>'''

SVG[6] = '''<svg aria-label="Puerta plegable abierta al fondo del taller; fuera amanece sobre las lomas del Valle del Ambroz, con Hervás marcado en verde y la carretera" width="900" height="560" viewBox="0 0 900 560" xmlns="http://www.w3.org/2000/svg">
<defs><linearGradient id="alba" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb4c9"/><stop offset="0.75" stop-color="#f6d9a8"/></linearGradient></defs>
<rect width="900" height="560" fill="#2f343a"/>
<rect x="120" y="60" width="660" height="440" fill="url(#alba)"/>
<path d="M120 300 C 260 250 380 290 520 250 S 700 230 780 260 L780 500 L120 500 Z" fill="#8a9a8f"/>
<path d="M120 360 C 300 320 420 350 560 320 S 720 320 780 330 L780 500 L120 500 Z" fill="#6f8676"/>
<path d="M120 430 C 300 400 480 430 780 410 L780 500 L120 500 Z" fill="#4f6a58"/>
<rect x="452" y="322" width="12" height="10" fill="#e9e3d6"/><rect x="468" y="318" width="14" height="14" fill="#e9e3d6"/><rect x="486" y="324" width="10" height="8" fill="#e9e3d6"/><rect x="440" y="326" width="10" height="8" fill="#e9e3d6"/>
<circle cx="470" cy="296" r="22" fill="none" stroke="#4ba939" stroke-width="4"/><circle cx="470" cy="296" r="9" fill="#4ba939"/>
<path d="M140 492 C 260 460 330 420 400 380 S 520 340 620 300" fill="none" stroke="#fbfbf8" stroke-width="3" stroke-dasharray="10 8" opacity="0.8"/>
<polygon points="668,60 706,70 706,490 668,500" fill="#dfeee5" fill-opacity="0.35" stroke="#f5f6f4" stroke-width="7"/>
<polygon points="706,70 742,60 742,500 706,490" fill="#dfeee5" fill-opacity="0.35" stroke="#f5f6f4" stroke-width="7"/>
<polygon points="742,60 780,70 780,490 742,500" fill="#dfeee5" fill-opacity="0.35" stroke="#f5f6f4" stroke-width="7"/>
<rect x="110" y="50" width="680" height="460" fill="none" stroke="#eef0ee" stroke-width="16"/>
<polygon points="120,500 780,500 900,560 0,560" fill="#f6d9a8" opacity="0.35"/>
</svg>'''

COVER_SVG = '''<svg aria-label="Ventana abriéndose con luz cálida detrás, sobre fondo oscuro" width="720" height="824" viewBox="0 0 720 824" xmlns="http://www.w3.org/2000/svg">
<defs><radialGradient id="g" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#f6d79a" stop-opacity="0.5"/><stop offset="1" stop-color="#f6d79a" stop-opacity="0"/></radialGradient>
<linearGradient id="luz" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3d9a0"/><stop offset="1" stop-color="#c98f4a"/></linearGradient></defs>
<ellipse cx="360" cy="400" rx="360" ry="400" fill="url(#g)"/>
<polygon points="163,722 557,722 700,824 20,824" fill="#f6d79a" opacity="0.16"/>
<rect x="163" y="153" width="394" height="534" fill="url(#luz)"/>
<rect x="150" y="140" width="420" height="560" fill="none" stroke="#e9ece9" stroke-width="26"/>
<polygon points="163,153 336,206 336,634 163,687" fill="#dfeee5" fill-opacity="0.28" stroke="#f5f6f4" stroke-width="18" stroke-linejoin="round"/>
<rect x="128" y="700" width="464" height="22" fill="#4ba939"/>
</svg>'''

def nota(t): return f"<aside>{t}</aside>"

def pie(n):
    barras = "".join(f'<div style="width:72px;height:8px;background:{"#4ba939" if i == n else LINE}"></div>' for i in range(1, 7))
    return (f'<div style="position:absolute;left:128px;bottom:64px;width:1664px;display:flex;flex-direction:row;align-items:center;gap:12px">'
            f'{barras}<p style="font-size:24px;color:{MUTED};{MONO}">Tramo {n} de 6 · {TRAMOS[n-1][0]}</p></div>')

def bloque(etq, txt):
    return (f'<div style="display:flex;flex-direction:column;gap:6px;border-top:1px solid {LINE};padding:16px 0 0 0">'
            f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{MUTED}">{etq}</p>'
            f'<p style="font-size:26px;line-height:1.4">{txt}</p></div>')

def tramo(n, visual, se_ve, al_bajar, pantalla, caja_t, caja, notas):
    titulo, rango = TRAMOS[n - 1]
    return (f'<section id="tramo{n}" data-transition="fade" style="background:{BG};color:{INK};{SANS};padding:128px 128px 160px;display:flex;flex-direction:row;gap:64px;align-items:flex-start">'
            f'<div style="width:900px;display:flex;flex-direction:column;gap:24px">{visual}'
            f'<div style="background:{TINTE};padding:20px 28px;display:flex;flex-direction:column;gap:4px">'
            f'<p style="font-size:24px;font-weight:600;color:{VT}">{caja_t}</p><p style="font-size:26px;line-height:1.35">{caja}</p></div></div>'
            f'<div style="flex:1;display:flex;flex-direction:column;gap:24px">'
            f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{VT}">Tramo {n} · {rango} del recorrido</p>'
            f'<h2 style="{DISP};font-size:60px;font-weight:800;line-height:1.05">{titulo}</h2>'
            f'{bloque("Se ve", se_ve)}{bloque("Al bajar", al_bajar)}{bloque("En pantalla", pantalla)}</div>'
            f'{pie(n)}{nota(notas)}</section>')

slides = {}
slides["portada"] = (
    f'<section id="portada" data-transition="fade" style="background:{DARK};color:#eef1ee;{SANS};padding:128px;display:flex;flex-direction:row;gap:64px;align-items:center">'
    f'<div style="flex:1;display:flex;flex-direction:column;gap:32px">'
    f'<p style="font-size:24px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#4ba939">Metal Hervás · Página inicial</p>'
    f'<h1 style="{DISP};font-size:120px;font-weight:800;line-height:0.98">A través de la ventana</h1>'
    f'<p style="font-size:36px;line-height:1.4;color:#a3ada7">Guion de la web animada: entras por una ventana a nuestro taller y sales por otra al Valle del Ambroz.</p></div>'
    f'{COVER_SVG}{nota("Guion para validar antes de programar. Seis tramos de un solo recorrido de cámara; el scroll mueve la cámara.")}</section>')

tarjetas = "".join(
    f'<div style="display:flex;flex-direction:column;gap:10px;border-top:6px solid {"#4ba939" if i in (0, 5) else "#87d2a9"};padding:20px 0 0 0">'
    f'<p style="{MONO};font-size:28px;color:{VT}">{i + 1:02d}</p>'
    f'<h3 style="{DISP};font-size:32px;font-weight:800;line-height:1.15">{t}</h3>'
    f'<p style="font-size:24px;color:{MUTED}">{r}</p></div>'
    for i, (t, r) in enumerate(TRAMOS))
slides["idea"] = (
    f'<section id="idea" data-transition="fade" style="background:{BG};color:{INK};{SANS};padding:128px;display:flex;flex-direction:column;gap:56px">'
    f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{VT}">La idea</p>'
    f'<h2 style="{DISP};font-size:72px;font-weight:800;line-height:1.05">Una sola animación, de la calle al valle</h2>'
    f'<p style="font-size:32px;line-height:1.45;color:{MUTED};width:1300px">La web es un recorrido continuo. Al bajar, la cámara avanza: cada tramo del recorrido es una parte de la página, y la ventana, que es lo que fabricáis, hace de puerta de entrada y de salida.</p>'
    f'<div style="display:grid;grid-template-columns:repeat(6, 1fr);gap:24px">{tarjetas}</div>'
    f'{nota("Los porcentajes son la parte del scroll que ocupa cada tramo. Todos los textos de la página siguen siendo HTML real, para Google y para quien no pueda ver la animación.")}</section>')

slides["tramo1"] = tramo(1, SVG[1],
    "Una casa del valle en maqueta, de noche, con una sola ventana encendida. Encima, el titular y los botones.",
    "La cámara avanza despacio hacia la ventana encendida; el resto de la casa se queda atrás.",
    "Hierro, aluminio y PVC · Llamar al 664 40 96 18 · Pedir presupuesto",
    "Hace falta", "Las medidas de una ventana tipo que fabriquéis, para que el hueco sea real.",
    "Es lo primero que se ve: tiene que leerse y poder llamar sin bajar nada.")
slides["tramo2"] = tramo(2, SVG[2],
    "La hoja se abre en oscilobatiente: primero bascula y luego gira. Al cruzar el marco se ve el corte del perfil.",
    "Pasamos por la ventana. El corte enseña las cámaras del perfil y el refuerzo de acero.",
    "Fabricamos nuestras ventanas de PVC · GEALAN S 9000 · 82,5 mm · Uf ≤ 0,89 W/(m²K)",
    "Hace falta", "El plano de sección del S 9000. El dibujo de la izquierda es un esquema, no el perfil real.",
    "El momento protagonista. El perfil se modela con el plano de GEALAN; sin él, no se enseña el corte.")
slides["tramo3"] = tramo(3, SVG[3],
    "Una nave con pilares y vigas IPE. La cámara pasa bajo un nudo con la misma perspectiva que la viga del logo.",
    "En un puesto saltan chispas, y en una ventana del fondo se ve vuestro vídeo real de soldadura.",
    "Naves y estructuras metálicas · Medimos, fabricamos en Hervás y montamos",
    "Ya lo tenemos", "El nudo 3D de los prototipos, con medidas IPE 300 reales, y el vídeo de soldadura nocturna.",
    "Aquí se reutiliza el nudo que ya validasteis en Acero.")
slides["tramo4"] = tramo(4, SVG[4],
    "Sobre un banco de castaño, cuatro piezas en corte: viga de hierro, aluminio con rotura de puente térmico, PVC y vidrio.",
    "Cada pieza se ilumina cuando aparece su texto, con una cifra real del fabricante.",
    "Hierro · Aluminio · PVC · Vidrio Climalit · Ver todos los productos",
    "Hace falta", "El corte de una serie de aluminio de Aluval o Extrugasa. Hasta tenerlo, esa pieza no se modela.",
    "Sustituye a la sección Qué hacemos y adelanta la página de productos.")
fotos = "".join(
    f'<div style="border:16px solid #fbfbf8;box-shadow:inset 0 0 0 2px #c9c0b1;overflow:hidden;display:flex"><img src="{FOTOS[k]}" alt="{a}" style="width:364px;height:194px;object-fit:cover"></div>'
    for k, a in [("chalet", "Fachada de chalet con carpintería exterior"), ("nave", "Nave metálica terminada"),
                 ("pabellon", "Pabellón acristalado con perfilería negra"), ("porche", "Porche con puertas plegables de vidrio")])
pared = f'<div style="width:900px;height:560px;background:#c9c0b1;padding:36px;display:grid;grid-template-columns:repeat(2, 1fr);grid-template-rows:226px 226px;gap:36px">{fotos}</div>'
slides["tramo5"] = tramo(5, pared,
    "Una pared con una fila de ventanas. A través de cada una se ve una obra real, no un dibujo.",
    "La cámara pasa de ventana en ventana; cada obra lleva su pie de foto.",
    "Obra hecha · el tipo de trabajo de cada foto · Ver todos los trabajos",
    "Hace falta", "Elegir 6 obras y tener el permiso de sus dueños para publicarlas.",
    "Las fotos se pueden mejorar con Google Flow, sin tocar el producto.")
slides["tramo6"] = tramo(6, SVG[6],
    "Al fondo del taller se abre una puerta plegable. Fuera amanece sobre el Valle del Ambroz, con Hervás marcado.",
    "La cámara sale y se queda mirando el valle. Ahí aparece el contacto.",
    "Pásate por el taller · 664 40 96 18 · 927 47 36 19 · Formulario de presupuesto",
    "No hace falta nada", "El valle es un esquema en maqueta, no una foto ni un mapa exacto.",
    "Cierra el recorrido con la misma idea: otra ventana, ahora hacia fuera.")

def tarjeta(titulo, cuerpo, extra):
    return (f'<div style="flex:1;background:#ffffff;border:1px solid {LINE};padding:40px;display:flex;flex-direction:column;gap:20px">'
            f'{extra}<h3 style="{DISP};font-size:40px;font-weight:800;line-height:1.1">{titulo}</h3>'
            f'<p style="font-size:28px;line-height:1.45;color:{MUTED}">{cuerpo}</p></div>')
muestras = "".join(f'<div style="flex:1;height:72px;background:{c}"></div>' for c in ["#c9c0b1", "#3b4148", "#9a9fa3", "#26292c", "#4ba939"])
luz = '<div style="height:72px;background:linear-gradient(90deg, #16222b 0%, #f3d9a0 55%, #8fb4c9 100%)"></div>'
foto = f'<img src="{FOTOS["nave"]}" alt="Nave metálica terminada, una de las fotos reales de obra" style="width:453px;height:72px;object-fit:cover">'
slides["estilo"] = (
    f'<section id="estilo" data-transition="fade" style="background:{BG};color:{INK};{SANS};padding:128px;display:flex;flex-direction:column;gap:56px">'
    f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{VT}">Cómo se ve</p>'
    f'<h2 style="{DISP};font-size:72px;font-weight:800;line-height:1.05">Una maqueta de arquitectura, no una foto</h2>'
    f'<div style="display:flex;gap:32px">'
    f'{tarjeta("Volúmenes limpios", "Piedra, pizarra y acero, con el verde de la marca como acento. Sin texturas falsas: así pesa poco en el móvil.", f"<div style=\"display:flex\">{muestras}</div>")}'
    f'{tarjeta("La luz cuenta la historia", "Fuera anochece, dentro está la luz del taller y al salir amanece sobre el valle.", luz)}'
    f'{tarjeta("Lo real, dentro", "Fotos de vuestras obras, el vídeo de soldadura y los datos de cada fabricante. Nada inventado.", foto)}'
    f'</div>{nota("Un acabado fotorrealista costaría mucho más, pesaría demasiado para las conexiones de la zona y quedaría falso.")}</section>')

filas = [("Plano de sección del GEALAN S 9000", "Distribuidor de GEALAN", "La ventana que se abre (tramo 2)"),
         ("Corte de una serie de aluminio", "Aluval o Extrugasa", "El banco de trabajo (tramo 4)"),
         ("Medidas de una ventana tipo", "Familia", "El hueco de la casa (tramo 1)"),
         ("6 obras y el permiso de sus dueños", "Familia", "Ventanas a las obras (tramo 5)"),
         ("WhatsApp en el 664 40 96 18: sí o no", "Familia", "El contacto (tramo 6)"),
         ("Elegir logo", "Familia", "Toda la web")]
tabla = (f'<table style="width:1664px;font-size:28px;color:{INK}">'
         f'<tr><th style="width:44%;text-align:left">Qué</th><th style="width:22%;text-align:left">Quién</th><th style="width:34%;text-align:left">Para qué</th></tr>'
         + "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in filas) + '</table>')
slides["falta"] = (
    f'<section id="falta" data-transition="fade" style="background:{BG};color:{INK};{SANS};padding:128px;display:flex;flex-direction:column;gap:48px">'
    f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{VT}">Antes de programar todo</p>'
    f'<h2 style="{DISP};font-size:72px;font-weight:800;line-height:1.05">Lo que hace falta y quién lo tiene</h2>'
    f'{tabla}{nota("Nada de esto bloquea la prueba de los tramos 1 y 2: se puede empezar con medidas de hueco reales y dejar el corte del perfil para cuando llegue el plano.")}</section>')

pasos = [("1", "Prueba de los tramos 1 y 2", "La casa y la ventana que se abre, probadas en un móvil real."),
         ("2", "El resto del recorrido", "Si convence, taller, banco, obras y salida al valle."),
         ("3", "La web definitiva", "En Astro, con versión sin animación para quien la desactive y textos que lee Google.")]
cajas = "".join(
    f'<div style="flex:1;border-top:6px solid #4ba939;padding:24px 0 0 0;display:flex;flex-direction:column;gap:12px">'
    f'<p style="{MONO};font-size:32px;color:#4ba939">{n}</p><h3 style="{DISP};font-size:40px;font-weight:800;line-height:1.1;color:#eef1ee">{t}</h3>'
    f'<p style="font-size:28px;line-height:1.45;color:#a3ada7">{d}</p></div>' for n, t, d in pasos)
slides["siguiente"] = (
    f'<section id="siguiente" data-transition="fade" style="background:{DARK};color:#eef1ee;{SANS};padding:128px;display:flex;flex-direction:column;gap:56px">'
    f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:#4ba939">Siguiente paso</p>'
    f'<h2 style="{DISP};font-size:72px;font-weight:800;line-height:1.05">¿Os encaja el recorrido?</h2>'
    f'<p style="font-size:32px;line-height:1.45;color:#a3ada7;width:1300px">Decidnos si cambiaríais el orden, algún tramo o lo que se ve en él. Con el visto bueno, empezamos por una prueba corta.</p>'
    f'<div style="display:flex;gap:48px">{cajas}</div>'
    f'{nota("Se puede comentar directamente sobre cada diapositiva.")}</section>')

for k, html in slides.items():
    (S / f"{k}.html").write_text(html, encoding="utf-8")

deck = {"v": 4, "createdOnFiles": {"v": 1, "at": "2026-10-03T16:40:00Z"}, "lists": "css",
        "title": "Guion «A través de la ventana»", "cover": "portada", "order": ORDER,
        "sections": {"s1": {"description": "La idea: una sola animación que entra y sale por una ventana", "start": "portada"},
                     "s2": {"description": "Los seis tramos del recorrido, uno por diapositiva", "start": "tramo1"},
                     "s3": {"description": "Cómo se ve, qué falta y el siguiente paso", "start": "estilo"}},
        "faces": {"archivo": {"family": "Archivo", "href": "https://fonts.googleapis.com/css2?family=Archivo:wght@500..900&display=swap"},
                  "ibm-plex-sans": {"family": "IBM Plex Sans", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&display=swap"},
                  "ibm-plex-mono": {"family": "IBM Plex Mono", "href": "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&display=swap"}},
        "designSystems": [{"title": "Metal Hervás", "namespace": "metal-hervas", "artifact": "https://claude.ai/artifact/3DZaLvDXRyQ3gG47BAbq5f",
                           "version": "1790996051-eea8", "copiedAt": "2026-10-03T16:40:00Z"}]}
(R / "project" / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print({k: len(v) for k, v in slides.items()})
