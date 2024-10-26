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

# Definir a largura da página como ampla
st.set_page_config(layout="wide")

# Função para adicionar linha manual abaixo de uma linha específica
def add_manual_row(below_index):
    if below_index not in st.session_state.manual_rows:
        st.session_state.manual_rows[below_index] = []
    st.session_state.manual_rows[below_index].append(len(st.session_state.manual_rows[below_index]) + 1)

# Função para excluir uma linha manual ou automática
def delete_row(index, is_manual=False, manual_index=None):
    if is_manual:
        st.session_state.manual_rows[index].remove(manual_index)
        if not st.session_state.manual_rows[index]:
            del st.session_state.manual_rows[index]
    else:
        st.session_state.automatic_rows.remove(index)

# Upload do arquivo principal
uploaded_file = st.file_uploader("Upload do arquivo planilhão sumarizado", type="xlsx")
# Upload do arquivo de referência
uploaded_reference = st.file_uploader("Upload do arquivo de referência para a SEQOP", type="xlsx")

# Dicionário para armazenar listas de linhas manuais entre as linhas automáticas
if 'manual_rows' not in st.session_state:
    st.session_state.manual_rows = {}
if 'automatic_rows' not in st.session_state:
    st.session_state.automatic_rows = []

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
                if i not in st.session_state.automatic_rows:
                    st.session_state.automatic_rows.append(i)

                st.markdown(f"<div style='background-color: #008542; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha {i + 1}</div>", unsafe_allow_html=True)

                # Botão para excluir linha automática
                if st.button(f"Excluir Linha {i + 1}"):
                    delete_row(i)
                    continue  # Pule o resto do loop para essa linha

                # Obter valores de filtro da linha do arquivo de referência, ignorando colunas com valor "TODOS"
                atividade = row.get('ATIVIDADE') if row.get('ATIVIDADE') != "TODOS" else None
                operacao = row.get('OPERACAO') if row.get('OPERACAO') != "TODOS" else None
                etapa = row.get('ETAPA') if row.get('ETAPA') != "TODOS" else None
                fase = row.get('FASE') if row.get('FASE') != "TODOS" else None
                obz = row.get('Obz') if row.get('Obz') != "TODOS" else None
                broca = [row.get('Diâmetro Broca')] if pd.notna(row.get('Diâmetro Broca')) and row.get('Diâmetro Broca') != "TODOS" else None
                revestimento = [row.get('Diâmetro Revestimento')] if pd.notna(row.get('Diâmetro Revestimento')) and row.get('Diâmetro Revestimento') != "TODOS" else None
                tipo_sonda = [row.get('Tipo_sonda')] if pd.notna(row.get('Tipo_sonda')) and row.get('Tipo_sonda') != "TODOS" else None

                # Renderizar campos com valores pré-preenchidos do arquivo de referência
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    atividade = st.selectbox(f'ATIVIDADE (Linha {i + 1}):', ['Todos'] + sorted(df['ATIVIDADE'].unique()), index=(df['ATIVIDADE'].unique().tolist().index(atividade) + 1) if atividade else 0)
                    if atividade == 'Todos':
                        atividade = None

                with col2:
                    operacao = st.selectbox(f'OPERAÇÃO (Linha {i + 1}):', ['Todos'] + sorted(df['OPERACAO'].unique()), index=(df['OPERACAO'].unique().tolist().index(operacao) + 1) if operacao else 0)
                    if operacao == 'Todos':
                        operacao = None

                with col3:
                    etapa = st.selectbox(f'ETAPA (Linha {i + 1}):', ['Todos'] + sorted(df['ETAPA'].unique()), index=(df['ETAPA'].unique().tolist().index(etapa) + 1) if etapa else 0)
                    if etapa == 'Todos':
                        etapa = None

                with col4:
                    fase = st.selectbox(f'FASE (Linha {i + 1}):', ['Todos'] + sorted(df['FASE'].unique()), index=(df['FASE'].unique().tolist().index(fase) + 1) if fase else 0)
                    if fase == 'Todos':
                        fase = None

                col5, col6, col7, col8 = st.columns(4)

                with col5:
                    obz = st.selectbox(f'OBZ (Linha {i + 1}):', ['Todos'] + sorted(df['Obz'].unique()), index=(df['Obz'].unique().tolist().index(obz) + 1) if obz else 0)
                    if obz == 'Todos':
                        obz = None

                with col6:
                    broca = st.multiselect(f'DIÂMETRO BROCA (Linha {i + 1}):', ['Todos'] + sorted(df['Diâmetro Broca'].unique()), default=broca or 'Todos')
                    if 'Todos' in broca:
                        broca = None

                with col7:
                    revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha {i + 1}):', ['Todos'] + sorted(df['Diâmetro Revestimento'].unique()), default=revestimento or 'Todos')
                    if 'Todos' in revestimento:
                        revestimento = None

                with col8:
                    tipo_sonda = st.multiselect(f'TIPO SONDA (Linha {i + 1}):', ['Todos'] + sorted(df['Tipo_sonda'].unique()), default=tipo_sonda or 'Todos')
                    if 'Todos' in tipo_sonda:
                        tipo_sonda = None

                # Aplicar filtro e exibir os dados
                df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)
                df_non_outliers = df_filtered[df_filtered['Outlier'] == False]
                df_outliers = df_filtered[df_filtered['Outlier'] == True]

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

                        # Botão para excluir linha manual
                        if st.button(f"Excluir Linha Manual {manual_row_num} abaixo de Linha {i + 1}"):
                            delete_row(i + 1, is_manual=True, manual_index=manual_row_num)
                            continue  # Pule o resto do loop para essa linha manual

                        # Campos de entrada para a linha manual
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            atividade = st.selectbox(f'ATIVIDADE (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['ATIVIDADE'].unique()))
                        
                        with col2:
                            operacao = st.selectbox(f'OPERAÇÃO (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['OPERACAO'].unique()))
                        
                        with col3:
                            etapa = st.selectbox(f'ETAPA (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['ETAPA'].unique()))
                        
                        with col4:
                            fase = st.selectbox(f'FASE (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['FASE'].unique()))

                        col5, col6, col7, col8 = st.columns(4)

                        with col5:
                            obz = st.selectbox(f'OBZ (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Obz'].unique()))
                        
                        with col6:
                            broca = st.multiselect(f'DIÂMETRO BROCA (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Diâmetro Broca'].unique()))
                        
                        with col7:
                            revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Diâmetro Revestimento'].unique()))
                        
                        with col8:
                            tipo_sonda = st.multiselect(f'TIPO SONDA (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Tipo_sonda'].unique()))

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

                # Botão para excluir linha manual no final
                if st.button(f"Excluir Linha Manual {manual_row_num} (Final)"):
                    delete_row(-1, is_manual=True, manual_index=manual_row_num)
                    continue

                # Campos de entrada para a linha manual no final
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    atividade = st.selectbox(f'ATIVIDADE (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['ATIVIDADE'].unique()))
                
                with col2:
                    operacao = st.selectbox(f'OPERAÇÃO (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['OPERACAO'].unique()))
                
                with col3:
                    etapa = st.selectbox(f'ETAPA (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['ETAPA'].unique()))
                
                with col4:
                    fase = st.selectbox(f'FASE (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['FASE'].unique()))

                col5, col6, col7, col8 = st.columns(4)

                with col5:
                    obz = st.selectbox(f'OBZ (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Obz'].unique()))
                
                with col6:
                    broca = st.multiselect(f'DIÂMETRO BROCA (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Diâmetro Broca'].unique()))
                
                with col7:
                    revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Diâmetro Revestimento'].unique()))
                
                with col8:
                    tipo_sonda = st.multiselect(f'TIPO SONDA (Linha Manual {manual_row_num}):', ['Todos'] + sorted(df['Tipo_sonda'].unique()))

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
