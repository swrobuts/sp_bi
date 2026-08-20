# Lab 05 – Fallstudie Retail Analytics

**Zeitbedarf:** 90–150 Minuten für die ganze Fallstudie.
**Voraussetzung:** Python 3.10 oder neuer; für Schritt 3 Power BI Desktop.

```bash
cp ../../data/train.csv .
pip install -r requirements.txt
python explore.py    # Datenexploration
python app.py        # Dash-App auf http://127.0.0.1:8050
```

**Sollausgabe `explore.py`:**

```
(9800, 18)
Gesamtumsatz:     $2,261,537
Bestellungen:      4,922
Positionen:        9,800
Ø Bestellwert:   $459.48
Zeitraum:          03.01.2015 bis 30.12.2018
```

`df.isnull().sum()` meldet elf fehlende `Postal Code`. Das ist kein Fehler
im Datensatz, sondern eine Entscheidung: Für Umsatz-, Kategorie- und
Regionsauswertungen ist die Postleitzahl ohne Belang, deshalb bleiben die
Zeilen drin. Erst eine Karte auf PLZ-Ebene wäre betroffen – dann würde man
die elf Zeilen ausweisen statt sie zu erfinden. Löschen wäre hier falsch:
es würde Umsatz vernichten, der tatsächlich stattgefunden hat.

`measures.dax` enthält die DAX-Measures inklusive Kalendertabelle für
Power BI. Sollwerte: Umsatz 2.261.536,78 · Bestellungen 4.922 ·
Ø Bestellwert 459,48 · YoY-Wachstum 2018 gegenüber 2017 rund 20,3 %.
