import dash
from dash import dcc, html


import pandas as pd
import numpy as np
from datetime import datetime
import os
from dash.dependencies import Input, Output
# sns.set_style('darkgrid')

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from StockSelection.StockSelection_api import *

page = html.Div([
    html.Div(["Header"]),
    dcc.Store(id = 'memory-output', data = read_latest_data_from_sql('../data').to_dict('records')),
    dcc.Store(id = 'memory-input'),
    html.Div([
        html.Div([
            "X",
            dcc.Dropdown(value = '市盈率',
                         id='x-columns')]),
        html.Div([
            "Y",
            dcc.Dropdown(value = '市净率',
                         id='y-columns')]),
        html.Div([
            "Size",
            dcc.Dropdown(value = '资本金',
                         id='size-columns')]),
        html.Div([
            "Color",
            dcc.Dropdown(value = '行业1',
                         id='color-columns')]),
        html.Div([
            "Hover Data",
            dcc.Dropdown(value = ['名字', '代码', '市盈率', '市净率', '资本金','换手率','行业1','行业2','行业3'],
                         id='hover-columns',
                         multi=True) ]),
        html.Button('update', id='update', n_clicks=0)
        ], style = dict(display='inline-block',verticalAlign = 'top', width = '20%')),

    html.Div(id = "StockSelector",
             style = dict(display='inline-block',verticalAlign = 'top',width = '80%',height = '800px')),
    html.Div(
             [html.Div(style = dict(height = '10px')),
              html.Div(id = "StockSelector-table")],
             style = dict(display='inline-block',verticalAlign = 'top' ,width = '100%'))
],style = dict(margin = {'margin-left':'8%', 'margin-right':'8%'}))
