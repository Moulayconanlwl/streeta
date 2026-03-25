# -*- coding: utf-8 -*-
"""
Comprehensive multilingual street type / prefix / suffix dictionaries.
Organized by language group with indication of typical number position.
NUMBER_FIRST  → number precedes the street name  (EN/FR/NL/Nordic/…)
NUMBER_LAST   → number follows the street name   (DE/IT/ES/PT/Slavic/…)
"""

# ── ENGLISH (US / UK / CA / AU / NZ / ZA / IE) ────────────────────────────
EN_PREFIXES = set()          # English has no prefix; number always comes first
EN_SUFFIXES = {
    # Full forms
    "street","avenue","road","lane","drive","court","place","crescent","close",
    "way","grove","gardens","terrace","boulevard","circle","parade","rise",
    "highway","freeway","expressway","motorway","parkway","bypass",
    "alley","arcade","approach","bank","bend","broadway","causeway","chase",
    "common","concourse","corner","corso","cutting","dale","dene","deviation",
    "distributor","divide","downs","east","elbow","end","esplanade","estate",
    "flat","formation","frontage","gap","gate","glade","glen","grange","green",
    "grove","heights","hill","hollow","interchange","island","junction","keys",
    "knoll","link","loop","mall","manor","mews","nook","north","outlook",
    "oval","park","passage","path","pathway","pike","plaza","pocket","point",
    "port","promenade","quadrant","quay","reach","reserve","ridge","ring",
    "row","run","slope","south","square","steps","strip","subdivision",
    "tce","thoroughfare","track","trail","turn","underpass","vale","valley",
    "view","village","vista","walk","west","wharf","yard",
    # Abbreviations
    "st","ave","rd","ln","dr","ct","pl","cres","cl","wy","blvd","cir","hwy",
    "fwy","expy","pkwy","byp","aly","arc","bvd","ch","crk","espl","fld","grn",
    "hts","jct","lp","mnr","mw","pk","plz","pt","qy","rdg","riv","sq","ter",
    "trl","vly","vw","vlg",
}
EN_NUMBER_POSITION = "first"

# ── FRENCH (FR / BE / CH / LU / CA-QC / MA / DZ / TN / CI / SN) ──────────
FR_PREFIXES = {
    # Full forms
    "rue","avenue","boulevard","allée","allee","impasse","place","chemin",
    "route","voie","passage","square","villa","résidence","residence",
    "domaine","lotissement","hameau","quartier","cité","cite","zone",
    "parc","quai","mail","promenade","sentier","sente","ruelle","clos",
    "cour","galerie","montée","montee","descente","traverse","carrefour",
    "chaussée","chaussee","liaison","rocade","déviation","deviation",
    "esplanade","parvis","porche","venelle","virage","voie",
    # Abbreviations
    "r","av","ave","bd","all","imp","pl","ch","rte","psg","sq","res","dom",
    "lot","ham","qrt","cit","zon","par","qi","ml","prom","sent","rul",
    "clos","cour","gal","mont","desc","trav","carr","chss","lia","roc","dev",
    "espl","parv","ven",
}
FR_SUFFIXES = {"bis","ter","quater","quinquies","tris","a","b","c"}
FR_NUMBER_POSITION = "first"

# ── GERMAN (DE / AT / CH-DE / LI / LU-DE) ────────────────────────────────
DE_PREFIXES = set()          # German typically has no prefix; street name + type + number
DE_SUFFIXES = {
    # Full forms (often compounded: Hauptstraße)
    "straße","strasse","gasse","weg","allee","platz","ring","damm",
    "chaussee","promenade","graben","stieg","steig","ufer","zeile",
    "markt","pfad","gang","passage","allee","brücke","brucke","brückenweg",
    "gässchen","gasschen","stadtweg","feldweg","waldweg","bergweg",
    "querstraße","querstrasse","nebenstraße","nebenstrasse","hauptstraße","hauptstrasse",
    "bundesstraße","bundesstrasse","landstraße","landstrasse","kreisstraße","kreisstrasse",
    # Abbreviations
    "str","pl","rg","weg","all","ch","prom","gr","sg","uf","zl","mkt","pf","gng",
}
DE_NUMBER_POSITION = "last"

