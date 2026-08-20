# Datensatz: Superstore Sales

`train.csv` – Retail-Datensatz eines globalen Superstores über vier Jahre
(2015–2018). Grundlage der Übungen in Lab 04, Lab 05 und Lab 06.

| | |
|---|---|
| Quelle | [Superstore Sales Dataset (Kaggle, Rohit Sahoo)](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting) |
| Lizenz | GPL 2 |
| Umfang | 9.800 Zeilen × 18 Spalten, 2,13 MB |
| Zeitraum | 03.01.2015 – 30.12.2018 |

## Spalten

`Row ID`, `Order ID`, `Order Date`, `Ship Date`, `Ship Mode`, `Customer ID`,
`Customer Name`, `Segment`, `Country`, `City`, `State`, `Postal Code`,
`Region`, `Product ID`, `Category`, `Sub-Category`, `Product Name`, `Sales`

## Zwei Stolperfallen

**1. Datumsformat ist TT/MM/JJJJ**, nicht US-Format. Ohne `dayfirst=True`
bricht das Einlesen ab, sobald der Tag größer als 12 ist – das betrifft
5.841 der 9.800 Zeilen:

```python
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
```

**2. Kein `Profit`, `Quantity` oder `Discount`.** Dies ist die
Forecasting-Variante des Superstore-Datensatzes; sie enthält als einzige
Kennzahl `Sales`. Deckungsbeitrags- und Margenanalysen sind damit nicht
möglich – die Übungen arbeiten deshalb mit Umsatz, Bestellanzahl und
durchschnittlichem Bestellwert.

## Referenzwerte

Diese Zahlen werden an mehreren Stellen als Sollausgabe genannt. Wer sie
reproduziert, hat richtig eingelesen:

| | |
|---|---|
| Zeilen × Spalten | 9.800 × 18 |
| Bestellungen (`Order ID` distinct) | 4.922 |
| Gesamtumsatz | 2.261.536,78 |
| Ø Bestellwert | 459,48 |
| Fehlende Werte | 11 × `Postal Code`, sonst keine |
| Zeitraum | 03.01.2015 – 30.12.2018 |
| Umsatz je Jahr | 2015: 479.856,21 · 2016: 459.436,01 · 2017: 600.192,55 · 2018: 722.052,02 |
| Umsatz je Kategorie | Technology 827.455,87 · Furniture 728.658,58 · Office Supplies 705.422,33 |

Dieselben Werte liefern pandas, die DAX-Measures in Power BI und der
PostgreSQL-Import aus Lab 06. Weicht eine Zahl ab, ist fast immer das
Datumsformat (`dayfirst=True` bzw. `SET datestyle = 'ISO, DMY'`) oder das
Encoding (`latin-1`) schuld.

**Achtung beim SQL-Import:** `Sales` hat bis zu vier Nachkommastellen
(z. B. 957,5775). Eine Spalte `numeric(12,2)` rundet schon beim Import, die
Gesamtsumme weicht dann um rund 20 Cent ab. Das Schema in
`starter/lab-06-stack/init/01_schema.sql` verwendet deshalb `numeric(12,4)`.
