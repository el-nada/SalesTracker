import dash
from dash import html, dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard"),
    html.Div([
        dcc.DatePickerRange(id='date-range'),
        dcc.Dropdown(id='store-dropdown'),
        dcc.Dropdown(id='category-dropdown'),
    ]),
    dcc.Graph(id='main-chart')
])

if __name__ == '__main__':
    app.run(debug=True)
