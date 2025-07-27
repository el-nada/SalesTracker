from dash import html, dcc

def initialize_filter(options):
    date_range, store_options, category_options, price_slider = options
    start, end = date_range
    high, low = price_slider

    return html.Div([
        html.Div([
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
                ], className="filter-item date-picker-col"),
                
                html.Div([
                    html.Div([
                        html.Span("euro", className="material-icons icon-label"),
                        html.Label("Price Selector", className="filter-label price-label"),
                    ], className="filter-title"),

                    dcc.Slider(
                            low, high, step=(high - low) // 10,
                            value=high,
                            id='price-slider',
                            tooltip={"placement": "bottom", "always_visible": True},
                            className="styled-slider"
                        )
                ], className="filter-item price-row"),
            ], className="filter-column dropdowns-col"),

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
    ], className="filter-container")


def initialize_fc_filter(store_options, product_options):
    return html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("store", className="material-icons icon-label"),
                        html.Label("Store", className="filter-label"),
                    ], className="filter-title"),
                    dcc.Dropdown(
                        id='fc-store',
                        options=store_options, 
                        value=store_options[0]["value"],
                        placeholder="Select Store",
                        className='styled-dropdown'
                    )
                ], className="filter-item"),
                
                html.Div([
                    html.Div([
                        html.Span("category", className="material-icons icon-label"),
                        html.Label("Product", className="filter-label"),
                    ], className="filter-title"), 
                    dcc.Dropdown(
                        id='fc-product',
                        options=product_options, 
                        value=product_options[0]["value"],
                        placeholder="Select Product",
                        className='styled-dropdown'
                    )
                ], className="filter-item "),
            ], className="filter-column dropdowns-col"),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.Span("calendar_month", className="material-icons icon-label"),
                        html.Label("Forecast Horizon", className="filter-label"),
                    ], className="filter-title"), 
                    dcc.Slider(
                        id="fc-horizon", 
                        min=4, 
                        max=16, 
                        step=4, 
                        value=8,
                        marks={4: "4w", 8: "8w", 12: "12w", 16: "16w"}, 
                        className="styled-slider",
                    )
                ], className="filter-item "),
                
                html.Div([
                    html.Button(
                        "Run Forecast", 
                        id="fc-button", 
                        n_clicks=0,
                        className="run-button"
                    )
                ], className="filter-item"),
            ], className="filter-column dropdowns-col"),
        ], className="filter-row first-row"),
    ], className="filter-container")
])
