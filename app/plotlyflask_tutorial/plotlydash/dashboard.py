"""Instantiate a Dash app."""
import numpy as np
import pandas as pd
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from .data import create_dataframe, pull_tickers, query_to_pandas
from .layout import html_layout
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

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
                    value=tickers[0],
                    multi=True)
            ]),
            html.H1(id='ticker-title'),
            html.Div([
                html.Div([dcc.Graph(id='line-graph')], style={'width': '66%', 'height': '400px', 'display': 'inline-block'}) ,
                html.Div([
                    dcc.Graph(id='heat-map1')
                    ], style={'width': '32%', 'height': '400px', 'display': 'inline-block', 'margin': 0, 'padding': 0})
            ], style={'display': 'inline-block', 'width': '98%'}),
            html.Div([
                html.Div([
                    dcc.Graph(id='ticker-dividend')
                    ], style={'width': '66%', 'height': '400px', 'display': 'inline-block', 'margin': 0, 'padding': 0}),
                html.Div([
                    dcc.Graph(id='heat-map')
                    ], style={'width': '32%', 'height': '400px', 'display': 'inline-block', 'margin': 0, 'padding': 0})
            ], style={'display': 'inline-block', 'width': '98%'}) ,
            
            html.Div([
                dash_table.DataTable(
                    id='ticker-descr',
                    style_data={'whiteSpace': 'normal', 'height': 'auto', 'textAlign': 'left'},
                    style_cell={'textAlign': 'left', 'padding': '5px'},
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    #style_cell_conditional=[
                    #    {
                    #        'if': {'column_id': c},
                    #        'textAlign': 'left'
                    #    } for c in ['Date', 'Region']
                    #],
                    columns=[
                    {'name': 'Ticker', 'id': 'ticker'},
                    {'name': 'Company', 'id': 'company_name'},
                    {'name': 'Sector', 'id': 'sector'},
                    {'name': 'City', 'id': 'city'},
                    {'name': 'State', 'id': 'state'},
                    {'name': 'Website', 'id': 'website'},
                    {'name': 'Business Summary', 'id': 'long_biz_summary'}
                ]
                )
            
            ])
            
            
    ],
        id='dash-container'
    )
    
    @dash_app.callback(
        dash.dependencies.Output('line-graph', 'figure'),
        [dash.dependencies.Input('ticker-filter', 'value')])
    def create_time_series(ticker_filter):
        
        df = create_dataframe(ticker_filter)

