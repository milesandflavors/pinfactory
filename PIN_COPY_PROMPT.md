# Pin-szövegíró prompt (Miles & Flavors / PinFactory)

Ezt a promptot használd minden alkalommal, amikor egy cikkhez pin-szövegeket (pins.csv sorokat) generálsz — új cikkhez vagy meglévő pin frissítéséhez egyaránt.

## Bemenet
- Cikk URL / cím
- Cikk fő témája, 2-3 mondatos tartalmi összefoglaló
- Hány pin készül hozzá (jellemzően 3-5)

## Alapszabály: variáld a szöget pinenként

Egy cikk pinjei **ne ugyanazt a hook-típust** használják. Minden pinhez válassz egyet (és ne ismételd a cikken belül):

1. **Vágykeltő / aspirációs** — érzéki, élmény-alapú, "képzeld el ahogy…" hangulat
2. **Hasznossági / instruktív** — konkrét probléma-megoldás, "pontosan mit kell tudni", "step by step"
3. **Kíváncsiságkeltő** — "amit senki nem mond el", "a hiba amit a legtöbben elkövetnek", rejtély-érzés
4. **First-timer** — bizonyítottan magas CTR-t hoz (lásd [[feedback-firsttimer-angle]]), különösen bucket list / hidden gems / itinerary típusnál
5. **Sürgősség / FOMO** — "mielőtt lekésed", szezonalitás, "a legjobb időszak"
6. **Összehasonlítás / döntéstámogatás** — "X vs Y, melyik éri meg jobban"

A cél: minden pin más érzelmi indítékból generáljon kattintást, hogy a batch ne ismételje magát.

## Kimenet — pinenként 4 mező

### 1. Pin cím (Pin cim)
- **MAX 100 karakter** (Pinterest kemény limitje — ellenőrizd!)
- Tükrözze az adott pin hook-szögét
- Elöl 1 fő kulcsszó (SEO), de természetes, nem robotikus megfogalmazásban
- Egy cikk pinjei között ne legyen két egyforma vagy majdnem egyforma cím

### 2. Pin leírás (Pin leiras)
- **MAX 500 karakter** (Pinterest limit), törekedj rá, hogy közel kitöltse
- Kövesd a bevált háromrészes struktúrát ([[pin-description-style]]):
  1. Érzelmi hook / helyzetbe helyezés (1-2 mondat, érzékletes, "ott vagy" hangvétel)
  2. Kulcsszavas természetes összefoglaló — süss bele **minden** releváns kulcsszót (helyszínnevek, aktivitások, "travel guide / itinerary / travel tips / best time to visit / where to stay" stb.) folyó, értelmes mondatokban
  3. **Soha ne zárj pipe-listával** (`keyword | keyword | keyword` TILOS — Pinterest és Google is spamnek veszi)

### 3. Pin bold + Pin light (a képen megjelenő szöveg)
- Ez **nem ugyanaz**, mint a leírás — ez az, amit a néző ténylegesen lát a pin vizuálján
- **Rövid, ütős**, kb. 3-8 szó soronként
- Legyen "tovább akarom olvasni" hatású: félbehagyott gondolat, kérdés, meglepő szám/állítás
- Ne legyen teljes, kilistázott mondat — tömör, figyelemfelkeltő
- **Pin bold** = főcím (nagyobb, erősebb súlyú), **Pin light** = alcím/kiegészítés (kisebb, támogató)

### 4. Alt text
- **Egyelőre üresen hagyva** — amíg nincs kiválasztva a fotó, nem tudjuk mit írjunk le rajta. Ezt a mezőt csak akkor töltsd ki, amikor megvan a konkrét kép.

## SEO-kiegészítés (2026-08-06-i kutatás alapján)

### Kulcsszó-elhelyezés a címben
A **fő kulcsszó mindig a cím legelején** legyen, nem a végén elrejtve. Az algoritmus a cím eleji szavaknak nagyobb súlyt ad. ("Chicago Riverwalk: Free Things to Do in 2 Hours" — nem "2 Hours of Fun: Chicago Riverwalk Free Things".)

### Minden pin leírása legyen ténylegesen egyedi, nem csak a címe
A Pinterest 2026-os "fresh pin" definíciója: **Kép + URL + Leírás egyedi kombinációja**. Ha egy cikkhez 3-5 pin készül, ne csak a Pin cím és a kép változzon — a **leírás szövege is legyen érdemben más** pinenként (más hook, más kulcsszó-hangsúly), különben az algoritmus nem kezeli valódi friss pinnek.

### Egy fő + egy támogató kulcsszó pinenként
Célozz pinenként **1 long-tail kulcsszó-kifejezést** (pl. "chicago riverwalk free things to do") **+ 1 támogató mid-tail kifejezést** (pl. "chicago itinerary") — ne halmozz be 5-6 különböző témát egy leírásba, az felhígítja a relevanciát.

