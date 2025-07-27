from components.filters import initialize_filter, initialize_fc_filter
from components.cards import initialize_cards, initialize_fc_card
from components.charts import initialize_chart, initialize_inventory_sales_chart, initialize_discount_disctribution, initialize_category_region_treemap, initialize_promo_vs_no_promo, initialize_price_demand_correlation_chart
from utils.data_loader import load_data, compute_kpis, compute_filter_args
from utils.charts import generate_empty_graph
from dash import html
from dash import dcc

def create_layout():
    return html.Div([
        dcc.Tabs(id="main-tabs", value="historical", children=[
            dcc.Tab(label="Dashboard", value="historical"),
            dcc.Tab(label="Forecast ",  value="forecast"),
        ]),
        html.Div(id="tabs-content")
    ], className="dashboard-container")
    
def historical_layout(data):
    filter_args = compute_filter_args(data)
    kpi_values = compute_kpis(data)
    return html.Div([
        html.Div(initialize_filter(filter_args), className="filter-section"),

        html.Div([
            html.Div([
                 html.Div(
                    id="cards-container",
                    className="kpi-row", 
                    children=initialize_cards(kpi_values)
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

def forecast_layout():
    raw_data = load_data()  
    
    store_options = [
        {"label": s, "value": s}
        for s in sorted(raw_data["Store ID"].unique())
    ]
    product_options = [
        {"label": p, "value": p}
        for p in sorted(raw_data["Product ID"].unique())
    ]

    # Create default KPI cards
    default_kpis = html.Div([
        initialize_fc_card("MAE", "-"),
        initialize_fc_card("RMSE", "-"),
        initialize_fc_card("R²", "-"),
    ], className="fc-kpi-row", id="fc-kpi-row")

    return html.Div([
        html.Div(initialize_fc_filter(store_options, product_options), className="filter-section"),
        
        html.Div([
            html.Div([
                html.Div([
                    html.H4("Forecast Performance", className="kpi-section-title"),
                    default_kpis  
                ], className="kpi-container")
            ], className="kpi-column"),
            
            html.Div([
                html.Div([
                    dcc.Graph(
                        id="fc-forecast-graph",
                        figure=generate_empty_graph() 
                    )
                ], className="chart-box")
            ], className="graph-column"),
        ], className="row main-content-row"),
    ], className="dashboard-container")