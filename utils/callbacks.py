from dash import Output, Input, State
from utils.data_loader import compute_kpis, load_filtered_data, make_forecast_kpis
from components.cards import initialize_cards, initialize_fc_card
from components.layout import historical_layout, forecast_layout
from utils.data_loader import load_data
from utils.charts import *
from model.train import get_forecast
from dash import html 

def register_callbacks(app):
    @app.callback(
        Output('cards-container', 'children'),  # Update the container's children
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
    
    @app.callback(
        Output("tabs-content", "children"),
        Input("main-tabs", "value")
    )
    def render_tab(tab):
        data = load_data()  # You can cache this if expensive
        if tab == "historical":
            return historical_layout(data)
        else:
            return forecast_layout()
        
    @app.callback(
        Output("fc-forecast-graph", "figure"),
        Output("fc-kpi-row", "children"), 
        Input("fc-button", "n_clicks"),
        State("fc-store", "value"),
        State("fc-product", "value"),
        State("fc-horizon", "value")
    )
    def run_forecast(n_clicks, store_id, product_id, horizon):
        if n_clicks == 0:
            return generate_empty_graph(), [
                initialize_fc_card("MAE", "-"),
                initialize_fc_card("RMSE", "-"),
                initialize_fc_card("R²", "-")
            ]
        
        weekly, (y_test, preds), err = get_forecast(store_id, product_id, horizon)
        
        if err:
            return generate_empty_graph(), [
                initialize_fc_card("Error", err, is_error=True)
            ]
        
        fig = make_forecast_chart(weekly, y_test, preds, horizon, store_id, product_id)
        kpis = make_forecast_kpis(y_test, preds)
        
        return fig, [
            initialize_fc_card("MAE", kpis["MAE"]),
            initialize_fc_card("RMSE", kpis['RMSE']),
            initialize_fc_card("R²", kpis['R²'])
        ]