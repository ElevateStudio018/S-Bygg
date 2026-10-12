"""Builds docs/*.html for S-Bygg i Umeå AB.

Run:  python3 scripts/build.py docs

All text, services, the review and contact details live in this file. Services with confirmed=False and the
FAQ answers are suggestions that S-Bygg should confirm or edit before launch.
"""
import html
import json
import pathlib
import sys
from urllib.parse import quote_plus

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")

# --- Verified company details (Google Maps) -----------------------------------------------------------------------
NAME = "S-Bygg i Umeå AB"
PHONE, TEL = "070-332 06 44", "+46703320644"
STREET, POSTAL, CITY = "Fatvägen", "906 20", "Umeå"
ADDR = f"{STREET}, {POSTAL} {CITY}"
RATING, REVIEW_COUNT = "5,0", 1
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{NAME}, {ADDR}")
MAP_EMBED = "https://www.google.com/maps?q=" + quote_plus(ADDR) + "&z=14&hl=sv&output=embed"
# Google Maps only says the business closes at 16. Edit when the real hours are known.
HOURS = "Dagtid, till kl. 16"

# Not known yet: left empty, and then not shown anywhere.
EMAIL = ""
ORG_NR = ""

# The quote form e-mails through FormSubmit. Elevate Studio receives the requests during the preview; at launch this
# becomes S-Bygg's own address. The first request to a new address only sends an activation e-mail.
FORM_EMAIL = "elevate.studio018@gmail.com"

SITE_URL = "https://elevatestudio018.github.io/S-Bygg/"

# --- Services -------------------------------------------------------------------------------------------------------
# confirmed=True: work described in the customer review on Google. confirmed=False: a suggestion to confirm or remove.
SERVICES = [
    dict(
        slug="kok", title="Köksrenovering", confirmed=True,
        photo="kok", pos="50% 55%", alt="Ljust kök med vita luckor och trägolv",
        short="Från nya luckor till totalrenovering av hela köket.",
        body=[
            "Vi gör köksrenoveringar i Umeå – från några nya skåp till att riva ut allt och bygga upp köket på nytt. Senast totalrenoverade vi köket i en Västerbottensvilla och tog samtidigt upp en ny utgång till altanen.",
            "Rivning, regelverk, väggar, montering av stommar och luckor, lister och anpassningar gör vi själva. El och VVS går vi igenom med dig innan start, så att det är klart vem som gör vad.",
        ],
        items=["Rivning av gammalt kök", "Nya väggar och ytskikt", "Montering av stommar, luckor och bänkskivor",
               "Öppning mot angränsande rum", "Lister och foder"],
    ),
    dict(
        slug="ombyggnad", title="Ombyggnad och renovering", confirmed=True,
        photo="ombyggnad", pos="50% 50%", alt="Rum under renovering med stegar och verktyg",
        short="Ny planlösning, nya väggar eller renovering i etapper.",
        body=[
            "Ett slutet kök som ska öppnas mot vardagsrummet, ett rum som ska delas eller ett äldre hus som ska renoveras i omgångar. Vi bygger om i villor och bostäder i Umeå.",
            "Vi tittar på huset tillsammans med dig och går igenom vad som ska göras och i vilken ordning, innan något arbete börjar.",
        ],
        items=["Ändrad planlösning", "Nya och rivna innerväggar", "Golv, väggar och innertak", "Renovering i etapper",
               "Anpassningar i äldre hus"],
    ),
    dict(
        slug="oppningar", title="Nya öppningar och dörrar", confirmed=True,
        photo="dorr", pos="50% 45%", alt="Snickare skruvar fast ett gångjärn i en dörrkarm",
        short="Öppningar mellan rum och nya utgångar, till exempel mot altanen.",
        body=[
            "En ny öppning mellan två rum eller en ny dörr ut mot altanen ger mer ljus och ett bättre flöde i huset. Vi har bland annat tagit upp en utgång från ett kök till en större altan i en Västerbottensvilla.",
            "Väggen är ofta bärande. Vi ser över den först, och behöver konstruktionen räknas på tar vi upp det med dig innan vi börjar.",
        ],
        items=["Öppning mellan rum", "Ny dörr till altan eller trädgård", "Avväxling och förstärkning", "Karmar, foder och tätning",
               "Återställning av väggen runt öppningen"],
    ),
    dict(
        slug="altan", title="Altaner och trädäck", confirmed=False,
        photo="altan", pos="50% 60%", alt="Träaltan med räcke en höstdag",
        short="Nya altaner, utbyggnad och räcken.",
        body=[
            "Vi tar emot förfrågningar om nya altaner, trädäck och arbeten i anslutning till befintliga altaner.",
            "Berätta om läget, storleken och hur altanen ska ansluta till huset, så hör vi av oss.",
        ],
        items=["Ny altan eller trädäck", "Utbyggnad av befintlig altan", "Räcken och trappor", "Ny utgång från huset"],
    ),
    dict(
        slug="tillbyggnad", title="Tillbyggnader", confirmed=False,
        photo="tillbyggnad", pos="50% 50%", alt="Regelstomme av trä under uppförande",
        short="Ett nytt rum, ett uterum eller en entré.",
        body=[
            "Vi tar emot förfrågningar om tillbyggnader i Umeå med omnejd.",
            "Krävs bygglov eller anmälan ska det vara klart innan arbetet börjar. Vi går igenom vad som gäller för ditt projekt.",
        ],
        items=["Nytt rum", "Uterum", "Entré och vindfång", "Förråd och garage"],
    ),
    dict(
        slug="inredning", title="Inredningssnickeri", confirmed=False,
        photo="inredning", pos="50% 40%", alt="Snickare mäter och märker upp ett trästycke",
        short="Platsbyggd förvaring, golv, lister och trappor.",
        body=[
            "Vi tar emot förfrågningar om platsbyggd förvaring, golvläggning, lister, foder och andra mindre snickeriarbeten.",
        ],
        items=["Platsbyggda garderober och hyllor", "Golvläggning", "Lister, foder och socklar", "Trappor inomhus"],
    ),
]
DONE = [s for s in SERVICES if s["confirmed"]]
ASK = [s for s in SERVICES if not s["confirmed"]]
WORK_TYPES = [s["title"] for s in SERVICES] + ["Annat"]

