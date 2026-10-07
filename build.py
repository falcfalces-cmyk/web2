#!/usr/bin/env python3
"""Genera las paginas del sitio (estilo del skill web-builder: barra lateral, migas, buscador Ctrl K).
Uso: python3 build.py
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
ICONS = ROOT / "assets" / "icons"


def css_version() -> str:
    """Huella del CSS para forzar recarga en navegadores con cache (moviles)."""
    data = (ROOT / "css" / "style.css").read_bytes()
    return hashlib.md5(data).hexdigest()[:8]


def js_version(nombre: str) -> str:
    """Huella de un JS: el indice se genera en main(), asi que si aun no existe se usa la del build anterior."""
    f = ROOT / "js" / nombre
    return hashlib.md5(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"

TEL_TXT = "941 89 37 78"
TEL_HREF = "tel:+34941893778"
EMAIL = "info@grupobelcom.com"
BASE_URL = "https://www.grupobelcom.com"
TARIFAS = json.loads((ROOT / "tarifas.json").read_text(encoding="utf-8"))

SERVICES = [
    ("conectividad", "Conectividad y redes", [
        ("telecomunicaciones", "Telecomunicaciones", "Voz, datos y comunicaciones unificadas para empresa, industria y entornos públicos."),
        ("fibra", "Fibra óptica", "Despliegue FTTH y troncales, empalmes y certificación de cada tramo."),
        ("redes", "Infraestructuras de red", "Cableado estructurado, redundancia y monitorización proactiva."),
        ("telefonia", "Telefonía", "Centralitas IP, telefonía fija y móvil, todo gestionado desde un mismo servicio."),
    ]),
    ("seguridad", "Seguridad", [
        ("ciberseguridad", "Ciberseguridad", "Auditorías, firewalls de nueva generación y protección frente a ransomware."),
        ("videovigilancia", "Videovigilancia", "Cámaras IP, grabación, analítica de vídeo y acceso remoto."),
        ("alarmas", "Alarmas", "Sistemas de intrusión conectados con aviso inmediato."),
    ]),
    ("energia", "Instalaciones eléctricas y energía", [
        ("electricidad", "Electricidad", "Baja tensión para vivienda, industria y entornos públicos, con boletines en regla."),
        ("renovables", "Energías renovables", "Fotovoltaica y autoconsumo para reducir la factura energética."),
        ("cargadores-ve", "Cargadores VE", "Puntos de recarga para particulares, comunidades y flotas."),
    ]),
    ("automatizacion", "Automatización e informática", [
        ("domotica", "Domótica", "Automatización de vivienda y edificios con KNX, Loxone y otros sistemas: iluminación, clima y accesos desde un único punto."),
        ("informatica", "Soluciones informáticas", "Equipos, servidores, copias de seguridad y soporte técnico para que la informática de tu empresa funcione sin sobresaltos."),
    ]),
]


SERVICE_IMAGES = {
    "telecomunicaciones": "telecomunicaciones.jpg",
    "fibra": "fibra.jpg",
    "redes": "rack.jpg",
    "telefonia": "telefonia.jpg",
    "ciberseguridad": "ciberseguridad.jpg",
    "videovigilancia": "seguridad.jpg",
    "alarmas": "alarmas.jpg",
    "electricidad": "electricidad.jpg",
    "renovables": "solar.jpg",
    "cargadores-ve": "cargador.jpg",
    "domotica": "domotica.jpg",
    "informatica": "informatica.jpg",
}


# Descripcion ampliada para la pagina de Servicios (las tarjetas usan la corta)
SERVICE_LONG = {
    "telecomunicaciones": "Diseñamos e instalamos las comunicaciones de tu empresa: voz, datos y comunicaciones unificadas en un único sistema. Estudiamos tu actividad, dimensionamos la infraestructura y nos encargamos de la puesta en marcha y del mantenimiento, para que las llamadas, la conexión y las herramientas de trabajo funcionen siempre, tanto en oficinas como en naves industriales y entornos públicos.",
    "fibra": "Desplegamos fibra óptica hasta tu empresa, tu vivienda o tu polígono: troncales, acometidas y redes FTTH. Realizamos empalmes con fusionadora y medimos y documentamos cada tramo para garantizar la calidad de la señal. Además de instalar, te asesoramos sobre la velocidad que necesitas y nos ocupamos de las incidencias.",
    "redes": "Montamos y ordenamos la red de tu empresa: cableado estructurado, armarios rack, conmutadores, wifi y enlaces redundantes. Diseñamos pensando en el día que algo falle, no solo en el día de la instalación, y añadimos monitorización para detectar los problemas antes de que lo note nadie.",
    "telefonia": "Centralitas IP y telefonía fija y móvil gestionadas desde un mismo servicio. Configuramos extensiones, desvíos, buzones y horarios, integramos la telefonía con el resto de tus sistemas y te acompañamos en el cambio para que no pierdas ninguna llamada durante la migración.",
    "ciberseguridad": "Protegemos tus sistemas y tus datos frente a amenazas actuales. Revisamos tu situación con una auditoría, configuramos firewalls de nueva generación, segmentamos la red y preparamos copias y planes de respuesta ante ransomware. Todo explicado de forma clara y adaptado al tamaño de tu empresa.",
    "videovigilancia": "Instalamos sistemas de videovigilancia con cámaras IP, grabación en servidor o en la nube y acceso remoto desde el móvil. Elegimos la cámara y la ubicación según lo que quieras vigilar y añadimos analítica de vídeo para avisarte solo de lo importante, en naves, comercios, comunidades y espacios públicos.",
    "alarmas": "Sistemas de alarma de intrusión conectados con aviso inmediato, para vivienda, comercio e industria. Combinamos detectores, sirenas y control desde el móvil, y los integramos con la videovigilancia y el control de accesos para tener la seguridad de tu instalación bajo un único criterio.",
    "electricidad": "Instalaciones eléctricas de baja tensión para vivienda, industria y entornos públicos: cuadros, líneas, iluminación y reformas. Trabajamos con instaladores propios, y nos encargamos de los boletines y la legalización, además del mantenimiento para que tu instalación esté siempre en regla.",
    "renovables": "Proyectos de energía fotovoltaica y autoconsumo para reducir tu factura de la luz. Estudiamos tu consumo, dimensionamos la instalación, nos ocupamos de la legalización y los trámites, y la ponemos en marcha. Después, nos mantenemos disponibles para revisiones y para ampliar el sistema si lo necesitas.",
    "cargadores-ve": "Puntos de recarga para vehículo eléctrico en viviendas, comunidades de vecinos, empresas y flotas. Revisamos tu instalación eléctrica, elegimos el cargador y la potencia adecuados, gestionamos la legalización y, si hace falta, añadimos gestión de la carga para no sobrecargar el suministro.",
    "domotica": "Automatización de viviendas y edificios con KNX, Loxone y otros sistemas: iluminación, climatización, persianas y accesos controlados desde un único punto. Diseñamos la instalación contigo para que sea fácil de usar, ahorre energía y pueda crecer con el tiempo.",
    "informatica": "Soluciones informáticas para empresa: equipos y servidores, redes internas, correo, copias de seguridad y soporte técnico continuo. Nos ocupamos de que tu tecnología esté actualizada, protegida y funcionando, y estamos disponibles cuando surge una incidencia.",
}


def icon(name: str) -> str:
    """Devuelve el SVG del icono, listo para insertar en linea."""
    svg = (ICONS / f"{name}.svg").read_text(encoding="utf-8")
    svg = re.sub(r"\s+", " ", svg).strip()
    svg = svg.replace('width="24" height="24" ', "")
    return svg


ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>'
ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>'
ICON_SHIELD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>'

LOCAL_BUSINESS_JSONLD = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Grupo Belcom",
  "image": "{BASE_URL}/assets/hero.jpg",
  "telephone": "+34941893778",
  "email": "{EMAIL}",
  "url": "{BASE_URL}/",
  "areaServed": ["La Rioja", "Navarra", "Aragón", "País Vasco"],
  "address": [
    {{"@type": "PostalAddress", "addressLocality": "Logroño", "addressRegion": "La Rioja", "addressCountry": "ES"}},
    {{"@type": "PostalAddress", "addressLocality": "Tudela", "addressRegion": "Navarra", "addressCountry": "ES"}},
    {{"@type": "PostalAddress", "addressLocality": "Pamplona", "addressRegion": "Navarra", "addressCountry": "ES"}},
    {{"@type": "PostalAddress", "addressLocality": "Zaragoza", "addressRegion": "Aragón", "addressCountry": "ES"}},
    {{"@type": "PostalAddress", "addressLocality": "Vitoria", "addressRegion": "País Vasco", "addressCountry": "ES"}}
  ]
}}
</script>
"""



