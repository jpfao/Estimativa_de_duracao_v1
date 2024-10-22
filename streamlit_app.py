import streamlit as st
import pandas as pd

# Função para filtrar as opções e remover outliers
def filter_options(df, atividade=None, operacao=None, etapa=None, fase=None, obz=None, broca=None, revestimento=None, tipo_sonda=None):
    df_filtered = df[df['Outlier'] == False]  # Remover outliers
    
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
        
        # Exibir o número de linhas e colunas do arquivo
        st.success(f"Arquivo carregado com sucesso! Tamanho: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        # Inicializar número de linhas, se não estiver no estado
        if 'num_rows' not in st.session_state:
            st.session_state.num_rows = 1

        st.title('Formulário Interativo para Sequência Operacional')

        # Renderizar múltiplas linhas de formulários
        for row in range(st.session_state.num_rows):
            # Criar faixa de separação para cada linha
            st.markdown(f"""
                <div style='background-color: #008542; padding: 1px; margin-bottom: 10px;'>
                    <h4 style='color: white; text-align: center; margin: 5; font-size: 130%;'>Linha {row + 1}</h4>
                </div>
            """, unsafe_allow_html=True)

            # Primeira linha de campos: ATIVIDADE, OPERACAO, ETAPA, FASE
            col1, col2, col3, col4 = st.columns([2, 2, 2, 2])  # Largura ajustada para os campos de seleção
            
            # Seleção da ATIVIDADE
            with col1:
                atividade = st.selectbox(f'ATIVIDADE (linha {row + 1}):', df['ATIVIDADE'].unique(), key=f'atividade_{row}')
            
            # Filtrar as opções de OPERAÇÃO com base na ATIVIDADE selecionada
            df_filtered_atividade = filter_options(df, atividade=atividade)
            
            # Seleção da OPERAÇÃO
            with col2:
                operacao = st.selectbox(f'OPERACAO (linha {row + 1}):', df_filtered_atividade['OPERACAO'].unique(), key=f'operacao_{row}')
            
            # Filtrar as opções de ETAPA com base na ATIVIDADE e OPERAÇÃO selecionadas
            df_filtered_operacao = filter_options(df, atividade=atividade, operacao=operacao)
            
            # Seleção da ETAPA
            with col3:
                etapa = st.selectbox(f'ETAPA (linha {row + 1}):', df_filtered_operacao['ETAPA'].unique(), key=f'etapa_{row}')
            
            # Filtrar as opções de FASE com base na ATIVIDADE, OPERAÇÃO e ETAPA selecionadas
            df_filtered_etapa = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa)
            
            # Seleção da FASE (como picklist)
            with col4:
                fase = st.selectbox(f'FASE (linha {row + 1}):', df_filtered_etapa['FASE'].unique(), key=f'fase_{row}')
            
            # Segunda linha de campos: DIÂMETRO BROCA, DIÂMETRO REVESTIMENTO, OBZ, TIPO SONDA
            col5, col6, col7, col8 = st.columns([2, 2, 2, 2])
            
            # Seleção de DIÂMETRO BROCA com múltipla escolha
            with col5:
                broca = st.multiselect(f'DIÂMETRO BROCA (linha {row + 1}):', ['Todos'] + list(df_filtered_etapa['Diâmetro Broca'].unique()), default='Todos', key=f'broca_{row}')
            
            # Seleção de DIÂMETRO REVESTIMENTO com múltipla escolha
            with col6:
                revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (linha {row + 1}):', ['Todos'] + list(df_filtered_etapa['Diâmetro Revestimento'].unique()), default='Todos', key=f'revestimento_{row}')
            
            # Seleção de OBZ
            with col7:
                obz = st.selectbox(f'OBZ (linha {row + 1}):', df_filtered_etapa['Obz'].unique(), key=f'obz_{row}')
            
            # Seleção de TIPO SONDA com múltipla escolha
            with col8:
                tipo_sonda = st.multiselect(f'TIPO SONDA (linha {row + 1}):', ['Todos'] + list(df_filtered_etapa['Tipo_sonda'].unique()), default='Todos', key=f'tipo_sonda_{row}')
            
            # Filtrando dados para cada linha e removendo outliers
            df_filtrado = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)

            # Exibir o número de amostras filtradas
            st.info(f'Número de amostras filtradas: {df_filtrado.shape[0]}')

            # Exibir a tabela filtrada
            if not df_filtrado.empty:
                st.write('Amostragem dos dados correspondentes (sem outliers):')
                st.dataframe(df_filtrado)
        
        # Botão para adicionar nova linha
        st.button("Adicionar nova linha", on_click=add_new_row)
    
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
else:
    st.warning("Nenhum arquivo foi carregado.")
