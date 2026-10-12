"""Builds docs/*.html for S-Bygg i Umeå AB.

Run:  python3 scripts/build.py docs

All text, services, reviews and contact details live in this file. Anything marked
FÖRSLAG (suggestion) is generated copy that S-Bygg should confirm or edit before launch.
"""
import html
import json
import pathlib
import sys
from urllib.parse import quote_plus

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "docs")

# --- Verified company details (from Google Maps) -----------------------------------------------------------------
NAME = "S-Bygg i Umeå AB"
SHORT = "S-Bygg"
PHONE, TEL = "070-332 06 44", "+46703320644"
STREET, POSTAL, CITY = "Fatvägen", "906 20", "Umeå"
ADDR = f"{STREET}, {POSTAL} {CITY}"
PLUS_CODE = "V883+PQ Umeå"
RATING, REVIEW_COUNT = "5,0", 1
MAPS_LINK = "https://www.google.com/maps/search/?api=1&query=" + quote_plus(f"{NAME}, {ADDR}")
MAP_EMBED = "https://www.google.com/maps?q=" + quote_plus(ADDR) + "&z=14&hl=sv&output=embed"
# Google Maps only says the business closes at 16. Edit when the real hours are known.
HOURS = "Vi nås dagtid, fram till kl. 16."

# Not known yet: leave empty until verified, and nothing about them is shown.
EMAIL = ""
ORG_NR = ""

# Where the quote form sends its e-mail (FormSubmit, free). Elevate Studio receives the requests during the preview;
# at launch this becomes S-Bygg's own address. The first request to a new address only sends an activation e-mail.
FORM_EMAIL = "elevate.studio018@gmail.com"

SITE_URL = "https://elevatestudio018.github.io/S-Bygg/"

