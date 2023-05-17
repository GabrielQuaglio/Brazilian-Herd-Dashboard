def atualizar_opcoes_cidade(valor_selecionado, df_info):
    # Obter as cidades correspondentes à UF selecionada
    cidades = df_info[df_info['SIGLA'] == valor_selecionado]['CIDADE'].unique()
    opcoes_cidade = [{'label': valor, 'value': valor} for valor in cidades]
    return opcoes_cidade