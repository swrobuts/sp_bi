import plotly.express as px
import pandas as pd

df = pd.read_csv('train.csv', encoding='latin-1')

# Umsatz nach Kategorie (Balkendiagramm)
fig = px.bar(
    df.groupby('Category')['Sales'].sum().reset_index(),
    x='Category',
    y='Sales',
    title='Umsatz nach Kategorie',
    color_discrete_sequence=['#2563EB']
)
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font_family='Space Grotesk'  # Font muss via Google Fonts geladen sein; lokal ggf. weglassen
)
fig.show()

# Umsatz-Trend über Zeit (Linie)
# dayfirst=True ist Pflicht: die Daten liegen als TT/MM/JJJJ vor.
# Ohne den Parameter bricht pandas ab, sobald der Tag > 12 ist.
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly['Order Date'] = monthly['Order Date'].astype(str)

fig2 = px.line(
    monthly,
    x='Order Date',
    y='Sales',
    title='Monatlicher Umsatz-Trend'
)
fig2.show()

# Scatter: Umsatz vs. Bestellanzahl je Sub-Kategorie
# Der Datensatz enthaelt als einzige Kennzahl 'Sales'. Eine zweite
# Dimension gewinnt man durch Aggregation - hier die Zahl der Positionen.
by_sub = df.groupby(['Category', 'Sub-Category']).agg(
    Umsatz=('Sales', 'sum'),
    Positionen=('Order ID', 'count')
).reset_index()

fig3 = px.scatter(
    by_sub,
    x='Positionen',
    y='Umsatz',
    color='Category',
    text='Sub-Category',
    size='Umsatz',
    title='Umsatz vs. Bestellpositionen je Sub-Kategorie'
)
fig3.update_traces(textposition='top center')
fig3.show()
