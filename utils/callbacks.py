import plotly.express as px
import dash 
from dash import Output, Input
from utils.data_loader import load_data, compute_kpis
from components.cards import initialize_cards

def register_callbacks(app):
    @app.callback(
        Output('graph-id', 'figure'),
        Input('store-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'), 
        Input('price-slider', 'value')
    )

    def update_graph(store, category, start_date, end_date, price):
        df = load_data()

        # Apply filters
        if store:
            df = df[df['Store ID'] == store]
        if category:
            df = df[df['Category'] == category]
        if start_date and end_date:
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if price : 
            df = df[df['Price'] <= price]

        fig = px.line(df, x='Date', y='Units Sold', color='Store ID')
        return fig
    
    @app.callback(
        Output('cards', 'children'),
        Input('store-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'), 
        Input('price-slider', 'value')
    )

    def update_KPI(store, category, start_date, end_date, price):
        df = load_data()

        # Apply filters
        if store:
            df = df[df['Store ID'] == store]
        if category:
            df = df[df['Category'] == category]
        if start_date and end_date:
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if price : 
            df = df[df['Price'] <= price]

        kpi_values = compute_kpis(df)

        return initialize_cards(kpi_values)