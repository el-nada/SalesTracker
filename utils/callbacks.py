from dash import Output, Input
from utils.data_loader import compute_kpis, load_filtered_data
from components.cards import initialize_cards
from utils.charts import *

    
def register_callbacks(app):
    @app.callback(
        Output('cards', 'children'),
        Input('store-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'), 
        Input('price-slider', 'value')
    )
    def update_KPI(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        kpi_values = compute_kpis(df)
        return initialize_cards(kpi_values)
    
    @app.callback(
        Output('graph-id', 'figure'),
        Input('store-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'), 
        Input('price-slider', 'value')
    )
    def update_sales_chart(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        
        if df.empty:
            return generate_empty_graph()

        return generate_monthly_chart(df)
    
    @app.callback(
            Output('inventory-sales-chart', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_inventory_chart(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_inventory_sales_chart(df, 10)
    
    @app.callback(
            Output('category-region-treemap', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_category_treemap(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_category_treemap(df)
    
    @app.callback(
            Output('promo-impact-delta-chart', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_promo_impact(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_promo_impact(df)
    
    @app.callback(
            Output('discount-vs-sales-chart', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_discount_distribution(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_discount_distribution(df)
    
    @app.callback(
            Output('price-demand-heatmap', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_avg_demand(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_avg_demand(df)