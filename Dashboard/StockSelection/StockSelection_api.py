import os
import pandas as pd
import numpy as np
import sqlite3 as sql
import plotly.express as px
import logging

def read_latest_data(path):

    file_list = os.listdir(path)
    latest_file = sorted(file_list)[-1]

    df= pd.read_csv(os.path.join(path, latest_file), index_col = 0)

    return df



def read_latest_data_from_sql(path):


    # logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    # file_handler = logging.FileHandler("E:\Allen\Project\quantlib\log.txt")
    # file_handler.setargs = ()
    # logger.addHandler(file_handler)


    con = sql.connect('..\..\data\stock.db')

    cur = con.cursor()

    df= pd.read_sql('select * from valuation', con = con)

    #df = df.drop('录入时间',axis = 1)

    #logger.info(os.listdir())
    #logger.info(df.shape)

    return df


def selector_plot_v1(df_m, x, y, size, color, hover):
    # Scatter fig
    df_m[color] = df_m[color].fillna(0)

    df_m[size] = df_m[size].apply(lambda x: max(x,0))

    df_m[size] = df_m[size].fillna(0)

    fig = px.scatter(df_m, x=x, y=y, color=(color if df_m[color].dtype == 'object' else np.log(df_m[color])),
                     size=size, hover_name="名字",hover_data=hover,
                     size_max=80, log_x=(False if df_m[x].dtype == 'object' else True), log_y = (False if df_m[y].dtype == 'object' else True),
                     color_discrete_sequence=px.colors.qualitative.Dark24+px.colors.qualitative.Alphabet,
                    opacity = .5)

    fig.update_layout(xaxis = dict(title  = x),
                      yaxis = dict(title  = y),
                     template = 'plotly_white',
                      title = "A股选股器",
                      legend = dict(x = -0.2 ,title = dict(text = color)),
                      coloraxis = dict(colorbar = dict(x = -0.2 ,title = dict(text = color))),
                      height = 800,
                      dragmode='select',
                      )

    # Modifiy Hover Data
    # for data in fig.data:
    #     data['hovertemplate'] =("<b>%{hovertext}</b><br><br>"+
    #                                 "%{customdata[0]}<br>"+
    #                                 "%{customdata[1]}<br>"+
    #                                 "%{customdata[2]}<br>"+
    #                                 "市盈率：%{x:.2f}<br>"+
    #                                 "市净率：%{y:.2f}<br>"+
    #                                 "换手率：%{customdata[4]:.2f}<br>"+
    #                                 "市场份额(亿):%{customdata[3]:.0f}<extra></extra>"
    #                                 )
    #

    return fig
