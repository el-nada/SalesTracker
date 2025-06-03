import dash
from dash import html, dcc

def initialize_filter(): 
    return html.Div([
        dcc.DatePickerRange(id='date-range'),
        dcc.Dropdown(id='store-dropdown'),
        dcc.Dropdown(id='category-dropdown'),
    ])
