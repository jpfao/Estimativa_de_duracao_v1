import streamlit as st
import pandas as pd

# Função para filtrar as opções e remover outliers
@st.cache_data
def filter_options(df, atividade=None, operacao=None, etapa=None, fase=None, obz=None, broca=None, revestimento=None, tipo_sonda=None):
    df_filtered = df.copy()  # Trabalhar com cópia para evitar alterações no original
    
    # Aplicar filtros apenas se o valor for diferente de "TODOS" e não for None
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
    if broca and isinstance(broca, list) and 'TODOS' not in broca:
        df_filtered = df_filtered[df_filtered['Diâmetro Broca'].isin(broca)]
    if revestimento and isinstance(revestimento, list) and 'TODOS' not in revestimento:
        df_filtered = df_filtered[df_filtered['Diâmetro Revestimento'].isin(revestimento)]
    if tipo_sonda and isinstance(tipo_sonda, list) and 'TODOS' not in tipo_sonda:
        df_filtered = df_filtered[df_filtered['Tipo_sonda'].isin(tipo_sonda)]
    
    return df_filtered

# Função para obter os valores de uma linha específica
def obter_valores_linha(df, linha_numero):
    linha = df[df['Linha'] == linha_numero]
    if linha.empty:
        return None
    return {
        'FASE': linha['FASE'].values[0],
        'ATIVIDADE': linha['ATIVIDADE'].values[0],
        'OPERACAO': linha['OPERACAO'].values[0],
        'ETAPA': linha['ETAPA'].values[0],
        'Tipo_sonda': linha['Tipo_sonda'].values[0]
    }

# Configurar a página para exibição ampla
st.set_page_config(layout="wide")

# Upload do arquivo principal
uploaded_file = st.file_uploader("Upload do arquivo planilhão sumarizado", type="xlsx")

# Upload do arquivo de referência
uploaded_reference = st.file_uploader("Upload do arquivo de referência para a SEQOP", type="xlsx")

if uploaded_file is not None:
    try:
        # Carregar o arquivo principal
        df = pd.read_excel(uploaded_file)
        
        # Garantir que as colunas sejam do tipo string
        for col in ['ATIVIDADE', 'OPERACAO', 'ETAPA', 'FASE', 'Obz', 'Tipo_sonda', 'Diâmetro Broca', 'Diâmetro Revestimento']:
            df[col] = df[col].astype(str)
        
        # Exibir informações sobre o arquivo carregado
        st.success(f"Arquivo principal carregado com sucesso! Tamanho: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        st.title('Seleção de amostras para Simulação da Estimativa de duração de Poço')

        # Carregar o arquivo de referência, se disponível
        if uploaded_reference is not None:
            df_reference = pd.read_excel(uploaded_reference)
            st.success("Arquivo de referência carregado com sucesso!")

            # Garantir que as colunas do DataFrame de referência sejam strings
            for col in ['FASE', 'ATIVIDADE', 'OPERACAO', 'ETAPA', 'Tipo_sonda']:
                df_reference[col] = df_reference[col].astype(str)

            # Iterar sobre as linhas do DataFrame de referência
            for i in range(1, len(df_reference) + 1):
                st.markdown(f"<div style='background-color: #008542; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha {i}</div>", unsafe_allow_html=True)
                
                # Obter os valores para a linha atual
                valores = obter_valores_linha(df_reference, i)
                
                if valores is None:
                    st.warning(f"Linha {i} não encontrada no arquivo de referência.")
                    continue
                
                # Renderizar campos com valores obtidos do arquivo de referência
                col1, col2, col3, col4, col5 = st.columns(5)
            
                with col1:
                    fase = st.selectbox(f'FASE (Linha {i}):', sorted(['Todos'] + df_reference['FASE'].unique().tolist()), index=(df_reference['FASE'].unique().tolist().index(valores['FASE']) + 1) if valores['FASE'] else 0)
                    if fase == 'Todos':
                        fase = None
            
                with col2:
                    atividade = st.selectbox(f'ATIVIDADE (Linha {i}):', sorted(['Todos'] + df_reference['ATIVIDADE'].unique().tolist()), index=(df_reference['ATIVIDADE'].unique().tolist().index(valores['ATIVIDADE']) + 1) if valores['ATIVIDADE'] else 0)
                    if atividade == 'Todos':
                        atividade = None
            
                with col3:
                    operacao = st.selectbox(f'OPERAÇÃO (Linha {i}):', sorted(['Todos'] + df_reference['OPERACAO'].unique().tolist()), index=(df_reference['OPERACAO'].unique().tolist().index(valores['OPERACAO']) + 1) if valores['OPERACAO'] else 0)
                    if operacao == 'Todos':
                        operacao = None
            
                with col4:
                    etapa = st.selectbox(f'ETAPA (Linha {i}):', sorted(['Todos'] + df_reference['ETAPA'].unique().tolist()), index=(df_reference['ETAPA'].unique().tolist().index(valores['ETAPA']) + 1) if valores['ETAPA'] else 0)
                    if etapa == 'Todos':
                        etapa = None
            
                with col5:
                    tipo_sonda = st.selectbox(f'TIPO SONDA (Linha {i}):', sorted(['Todos'] + df_reference['Tipo_sonda'].unique().tolist()), index=(df_reference['Tipo_sonda'].unique().tolist().index(valores['Tipo_sonda']) + 1) if valores['Tipo_sonda'] else 0)
                    if tipo_sonda == 'Todos':
                        tipo_sonda = None

                # Aplicar filtro e exibir os dados
                df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, tipo_sonda=tipo_sonda)
                df_non_outliers = df_filtered[df_filtered['Outlier'] == False]
                df_outliers = df_filtered[df_filtered['Outlier'] == True]

                # Exibir a quantidade de amostras sem e com outliers
                st.markdown(
                    f"<div style='background-color: #E8F4FF; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #00008B; font-size: 18px; text-align: center;'>"
                    f"Quantidade de Amostras sem Outliers (Linha {i}): <strong>{df_non_outliers.shape[0]}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_non_outliers.reset_index(drop=True))

                st.markdown(
                    f"<div style='background-color: #FFE8E8; padding: 10px; border-radius: 5px; margin: 20px 0 10px 0; color: #8B0000; font-size: 18px; text-align: center;'>"
                    f"Quantidade de Amostras com Outliers (Linha {i}): <strong>{df_outliers.shape[0]}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_outliers.reset_index(drop=True))

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")

else:
    st.warning("Nenhum arquivo foi carregado. Por favor, faça o upload dos arquivos necessários.")
