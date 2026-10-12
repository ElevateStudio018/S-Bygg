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
ARROW = '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 12h15M13 6l6 6-6 6"/></svg>'
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m10 1.6 2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 15l-5.2 2.8 1-5.9L1.5 7.8l5.9-.8z"/></svg>'
FAVICON = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' fill='%23141414'/>"
           "<text x='16' y='23.5' text-anchor='middle' font-family='Arial,sans-serif' font-weight='700' font-size='20' fill='%23ffffff'>S</text>"
           "<rect x='0' y='28' width='32' height='4' fill='%23d2451e'/></svg>")


def stars(n=5):
    return f'<span class="stars" role="img" aria-label="{n} av 5 stjärnor">{STAR * n}</span>'


def img(src, alt="", pos="50% 50%", sizes="100vw", lazy=True):
    return (f'<img src="img/{src}.jpg" srcset="img/{src}-s.jpg 800w, img/{src}.jpg 1800w" sizes="{sizes}" '
            f'alt="{E(alt)}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async" style="object-position:{pos}">')


def logo():
    return '<span class="wm">S-Bygg<small>i Umeå AB</small></span>'


NAV = [("tjanster", "Tjänster"), ("referens", "Referens"), ("om", "Om oss"), ("kontakt", "Kontakt")]


