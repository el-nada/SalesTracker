import dash
from dash import html, dcc, dash_table

def initialize_chart(data):
    
    return dash_table.DataTable(data=data.to_dict('records'), page_size=10)
