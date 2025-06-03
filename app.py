import dash
from dash import html, dcc

from components.layout import create_layout
app = dash.Dash(__name__)

app.layout = create_layout()

if __name__ == '__main__':
    app.run(debug=True)
