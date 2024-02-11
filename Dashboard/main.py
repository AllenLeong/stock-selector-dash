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

from StockSelection import StockSelection_page, StockSelection_callbacks


app = dash.Dash()

app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id = 'url',refresh=False),

    html.Div(id = 'page-content'),
])
@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
)
def display_page(pathname):
    if pathname =='/StockSelection':
        return StockSelection_page.page
    else:
        return html.Div('404')


from StockSelection.StockSelection_callbacks import *

if __name__ == '__main__':
    app.run_server(debug=True)
