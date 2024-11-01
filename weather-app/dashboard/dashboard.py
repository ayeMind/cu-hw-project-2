import dash
import plotly.express as px
from flask import Flask, session
from dash import dcc, html, Input, Output, dash_table
import pandas as pd

from utils import create_dataframe

def init_dashboard(app: Flask):

    @dash.callback(
        Output("graph", "figure"),
        Output("table-container", "children"),
        Input("urzl", "pathname"),
        Input("parameter-dropdown", "value") 
    )
    # Вызывается автоматически
    def update_graph_and_table(pathname, selected_parameter): 
        if pathname == "/dash/":
            weather_cities = session.get("weather_cities")
            if weather_cities is None:
                return dash.no_update, dash.no_update 
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

            figure = px.line(df, 
                             x="date", 
                             y=selected_parameter, 
                             color="city",
                             labels=labels) 
            
            def custom_sort_key(dates):
                date_order = {
                    "Сегодня": 0,
                    "Завтра": 1,
                    "Послезавтра": 2,
                    "Через 3 дня": 3,
                    "Через 4 дня": 4,
                }
                return [date_order.get(date, 5) for date in dates]

            pivot_table = pd.pivot_table(df, values='result', index='date', columns='city', aggfunc=lambda x: x) \
                .reset_index() \
                .rename(columns={'date': 'Дата'}) \
                .sort_values(by='Дата', key=custom_sort_key)
                
            print(pivot_table)

            table = dash_table.DataTable(
                id='result-table',
                columns=[{'name': col, 'id': col} for col in pivot_table.columns],
                data=pivot_table.reset_index().to_dict('records'),
                style_cell={'textAlign': 'center'}, 
            )

            return figure, table


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
            style={"width": "200px"}
        ),
        dcc.Graph(id="graph", style={"width": "100%"}),
        html.H3(id="table-title", style={"margin-left": "20px"}, children="Оценка погоды"),
        html.Div(id="table-container", style={"margin-top": "20px"}) 
    ], style={"height": "auto", "width": "100%", "position": "relative"})

    return dash_module.server