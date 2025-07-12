from components.filters import initialize_filter
from components.cards import initialize_cards
from components.charts import initialize_chart, initialize_inventory_sales_chart, initialize_discount_vs_sales_chart, initialize_category_region_stacked_bar, initialize_category_region_treemap, initialize_discount_vs_sales_scatter, initialize_promotion_over_time_chart, initialize_seasonality_epidemic_chart, initialize_price_demand_correlation_chart, initialize_weather_sales_bar
from utils.data_loader import load_data, compute_kpis, compute_filter_args

import dash
from dash import html

def create_layout():

    data = load_data()
    filter_args = compute_filter_args(data)
    kpi_values = compute_kpis(data)

    return html.Div([
        initialize_filter(filter_args),
        initialize_cards(kpi_values),
        initialize_chart(data),
        initialize_inventory_sales_chart(data),
        initialize_category_region_stacked_bar(data),
        initialize_category_region_treemap(data),
        initialize_promotion_over_time_chart(data),
        initialize_discount_vs_sales_chart(data), 
        initialize_discount_vs_sales_scatter(data), 
        initialize_seasonality_epidemic_chart(data),
        initialize_price_demand_correlation_chart(data),
        initialize_weather_sales_bar(data)
    ])