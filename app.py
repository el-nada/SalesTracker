import dash
from dash import html, dcc

from components.layout import create_layout
from utils.callbacks import register_callbacks

app = dash.Dash(__name__)
register_callbacks(app)

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)
