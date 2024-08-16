# Importações
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wordcloud import WordCloud

# Title da página
st.set_page_config(
    page_title="Passos Mágicos | DataThon - Grupo 26",
    page_icon="🪄",
    initial_sidebar_state="expanded",
)

# Título Análises
st.header('🪄 Análise Exploratória', divider='rainbow')

# Criando a conexão com o BD
def create_conn():
    # Defina os parâmetros de conexão
    db_user = st.secrets["DB_USER"]
    db_password = st.secrets["DB_PASSWORD"]
    db_host = st.secrets["DB_HOST"]
    db_port = '5432'
    db_name = 'magic-steps'

    # Crie a URL de conexão
    connection_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    # Crie um engine do SQLAlchemy
    engine = create_engine(connection_url)
    return engine


engine = create_conn()
# Fim conexão BD

# ------- Início Análises -------

# Criando as abas
tab1, tab2, tab3 = st.tabs(["Gráficos", "Conclusão", "Sugestão"])

# tab1 - Gráficos
with tab1:
    # Tabela 1 - Defina a consulta SQL para a view
    query = 'SELECT * FROM magic_steps.inativos_full'

    # Execute a consulta e carregue os resultados em um DataFrame
    df_inativos_full = pd.read_sql(query, engine)

    # Mostre as primeiras linhas do DataFrame em uma tabela no Streamlit
    #st.dataframe(df_inativos_full.head())

    # Se quiser mostrar toda a tabela:
    st.dataframe(df_inativos_full)

    # Gráfico 2 - Distribuição dos Motivos de Inativação

    st.write("### Distribuição dos Motivos de Inativação")

    # Conte as ocorrências de cada motivo de inativação
    reason_counts = df_inativos_full['motivoinativacao'].value_counts()

    # Plot as ocorrências de cada motivo de inativação
    fig = plt.figure(figsize=(10, 6))
    reason_counts.plot(kind='bar')
    plt.title('Distribuição dos Motivos de Inativação')
    plt.xlabel('Motivo de Inativação')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    st.pyplot(fig)

    st.write("**Motivos de inativação entre os alunos:**")

    st.markdown("""
    - Mudou de bairro/Cidade/Distância
    - Outras prioridades/trabalho: Este é o motivo mais frequente para a inativação dos alunos. Isso sugere que muitos estudantes estão priorizando o trabalho ou outras atividades sobre seus estudos.
    - Sem adaptação ao curso: Outro motivo comum, indicando que alguns alunos podem não ter se ajustado bem ao curso ou à instituição.
    - Desistência por motivos pessoais: Reflete que questões pessoais são uma razão significativa para alguns alunos deixarem o curso.
    - Problemas financeiros: Também aparece com frequência, indicando que dificuldades econômicas têm um impacto considerável na continuidade dos estudos.
    """)

    st.write("Este gráfico ajuda a entender melhor os desafios enfrentados pelos alunos e pode auxiliar na formulação de estratégias para reduzir as taxas de inativação, como suporte financeiro, aconselhamento acadêmico e ajustes curriculares.")

    # Tabela 3 - Relação Aluno x Turma

    st.write("### Relação Aluno x Turma")

    # Ler as tabelas do PostgreSQL para dataframes pandas
    tbsituacaoalunoturma_m = pd.read_sql_table('tbsituacaoalunoturma_m', con=engine, schema='magic_steps')
    tbalunoturma = pd.read_sql_table('tbalunoturma', con=engine, schema='magic_steps')

    # Fazer o join entre os dataframes
    merged_df = pd.merge(tbsituacaoalunoturma_m, tbalunoturma, left_on='IdSituacaoAlunoTurma', right_on='IdSituacaoAlunoTurma')

    # Filtrar os dados conforme a condição especificada
    filtered_df = merged_df[merged_df['SituacaoSistema'] != 'P']

    # Converter a coluna de data para datetime e extrair o ano
    filtered_df['DataSituacaoAtivo'] = pd.to_datetime(filtered_df['DataSituacaoAtivo'])
    filtered_df['ano'] = filtered_df['DataSituacaoAtivo'].dt.year

    # Agrupar pelos campos necessários e contar
    grouped_df = filtered_df.groupby(['SituacaoAlunoTurma', 'ano']).size().reset_index(name='count')

    # Ordenar por ano em ordem decrescente
    result_df = grouped_df.sort_values(by='ano', ascending=False)

    # Mostrar o resultado como uma tabela no Streamlit
    st.dataframe(result_df)

    st.write("Pode haver mais de um aluno por situação aluno turma, ou seja, um aluno pode estar em mais de um tipo de Situação.")

    # Gráfico 4 - Tendências de Situação dos Alunos ao Longo dos Anos
    st.write("### Tendências de Situação dos Alunos ao Longo dos Anos")

    # Análise de tendências
    fig, ax = plt.subplots(figsize=(12, 8))

    # Criar o gráfico de barras empilhadas usando o dataframe pivotado
    pivot_df = result_df.pivot(index='ano', columns='SituacaoAlunoTurma', values='count')
    pivot_df.plot(kind='bar', stacked=True, ax=ax)

    # Adicionar rótulos e título
    ax.set_xlabel('Ano')
    ax.set_ylabel('Número de Alunos')
    ax.set_title('Tendências de Situação dos Alunos ao Longo dos Anos')

    # Configurar a legenda, rotação dos rótulos do eixo x, e a grade
    ax.legend(title='Situação do Aluno')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.grid(True)

    st.pyplot(fig)

    # Tabela 5 - 

    # Defina a consulta SQL para a view
    query = 'SELECT * FROM magic_steps.vw_aluno_obs_v2'

    # Execute a consulta e carregue os resultados em um DataFrame
    df_v2 = pd.read_sql(query, engine)

    # Mostrar as primeiras linhas do DataFrame no Streamlit
    st.dataframe(df_v2.head())

    # Se você quiser exibir todo o DataFrame:
    # st.dataframe(df_v2)

    # Tabela 6 - 

    # Defina a consulta SQL para a view
    # query = 'SELECT * FROM magic_steps.vw_aluno_obs_v2'

    # Execute a consulta e carregue os resultados em um DataFrame
    # df_v2 = pd.read_sql(query, engine)

    # Mostrar as primeiras linhas do DataFrame no Streamlit
    # st.dataframe(df_v2.head())

    # Se quiser exibir todo o DataFrame no Streamlit:
    # st.dataframe(df_v2)

    # Gráfico 7 - Nuvem de palavras - Desistentes

    st.write("### Nuvem de Palavras - Desistente")

    # Filtrar registros onde SituacaoAlunoTurma é 'Desistente'
    desistente_records = df_v2[df_v2['SituacaoAlunoTurma'] == 'Desistente']

    # Concatenar textos da coluna ObservacaoRegistro
    text = ' '.join(desistente_records['ObservacaoRegistro'].dropna())

    # Gerar a nuvem de palavras
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

    # Configurar o gráfico para exibir a nuvem de palavras
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Nuvem de Palavras - Desistente')

    # Exibir a nuvem de palavras no Streamlit
    st.pyplot(fig)

    # Gráfico 8 - Motivos de Inativação dos Alunos

    st.write("### Motivos de Inativação dos Alunos")

    # Process the data for gender and race distribution
    gender_distribution = df_v2['Sexo'].value_counts()
    race_distribution = df_v2['CorRaca'].value_counts()

    # Process the data for reasons of inactivation
    inactivation_reasons = df_v2['MotivoInativacao'].value_counts()

    # Plotting reasons for inactivation
    fig = plt.figure(figsize=(12, 6))
    inactivation_reasons.plot(kind='bar')
    plt.title('Motivos de Inativação dos Alunos')
    plt.xlabel('Motivo de Inativação')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)

    # Gráfico 9 - Mudanças de Situação ao Longo do Tempo (DataOcorrencia)

    st.write("### Mudanças de Situação ao Longo do Tempo (DataOcorrencia)")

    # Converter as colunas de data para o formato datetime
    df_v2['DataOcorrencia'] = pd.to_datetime(df_v2['DataOcorrencia'], errors='coerce')
    df_v2['DataInclusao'] = pd.to_datetime(df_v2['DataInclusao'], errors='coerce')

    # Contar a quantidade de mudanças de situação ao longo do tempo usando 'DataOcorrencia'
    ocorrencia_counts = df_v2.groupby(df_v2['DataOcorrencia'].dt.to_period('M'))['SituacaoAlunoTurma'].count()

    # Criar gráfico de linha para visualizar as mudanças de situação ao longo do tempo
    fig = plt.figure(figsize=(12, 6))
    ocorrencia_counts.plot(kind='line')
    plt.title('Mudanças de Situação ao Longo do Tempo (DataOcorrencia)')
    plt.xlabel('Data')
    plt.ylabel('Quantidade de Mudanças')
    plt.xticks(rotation=45)
    plt.grid(True)

    st.pyplot(fig)

    st.write("Insights sobre Mudanças de Situação ao Longo do Tempo O gráfico acima mostra a quantidade de mudanças de situação ao longo do tempo, utilizando a coluna DataOcorrencia:")

    st.write("Flutuações Regulares: É possível observar picos e vales na quantidade de mudanças de situação. Esses picos podem corresponder a períodos críticos no calendário acadêmico, como finais de semestre ou ano letivo.")

    st.write("Tendências Temporais: Algumas épocas do ano podem apresentar mais mudanças, o que pode estar associado a fatores externos, como feriados ou processos administrativos.")

    st.write("Possíveis Intervenções: Identificar esses períodos pode ser útil para implementar intervenções direcionadas, como campanhas de retenção ou suporte adicional para alunos em risco de desistência.")


