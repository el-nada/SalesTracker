from dash import html, dcc

def initialize_filter(options):
    date_range, store_options, category_options, price_slider = options
    start, end = date_range
    high, low = price_slider

    return html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Span("date_range", className="material-icons icon-label"),
                    html.Label("Date Range", className="filter-label"),
                ], className="filter-title"),

                dcc.DatePickerRange(
                    id='date-range',
                    min_date_allowed=start,
                    max_date_allowed=end,
                    className='styled-date-picker'
                ),
            ], className="filter-column date-picker-col"),

            html.Div([
                html.Div([
                    html.Div([
                        html.Span("store", className="material-icons icon-label"),
                        html.Label("Store", className="filter-label"),
                    ], className="filter-title"),
                    
                    dcc.Dropdown(
                        id='store-dropdown',
                        options=[{'label': store, 'value': store} for store in store_options],
                        placeholder="Select Store",
                        className='styled-dropdown'
                    )
                ], className="filter-item"),

                html.Div([
                    html.Div([
                        html.Span("category", className="material-icons icon-label"),
                        html.Label("Category", className="filter-label"),
                    ], className="filter-title"), 

                    dcc.Dropdown(
                        id='category-dropdown',
                        options=[{'label': category, 'value': category} for category in category_options],
                        placeholder="Select Category",
                        className='styled-dropdown'
                    )
                ], className="filter-item"),
            ], className="filter-column dropdowns-col"),
        ], className="filter-row first-row"),

    
        html.Div([
            html.Span("euro", className="material-icons icon-label"),
            html.Label("Price Selector", className="filter-label price-label"),
            dcc.Slider(
                low, high, step=(high - low) // 10,
                value=high,
                id='price-slider',
                tooltip={"placement": "bottom", "always_visible": True},
                className="styled-slider"
            )
        ], className="filter-row price-row"),
    ], className="filter-container")
