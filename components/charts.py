import dash
from dash import html, dcc, dash_table
import plotly.express as px

def initialize_chart(data):
    fig = px.line(data, x='Date', y='Units Sold', color='Store ID')
    return dcc.Graph(figure=fig)
