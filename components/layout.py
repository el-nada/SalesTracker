from components.filters import initialize_filter
from components.cards import initialize_card
from components.charts import initialize_chart
from utils.data_loader import load_data, compute_kpis

import pandas as pd
import dash
from dash import html, dcc

def create_layout():

    data = load_data()
    kpi_values = compute_kpis(data)

    sales_is_positive = float(kpi_values["delta_sales"].replace('%', '')) > 0
    units_is_positive = float(kpi_values["delta_units"].replace('%', '')) > 0

    return html.Div([
        initialize_filter(data['Store ID'].unique() , data['Category'].unique()),

        html.Div([
            initialize_card("Total Sales", kpi_values["total_sales"], kpi_values["delta_sales"], sales_is_positive>0),
            initialize_card("Units Sold", kpi_values["units_sold"], kpi_values["delta_units"], units_is_positive>0),
        ], className="card-container"), 

        initialize_chart(data)
    ])