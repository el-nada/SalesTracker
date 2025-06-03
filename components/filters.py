import dash
from dash import html, dcc

def initialize_filter(store_options, category_options): 
    return html.Div([
        dcc.DatePickerRange(id='date-range'),

        dcc.Dropdown(
            id='store-dropdown',
            options=[{'label': store, 'value': store} for store in store_options],
            placeholder="Select Store"
        ),

        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in category_options],
            placeholder="Select Category"
        )
    ])
