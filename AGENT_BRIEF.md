# AGENT BRIEF: BI Lab – Business Intelligence Companion Site

## Aufgabe
Baue eine vollständige statische Companion-Website für das Hochschul-Modul **"Business Intelligence"** an der THWS Business School. Das Projekt heißt **"BI Lab"**.

Die Site folgt exakt dem Design-System von https://github.com/swrobuts/inme (dem INME Lab) – du kannst die INME-Dateien in `/tmp/inme-lab/` als Vorlage/Referenz nutzen.

---

## Ausgabe
Alle Dateien direkt in `/tmp/sp_bi-lab/` (= Git-Root für GitHub Pages):
- `index.html`
- `lab-01-grundlagen.html`
- `lab-02-daten.html`
- `lab-03-kpis.html`
- `lab-04-dashboards.html`
- `lab-05-fallstudie.html`
- `lab-06-souveraenitaet.html`

Keine anderen Ordner, kein Build-Tool, kein npm.

---

## Zielgruppe
Bachelorstudierende der Wirtschaftsinformatik / Business Analytics im 4.–6. Semester. Grundkenntnisse in Programmierung (Python) vorhanden, BI-Erfahrung: keine.

---

## Tech Stack (identisch INME – NICHT ändern!)
```html
<!-- Tailwind CSS 2 -->
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2/dist/tailwind.min.css" rel="stylesheet">

<!-- React 18 + Babel -->
<script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=EB+Garamond:wght@400;500;600&display=swap" rel="stylesheet">
```

Alles über CDN. Kein Build-Tool, kein npm, kein Server. GitHub Pages = statisch.

---

## Design-System (unterscheidet sich von INME in der Farbe!)

### Primärfarbe (STATT INME-Rot)
```css
:root {
  --primary: #1E3A8A;   /* Deep Navy */
  --accent:  #2563EB;   /* Bright Blue */
  --dark:    #1A1A1A;
  --light-bg: #FAFAFA;
  --primary-light: rgba(30,58,138,0.08);
}
h2 { color: #1E3A8A; }
h3 { color: #1E3A8A; }
.bauhaus-accent-line { background: #2563EB; }
.bauhaus-badge { background: #2563EB; }
```

### DE/EN Farbwechsel (wie INME Red↔Mango)
- **DE-Modus:** Navy `#1E3A8A` / Accent `#2563EB`
- **EN-Modus:** Teal `#0D9488` / Accent `#14B8A6`
- Hero-Hintergrund wechselt je nach Sprache
- Alle roten Elemente aus INME → Blau / Teal