# ── ITALIAN (IT / CH-IT / SM / VA) ────────────────────────────────────────
IT_PREFIXES = {
    # Full forms
    "via","corso","piazza","viale","vicolo","largo","lungarno","strada",
    "salita","scalinata","rotonda","contrada","borgata","borgonuovo","rione",
    "sestiere","traversa","viottolo","calata","corsia","galleria","passaggio",
    "piazzale","piazzetta","regione","regionale","localita","località",
    "stradone","stradello","stradina","vico","sopportico","portico",
    # Abbreviations
    "v","c","p","pza","pzza","vl","vcl","lgo","str","sal","rot","cont",
    "trav","gal","pass","pzle","reg","loc","vico","prt","pco",
}
IT_SUFFIXES = set()
IT_NUMBER_POSITION = "last"

# ── SPANISH (ES / MX / AR / CO / CL / PE / VE / EC / BO / PY / UY / CR / DO / PA) ──
ES_PREFIXES = {
    # Full forms
    "calle","avenida","plaza","paseo","carrera","carretera","camino","vía",
    "via","rambla","ronda","travesía","travesia","glorieta","bulevar",
    "boulevard","barrio","urbanización","urbanizacion","colonia","manzana",
    "prolongación","prolongacion","diagonal","lateral","transversal","circunvalación",
    "circunvalacion","autopista","autovía","autovia","carretera","sendero",
    "peatonal","alameda","pasaje","vereda","callejón","callejon",
    "andador","circuito","privada","boulevard","boulevard","blvd",
    # Abbreviations
    "c","av","avda","pz","pso","crra","carr","cam","vía","via","rbl",
    "rnda","trvs","glta","blvr","blvd","bº","urb","col","mzna","prol",
    "diag","lat","transv","circunv","autop","autov","ctra","snd","pjl",
    "alam","pje","vrda","cjon","cjn","and","circ","priv",
}
ES_SUFFIXES = set()
ES_NUMBER_POSITION = "last"

# ── PORTUGUESE (PT / BR / AO / MZ / CV / GW / ST / TL) ────────────────────
PT_PREFIXES = {
    # Full forms
    "rua","avenida","praça","praca","estrada","travessa","largo","beco",
    "calçada","calcada","alameda","viela","vela","caminho","rodovia","autoestrada",
    "estr","ladeira","servidão","servidao","parque","jardim","galeria","passagem",
    "vale","aclive","declive","servidão","loteamento","condomínio","condominio",
    "quarteirão","quarteirao","vila","setor","setor","setor","quadra","conjunto",
    "residencial","empresarial","comercial","industrial",
    # Abbreviations
    "r","av","avda","pca","est","trav","lgo","bco","clc","alm","vla","vl",
    "cam","rod","aut","lad","srv","pq","jrd","gal","pas","se","lot","cond",
    "qrt","vl","set","qd","cj","res","emp","com","ind",
}
PT_SUFFIXES = set()
PT_NUMBER_POSITION = "last"

# ── DUTCH (NL / BE-NL) ────────────────────────────────────────────────────
NL_PREFIXES = set()          # Dutch: number first, like English
NL_SUFFIXES = {
    # Full forms (often compounded: Hoofdstraat → treat bare form)
    "straat","laan","weg","plein","gracht","kade","singel","dijk","steeg",
    "markt","dreef","allee","baan","pad","rijweg","brug","hoek","boulevard",
    "promenade","esplanade","wijk","hof","dam","haven","oever","buurt",
    # Abbreviations
    "str","ln","wg","pl","grcht","kd","sngl","dk","stg","mkt","drf",
    "all","bn","pd","rjwg","brg","hk","blvd","prom","espl","wk","hf","dm","hv",
}
NL_NUMBER_POSITION = "first"

# ── RUSSIAN / UKRAINIAN / BELARUSIAN ──────────────────────────────────────
RU_PREFIXES = {
    # Cyrillic full forms
    "улица","ул","проспект","пр","пр-т","переулок","пер","площадь","пл",
    "бульвар","бул","набережная","наб","шоссе","ш","тупик","тупик","аллея",
    "проезд","пр-д","линия","лн","переулок","пер","квартал","кв",
    # Transliterated
    "ulitsa","ul","prospekt","pr","pereulok","per","ploshchad","pl",
    "bulvar","bul","naberezhnaya","nab","shosse","sh","tupik","alleya",
    "proezd","liniya","kvartal",
}
RU_SUFFIXES = set()
RU_NUMBER_POSITION = "last"   # ул. Ленина, 15 → number last