# --- Services -------------------------------------------------------------------------------------------------------
# confirmed=True: the work is described in the customer review on Google. confirmed=False: FÖRSLAG, typical carpentry
# work that S-Bygg should confirm, edit or remove before launch.
SERVICES = [
    dict(
        slug="kok", title="Köksrenovering", confirmed=True, icon="kitchen",
        photo="kok", pos="50% 55%", alt="Ljust kök med vita luckor och trägolv (illustrationsbild)",
        short="Från ett par nya luckor till en totalrenovering av hela köket.",
        lead="Köket är ofta det rum som betyder mest i ett hem – och det som tål minst slarv. Vi hjälper dig med köksrenovering i Umeå, från planering till färdigt resultat.",
        body=[
            "En köksrenovering kan vara allt från att byta ut några skåp till att riva ut och bygga upp hela köket på nytt. Vi har bland annat totalrenoverat köket i en Västerbottensvilla, där arbetet också omfattade en ny öppning med utgång till altanen.",
            "Vi går igenom vad du vill ha ut av köket, vad som behöver göras och i vilken ordning. Snickeriarbetet – rivning, regelverk, väggar, montering av stommar och luckor, lister och anpassningar – sköter vi. Behövs el, VVS eller andra yrkesgrupper pratar vi om hur det ska lösas i ditt projekt.",
        ],
        items=["Rivning av gammalt kök", "Nya väggar, regelverk och ytskikt", "Montering av köksstommar, luckor och bänkskivor",
               "Öppningar mot angränsande rum", "Lister, foder och de sista detaljerna"],
    ),
    dict(
        slug="ombyggnad", title="Ombyggnad och renovering", confirmed=True, icon="hammer",
        photo="ombyggnad", pos="50% 50%", alt="Rum under renovering med stegar och verktyg (illustrationsbild)",
        short="Ombyggnader i villor och bostäder – när planlösningen inte längre passar.",
        lead="Vill du göra om ett rum, ändra planlösningen eller renovera ett hus i flera steg? Vi tar oss an ombyggnader och renoveringar i bostäder i Umeå.",
        body=[
            "Många hus i Västerbotten är byggda för ett annat sätt att leva än i dag. Med en genomtänkt ombyggnad kan ett slutet kök bli en del av vardagsrummet, ett outnyttjat utrymme bli ett nytt rum eller en mörk hall få mer ljus.",
            "Vi går igenom ditt hus och dina önskemål tillsammans med dig, och föreslår hur arbetet kan läggas upp. Du får ett tydligt upplägg innan vi börjar, så att du vet vad som ska göras.",
        ],
        items=["Ändrad planlösning", "Nya innerväggar och rivning av väggar", "Renovering av rum i flera steg",
               "Byte av golv, väggar och innertak", "Anpassningar i äldre hus"],
    ),
    dict(
        slug="oppningar", title="Nya öppningar och dörrar", confirmed=True, icon="door",
        photo="dorr", pos="50% 45%", alt="Snickare som skruvar fast ett gångjärn i en dörrkarm (illustrationsbild)",
        short="Ta upp en ny öppning eller dörr – till exempel ut mot altanen.",
        lead="En ny öppning kan förändra ett helt hus. Vi har bland annat tagit upp en öppning med utgång från ett kök till en större altan i en Västerbottensvilla.",
        body=[
            "Att öppna upp mellan två rum eller ta upp en ny dörr ut till trädgården eller altanen är ett effektivt sätt att få mer ljus och ett bättre flöde i huset. Det kräver samtidigt noggrannhet, eftersom väggen ofta har en bärande funktion.",
            "Vi börjar med att se över väggen och förutsättningarna, och går igenom hur öppningen kan göras. Behöver konstruktionen räknas på eller något annat utredas tar vi upp det med dig innan arbetet startar.",
        ],
        items=["Öppningar mellan rum", "Nya dörrar ut till altan eller trädgård", "Avväxling och förstärkning av väggen",
               "Karmar, foder och tätning", "Återställning av ytorna runt öppningen"],
    ),
    dict(
        slug="altan", title="Altaner och trädäck", confirmed=False, icon="deck",
        photo="altan", pos="50% 60%", alt="Träaltan med räcke en höstdag (illustrationsbild)",
        short="Altaner, trädäck och arbeten där huset möter utemiljön.",
        lead="En altan förlänger sommaren – även i Umeå. Vi tar gärna emot förfrågningar om nya altaner, trädäck och arbeten i anslutning till befintliga altaner.",
        body=[
            "En bra altan börjar med en stabil grund och ett genomtänkt utförande. Läge, sol, höjd och hur altanen ansluter till huset påverkar hur mycket den kommer att användas.",
            "Berätta om dina planer, så går vi igenom vad som är möjligt och hur arbetet kan läggas upp. Vi kan också titta på hur en ny dörr eller öppning från huset kan göra altanen till en naturlig del av hemmet.",
        ],
        items=["Nya altaner och trädäck", "Utbyggnad av befintlig altan", "Räcken och trappor",
               "Ny utgång från huset till altanen", "Reparation av äldre trädäck"],
    ),
    dict(
        slug="tillbyggnad", title="Tillbyggnader", confirmed=False, icon="extend",
        photo="tillbyggnad", pos="50% 50%", alt="Regelstomme av trä under uppförande (illustrationsbild)",
        short="Mer utrymme genom att bygga till – ett nytt rum, ett uterum eller en entré.",
        lead="När huset börjar kännas för litet kan en tillbyggnad vara ett alternativ till att flytta. Vi tar gärna emot förfrågningar om tillbyggnader i Umeå med omnejd.",
        body=[
            "En tillbyggnad behöver passa både huset och tomten. Vi går igenom vad du vill uppnå och hur tillbyggnaden kan ansluta till det befintliga huset.",
            "Kräver projektet bygglov eller anmälan till kommunen ska det vara klart innan arbetet börjar. Vi pratar igenom vad som gäller för just ditt projekt när vi ses.",
        ],
        items=["Nya rum och sovrum", "Uterum och inglasningar", "Entréer och vindfång", "Förråd och garage", "Anslutning till befintligt hus"],
    ),
    dict(
        slug="inredning", title="Inredningssnickeri", confirmed=False, icon="square",
        photo="inredning", pos="50% 40%", alt="Snickare som mäter och märker upp ett trästycke (illustrationsbild)",
        short="Platsbyggda lösningar, golv, lister och de detaljer som gör det färdigt.",
        lead="Det är i detaljerna man ser hantverket. Vi tar gärna emot förfrågningar om inredningssnickeri och mindre snickeriarbeten i hemmet.",
        body=[
            "Platsbyggda garderober, bokhyllor, nischer och förvaring anpassas efter rummet i stället för tvärtom. Det ger lösningar som utnyttjar utrymmet fullt ut.",
            "Vi hjälper också till med golv, lister, foder, trappor och andra snickeriarbeten där noggrannheten avgör hur resultatet blir.",
        ],
        items=["Platsbyggd förvaring och garderober", "Golvläggning", "Lister, foder och socklar", "Trappor och räcken inomhus",
               "Mindre snickeriarbeten"],
    ),
]
WORK_TYPES = [s["title"] for s in SERVICES] + ["Annat byggprojekt"]

# --- Reviews --------------------------------------------------------------------------------------------------------
# Copied exactly from Google. The text ends where Google cut it off; the rest is not known, so it is not filled in.
REVIEWS = [
    dict(
        name="Magnus Eltoft", stars=5, when="Omdöme på Google",
        text="Vi anlitade byggfirman S-Bygg här i Umeå för ett tag sen när vi skulle göra en totalrenovering av köket i vår Västerbottensvilla, vart även så att de fick förtroendet med att göra en öppning med utgång från köket till en större altan med …",
        truncated=True,
        reply="Stort tack för förtroendet!",
    ),
]

