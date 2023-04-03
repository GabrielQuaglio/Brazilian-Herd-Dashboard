# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import Funcoes
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__)

# assume you have a "long-form" data frameMy Project 83723
# see https://plotly.com/python/px-arguments/ for more options
df_info = pd.read_csv(fr"C:\Users\quagl\OneDrive\Documentos\Python_dash\Informações_reabnhos_municipios.csv")
uf_selecionado = ''


#df = pd.read_csv('Dados_bovinos_completo')



app.layout = html.Div(children=[
    html.H1('Dashboard analitico dos rebanhos brasileiros', className="app-header"),
    html.Div(children=[
        dbc.Row(children=[
            dbc.Col(children=[
                dcc.Dropdown(
                    
                    id='menu-suspenso-UF',
                    options=[{'label': valor, 'value': valor} for valor in df_info['SIGLA'].unique()],
                    value=df_info['SIGLA'][0],
                    className='my-dropdown'
                )
            ], md=4),
            dbc.Col(children=[
                dcc.Dropdown(
                    id='menu-suspenso-mun',
                    value='',
                    className='my-dropdown'
                )
            ], md=4),
            dbc.Col(children=[
                html.Button('Clique aqui', id='botao', className='my-button')

            ])
            
        ],className='d-flex justify-content-between')
    ], className='my-custom-div')
], className='app-header')


@app.callback(
    Output('menu-suspenso-mun', 'options'),
    Input('menu-suspenso-UF', 'value')
)
def atualizar_opcoes_cidade(uf_selecionada):
    uf_selecionado = uf_selecionada
    opcoes_cidade = [{'label': cidade, 'value': cidade} for cidade in df_info[df_info['SIGLA'] == uf_selecionada]['NM_MUN'].unique()]
    return opcoes_cidade






    



import webbrowser
webbrowser.open_new('http://localhost:8050/')

if __name__ == '__main__':
    app.run_server(debug=True)