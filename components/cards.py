import dash
from dash import html, dcc

def initialize_card(title, value, delta, is_positive):
    color = "green" if is_positive else "red"
    return html.Div([
        html.H4(title),
        html.H2(f"{value}"),
        html.P(f"Δ {delta}", style={"color": color})
    ], className="kpi-card")
