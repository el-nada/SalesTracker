from dash import Output, Input, State
from utils.data_loader import compute_kpis, load_filtered_data
from components.cards import initialize_cards
from components.layout import historical_layout, forecast_layout
from utils.data_loader import load_data
from utils.charts import *
from model.train import create_features, build_model
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
def register_callbacks(app):
    @app.callback(
        Output('cards', 'children'),
        Input('store-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'), 
        Input('price-slider', 'value')
    )
    def update_KPI(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        kpi_values = compute_kpis(df)
        return initialize_cards(kpi_values)
    
    @app.callback(
        Output('graph-id', 'figure'),
        Input('store-dropdown', 'value'),
        Input('category-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date'), 
        Input('price-slider', 'value')
    )
    def update_sales_chart(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        
        if df.empty:
            return generate_empty_graph()

        return generate_monthly_chart(df)
    
    @app.callback(
            Output('inventory-sales-chart', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_inventory_chart(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_inventory_sales_chart(df, 10)
    
    @app.callback(
            Output('category-region-treemap', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_category_treemap(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_category_treemap(df)
    
    @app.callback(
            Output('promo-impact-delta-chart', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_promo_impact(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_promo_impact(df)
    
    @app.callback(
            Output('discount-vs-sales-chart', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_discount_distribution(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_discount_distribution(df)
    
    @app.callback(
            Output('price-demand-heatmap', 'figure'),
            Input('store-dropdown', 'value'),
            Input('category-dropdown', 'value'),
            Input('date-range', 'start_date'),
            Input('date-range', 'end_date'), 
            Input('price-slider', 'value')
        )
    def update_avg_demand(store, category, start_date, end_date, price):
        df = load_filtered_data(store, category, start_date, end_date, price)
        if df.empty:
            return generate_empty_graph()

        return generate_avg_demand(df)
    
    @app.callback(
        Output("tabs-content", "children"),
        Input("main-tabs", "value")
    )
    def render_tab(tab):
        data = load_data()  # You can cache this if expensive
        if tab == "historical":
            return historical_layout(data)
        else:
            return forecast_layout()
        
    @app.callback(
        Output("fc-forecast-graph", "figure"),
        Output("fc-kpi", "children"),
        Input("fc-button", "n_clicks"),
        State("fc-store",   "value"),
        State("fc-product", "value"),
        State("fc-horizon", "value")
    )
    def run_forecast(n_clicks, store_id, product_id, horizon):
        if n_clicks == 0:
            return go.Figure(), ""

        # 1) Build weekly features for the chosen store/product
        df = load_data()
        df = df[(df["Store ID"]==store_id) & (df["Product ID"]==product_id)]
        weekly = create_features(df)  # this is your weekly Sales + lags + etc.

        # 2) If not enough weeks, bail
        if len(weekly) < horizon + 1:
            fig = go.Figure()
            fig.update_layout(title="Not enough data for that horizon")
            return fig, "Insufficient history"

        # 3) Split train / test on the last `horizon` weeks
        X = weekly.drop(columns=['Units_Sold','Week_Marker','Week_Start','Week_End','Days_in_Week'])
        y = weekly['Units_Sold']
        X_train, X_test = X.iloc[:-horizon], X.iloc[-horizon:]
        y_train, y_test = y.iloc[:-horizon], y.iloc[-horizon:]

        # 4) Fit (or just load) your model on X_train/y_train
        #    For speed you can load a pre‑trained model, but here we refit:
        model = build_model()
        model.fit(X_train, y_train)

        # 5) Predict those last `horizon` weeks
        preds = model.predict(X_test)

        # 6) Build the figure overlaying actual vs. predicted
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=weekly['Week_Start'].iloc[-horizon:],
            y=y_test,
            mode='lines+markers',
            name='Actual'
        ))
        fig.add_trace(go.Scatter(
            x=weekly['Week_Start'].iloc[-horizon:],
            y=preds,
            mode='lines+markers',
            name='Forecast'
        ))
        fig.update_layout(
            title=f"{store_id} / {product_id} Forecast",
            xaxis_title="Week Start",
            yaxis_title="Units Sold"
        )

        # 7) Compute a quick KPI summary
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        kpi_text = f"Last {horizon} weeks MAE: {mae:.1f} units \n  RMSE : {rmse:.1f} units \n R2 : {r2:.3f}"

        return fig, kpi_text