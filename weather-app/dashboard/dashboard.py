import dash
import plotly.express as px
from flask import Flask, session
from dash import dcc, html, Input, Output

from utils import create_dataframe

def init_dashboard(app: Flask):

    @dash.callback(
        Output("graph", "figure"),
        Input("urzl", "pathname"),
        Input("parameter-dropdown", "value") 
    )
    def update_graph(pathname, selected_parameter):
        if pathname == "/dash/":
            weather_cities = session.get("weather_cities")
            if weather_cities is None:
                return dash.no_update
            df = create_dataframe(weather_cities)

            if selected_parameter is None:  
                selected_parameter = "temperature" 

            labels = {
                "date": "Дата",
                "temperature": "Температура",
                "humidity": "Влажность",
                "precipitation": "Осадки",
                "wind_speed": "Скорость ветра",
                "cloud_cover": "Облачность",
                "city": "Город"  
            }

            return px.line(df, 
                         x="date", 
                         y=selected_parameter, 
                         color="city",
                         labels=labels) 


    dash_module = dash.Dash(
        server=app,
        routes_pathname_prefix="/dash/",
    )

    dash_module.layout = html.Div([
        dcc.Location(id="urzl"),
        dcc.Dropdown( 
            id="parameter-dropdown",
            options=[
                {"label": "Температура", "value": "temperature"},
                {"label": "Влажность", "value": "humidity"},
                {"label": "Осадки", "value": "precipitation"},
                {"label": "Скорость ветра", "value": "wind_speed"},
                {"label": "Облачность", "value": "cloud_cover"},
            ],
            value="temperature",
            clearable=False, 
            style={"width": "200px", "margin-bottom": "10px"}
        ),
        dcc.Graph(id="graph", style={"width": "100%"}),
    ], style={"height": "auto", "width": "100%", "position": "relative"})

    return dash_module.server