# ── POLISH ────────────────────────────────────────────────────────────────
PL_PREFIXES = {
    "ulica","ul","aleja","al","plac","pl","skwer","sk","bulwar","rondo",
    "osiedle","os","droga","dr","trakt","szosa","zaułek","zaul","pas",
    # Abbreviations
    "ul","al","pl","sk","blw","rnd","os","dr","trk","sz","z",
}
PL_SUFFIXES = set()
PL_NUMBER_POSITION = "last"

# ── NORDIC: Swedish / Norwegian / Danish / Finnish / Icelandic ───────────
NORDIC_PREFIXES = set()
NORDIC_SUFFIXES = {
    # Swedish
    "gatan","gata","vägen","väg","leden","led","torget","torg","allén","allé",
    "stigen","stig","backen","backe","platsen","plats","esplanaden","esplanad",
    "bron","kvarngatan","promenaden","promenad",
    # Norwegian
    "gata","gate","veien","vei","allé","alléen","torget","torg","stien","sti",
    "brygga","kai",
    # Danish
    "gade","vej","allé","torvet","torg","stien","boulevard","plads",
    # Finnish
    "katu","tie","kuja","polku","latu","tori","aukio","bulevardi","esplanadi",
    # Icelandic
    "gata","vegur","braut","torg","stígur",
    # Abbreviations
    "g","v","l","t","a","s","b","p","e",
}
NORDIC_NUMBER_POSITION = "last"   # Storgatan 5, Kongens gate 12

# ── ARABIC (AR / SA / AE / EG / MA / DZ / TN / IQ / SY / JO / KW / QA / BH / OM / LB / LY / SD / YE) ──
AR_PREFIXES = {
    # Arabic script
    "شارع","ش","طريق","ط","ميدان","م","حارة","ح","زقاق","ز","درب","نهج","ن",
    "جادة","ج","كورنيش","ك","بلفار","قرية","حي","منطقة","قطعة",
    # Transliterated
    "sharia","shar","tariq","midan","haret","hara","zuqaq","darb","nahj",
    "jada","corniche","hay","mantiqa","qutiaa","boulevard",
}
AR_SUFFIXES = set()
AR_NUMBER_POSITION = "first"

# ── TURKISH (TR / CY-TR) ──────────────────────────────────────────────────
TR_PREFIXES = {
    "sokak","sokağı","sokagi","caddesi","cadde","bulvarı","bulvari","bulvar",
    "mahallesi","mahalle","yolu","yol","köyü","köy","posta","meydanı","meydan",
    # Abbreviations
    "sk","sok","cd","cad","blv","bul","mah","yl","yol","myd",
}
TR_SUFFIXES = set()
TR_NUMBER_POSITION = "last"   # Atatürk Cad. No:5 or Atatürk Sokak 5

# ── GREEK (GR / CY) ───────────────────────────────────────────────────────
GR_PREFIXES = {
    # Greek script
    "οδός","οδ","λεωφόρος","λεωφ","πλατεία","πλ","αγορά","αγ",
    "λιμάνι","ακτή","παραλία",
    # Transliterated
    "odos","leoforos","leof","plateia","pl","agora","ag","limani","akti","paralia",
}
GR_SUFFIXES = set()
GR_NUMBER_POSITION = "first"

# ── HEBREW (IL) ───────────────────────────────────────────────────────────
HE_PREFIXES = {
    "רחוב","רח","שדרות","שד","כיכר","סמטה","דרך","מסלול","גשר",
    "rehov","shderot","kikar","simta","derekh","maslul",
}
HE_SUFFIXES = set()
HE_NUMBER_POSITION = "first"

# ── HUNGARIAN (HU) ────────────────────────────────────────────────────────
HU_PREFIXES = {
    "utca","út","tér","körút","körút","sor","dűlő","dulo","köz","koz",
    "fasor","sétány","setany","liget","park","lejtő","lejto","rakpart",
    # Abbreviations
    "u","út","tér","krt","sor","dűl","köz","fas","sét","lg","pk","rkp",
}
HU_SUFFIXES = set()
HU_NUMBER_POSITION = "last"    # Kossuth utca 5

