# Lab 04 – Dashboards mit Plotly und Dash

**Zeitbedarf:** 20–30 Minuten. **Voraussetzung:** Python 3.10 oder neuer.

```bash
cp ../../data/train.csv .
pip install -r requirements.txt
python charts.py     # drei Plotly-Figuren, öffnen sich im Browser
python app.py        # Dash-App auf http://127.0.0.1:8050
```

**Sollzustand `charts.py`:** drei Figuren – Umsatz nach Kategorie,
monatlicher Trend, Streudiagramm Umsatz gegen Bestellpositionen.

**Sollzustand `app.py`:** die Konsole meldet `Running on http://127.0.0.1:8050`.
Die Seite zeigt ein Kategorie-Dropdown und zwei Diagramme, die sich beim
Umschalten aktualisieren.

Als Container:

```bash
docker build -t bi-lab-dash .
docker run --rm -p 8050:8050 bi-lab-dash
```

## Wenn etwas klemmt

| Symptom | Ursache | Abhilfe |
|---|---|---|
| `FileNotFoundError: train.csv` | Datensatz fehlt im Verzeichnis | `cp ../../data/train.csv .` |
| `UnicodeDecodeError` | falsches Encoding | `encoding='latin-1'` beibehalten |
| Datum-Fehler ab Tag 13 | `dayfirst=True` fehlt | die Datei ist TT/MM/JJJJ, nicht US-Format |
| Port 8050 belegt | andere App läuft | `app.run(debug=True, port=8051)` |
