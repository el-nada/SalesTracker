from components.filters import initialize_filter
from components.cards import initialize_cards
from components.charts import initialize_chart, initialize_inventory_sales_chart, initialize_discount_vs_sales_chart, initialize_category_region_stacked_bar, initialize_category_region_treemap, initialize_discount_vs_sales_scatter, initialize_promotion_over_time_chart, initialize_seasonality_epidemic_chart, initialize_price_demand_correlation_chart, initialize_weather_sales_bar
from utils.data_loader import load_data, compute_kpis, compute_filter_args
from dash import html

def create_layout():
    data = load_data()
    filter_args = compute_filter_args(data)
    kpi_values = compute_kpis(data)

    return html.Div([
        html.Div(initialize_filter(filter_args), className="filter-section"),

        html.Div([
            html.Div([
                html.Div(
                    [html.Div(card) for card in initialize_cards(kpi_values).children],
                    className="kpi-row"
                ),
                html.Div(initialize_chart(data), className="chart-box"),
            ], className="left-panel"),

            html.Div(initialize_inventory_sales_chart(data), className="chart-box full-height"),
        ], className="dashboard-row"),
        html.Div([
            html.Div(initialize_category_region_stacked_bar(data), className="chart-box"),
            html.Div(initialize_category_region_treemap(data), className="chart-box"),
        ], className="chart-row"),

        # === ROW 3 ===
        html.Div([
            html.Div(initialize_promotion_over_time_chart(data), className="chart-box"),
            html.Div(initialize_discount_vs_sales_chart(data), className="chart-box"),
        ], className="chart-row"),

        # === ROW 4 ===
        html.Div([
            html.Div(initialize_discount_vs_sales_scatter(data), className="chart-box"),
            html.Div(initialize_seasonality_epidemic_chart(data), className="chart-box"),
        ], className="chart-row"),

        # === ROW 5 ===
        html.Div([
            html.Div(initialize_price_demand_correlation_chart(data), className="chart-box"),
            html.Div(initialize_weather_sales_bar(data), className="chart-box"),
        ], className="chart-row"),

    ], className="dashboard-container")