import dash
from dash import html, dcc

from components.layout import create_layout
from utils.callbacks import register_callbacks
import dash_bootstrap_components 

app = dash.Dash(__name__, external_stylesheets=[
    "https://fonts.googleapis.com/icon?family=Material+Icons",
    "https://use.fontawesome.com/releases/v5.15.4/css/all.css"
])

register_callbacks(app)

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)
