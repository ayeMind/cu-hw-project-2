import dash
from flask import Flask

def init_dashboard(app: Flask):
    dash_module = dash.Dash(
        server=app,
        routes_pathname_prefix="/dash/",
    )
    
    dash_module.layout = dash.html.Div([
        dash.dcc.Location(id="urzl"),
        dash.html.Div(id="page-content")
    ])

    return dash_module.server