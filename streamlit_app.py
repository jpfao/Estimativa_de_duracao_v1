import streamlit as st
import pandas as pd

# Função para filtrar os valores das listas de acordo com a seleção
def filter_options(df, atividade, operacao, etapa):
    df_filtered = df[(df['ATIVIDADE'] == atividade) &
                     (df['OPERACAO'] == operacao) &
                     (df['ETAPA'] == etapa)]
    return df_filtered

# Função para adicionar uma nova linha ao formulário
def add_new_row():
    if 'num_rows' not in st.session_state:
        st.session_state.num_rows = 1
    else:
        st.session_state.num_rows += 1

# Definir a largura da página como ampla
st.set_page_config(layout="wide")

# Upload do arquivo Excel
uploaded_file = st.file_uploader("Upload do arquivo Excel", type="xlsx")

if uploaded_file is not None:
    try:
        # Carregar o arquivo Excel
        df = pd.read_excel(uploaded_file)
        
        # Exibir os dados carregados
        st.write(df)

        # Exibir o número de linhas e colunas do arquivo
        st.success(f"Arquivo carregado com sucesso! Tamanho: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        # Listas de valores únicos para picklists
        atividades = df['ATIVIDADE'].unique()
        operacoes = df['OPERACAO'].unique()
        etapas = df['ETAPA'].unique()

        # Inicializar número de linhas, se não estiver no estado
        if 'num_rows' not in st.session_state:
            st.session_state.num_rows = 1

        st.title('Formulário Interativo para Sequência Operacional')

        # Renderizar múltiplas linhas de formulários
        for row in range(st.session_state.num_rows):
            st.write(f"**Linha {row + 1}**")
            
            # Criar colunas ajustando a largura dos campos
            col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])  # Largura ajustada para os campos de seleção
            
            with col1:
                atividade = st.selectbox(f'ATIVIDADE (linha {row + 1}):', atividades, key=f'atividade_{row}', 
                                         label_visibility="visible", use_container_width=True)
            with col2:
                operacao = st.selectbox(f'OPERACAO (linha {row + 1}):', operacoes, key=f'operacao_{row}', 
                                        label_visibility="visible", use_container_width=True)
            with col3:
                etapa = st.selectbox(f'ETAPA (linha {row + 1}):', etapas, key=f'etapa_{row}', 
                                     label_visibility="visible", use_container_width=True)
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
    
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
else:
    st.warning("Nenhum arquivo foi carregado.")
