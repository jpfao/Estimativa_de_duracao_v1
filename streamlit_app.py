import streamlit as st
import pandas as pd

# Função para carregar os dados da planilha Excel
@st.cache_data
def load_data():
    return pd.read_excel('NovaBasePRF_2021-2024_Codificados&Dinamica_06_09_outliers.xlsx')

# Função para adicionar uma nova linha ao formulário
def add_new_row():
    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = 1
    else:
        st.session_state.num_rows += 1

# Função para filtrar os valores das listas de acordo com a seleção
def filter_options(df, atividade, operacao, etapa):
    df_filtered = df[(df['ATIVIDADE'] == atividade) &
                     (df['OPERACAO'] == operacao) &
                     (df['ETAPA'] == etapa)]
    return df_filtered

# Carregar os dados da planilha Excel
df = load_data()

if not df.empty:
    # Inicializar número de linhas
    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = 1

    # Listas de valores únicos para picklists
    atividades = df['ATIVIDADE'].unique()
    operacoes = df['OPERACAO'].unique()
    etapas = df['ETAPA'].unique()

    # Título do formulário
    st.title('Formulário Interativo para Sequência Operacional')

    # Renderizar múltiplas linhas de formulários
    for row in range(st.session_state.num_rows):
        st.write(f"**Linha {row + 1}**")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            atividade = st.selectbox(f'Selecione a ATIVIDADE (linha {row + 1}):', atividades, key=f'atividade_{row}')
        with col2:
            operacao = st.selectbox(f'Selecione a OPERACAO (linha {row + 1}):', operacoes, key=f'operacao_{row}')
        with col3:
            etapa = st.selectbox(f'Selecione a ETAPA (linha {row + 1}):', etapas, key=f'etapa_{row}')
        with col4:
            fase = st.number_input(f'FASE (linha {row + 1}):', min_value=0, max_value=100, key=f'fase_{row}')
        with col5:
            extensao = st.number_input(f'EXTENSÃO (linha {row + 1}):', min_value=0.0, key=f'extensao_{row}')
        
        # Filtrando dados para cada linha
        df_filtrado = filter_options(df, atividade, operacao, etapa)
        st.write('Amostragem dos dados correspondentes:')
        st.write(df_filtrado)
    
    # Botão para adicionar nova linha
    st.button("Adicionar nova linha", on_click=add_new_row)
    
else:
    st.warning("Nenhum dado disponível para exibição.")