def header(home):
    pre = "" if home else "index.html"
    links = "".join(f'<a href="{pre}#{a}">{t}</a>' for a, t in NAV)
    rows = "".join(f'<li><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)
    return f'''<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="head">
  <div class="wrap bar">
    <a class="logo" href="{'#top' if home else 'index.html'}" aria-label="{NAME}, till startsidan">{logo()}</a>
    <nav class="nav" aria-label="Huvudmeny">{links}</nav>
    <a class="tel" href="tel:{TEL}">{PHONE}</a>
    <a class="btn btn-go head-cta" href="{pre}#offert">Begär offert</a>
    <button class="menu-btn" id="menuBtn" type="button" aria-expanded="false" aria-controls="menu">Meny</button>
  </div>
  <nav class="menu" id="menu" aria-label="Meny" hidden>
    <ul class="wrap">{rows}<li><a href="tel:{TEL}">Ring {PHONE}</a></li></ul>
  </nav>
</header>'''


def footer(home):
    pre = "" if home else "index.html"
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    mail = f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>' if EMAIL else ""
    org = f"<li>Org.nr {ORG_NR}</li>" if ORG_NR else ""
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><a class="logo" href="{pre or '#top'}">{logo()}</a></div>
      <ul><li><a href="tel:{TEL}">{PHONE}</a></li>{mail}<li><a href="{MAPS_LINK}" target="_blank" rel="noopener">{ADDR}</a></li>{org}</ul>
      <ul>{svc}</ul>
      <ul>{"".join(f'<li><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)}<li><a href="{pre}#offert">Begär offert</a></li></ul>
    </div>
    <div class="foot-end">
      <span>© <span data-year>2026</span> {NAME}. Bilderna är stockfoton från Pexels.</span>
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
<meta name="theme-color" content="#141414">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="data:image/svg+xml,{FAVICON}">
{jsonld() if home else ''}
</head>
<body>
{header(home)}
<main id="main">
{main}
</main>
{footer(home)}'''
    (OUT / name).write_text(doc, encoding="utf-8")


def section(sid, title, body, cls=""):
    """Every section: a rule across the page, the heading in the left column, the content in the right."""
    return (f'<section class="sec {cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap cols">'
            f'<h2 id="{sid}-h">{title}</h2><div class="body">{body}</div></div></section>')


def service_row(s):
    return (f'<li><a class="row" href="tjanst-{s["slug"]}.html"><span class="row-ph">{img(s["photo"], "", s["pos"], "160px")}</span>'
            f'<span class="row-t"><b>{s["title"]}</b><span>{s["short"]}</span></span>{ARROW}</a></li>')


def review_block():
    out = []
    for r in REVIEWS:
        more = (f'<a href="{MAPS_LINK}" target="_blank" rel="noopener">Läs hela omdömet på Google</a>' if r.get("truncated") else "")
        reply = f'<p class="reply"><b>S-Bygg svarade:</b> ”{E(r["reply"])}”</p>' if r.get("reply") else ""
        out.append(f'<figure class="review">{stars(r["stars"])}<blockquote><p>”{E(r["text"])}”</p></blockquote>'
                   f'<figcaption>{E(r["name"])}, Google · {more}</figcaption>{reply}</figure>')
    return "".join(out)


def quote_form():
    opts = "".join(f"<option>{E(t)}</option>" for t in WORK_TYPES)
    return f'''<form class="form" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}">
  <div class="f2">
    <p class="field"><label for="f-namn">Namn</label><input id="f-namn" name="Namn" autocomplete="name" required><span class="err" id="e-namn" hidden>Skriv ditt namn.</span></p>
    <p class="field"><label for="f-tel">Telefon</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel"><span class="err" id="e-tel" hidden>Skriv telefon eller e-post.</span></p>
  </div>
  <div class="f2">
    <p class="field"><label for="f-epost">E-post</label><input id="f-epost" name="E-post" type="email" autocomplete="email"><span class="err" id="e-epost" hidden>Kontrollera e-postadressen.</span></p>
    <p class="field"><label for="f-typ">Typ av jobb</label><select id="f-typ" name="Typ av byggprojekt"><option value="">Välj</option>{opts}</select></p>
  </div>
  <p class="field"><label for="f-besk">Beskriv jobbet</label><textarea id="f-besk" name="Beskrivning" rows="5" placeholder="Vad ska göras, var och när?"></textarea></p>
  <p class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="_honey" tabindex="-1" autocomplete="off"></p>
  <p class="form-end"><button class="btn btn-go" type="submit">Skicka</button><span>Telefon eller e-post räcker. Vi använder uppgifterna bara för att svara dig.</span></p>
  <p class="send-err" id="send-err" role="alert" hidden>Det gick inte att skicka just nu. Försök igen, eller ring <a href="tel:{TEL}">{PHONE}</a>.</p>
</form>
<div class="done" id="qdone" tabindex="-1" hidden>
  <p class="done-h">Tack, vi har fått din förfrågan.</p>
  <p>Vi hör av oss så snart vi kan. Brådskar det, ring <a href="tel:{TEL}">{PHONE}</a>.</p>
  <button class="link" type="button" id="qagain">Skicka en till</button>
</div>'''


# --- Start page -----------------------------------------------------------------------------------------------------
def index():
    done = "".join(service_row(s) for s in DONE)
    ask = ", ".join(f'<a href="tjanst-{s["slug"]}.html">{s["title"].lower() if i else s["title"]}</a>' for i, s in enumerate(ASK))
    steps = "".join(f"<li><b>{t}</b><span>{d}</span></li>" for t, d in STEPS)
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)

    tjanster = f'''<ul class="rows">{done}</ul>
<p class="also">Fråga oss också om {ask}.</p>'''

    referens = f'''<figure class="ref-ph">{img("kok-2", "Ljust kök med köksö och trägolv", "50% 50%", "(min-width: 960px) 66vw, 100vw")}<figcaption>Illustrationsbild, inte från projektet.</figcaption></figure>
<h3>Kök i Västerbottensvilla, Umeå</h3>
<p class="ref-txt">Totalrenovering av köket och en ny öppning med utgång från köket till en större altan.</p>
{review_block()}
<p class="rating">{stars()} {RATING} av 5 på Google ({REVIEW_COUNT} omdöme)</p>'''

    om = f'''<div class="om">
  <div>
    <p class="big">{NAME} är ett bygg- och snickeriföretag i Umeå. Vi renoverar och bygger om i villor och bostäder: kök, väggar, öppningar och snickeriet runt omkring.</p>
    <h3>Så går det till</h3>
    <ol class="steps">{steps}</ol>
  </div>
  <figure>{img("snickeri", "Snickare sågar till en träbit i verkstaden", "50% 50%", "(min-width: 960px) 33vw, 100vw")}<figcaption>Illustrationsbild.</figcaption></figure>
</div>'''

    fragor = f'<div class="faq">{faq}</div>'

    kontakt = f'''<div class="kontakt">
  <div>
    <a class="phone" href="tel:{TEL}">{PHONE}</a>
    <dl class="facts"><div><dt>Adress</dt><dd>{ADDR}</dd></div><div><dt>Tider</dt><dd>{HOURS}</dd></div></dl>
  </div>
  <div id="offert"><h3>Begär offert</h3>{quote_form()}</div>
</div>'''

    main = f'''<section class="hero" id="top" aria-labelledby="hero-h">
  <div class="hero-ph">{img("hero-renovering", "Snickare i ett hus under ombyggnad", "50% 45%", lazy=False)}</div>
  <div class="wrap hero-in">
    <h1 id="hero-h">Snickare i Umeå</h1>
    <p>Köksrenoveringar, ombyggnader och nya öppningar i villor och bostäder.</p>
    <p class="hero-btns"><a class="btn btn-go" href="#offert">Begär offert</a><a class="btn btn-ghost" href="tel:{TEL}">Ring {PHONE}</a></p>
    <a class="hero-rate" href="#referens">{stars()} {RATING} på Google</a>
  </div>
  <span class="hero-note">Illustrationsbild</span>
</section>
{section("tjanster", "Tjänster", tjanster)}
{section("referens", "Referens", referens)}
{section("om", "Om oss", om)}
{section("fragor", "Vanliga frågor", fragor)}
{section("kontakt", "Kontakt", kontakt, "dark")}
<section class="map" aria-label="Karta">
  <iframe src="{MAP_EMBED}" title="Karta: {ADDR}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  <p class="wrap"><a href="{MAPS_LINK}" target="_blank" rel="noopener">Öppna i Google Maps {ARROW}</a></p>
</section>'''
    page("index.html", "Snickare i Umeå – kök, ombyggnad, renovering | S-Bygg i Umeå AB",
         "S-Bygg i Umeå AB gör köksrenoveringar, ombyggnader och nya öppningar i villor och bostäder i Umeå. Ring 070-332 06 44 eller begär offert.",
         main, home=True)


# --- Service pages --------------------------------------------------------------------------------------------------
def service_page(s):
    items = "".join(f"<li>{i}</li>" for i in s["items"])
    body = "".join(f"<p>{p}</p>" for p in s["body"])
    review = ""
    if s["confirmed"]:
        review = f'<h3>Omdöme</h3>{review_block()}'
    others = "".join(service_row(o) for o in SERVICES if o["slug"] != s["slug"])
    content = f'''<div class="svc">
  <div class="prose">{body}
    <h3>Det kan ingå</h3><ul class="list">{items}</ul>
    {review}
  </div>
  <aside class="svc-side">
    <a class="btn btn-go" href="index.html?typ={quote_plus(s["title"])}#offert">Begär offert</a>
    <a class="btn btn-line" href="tel:{TEL}">Ring {PHONE}</a>
  </aside>
</div>'''
    main = f'''<section class="phero" aria-labelledby="ph-h">
  <div class="wrap">
    <nav class="crumbs" aria-label="Brödsmulor"><a href="index.html">Start</a> / <a href="index.html#tjanster">Tjänster</a> / <span aria-current="page">{s["title"]}</span></nav>
    <h1 id="ph-h">{s["title"]} i Umeå</h1>
    <p>{s["short"]}</p>
  </div>
  <figure class="wrap phero-ph">{img(s["photo"], s["alt"], s["pos"], lazy=False)}<figcaption>Illustrationsbild.</figcaption></figure>
</section>
{section("om-jobbet", "Om jobbet", content)}
{section("fler", "Fler tjänster", f'<ul class="rows">{others}</ul>')}'''
    desc = f'{s["title"]} i Umeå. {s["short"]} S-Bygg i Umeå AB, telefon 070-332 06 44.'
    page(f'tjanst-{s["slug"]}.html', f'{s["title"]} i Umeå | S-Bygg i Umeå AB', desc, main, image=s["photo"])


def not_found():
    main = '<section class="phero"><div class="wrap"><h1>Sidan finns inte</h1><p><a href="index.html">Till startsidan</a></p></div></section>'
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
