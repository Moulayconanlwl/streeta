# International Building Number Extractor
## Project structure
```
├── address_parser/
│   ├── __init__.py                 # Package entry – exposes InternationalBuildingNumberExtractor
│   ├── extractor.py                # Core engine: 9-pass multi-language extraction pipeline
│   ├── patterns.py                 # All regex patterns (7 pattern sets)
│   ├── language_detector.py        # Script & keyword-based language/format detector
│   └── abbrevs/
│       ├── __init__.py
│       └── multilingual.py         # 22 language dictionaries (EN/FR/DE/IT/ES/PT/NL/RU/PL/
│                                   #  NORDIC/AR/TR/GR/HE/HU/RO/CS/JP/ZH/KO/IN/SW)
├── excel_processor.py              # CLI + Python API for Excel processing
├── requirements.txt
└── README.md
```

## Quick start
```bash
pip install -r requirements.txt

# Command line
python excel_processor.py --input your_file.xlsx

# Python
from address_parser import InternationalBuildingNumberExtractor
ext = InternationalBuildingNumberExtractor()
r = ext.extract("12 rue de la Paix", "")
print(r.building_number)   # 12
```

## Language coverage

| Group | Languages | Number position | Examples |
|-------|-----------|-----------------|---------|
| EN    | US/UK/AU/CA/NZ/ZA/IE | First | `123 Main St` |
| FR    | FR/BE/CH/LU/MA | First | `12 rue de la Paix`, `12bis av. Mozart` |
| DE    | DE/AT/CH/LI | Last | `Hauptstraße 12`, `Musterweg 4A` |
| IT    | IT/CH/SM | Last | `Via Roma 10`, `Corso Vittorio 45` |
| ES    | ES/MX/AR/CO/CL/PE/… | Last | `Calle Mayor 5`, `Av. Insurgentes 1602` |
| PT    | PT/BR/AO/MZ | Last | `Rua das Flores, 123` |
| NL    | NL/BE | First | `Dorpsstraat 25` |
| RU    | RU/UA/BY | Last | `ул. Ленина, д.15` |
| PL    | PL | Last | `ul. Marszałkowska 142` |
| NORDIC| SE/NO/DK/FI/IS | Last | `Storgatan 5`, `Kongens gate 12` |
| AR    | SA/AE/EG/MA/… | First | `شارع 12`, inline `No.5` |
| TR    | TR/CY | Last | `Atatürk Cad. No:5` |
| GR    | GR/CY | First | `Οδός 10` |
| HE    | IL | First | `רחוב 15` |
| HU    | HU | Last | `Kossuth utca 5` |
| RO    | RO/MD | Last | `Strada Victoriei 12` |
| CS    | CZ/SK | Last | `Náměstí 12` |
| JP    | JP | Complex | `1丁目19番11号` → `1-19-11` |
| ZH    | CN/TW/HK | Complex | `建国路93号` → `93` |
| KO    | KR | Complex | `테헤란로 427` |
| IN    | IN | First | `12 MG Road` |
| SW    | TZ/KE | First | `Plot 42 Uhuru St` |

## Extraction pipeline (9 passes)
1. Inline `No.` / `nº` / `nr.` / `#` anywhere → 0.97 confidence
2. After-comma pattern `, 123` → 0.93
3. Russian `д. 15` / `дом 15` indicator → 0.96
4. Japanese chome-ban-go `1丁目19番11号` → 0.95
5. CJK `号` / Korean `번지` indicators → 0.90
6. Language-aware: starts with digit (number-FIRST) → 0.95
7. Language-aware: known prefix detected (number-LAST) → 0.90
8. Trailing-number heuristic → 0.75
9. First isolated number (last resort) → 0.45

## Output columns added to Excel
| Column | Description |
|--------|-------------|
| `BUILDING_NUMBER` | Extracted number (`12`, `12A`, `12bis`, `10-12`) |
| `FULL_ADDRESS` | Concatenation of LN3 + LN4 (audit trail) |
| `BN_CONFIDENCE` | 0.0–1.0 (green ≥0.90, yellow ≥0.70, red <0.70) |
| `BN_LANG` | Detected language code |
| `BN_METHOD` | Human-readable extraction method description |
