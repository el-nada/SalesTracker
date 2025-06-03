import dash
from dash import html, dcc

def initialize_filter(options):
    date_range, store_options, category_options, price_slider = options
    start, end = date_range
    high, low = price_slider

    return html.Div([
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=start,
            max_date_allowed=end,
        ),

        dcc.Dropdown(
            id='store-dropdown',
            options=[{'label': store, 'value': store} for store in store_options],
            placeholder="Select Store"
        ),

        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': category, 'value': category} for category in category_options],
            placeholder="Select Category"
        ), 

        dcc.Slider(
            low, high, (high-low)/10,
            value=high,
            id='price-slider'
        )
    ])