#        fig = px.line(df, x="year_month", y=["lowest_close", "avg_close", "highest_close"], title='Monthly Low and High Price')
        fig = px.line(df, x="year_month", y= "avg_close", color='ticker', title='Monthly Low and High Price')
        
        fig.update_layout(height=400)

        return  fig

    @dash_app.callback(
        #dash.dependencies.Output('table', 'data'), dash.dependencies.Output('table', 'columns')
        dash.dependencies.Output('heat-map1', 'figure'),
        dash.dependencies.Input("ticker-filter", "value"))
    def create_table(ticker_filter):

        metric_col = 'avg_close'

        df_sub = create_dataframe(ticker_filter)

        df_piv = df_sub.pivot(
            index='year_month',
            columns='ticker',
            values=metric_col
        )

        #df_piv.reset_index(inplace=True)

        cor_mat = df_piv.corr()

        cor_mat_np = cor_mat.to_numpy()

        col_labs = list(cor_mat.columns.values)     
        
        heat_data = go.Heatmap(
            z=cor_mat,
            x=col_labs,
            y=col_labs,
            zmin=-1,
            zmax=1,
            colorscale=[[0.0, "rgb(165,0,38)"],
                [0.1111111111111111, "rgb(215,48,39)"],
                [0.2222222222222222, "rgb(244,109,67)"],
                [0.3333333333333333, "rgb(253,174,97)"],
                [0.4444444444444444, "rgb(254,224,144)"],
                [0.5555555555555556, "rgb(224,243,248)"],
                [0.6666666666666666, "rgb(171,217,233)"],
                [0.7777777777777778, "rgb(116,173,209)"],
                [0.8888888888888888, "rgb(69,117,180)"],
                [1.0, "rgb(49,54,149)"]]
        )



        #fig = go.Figure(heat_data)

        fig = ff.create_annotated_heatmap(
            z=cor_mat_np,
            x=col_labs,
            y=col_labs,
            zmin=-1,
            zmax=1,
            showscale=True,
            colorscale=[[0.0, "rgb(165,0,38)"],
                [0.1111111111111111, "rgb(215,48,39)"],
                [0.2222222222222222, "rgb(244,109,67)"],
                [0.3333333333333333, "rgb(253,174,97)"],
                [0.4444444444444444, "rgb(254,224,144)"],
                [0.5555555555555556, "rgb(224,243,248)"],
                [0.6666666666666666, "rgb(171,217,233)"],
                [0.7777777777777778, "rgb(116,173,209)"],
                [0.8888888888888888, "rgb(69,117,180)"],
                [1.0, "rgb(49,54,149)"]]
        )

        return fig


    @dash_app.callback(
        #dash.dependencies.Output('table', 'data'), dash.dependencies.Output('table', 'columns')
        dash.dependencies.Output('heat-map', 'figure'),
        dash.dependencies.Input("ticker-filter", "value"))
    def create_table(ticker_filter):

        metric_col = 'avg_close'

        df_sub = create_dataframe(ticker_filter)

        df_piv = df_sub.pivot(
            index='year_month',
            columns='ticker',
            values=metric_col
        )

        #df_piv.reset_index(inplace=True)

        cor_mat = df_piv.corr()
        cor_mat_np = cor_mat.to_numpy()
        col_labs = list(cor_mat.columns.values)     
        
        heat_data = go.Heatmap(
            z=cor_mat,
            x=col_labs,
            y=col_labs,
            zmin=-1,
            zmax=1,
            colorscale=[[0.0, "rgb(165,0,38)"],
                [0.1111111111111111, "rgb(215,48,39)"],
                [0.2222222222222222, "rgb(244,109,67)"],
                [0.3333333333333333, "rgb(253,174,97)"],
                [0.4444444444444444, "rgb(254,224,144)"],
                [0.5555555555555556, "rgb(224,243,248)"],
                [0.6666666666666666, "rgb(171,217,233)"],
                [0.7777777777777778, "rgb(116,173,209)"],
                [0.8888888888888888, "rgb(69,117,180)"],
                [1.0, "rgb(49,54,149)"]]
        )

        fig = ff.create_annotated_heatmap(
            z=cor_mat_np,
            x=col_labs,
            y=col_labs,
            zmin=-1,
            zmax=1,
            showscale=True,
            colorscale=[[0.0, "rgb(165,0,38)"],
                [0.1111111111111111, "rgb(215,48,39)"],
                [0.2222222222222222, "rgb(244,109,67)"],
                [0.3333333333333333, "rgb(253,174,97)"],
                [0.4444444444444444, "rgb(254,224,144)"],
                [0.5555555555555556, "rgb(224,243,248)"],
                [0.6666666666666666, "rgb(171,217,233)"],
                [0.7777777777777778, "rgb(116,173,209)"],
                [0.8888888888888888, "rgb(69,117,180)"],
                [1.0, "rgb(49,54,149)"]]
        )

        return fig

    @dash_app.callback(
        dash.dependencies.Output('ticker-title', 'children'),
        dash.dependencies.Input('ticker-filter', 'value'))
    def create_title(ticker_filter):

        ticker_list_clean = [ticker.upper() for ticker in ticker_filter]

        if len(ticker_list_clean) > 1:
            ticker_list_str = "', '".join(ticker_list_clean)
        else:
            ticker_list_str = ticker_list_clean[0]
        
        ticker_list_str = f"('{ticker_list_str}')"

        query = f"SELECT company_name FROM lkp.ticker WHERE ticker in {ticker_list_str}"

        temp_df = query_to_pandas(query=query)

        company_names = temp_df.company_name.tolist()

        company_names_str = ', '.join(company_names)

        title = f'Showing data for: {company_names_str}'
        
        return title

    @dash_app.callback(
        dash.dependencies.Output('ticker-descr', 'data'),
        dash.dependencies.Input('ticker-filter', 'value'))
    def create_ticker_info_table(ticker_filter):

        ticker_list_clean = [ticker.upper() for ticker in ticker_filter]

        if len(ticker_list_clean) > 1:
            ticker_list_str = "', '".join(ticker_list_clean)
        else:
            ticker_list_str = ticker_list_clean[0]
        
        ticker_list_str = f"('{ticker_list_str}')"

        query = (
            "select "
                "ti.ticker, "
                "t.company_name, "
                "ti.sector, "
                "ti.city, "
                "ti.state, "
                "ti.country, "
                "ti.website, "
                "ti.long_biz_summary "
            "from lkp.ticker_info as ti "
            "left join lkp.ticker as t "
            "on ti.ticker = t.ticker "
            f"WHERE t.ticker in {ticker_list_str}"
        )
        
        temp_df = query_to_pandas(query=query)

        temp_dict = temp_df.to_dict(orient='records')
       
        return temp_dict


    @dash_app.callback(
        dash.dependencies.Output('ticker-dividend', 'figure'),
        dash.dependencies.Input('ticker-filter', 'value'))
    def create_div_table(ticker_filter):

        ticker_list_clean = [ticker.upper() for ticker in ticker_filter]

        if len(ticker_list_clean) > 1:
            ticker_list_str = "', '".join(ticker_list_clean)
        else:
            ticker_list_str = ticker_list_clean[0]
        
        ticker_list_str = f"('{ticker_list_str}')"

        query = (
            "select "
	            "a.ticker as ticker_div, "
                "a.market_date, "
                "a.dividends, "
                "ms.* "
            "from raw.actions as a "
            "left join raw.monthly_summary as ms "
            "on "
                "a.ticker = ms.ticker "
                "and substring(cast(a.market_date as varchar), 1, 7) = ms.year_month "
            "WHERE "
                f"a.ticker in {ticker_list_str} "
                "and a.dividends <> 0 "
        )
        
        temp_df = query_to_pandas(query=query) 

        fig = px.scatter(temp_df, x="market_date", y= "dividends", color='ticker_div', title='Dividends Paid')
    
        fig.update_layout(height=400)

        return fig


    return dash_app.server




