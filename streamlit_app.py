import streamlit as st
import pandas as pd

# Função para filtrar as opções e remover outliers
@st.cache_data
def filter_options(df, atividade=None, operacao=None, etapa=None, fase=None, obz=None, broca=None, revestimento=None, tipo_sonda=None):
    df_filtered = df.copy()  # Trabalhar com cópia para evitar alterações no original
    
    if atividade:
        df_filtered = df_filtered[df_filtered['ATIVIDADE'] == atividade]
    if operacao:
        df_filtered = df_filtered[df_filtered['OPERACAO'] == operacao]
    if etapa:
        df_filtered = df_filtered[df_filtered['ETAPA'] == etapa]
    if fase:
        df_filtered = df_filtered[df_filtered['FASE'] == fase]
    if obz:
        df_filtered = df_filtered[df_filtered['Obz'] == obz]
    if broca and 'Todos' not in broca:
        df_filtered = df_filtered[df_filtered['Diâmetro Broca'].isin(broca)]
    if revestimento and 'Todos' not in revestimento:
        df_filtered = df_filtered[df_filtered['Diâmetro Revestimento'].isin(revestimento)]
    if tipo_sonda and 'Todos' not in tipo_sonda:
        df_filtered = df_filtered[df_filtered['Tipo_sonda'].isin(tipo_sonda)]
    
    return df_filtered

# Definir a largura da página como ampla
st.set_page_config(layout="wide")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Upload do arquivo Excel", type="xlsx")

if uploaded_file is not None:
    try:
        # Carregar o arquivo Excel
        df = pd.read_excel(uploaded_file)
        
        # Exibir o número de linhas e colunas do arquivo
        st.success(f"Arquivo carregado com sucesso! Tamanho: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        # Filtrar os dados entre Outliers e não-Outliers
        df_non_outliers = df[df['Outlier'] == False]
        df_outliers = df[df['Outlier'] == True]
        
        # Exibir tabela de amostras onde 'Outlier' é False
        st.write("Tabela - Amostras sem Outliers (Outlier = False):")
        st.dataframe(df_non_outliers.reset_index(drop=True))
        
        # Exibir tabela de amostras onde 'Outlier' é True
        st.write("Tabela - Amostras com Outliers (Outlier = True):")
        st.dataframe(df_outliers.reset_index(drop=True))

    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
else:
    st.warning("Nenhum arquivo foi carregado.")
