import dash
import dash_core_components as dcc
import dash_html_components as htlm
import investpy

import pandas as pd


from datetime import datetime, date
import pandas as pd
import numpy as np
from dash import Input, Output
import plotly.graph_objects as go




import yfinance as yf

# since = '20190101'

# since_ = pd.to_datetime(since,format = '%Y%m%d')



#countries=investpy.etfs.get_etf_countries()

df_1=investpy.etfs.get_etfs(country='united states')

df_1.drop_duplicates('name', inplace = True)
df_1.drop_duplicates('full_name', inplace = True)
df_1.reset_index(inplace = True, drop = True)

listado_etf = []
for etf in df_1['name'].unique():
    temp_dict = {'label':etf + "/" + df_1[df_1['name']==etf]['symbol'].values[0] ,'value':df_1[df_1['name']==etf]['symbol'].values[0]}
    listado_etf.append(temp_dict)



app = dash.Dash()
server = app.server 

app.layout = htlm.Div( [
        dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(1995, 8, 5),
                # max_date_allowed=date(2017, 9, 19),
                #initial_visible_month=date(2017, 8, 5),
                start_date =date(2020, 1, 1)  ,
                end_date=date(2024, 1, 1) , style ={'width':'99%',
                'display':'inline-block'}
            ),

                htlm.Div([  
                dcc.Dropdown(id = "selector1", 
                options =listado_etf,
                value = ['SPY','EWZ'], multi=True)] , style ={'width':'48%',
                'display':'inline-block'} ),

                htlm.Div([  
                dcc.Dropdown(id = "selector2", 
                options =[{'label':i,'value':i} for i in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']],
                value = 'Close')] , style ={'width':'48%',
                'display':'inline-block'}),

                dcc.Graph(id ='grafico'),

                # htlm.Div(id = "Mi-salida")
                
                ], style={'padding': 14}
        )

# @app.callback( Output("Mi-salida", "children"),
#               [Input('my-date-picker-range', 'start_date'),
#                Input('my-date-picker-range', 'end_date')])
# def devuelve_mi_salida(start, end):
#     return 'has insertado : "{}" "{}"'.format(type(start) , end)

@app.callback(Output('grafico','figure'),
              [ Input('selector1','value'),
               Input('selector2', 'value'),
               Input('my-date-picker-range','start_date'),
               Input('my-date-picker-range','end_date')])
def grafico(valor_selector1,valor_selector2, since, end):

    since_ = pd.to_datetime(since, format = "%Y-%m-%d")
    end_ = pd.to_datetime(end, format = "%Y-%m-%d")
    datos= yf.download(valor_selector1, start=since_, end = end_, interval='1d')


    if len(valor_selector1)>1:

        datos = datos[valor_selector2] 

    elif len(valor_selector1) ==1:
        
        datos = pd.DataFrame(datos[valor_selector2]) 

        datos = datos.rename(columns = {valor_selector2:valor_selector1[0]})

    # print(datos.tail(10))
    datos = datos.fillna(method = 'ffill')
    
    datos = datos.pct_change() + 1

    datos = datos.cumprod()

    datos.dropna(inplace = True)


    layers =[]

    for etf in valor_selector1:

        temp = go.Scatter(x = datos.index,
                           y = datos[etf],
                           mode = 'lines',
                           name=etf)

        layers.append(temp)

    return {
        'data':layers,

        'layout': go.Layout(title = 'ETF',
                            xaxis = {'title':'Fecha'})


    }


if __name__=='__main__':
    app.run_server()