FAQ = [
    ("Vilka typer av bygg- och snickeriarbeten kan jag fråga om?",
     "Vi har bland annat gjort köksrenoveringar, ombyggnader i bostäder och nya öppningar, till exempel en utgång från kök till altan. Du är välkommen att höra av dig även om andra bygg- och snickeriarbeten – berätta vad du planerar så säger vi om det är något vi kan hjälpa till med."),
    ("Hur kontaktar jag er?",
     f"Enklast är att ringa oss på <a href=\"tel:{TEL}\">{PHONE}</a>. Du kan också fylla i <a href=\"#offert\">formuläret</a> här på sidan, så hör vi av oss."),
    ("Kan jag begära en offert?",
     "Ja. Beskriv ditt projekt i formuläret eller ring oss. Ofta behöver vi se förutsättningarna på plats innan vi kan ge ett pris som stämmer."),
    ("Hur går det till att diskutera ett byggprojekt?",
     "Du berättar vad du har tänkt dig, och vi går igenom omfattning, önskemål och förutsättningar tillsammans. Sedan tar vi fram ett upplägg och, om det passar, en offert. Inget är bestämt förrän vi är överens."),
    ("Vilka områden arbetar ni i?",
     "Vi har vår bas i Umeå. Ligger ditt projekt utanför stan – hör av dig och berätta var, så säger vi om vi kan ta det."),
    ("Kan jag få ROT-avdrag?",
     "ROT-avdraget gäller arbetskostnaden för många reparationer, ombyggnader och tillbyggnader i bostäder. Vad som gäller i ditt fall går vi gärna igenom när vi pratar om offerten."),
]

STEPS = [
    ("Du hör av dig", "Ring eller skicka en förfrågan och berätta kort om ditt projekt – stort som litet."),
    ("Vi går igenom projektet", "Vi pratar om omfattning, önskemål och förutsättningar, gärna på plats hos dig."),
    ("Upplägg och offert", "Du får ett förslag på hur arbetet kan göras och, om det passar, en offert."),
    ("Arbetet genomförs", "Vi planerar och utför arbetet enligt det vi kommit överens om, och håller dig uppdaterad."),
]

# --- Shared pieces --------------------------------------------------------------------------------------------------
E = html.escape

ICONS = {
    "kitchen": '<path pathLength="1" d="M4 28V11h24v17M4 17h24M16 17v11"/><path pathLength="1" d="M10 4h12l3 7H7z"/><path pathLength="1" d="M11 21v3M21 21v3"/>',
    "hammer": '<path pathLength="1" d="M15 13 5.5 22.5a2.1 2.1 0 0 0 3 3L18 16"/><path pathLength="1" d="m12.5 10.5 6-6 2.5 1.2 1.5-1.5 5 5-1.5 1.5 1.2 2.5-4 4-9-9"/>',
    "door": '<path pathLength="1" d="M8 28V5h14v23M3 28h26"/><path pathLength="1" d="M18 17v.5"/><path pathLength="1" d="M22 9l5 2v15l-5 2"/>',
    "deck": '<path pathLength="1" d="M3 17h26M3 22h26M3 27h26"/><path pathLength="1" d="M6 27V9M26 27V9M6 9h20M11 17V9M16 17V9M21 17V9"/>',
    "extend": '<path pathLength="1" d="M3 28V14l9-8 9 8v14H3"/><path pathLength="1" d="M21 28h8V18h-8"/><path pathLength="1" d="M10 28v-7h4v7"/>',
    "square": '<path pathLength="1" d="M5 27V5h5v17h17v5z"/><path pathLength="1" d="M5 10h2M5 15h2M14 25v-2M19 25v-2"/>',
    "phone": '<path d="M21 16.5v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 1.1 3.8 2 2 0 0 1 3.1 1.6h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L7.1 9.5a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
}


def icon(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'


def phone_icon():
    return f'<svg class="pi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS["phone"]}</svg>'


CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>'
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="m10 1.6 2.6 5.4 5.9.8-4.3 4.1 1 5.9L10 15l-5.2 2.8 1-5.9L1.5 7.8l5.9-.8z"/></svg>'


def stars(n=5, label=None):
    label = label or f"{n} av 5 stjärnor"
    return f'<span class="stars" role="img" aria-label="{label}">{STAR * n}</span>'


# The mark: a gable over an S, like the roof line under the section headings.
LOGO = (f'<svg class="logo-svg" viewBox="0 0 178 44" aria-hidden="true">'
        '<path d="M3 41V19L21 5l18 14v22" fill="none" stroke="var(--oak)" stroke-width="3.2" stroke-linejoin="round"/>'
        '<text x="21" y="37" text-anchor="middle" class="lg-s">S</text>'
        '<text x="50" y="27" class="lg-name">S-Bygg</text>'
        '<text x="51" y="40.5" class="lg-sub">I UMEÅ AB</text></svg>')
FAVICON = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%231e3a2f'/>"
           "<path d='M5 27V14L16 5l11 9v13' fill='none' stroke='%23d39a5c' stroke-width='2.6' stroke-linejoin='round'/>"
           "<text x='16' y='25' text-anchor='middle' font-family='Arial,sans-serif' font-weight='700' font-size='13' fill='%23fbf9f5'>S</text></svg>")


