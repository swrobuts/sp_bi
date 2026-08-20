import pandas as pd
import numpy as np

# Datensatz laden (Kaggle: Superstore Sales Dataset -> train.csv)
df = pd.read_csv('train.csv', encoding='latin-1')

# Datum: die Datei nutzt TT/MM/JJJJ -> dayfirst=True ist Pflicht,
# sonst bricht das Parsen ab, sobald der Tag groesser als 12 ist.
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Grundlegende Infos
print(df.shape)          # (9800, 18)
print(df.dtypes)         # Datentypen pruefen
print(df.isnull().sum()) # Nullwerte pruefen
print(df.describe())     # Statistische Uebersicht

# Key Stats
print(f"Gesamtumsatz:     ${df['Sales'].sum():,.0f}")
print(f"Bestellungen:      {df['Order ID'].nunique():,}")
print(f"Positionen:        {len(df):,}")
print(f"Ø Bestellwert:   ${df.groupby('Order ID')['Sales'].sum().mean():,.2f}")
print(f"Zeitraum:          {df['Order Date'].min():%d.%m.%Y} bis {df['Order Date'].max():%d.%m.%Y}")
