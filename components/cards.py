import dash
from dash import html, dcc


def initialize_cards(kpi_values): 
    sales_is_positive = float(kpi_values["delta_sales"].replace('%', '')) > 0
    units_is_positive = float(kpi_values["delta_units"].replace('%', '')) > 0

    return html.Div([
            initialize_card("Total Sales", kpi_values["total_sales"], kpi_values["delta_sales"], sales_is_positive>0),
            initialize_card("Units Sold", kpi_values["units_sold"], kpi_values["delta_units"], units_is_positive>0),
        ], className="card-container", id="cards")


def initialize_card(title, value, delta, is_positive):
    color = "green" if is_positive else "red"
    return html.Div([
        html.H4(title),
        html.H2(f"{value}"),
        html.P(f"Δ {delta}", style={"color": color})
    ], className="kpi-card")
