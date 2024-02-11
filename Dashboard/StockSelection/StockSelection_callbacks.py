import os

#os.chdir("../")
import dash
from dash import dcc, html
from main import app
from dash.dependencies import Input, Output,State
from StockSelection.StockSelection_api import *
import logging
#import dash_table
from dash.dash_table.Format import Format, Scheme, Sign,Group, Prefix


@app.callback(
    Output('x-columns','options'),
    Output('y-columns','options'),
    Output('size-columns','options'),
    Output('color-columns','options'),
    Output('hover-columns','options'),
    Input('memory-output', 'data')
)
def update_dropdown_table_columns(data):

    return [pd.DataFrame(data).columns.tolist() for i in range(5)]


@app.callback(
    Output('memory-input', 'data'),
    Output('StockSelector', 'children'),
    Output('update', 'n_clicks'),
    Input('update', 'n_clicks'),
    State('memory-output','data'),
    State('x-columns','value'),
    State('y-columns','value'),
    State('size-columns','value'),
    State('color-columns','value'),
    State('hover-columns','value'),
)
def update_middle_table_selector(n_clicks, data,x,y,size,color,hover):
    if n_clicks <=1:
        df_m = pd.DataFrame(data)
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler("E:\Allen\Project\quantlib\log.txt")
        file_handler.setargs = ()
        logger.addHandler(file_handler)


        logger.info(f' clicks {n_clicks}')

        columns = np.unique(np.array(['名字','代码',x,y,color,size]+hover))

        df_m = df_m[columns.tolist()]

        fig = selector_plot_v1(df_m, x, y, size, color, hover)
        logger.info(df_m.columns)
        return  df_m.to_dict('records'), dcc.Graph(id = "StockSelector_graph",figure = fig) , 0

@app.callback(
    Output('StockSelector-table','children'),
    Input('StockSelector_graph','selectedData'),
    State('memory-input', 'data')
)
def update_selector_table(value,data):
    df = pd.DataFrame(data)

    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    # file_handler = logging.FileHandler("E:\Allen\Project\quantlib\log.txt")
    # file_handler.setargs = ()
    # logger.addHandler(file_handler)

    if value:
        value = [i['hovertext'] for i in value['points']]
        df = df[df['名字'].isin(value)]
    datatable = dash.dash_table.DataTable(
        data= df.to_dict('records'),

        columns = [{"name": i, "id": i} if df[i].dtype =='object' \
                    else {"name": i, "id": i, "type": "numeric",  "format":Format(precision=2, scheme=Scheme.decimal).group(True)}\
                    for i in df.columns],
        sort_action="native",
        sort_mode="single",
        row_selectable='multi',
        selected_rows=[],

        filter_action='custom',
        filter_query='',
        fixed_rows={'headers': True},
        style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold',
        'fontFamily':'微软雅黑'
        },
        style_table={
            'overflowX': 'hidden',
            'textOverflow': 'ellipsis',
            'width': '100%',
            'height':"1000px",
            'overflowy': 'auto','border':'none',
            'fontFamily':'微软雅黑',
            #'minWidth': '100%'
            },
        style_cell={#'textAlign': 'left',
                    'width': '100px'},

        style_data_conditional=[
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)',
            },
            {
            'if': {'column_type': 'text'},
            'textAlign': 'left'
            },

        ],


        style_as_list_view=True,
    )



    return datatable
