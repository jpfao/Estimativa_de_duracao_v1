import streamlit as st
import pandas as pd

# Função para filtrar as opções e remover outliers com filtros interdependentes
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

            for i, row in df_reference.iterrows():
                st.markdown(f"<div style='background-color: #008542; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha {i + 1}</div>", unsafe_allow_html=True)

                # Gerar lista de opções válidas após cada filtro e ordenar
                atividade_options = sorted(df['ATIVIDADE'].unique().tolist())
                operacao_options = sorted(df['OPERACAO'].unique().tolist())
                etapa_options = sorted(df['ETAPA'].unique().tolist())
                fase_options = sorted(df['FASE'].unique().tolist())
                obz_options = sorted(df['Obz'].unique().tolist())
                broca_options = sorted(df['Diâmetro Broca'].unique().tolist())
                revestimento_options = sorted(df['Diâmetro Revestimento'].unique().tolist())
                tipo_sonda_options = sorted(df['Tipo_sonda'].unique().tolist())

                # Obter valores de filtro da linha do arquivo de referência
                atividade = st.selectbox(f'ATIVIDADE (Linha {i + 1}):', ['Todos'] + atividade_options)
                operacao = st.selectbox(f'OPERAÇÃO (Linha {i + 1}):', ['Todos'] + operacao_options)
                etapa = st.selectbox(f'ETAPA (Linha {i + 1}):', ['Todos'] + etapa_options)
                fase = st.selectbox(f'FASE (Linha {i + 1}):', ['Todos'] + fase_options)
                obz = st.selectbox(f'OBZ (Linha {i + 1}):', ['Todos'] + obz_options)
                broca = st.multiselect(f'DIÂMETRO BROCA (Linha {i + 1}):', ['Todos'] + broca_options)
                revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha {i + 1}):', ['Todos'] + revestimento_options)
                tipo_sonda = st.multiselect(f'TIPO SONDA (Linha {i + 1}):', ['Todos'] + tipo_sonda_options)
                
                # Aplicar filtro e atualizar opções subsequentes
                df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)
                df_non_outliers = df_filtered[df_filtered['Outlier'] == False]
                df_outliers = df_filtered[df_filtered['Outlier'] == True]

                # Exibir dados filtrados e contagem
                st.markdown(
                    f"<div style='background-color: #E8F4FF; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #00008B; font-size: 18px; text-align: center;'>"
                    f"Quantidade de Amostras sem Outliers (Linha {i + 1}): <strong>{df_non_outliers.shape[0]}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_non_outliers.reset_index(drop=True))

                st.markdown(
                    f"<div style='background-color: #FFE8E8; padding: 10px; border-radius: 5px; margin: 20px 0 10px 0; color: #8B0000; font-size: 18px; text-align: center;'>"
                    f"Quantidade de Amostras com Outliers (Linha {i + 1}): <strong>{df_outliers.shape[0]}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_outliers.reset_index(drop=True))

                # Botão para incluir linha manual abaixo da linha automática atual
                if st.button(f"Incluir linha abaixo da Linha {i + 1}"):
                    add_manual_row(i + 1)

                # Exibir linhas manuais adicionadas abaixo da linha automática atual
                if i + 1 in st.session_state.manual_rows:
                    for manual_row_num in st.session_state.manual_rows[i + 1]:
                        st.markdown(
                            f"<div style='background-color: #8B008B; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha Manual {manual_row_num}</div>",
                            unsafe_allow_html=True
                        )

                        # Campos de entrada para a linha manual e filtro interdependente
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            atividade = st.selectbox(f'ATIVIDADE (Linha Manual {manual_row_num}):', ['Todos'] + atividade_options)
                        with col2:
                            operacao = st.selectbox(f'OPERAÇÃO (Linha Manual {manual_row_num}):', ['Todos'] + operacao_options)
                        with col3:
                            etapa = st.selectbox(f'ETAPA (Linha Manual {manual_row_num}):', ['Todos'] + etapa_options)
                        with col4:
                            fase = st.selectbox(f'FASE (Linha Manual {manual_row_num}):', ['Todos'] + fase_options)

                        col5, col6, col7, col8 = st.columns(4)
                        with col5:
                            obz = st.selectbox(f'OBZ (Linha Manual {manual_row_num}):', ['Todos'] + obz_options)
                        with col6:
                            broca = st.multiselect(f'DIÂMETRO BROCA (Linha Manual {manual_row_num}):', ['Todos'] + broca_options)
                        with col7:
                            revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha Manual {manual_row_num}):', ['Todos'] + revestimento_options)
                        with col8:
                            tipo_sonda = st.multiselect(f'TIPO SONDA (Linha Manual {manual_row_num}):', ['Todos'] + tipo_sonda_options)

                        # Aplicar o filtro para a linha manual e exibir os dados
                        df_manual_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)
                        df_manual_non_outliers = df_manual_filtered[df_manual_filtered['Outlier'] == False]
                        df_manual_outliers = df_manual_filtered[df_manual_filtered['Outlier'] == True]

                        st.markdown(
                            f"<div style='background-color: #E8F4FF; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #00008B; font-size: 18px; text-align: center;'>"
                            f"Quantidade de Amostras sem Outliers (Linha Manual {manual_row_num}): <strong>{df_manual_non_outliers.shape[0]}</strong>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        st.dataframe(df_manual_non_outliers.reset_index(drop=True))

                        st.markdown(
                            f"<div style='background-color: #FFE8E8; padding: 10px; border-radius: 5px; margin: 20px 0 10px 0; color: #8B0000; font-size: 18px; text-align: center;'>"
                            f"Quantidade de Amostras com Outliers (Linha Manual {manual_row_num}): <strong>{df_manual_outliers.shape[0]}</strong>"
                            f"</div>",
                            unsafe_allow_html=True
                        )
                        st.dataframe(df_manual_outliers.reset_index(drop=True))

        # Adicionar linha manual globalmente (independente das linhas automáticas)
        if st.button("Incluir linha manual no final"):
            add_manual_row(-1)

        # Exibir linhas manuais adicionadas ao final
        if -1 in st.session_state.manual_rows:
            for manual_row_num in st.session_state.manual_rows[-1]:
                st.markdown(
                    f"<div style='background-color: #8B008B; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha Manual {manual_row_num} (Final)</div>",
                    unsafe_allow_html=True
                )

                # Campos de entrada para a linha manual no final
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    atividade = st.selectbox(f'ATIVIDADE (Linha Manual {manual_row_num}):', ['Todos'] + atividade_options)
                
                with col2:
                    operacao = st.selectbox(f'OPERAÇÃO (Linha Manual {manual_row_num}):', ['Todos'] + operacao_options)
                
                with col3:
                    etapa = st.selectbox(f'ETAPA (Linha Manual {manual_row_num}):', ['Todos'] + etapa_options)
                
                with col4:
                    fase = st.selectbox(f'FASE (Linha Manual {manual_row_num}):', ['Todos'] + fase_options)

                col5, col6, col7, col8 = st.columns(4)

                with col5:
                    obz = st.selectbox(f'OBZ (Linha Manual {manual_row_num}):', ['Todos'] + obz_options)
                
                with col6:
                    broca = st.multiselect(f'DIÂMETRO BROCA (Linha Manual {manual_row_num}):', ['Todos'] + broca_options)
                
                with col7:
                    revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha Manual {manual_row_num}):', ['Todos'] + revestimento_options)
                
                with col8:
                    tipo_sonda = st.multiselect(f'TIPO SONDA (Linha Manual {manual_row_num}):', ['Todos'] + tipo_sonda_options)

                # Aplicar o filtro para a linha manual final e exibir os dados
                df_final_manual_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)
                df_final_manual_non_outliers = df_final_manual_filtered[df_final_manual_filtered['Outlier'] == False]
                df_final_manual_outliers = df_final_manual_filtered[df_final_manual_filtered['Outlier'] == True]

                st.markdown(
                    f"<div style='background-color: #E8F4FF; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #00008B; font-size: 18px; text-align: center;'>"
                    f"Quantidade de Amostras sem Outliers (Linha Manual {manual_row_num} - Final): <strong>{df_final_manual_non_outliers.shape[0]}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_final_manual_non_outliers.reset_index(drop=True))

                st.markdown(
                    f"<div style='background-color: #FFE8E8; padding: 10px; border-radius: 5px; margin: 20px 0 10px 0; color: #8B0000; font-size: 18px; text-align: center;'>"
                    f"Quantidade de Amostras com Outliers (Linha Manual {manual_row_num} - Final): <strong>{df_final_manual_outliers.shape[0]}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_final_manual_outliers.reset_index(drop=True))

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")

else:
    st.warning("Nenhum arquivo foi carregado.")
