# Beispieldaten für Lab 02

Drei kleine Quellen mit **denselben zwölf Zeilen** – einmal als CSV, einmal
als Excel-Arbeitsmappe, einmal als JSON über HTTP. Genau darum geht es in
Lab 02: dieselben Zahlen kommen über verschiedene Wege ins Werkzeug, und am
Ende muss dasselbe herauskommen.

| Datei | Rolle im Lab | Direktlink |
|---|---|---|
| `umsatz.csv` | `pd.read_csv` | [umsatz.csv](umsatz.csv) |
| `bericht.xlsx` | `pd.read_excel`, Blatt `Umsatz` | [bericht.xlsx](bericht.xlsx) |
| `sales_api.json` | `requests.get` + `pd.json_normalize` | [sales_api.json](sales_api.json) |

Die JSON-Datei ist zusätzlich über HTTP erreichbar und wird im Lab genau so
geladen:

```
https://swrobuts.github.io/sp_bi/data/beispiel/sales_api.json
```

## Spalten

`Monat`, `Region`, `Produktgruppe`, `Umsatz`, `Bestellungen`

Die Nutzlast der JSON-Datei liegt unter dem Schlüssel `data`, daneben stehen
Metadaten unter `meta`. Das ist der Normalfall bei REST-APIs und der Grund,
warum `pd.json_normalize(response.json()['data'])` den Schlüssel braucht.

## Kontrollwerte

| | |
|---|---|
| Zeilen × Spalten | 12 × 5 |
| Summe `Umsatz` | 243.209,05 |
| Summe `Bestellungen` | 1.357 |

Alle drei Quellen müssen dieselben Werte liefern – der Codeblock im Lab
prüft das am Ende mit einem `assert`.

## Herkunft und Lizenz

**Frei erfunden.** Die Zahlen stammen von keinem realen Unternehmen; damit
entsteht keine Lizenz- oder Datenschutzfrage. Erzeugt von
`tools/build_example_data.py` – wer die Daten ändern will, ändert das Skript
und lässt es erneut laufen.

Die Dateien sind bewusst **ohne Defekte**: fehlende Werte, Duplikate und
falsche Datentypen werden in Lab 02 am echten Kursdatensatz
[`../train.csv`](../train.csv) geübt, wo es sie tatsächlich gibt.