# -----------------------------------------------------------------------------------

# tab2 - Conclusão
with tab2:
    st.write("""Com as análises, podemos concluir que a Passos Mágicos possui fatores importantes que contribuem para a desistência dos alunos. 
    A implementação de estratégias nas áreas de apoio financeiro, flexibilidade nos horários, suporte psicopedagógico, e envolvimento comunitário pode reduzir a taxa de evasão. Recomendamos que a Associação adote medidas para fortalecer o suporte oferecido aos alunos, garantindo maior retenção e sucesso acadêmico. O compromisso contínuo com a inovação e o apoio individualizado será essencial para transformar ainda mais a vida de crianças e jovens de baixa renda, assegurando-lhes melhores oportunidades de futuro.
    """)

# -----------------------------------------------------------------------------------

# tab3 - Sugestãoo
with tab3:
    st.write(""" Os principais motivos para a inativação dos alunos incluem mudanças de residência que dificultam o acesso à instituição, 
    a priorização de outras atividades ou trabalho em detrimento dos estudos, dificuldades de adaptação ao curso ou à instituição,
     questões pessoais que levaram à desistência, e problemas financeiros que afetam a continuidade dos estudos. Para reduzir a evasão e melhorar a retenção dos alunos, recomendamos as seguintes ações:

**Programas de Apoio Financeiro:**
     - Estabelecimento de um fundo de emergência para auxiliar estudantes que enfrentam crises financeiras temporárias.

**Flexibilidade nos Horários:**
   - Oferecer cursos noturnos e de fim de semana.
   - Expandir o acesso a aulas e materiais online (EAD).

**Envolvimento Familiar e Comunitário:**
   - Promover programas de envolvimento dos pais e atividades comunitárias.
   - Estabelecer parcerias com comunidades locais.

**Diversificação de Atividades e Currículo:**
   - Oferecer atividades extracurriculares atraentes.
   - Customizar o currículo para atender às necessidades individuais dos alunos.
""")
# -----------------------------------------------------------------------------------
