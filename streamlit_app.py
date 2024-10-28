import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    if broca and isinstance(broca, list) and 'TODOS' not in broca:
        df_filtered = df_filtered[df_filtered['Diâmetro Broca'].isin(broca)]
    if revestimento and isinstance(revestimento, list) and 'TODOS' not in revestimento:
        df_filtered = df_filtered[df_filtered['Diâmetro Revestimento'].isin(revestimento)]
    if tipo_sonda and isinstance(tipo_sonda, list) and 'TODOS' not in tipo_sonda:
        df_filtered = df_filtered[df_filtered['Tipo_sonda'].isin(tipo_sonda)]
    
    # Remover colunas indesejadas
    columns_to_drop = ['depth_range_start', 'depth_range_end', 'Tipo_avanço', 'Extensão']
    df_filtered.drop(columns=columns_to_drop, inplace=True, errors='ignore')
    
    return df_filtered

# Função para gerar o boxplot com Plotly
def plot_boxplot_with_plotly(data, column, lim_inf, lim_sup, title):
    fig = go.Figure()
    
    # Adicionar boxplot
    fig.add_trace(go.Box(
        x=data[column],
        marker=dict(color='lightblue'),
        boxpoints='all',
        jitter=0.3,
        pointpos=-1.8
    ))
    
    # Adicionar linhas de referência
    median = round(data[column].median(), 1)
    lim_inf = round(lim_inf, 1)
    lim_sup = round(lim_sup, 1)
    
    fig.add_vline(x=median, line=dict(color="green", dash="dash"), name="Mediana", annotation_text=f"Mediana: {median:.1f}")
    fig.add_vline(x=lim_inf, line=dict(color="blue", dash="dash"), name="Limite Inferior", annotation_text=f"Limite Inferior: {lim_inf:.1f}")
    fig.add_vline(x=lim_sup, line=dict(color="orange", dash="dash"), name="Limite Superior", annotation_text=f"Limite Superior: {lim_sup:.1f}")
    
    # Configurações do layout
    fig.update_layout(
        title=title,
        width=400,  # Largura do gráfico
        height=200,  # Altura do gráfico
        margin=dict(l=40, r=40, t=40, b=40),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

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
        
        # Converter as colunas para o tipo string
        for col in ['ATIVIDADE', 'OPERACAO', 'ETAPA', 'FASE', 'Obz', 'Tipo_sonda', 'Diâmetro Broca', 'Diâmetro Revestimento']:
            df[col] = df[col].astype(str)
        
        # Formatar os valores de 'Taxa', 'LIM_INF_OUT' e 'LIM_SUP_OUT' para uma casa decimal
        df['Taxa'] = df['Taxa'].round(1)
        df['LIM_INF_OUT'] = df['LIM_INF_OUT'].round(1)
        df['LIM_SUP_OUT'] = df['LIM_SUP_OUT'].round(1)

        # Exibir o número de linhas e colunas do arquivo principal
        st.success(f"Arquivo principal carregado com sucesso! Tamanho: {df.shape[0]} linhas e {df.shape[1]} colunas.")
        
        st.title('Formulário Interativo para Sequência Operacional')

        # Carregar e exibir linhas do arquivo de referência
        if uploaded_reference is not None:
            df_reference = pd.read_excel(uploaded_reference)
            st.success("Arquivo de referência carregado com sucesso!")

            # Iterar sobre as linhas do DataFrame de referência
            for i, row in df_reference.iterrows():
                st.markdown(f"<div style='background-color: #008542; padding: 1px; margin-bottom: 10px; color: white; text-align: center;'>Linha {i + 1}</div>", unsafe_allow_html=True)

                # Grupos de amostras: "Com avanço" e "Sem avanço"
                for avancado in ["Com avanço", "Sem avanço"]:
                    st.markdown(f"<div style='background-color: #CCCCCC; padding: 5px; margin-top: 10px; color: #333333; text-align: center;'>Grupo: {avancado}</div>", unsafe_allow_html=True)

                    # Obter valores de filtro da linha do arquivo de referência
                    atividade = row.get('ATIVIDADE')
                    operacao = row.get('OPERACAO')
                    etapa = row.get('ETAPA')
                    fase = str(row.get('FASE'))  # Converter para string para garantir a compatibilidade
                    tipo_sonda = row.get('Tipo_sonda')
                    broca = [row.get('Diâmetro Broca')] if pd.notna(row.get('Diâmetro Broca')) else None
                    revestimento = [row.get('Diâmetro Revestimento')] if pd.notna(row.get('Diâmetro Revestimento')) else None

                    # Renderizar campos de seleção de filtros
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        atividade = st.selectbox(f'ATIVIDADE (Linha {i + 1}, {avancado}):', ['Todos'] + df['ATIVIDADE'].unique().tolist(), 
                                                 index=(df['ATIVIDADE'].unique().tolist().index(atividade) + 1) if atividade and atividade in df['ATIVIDADE'].unique() else 0)
                        if atividade == 'Todos':
                            atividade = None

                    with col2:
                        operacao = st.selectbox(f'OPERAÇÃO (Linha {i + 1}, {avancado}):', ['Todos'] + df['OPERACAO'].unique().tolist(), 
                                                index=(df['OPERACAO'].unique().tolist().index(operacao) + 1) if operacao and operacao in df['OPERACAO'].unique() else 0)
                        if operacao == 'Todos':
                            operacao = None

                    with col3:
                        etapa = st.selectbox(f'ETAPA (Linha {i + 1}, {avancado}):', ['Todos'] + df['ETAPA'].unique().tolist(), 
                                             index=(df['ETAPA'].unique().tolist().index(etapa) + 1) if etapa and etapa in df['ETAPA'].unique() else 0)
                        if etapa == 'Todos':
                            etapa = None

                    with col4:
                        fase = st.selectbox(f'FASE (Linha {i + 1}, {avancado}):', ['Todos'] + df['FASE'].unique().tolist(), 
                                            index=(df['FASE'].unique().tolist().index(fase) + 1) if fase and fase in df['FASE'].unique() else 0)
                        if fase == 'Todos':
                            fase = None

                    col5, col6, col7, col8 = st.columns(4)

                    with col5:
                        obz = st.selectbox(f'COM AVANÇO/SEM AVANÇO (Linha {i + 1}, {avancado}):', ['Todos'] + df['Obz'].unique().tolist(), 
                                           index=(df['Obz'].unique().tolist().index(avancado) + 1) if avancado and avancado in df['Obz'].unique() else 0)
                        if obz == 'Todos':
                            obz = None

                    with col6:
                        broca = st.multiselect(f'DIÂMETRO BROCA (Linha {i + 1}, {avancado}):', ['Todos'] + df['Diâmetro Broca'].unique().tolist(), default=broca or ['Todos'])
                        if 'Todos' in broca:
                            broca = None

                    with col7:
                        revestimento = st.multiselect(f'DIÂMETRO REVESTIMENTO (Linha {i + 1}, {avancado}):', ['Todos'] + df['Diâmetro Revestimento'].unique().tolist(), default=revestimento or ['Todos'])
                        if 'Todos' in revestimento:
                            revestimento = None

                    with col8:
                        tipo_sonda = st.multiselect(f'TIPO SONDA (Linha {i + 1}, {avancado}):', ['Todos'] + df['Tipo_sonda'].unique().tolist(), default=tipo_sonda or ['Todos'])
                        if 'Todos' in tipo_sonda:
                            tipo_sonda = None

                    # Aplicar filtro e exibir os dados
                    df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=avancado, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)
                    df_non_outliers = df_filtered[df_filtered['Outlier'] == False]
                    df_outliers = df_filtered[df_filtered['Outlier'] == True]

                    # Exibir o gráfico correspondente para cada grupo
                    if avancado == "Com avanço" and not df_filtered.empty:
                        plot_boxplot_with_plotly(df_filtered, 'Taxa', df_filtered['LIM_INF_OUT'].min(), df_filtered['LIM_SUP_OUT'].max(),
                                                 f'Boxplot de Taxa - Linha {i + 1}, Grupo Com avanço')
                    elif avancado == "Sem avanço" and not df_filtered.empty:
                        df_filtered.rename(columns={'TEMPO_TOTAL_HORAS': 'Tempo em horas'}, inplace=True)
                        plot_boxplot_with_plotly(df_filtered, 'Tempo em horas', df_filtered['LIM_INF_OUT'].min(), df_filtered['LIM_SUP_OUT'].max(),
                                                 f'Boxplot de Tempo em horas - Linha {i + 1}, Grupo Sem avanço')

                    # Exibir a quantidade de amostras sem e com outliers
                    st.markdown(
                        f"<div style='background-color: #E8F4FF; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #00008B; font-size: 18px; text-align: center;'>"
                        f"Quantidade de Amostras sem Outliers (Linha {i + 1}, {avancado}): <strong>{df_non_outliers.shape[0]}</strong>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.dataframe(df_non_outliers.reset_index(drop=True))

                    st.markdown(
                        f"<div style='background-color: #FFE8E8; padding: 10px; border-radius: 5px; margin: 20px 0 10px 0; color: #8B0000; font-size: 18px; text-align: center;'>"
                        f"Quantidade de Amostras com Outliers (Linha {i + 1}, {avancado}): <strong>{df_outliers.shape[0]}</strong>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                    st.dataframe(df_outliers.reset_index(drop=True))

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")

else:
    st.warning("Nenhum arquivo foi carregado. Por favor, faça o upload dos arquivos necessários.")

