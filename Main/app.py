# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import Funcoes
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = Dash(__name__)

# assume you have a "long-form" data frameMy Project 83723
# see https://plotly.com/python/px-arguments/ for more options
df_info = pd.read_csv(fr"C:\Users\quagl\OneDrive\Documentos\Python_dash/Dados_dash/Informações_reabnhos_municipios.csv")
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
            ], md=3),
            dbc.Col(children=[
                dcc.Dropdown(
                    id='menu-suspenso-mun',
                    value='',
                    className='my-dropdown'
                )
            ], md=3),
            dbc.Col(children=[
                dcc.Dropdown(
                    id='menu-suspenso-ano',
                    value='',
                    className='my-dropdown'
                )
            ], md=3),
            dbc.Col(children=[
                html.Button('Clique aqui', id='botao', className='my-button')

            ])

            
        ],className='d-flex justify-content-between')
    ], className='my-custom-div'),

        dbc.Row(id = 'primeira-linha', children=[
            dbc.Col(id = 'coluna-kpi-ovino', children=[
                html.Div(id = 'kpi-ovino', children = [


                ], className='kpi-card')
                
            ], md=3),
        

    ]),

    html.Div(id='segunda-linha', children= [
       
    ])
])



@app.callback(
    Output('menu-suspenso-mun', 'options'),
    Input('menu-suspenso-UF', 'value')
)
def atualizar_opcoes_cidade(uf_selecionada):
    uf_selecionado = uf_selecionada
    opcoes_cidade = [{'label': cidade, 'value': cidade} for cidade in df_info[df_info['SIGLA'] == uf_selecionada]['NM_MUN'].unique()]
    return opcoes_cidade

@app.callback(
    Output('menu-suspenso-ano', 'options'),
    Input('menu-suspenso-mun', 'value')
)
def atualizar_opcoes_cidade(mun_selecionado):
    mun_selecionado = mun_selecionado
    opcoes_ano = [{'label': ano, 'value': ano} for ano in df_info[df_info['NM_MUN'] == mun_selecionado]['ano'].unique()]
    return opcoes_ano

@app.callback(
Output('segunda-linha', 'children'),
    State('menu-suspenso-UF', 'value'),
    State('menu-suspenso-mun', 'value'),
    State('menu-suspenso-ano', 'value'),
    Input('botao', 'n_clicks')
)
def atualizar_segunda_linha( uf_selecionada, mun_selecionado,ano_selecionado, n_clicks):
    if n_clicks:
        fig, info_filtrada = grafico_pizza(mun_selecionado,uf_selecionada, ano_selecionado)
        div_interna1 = html.Div('Conteúdo da div interna 1')
        div_interna2 = html.Div('Conteúdo da div interna 2')
        div_interna3 = html.Div('Conteúdo da div interna 3')
        return dcc.Graph(id='grafico_pizza', figure = fig)
    else:
        return []


@app.callback(
    Output('kpi-ovino', 'children'),
    State('menu-suspenso-UF', 'value'),
    State('menu-suspenso-mun', 'value'),
    State('menu-suspenso-ano', 'value'),
    Input('botao', 'n_clicks')
)
def atualizar_primeira_linha( uf_selecionada, mun_selecionado,ano_selecionado ,n_clicks):
    if n_clicks:

        numero_ovinos = df_info[(df_info['NM_MUN'] == 'Ariquemes') & (df_info['ano'] == ano_selecionado)]['Ovino'].values[0]
        media_ovinos = df_info[df_info['ano'] == ano_selecionado]['Ovino'].sum() / len(df_info[df_info['ano'] == ano_selecionado]['Ovino'])
        kpi_ovino = make_kpi_pct('N.º de Ovinos', 'variação em relação a média nacional',numero_ovinos,media_ovinos, 'Ovino'  )
       
        return dcc.Graph(id='kpi-ovino', figure = kpi_ovino)
    else:
        return []




def grafico_pizza(municipio, uf, ano):
    print(municipio, uf, ano)
    print(df_info[['NM_MUN','SIGLA','ano']].dtypes)
    print(df_info[['NM_MUN','SIGLA','ano']])
    filtro = ((df_info['NM_MUN'] == municipio) &
              (df_info['SIGLA'] == uf) &
              (df_info['ano'] == ano))
    sub_df = df_info[filtro]
    
    sub_df = sub_df.set_index('Cod_uf')
    sub_df = sub_df[['Ovino',
       'Bovino', 'Equino', 'Caprino']]
    

    # Soma de todos os tipos de rebanho
    total = sub_df[['Ovino', 'Bovino', 'Equino', 'Caprino'
                    ]].sum().sum()
    print(total)

   
   
    
    # Criação do gráfico de pizza
    fig = px.pie(sub_df,names = list(sub_df.columns), values = sub_df.values[0], 
                 title=f'Total de rebanhos em {municipio}/{uf} em {ano}',
                 color_discrete_sequence=px.colors.qualitative.Safe,
                 labels={'names': 'Tipo de rebanho', 'values': 'Porcentagem'},
                 hole=0.3, width=600, height=400)
    
    fig.update_layout(title_font_size=20, legend_font_size=16)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig, df_info[filtro]


def make_kpi_pct(titulo, subtitulo, valor,referencia, coluna):
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = valor,
        title = {"text": f"{titulo}<br><span style='font-size:0.8em;color:gray'>{subtitulo}</span><br><span style='font-size:0.8em;color:gray'>Subsubtitle</span>"},
        delta = {'reference': referencia, 'relative': True},
        domain = {'x': [0.6, 1], 'y': [0, 1]}))

    return fig









    



import webbrowser
webbrowser.open_new('http://localhost:8050/')

if __name__ == '__main__':
    app.run_server(debug=True)