### Alles andere IDENTISCH zu INME:
- Navbar sticky, 56px, weiß, Border-Bottom
- Lang-Toggle DE/EN (oben rechts)
- Bauhaus-Karten (border 1px #E5E7EB, border-radius 10px, box-shadow)
- Stats-Bar unter Hero (weiß, large numbers, UPPERCASE labels)
- Jony Ive Quote strip (zwischen Stats und Labs)
- Lab-Karten im 3-spalten-Grid mit "ZUM LAB →" Footer
- Bonus-Card (span 3, gestrichelter Rand, "BONUS-PROJEKT" Badge)
- Footer (schwarz, zweispaltig)
- localStorage Sprachpersistenz: `localStorage.getItem('bi-lang')` (WICHTIG: key = 'bi-lang', nicht 'inme-lang'!)
- `?lang=en` URL-Parameter Passthrough auf Lab-Seiten

### KRITISCHE CSS-REGELN (Lessons Learned aus INME):
1. **TomSelect NICHT verwenden** (wird hier nicht gebraucht)
2. **Kein `overflow: hidden` auf SVG-Elementen** (destruktiv für Plotly/Charts)
3. **JSX Unicode:** Strings mit Unicode-Escapes in `{}` wrappen: `{'Gebäude'}` NICHT direkt im Tag
4. **CSS-Duplikate vermeiden** – nur eine Hover-Regel pro Klasse
5. **`var` statt `let/const` für globale Script-Vars** (verhindert `window.x` Probleme)

---

## Sprachpersistenz (PFLICHT auf allen Seiten)

### index.html (React)
```js
const [lang, setLang] = React.useState(() => localStorage.getItem('bi-lang') || 'de');
const toggleLang = () => {
  const newLang = lang === 'de' ? 'en' : 'de';
  setLang(newLang);
  localStorage.setItem('bi-lang', newLang);
};
```

### lab-*.html (React)
```js
const urlLang = new URLSearchParams(window.location.search).get('lang');
const [lang, setLang] = React.useState(() => localStorage.getItem('bi-lang') || urlLang || 'de');
```

### Lab-Links in index.html: ?lang=en anhängen wenn lang === 'en'
```js
// Jeder Lab-Link:
href={`lab-01-grundlagen.html${lang === 'en' ? '?lang=en' : ''}`}
```

---

## index.html – Struktur

### Navbar
```
[BI Lab]                    [DE | EN]
```
- Logo "BI Lab" = `--primary` Farbe, fett
- THWS Badge neben Logo

### Hero
- Hintergrund: Navy `#1E3A8A` (DE) / Teal `#0D9488` (EN)
- Eyebrow-Tag: "BUSINESS INTELLIGENCE · THWS BUSINESS SCHOOL"
- Titel: "BI Lab" (riesig, 6.5rem–8rem, weiß, Space Grotesk)
- Subtitle: "Power BI · Python · Plotly Dash" (DE) / "Power BI · Python · Plotly Dash" (EN)
- Keine dekorativen Emojis
- Geometrische Hintergrundformen (wie INME) – Farbe angepasst

### Stats-Bar (direkt unter Hero, weiß)
```
6 LABS   |   1 FALLSTUDIE   |   Power BI & Python   |   Open Source BI
```
Zahlen in Navy, UPPERCASE Labels, identisches Layout zu INME.

### Quote Strip (zwischen Stats und Labs)
```
"In God we trust. All others must bring data." — W. Edwards Deming
```

### Lab-Karten Grid (3 Spalten)
Identisches Layout zu INME lab-cards.
Border-left: 4px `--accent` Blau.
"ZUM LAB →" CTA Footer: hover fill Blau.
Lab-Nummer: groß (2.5rem), prominent.

### Bonus-Card (span 3, gestrichelter Rand)
Title: "BONUS-PROJEKT: Data Sovereignty Stack"
Badge: "BONUS-PROJEKT"
Chips: Apache Superset · Metabase · Docker · PostgreSQL · DSGVO · Self-Hosted
5 Kriterien warum self-hosted BI wichtig ist: Datensouveränität, No Vendor Lock-in, DSGVO-Konformität, Kostenfreiheit, Volle Kontrolle
Link → `lab-06-souveraenitaet.html`

---

## Lab-Inhalte

### lab-01-grundlagen.html – Grundlagen Business Intelligence

**Lernziele:**
1. BI-Begriff und historische Entwicklung erklären
2. BI-Architektur (OLTP → ETL → DWH → Reporting) verstehen
3. KPI-Konzepte (Lead vs. Lag Indicators) kennen
4. BI-Tool-Landschaft überblicken

**Inhalte:**

#### Was ist Business Intelligence?
- Definition: Systeme zur Sammlung, Analyse und Visualisierung von Geschäftsdaten für Entscheidungsunterstützung
- Geschichte: Von Mainframe-Reports → Data Warehouses (1990er) → Self-Service BI (2010er) → KI-gestützte BI (heute)
- Abgrenzung: BI vs. Data Science vs. Analytics

#### BI-Architektur
```
Datenquellen → ETL/ELT → Data Warehouse → BI-Tool → Dashboard
(ERP, CRM, CSV)  (Extraktion,  (zentrales   (Power BI,   (Entscheidung)
                  Transform)    Speichern)   Plotly Dash)
```
Einfaches ASCII-Diagramm oder Mermaid.

#### KPI-Konzepte
- Was ist eine KPI? (Key Performance Indicator)
- Arten: quantitativ vs. qualitativ, absolut vs. relativ
- Lead Indicators (vorausschauend) vs. Lag Indicators (rückblickend)
- SMART-KPIs (Specific, Measurable, Achievable, Relevant, Time-bound)
- Beispiele aus dem Retail: Umsatz, Conversion Rate, Customer Lifetime Value, Churn Rate

#### Tool-Überblick
| Tool | Typ | Kosten | Datenhoheit |
|------|-----|--------|-------------|
| Power BI | Closed-Source | Freemium/Abo | Microsoft Cloud |
| Tableau | Closed-Source | Abo | Salesforce Cloud |
| Plotly Dash | Open-Source | Kostenlos | Selbst gehostet |
| Apache Superset | Open-Source | Kostenlos | Selbst gehostet |
| Metabase | Open-Source | Kostenlos/Abo | Flexibel |

#### YouTube-Ressourcen
- "Power BI for Beginners" – Guy in a Cube (EN): https://www.youtube.com/@GuyInACube
- "Business Intelligence Grundlagen" – offizieller Microsoft-Kanal: https://www.youtube.com/@MicrosoftPowerBI
- SQLBI Channel (DAX & Power BI): https://www.youtube.com/@SQLBI

#### Verständnisfragen / Quiz
3 Multiple-Choice-Fragen (wie INME-Quiz-Format falls vorhanden, sonst einfache Liste)

---

### lab-02-daten.html – Daten: Quellen, Modelle, Qualität

**Lernziele:**
1. Verschiedene Datenquellen anbinden
2. Star Schema und Snowflake Schema verstehen und entwerfen
3. Datenqualitätsprobleme erkennen und beheben
4. Power Query (Power BI) und Pandas (Python) für Datentransformation nutzen

**Inhalte:**

#### Datenquellen
- Strukturiert: CSV, Excel, SQL-Datenbanken (MySQL, PostgreSQL)
- Semi-strukturiert: JSON, XML, REST-APIs
- Cloud-Quellen: Google Sheets, Azure, SharePoint
- In Power BI: "Daten abrufen" Dialog
- In Python: `pd.read_csv()`, `pd.read_excel()`, `requests` + `pd.json_normalize()`

#### Datenmodellierung
**Star Schema:**
```
              Dim_Zeit
                 |
Dim_Produkt — Fakt_Umsatz — Dim_Kunde
                 |
             Dim_Region
```
- Faktentabelle: Messgrößen (Umsatz, Menge, Preis)
- Dimensionstabellen: Kontexte (Zeit, Produkt, Kunde, Region)
- Vorteile: Einfache Abfragen, gute Performance, leicht verständlich

**Snowflake Schema:**
- Normalisierte Dimensionen (Hierarchien aufgebrochen)
- Vor-/Nachteile vs. Star Schema

#### Datenqualität
- Häufige Probleme: Nullwerte, Duplikate, falsche Datentypen, Inkonsistenzen (z.B. "DE" vs "Germany")
- In Power BI: Power Query Editor (Filtern, Ersetzen, Typen setzen)
- In Python/Pandas:
```python
df.isnull().sum()          # Nullwerte prüfen
df.drop_duplicates()       # Duplikate entfernen
df['date'] = pd.to_datetime(df['date'])  # Typen konvertieren
df['country'].str.strip().str.upper()    # String-Bereinigung
```

#### Code-Beispiele (mit Copy-Buttons, Light-Gray Background)
Pandas-Snippets für: Laden, Prüfen, Bereinigen, Aggregieren

#### YouTube-Ressourcen
- "Power Query Tutorial" – Curbal Channel: https://www.youtube.com/@Curbal
- "Pandas Data Cleaning" – Keith Galli: https://www.youtube.com/@KeithGalli

---

### lab-03-kpis.html – KPIs mit DAX & Python

**Lernziele:**
1. DAX-Grundlagen in Power BI anwenden
2. Measures vs. Calculated Columns verstehen
3. Wichtige Business-KPIs in DAX und Python berechnen
4. Filter-Kontext in DAX verstehen

**Inhalte:**

#### DAX – Data Analysis Expressions
- Was ist DAX? (Excel-ähnliche Formelsprache für Power BI)
- **Measures** (dynamisch, berechnet im Filter-Kontext) vs. **Calculated Columns** (statisch, Zeile für Zeile)
- Goldene Regel: Fast immer Measures verwenden!

#### Wichtige DAX-Funktionen
```dax
-- Einfache Aggregation
Gesamtumsatz = SUM(Umsatz[Betrag])

-- Mit Bedingung (CALCULATE)
Umsatz_DE = CALCULATE(SUM(Umsatz[Betrag]), Umsatz[Land] = "Deutschland")

-- Division mit Null-Absicherung
Marge_% = DIVIDE([Bruttogewinn], [Umsatz], 0)

-- Zeitintelligenz
Umsatz_VJ = CALCULATE([Gesamtumsatz], SAMEPERIODLASTYEAR(Datum[Datum]))
Wachstum_% = DIVIDE([Gesamtumsatz] - [Umsatz_VJ], [Umsatz_VJ], 0)

-- Ranking
Top_Produkte = RANKX(ALL(Produkt[Name]), [Gesamtumsatz])
```

#### Python-Äquivalente (Pandas)
```python
# Gesamtumsatz
umsatz_gesamt = df['Betrag'].sum()

# Umsatz DE
umsatz_de = df[df['Land'] == 'Deutschland']['Betrag'].sum()

# Marge
marge_pct = df['Bruttogewinn'].sum() / df['Betrag'].sum() * 100

# Jahresvergleich
yearly = df.groupby(df['Datum'].dt.year)['Betrag'].sum()
wachstum = yearly.pct_change() * 100

# Ranking
top_produkte = df.groupby('Produkt')['Betrag'].sum().rank(ascending=False)
```

#### Wichtige Business-KPIs (Tabelle)
| KPI | Formel | DAX | Python |
|-----|--------|-----|--------|
| Umsatz | Σ Betrag | SUM() | .sum() |
| Bruttogewinn | Umsatz - COGS | CALCULATE() | subtraction |
| Marge % | GP / Umsatz × 100 | DIVIDE() | / * 100 |
| YoY-Wachstum | (Jetzt - VJ) / VJ | SAMEPERIODLASTYEAR | pct_change() |
| Conversion Rate | Käufe / Besuche | DIVIDE() | / |
| Customer LTV | Ø Bestellwert × Frequenz | Measures | groupby |

#### Filter-Kontext erklären (wichtig für DAX-Verständnis)
- Row Context vs. Filter Context
- Warum CALCULATE() so mächtig ist

#### YouTube-Ressourcen
- SQLBI "DAX Introduction": https://www.youtube.com/@SQLBI
- "DAX Fridays" – Curbal: https://www.youtube.com/@Curbal

---

### lab-04-dashboards.html – Dashboard-Design & Plotly Dash

**Lernziele:**
1. Dashboard-Design-Prinzipien anwenden
2. Plotly Express Charts erstellen
3. Plotly Dash App mit Layout und Callbacks bauen
4. Power BI vs. Plotly Dash architektonisch vergleichen

**Inhalte:**

#### Dashboard-Design-Prinzipien
- **Data-Ink Ratio** (Tufte): Nur nötige visuelle Elemente
- **5-Second Rule**: Dashboard-Kernaussage in 5 Sekunden erkennbar
- **Visual Hierarchy**: Wichtigstes oben links
- **Farbe sparsam**: Max. 3–4 Farben, semantische Bedeutung (Rot = schlecht, Grün = gut)
- **Falsche Chart-Typen**: Wann kein Tortendiagramm? Wann Balken vs. Linie?

#### Chart-Auswahl (Entscheidungsbaum)
```
Vergleich über Zeit → Linien- oder Balkendiagramm
Rangliste           → Horizontales Balkendiagramm
Anteil/Komposition  → Gestapeltes Balken (NICHT Torte bei >4 Kategorien)
Korrelation         → Streudiagramm (Scatter Plot)
Geografisch         → Choropleth / Karte
KPI-Einzel          → Card/Scorecard
```

#### Plotly Express (Python)
```python
import plotly.express as px
import pandas as pd

df = pd.read_csv('superstore.csv')

# Umsatz nach Kategorie
fig = px.bar(df.groupby('Category')['Sales'].sum().reset_index(),
             x='Category', y='Sales',
             title='Umsatz nach Kategorie',
             color_discrete_sequence=['#2563EB'])
fig.show()

# Umsatz über Zeit
fig2 = px.line(df.groupby('Order Date')['Sales'].sum().reset_index(),
               x='Order Date', y='Sales')

# Scatter: Umsatz vs. Gewinn
fig3 = px.scatter(df, x='Sales', y='Profit',
                  color='Category', hover_data=['Product Name'])
```

#### Plotly Dash Architektur
```python
# app.py
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
df = pd.read_csv('superstore.csv')

app.layout = html.Div([
    html.H1('Sales Dashboard'),

    dcc.Dropdown(
        id='category-filter',
        options=[{'label': c, 'value': c} for c in df['Category'].unique()],
        value=df['Category'].unique()[0]
    ),

    dcc.Graph(id='sales-chart')
])

@app.callback(
    Output('sales-chart', 'figure'),
    Input('category-filter', 'value')
)
def update_chart(category):
    filtered = df[df['Category'] == category]
    fig = px.bar(filtered.groupby('Sub-Category')['Sales'].sum().reset_index(),
                 x='Sub-Category', y='Sales')
    return fig

if __name__ == '__main__':
    app.run(debug=True)
```

**Dash-Architektur erklären:**
- App = Flask + React Frontend
- Layout = deklarativ (wie HTML, aber Python)
- Callbacks = Reaktivität (Input → Output)

#### Power BI vs. Plotly Dash Vergleich
| Aspekt | Power BI | Plotly Dash |
|--------|----------|-------------|
| Lernkurve | Niedrig (GUI) | Mittel (Python) |
| Flexibilität | Mittel | Sehr hoch |
| Deployment | Power BI Service (Cloud) | Eigener Server/Cloud |
| Kosten | Freemium + Abo | Kostenlos (Open Source) |
| Datenhoheit | Microsoft Cloud | Selbst kontrolliert |
| Customization | Begrenzt | Unbegrenzt |
| KI-Integration | Built-in (Copilot) | Manuell (Python-Ökosystem) |
| Ideal für | Schnelle Business Reports | Entwickler, komplexe Apps |

#### YouTube-Ressourcen
- "Charming Data" – Plotly Dash Tutorials: https://www.youtube.com/@CharmingData
- "Plotly Express Full Tutorial" – Rob Mulla: https://www.youtube.com/@RobMulla

---

### lab-05-fallstudie.html – Fallstudie: Retail Analytics

**Lernziele:**
1. Kompletten BI-Workflow von Daten bis Dashboard durchlaufen
2. Dieselbe Fallstudie in Power BI UND Python umsetzen
3. Vor-/Nachteile beider Ansätze praktisch erleben
4. Professionelle KPI-Hierarchien entwerfen

**Datensatz: Superstore Dataset**
- Quelle: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final (öffentlich, frei nutzbar)
- Inhalt: Bestellungen, Produkte, Kunden, Regionen (US-Daten)
- Felder: Order ID, Order Date, Ship Mode, Customer Name, Segment, Country, City, State, Region, Product ID, Category, Sub-Category, Product Name, Sales, Quantity, Discount, Profit

**Warum Superstore?**
- Standard-Datensatz in BI-Ausbildungen weltweit
- Realistische Komplexität ohne Datenschutzprobleme
- In Power BI bereits als Beispiel integriert

#### Schritt 1: Datenerkundung (Python/Pandas)
```python
import pandas as pd
import numpy as np

df = pd.read_csv('superstore.csv', encoding='latin-1')
print(df.shape)          # (9994, 21)
print(df.dtypes)
print(df.isnull().sum())
print(df.describe())

# Key Stats
print(f"Gesamtumsatz: ${df['Sales'].sum():,.0f}")
print(f"Gesamtgewinn: ${df['Profit'].sum():,.0f}")
print(f"Marge: {df['Profit'].sum()/df['Sales'].sum()*100:.1f}%")
print(f"Zeitraum: {df['Order Date'].min()} bis {df['Order Date'].max()}")
```

#### Schritt 2: KPI-Hierarchie definieren
**Strategisch:** Gesamtumsatz, Gesamtgewinn, Marge %
**Operativ:** Umsatz nach Region, nach Kategorie, Top-10-Produkte, Wachstum YoY
**Warnsignale:** Negative Marge nach Sub-Kategorie, Discount-Analyse

#### Schritt 3: Power BI – Step by Step
1. CSV importieren via "Daten abrufen > Text/CSV"
2. Power Query: Order Date auf datetime setzen, Duplikate prüfen
3. Measures erstellen:
   ```dax
   Umsatz = SUM(Orders[Sales])
   Gewinn = SUM(Orders[Profit])
   Marge % = DIVIDE([Gewinn], [Umsatz], 0) * 100
   Bestellungen = COUNTROWS(Orders)
   Ø Bestellwert = DIVIDE([Umsatz], [Bestellungen], 0)
   ```
4. Visuals: 4 KPI-Cards oben, Umsatz-Linie, Kategorie-Balken, Region-Karte, Profit-Scatter
5. Slicer: Jahr, Region, Kategorie
6. Formating: Einheitliche Farben, Titel, Datenbeschriftungen

#### Schritt 4: Plotly Dash – Step by Step
Komplettes `app.py` mit:
- 4 KPI-Cards (Umsatz, Gewinn, Marge, Bestellungen)
- Umsatz-Trend-Linie (monatlich aggregiert)
- Kategorie-Balkendiagramm
- Region-Balkendiagramm
- Dropdown-Filter für Segment und Region

Vollständiger Code (ca. 80–100 Zeilen) mit Kommentaren

#### Schritt 5: Vergleich
Reflexionsfragen:
1. Was dauerte länger: Power BI oder Dash?
2. Welches Dashboard lässt sich leichter anpassen?
3. Welches würdest du bei einem Kunden einsetzen – und warum?
4. Wie würdest du die Dash-App deployen?

#### YouTube-Ressourcen
- "Build a BI Dashboard in Power BI" – Guy in a Cube
- "Plotly Dash Full App Tutorial" – Charming Data: https://www.youtube.com/@CharmingData

---

### lab-06-souveraenitaet.html – Digitale Souveränität & Open-Source BI

**Lernziele:**
1. Begriff "Digitale Souveränität" definieren und kontextualisieren
2. Open-Source BI-Tools kennen und einordnen
3. Kritische Abhängigkeiten von Cloud-Anbietern erkennen
4. Einfachen Self-Hosted BI-Stack mit Docker beschreiben

**Inhalte:**

#### Was ist Digitale Souveränität?
- Definition: Fähigkeit von Organisationen/Staaten, eigene digitale Infrastruktur zu kontrollieren
- EU-Perspektive: GAIA-X, European Cloud Initiative
- Konkret für BI: Wo liegen meine Daten? Wer kann darauf zugreifen?
- DSGVO-Relevanz: Datentransfer in Drittländer (USA) problematisch bei personenbezogenen Daten

#### Cloud Lock-in analysieren
**Power BI (Microsoft):**
- Daten in Azure-Cloud (USA-Server)
- Lizenzen: Desktop kostenlos, Service ab ~9€/User/Monat
- Pro-Daten: Microsoft kann theoretisch auf Unternehmensdaten zugreifen
- Ausweg: Power BI Report Server (On-Premises) – aber teuer

**Open-Source Alternativen:**
| Tool | Typ | Docker | Stärken |
|------|-----|--------|---------|
| **Apache Superset** | Self-Hosted | Ja | Mächtig, SQL-first, große Community |
| **Metabase** | Self-Hosted + Cloud | Ja | Einfach, gut für Non-Techniker |
| **Redash** | Self-Hosted | Ja | SQL-fokussiert, API-Zugriff |
| **Plotly Dash** | Self-Hosted | Ja | Maximale Flexibilität, Python-Ökosystem |
| **Grafana** | Self-Hosted + Cloud | Ja | Ideal für Metriken/Monitoring |

#### Docker Self-Hosted Setup (Metabase als Beispiel)
```yaml
# docker-compose.yml für Metabase
version: '3'
services:
  metabase:
    image: metabase/metabase:latest
    ports:
      - "3000:3000"
    environment:
      MB_DB_TYPE: postgres
      MB_DB_DBNAME: metabase
      MB_DB_HOST: postgres
      MB_DB_USER: metabase
      MB_DB_PASS: metabasepassword
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: metabase
      POSTGRES_PASSWORD: metabasepassword
      POSTGRES_DB: metabase
    volumes:
      - metabase_data:/var/lib/postgresql/data

volumes:
  metabase_data:
```

```bash
# Starten:
docker compose up -d
# Zugriff: http://localhost:3000
```

#### DSGVO & Compliance-Checkliste
- [ ] Verarbeitungsverzeichnis angelegt?
- [ ] Auftragsverarbeitungsvertrag (AVV) mit Cloud-Anbieter?
- [ ] Datentransfer in Drittländer dokumentiert?
- [ ] Datenschutzfolgenabschätzung (DSFA) bei sensiblen Daten?
- [ ] Löschkonzept vorhanden?

#### Entscheidungsmatrix: Wann Power BI, wann Open Source?
| Szenario | Empfehlung |
|----------|-----------|
| Kleines Team, keine IT-Infrastruktur | Power BI / Metabase Cloud |
| Personenbezogene Daten (HR, Kunden) | Metabase/Superset self-hosted |
| Komplexe Custom-Dashboards | Plotly Dash |
| Public Sector / Behörden | Open Source Pflicht (EU-Richtlinien) |
| Startup, schnell deployen | Metabase + Docker |

#### Abschlussprojekt-Idee
Beschreibung: Baue einen vollständigen Self-Hosted BI-Stack:
1. PostgreSQL als Datenbank
2. Metabase als BI-Frontend
3. Superstore-Daten importieren
4. 3 Dashboards erstellen

#### YouTube-Ressourcen
- "Apache Superset Tutorial" – offizieller Channel: https://www.youtube.com/@ApacheSuperset
- "Metabase Tutorial for Beginners": Suche "Metabase tutorial 2024" auf YouTube

---

## Lab-Seiten Struktur (jede Lab-Datei)

Jede Lab-Datei hat folgende Struktur (React-basiert, identisch INME):

```
1. Navbar (sticky, wie index.html)
2. Lab-Header
   - Zurück-Link "← Übersicht"
   - Lab-Nummer (groß, Farbe)
   - Titel (h1)
   - Kurzbeschreibung
   - 3 Lernziele als Chips/Badges
3. Content-Sektionen
   - Abschnitte mit Überschriften
   - Code-Blocks (hell-grau Hintergrund, Copy-Button)
   - Tabellen (Bauhaus-Stil)
   - Info-Boxen / Tip-Boxen (blau statt rot)
4. YouTube-Ressourcen-Box
5. Nächster Lab Link → (am Ende)
6. Footer
```

## Code-Block Styling (PFLICHT – identisch INME final)
```css
.code-block {
  background: #F3F4F6;
  color: #1A1A1A;
  border-left: 4px solid #D1D5DB;
  font-family: 'Fira Code', 'Courier New', monospace;
  font-size: 0.85rem;
  padding: 1rem 1.25rem;
  border-radius: 0 8px 8px 0;
  overflow-x: auto;
}
```

Kein rotes/blaues Hintergrund für Code-Blocks! Immer hellgrau.

## CodeBlock Komponente (React)
```jsx
function CodeBlock({ code, language = '' }) {
  const [copied, setCopied] = React.useState(false);
  const copy = () => {
    navigator.clipboard.writeText(code).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    }).catch(() => {
      const el = document.createElement('textarea');
      el.value = code;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    });
  };
  return (
    <div style={{ position: 'relative', marginBottom: '1rem' }}>
      <pre className="code-block">{code}</pre>
      <button onClick={copy} style={{
        position: 'absolute', top: '0.5rem', right: '0.5rem',
        background: copied ? '#059669' : '#E5E7EB',
        color: copied ? 'white' : '#374151',
        border: 'none', borderRadius: '4px',
        padding: '0.2rem 0.5rem', fontSize: '0.75rem',
        cursor: 'pointer', fontFamily: 'Space Grotesk, sans-serif'
      }}>
        {copied ? '✓ Kopiert' : 'Kopieren'}
      </button>
    </div>
  );
}
```

---

## Allgemeine Regeln

1. **Keine Emojis** (außer in inhaltlichen Beispielen)
2. **Kein HTML in Kommentaren** im JSX – immer `{/* */}`
3. **Bilingual von Anfang an** – jeder String in `t = { de: {...}, en: {...} }` Objekt
4. **Korrekte Inhalte** – keine erfundenen DAX-Funktionen oder Plotly-Parameter
5. **Copy-Buttons** auf allen Code-Blöcken
6. **Title-Tags** korrekt: `<title>Lab 01 – Grundlagen BI · THWS BI Lab</title>`
7. **GitHub Pages kompatibel** – kein Server, kein Backend, alle Pfade relativ
8. **Konsistentes Footer-Design** – identisch auf allen Seiten
9. **Arbeite Datei für Datei** – erst `index.html` fertig, dann `lab-01`, etc.

---

## Abschluss-Aufgabe

Wenn alle 7 Dateien gebaut sind:
```bash
cd /tmp/sp_bi-lab
git add -A
git commit -m "feat: initial BI Lab site (7 pages, bilingual, Bauhaus design)"
git push origin main
```

Dann diesen Befehl ausführen um fertig zu signalisieren:
```bash
OPENCLAW_CONFIG_PATH=/Users/robert/clawd/.openclaw-macbot/openclaw.json \
OPENCLAW_STATE_DIR=/Users/robert/clawd/.openclaw-macbot \
openclaw system event --text "BI Lab fertig: 7 HTML-Seiten gebaut + gepusht nach github.com/swrobuts/sp_bi" --mode now
```

---

## Referenz-Dateien

Der komplette INME-Code liegt in `/tmp/inme-lab/`. Schau dort nach:
- `index.html` für die genaue Navbar/Hero/Stats/Grid-Struktur
- `lab-01-grundlagen.html` für die Lab-Seiten-Struktur
- `lab-06-implementation.html` für das Footer-Design

Kopiere das Strukturgerüst, ersetze Inhalte und Farben.
