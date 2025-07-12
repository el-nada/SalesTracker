from dash import Output, Input
from utils.data_loader import compute_kpis, load_filtered_data
from components.cards import initialize_cards

from utils.charts import generate_monthly_chart, generate_empty_graph, generate_inventory_sales_chart

    
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
    
    # Monthly sales 
    @app.callback(
        Output('graph-id', 'figure'),
        Input('store-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'), 
        Input('price-slider', 'value')
    )

    def update_graph(store, category, start_date, end_date, price):
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
    def update_graph(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_inventory_sales_chart(df, 10)