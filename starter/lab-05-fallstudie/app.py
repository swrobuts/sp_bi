# app.py – Superstore Retail Analytics Dashboard
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# Ein Dashboard, das auf dem Handy bricht, ist kein fertiges Dashboard.
# Feste Spaltenzahlen (repeat(4, 1fr)) sprengen jedes schmale Display,
# deshalb liegt das Raster in CSS mit Media Queries statt in Inline-Styles.
app.index_string = """<!DOCTYPE html>
<html>
  <head>
    {%metas%}<title>{%title%}</title>{%favicon%}{%css%}
    <style>
      body { margin: 0; font-family: -apple-system, BlinkMacSystemFont,
             'Segoe UI', sans-serif; }
      .kpi-grid, .chart-grid { display: grid; gap: 1rem; }
      .kpi-grid   { padding: 1rem 2rem;   grid-template-columns: 1fr; }
      .chart-grid { padding: 0 2rem 1rem; grid-template-columns: 1fr; }
      .filter-row { display: flex; flex-wrap: wrap; gap: 1rem;
                    padding: 1rem 2rem; background: #f8fafc; }
      /* min-width: 0 ist noetig, sonst schrumpfen Flex-Kinder nicht unter
         ihre Inhaltsbreite - derselbe Fallstrick wie bei den Lab-Seiten. */
      .filter-row > div { flex: 1 1 240px; min-width: 0; }
      @media (min-width: 640px)  { .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
      @media (min-width: 1000px) { .kpi-grid   { grid-template-columns: repeat(4, 1fr); }
                                   .chart-grid { grid-template-columns: 1fr 1fr; } }
      /* Plotly zeichnet in SVG und richtet sich nicht von allein nach dem
         Container - ohne diese Regel ragen die Diagramme heraus. */
      .js-plotly-plot, .plot-container, .dash-graph { max-width: 100%; }
    </style>
  </head>
  <body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body>
</html>"""

# Daten laden und vorbereiten
df = pd.read_csv('train.csv', encoding='latin-1')
# TT/MM/JJJJ -> dayfirst=True zwingend
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()

# Farben als Python-Konstanten (NICHT CSS-Variablen!)
# Plotly rendert zu SVG/Canvas, nicht ins DOM –
# var(--col-primary) funktioniert dort nicht.
COL_PRIMARY = '#1E3A8A'
COL_ACCENT  = '#2563EB'

app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Superstore Analytics Dashboard',
                style={'margin': '0', 'fontSize': '1.5rem'}),
    ], style={'background': COL_PRIMARY, 'color': 'white',
              'padding': '1rem 2rem'}),

    # Filter
    html.Div([
        html.Div([
            html.Label('Segment:'),
            dcc.Dropdown(
                id='segment-filter',
                options=[{'label': s, 'value': s}
                         for s in df['Segment'].unique()],
                value=df['Segment'].unique().tolist(),
                multi=True, clearable=False
            ),
        ], style={'flex': 1}),
        html.Div([
            html.Label('Region:'),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': r, 'value': r}
                         for r in df['Region'].unique()],
                value=df['Region'].unique().tolist(),
                multi=True, clearable=False
            ),
        ], style={'flex': 1}),
    ], className='filter-row'),

    # KPI Cards
    html.Div(id='kpi-cards', className='kpi-grid'),

    # Charts
    html.Div([
        dcc.Graph(id='trend-chart', config={'responsive': True}),
        dcc.Graph(id='category-chart', config={'responsive': True}),
    ], className='chart-grid'),

    dcc.Graph(id='scatter-chart', config={'responsive': True},
              style={'padding': '0 2rem 2rem'}),
])

def kpi_card(title, value, color=COL_PRIMARY):
    return html.Div([
        html.Div(value, style={'fontSize': '1.75rem', 'fontWeight': '800',
                               'color': color}),
        html.Div(title, style={'fontSize': '0.75rem', 'color': '#6B7280',
                               'textTransform': 'uppercase',
                               'letterSpacing': '0.08em'}),
    ], style={'background': 'white', 'padding': '1.25rem',
              'border': '1px solid #e5e7eb',
              'borderLeft': f'4px solid {color}'})

@app.callback(
    Output('kpi-cards', 'children'),
    Output('trend-chart', 'figure'),
    Output('category-chart', 'figure'),
    Output('scatter-chart', 'figure'),
    Input('segment-filter', 'value'),
    Input('region-filter', 'value')
)
def update_dashboard(segments, regions):
    fdf = df[df['Segment'].isin(segments) &
             df['Region'].isin(regions)]

    # KPI Cards
    total_sales = fdf['Sales'].sum()
    orders = fdf['Order ID'].nunique()
    positions = len(fdf)
    avg_order = total_sales / orders if orders else 0

    cards = [
        kpi_card('Umsatz', f'${total_sales:,.0f}'),
        kpi_card('Bestellungen', f'{orders:,}'),
        kpi_card('Ø Bestellwert', f'${avg_order:,.0f}', COL_ACCENT),
        kpi_card('Positionen', f'{positions:,}'),
    ]

    # Trend
    trend = fdf.groupby('Month')['Sales'].sum().reset_index()
    fig1 = px.line(trend, x='Month', y='Sales',
                   title='Umsatz-Trend (monatlich)',
                   color_discrete_sequence=[COL_ACCENT])
    fig1.update_layout(plot_bgcolor='white', paper_bgcolor='white')

    # Kategorie
    by_cat = fdf.groupby('Category')['Sales'].sum().reset_index()
    fig2 = px.bar(by_cat, x='Category', y='Sales',
                  title='Umsatz nach Kategorie',
                  color_discrete_sequence=[COL_PRIMARY])
    fig2.update_layout(plot_bgcolor='white', paper_bgcolor='white')

    # Scatter
    by_sub = fdf.groupby('Sub-Category').agg(
        Sales=('Sales','sum'), Positionen=('Order ID','count')
    ).reset_index()
    fig3 = px.scatter(by_sub, x='Positionen', y='Sales',
                      text='Sub-Category', size='Sales',
                      title='Umsatz vs. Bestellpositionen nach Sub-Kategorie',
                      color_discrete_sequence=[COL_ACCENT])
    fig3.update_traces(textposition='top center')
    fig3.update_layout(plot_bgcolor='white', paper_bgcolor='white')

    return cards, fig1, fig2, fig3

if __name__ == '__main__':
    app.run(debug=True)