def img(src, alt="", pos="50% 50%", sizes="100vw", lazy=True, cls="photo"):
    return (f'<img class="{cls}" src="img/{src}.jpg" srcset="img/{src}-s.jpg 800w, img/{src}.jpg 1800w" sizes="{sizes}" '
            f'alt="{E(alt)}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async" style="object-position:{pos}">')


NAV = [("tjanster", "Tjänster"), ("projekt", "Projekt"), ("omdomen", "Omdömen"), ("om-oss", "Om oss"), ("kontakt", "Kontakt")]


def header(home):
    pre = "" if home else "index.html"
    links = "".join(f'<a href="{pre}#{a}">{t}</a>' for a, t in NAV)
    rows = "".join(f'<li data-i><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    return f'''<a class="skip" href="#main">Hoppa till innehållet</a>
<header class="site-head" id="head">
  <div class="in bar">
    <a class="logo" href="{'#top' if home else 'index.html'}" aria-label="{NAME}, {'till toppen' if home else 'till startsidan'}">{LOGO}</a>
    <nav class="mainnav" aria-label="Huvudmeny">{links}</nav>
    <a class="callbtn" href="tel:{TEL}" aria-label="Ring {PHONE}">{phone_icon()}<span>{PHONE}</span></a>
    <a class="btn btn-oak navcta" href="{pre}#offert">Begär offert</a>
    <button class="burger" id="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Öppna menyn"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Meny" hidden>
  <div class="menu-panel">
    <div class="menu-top"><span class="tag">Meny</span><button class="menu-close" id="menuClose" type="button" aria-label="Stäng menyn"><svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 4l12 12M16 4 4 16"/></svg></button></div>
    <ul class="menu-rows">{rows}</ul>
    <div class="menu-foot" data-i>
      <p class="tag">Tjänster</p><ul class="menu-svc">{svc}</ul>
      <a class="btn btn-oak" href="{pre}#offert">Begär offert</a>
      <a class="btn btn-line-light" href="tel:{TEL}">{phone_icon()} {PHONE}</a>
    </div>
  </div>
</div>'''


def footer(home):
    pre = "" if home else "index.html"
    svc = "".join(f'<li><a href="tjanst-{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES)
    links = "".join(f'<li><a href="{pre}#{a}">{t}</a></li>' for a, t in NAV)
    extra = (f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>' if EMAIL else "")
    org = f" · Org.nr {ORG_NR}" if ORG_NR else ""
    return f'''<section class="fcta" aria-labelledby="fcta-h">
  <div class="in">
    <div><h2 id="fcta-h">Har du ett byggprojekt på gång?</h2><p>Berätta om det, så hör vi av oss. Eller ring oss direkt på {PHONE}.</p></div>
    <div class="fcta-btns"><a class="btn btn-oak" href="{pre}#offert">Begär offert</a><a class="btn btn-line-light" href="tel:{TEL}">{phone_icon()} Ring oss</a></div>
  </div>
</section>
<footer class="site-foot">
  <div class="in">
    <div class="fgrid">
      <div class="fabout">
        <a class="logo" href="{pre or '#top'}" aria-label="{NAME}, till startsidan">{LOGO}</a>
        <p>Bygg- och snickeriarbeten i Umeå – köksrenoveringar, ombyggnader och nya öppningar i bostäder.</p>
      </div>
      <div><h2 class="fh">Kontakt</h2><ul>
        <li><a href="tel:{TEL}">{phone_icon()} {PHONE}</a></li>{extra}
        <li><a href="{MAPS_LINK}" target="_blank" rel="noopener">{ADDR}</a></li></ul></div>
      <div><h2 class="fh">Tjänster</h2><ul>{svc}</ul></div>
      <div><h2 class="fh">Sidan</h2><ul>{links}</ul></div>
    </div>
    <div class="fbottom">
      <span>© <span data-year>2026</span> {NAME}{org} · Foton: Pexels (illustrationsbilder)</span>
      <a class="credit" href="https://elevatestudio.nu" target="_blank" rel="noopener"><span class="mark" aria-hidden="true"></span>Byggd av Elevate Studio</a>
    </div>
  </div>
</footer>
<script src="assets/site.js" defer></script>
</body>
</html>
'''


def jsonld():
    data = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": NAME,
        "url": SITE_URL,
        "telephone": TEL,
        "image": SITE_URL + "img/hero-renovering.jpg",
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
<meta name="theme-color" content="#1e3a2f">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&family=Figtree:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/site.css">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="data:image/svg+xml,{FAVICON}">
{jsonld() if home else ''}
</head>
<body{' class="home"' if home else ''}>
{header(home)}
<main id="main"{' class="top-anchor"' if home else ''}>
{main}
</main>
{footer(home)}'''
    (OUT / name).write_text(doc, encoding="utf-8")


def head2(eyebrow, title, hid, center=False, extra=""):
    return (f'<div class="sh{" center" if center else ""}" data-reveal><span class="eyebrow">{eyebrow}</span>'
            f'<h2 class="h2" id="{hid}">{title}</h2>{extra}</div>')


def ruler():
    # The carpenter's folding rule along the foot of the hero: ticks every centimetre, numbers every ten.
    nums = "".join(f"<span>{n}</span>" for n in range(10, 210, 10))
    return f'<div class="ruler" aria-hidden="true"><div class="ruler-nums">{nums}</div></div>'


def service_card(s, i, prefix=""):
    tag = '<span class="ref">Utfört åt kund</span>' if s["confirmed"] else ""
    return (f'<a class="card" href="{prefix}tjanst-{s["slug"]}.html" data-reveal style="--d:{(i % 3) * 80}ms">'
            f'<div class="card-ph">{img(s["photo"] + "", s["alt"], s["pos"], "(min-width: 1100px) 400px, (min-width: 640px) 50vw, 100vw")}{tag}</div>'
            f'<div class="card-body"><span class="draw">{icon(s["icon"])}</span><h3>{s["title"]}</h3><p>{s["short"]}</p>'
            f'<span class="more">Läs mer{CHEV}</span></div></a>')


def review_cards():
    out = []
    for r in REVIEWS:
        more = (f' <a class="rv-more" href="{MAPS_LINK}" target="_blank" rel="noopener">Läs hela omdömet på Google</a>'
                if r.get("truncated") else "")
        reply = (f'<div class="rv-reply"><b>Svar från {SHORT}</b><p>”{E(r["reply"])}”</p></div>' if r.get("reply") else "")
        initials = "".join(p[0] for p in r["name"].split()[:2])
        out.append(f'''<figure class="rv" data-reveal>
  <div class="rv-top">{stars(r["stars"])}<span class="rv-src">{r["when"]}</span></div>
  <blockquote><p>”{E(r["text"])}”</p></blockquote>{more}
  <figcaption><span class="av" aria-hidden="true">{initials}</span><span><b>{E(r["name"])}</b><small>{r["stars"]} av 5 stjärnor</small></span></figcaption>
  {reply}
</figure>''')
    return "".join(out)


def quote_form():
    opts = "".join(f'<option>{E(t)}</option>' for t in WORK_TYPES)
    return f'''<form class="qform" id="qform" novalidate data-endpoint="https://formsubmit.co/ajax/{FORM_EMAIL}" data-phone="{PHONE}">
  <div class="f2">
    <div class="field"><label for="f-namn">Namn <span class="req" aria-hidden="true">*</span></label><input id="f-namn" name="Namn" autocomplete="name" required><p class="err" id="e-namn" hidden>Skriv ditt namn.</p></div>
    <div class="field"><label for="f-tel">Telefonnummer</label><input id="f-tel" name="Telefon" type="tel" autocomplete="tel" inputmode="tel"><p class="err" id="e-tel" hidden>Skriv ett telefonnummer eller en e-postadress.</p></div>
  </div>
  <div class="f2">
    <div class="field"><label for="f-epost">E-postadress</label><input id="f-epost" name="E-post" type="email" autocomplete="email"><p class="err" id="e-epost" hidden>Kontrollera e-postadressen.</p></div>
    <div class="field"><label for="f-typ">Typ av byggprojekt</label><select id="f-typ" name="Typ av byggprojekt"><option value="">Välj …</option>{opts}</select></div>
  </div>
  <div class="field"><label for="f-besk">Beskrivning av projektet</label><textarea id="f-besk" name="Beskrivning" rows="5" placeholder="Vad vill du göra, var ligger det och när vill du komma igång?"></textarea></div>
  <div class="hp" aria-hidden="true"><label for="f-web">Lämna tomt</label><input id="f-web" name="_honey" tabindex="-1" autocomplete="off"></div>
  <p class="fnote">Fyll i telefonnummer eller e-post så att vi kan nå dig. Uppgifterna används bara för att svara på din förfrågan.</p>
  <button class="btn btn-oak btn-wide" type="submit"><span class="bt">Skicka förfrågan</span></button>
  <p class="send-err" id="send-err" role="alert" hidden>Förfrågan kunde inte skickas just nu. Försök igen om en stund, eller ring oss på <a href="tel:{TEL}">{PHONE}</a>.</p>
</form>
<div class="qdone" id="qdone" tabindex="-1" hidden>
  <span class="qdone-ic" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path pathLength="1" d="m8 16.5 5.5 5.5L25 10"/></svg></span>
  <h3>Tack! Vi har tagit emot din förfrågan.</h3>
  <p>Vi hör av oss så snart vi kan. Vill du prata redan nu går det bra att ringa oss på <a href="tel:{TEL}">{PHONE}</a>.</p>
  <button class="lnk" type="button" id="qagain">Skicka en ny förfrågan</button>
</div>'''


# --- Start page -----------------------------------------------------------------------------------------------------
def index():
    cards = "".join(service_card(s, i) for i, s in enumerate(SERVICES))
    steps = "".join(f'<li data-reveal style="--d:{i * 90}ms"><span class="num">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></li>'
                    for i, (t, d) in enumerate(STEPS))
    faq = "".join(f'<details data-reveal><summary>{q}<span class="pm" aria-hidden="true"></span></summary><div class="ans"><p>{a}</p></div></details>'
                  for q, a in FAQ)
    main = f'''<section class="hero" aria-labelledby="hero-h">
  <div class="hero-grid">
    <div class="hero-copy">
      <p class="eyebrow light rise" style="--d:100ms">Snickare och byggföretag i Umeå</p>
      <h1 id="hero-h" class="rise" style="--d:220ms">Bygg- och snickeri&shy;arbeten <em>i Umeå</em></h1>
      <p class="hero-lead rise" style="--d:340ms">Planerar du en renovering eller ett nytt byggprojekt? Kontakta {NAME} så pratar vi om dina idéer och hittar en lösning som passar ditt hem.</p>
      <div class="hero-btns rise" style="--d:460ms">
        <a class="btn btn-oak" href="#offert">Begär offert</a>
        <a class="btn btn-line-light" href="tel:{TEL}">{phone_icon()} Ring {PHONE}</a>
      </div>
      <a class="hero-rating rise" style="--d:580ms" href="#omdomen">{stars(5, f"Betyg {RATING} av 5 på Google")}<span><b>{RATING}</b> på Google · {REVIEW_COUNT} omdöme</span></a>
    </div>
    <div class="hero-ph">
      {img("hero-renovering", "Snickare i ett hus under ombyggnad med regelstomme och nya bjälklag (illustrationsbild)", "50% 50%", "(min-width: 960px) 50vw, 100vw", lazy=False, cls="photo parallax-top")}
      <span class="ph-note">Illustrationsbild</span>
    </div>
  </div>
  {ruler()}
</section>

<section class="sec" id="tjanster" aria-labelledby="tj-h">
  <div class="in">
    {head2("Tjänster", "Det här kan vi hjälpa dig med", "tj-h", extra='<p class="sh-lead">Köksrenoveringar, ombyggnader och nya öppningar i bostäder har vi gjort åt kunder i Umeå. Hör gärna av dig om andra bygg- och snickeriarbeten också.</p>')}
    <div class="cards">{cards}</div>
  </div>
</section>

<section class="sec about" id="om-oss" aria-labelledby="om-h">
  <div class="in about-grid">
    <div class="about-ph" data-reveal>
      <div class="frame">{img("matt", "Snickare som mäter en planka med tumstock och måttband (illustrationsbild)", "50% 50%", "(min-width: 960px) 45vw, 100vw")}</div>
      <div class="frame small">{img("hus-vasterbotten", "Rött trähus i Skellefteå, Västerbotten (illustrationsbild)", "50% 60%", "(min-width: 960px) 20vw, 40vw")}</div>
    </div>
    <div class="about-txt">
      {head2("Om oss", "Ett lokalt byggföretag i Umeå", "om-h")}
      <p class="lead" data-reveal>{NAME} är ett bygg- och snickeriföretag med bas i Umeå. Vi arbetar med renoveringar och ombyggnader i bostäder – från ett nytt kök till en öppning som förändrar hur hela huset används.</p>
      <p data-reveal>Som kund ska du veta vad som ska göras, varför och i vilken ordning. Därför börjar vi alltid med att lyssna och gå igenom förutsättningarna tillsammans med dig, innan något arbete planeras. Sedan gör vi jobbet ordentligt – med samma noggrannhet i detaljerna som i stommen.</p>
      <ul class="values" data-reveal>
        <li><b>Tydlig dialog</b><span>Du vet vad som händer i ditt projekt.</span></li>
        <li><b>Noggrant hantverk</b><span>Rätt gjort från regel till list.</span></li>
        <li><b>Lokalt i Umeå</b><span>Nära till dig och ditt hus.</span></li>
      </ul>
    </div>
  </div>
</section>

<section class="sec projects" id="projekt" aria-labelledby="pr-h">
  <div class="in">
    {head2("Projekt och referenser", "Ett kök som öppnades mot altanen", "pr-h")}
    <article class="feat" data-reveal>
      <div class="feat-ph">{img("kok-2", "Ljust kök med köksö och trägolv (illustrationsbild)", "50% 50%", "(min-width: 960px) 60vw, 100vw")}<span class="ph-note">Illustrationsbild</span></div>
      <div class="feat-body">
        <span class="tag">Referens · Umeå</span>
        <h3>Totalrenovering av kök i Västerbottensvilla</h3>
        <p>En kund i Umeå anlitade oss för att totalrenovera köket i sin Västerbottensvilla. I uppdraget ingick också att göra en öppning med utgång från köket till en större altan.</p>
        <ul class="feat-list"><li>Totalrenovering av kök</li><li>Ny öppning med utgång till altan</li></ul>
        <p class="feat-quote">”…vart även så att de fick förtroendet med att göra en öppning med utgång från köket till en större altan…” <span>– Magnus Eltoft, på Google</span></p>
        <a class="arrow" href="tjanst-kok.html">Läs om köksrenovering{CHEV}</a>
      </div>
    </article>
    <div class="gallery" data-reveal>
      <a href="tjanst-oppningar.html">{img("fonster", "Hantverkare som monterar en fönsterkarm (illustrationsbild)", "50% 40%", "(min-width: 960px) 33vw, 50vw")}<span>Öppningar och dörrar</span></a>
      <a href="tjanst-altan.html">{img("altan-2", "Trädäck vid ett modernt hus (illustrationsbild)", "50% 60%", "(min-width: 960px) 33vw, 50vw")}<span>Altaner</span></a>
      <a href="tjanst-inredning.html">{img("snickeri", "Snickare som sågar till trä i verkstaden (illustrationsbild)", "50% 50%", "(min-width: 960px) 33vw, 50vw")}<span>Snickeri</span></a>
    </div>
    <p class="caption">Bilderna i det här avsnittet är illustrationsbilder. Bilder från våra egna projekt kommer att läggas upp här.</p>
  </div>
</section>

<section class="sec reviews" id="omdomen" aria-labelledby="rv-h">
  <div class="in">
    {head2("Omdömen", "Vad våra kunder säger", "rv-h", center=True, extra=f'<p class="sh-lead">{stars(5, f"Betyg {RATING} av 5")} <b>{RATING} av 5</b> på Google, baserat på {REVIEW_COUNT} omdöme.</p>')}
    <div class="rv-grid">{review_cards()}</div>
  </div>
</section>

<section class="band" aria-labelledby="band-h">
  <div class="band-ph">{img("altan", "", "50% 60%")}</div>
  <div class="in band-in" data-reveal>
    <span class="eyebrow light">Kök, öppningar och altan</span>
    <h2 id="band-h">Ett hem som hänger ihop – inne som ute</h2>
    <p>En ny öppning mot altanen kan göra mer för huset än man tror. Vi hjälper dig att se möjligheterna och att få det gjort ordentligt.</p>
    <a class="btn btn-oak" href="tjanst-oppningar.html">Läs om nya öppningar</a>
  </div>
</section>

<section class="sec process" id="sa-jobbar-vi" aria-labelledby="ps-h">
  <div class="in">
    {head2("Arbetsprocess", "Så går det till", "ps-h", extra='<p class="sh-lead">Så här brukar ett uppdrag se ut. Varje projekt är olika, och vi anpassar upplägget efter ditt.</p>')}
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="sec faq" id="fragor" aria-labelledby="fq-h">
  <div class="in faq-grid">
    <div>{head2("Vanliga frågor", "Undrar du något?", "fq-h", extra=f'<p class="sh-lead">Hittar du inte svaret här? Ring oss på <a href="tel:{TEL}">{PHONE}</a>.</p>')}</div>
    <div class="faq-list">{faq}</div>
  </div>
</section>

<section class="sec contact" id="kontakt" aria-labelledby="kt-h">
  <div class="in contact-grid">
    <div>
      {head2("Kontakt", "Berätta om ditt projekt", "kt-h")}
      <p class="lead" data-reveal>Ring oss eller skicka en förfrågan, så hör vi av oss för att prata om vad du har tänkt dig.</p>
      <ul class="crows" data-reveal>
        <li><span class="ci">{phone_icon()}</span><span><small>Telefon</small><a href="tel:{TEL}">{PHONE}</a></span></li>
        <li><span class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg></span><span><small>Adress</small><b>{ADDR}</b></span></li>
        <li><span class="ci"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><span><small>Tider</small><b>{HOURS}</b></span></li>
      </ul>
      <a class="btn btn-forest call-big" href="tel:{TEL}" data-reveal>{phone_icon()} Ring {PHONE}</a>
    </div>
    <div class="form-card" id="offert" data-reveal>
      <h3>Begär offert</h3>
      <p class="fc-lead">Beskriv ditt projekt så återkommer vi.</p>
      {quote_form()}
    </div>
  </div>
</section>

<section class="map" aria-labelledby="map-h">
  <h2 class="sr" id="map-h">Här finns vi</h2>
  <div class="map-frame"><iframe src="{MAP_EMBED}" title="Karta: {NAME}, {ADDR}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  <div class="map-bar"><div class="in"><p><span class="pin" aria-hidden="true"></span>{NAME} · {ADDR}</p><a class="arrow" href="{MAPS_LINK}" target="_blank" rel="noopener">Öppna i Google Maps{CHEV}</a></div></div>
</section>'''
    page("index.html", "Snickare i Umeå – bygg och renovering | S-Bygg i Umeå AB",
         "S-Bygg i Umeå AB utför bygg- och snickeriarbeten i Umeå: köksrenovering, ombyggnad och nya öppningar i bostäder. Ring 070-332 06 44 eller begär offert.",
         main, home=True)


# --- Service pages --------------------------------------------------------------------------------------------------
def service_page(s):
    items = "".join(f"<li>{i}</li>" for i in s["items"])
    body = "".join(f'<p data-reveal>{p}</p>' for p in s["body"])
    others = [o for o in SERVICES if o["slug"] != s["slug"]][:3]
    rel = "".join(service_card(o, i) for i, o in enumerate(others))
    note = ("" if s["confirmed"] else
            '<p class="sv-note">Vi tar gärna emot förfrågningar om den här typen av arbete. Berätta om ditt projekt så säger vi om det är något vi kan hjälpa till med.</p>')
    ref = ""
    if s["confirmed"]:
        r = REVIEWS[0]
        ref = (f'<figure class="sv-ref" data-reveal>{stars(5)}<blockquote><p>”{E(r["text"])}”</p></blockquote>'
               f'<figcaption>{E(r["name"])}, omdöme på Google</figcaption></figure>')
    main = f'''<section class="phero" aria-labelledby="ph-h">
  <div class="phero-ph">{img(s["photo"], s["alt"], s["pos"], lazy=False, cls="photo parallax-top")}</div>
  <div class="in phero-in">
    <nav class="crumbs" aria-label="Brödsmulor"><a href="index.html">Start</a><span aria-hidden="true">/</span><a href="index.html#tjanster">Tjänster</a><span aria-hidden="true">/</span><span aria-current="page">{s["title"]}</span></nav>
    <h1 id="ph-h" class="rise" style="--d:150ms">{s["title"]} <em>i Umeå</em></h1>
    <p class="rise" style="--d:280ms">{s["short"]}</p>
  </div>
  {ruler()}
</section>
<section class="sec">
  <div class="in sv-grid">
    <div class="sv-main">
      <p class="lead" data-reveal>{s["lead"]}</p>
      {body}
      {note}
      <h2 class="h2 sm" data-reveal>Det här kan ingå</h2>
      <ul class="checks" data-reveal>{items}</ul>
      {ref}
    </div>
    <aside class="sv-aside" data-reveal>
      <span class="draw big">{icon(s["icon"])}</span>
      <h2>Prata med oss om ditt projekt</h2>
      <p>Berätta vad du har tänkt dig, så hör vi av oss.</p>
      <a class="btn btn-oak btn-wide" href="index.html?typ={quote_plus(s["title"])}#offert">Begär offert</a>
      <a class="btn btn-line btn-wide" href="tel:{TEL}">{phone_icon()} {PHONE}</a>
      <p class="aside-small">{ADDR}</p>
    </aside>
  </div>
</section>
<section class="sec tint">
  <div class="in">
    {head2("Fler tjänster", "Annat vi kan hjälpa till med", "more-h")}
    <div class="cards">{rel}</div>
  </div>
</section>'''
    desc = f'{s["title"]} i Umeå. {s["short"]} Kontakta S-Bygg i Umeå AB på 070-332 06 44 för att diskutera ditt projekt.'
    page(f'tjanst-{s["slug"]}.html', f'{s["title"]} i Umeå | S-Bygg i Umeå AB', desc, main, image=s["photo"])


def not_found():
    main = '''<section class="phero plain"><div class="in phero-in"><h1>Sidan finns inte</h1><p>Sidan du letar efter kan ha flyttats eller tagits bort.</p><p style="margin-top:24px"><a class="btn btn-oak" href="index.html">Till startsidan</a></p></div></section>'''
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
