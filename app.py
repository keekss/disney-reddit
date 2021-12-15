# Run with terminal command 'python3 app.py' from main project directory
# View at http://127.0.0.1:8050/ in your web browser

# Note: you may need to install additional libraries, e.g.:
## dash
## dash_bootstrap_components
## dash_daq

import pickle

f = open('graphs.txt', 'rb')
t = pickle.load(f)

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

disney_dark_blue_hex = '#10194A'

def graph_tab(name, number):
    return dcc.Tab(
        label = name,
        value = 'tab-' + str(number),
        className = 'graph-tab',
    ),

graph_file_names = [
    'ticker_plot_dis.png',
    'subreddit_post_scores.png',
    'linear_regressions.png'
]

app.layout = dbc.Container(fluid = True, children = [
    dbc.Container(fluid = True, children = [
        dbc.Row([
            dbc.Col(
                html.Section([
                    html.H1(t['a']),
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
                    ], style = dict(paddingTop = '10px')),
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
        children = [
            dcc.Tab(
                label = '1: Disney Stock Prices',
                value = 'tab-1',
                className = 'graph-tab',
            ),
            dcc.Tab(
                label = '2: Subreddit Post Scores',
                value = 'tab-2',
                className = 'graph-tab',

            ),
            dcc.Tab(
                label = '3A: Post Sentiment & Stock Price', 
                value = 'tab-3a',
                className = 'graph-tab',

            ),
            dcc.Tab(
                label = '3B: Comment Sentiment & Stock Price', 
                value = 'tab-3b',
                className = 'graph-tab',

            ),
        ]),
        html.Div(id = 'tabs-content')    
    ]),
])

graph_font = dict(
    family = 'Avenir',
    size = 24,
)

def graph_container(image_file_path):
    return dbc.Row(
        html.Img(
            src=app.get_asset_url(image_file_path),
            className = 'graph'
        ),
        className = 'graph-container'
    )

tab_1 = graph_container('ticker_plot_dis.png')

tab_2 = graph_container('subreddit_post_scores.png')

tab_3 = graph_container('linear_regressions.png')

tab_2 = dbc.Row(
    html.Img(
        src=app.get_asset_url('ticker_plot_dis.png'),
        className = 'graph'
    ),
    className = 'graph-container'
)

# Tab 2: Disneyland Ride Sentiments

from sklearn import preprocessing
import folium
import branca
import branca.colormap as cm

df_rides = pd.read_csv("./sampleData/disneyland_rides_lat_long_w_sentiment.csv")

#create a map object
map = folium.Map(location=[33.8121, -117.9190], zoom_start=18)

loc = 'Reddit sentiments shown by ride location, normalized between 0 and 1'
title_html = '''
             <h3 align="center" style="font-size:32px;font-family:Avenir"><b>{}</b></h3>
             '''.format(loc) 
map.get_root().html.add_child(folium.Element(title_html))

#create a feature group
fg = folium.FeatureGroup(name="Disneyland Attractions")

#read in the data
# data = pd.read_csv("disneyland_attractions.csv")
data = df_rides

colormap = cm.LinearColormap(
    colors=['red','green'],
    index=[0,1],vmin=0,vmax=1
)

#iterate through the dataframe and add each attraction to the feature group
for index, row in data.iterrows():
    fg.add_child(folium.Marker(
        location=[row["lat"], row["long"]], 
        popup="{} : {}".format(row["ride"].upper(), round(row['sentiment'], 2)), 
        icon=folium.Icon(color="black", icon_color=colormap(row['sentiment'])))
    )

map.add_child(colormap)
    
#add the feature group to the map
map.add_child(fg)

ride_map = map.save('ride_map.html')

ride_map_frame = html.Iframe(
    id = 'ride_map',
    srcDoc = open('ride_map.html', 'r').read(),
    width = '100%',
    height = '850'
)

tab_2 = dbc.Row([
    ride_map_frame
])

# Tab 3A
ps_df = pd.read_csv('sampleData/SMOOTHED_POST_SENTIMENT.csv')
ps = ps_df['Sentiment']
ps_dates = ps_df['Date']

pp_df = pd.read_csv('sampleData/POST_FINANCE.csv')
pp_raw = pp_df['Close_Price']
# Take natural log
pp = np.log(pp_raw)
pp_dates = pp_df['Date']

post_fig = make_subplots(specs=[[{"secondary_y": True}]])

post_fig.add_trace(
    go.Scatter(
        x = ps_dates,
        y = ps,
        name = 'Post Sentiment',
    ),
    secondary_y = False
)

post_fig.add_trace(
    go.Scatter(
        x = pp_dates,
        y = pp,
        name = 'Natural Log of Stock Price',
    ),
    secondary_y = True
)

post_fig.update_layout(
    title_text = 'Post Sentiment & Stock Price vs. Time',
    xaxis_title = 'Date',
    title_x = 0.5,
    height = 850,
    yaxis_showgrid = False,
    font = graph_font,
)

post_fig.update_yaxes(
    title_text='Sentiment (5 = Highest; 1 = Lowest)',
    tickformat = ".2f", showgrid = False,
    secondary_y=False,
)
post_fig.update_yaxes(title_text='Natural Log of Stock Price (USD)', tickformat = ".1f", showgrid = False, secondary_y=True,)


tab_3a = dbc.Row([
    dcc.Graph(figure = post_fig)
])

# Tab 3B
cs_df = pd.read_csv('sampleData/SMOOTHED_COMMENT_SENTIMENT.csv')
cs = cs_df['Sentiment']
cs_dates = cs_df['Date']

cp_df = pd.read_csv('sampleData/COMMENT_FINANCE.csv')
cp_raw = cp_df['Price']
# Take natural log
cp = np.log(cp_raw)
cp = np.round(cp, 2)
cp_dates = cp_df['Date']

comment_fig = make_subplots(specs=[[{"secondary_y": True}]])

comment_fig.add_trace(
    go.Scatter(
        x = cs_dates,
        y = cs,
        name = 'Comment Sentiment',
    ),
    secondary_y = False
)

comment_fig.add_trace(
    go.Scatter(
        x = cp_dates,
        y = cp,
        name = 'Natural Log of Stock Price',
    ),
    secondary_y = True
)

comment_fig.update_layout(
    title_text = 'Comment Sentiment & Stock Price vs. Time',
    xaxis_title = 'Date',
    title_x = 0.5,
    height = 850,
    yaxis_showgrid = False,
    font = graph_font,
)

comment_fig.update_yaxes(title_text='Sentiment (5 = Highest; 1 = Lowest)', tickformat = ".2f", showgrid = False, secondary_y=False)
comment_fig.update_yaxes(title_text='Natural Log of Stock Price (USD)', tickformat = ".1f", showgrid = False, secondary_y=True)


tab_3b = dbc.Row([
    dcc.Graph(figure = comment_fig)
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return tab_1
    elif tab == 'tab-2':
        return tab_2
    elif tab == 'tab-3a':
        return tab_3a
    elif tab == 'tab-3b':
        return tab_3b

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

@app.callback(
   Output('extra-info-text', 'children'),
   Input('extra-info-dropdown', 'value'))
def choose_extra_info(choice):
    if choice and extra_info_dict[choice]:
        return extra_info_dict[choice]
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
