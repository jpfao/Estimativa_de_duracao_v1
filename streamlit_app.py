import os
import streamlit as st
import pandas as pd

# Função para carregar a planilha Excel
@st.cache_data
def load_data():
    file_path = 'NovaBasePRF_2021-2024_Codificados&Dinamica_06_09_outliers.xlsx'
    if not os.path.isfile(file_path):
        st.error(f"Arquivo não encontrado: {file_path}")
        return pd.DataFrame()  # Retorna um DataFrame vazio ou trata o erro apropriadamente
    try:
        return pd.read_excel(file_path)
    except KeyError as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame()

# Função para filtrar os valores das listas de acordo com a seleção
def filter_options(df, atividade, operacao, etapa):
    df_filtered = df[(df['ATIVIDADE'] == atividade) &
                     (df['OPERACAO'] == operacao) &
                     (df['ETAPA'] == etapa)]
    return df_filtered

# Carregar os dados da planilha Excel
df = load_data()

if not df.empty:
    # Listas de valores únicos para picklists
    atividades = df['ATIVIDADE'].unique()
    operacoes = df['OPERACAO'].unique()
    etapas = df['ETAPA'].unique()

    # Interatividade com o usuário - Picklists
    st.title('Formulário Interativo para Sequência Operacional')

    atividade_selecionada = st.selectbox('Selecione a ATIVIDADE:', atividades)
    operacao_selecionada = st.selectbox('Selecione a OPERACAO:', operacoes)
    etapa_selecionada = st.selectbox('Selecione a ETAPA:', etapas)

    # Inputs numéricos
    fase = st.number_input('FASE:', min_value=0, max_value=100)
    extensao = st.number_input('EXTENSÃO:', min_value=0.0)

    # Filtrando dados
    df_filtrado = filter_options(df, atividade_selecionada, operacao_selecionada, etapa_selecionada)

    st.write('Amostragem dos dados correspondentes:')
    st.write(df_filtrado)
else:
    st.warning("Nenhum dado disponível para exibição.")