# --- Review (copied exactly from Google; the text ends where Google cuts it off) -------------------------------------
REVIEWS = [
    dict(
        name="Magnus Eltoft", stars=5,
        text="Vi anlitade byggfirman S-Bygg här i Umeå för ett tag sen när vi skulle göra en totalrenovering av köket i vår Västerbottensvilla, vart även så att de fick förtroendet med att göra en öppning med utgång från köket till en större altan med …",
        truncated=True,
        reply="Stort tack för förtroendet!",
    ),
]

FAQ = [
    ("Vilka jobb tar ni?",
     "Köksrenoveringar, ombyggnader och nya öppningar i bostäder har vi gjort. Fråga gärna om andra snickeri- och byggjobb också."),
    ("Kan jag få en offert?",
     f"Ja. Fyll i <a href=\"#offert\">formuläret</a> eller ring <a href=\"tel:{TEL}\">{PHONE}</a>. Oftast behöver vi se huset innan vi kan ge ett pris som håller."),
    ("Var jobbar ni?",
     "Vi utgår från Umeå. Ligger jobbet utanför stan, säg var, så svarar vi om vi kan ta det."),
    ("Gäller ROT-avdrag?",
     "ROT-avdraget gäller arbetskostnaden för många renoveringar och ombyggnader i bostäder. Vi går igenom vad som gäller för ditt jobb i offerten."),
]

STEPS = [
    ("Du ringer eller skriver", "Berätta kort vad du vill göra."),
    ("Vi tittar på jobbet", "Gärna på plats, så att vi ser förutsättningarna."),
    ("Du får en offert", "Med vad som ingår och vad det kostar."),
    ("Vi bygger", "Enligt det vi har kommit överens om."),
]

