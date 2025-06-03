from components.filters import initialize_filter
from components.cards import initialize_card
from components.charts import initialize_chart
from utils.data_loader import load_data

import dash
from dash import html, dcc

def create_layout():
    return html.Div([
        initialize_filter(),
        html.Div([initialize_card("t", "t", "t", "t"), initialize_card("t", "t", "t", "t")]),
        initialize_chart(load_data())
    ])