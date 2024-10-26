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
        
        st.title('Formulário Interativo para Sequência Operacional')

        # Renderizar formulários interativos
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            atividade = st.selectbox('ATIVIDADE:', ['Todos'] + df['ATIVIDADE'].unique().tolist())
            if atividade == 'Todos':
                atividade = None

        with col2:
            operacao = st.selectbox('OPERAÇÃO:', ['Todos'] + df['OPERACAO'].unique().tolist())
            if operacao == 'Todos':
                operacao = None

        with col3:
            etapa = st.selectbox('ETAPA:', ['Todos'] + df['ETAPA'].unique().tolist())
            if etapa == 'Todos':
                etapa = None

        with col4:
            fase = st.selectbox('FASE:', ['Todos'] + df['FASE'].unique().tolist())
            if fase == 'Todos':
                fase = None

        col5, col6, col7, col8 = st.columns(4)

        with col5:
            obz = st.selectbox('OBZ:', ['Todos'] + df['Obz'].unique().tolist())
            if obz == 'Todos':
                obz = None

        with col6:
            broca = st.multiselect('DIÂMETRO BROCA:', ['Todos'] + df['Diâmetro Broca'].unique().tolist(), default='Todos')
            if 'Todos' in broca:
                broca = None

        with col7:
            revestimento = st.multiselect('DIÂMETRO REVESTIMENTO:', ['Todos'] + df['Diâmetro Revestimento'].unique().tolist(), default='Todos')
            if 'Todos' in revestimento:
                revestimento = None

        with col8:
            tipo_sonda = st.multiselect('TIPO SONDA:', ['Todos'] + df['Tipo_sonda'].unique().tolist(), default='Todos')
            if 'Todos' in tipo_sonda:
                tipo_sonda = None

        # Aplicar filtro com base nos valores selecionados
        df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)

        # Dividir os dados filtrados em Outliers e Não-Outliers
        df_non_outliers = df_filtered[df_filtered['Outlier'] == False]
        df_outliers = df_filtered[df_filtered['Outlier'] == True]

        # Exibir tabela de amostras onde 'Outlier' é False
        st.write("Amostras não Outliers")
        st.dataframe(df_non_outliers.reset_index(drop=True))

        # Exibir tabela de amostras onde 'Outlier' é True
        st.write("Amostras outliers")
        st.dataframe(df_outliers.reset_index(drop=True))

    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
else:
    st.warning("Nenhum arquivo foi carregado.")
