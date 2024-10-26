import streamlit as st
import pandas as pd

# Função para filtrar as opções e remover outliers
@st.cache_data
def filter_options(df, atividade=None, operacao=None, etapa=None, fase=None, obz=None, broca=None, revestimento=None, tipo_sonda=None):
    df_filtered = df.copy()  # Trabalhar com cópia para evitar alterações no original
    
    if atividade and atividade != "TODOS":
        df_filtered = df_filtered[df_filtered['ATIVIDADE'] == atividade]
    if operacao and operacao != "TODOS":
        df_filtered = df_filtered[df_filtered['OPERACAO'] == operacao]
    if etapa and etapa != "TODOS":
        df_filtered = df_filtered[df_filtered['ETAPA'] == etapa]
    if fase and fase != "TODOS":
        df_filtered = df_filtered[df_filtered['FASE'] == fase]
    if obz and obz != "TODOS":
        df_filtered = df_filtered[df_filtered['Obz'] == obz]
    if broca and 'TODOS' not in broca:
        df_filtered = df_filtered[df_filtered['Diâmetro Broca'].isin(broca)]
    if revestimento and 'TODOS' not in revestimento:
        df_filtered = df_filtered[df_filtered['Diâmetro Revestimento'].isin(revestimento)]
    if tipo_sonda and 'TODOS' not in tipo_sonda:
        df_filtered = df_filtered[df_filtered['Tipo_sonda'].isin(tipo_sonda)]
    
    return df_filtered

# Função para obter as opções de filtro em ordem alfabética, baseadas nos dados filtrados
def get_filter_options(df, coluna):
    return sorted(df[coluna].dropna().unique().tolist())  # Ordenar em ordem alfabética
# Definir a largura da página como ampla
st.set_page_config(layout="wide")

# Upload do arquivo principal
uploaded_file = st.file_uploader("Upload do arquivo planilhão sumarizado", type="xlsx")

# Upload do arquivo de referência
uploaded_reference = st.file_uploader("Upload do arquivo de referência para a SEQOP", type="xlsx")

# Dicionário para armazenar listas de linhas manuais entre as linhas automáticas
if 'manual_rows' not in st.session_state:
    st.session_state.manual_rows = {}

def add_manual_row(below_index):
    """Função para adicionar uma nova linha manual abaixo de uma linha automática."""
    if below_index not in st.session_state.manual_rows:
        st.session_state.manual_rows[below_index] = []
    st.session_state.manual_rows[below_index].append(len(st.session_state.manual_rows[below_index]) + 1)

if uploaded_file is not None:
    try:
        # Carregar o arquivo principal
        df = pd.read_excel(uploaded_file)
        
        # Exibir o número de linhas e colunas do arquivo principal
        st.success(f"Arquivo principal carregado com sucesso! Tamanho: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        st.title('Formulário Interativo para Sequência Operacional')

        # Carregar e exibir linhas do arquivo de referência
        if uploaded_reference is not None:
            df_reference = pd.read_excel(uploaded_reference)
            st.success("Arquivo de referência carregado com sucesso!")

            # Obter valores de filtro possíveis para cada campo com base no DataFrame atual
            atividade_options = ["Todos"] + get_filter_options(df, 'ATIVIDADE')
            operacao_options = ["Todos"] + get_filter_options(df, 'OPERACAO')
            etapa_options = ["Todos"] + get_filter_options(df, 'ETAPA')
            fase_options = ["Todos"] + get_filter_options(df, 'FASE')
            obz_options = ["Todos"] + get_filter_options(df, 'Obz')
            broca_options = ["Todos"] + get_filter_options(df, 'Diâmetro Broca')
            revestimento_options = ["Todos"] + get_filter_options(df, 'Diâmetro Revestimento')
            tipo_sonda_options = ["Todos"] + get_filter_options(df, 'Tipo_sonda')
            for i, row in df_reference.iterrows():
                st.markdown(f"<div style='background-color: #008542; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha {i + 1}</div>", unsafe_allow_html=True)

                # Obter valores dos filtros da linha do arquivo de referência
                atividade = st.selectbox(f'ATIVIDADE (Linha {i + 1}):', atividade_options)
                operacao = st.selectbox(f'OPERAÇÃO (Linha {i + 1}):', operacao_options)
                etapa = st.selectbox(f'ETAPA (Linha {i + 1}):', etapa_options)
                fase = st.selectbox(f'FASE (Linha {i + 1}):', fase_options)
                obz = st.selectbox(f'OBZ (Linha {i + 1}):', obz_options)
                broca = st.multiselect(f'DIÂMETRO BROCA (Linha {i + 1}):', broca_options, default='Todos')
                revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha {i + 1}):', revestimento_options, default='Todos')
                tipo_sonda = st.multiselect(f'TIPO SONDA (Linha {i + 1}):', tipo_sonda_options, default='Todos')

                # Filtrar o DataFrame e atualizar as opções para filtros dependentes
                df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)

                # Atualizar as opções dos filtros baseando-se no DataFrame filtrado
                atividade_options = ["Todos"] + get_filter_options(df_filtered, 'ATIVIDADE')
                operacao_options = ["Todos"] + get_filter_options(df_filtered, 'OPERACAO')
                etapa_options = ["Todos"] + get_filter_options(df_filtered, 'ETAPA')
                fase_options = ["Todos"] + get_filter_options(df_filtered, 'FASE')
                obz_options = ["Todos"] + get_filter_options(df_filtered, 'Obz')
                broca_options = ["Todos"] + get_filter_options(df_filtered, 'Diâmetro Broca')
                revestimento_options = ["Todos"] + get_filter_options(df_filtered, 'Diâmetro Revestimento')
                tipo_sonda_options = ["Todos"] + get_filter_options(df_filtered, 'Tipo_sonda')

                # Exibir DataFrames filtrados para amostras válidas e outliers
                df_non_outliers = df_filtered[df_filtered['Outlier'] == False]
                df_outliers = df_filtered[df_filtered['Outlier'] == True]

                st.markdown(f"<div style='background-color: #E8F4FF; padding: 10px; color: #00008B;'>Quantidade de Amostras sem Outliers: {df_non_outliers.shape[0]}</div>", unsafe_allow_html=True)
                st.dataframe(df_non_outliers.reset_index(drop=True))
                st.markdown(f"<div style='background-color: #FFE8E8; padding: 10px; color: #8B0000;'>Quantidade de Amostras com Outliers: {df_outliers.shape[0]}</div>", unsafe_allow_html=True)
                st.dataframe(df_outliers.reset_index(drop=True))
    
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")

else:
    st.warning("Nenhum arquivo foi carregado.")
