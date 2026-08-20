#!/usr/bin/env python3
"""Erzeugt die drei kleinen Beispielquellen fuer Lab 02.

Lab 02 zeigt, wie dieselben Zahlen aus CSV, Excel und einer JSON-API kommen.
Frueher standen dort Platzhalternamen (daten.csv, bericht.xlsx,
api.example.com) - der Block sah ausfuehrbar aus, war es aber nicht.

Die drei Dateien enthalten bewusst DIESELBEN zwoelf Monatszeilen. Damit
laesst sich am Ende pruefen, ob alle drei Wege zum selben Ergebnis fuehren -
genau die Lernabsicht des Abschnitts.

Der Datensatz ist frei erfunden (fiktives Unternehmen), damit keine
Lizenzfrage entsteht. Er ist absichtlich klein und ohne Defekte: die
Datenqualitaets-Uebungen laufen auf train.csv, nicht hier.

Aufruf:  python3 tools/build_example_data.py
"""

import csv
import json
from pathlib import Path

from openpyxl import Workbook

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "beispiel"

HEADER = ["Monat", "Region", "Produktgruppe", "Umsatz", "Bestellungen"]

ROWS = [
    ["2025-01", "Nord", "Hardware",    18450.00, 112],
    ["2025-02", "Nord", "Hardware",    17920.50, 108],
    ["2025-03", "Nord", "Software",    24310.75, 143],
    ["2025-04", "Sued", "Hardware",    21075.20, 126],
    ["2025-05", "Sued", "Software",    28640.00, 167],
    ["2025-06", "Sued", "Dienstleistung", 15230.40, 61],
    ["2025-07", "West", "Hardware",    19880.90, 119],
    ["2025-08", "West", "Software",    26115.30, 154],
    ["2025-09", "West", "Dienstleistung", 14760.00, 58],
    ["2025-10", "Ost",  "Hardware",    16340.60, 101],
    ["2025-11", "Ost",  "Software",    22980.15, 138],
    ["2025-12", "Ost",  "Dienstleistung", 17505.25, 70],
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)

    # 1. CSV - Semikolon waere deutscher Excel-Standard, hier bewusst Komma,
    #    damit pd.read_csv ohne sep-Argument funktioniert.
    csv_path = OUT / "umsatz.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(HEADER)
        w.writerows(ROWS)
    print("erzeugt:", csv_path.relative_to(ROOT))

    # 2. Excel - ein Blatt "Umsatz". Der Blattname ist Teil der Daten und
    #    bleibt deshalb in beiden Sprachfassungen des Labs gleich.
    wb = Workbook()
    ws = wb.active
    ws.title = "Umsatz"
    ws.append(HEADER)
    for row in ROWS:
        ws.append(row)
    for col, width in zip("ABCDE", (10, 10, 16, 12, 14)):
        ws.column_dimensions[col].width = width
    xlsx_path = OUT / "bericht.xlsx"
    wb.save(xlsx_path)
    print("erzeugt:", xlsx_path.relative_to(ROOT))

    # 3. JSON im Format einer typischen REST-Antwort: Nutzlast unter "data",
    #    daneben Metadaten. Genau deshalb braucht pd.json_normalize den Key.
    payload = {
        "meta": {
            "source": "BI Lab Beispieldaten (fiktiv)",
            "currency": "EUR",
            "count": len(ROWS),
        },
        "data": [dict(zip(HEADER, row)) for row in ROWS],
    }
    json_path = OUT / "sales_api.json"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                         encoding="utf-8")
    print("erzeugt:", json_path.relative_to(ROOT))

    total = sum(r[3] for r in ROWS)
    orders = sum(r[4] for r in ROWS)
    print(f"Kontrollwerte: {len(ROWS)} Zeilen, Umsatz {total:,.2f}, Bestellungen {orders}")


if __name__ == "__main__":
    main()
