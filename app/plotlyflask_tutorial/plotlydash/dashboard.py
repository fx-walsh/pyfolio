"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe, pull_tickers
from .layout import html_layout
import plotly.express as px

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
            'https://fonts.googleapis.com/css?family=Lato'
        ]
    )

    # Load DataFrame
    tickers = pull_tickers()

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div([
            html.Div([
                dcc.Dropdown(
                    id='ticker-filter',
                    options=[{'label': i, 'value': i} for i in tickers],
                    value='Tickers')
            ]),
            html.Div([dcc.Graph(id='line-graph')]),
            html.Div([dash_table.DataTable(
                        id='table',
                        sort_action="native",
                        sort_mode='native',
                        page_size=300)
        ])
    ],
        id='dash-container'
    )
    
    @dash_app.callback(
        dash.dependencies.Output('line-graph', 'figure'),
        [dash.dependencies.Input('ticker-filter', 'value')])
    def create_time_series(ticker_filter):
        
        df = create_dataframe(ticker_filter)

        fig = px.line(df, x="market_date", y="open_price", title='Open Price Over Time')
        
        return  fig


    @dash_app.callback(
        [dash.dependencies.Output('table', 'data'), dash.dependencies.Output('table', 'columns')],
        [dash.dependencies.Input("ticker-filter", "value")])
    def create_table(ticker_filter):

        df_sub = create_dataframe(ticker_filter)

        return df_sub.to_dict('records'), [{"name": i, "id": i} for i in df_sub.columns]
    
    

    return dash_app.server




