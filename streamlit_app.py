import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    return df_filtered

# Função para gerar o boxplot com rótulos
def plot_boxplot_with_labels(data, column, lim_inf, lim_sup, title):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x=data[column], color='lightblue', flierprops={'marker': 'o', 'color': 'red'})
    median_value = data[column].median()
    
    # Adicionar rótulos para a mediana, limite inferior e limite superior
    plt.axvline(median_value, color='green', linestyle='--', label=f'Mediana: {median_value:.2f}')
    plt.axvline(lim_inf, color='blue', linestyle='--', label=f'Limite Inferior: {lim_inf:.2f}')
    plt.axvline(lim_sup, color='orange', linestyle='--', label=f'Limite Superior: {lim_sup:.2f}')
    
    plt.title(title)
    plt.xlabel(column)
    plt.legend()
    plt.grid()
    st.pyplot(plt.gcf())  # Mostrar o gráfico no Streamlit
    plt.close()

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

                    # Aplicar filtro e exibir os dados
                    df_filtered = filter_options(df, atividade=atividade, operacao=operacao, etapa=etapa, fase=fase, obz=avancado, broca=broca, revestimento=revestimento, tipo_sonda=tipo_sonda)
                    
                    # Remover colunas indesejadas
                    columns_to_drop = ['depth_range_start', 'depth_range_end', 'Tipo_avanço', 'Extensão']
                    df_filtered.drop(columns=columns_to_drop, inplace=True, errors='ignore')

                    # Exibir o gráfico correspondente para cada grupo
                    if avancado == "Com avanço" and not df_filtered.empty:
                        plot_boxplot_with_labels(df_filtered, 'Taxa', df_filtered['LIM_INF_OUT'].min(), df_filtered['LIM_SUP_OUT'].max(),
                                                 f'Boxplot de Taxa - Linha {i + 1}, Grupo Com avanço')
                    elif avancado == "Sem avanço" and not df_filtered.empty:
                        df_filtered.rename(columns={'TEMPO_TOTAL_HORAS': 'Tempo em horas'}, inplace=True)
                        plot_boxplot_with_labels(df_filtered, 'Tempo em horas', df_filtered['LIM_INF_OUT'].min(), df_filtered['LIM_SUP_OUT'].max(),
                                                 f'Boxplot de Tempo em horas - Linha {i + 1}, Grupo Sem avanço')

                    # Exibir as amostras filtradas
                    st.dataframe(df_filtered.reset_index(drop=True))

    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar o arquivo: {e}")

else:
    st.warning("Nenhum arquivo foi carregado. Por favor, faça o upload dos arquivos necessários.")
