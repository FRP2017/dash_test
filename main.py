import dash
import dash_core_components as dcc
import dash_html_components as htlm
import investpy

import pandas as pd


from datetime import datetime
import pandas as pd
import numpy as np
from dash import Input, Output
import plotly.graph_objects as go




import yfinance as yf

since = '20190101'

since_ = pd.to_datetime(since,format = '%Y%m%d')



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
                htlm.Div([  
                dcc.Dropdown(id = "selector1", 
                options =listado_etf,
                value = 'SPY')] , style ={'width':'48%',
                'display':'inline-block'} ),

                htlm.Div([  
                dcc.Dropdown(id = "selector2", 
                options =[{'label':i,'value':i} for i in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']],
                value = 'Close')] , style ={'width':'48%',
                'display':'inline-block'}),

                dcc.Graph(id ='grafico')], style={'padding': 14}
        )

@app.callback(Output('grafico','figure'),
              [ Input('selector1','value'),
               Input('selector2', 'value')])
def grafico(valor_selector1,valor_selector2):

    datos= yf.download(valor_selector1, start=since_, interval='1d')

    datos = datos[[valor_selector2]] 

    datos.reset_index(inplace = True)

    return {
        'data':[go.Scatter(x = datos['Date'],
                           y = datos[valor_selector2],
                           mode = 'lines')],

        'layout': go.Layout(title = valor_selector1,
                            xaxis = {'title':'Fecha'})


    }


if __name__=='__main__':
    app.run_server()