def _lucide(inner, cls="lucide"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>'


I = {
    "search": _lucide('<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>'),
    "phone": _lucide(ICON_PHONE[ICON_PHONE.index("<path"):ICON_PHONE.rindex("</svg>")]),
    "mail": _lucide(ICON_MAIL[ICON_MAIL.index("<rect"):ICON_MAIL.rindex("</svg>")]),
    "arrow": _lucide('<path d="M5 12h14M12 5l7 7-7 7"/>'),
    "check": _lucide('<path d="M20 6 9 17l-5-5"/>'),
    "pin": _lucide('<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
    "sun": _lucide('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2m-7.07-2.93 1.41-1.41m11.32-11.32 1.41-1.41M2 12h2m16 0h2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41"/>'),
    "moon": _lucide('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>'),
    "monitor": _lucide('<rect width="20" height="14" x="2" y="3" rx="2"/><path d="M8 21h8M12 17v4"/>'),
    "panel": _lucide('<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/>'),
    "menu": _lucide('<path d="M4 6h16M4 12h16M4 18h16"/>'),
    "x": _lucide('<path d="M18 6 6 18M6 6l12 12"/>'),
    "home": _lucide('<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'),
    "grid": _lucide('<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>'),
    "euro": _lucide('<path d="M4 10h12M4 14h9"/><path d="M19 6a7.7 7.7 0 0 0-5.2-2A7.9 7.9 0 0 0 6 12c0 4.4 3.5 8 7.8 8 2 0 3.8-.8 5.2-2"/>'),
    "shield": _lucide('<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>'),
    "file": _lucide('<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4M10 9H8M16 13H8M16 17H8"/>'),
}


def svc_icon(sid):
    """Icono de servicio (los SVG de assets/icons) con la clase lucide."""
    return icon(sid).replace("<svg", '<svg class="lucide" aria-hidden="true"', 1)


GROUP_ICON = {"conectividad": "telecomunicaciones", "seguridad": "ciberseguridad",
              "energia": "electricidad", "automatizacion": "domotica"}
GROUP_IMAGE = {"conectividad": "telecomunicaciones.jpg", "seguridad": "seguridad.jpg",
               "energia": "solar.jpg", "automatizacion": "domotica.jpg"}
GROUP_LEAD = {
    "conectividad": "Fibra, redes y telefonía con redundancia y monitorización.",
    "seguridad": "Ciberseguridad, cámaras y alarmas bajo un mismo criterio.",
    "energia": "Baja tensión, fotovoltaica y puntos de recarga, con la legalización incluida.",
    "automatizacion": "Domótica KNX y Loxone, y la informática de tu empresa funcionando.",
}
DELEGACIONES = [("Logroño", "La Rioja"), ("Tudela", "Navarra"), ("Pamplona", "Navarra"),
                ("Zaragoza", "Aragón"), ("Vitoria", "País Vasco")]
N_SERVICIOS = sum(len(items) for _, _, items in SERVICES)
PAGES = {"index": "index.html", "servicios": "servicios.html", "tarifas": "tarifas.html", "contacto": "contacto.html"}
PRECIO_FIBRA = TARIFAS["fibra"]["tarifas"][0]["precio"]
PRECIO_MOVIL = TARIFAS["movil"]["tarifas"][0]["precio"]


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def head(title, desc, path="", schema=False):
    url = f"{BASE_URL}/{path}"
    og_image = f"{BASE_URL}/assets/hero.jpg"
    schema_html = LOCAL_BUSINESS_JSONLD if schema else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0a0b11" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{url}">
<link rel="preload" as="font" type="font/woff2" href="assets/fonts/geist.woff2" crossorigin>
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="512x512" href="assets/favicon-512.png">
<link rel="apple-touch-icon" href="assets/favicon-180.png">
<script>try{{var t=localStorage.getItem('belcom-tema');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="stylesheet" href="css/style.css?v={css_version()}">
{schema_html}</head>
<body>
"""


def sidebar(active):
    def item(key, href, ico, label, count=None):
        on = " on" if key == active else ""
        cnt = f'<span class="count">{count}</span>' if count else ""
        return (f'<a class="sb-item{on}" href="{href}" data-tip="{label}"{" aria-current=\"page\"" if on else ""}>'
                f'{I[ico]}<span class="lbl">{label}</span>{cnt}</a>')

    nav = "\n      ".join([
        item("index", "index.html", "home", "Inicio"),
        item("servicios", "servicios.html", "grid", "Servicios", N_SERVICIOS),
        item("tarifas", "tarifas.html", "euro", "Tarifas"),
        item("delegaciones", "index.html#delegaciones", "pin", "Delegaciones", len(DELEGACIONES)),
        item("contacto", "contacto.html", "mail", "Contacto"),
    ])
    groups = "\n      ".join(
        f'<a class="sb-item" href="servicios.html#grupo-{gid}" data-tip="{gname}">{svc_icon(GROUP_ICON[gid])}'
        f'<span class="lbl">{gname}</span><span class="count">{len(items)}</span></a>'
        for gid, gname, items in SERVICES
    )
    return f"""<aside class="sb" id="sb">
    <div class="sb-head">
      <a class="sb-brand" href="index.html" aria-label="Grupo Belcom — inicio">
        <img class="logo-l" src="assets/wordmark-dark.png" srcset="assets/wordmark-dark.png 1x, assets/wordmark-dark@2x.png 2x" width="75" height="30" alt="Grupo Belcom">
        <img class="logo-d" src="assets/wordmark-alpha.png" srcset="assets/wordmark-alpha.png 1x, assets/wordmark-alpha@2x.png 2x" width="75" height="30" alt="">
      </a>
      <span class="sb-mark" aria-hidden="true">B</span>
      <button type="button" class="btn btn-ghost btn-icon btn-sm" id="sb-fold" data-tip="Plegar la barra (Ctrl ←)" aria-label="Plegar la barra lateral">{I["panel"]}</button>
      <button type="button" class="btn btn-ghost btn-icon btn-sm sb-close" id="sb-close" aria-label="Cerrar el menú">{I["x"]}</button>
    </div>
    <div class="sb-product">Telecomunicaciones, redes y electricidad</div>
    <button type="button" class="sb-search" data-cmdk data-tip="Buscar (Ctrl K)">{I["search"]}<span>Buscar…</span><kbd>Ctrl K</kbd></button>
    <a class="btn btn-primary sb-new" href="contacto.html" data-tip="Contratar fibra óptica">{I["arrow"]}<span>Contratar fibra óptica</span></a>
    <nav class="sb-nav" aria-label="Principal">
      {nav}
    </nav>
    <div class="sb-group">Líneas de servicio</div>
    <nav class="sb-nav" aria-label="Líneas de servicio">
      {groups}
    </nav>
    <div class="sb-spacer"></div>
    <div class="sb-foot">
      <div class="seg full theme-seg" role="group" aria-label="Tema">
        <button type="button" data-tema="system" data-tip="Según el sistema" aria-label="Tema del sistema">{I["monitor"]}</button>
        <button type="button" data-tema="light" data-tip="Claro" aria-label="Tema claro">{I["sun"]}</button>
        <button type="button" data-tema="dark" data-tip="Oscuro" aria-label="Tema oscuro">{I["moon"]}</button>
      </div>
    </div>
  </aside>"""


def shell(active, crumbs, body):
    """Carcasa: barra lateral, cabecera con migas y lienzo con scroll."""
    if crumbs:
        trail = '<a href="index.html">Inicio</a>' + "".join(
            f'<span class="sep">/</span>' + (f'<a href="{h}">{t}</a>' if h else f"<b>{t}</b>") for t, h in crumbs)
    else:
        trail = "<b>Inicio</b>"
    return f"""<a href="#contenido" class="skip-link">Ir al contenido</a>
<div class="app" id="app">
  <script>try{{if(localStorage.getItem('belcom-sb')==='1')document.getElementById('app').classList.add('collapsed')}}catch(e){{}}</script>
  {sidebar(active)}
  <div class="main">
    <header class="topbar">
      <button type="button" class="btn btn-ghost btn-icon nav-burger" id="nav-burger" aria-label="Abrir el menú" aria-controls="sb">{I["menu"]}</button>
      <nav class="crumbs" aria-label="Migas de pan">{trail}</nav>
      <div class="right">
        <span class="badge ok sq hide-s" data-tip="Si algo falla, viene alguien de Belcom"><span class="dot"></span>Respuesta urgente &lt;24 h</span>
        <a class="btn btn-sm tel" href="{TEL_HREF}" aria-label="Llamar al {TEL_TXT}">{I["phone"]}<b>{TEL_TXT}</b></a>
      </div>
    </header>
    <main class="content" id="contenido" tabindex="-1">
      <div class="page">
{body}
        <footer class="foot-legal">
          <span>&copy; <span id="year">2026</span> Grupo Belcom · <a href="mailto:{EMAIL}">{EMAIL}</a></span>
          <nav aria-label="Legal"><a href="aviso-legal.html">Aviso legal</a><a href="privacidad.html">Privacidad</a><a href="cookies.html">Cookies</a></nav>
        </footer>
      </div>
    </main>
  </div>
  <div class="nav-scrim" id="nav-scrim"></div>
</div>
<div id="tip" role="tooltip"></div>
<script src="js/indice.js?v={js_version('indice.js')}"></script>
<script src="js/main.js?v={js_version('main.js')}"></script>
</body>
</html>
"""


def page_head(title, intro):
    return f"""        <div class="ph">
          <div>
            <h1>{title}</h1>
            <p class="sub">{intro}</p>
          </div>
        </div>"""


def cta_card(titulo, texto):
    return f"""        <section class="card cta" style="margin-top:40px">
          <div>
            <h2>{titulo}</h2>
            <p>{texto}</p>
          </div>
          <div class="actions">
            <a href="contacto.html" class="btn btn-primary">Contratar fibra óptica {I["arrow"]}</a>
            <a href="{TEL_HREF}" class="btn">{I["phone"]} {TEL_TXT}</a>
          </div>
        </section>"""


# ---------- tarifas ----------
def _precio(p):
    ent, _, dec = p.partition(",")
    dec_html = f"<sup>,{dec}</sup>" if dec else ""
    return f'<div class="price"><b>{ent}</b>{dec_html}<small>€/mes</small></div>'


def _tarifa_card(grupo, t):
    feat = t.get("destacada")
    badge = '<span class="badge accent sq">Más elegida</span>' if feat else ""
    if grupo == "fibra" and "velocidad" in t:
        head_ = f'<div class="sp">{t["velocidad"]}<small>Mbps</small></div><div class="sub">Fibra óptica · cualquier zona</div>'
    elif grupo == "movil":
        head_ = f'<div class="sp">{t["datos"]}</div><div class="sub">{t["nombre"]} incluidos</div>'
    else:
        head_ = f'<div class="sp">{t["nombre"]}</div><div class="sub">{t["detalle"]}</div>'
    return f"""            <article class="card plan{" feat" if feat else ""}">
              {badge}
              {head_}
              {_precio(t["precio"])}
              <a href="contacto.html" class="btn {"btn-primary" if feat else ""}">Contratar {I["arrow"]}</a>
            </article>"""


def tarifas_block():
    """Selector Fibra / Móvil / Fijo con tarjetas de precio. Datos en tarifas.json."""
    grupos = ["fibra", "movil", "fijo"]
    tabs = "".join(
        f'<button type="button" class="{"on" if i == 0 else ""}" data-ptab="{g}" aria-pressed="{"true" if i == 0 else "false"}">{TARIFAS[g]["titulo"]}</button>'
        for i, g in enumerate(grupos)
    )
    panels = []
    for g in grupos:
        d = TARIFAS[g]
        cards = "\n".join(_tarifa_card(g, t) for t in d["tarifas"])
        panels.append(f"""        <div class="ptab-panel" id="ptab-{g}">
          <div class="plans">
{cards}
          </div>
          <div class="callout plans-note">{I["check"]}<span>{d["nota"]}</span></div>
        </div>""")
    return f'        <div class="seg lg seg-wrap" role="group" aria-label="Tipo de tarifa">{tabs}</div>\n' + "\n".join(panels)


def build_tarifas():
    return (
        head("Tarifas · Grupo Belcom",
             "Tarifas de fibra óptica desde 20,90 €, móvil sin permanencia desde 6,90 € y línea fija desde 6 €. Mismo precio en cualquier zona.",
             path="tarifas.html")
        + shell("tarifas", [("Tarifas", None)], f"""
{page_head("Fibra, móvil y fijo, <em>sin sorpresas</em>", "Precios claros y el mismo en cualquier pueblo. Sin permanencia en móvil. Si necesitas algo a medida, te lo preparamos.")}
{tarifas_block()}
{cta_card("¿Dudas sobre qué tarifa te conviene?", "Te asesoramos sin compromiso y te damos de alta nosotros.")}""")
    )


# ---------- inicio ----------
def _tarcard(k, valor, d, href):
    ent, _, dec = valor.partition(",")
    dec_html = f"<sup style='font-size:.5em'>,{dec}</sup>" if dec else ""
    return f"""        <a class="card tarcard c4" href="{href}">
          <span class="k">{k}</span>
          <span class="v">{ent}{dec_html}<small>€/mes</small></span>
          <span class="d">{d}</span>
          <span class="link">Ver tarifas {I["arrow"]}</span>
        </a>"""


def build_index():
    fibra = TARIFAS["fibra"]["tarifas"]
    velocidades = [t["velocidad"] for t in fibra if "velocidad" in t]
    movil = TARIFAS["movil"]["tarifas"]
    fijo = TARIFAS["fijo"]["tarifas"]
    cats = []
    for n, (gid, gname, items) in enumerate(SERVICES, start=1):
        chips = "".join(f'<a class="chip-link" href="servicios.html#{sid}">{svc_icon(sid)}{sname}</a>' for sid, sname, _ in items)
        cats.append(f"""          <article class="card cat">
            <div class="cat-img"><img src="assets/{GROUP_IMAGE[gid]}" alt="" loading="lazy"><span class="badge soft sq cat-n num">{n:02d}</span></div>
            <div class="cat-b">
              <h3>{gname}</h3>
              <p>{GROUP_LEAD[gid]}</p>
              <div class="chips">{chips}</div>
            </div>
          </article>""")
    cities = "".join(
        f'<div class="city"><b><span class="stdot"></span>{c}</b><small>{r}</small></div>' for c, r in DELEGACIONES)
    return (
        head("Grupo Belcom · Telecomunicaciones, redes y electricidad",
             "Telecomunicaciones, redes, electricidad, seguridad y energía en La Rioja, Navarra, Aragón y País Vasco.",
             path="index.html", schema=True)
        + shell("index", None, f"""
        <div class="bento-top">
          <section class="card hero-card">
            <span class="badge accent" style="align-self:flex-start"><span class="live-dot" style="width:6px;height:6px;background:currentColor"></span>La Rioja · Navarra · Aragón · País Vasco</span>
            <h1>Telecomunicaciones, redes y electricidad para tu <em>empresa</em></h1>
            <p class="lead">Fibra óptica, telefonía, seguridad y energía con un único equipo técnico: del proyecto a la puesta en marcha y el mantenimiento.</p>
            <div class="actions">
              <a href="contacto.html" class="btn btn-primary btn-lg">Contratar fibra óptica {I["arrow"]}</a>
              <a href="tarifas.html" class="btn btn-lg">Ver tarifas</a>
            </div>
            <ul class="checks">
              <li>{I["check"]}Equipo técnico propio</li>
              <li>{I["check"]}Mantenimiento incluido</li>
              <li>{I["check"]}Instalación certificada</li>
            </ul>
          </section>
          <div class="bento-r">
            <div class="card tile"><span class="k">Líneas de servicio</span><span class="v num">{N_SERVICIOS}</span><span class="d">De la fibra al cuadro eléctrico.</span></div>
            <div class="card tile"><span class="k">Delegaciones propias</span><span class="v num">{len(DELEGACIONES)}</span><span class="d">Técnicos en plantilla.</span></div>
            <div class="card tile accent"><span class="k">Respuesta urgente</span><span class="v num">&lt;24<small>h</small></span><span class="d">Viene alguien de Belcom.</span></div>
            <div class="card tile"><span class="k">Comunidades</span><span class="v num">4</span><span class="d">Mismo estándar en todas.</span></div>
            <div class="card tile"><span class="k">Permanencia en móvil</span><span class="v num">0<small>meses</small></span><span class="d">Mismo precio en cualquier pueblo.</span></div>
            <div class="card tile"><span class="k">Interlocutor</span><span class="v num">1</span><span class="d">Sin coordinar proveedores.</span></div>
          </div>
        </div>

        <div class="sec-h">
          <div>
            <h2>Todo lo que necesitas, con un solo interlocutor</h2>
            <p>{N_SERVICIOS} líneas de servicio bajo el mismo equipo técnico: no tienes que coordinar entre el de redes, el electricista y el de seguridad.</p>
          </div>
          <a class="link" href="servicios.html">Ver los {N_SERVICIOS} servicios en detalle {I["arrow"]}</a>
        </div>
        <div class="cats">
{chr(10).join(cats)}
        </div>

        <div class="sec-h" id="tarifas">
          <div>
            <h2>Fibra desde {PRECIO_FIBRA} € al mes</h2>
            <p>Tarifas sencillas, el mismo precio en cualquier zona, e instalación y soporte con técnicos de Belcom.</p>
          </div>
          <a class="link" href="tarifas.html">Todas las tarifas {I["arrow"]}</a>
        </div>
        <div class="bento">
{_tarcard("Fibra óptica · desde", PRECIO_FIBRA, ", ".join(velocidades[:-1]) + f" y {velocidades[-1]} Mbps. Mismo precio en cualquier zona.", "tarifas.html#fibra")}
{_tarcard("Móvil · desde", PRECIO_MOVIL, f'{movil[0]["nombre"]} y hasta {movil[-1]["datos"]}. Sin permanencia.', "tarifas.html#movil")}
{_tarcard("Línea fija · desde", fijo[0]["precio"], f'{fijo[0]["nombre"]}, o {fijo[1]["nombre"].lower()} por {fijo[1]["precio"]} €.', "tarifas.html#fijo")}
        </div>

        <div class="sec-h" id="delegaciones">
          <div>
            <h2>Delegaciones propias, no subcontratas</h2>
            <p>Equipo técnico en plantilla repartido por cuatro comunidades. Cuando llamas, viene alguien de Belcom.</p>
          </div>
        </div>
        <div class="card cities">{cities}</div>

{cta_card("¿Tienes un proyecto sobre la mesa?", "Cuéntanos qué necesitas y te damos una propuesta técnica sin compromiso.")}
        <div class="callout ok kd">{I["shield"]}<span><b>Empresa adherida al Programa Kit Digital.</b> Plan de Recuperación, Transformación y Resiliencia — financiado por los fondos NextGeneration UE.</span></div>""")
    )


# ---------- servicios ----------
def build_servicios():
    subnav = "".join(f'<a class="chip-link" href="#grupo-{g}">{svc_icon(GROUP_ICON[g])}{n}</a>' for g, n, _ in SERVICES)
    groups = []
    for gi, (gid, gname, items) in enumerate(SERVICES, start=1):
        cards = "\n".join(f"""            <article class="card svc" id="{sid}">
              <div class="svc-img"><img src="assets/{SERVICE_IMAGES.get(sid, "hero.jpg")}" alt="{sname} — Grupo Belcom" loading="lazy"></div>
              <div class="svc-b">
                <div class="svc-t"><span class="ico">{svc_icon(sid)}</span><h3>{sname}</h3></div>
                <p>{SERVICE_LONG.get(sid, sdesc)}</p>
              </div>
            </article>""" for sid, sname, sdesc in items)
        groups.append(f"""        <section class="svc-group" id="grupo-{gid}">
          <div class="sec-h"><h2><span class="badge soft sq num">{gi:02d}</span>{gname}</h2></div>
          <div class="svc-list">
{cards}
          </div>
        </section>""")
    return (
        head("Servicios · Grupo Belcom",
             "Telecomunicaciones, fibra, redes, electricidad, ciberseguridad, videovigilancia, alarmas, domótica KNX y Loxone, fotovoltaica, cargadores VE y soluciones informáticas.",
             path="servicios.html")
        + shell("servicios", [("Servicios", None)], f"""
{page_head(f"{N_SERVICIOS} líneas de servicio, <em>un único equipo</em> técnico", "Desde el cuadro eléctrico hasta el firewall. Diseño, ejecución y mantenimiento con el mismo interlocutor de principio a fin.")}
        <nav class="subnav" aria-label="Líneas de servicio">{subnav}</nav>
{chr(10).join(groups)}
{cta_card("¿Cómo podemos ayudarte?", "Asesoramiento técnico sin compromiso para contratar tu fibra óptica.")}""")
    )


# ---------- contacto ----------
def build_contacto():
    return (
        head("Contacto · Grupo Belcom",
             f"Contacta con Grupo Belcom: {TEL_TXT} · {EMAIL}. Logroño, Tudela, Zaragoza, Pamplona y Vitoria.",
             path="contacto.html")
        + shell("contacto", [("Contacto", None)], f"""
{page_head("Hablemos de tu <em>proyecto</em>", "Cuéntanos qué necesitas por teléfono o email y te respondemos con una propuesta técnica concreta.")}
        <div class="bento">
          <a class="card contact-card c6" href="{TEL_HREF}">
            <span class="ico">{I["phone"]}</span>
            <span><span class="k">Teléfono</span><br><span class="v">{TEL_TXT}</span></span>
          </a>
          <a class="card contact-card c6" href="mailto:{EMAIL}">
            <span class="ico">{I["mail"]}</span>
            <span><span class="k">Email</span><br><span class="v">{EMAIL}</span></span>
          </a>
        </div>
        <div class="card card-pad" style="margin-top:12px">
          <dl class="kv wide">
            <dt>Delegaciones</dt><dd>{" · ".join(c for c, _ in DELEGACIONES)}</dd>
            <dt>Zona de servicio</dt><dd>La Rioja · Navarra · Aragón · País Vasco</dd>
          </dl>
        </div>""")
    )



def build_aviso_legal():
    content = """
      <h2>1. Datos identificativos</h2>
      <p>En cumplimiento del artículo 10 de la Ley 34/2002, de Servicios de la Sociedad de la Información y Comercio Electrónico (LSSI-CE), se informa de los siguientes datos: el titular de este sitio web es <strong>Grupo Belcom</strong>, con CIF <strong>[CIF a completar]</strong> y domicilio social en <strong>[domicilio social a completar]</strong>. Puede contactar con nosotros en el teléfono {tel} o en el email <a href="mailto:{email}">{email}</a>.</p>

      <h2>2. Objeto y aceptación</h2>
      <p>El presente aviso legal regula el uso del sitio web grupobelcom.com. La navegación por este sitio atribuye la condición de usuario e implica la aceptación plena de las condiciones aquí recogidas.</p>

      <h2>3. Condiciones de uso</h2>
      <p>El usuario se compromete a hacer un uso adecuado y lícito del sitio web, de conformidad con la legislación aplicable, la buena fe y el orden público. Queda prohibido cualquier uso que pueda dañar, inutilizar o sobrecargar el sitio, o impedir su normal utilización por parte de otros usuarios.</p>

      <h2>4. Propiedad intelectual e industrial</h2>
      <p>Todos los contenidos de este sitio web (textos, imágenes, marcas, logotipos y demás elementos) son titularidad de Grupo Belcom o de terceros que han autorizado su uso, y están protegidos por la normativa de propiedad intelectual e industrial. Queda prohibida su reproducción, distribución o transformación sin autorización expresa.</p>

      <h2>5. Exclusión de responsabilidad</h2>
      <p>Grupo Belcom no se hace responsable de los daños derivados de la falta de disponibilidad o continuidad del sitio, ni del contenido de los sitios web de terceros a los que pudiera enlazarse desde este.</p>

      <h2>6. Legislación aplicable</h2>
      <p>Las presentes condiciones se rigen por la legislación española. Para la resolución de cualquier controversia, las partes se someten a los juzgados y tribunales que correspondan conforme a derecho.</p>
    """.format(tel=TEL_TXT, email=EMAIL)
    return _build_legal_page(
        slug="aviso-legal", label="Legal", title="Aviso <em>legal</em>",
        intro="Información sobre la identidad del titular de este sitio web y las condiciones de uso.",
        desc="Aviso legal de Grupo Belcom: identificación del titular, condiciones de uso y propiedad intelectual del sitio web.",
        content=content,
    )


def build_privacidad():
    content = """
      <h2>1. Responsable del tratamiento</h2>
      <p>El responsable del tratamiento de los datos personales es <strong>Grupo Belcom</strong>, CIF <strong>[CIF a completar]</strong>, domicilio social en <strong>[domicilio social a completar]</strong>, email de contacto <a href="mailto:{email}">{email}</a>.</p>

      <h2>2. Qué datos tratamos</h2>
      <p>Este sitio web no dispone de formularios ni de cuentas de usuario: no recoge datos personales de forma automática a través de la navegación. Los únicos datos que tratamos son los que usted decide facilitarnos voluntariamente al contactar por teléfono ({tel}) o por email ({email}) para solicitar información o presupuesto.</p>

      <h2>3. Finalidad y legitimación</h2>
      <p>Tratamos esos datos con la finalidad de atender su consulta o solicitud y, en su caso, elaborar y gestionar la propuesta técnica o el presupuesto solicitado. La base legal es el consentimiento del interesado, prestado al iniciar el contacto, y el interés legítimo en responder a su solicitud.</p>

      <h2>4. Conservación</h2>
      <p>Los datos se conservarán mientras se mantenga la relación comercial o precontractual, y posteriormente durante los plazos legalmente exigibles.</p>

      <h2>5. Destinatarios</h2>
      <p>No se ceden datos a terceros, salvo obligación legal.</p>

      <h2>6. Sus derechos</h2>
      <p>Puede ejercer sus derechos de acceso, rectificación, supresión, oposición, limitación del tratamiento y portabilidad escribiendo a <a href="mailto:{email}">{email}</a>. Asimismo, tiene derecho a presentar una reclamación ante la Agencia Española de Protección de Datos (www.aepd.es) si considera que el tratamiento no se ajusta a la normativa vigente.</p>
    """.format(tel=TEL_TXT, email=EMAIL)
    return _build_legal_page(
        slug="privacidad", label="Legal", title="Política de <em>privacidad</em>",
        intro="Cómo tratamos los datos personales que nos facilita al contactar con nosotros.",
        desc="Política de privacidad de Grupo Belcom: qué datos tratamos, con qué finalidad y cómo ejercer sus derechos RGPD.",
        content=content,
    )


def build_cookies():
    content = """
      <h2>1. Qué es una cookie</h2>
      <p>Una cookie es un pequeño fichero que un sitio web puede guardar en el navegador del usuario para recordar información sobre su visita.</p>

      <h2>2. Cookies que utiliza este sitio</h2>
      <p>Este sitio web <strong>no utiliza cookies propias ni de terceros</strong> con fines analíticos, publicitarios o de personalización. No se realiza ningún seguimiento de la navegación.</p>

      <h2>3. Cambios futuros</h2>
      <p>Si en el futuro se incorporase algún servicio que utilice cookies (por ejemplo, analítica web), esta política se actualizará y se solicitará el consentimiento del usuario cuando sea legalmente necesario.</p>

      <h2>4. Configuración del navegador</h2>
      <p>Aunque este sitio no instala cookies, puede configurar su navegador para bloquearlas o eliminarlas en cualquier momento desde su panel de ajustes de privacidad.</p>
    """
    return _build_legal_page(
        slug="cookies", label="Legal", title="Política de <em>cookies</em>",
        intro="Este sitio web no utiliza cookies de seguimiento ni de terceros.",
        desc="Política de cookies de Grupo Belcom: este sitio web no utiliza cookies analíticas ni de terceros.",
        content=content,
    )



def _build_legal_page(slug, label, title, intro, desc, content):
    return (
        head(f"{strip_tags(title)} · Grupo Belcom", desc, path=f"{slug}.html")
        + shell(slug, [(strip_tags(title), None)], f"""
{page_head(title, intro)}
        <article class="card prose">
{content}
        </article>""")
    )


def build_indice():
    """js/indice.js: datos del buscador Ctrl K (páginas, servicios, tarifas, delegaciones, acciones)."""
    items = [
        ("Páginas", "Inicio", "", "index.html", "home"),
        ("Páginas", "Servicios", f"{N_SERVICIOS} líneas de servicio", "servicios.html", "grid"),
        ("Páginas", "Tarifas", "Fibra, móvil y fijo", "tarifas.html", "euro"),
        ("Páginas", "Contacto", f"{TEL_TXT} · {EMAIL}", "contacto.html", "mail"),
        ("Páginas", "Aviso legal", "", "aviso-legal.html", "file"),
        ("Páginas", "Política de privacidad", "", "privacidad.html", "file"),
        ("Páginas", "Política de cookies", "", "cookies.html", "file"),
    ]
    for gid, gname, svcs in SERVICES:
        for sid, sname, sdesc in svcs:
            items.append(("Servicios", sname, gname, f"servicios.html#{sid}", "svc:" + sid))
    for g in ("fibra", "movil", "fijo"):
        d = TARIFAS[g]
        items.append(("Tarifas", d["titulo"], d["nota"], f"tarifas.html#{g}", "euro"))
    for c, r in DELEGACIONES:
        items.append(("Delegaciones", c, r, "index.html#delegaciones", "pin"))
    items += [
        ("Acciones", "Llamar", TEL_TXT, TEL_HREF, "phone"),
        ("Acciones", "Escribir un email", EMAIL, f"mailto:{EMAIL}", "mail"),
        ("Acciones", "Contratar fibra óptica", "", "contacto.html", "arrow"),
    ]
    iconos = {k: v for k, v in I.items()}
    for _, _, items_ in SERVICES:
        for sid, _, _ in items_:
            iconos["svc:" + sid] = svc_icon(sid)
    data = [{"g": g, "l": l, "s": s, "h": h, "i": i} for g, l, s, h, i in items]
    usados = {d["i"] for d in data}
    return ("// Generado por build.py: no editar a mano.\n"
            "window.BELCOM_INDICE = " + json.dumps(data, ensure_ascii=False) + ";\n"
            "window.BELCOM_ICONOS = " + json.dumps({k: v for k, v in iconos.items() if k in usados or k in ("search", "arrow")}, ensure_ascii=False) + ";\n")


def main():
    (ROOT / "js" / "indice.js").write_text(build_indice(), encoding="utf-8")
    print("  js/indice.js")
    builders = {
        "index": build_index,
        "servicios": build_servicios,
        "tarifas": build_tarifas,
        "contacto": build_contacto,
        "aviso-legal": build_aviso_legal,
        "privacidad": build_privacidad,
        "cookies": build_cookies,
    }
    for page, fn in builders.items():
        (ROOT / f"{page}.html").write_text(fn(), encoding="utf-8")
        print(f"  {page}.html")
    print("Listo.")


if __name__ == "__main__":
    main()
