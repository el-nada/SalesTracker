from components.filters import initialize_filter
from components.cards import initialize_cards
from components.charts import initialize_chart
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
        initialize_chart(data)
    ])