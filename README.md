# S-Bygg i Umeå AB – webbplats

Ny webbplats för S-Bygg i Umeå AB (bygg och snickeri i Umeå), byggd på Stenvaller-mallen men avskalad:
vitt, svart och grått, en enda signalorange som bara används på knapparna till offert, ett typsnitt (Archivo),
raka hörn, inga skuggor, inga ikoner i cirklar, inga dekorativa etiketter och inga animationer. Varje sektion har
en linje överst, rubriken i vänster kolumn och innehållet i höger.

## Sidor

Allt ligger i [`docs/`](docs/) och kräver inga verktyg – öppna `docs/index.html` i en webbläsare.

- `index.html` – startsidan: hero, tjänster, referens med kundomdöme, om oss med arbetsgång, vanliga frågor,
  kontakt med offertformulär och karta
- sex tjänstesidor: `tjanst-kok.html`, `tjanst-ombyggnad.html`, `tjanst-oppningar.html`, `tjanst-altan.html`,
  `tjanst-tillbyggnad.html`, `tjanst-inredning.html`
- `404.html`, `sitemap.xml`, `robots.txt`

## Ändra text

Sidorna genereras av `scripts/build.py`, där all text, alla tjänster, omdömen och kontaktuppgifter finns. Ändra där och kör:

```bash
python3 scripts/build.py docs
```

## Fakta och förslag – gå igenom före lansering

**Verifierat** (från Google Maps): företagsnamn, telefon 070-332 06 44, Fatvägen, 906 20 Umeå, betyg 5,0
(1 omdöme), omdömet från Magnus Eltoft och svaret ”Stort tack för förtroendet!”. Omdömet återges ordagrant och
slutar där Google klipper det – resten är inte påhittat.

**Förslag (genererad text) som S-Bygg bör bekräfta eller ändra:**

- Tjänsterna *Altaner och trädäck*, *Tillbyggnader* och *Inredningssnickeri* (`confirmed=False` i `SERVICES`).
  *Köksrenovering*, *Ombyggnad och renovering* och *Nya öppningar och dörrar* bygger på kundomdömet och står först
  på startsidan; de övriga nämns under ”Fråga oss också om”.
- Listorna ”Det kan ingå” på tjänstesidorna, arbetsprocessen och svaren i Vanliga frågor.
- Tiderna (`HOURS`): Google Maps säger bara att företaget stänger kl. 16.
- `EMAIL` och `ORG_NR` är tomma tills de är kända; då visas de inte alls.

Inga certifieringar, försäkringar, garantier, årtal, antal anställda eller år i branschen anges.

## Offertformuläret

Formuläret skickar e-post via [FormSubmit](https://formsubmit.co) (gratis) och visar ett tackmeddelande när det
gått fram. Under förhandsvisningen går förfrågningarna till Elevate Studio; byt `FORM_EMAIL` i `scripts/build.py`
till S-Byggs adress vid lansering. Första förfrågan till en ny adress skickar bara ett aktiveringsmejl.
En tjänstesidas ”Begär offert” fyller i projekttypen automatiskt (`index.html?typ=…#offert`).

## Bilder

Alla foton i `docs/img/` är stockbilder från [Pexels](https://www.pexels.com) (fria att använda) och märks på
sidan som illustrationsbilder – de är inte från S-Byggs egna projekt. Byt mot egna bilder genom att ersätta filerna
med samma namn (både `namn.jpg`, ca 1800 px, och `namn-s.jpg`, ca 800 px).

| Fil | Pexels-ID |
| --- | --- |
| `hero-renovering.jpg` | [4642437](https://www.pexels.com/photo/4642437/) |
| `kok.jpg` | [4682120](https://www.pexels.com/photo/4682120/) |
| `kok-2.jpg` | [4713242](https://www.pexels.com/photo/4713242/) |
| `ombyggnad.jpg` | [3990359](https://www.pexels.com/photo/3990359/) |
| `dorr.jpg` | [5691502](https://www.pexels.com/photo/5691502/) |
| `altan.jpg` | [10847167](https://www.pexels.com/photo/10847167/) |
| `tillbyggnad.jpg` | [8830259](https://www.pexels.com/photo/8830259/) |
| `inredning.jpg` | [5974396](https://www.pexels.com/photo/5974396/) |
| `snickeri.jpg` | [6790094](https://www.pexels.com/photo/6790094/) |

## Publicera

Sidan publiceras automatiskt av `.github/workflows/deploy-pages.yml` vid varje push (GitHub Pages, källa *GitHub Actions*). Byt `SITE_URL` i
`scripts/build.py` om sidan får en egen domän.
