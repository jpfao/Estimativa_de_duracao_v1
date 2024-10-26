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

# Upload do arquivo principal
uploaded_file = st.file_uploader("Upload do arquivo planilhão sumarizado", type="xlsx")

# Upload do arquivo de referência
uploaded_reference = st.file_uploader("Upload do arquivo de referência para a SEQOP", type="xlsx")

if uploaded_file is not None:
    try:
        # Carregar o arquivo principal
        df = pd.read_excel(uploaded_file)
        
        # Exibir o número de linhas e colunas do arquivo principal
        st.success(f"Arquivo principal carregado com sucesso! Tamanho: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        st.title('Formulário Interativo para Sequência Operacional')

        if uploaded_reference is not None:
            # Carregar o arquivo de referência
            df_reference = pd.read_excel(uploaded_reference)
            st.success("Arquivo de referência carregado com sucesso!")

            # Loop para criar uma seção de filtro para cada linha do arquivo de referência
            for i, row in df_reference.iterrows():
                st.markdown(f"<div style='background-color: #008542; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha {i + 1}</div>", unsafe_allow_html=True)

                # Obter valores de filtro da linha do arquivo de referência, ignorando colunas com valor "TODOS"
                atividade = row.get('ATIVIDADE') if row.get('ATIVIDADE') != "TODOS" else None
                operacao = row.get('OPERACAO') if row.get('OPERACAO') != "TODOS" else None
                etapa = row.get('ETAPA') if row.get('ETAPA') != "TODOS" else None
                fase = row.get('FASE') if row.get('FASE') != "TODOS" else None
                obz = row.get('Obz') if row.get('Obz') != "TODOS" else None
                broca = [row.get('Diâmetro Broca')] if pd.notna(row.get('Diâmetro Broca')) and row.get('Diâmetro Broca') != "TODOS" else None
                revestimento = [row.get('Diâmetro Revestimento')] if pd.notna(row.get('Diâmetro Revestimento')) and row.get('Diâmetro Revestimento') != "TODOS" else None
                tipo_sonda = [row.get('Tipo_sonda')] if pd.notna(row.get('Tipo_sonda')) and row.get('Tipo_sonda') != "TODOS" else None

                # Renderizar campos com valores pré-preenchidos do arquivo de referência, mas que podem ser ajustados manualmente
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    atividade = st.selectbox(f'ATIVIDADE (Linha {i + 1}):', ['Todos'] + df['ATIVIDADE'].unique().tolist(), index=(df['ATIVIDADE'].unique().tolist().index(atividade) + 1) if atividade else 0)
                    if atividade == 'Todos':
                        atividade = None

                with col2:
                    operacao = st.selectbox(f'OPERAÇÃO (Linha {i + 1}):', ['Todos'] + df['OPERACAO'].unique().tolist(), index=(df['OPERACAO'].unique().tolist().index(operacao) + 1) if operacao else 0)
                    if operacao == 'Todos':
                        operacao = None

                with col3:
                    etapa = st.selectbox(f'ETAPA (Linha {i + 1}):', ['Todos'] + df['ETAPA'].unique().tolist(), index=(df['ETAPA'].unique().tolist().index(etapa) + 1) if etapa else 0)
                    if etapa == 'Todos':
                        etapa = None

                with col4:
                    fase = st.selectbox(f'FASE (Linha {i + 1}):', ['Todos'] + df['FASE'].unique().tolist(), index=(df['FASE'].unique().tolist().index(fase) + 1) if fase else 0)
                    if fase == 'Todos':
                        fase = None

                col5, col6, col7, col8 = st.columns(4)

                with col5:
                    obz = st.selectbox(f'OBZ (Linha {i + 1}):', ['Todos'] + df['Obz'].unique().tolist(), index=(df['Obz'].unique().tolist().index(obz) + 1) if obz else 0)
                    if obz == 'Todos':
                        obz = None

                with col6:
                    broca = st.multiselect(f'DIÂMETRO BROCA (Linha {i + 1}):', ['Todos'] + df['Diâmetro Broca'].unique().tolist(), default=broca or 'Todos')
                    if 'Todos' in broca:
                        broca = None

                with col7:
                    revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha {i + 1}):', ['Todos'] + df['Diâmetro Revestimento'].unique().tolist(), default=revestimento or 'Todos')
                    if 'Todos' in revestimento:
                        revestimento = None

                with col8:
                    tipo_sonda = st.multiselect(f'TIPO SONDA (Linha {i + 1}):', ['Todos'] + df['Tipo_sonda'].unique().tolist(), default=tipo_sonda or 'Todos')
                    if 'Todos' in tipo_sonda:
                        tipo_sonda = None

                # Aplicar filtro com base nos valores da linha do arquivo de referência (ou ajustados manualmente)
                df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=obz, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)

                # Dividir os dados filtrados em Outliers e Não-Outliers
                df_non_outliers = df_filtered[df_filtered['Outlier'] == False]
                df_outliers = df_filtered[df_filtered['Outlier'] == True]

                # Exibir quantidade e tabela de amostras onde 'Outlier' é False com estilo customizado
                st.markdown(
                    f"<div style='background-color: #E8F4FF; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #00008B; font-size: 18px; text-align: center;'>"
                    f"Quantidade de Amostras sem Outliers (Linha {i + 1}): <strong>{df_non_outliers.shape[0]}</strong>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.dataframe(df_non_outliers.reset_index(drop=True))

                # Exibir quantidade e tabela de amostras onde 'Outlier' é True com estilo customizado e espaçamento uniforme
                st.markdown(
                    f"<div style='background-color: #FFE8E8; padding: 10px; border-radius: 5px; margin: 20px 0 10px 0; color: #8B0000; font-size: 
