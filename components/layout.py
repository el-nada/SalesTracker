from components.filters import initialize_filter
from components.cards import initialize_cards
from components.charts import initialize_chart, initialize_inventory_sales_chart, initialize_discount_disctribution, initialize_category_region_treemap, initialize_promo_vs_no_promo, initialize_price_demand_correlation_chart
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
                    initialize_cards(kpi_values).children,id="cards"
                ),
                html.Div(initialize_chart(data), className="chart-box"),
            ], className="left-panel"),

            html.Div(initialize_inventory_sales_chart(data), className="chart-box full-height"),
        ], className="dashboard-row"),
        
        html.Div([
            html.Div(initialize_category_region_treemap(data), className="chart-box"),
            html.Div(initialize_promo_vs_no_promo(data), className="chart-box"),
            html.Div(initialize_discount_disctribution(data), className="chart-box"),
            html.Div(initialize_price_demand_correlation_chart(data), className="chart-box"),
        ], className="chart-grid")

    ], className="dashboard-container")