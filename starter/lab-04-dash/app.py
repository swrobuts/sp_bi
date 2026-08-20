# app.py – Vollständiges Dash-Dashboard
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)
server = app.server  # Nötig für gunicorn app:server
df = pd.read_csv('train.csv', encoding='latin-1')

app.layout = html.Div([
    html.H1('Sales Dashboard', style={'fontFamily': 'Space Grotesk', 'color': '#1E3A8A'}),

    html.Label('Kategorie auswählen:'),
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': c, 'value': c} for c in df['Category'].unique()],
        value=df['Category'].unique()[0],
        clearable=False
    ),

    dcc.Graph(id='subcategory-chart'),
    dcc.Graph(id='orders-scatter')
], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '2rem'})


@app.callback(
    Output('subcategory-chart', 'figure'),
    Input('category-filter', 'value')
)
def update_bar(category):
    filtered = df[df['Category'] == category]
    sales_by_sub = filtered.groupby('Sub-Category')['Sales'].sum().reset_index()
    fig = px.bar(
        sales_by_sub,
        x='Sub-Category',
        y='Sales',
        title=f'Umsatz nach Sub-Kategorie: {category}',
        color_discrete_sequence=['#2563EB']
    )
    return fig


@app.callback(
    Output('orders-scatter', 'figure'),
    Input('category-filter', 'value')
)
def update_scatter(category):
    filtered = df[df['Category'] == category]
    by_sub = filtered.groupby('Sub-Category').agg(
        Umsatz=('Sales', 'sum'),
        Positionen=('Order ID', 'count')
    ).reset_index()
    fig = px.scatter(
        by_sub,
        x='Positionen',
        y='Umsatz',
        text='Sub-Category',
        size='Umsatz',
        title=f'Umsatz vs. Bestellpositionen: {category}',
        color_discrete_sequence=['#0D9488']
    )
    fig.update_traces(textposition='top center')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