# --- Markup helpers -------------------------------------------------------------------------------------------------
E = html.escape
PHONE_ICON = ('<svg class="pi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M21 16.5v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.8 2 2 0 0 1 3.1 1.6h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L7.1 9.5a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>'
              '<path d="M15 2.5a6.5 6.5 0 0 1 6.5 6.5M15 6a3 3 0 0 1 3 3"/></svg>')
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m10 1.6 2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 15l-5.2 2.8 1-5.9L1.5 7.8l5.9-.8z"/></svg>'


def stars(n=5):
    return f'<span class="stars" role="img" aria-label="{n} av 5 stjärnor">{STAR * n}</span>'


def img(src, alt="", pos="50% 50%", sizes="100vw", lazy=True):
    return (f'<img src="img/{src}.jpg" srcset="img/{src}-s.jpg 800w, img/{src}.jpg 1800w" sizes="{sizes}" '
            f'alt="{E(alt)}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async" style="object-position:{pos}">')


def photo(src, alt, pos="50% 50%", sizes="(min-width: 960px) 50vw, 100vw"):
    """A rounded photo with the note that it is a stock photo, not S-Bygg's own."""
    return f'<figure class="ph">{img(src, alt, pos, sizes)}<figcaption>Illustrationsbild</figcaption></figure>'


# S-Bygg's own logo, traced to a vector from assets-src/s-bygg-logo-original.jpg: red S, white BYGG for the dark header
# and footer. assets-src/s-bygg-logo-morkt.svg has dark letters for light backgrounds.
def logo():
    return '<img class="logo-img" src="img/s-bygg-logo.svg" alt="S-Bygg" width="480" height="125">'


def call_btn(label=None, cls=""):
    return f'<a class="pill pill-red {cls}" href="tel:{TEL}">{PHONE_ICON}<span>{label or "Ring " + PHONE}</span></a>'


NAV = [("tjanster", "Tjänster"), ("referens", "Referens"), ("om-oss", "Om oss"), ("fragor", "Frågor"), ("kontakt", "Kontakt")]