### Alt text — amikor már van kép, ne legyen általános
Az alt text 2026-ban már nem csak akadálymentesítés — a Pinterest AI ezzel **ellenőrzi, hogy a kép ténylegesen egyezik-e a szöveges kulcsszavakkal**. Amikor a fotó megvan:
- Írd le **konkrétan, mit mutat a kép** (helyszín, mit csinál rajta valaki, napszak stb.), kulcsszavakkal, de leíró jelleggel — ne csak a pin címét másold be.
- Ha a kép és a szöveg nem egyezik (pl. leírás "minimalist home office", de a képen kaotikus asztal látszik), a pin relevancia-pontszáma romlik. Ez azt is jelenti, hogy a **fotóválasztásnál** figyelni kell, hogy a kép vizuálisan tükrözze, amiről a pin cím/leírás szól.
- **Az alt text idézze a pinen lévő (bold+light) szöveget is**, ne csak a fotót írja le — a képre rásütött szöveg pixel, amit se a screen reader, se a Pinterest képfelismerő AI nem lát másképp. Formátum: `"[fotó leírása]. Pin text overlay: '[bold] — [light]'."` (user kérése, 2026-08-06).

### Board-specifikusság
A board neve maga is rangsorolási jel. Egy specifikus board (pl. "Chicago with Kids Itinerary") erősebb kontextust ad, mint egy általános ("Chicago Travel"). **Külön, később elvégzendő audit-feladat**: érdemes átnézni a jelenlegi board-listát, hogy elég specifikusak-e, mielőtt az új 18 cikk pinjeit szétosztjuk közöttük — ezt nem most csinálom, csak jelzem.

### Rich Pins / Open Graph — technikai előfeltétel, nem pin-szöveg kérdés
A Pinterest "Article Rich Pin" automatikusan behúzza a linkelt oldal meta title/meta description tartalmát, és ez plusz kulcsszó-réteget ad a pin indexeléséhez — de csak akkor működik, ha a blogcikk oldalán rendes Open Graph / schema markup van. Ez nem a pin-szöveg feladata, hanem a cikk technikai SEO-jáé — **külön ellenőrzésre érdemes**, ha még nem történt meg (nem most, csak jelzem, hogy van ilyen tartalék).

### Amit NEM kell csinálni
- **Hashtag-ek**: a rangsorolásban mára ~1%-os súlyuk van, nem kell erőltetni.
- **Kulcsszó-halmozás / nem természetes leírás**: az algoritmus ezt bünteti — ez megerősíti a meglévő "soha pipe-lista" szabályt.

## Még meg nem írt cikkekhez készülő pin — TILOS a "hamarosan jön" ÉS a "még csak tervezzük" keret (2026-08-15)

Ha egy pin olyan cikkhez készül, ami még nem létezik (de a pin-dátumig el fog készülni), a szöveg **soha ne utaljon rá, hogy a cikk/terv még nincs kész** — se nyíltan ("is coming", "coming soon", "a dedicated guide is coming", "save this for later"), se burkoltan ("Our Planning-Stage Itinerary", "We're planning a trip around...", "the itinerary I'm working on"). A pin úgy íródjon, mintha a cikk már kész, magabiztos, végleges útmutató lenne: normál marketingszöveg, csak a ténylegesen megerősített tényekre alapozva (ne találj ki konkrét számokat/árakat/időpontokat, se hamis személyes élményt, amit nem éltünk át — pl. ha még nem jártunk ott karácsonykor, ne írjunk úgy, mintha jártunk volna). **Why:** mindkét keret ugyanazt a hibát követi el más szavakkal — felfedi a gyártási/tervezési folyamatot a végterméktartalom helyett, ami gyengíti a hitelességet, és Pinteresten az olvasó kész megoldást keres, nem egy készülő tervet (user visszajelzés, 2026-08-15).

## Város-egyértelműség szabály (2026-08-06)

Minden pinen egyértelműen ki kell derülnie, MELYIK városról van szó — vagy a képből (felismerhető, ikonikus látvány), vagy a szövegből (cím/bold/light), de valahonnan mindig. Egy generikus, távoli felhőkarcoló-skyline (ami városok között könnyen összekeverhető) önmagában NEM elég. Kérdezd meg magadtól minden pinnél: "ha valaki csak a képet nézi, 1 másodperc alatt tudja-e, melyik város ez?" Ha nem egyértelmű: válassz ikonikusabb fotót, VAGY írd bele a városnevet a szövegbe.

## Önellenőrzés minden pin után
- [ ] Cím ≤ 100 karakter, **fő kulcsszó legelöl**?
- [ ] Leírás ≤ 500 karakter, nincs pipe-lista a végén?
- [ ] Ez a hook-szög és a leírás szövege is **ténylegesen más**, mint a cikk többi pinjéé?
- [ ] Van 1 fő long-tail + 1 támogató mid-tail kulcsszó, nincs túlzsúfolva?
- [ ] A pin bold/light rövid és kíváncsiságra ösztönző, nem csak megismétli a leírást?
- [ ] Alt text: üres, amíg nincs kép — amikor lesz, konkrétan azt írja le, ami a képen látszik, nem a puszta címet
