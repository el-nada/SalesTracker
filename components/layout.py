from components.filters import initialize_filter
from components.cards import initialize_cards
from components.charts import initialize_chart, initialize_inventory_sales_chart, initialize_discount_disctribution, initialize_category_region_treemap, initialize_promo_vs_no_promo, initialize_price_demand_correlation_chart
from utils.data_loader import load_data, compute_kpis, compute_filter_args
from dash import html
from dash import dcc

def create_layout():
    data = load_data()
    filter_args = compute_filter_args(data)
    kpi_values = compute_kpis(data)

    return html.Div([
        dcc.Tabs(id="main-tabs", value="historical", children=[
            dcc.Tab(label="Historical Dashboard", value="historical"),
            dcc.Tab(label="Forecast & What‑If",  value="forecast"),
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

def forecast_layout():
    # Load once at startup
    raw_data = load_data()  

    # Build store/product dropdown options
    store_options = [
        {"label": s, "value": s}
        for s in sorted(raw_data["Store ID"].unique())
    ]
    product_options = [
        {"label": p, "value": p}
        for p in sorted(raw_data["Product ID"].unique())
    ]

    return html.Div([
        html.Div([
            html.Div([
                html.Label("Select Store"),
                dcc.Dropdown(id="fc-store", options=store_options, value=store_options[0]["value"]) 
            ], className="four columns"),
            html.Div([
                html.Label("Select Product"),
                dcc.Dropdown(id="fc-product", options=product_options, value=product_options[0]["value"])
            ], className="four columns"),
            html.Div([
                html.Label("Forecast Horizon (weeks)"),
                dcc.Slider(id="fc-horizon", min=4, max=16, step=4, value=8,
                           marks={4: "4w", 8: "8w", 12: "12w", 16: "16w"})
            ], className="four columns"),
        ], className="row filter-section"),
        html.Div([
            html.Button("Run Forecast", id="fc-button", n_clicks=0)
        ], className="row"),
        html.Div(dcc.Graph(id="fc-forecast-graph"), className="chart-box"),
        html.Div([
            html.H4("Predicted Units Sold:"),
            html.Div(id="fc-kpi", className="kpi-card")
        ], className="row"),
    ])