def header(home):
    pre = "" if home else "index.html"
    links = "".join(f'<a href="{pre}#{a}">{t}</a>' for a, t in NAV)
    rows = "".join(f'<li><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    return f'''<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="head">
  <div class="wrap bar">
    <a class="logo" href="{'#top' if home else 'index.html'}" aria-label="{NAME}, till startsidan">{logo()}</a>
    <nav class="nav" aria-label="Huvudmeny">{links}</nav>
    <a class="pill pill-red head-call" href="tel:{TEL}">{PHONE_ICON}<span>{PHONE}</span></a>
    <a class="round round-red head-round" href="tel:{TEL}" aria-label="Ring {PHONE}">{PHONE_ICON}</a>
    <button class="burger" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu" aria-label="Meny"><span></span><span></span></button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden>
    <div class="wrap">
      <ul class="menu-main">{rows}</ul>
      <p class="menu-h">Tjänster</p><ul class="menu-svc">{svc}</ul>
      {call_btn()}
    </div>
  </nav>
</header>'''


def footer(home):
    pre = "" if home else "index.html"
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    mail = f'<p><a href="mailto:{EMAIL}">{EMAIL}</a></p>' if EMAIL else ""
    org = f"<p>Org.nr {ORG_NR}</p>" if ORG_NR else ""
    return f'''<footer class="foot">
  <div class="wrap">
    <a class="logo" href="{pre or '#top'}" aria-label="{NAME}, till startsidan">{logo()}</a>
    <div class="foot-grid">
      <div>
        <p class="foot-h">{NAME}</p>
        <p><b>Umeå</b></p>
        <p>{STREET},<br>{POSTAL} {CITY}</p>
        <p><a href="tel:{TEL}">{PHONE}</a></p>{mail}{org}
      </div>
      <div><p class="foot-h">Tjänster</p><ul>{svc}</ul></div>
      <div><p class="foot-h">S-Bygg</p><ul>{"".join(f'<li><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)}<li><a href="{pre}#offert">Begär offert</a></li></ul></div>
    </div>
    <div class="foot-end">
      <span>© <span data-year>2026</span> {NAME} · Bilderna är stockfoton från Pexels</span>
      <a href="https://elevatestudio.nu" target="_blank" rel="noopener">Byggd av Elevate Studio</a>
    </div>
  </div>
</footer>
<script src="assets/site.js" defer></script>
</body>
</html>
'''


def jsonld():
    data = {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": NAME, "url": SITE_URL,
        "telephone": TEL, "image": SITE_URL + "img/hero-renovering.jpg",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": POSTAL.replace(" ", ""),
                    "addressLocality": CITY, "addressCountry": "SE"},
        "areaServed": {"@type": "City", "name": "Umeå"},
    }
    if EMAIL:
        data["email"] = EMAIL
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def page(name, title, desc, main, home=False, image="hero-renovering"):
    url = SITE_URL + ("" if name == "index.html" else name)
    doc = f'''<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="sv_SE">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE_URL}img/{image}.jpg">
<meta name="theme-color" content="#1d1d1d">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
{jsonld() if home else ''}
</head>
<body>
{header(home)}
<main id="main">
{main}
</main>
{footer(home)}'''
    (OUT / name).write_text(doc, encoding="utf-8")


def card(s):
    return (f'<li class="card"><a href="tjanst-{s["slug"]}.html">{photo(s["photo"], s["alt"], s["pos"], "(min-width: 960px) 33vw, 100vw")}'
            f'<h3>{s["title"]}</h3><p>{s["short"]}</p><span class="more">Läs mer</span></a></li>')


def ask_pills(skip=None):
    return "".join(f'<a class="pill pill-dark" href="tjanst-{s["slug"]}.html">{s["title"]}</a>' for s in ASK if s["slug"] != skip)


def review_block(center=False):
    out = []
    for r in REVIEWS:
        more = (f' · <a href="{MAPS_LINK}" target="_blank" rel="noopener">Läs hela på Google</a>' if r.get("truncated") else "")
        reply = f'<p class="reply"><b>Svar från S-Bygg:</b> ”{E(r["reply"])}”</p>' if r.get("reply") else ""
        out.append(f'<figure class="review{" center" if center else ""}">{stars(r["stars"])}<blockquote><p>”{E(r["text"])}”</p></blockquote>'
                   f'<figcaption><b>{E(r["name"])}</b>, omdöme på Google{more}</figcaption>{reply}</figure>')
    return "".join(out)


def quote_form():
    opts = "".join(f"<option>{E(t)}</option>" for t in WORK_TYPES)
    req = '<span class="req" aria-hidden="true">*</span>'
    return f'''<form class="form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
  <p class="field"><label for="f-typ">Typ av jobb</label><select id="f-typ" name="Typ av byggprojekt"><option value="">– Välj ett alternativ –</option>{opts}</select></p>
  <p class="field"><label for="f-namn">För- och efternamn{req}</label><input id="f-namn" name="Namn" autocomplete="name" required><span class="err" id="e-namn" hidden>Skriv ditt namn.</span></p>
  <p class="field"><label for="f-tel">Telefonnummer{req}</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel"><span class="err" id="e-tel" hidden>Skriv telefonnummer eller e-post.</span></p>
  <p class="field"><label for="f-epost">E-post</label><input id="f-epost" name="E-post" type="email" autocomplete="email"><span class="err" id="e-epost" hidden>Kontrollera e-postadressen.</span></p>
  <p class="field"><label for="f-besk">Beskriv jobbet</label><textarea id="f-besk" name="Beskrivning" rows="5" placeholder="Vad ska göras, var och när?"></textarea></p>
  <p class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="_honey" tabindex="-1" autocomplete="off"></p>
  <p class="small">{req} Telefonnummer eller e-post räcker. Uppgifterna används bara för att svara dig.</p>
  <p><button class="pill pill-dark" type="submit">Skicka förfrågan</button></p>
  <p class="send-err" id="send-err" role="alert" hidden>Det gick inte att skicka just nu. Försök igen, eller ring <a href="tel:{TEL}">{PHONE}</a>.</p>
</form>
<div class="done" id="qdone" tabindex="-1" hidden>
  <p class="done-h">Tack! Vi har fått din förfrågan.</p>
  <p>Vi hör av oss så snart vi kan. Brådskar det, ring <a href="tel:{TEL}">{PHONE}</a>.</p>
  <p><button class="link" type="button" id="qagain">Skicka en ny förfrågan</button></p>
</div>'''


# --- Start page -----------------------------------------------------------------------------------------------------
def index():
    cards = "".join(card(s) for s in DONE)
    steps = "".join(f"<li><b>{t}</b> {d}</li>" for t, d in STEPS)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    done_links = " ".join(f'<a class="pill pill-dark" href="tjanst-{s["slug"]}.html">{s["title"]}</a>' for s in DONE)

    main = f'''<section class="hero" id="top" aria-labelledby="hero-h">
  <div class="hero-ph">{img("hero-renovering", "Snickare i ett hus under ombyggnad", "50% 45%", lazy=False)}</div>
  <div class="wrap hero-in">
    <h1 id="hero-h">Snickare och byggfirma i Umeå</h1>
    <p>{NAME} gör köksrenoveringar, ombyggnader och nya öppningar i villor och bostäder i Umeå.</p>
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="#offert">Begär offert</a></div>
  </div>
  <span class="hero-note">Illustrationsbild</span>
</section>

<section class="sec tint" aria-labelledby="intro-h">
  <div class="wrap split">
    {photo("kok-2", "Ljust kök med köksö och trägolv")}
    <div>
      <h2 id="intro-h">Köksrenovering och ombyggnad i Umeå</h2>
      <p class="lead">Vi river, bygger om och renoverar i villor och bostäder i Umeå. Senast totalrenoverade vi ett kök i en Västerbottensvilla och tog upp en ny utgång från köket till altanen.</p>
      <div class="btns">{done_links}</div>
    </div>
  </div>
</section>

<section class="sec" id="tjanster" aria-labelledby="tj-h">
  <div class="wrap">
    <h2 id="tj-h">Våra tjänster</h2>
    <ul class="cards">{cards}</ul>
    <h3 class="also-h">Vi tar också förfrågningar om</h3>
    <div class="btns">{ask_pills()}</div>
  </div>
</section>

<section class="sec tint" id="referens" aria-labelledby="ref-h">
  <div class="wrap narrow center">
    <h2 id="ref-h">Vad kunderna säger</h2>
    <p class="lead">{RATING} av 5 på Google ({REVIEW_COUNT} omdöme).</p>
    {review_block(center=True)}
  </div>
</section>

<section class="sec" id="om-oss" aria-labelledby="om-h">
  <div class="wrap split">
    {photo("snickeri", "Snickare sågar till en träbit i verkstaden")}
    <div>
      <h2 id="om-h">Ett lokalt byggföretag i Umeå</h2>
      <p class="lead">{NAME} är ett bygg- och snickeriföretag i Umeå. Vi renoverar och bygger om i villor och bostäder: kök, väggar, öppningar och snickeriet runt omkring.</p>
      <h3>Så går det till</h3>
      <ol class="steps">{steps}</ol>
      <div class="btns">{call_btn()}</div>
    </div>
  </div>
</section>

<section class="sec tint" id="kontakt" aria-labelledby="kt-h">
  <div class="wrap narrow">
    <h2 id="kt-h">Bli kontaktad av S-Bygg</h2>
    <p class="lead">Fyll i formuläret så hör vi av oss. Vill du hellre ringa går det bra, vi svarar {HOURS[0].lower() + HOURS[1:]}.</p>
    <div class="btns">{call_btn()}</div>
    <div id="offert">{quote_form()}</div>
  </div>
</section>

<section class="sec" id="fragor" aria-labelledby="fq-h">
  <div class="wrap narrow">
    <h2 id="fq-h">Vanliga frågor</h2>
    <div class="faq">{faq}</div>
  </div>
</section>

<section class="sec tint seo" aria-labelledby="seo-h">
  <div class="wrap narrow">
    <h2 id="seo-h">S-Bygg i Umeå</h2>
    <p>S-Bygg är en byggfirma i Umeå med inriktning på renovering och ombyggnad i bostäder. Vi gör <a href="tjanst-kok.html">köksrenoveringar i Umeå</a>, från nya luckor till totalrenovering, och <a href="tjanst-ombyggnad.html">ombyggnader och renoveringar</a> när planlösningen inte längre passar.</p>
    <p>Vill du öppna upp mellan två rum eller få en ny utgång till altanen tar vi upp <a href="tjanst-oppningar.html">nya öppningar och dörrar</a>. Ring {PHONE} eller <a href="#offert">begär en offert</a>, så tittar vi på jobbet.</p>
    <h3>Hitta hit</h3>
    <p>{NAME}, {ADDR}.</p>
    <div class="btns"><a class="pill pill-red" href="{MAPS_LINK}" target="_blank" rel="noopener">Öppna i Google Maps</a></div>
  </div>
</section>

<section class="map" aria-label="Karta">
  <iframe src="{MAP_EMBED}" title="Karta: {ADDR}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>'''
    page("index.html", "Snickare i Umeå – kök, ombyggnad, renovering | S-Bygg i Umeå AB",
         "S-Bygg i Umeå AB gör köksrenoveringar, ombyggnader och nya öppningar i villor och bostäder i Umeå. Ring 070-332 06 44 eller begär offert.",
         main, home=True)


# --- Service pages --------------------------------------------------------------------------------------------------
def service_page(s):
    items = "".join(f"<li>{i}</li>" for i in s["items"])
    body = "".join(f"<p>{p}</p>" for p in s["body"])
    review = f'<h2>Omdöme</h2>{review_block()}' if s["confirmed"] else ""
    others = "".join(card(o) for o in DONE if o["slug"] != s["slug"])
    main = f'''<section class="hero hero-small" aria-labelledby="ph-h">
  <div class="hero-ph">{img(s["photo"], s["alt"], s["pos"], lazy=False)}</div>
  <div class="wrap hero-in">
    <nav class="crumbs" aria-label="Brödsmulor"><a href="index.html">Start</a> / <a href="index.html#tjanster">Tjänster</a> / <span aria-current="page">{s["title"]}</span></nav>
    <h1 id="ph-h">{s["title"]} i Umeå</h1>
    <p>{s["short"]}</p>
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="index.html?typ={quote_plus(s["title"])}#offert">Begär offert</a></div>
  </div>
  <span class="hero-note">Illustrationsbild</span>
</section>
<section class="sec">
  <div class="wrap narrow prose">
    <h2>{s["title"]} med S-Bygg</h2>
    {body}
    <h3>Det kan ingå</h3>
    <ul class="list">{items}</ul>
    {review}
    <div class="btns">{call_btn()}<a class="pill pill-dark" href="index.html?typ={quote_plus(s["title"])}#offert">Begär offert</a></div>
  </div>
</section>
<section class="sec tint">
  <div class="wrap">
    <h2>Fler tjänster</h2>
    <ul class="cards">{others}</ul>
    <h3 class="also-h">Vi tar också förfrågningar om</h3>
    <div class="btns">{ask_pills(skip=s["slug"])}</div>
  </div>
</section>'''
    desc = f'{s["title"]} i Umeå. {s["short"]} S-Bygg i Umeå AB, telefon 070-332 06 44.'
    page(f'tjanst-{s["slug"]}.html', f'{s["title"]} i Umeå | S-Bygg i Umeå AB', desc, main, image=s["photo"])


def not_found():
    main = f'<section class="sec"><div class="wrap narrow"><h1>Sidan finns inte</h1><div class="btns"><a class="pill pill-dark" href="index.html">Till startsidan</a>{call_btn()}</div></div></section>'
    page("404.html", "Sidan finns inte | S-Bygg i Umeå AB", "Sidan kunde inte hittas.", main)


def seo_files():
    urls = ["index.html"] + [f'tjanst-{s["slug"]}.html' for s in SERVICES]
    locs = "".join(f"<url><loc>{SITE_URL}{'' if u == 'index.html' else u}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{locs}</urlset>\n', encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    index()
    for s in SERVICES:
        service_page(s)
    not_found()
    seo_files()
    print("Byggde", len(list(OUT.glob("*.html"))), "sidor i", OUT)
