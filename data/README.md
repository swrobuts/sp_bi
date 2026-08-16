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