# ── ROMANIAN (RO / MD) ────────────────────────────────────────────────────
RO_PREFIXES = {
    "strada","str","bulevardul","bulevard","bd","b-dul","calea","cal",
    "splaiurile","splaiul","spl","aleea","alee","al","piața","piata","pta",
    "intrarea","intr","fundătura","fundatura","fund","scuarul","scuar",
    "cheia","cheiul","prelungirea","prelungire",
}
RO_SUFFIXES = set()
RO_NUMBER_POSITION = "last"    # Strada Victoriei 12

# ── CZECH / SLOVAK (CZ / SK) ──────────────────────────────────────────────
CS_PREFIXES = {
    "ulice","ul","třída","trida","nám","náměstí","namesti","nábreží","nabrezi",
    "alej","al","bulvár","bulvar","cesta","c","sídliště","sidliste",
    "avenue","promenáda","promenada",
}
CS_SUFFIXES = set()
CS_NUMBER_POSITION = "last"

# ── JAPANESE (JP) ─────────────────────────────────────────────────────────
JP_KEYWORDS = {
    "丁目","番地","番","号","町","区","市","都","道","府","県","村","大字","字",
    "chome","banchi","ban","go","machi","ku","shi","to","do","fu","ken",
}
JP_NUMBER_POSITION = "complex"   # chome-ban-go system

# ── CHINESE (CN / TW / HK / SG-ZH / MO) ──────────────────────────────────
ZH_KEYWORDS = {
    "路","街","道","大道","大街","巷","弄","号","号楼","幢","栋","室","区",
    "lu","jie","dao","dadao","dajie","xiang","long","hao","lou","zhuang","dong","shi","qu",
}
ZH_NUMBER_POSITION = "complex"

# ── KOREAN (KR) ───────────────────────────────────────────────────────────
KO_KEYWORDS = {
    "로","길","동","구","시","도","번지","호","대로",
    "ro","gil","dong","gu","si","do","beonji","ho","daero",
}
KO_NUMBER_POSITION = "complex"

# ── INDIAN LANGUAGES (IN: Hindi / Bengali / Tamil / Telugu / etc.) ────────
IN_KEYWORDS = {
    # Common transliterated forms used in addresses
    "marg","road","rd","lane","ln","nagar","vihar","colony","enclave","sector",
    "phase","block","street","st","avenue","av","avenue","chowk","crossing",
    "market","layout","extension","extn","township","gali","mohalla",
}
IN_NUMBER_POSITION = "first"   # Most Indian addresses use English format

# ── SWAHILI / EAST AFRICA (TZ / KE / UG / RW / BI) ───────────────────────
SW_KEYWORDS = {
    "barabara","mtaa","njia","street","road","avenue","lane","plot",
}
SW_NUMBER_POSITION = "first"


# ─────────────────────────────────────────────────────────────────────────────
# MASTER LOOKUP TABLE
# Maps each normalized (lowercased) keyword to its language code + number position
# ─────────────────────────────────────────────────────────────────────────────
def build_master_lookup():
    lookup = {}  # keyword → (lang_code, position)

    groups = [
        (EN_PREFIXES | EN_SUFFIXES, "EN", "first"),
        (FR_PREFIXES, "FR", "first"),
        (DE_PREFIXES | DE_SUFFIXES, "DE", "last"),
        (IT_PREFIXES, "IT", "last"),
        (ES_PREFIXES, "ES", "last"),
        (PT_PREFIXES, "PT", "last"),
        (NL_PREFIXES | NL_SUFFIXES, "NL", "first"),
        (RU_PREFIXES, "RU", "last"),
        (PL_PREFIXES, "PL", "last"),
        (NORDIC_SUFFIXES, "NORDIC", "last"),
        (AR_PREFIXES, "AR", "first"),
        (TR_PREFIXES, "TR", "last"),
        (GR_PREFIXES, "GR", "first"),
        (HE_PREFIXES, "HE", "first"),
        (HU_PREFIXES, "HU", "last"),
        (RO_PREFIXES, "RO", "last"),
        (CS_PREFIXES, "CS", "last"),
        (JP_KEYWORDS, "JP", "complex"),
        (ZH_KEYWORDS, "ZH", "complex"),
        (KO_KEYWORDS, "KO", "complex"),
        (IN_KEYWORDS, "IN", "first"),
        (SW_KEYWORDS, "SW", "first"),
    ]

    for keyword_set, lang_code, position in groups:
        for kw in keyword_set:
            lookup[kw.lower()] = (lang_code, position)

    return lookup


MASTER_LOOKUP = build_master_lookup()
