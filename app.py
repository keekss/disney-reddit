# Run with terminal command 'python3 app.py' from main project directory
# View at http://127.0.0.1:8050/ in your web browser

# See project_writeup.ipynb for full details

# Note: you may need to install additional libraries, e.g.:
## dash
## dash_bootstrap_components
## dash_daq

import pandas as pd
from pandas.core.base import SelectionMixin

import numpy as np

# Import Dash and extra Plotly modules
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq
import dash_table as dt
from dash_table.Format import Format, Scheme, Group
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
from plotly.express import data

import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

import pickle

# Load fig object saved from project_writeup.ipynb
def load_fig(name):
    file_path = 'graphs/' + name + '.txt'
    f = open(file_path, 'rb')
    graph = pickle.load(f)
    f.close()
    return graph

stock_prices_fig = load_fig('stock_prices')
post_scores_fig = load_fig('post_scores')
comments_fig = load_fig('comments')
post_sentiment_fig = load_fig('post_sentiment')
comment_sentiment_fig = load_fig('comment_sentiment')

# Package loaded figs
def fig_graph_container(fig):
    return dbc.Row(
        dcc.Graph(
            figure = fig,
            className = 'graph'
        ), className = 'graph-container'
    )

# Package images from assets folder
def image_graph_container(image):
    return dbc.Row(
        html.Img(
            src=app.get_asset_url(image),
            className = 'graph'
        ),
        className = 'graph-container'
    )

ride_map_container = dbc.Row(
    html.Iframe(
        id = 'ride_map',
        srcDoc = open('ride_map.html', 'r').read(),
        width = '100%',
        height = '850',
        className = 'graph',
    ), className = 'graph-container',
)

tab_labels = [
    '1: Map of DisneyLand Ride Sentiment',
    '2: Character Mentions',
    '3: Stock Prices vs. Time',
    '4: Post Scores vs. Time',
    '5: Number of Comments vs. Time',
    '6a: Stock Prices vs. Post Scores',
    '6b: Stock Prices vs. Number of Comments',
    '7a: Stock Price vs. Post Sentiment',
    '7b: Stock Price vs. Comment Sentiment',
]

# Access tab content via dictionary with callback
tab_content = dict(
    ride_map = ride_map_container,
    character_mentions = image_graph_container('characters_chart.png'),
    stock_prices = fig_graph_container(stock_prices_fig),
    post_scores = fig_graph_container(post_scores_fig),
    comments = fig_graph_container(comments_fig),
    stock_post_reg = image_graph_container('stock_post_reg.png'),
    stock_comment_reg = image_graph_container('stock_comment_reg.png'),
    post_sentiment = fig_graph_container(post_sentiment_fig),
    comment_sentiment = fig_graph_container(comment_sentiment_fig),
)

# Package each tab in a dcc.Tab
tab_containers = []
for label, value in zip(tab_labels, list(tab_content.keys())):
    tab_containers.append(
        dcc.Tab(
            label = label,
            value = value,
            className = 'graph-tab'
        )
    )

disney_dark_blue_hex = '#10194A'

extra_info_dict = dict(
    writeup = [
        'All data processing and methodologies are detailed in a Jupyter Notebook',
        html.Br(),
        'Visualizations are included in-line.',
        html.Br(),
        dcc.Link(
            'View the Project Writeup',
            href='https://github.com/keekss/disney-reddit/blob/master/438%20Final%20Report.ipynb',
            style = dict(color = disney_dark_blue_hex),
        )
    ],
    pmaw = [
        'PMAW (Pushshift Multithread API Wrapper) uses the Pushshift API (see \"Pushshift\" info) to multithread ineractions of Pushshift endpoints to improve performance.  ',
        dcc.Link(
            'View the GitHub Repository',
            href='https://github.com/mattpodolak/pmaw',
            style = dict(color = disney_dark_blue_hex),
        )
    ],
    pushshift = [
        'Pushshift allows users to search Reddit.com posts and comments based on various criteria, such as keywords, creation date, and score.  ',
        html.Br(),
        dcc.Link(
            'View the GitHub Repository',
            href='https://github.com/pushshift/api',
            style = dict(color = disney_dark_blue_hex),
        )
    ],
    yfinance = [
        'yfinance allows users to access market data from Yahoo Finance, one of the leading financial media services.  Our group used yfinance to pull historical stock price data.  ',
        dcc.Link(
            'View the PyPI Project Page',
            href='https://pypi.org/project/yfinance/',
            style = dict(color = disney_dark_blue_hex),
        )
    ],
)

app.layout = dbc.Container(fluid = True, children = [
    dbc.Container(fluid = True, children = [
        dbc.Row([
            dbc.Col(
                html.Section([
                    html.H1(
                        'Disney Subreddit Visualizations',
                        id = 'main-title',
                    ),
                    html.H5(
                        'ICS 438 - Final Project, Fall 2021 - Andy Yu, Clark Whitehead, Frederick Straub, Kiko Whiteley',
                        style = dict(paddingTop = '0px')
                    ),
                    dbc.Row([
                        dbc.Col(html.H5('Visit our:'), width = 3),
                        dbc.Col(html.H5(
                            dcc.Link(
                                'GitHub Repository',
                                href='https://github.com/keekss/disney-reddit',
                                style = dict(color = disney_dark_blue_hex),
                                target = "_blank"
                            ), style = dict(color = disney_dark_blue_hex),
                        ), width = 4),
                        dbc.Col(html.H5(
                            dcc.Link(
                                'Project Writeup',
                                href='https://github.com/keekss/disney-reddit/blob/master/438%20Final%20Report.ipynb',
                                style = dict(color = disney_dark_blue_hex),
                                target = "_blank"
                            ), style = dict(color = disney_dark_blue_hex),
                        ), width = 5),
                    ], style = dict(paddingTop = '4px')),
                    html.H4(
                       
                    ),                    
                ]),
                width = 6
            ),
            dbc.Col(
                html.Section([
                    dbc.Row([
                        dbc.Col([
                            html.H4('Select Info:', style = dict(paddingTop = '8px')),
                            html.H4('Process & Libraries'),
                            html.Div([
                                dcc.Dropdown(
                                    id = 'extra-info-dropdown',
                                    options =[
                                        dict(label = 'Project Writeup', value = 'writeup'),
                                        dict(label = 'PMAW', value = 'pmaw'),
                                        dict(label = 'Pushshift', value = 'pushshift'),
                                        dict(label = 'yfinance', value = 'yfinance'),
                                    ],
                                    searchable = True,
                                ),
                            ])], width = 4),
                        dbc.Col(
                            html.H4(id = 'extra-info-text'), 
                            width = 8,
                            style = dict(margin = 'auto')
                        ),
                    ]),
                ])
            )
        ])
    ]),
    dbc.Container(fluid = True, children = [
        dcc.Tabs(
            id = 'tabs',
            colors = dict(
                primary = 'black',
                background = '#393F8F',
                border = 'whitesmoke'
            ),
            children = tab_containers
        ),
        html.Div(id = 'tabs-content', style = dict(float = 'left'))
    ]),
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return tab_content['ride_map']
    else:
        return tab_content[str(tab)]

@app.callback(
   Output('extra-info-text', 'children'),
   Input('extra-info-dropdown', 'value'))
def choose_extra_info(choice):
    if choice and extra_info_dict[choice]:
        return extra_info_dict[choice]
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
