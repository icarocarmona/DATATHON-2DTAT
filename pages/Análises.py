# Importações
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
    # Defina a consulta SQL para a view
    query = 'SELECT * FROM magic_steps.inativos_full'

    # Execute a consulta e carregue os resultados em um DataFrame
    df_inativos_full = pd.read_sql(query, engine)

    # Título gráfico - Distribuição dos Motivos de Inativação
    st.write("### Distribuição dos Motivos de Inativação")

    # Conte as ocorrências de cada motivo de inativação
    reason_counts = df_inativos_full['motivoinativacao'].value_counts()

    # Plote a distribuição dos motivos de inativação
    fig = plt.figure(figsize=(10, 6))
    reason_counts.plot(kind='bar')
    plt.title('Distribuição dos Motivos de Inativação')
    plt.xlabel('Motivo de Inativação')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Exibindo o gráfico no Streamlit
    st.pyplot(fig)

    # Título gráfico - Desempenho Médio por Disciplina
    st.write("### dDesempenho Médio por Disciplina")

    # Calcule a média de notas por disciplina
    average_grade_per_discipline = df_inativos_full.groupby(
        'nomedisciplina')['notafase'].mean().sort_values(ascending=False)

    # Plote as médias de notas por disciplina
    fig = plt.figure(figsize=(10, 6))
    average_grade_per_discipline.plot(kind='bar')
    plt.title('Desempenho Médio por Disciplina')
    plt.xlabel('Disciplina')
    plt.ylabel('Nota Média')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    st.pyplot(fig)

    st.write("**Outras prioridades/trabalho:** Este é o motivo mais frequente para a inativação dos alunos. Isso sugere que muitos estudantes estão priorizando o trabalho ou outras atividades sobre seus estudos.")

    st.write("**Sem adaptação ao curso:** Outro motivo comum, indicando que alguns alunos podem não ter se ajustado bem ao curso ou à instituição.")

    st.write("**Desistência por motivos pessoais:** Reflete que questões pessoais são uma razão significativa para alguns alunos deixarem o curso.")

    st.write("**Problemas financeiros:** Também aparece com frequência, indicando que dificuldades econômicas têm um impacto considerável na continuidade dos estudos.")

    st.write("Este gráfico ajuda a entender melhor os desafios enfrentados pelos alunos e pode auxiliar na formulação de estratégias para reduzir as taxas de inativação, como suporte financeiro, aconselhamento acadêmico e ajustes curriculares.")

    # Título gráfico - Distribuição dos Alunos por Situação ao Longo dos Anos
    st.write("### Distribuição dos Alunos por Situação ao Longo dos Anos")

    # Ler as tabelas do PostgreSQL para dataframes pandas
    tbsituacaoalunoturma_m = pd.read_sql_table(
        'tbsituacaoalunoturma_m', con=engine, schema='magic_steps')
    tbalunoturma = pd.read_sql_table(
        'tbalunoturma', con=engine, schema='magic_steps')

    # Fazer o join entre os dataframes
    merged_df = pd.merge(tbsituacaoalunoturma_m, tbalunoturma,
                         left_on='IdSituacaoAlunoTurma', right_on='IdSituacaoAlunoTurma')

    # Filtrar os dados conforme a condição especificada
    filtered_df = merged_df[merged_df['SituacaoSistema'] != 'P']

    # Converter a coluna de data para datetime e extrair o ano
    filtered_df['DataSituacaoAtivo'] = pd.to_datetime(
        filtered_df['DataSituacaoAtivo'])
    filtered_df['ano'] = filtered_df['DataSituacaoAtivo'].dt.year

    # Agrupar pelos campos necessários e contar
    grouped_df = filtered_df.groupby(
        ['SituacaoAlunoTurma', 'ano']).size().reset_index(name='count')

    # Ordenar por ano em ordem decrescente
    result_df = grouped_df.sort_values(by='ano', ascending=False)

    # Plotar a distribuição dos alunos por situação ao longo dos anos
    fig = plt.figure(figsize=(12, 8))
    for situacao in result_df['SituacaoAlunoTurma'].unique():
        subset = result_df[result_df['SituacaoAlunoTurma'] == situacao]
        plt.plot(subset['ano'], subset['count'], label=situacao)

    plt.xlabel('Ano')
    plt.ylabel('Número de Alunos')
    plt.title('Distribuição dos Alunos por Situação ao Longo dos Anos')
    plt.legend()
    plt.grid(True)

    st.pyplot(fig)

    # Título gráfico - Tendências de Situação dos Alunos ao Longo dos Anos
    st.write("### Tendências de Situação dos Alunos ao Longo dos Anos")

    pivot_df = result_df.pivot(
        index='ano', columns='SituacaoAlunoTurma', values='count')

    fig, ax = plt.subplots(figsize=(12, 8))
    pivot_df.plot(kind='bar', stacked=True, ax=ax)

    plt.xlabel('Ano')
    plt.ylabel('Número de Alunos')
    plt.title('Tendências de Situação dos Alunos ao Longo dos Anos')
    plt.legend(title='Situação do Aluno')
    plt.xticks(rotation=45)
    plt.grid(True)

    st.pyplot(fig)

    # Título gráfico - Comparação Entre Situações de Alunos
    st.write("### Comparação Entre Situações de Alunos")

    # Comparação entre situações
    fig = plt.figure(figsize=(12, 8))
    result_df.groupby('SituacaoAlunoTurma')['count'].sum().plot(kind='bar')

    plt.xlabel('Situação do Aluno')
    plt.ylabel('Total de Alunos')
    plt.title('Comparação Entre Situações de Alunos')
    plt.xticks(rotation=45)
    plt.grid(True)

    st.pyplot(fig)

    # Conexão BD para gráficos seguintes

    # Conectar ao banco de dados e ler as tabelas
    engine = create_conn()
    tbsituacaoalunoturma_m = pd.read_sql_table(
        'tbsituacaoalunoturma_m', con=engine, schema='magic_steps')
    tbalunoturma = pd.read_sql_table(
        'tbalunoturma', con=engine, schema='magic_steps')

    # Fazer o join entre os dataframes
    merged_df = pd.merge(tbsituacaoalunoturma_m, tbalunoturma,
                         left_on='IdSituacaoAlunoTurma', right_on='IdSituacaoAlunoTurma')

    # Filtrar os dados conforme a condição especificada
    filtered_df = merged_df[merged_df['SituacaoSistema'] != 'P']

    # Converter a coluna de data para datetime e extrair o ano
    filtered_df['DataSituacaoAtivo'] = pd.to_datetime(
        filtered_df['DataSituacaoAtivo'])
    filtered_df['ano'] = filtered_df['DataSituacaoAtivo'].dt.year

    # Filtrar apenas os "Desistentes"
    desistentes_df = filtered_df[filtered_df['SituacaoAlunoTurma']
                                 == 'Desistente']

    # Agrupar pelos campos necessários e contar
    grouped_df = desistentes_df.groupby(
        ['SituacaoAlunoTurma', 'ano']).size().reset_index(name='count')

    # Ordenar por ano em ordem decrescente
    result_df = grouped_df.sort_values(by='ano', ascending=False)

    # Título gráfico - Distribuição dos Desistentes ao Longo dos Anos
    st.write("### Distribuição dos Desistentes ao Longo dos Anos")

    # Plotar a distribuição dos desistentes ao longo dos anos
    fig = plt.figure(figsize=(12, 8))
    for situacao in result_df['SituacaoAlunoTurma'].unique():
        subset = result_df[result_df['SituacaoAlunoTurma'] == situacao]
        plt.plot(subset['ano'], subset['count'], label=situacao)

    plt.xlabel('Ano')
    plt.ylabel('Número de Alunos')
    plt.title('Distribuição dos Desistentes ao Longo dos Anos')
    plt.legend()
    plt.grid(True)

    st.pyplot(fig)

    # Título gráfico - Tendências de Desistentes ao Longo dos Anos
    st.write("### Tendências de Desistentes ao Longo dos Anos")

    # Análise de tendências
    pivot_df = result_df.pivot(
        index='ano', columns='SituacaoAlunoTurma', values='count')

    fig, ax = plt.subplots(figsize=(12, 8))
    pivot_df.plot(kind='bar', stacked=True, ax=ax)

    plt.xlabel('Ano')
    plt.ylabel('Número de Alunos')
    plt.title('Tendências de Desistentes ao Longo dos Anos')
    plt.legend(title='Situação do Aluno')
    plt.grid(True)

    st.pyplot(fig)

    # Título gráfico - Comparação de Desistentes Entre os Anos
    st.write("### Comparação de Desistentes Entre os Anos")

    # Comparação entre anos
    fig = plt.figure(figsize=(12, 8))
    result_df.groupby('ano')['count'].sum().plot(kind='bar')

    plt.xlabel('Ano')
    plt.ylabel('Total de Desistentes')
    plt.title('Comparação de Desistentes Entre os Anos')
    plt.grid(True)

    st.pyplot(fig)

    # Defina a consulta SQL para a view
    query = 'SELECT * FROM magic_steps.vw_aluno_obs'

    # Execute a consulta e carregue os resultados em um DataFrame
    df = pd.read_sql(query, engine)

    # Processar os dados para distribuição de gênero e raça
    gender_distribution = df['Sexo'].value_counts()
    race_distribution = df['CorRaca'].value_counts()

    # Processar os dados para motivos de inativação
    inactivation_reasons = df['MotivoInativacao'].value_counts()

    # Título gráfico - Distribuição de Gênero dos Alunos
    st.write("### Distribuição de Gênero dos Alunos")

    # Plotar a distribuição de gênero
    fig = plt.figure(figsize=(10, 5))
    gender_distribution.plot(kind='bar')
    plt.title('Distribuição de Gênero dos Alunos')
    plt.xlabel('Gênero')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=0)

    st.pyplot(fig)

    st.write("A distribuição de gênero entre os alunos parece ser equilibrada, com uma representação significativa tanto de alunos do sexo masculino quanto do sexo feminino.")

    # Título gráfico - Distribuição de Cor/Raça dos Alunos
    st.write("### Distribuição de Cor/Raça dos Alunos")

    # Plotar a distribuição de raça
    fig = plt.figure(figsize=(10, 5))
    race_distribution.plot(kind='bar')
    plt.title('Distribuição de Cor/Raça dos Alunos')
    plt.xlabel('Cor/Raça')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=0)

    st.pyplot(fig)

    st.write("A maioria dos alunos se identifica com uma cor/raça específica representada pelo código B no gráfico, o que pode indicar a predominância de um grupo racial na amostra.")

    # Título gráfico - Motivos de Inativação dos Alunos
    st.write("### Motivos de Inativação dos Alunos")

    # Plotar os motivos de inativação
    fig = plt.figure(figsize=(12, 6))
    inactivation_reasons.plot(kind='bar')
    plt.title('Motivos de Inativação dos Alunos')
    plt.xlabel('Motivo de Inativação')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)

    st.write("O motivo mais comum para a inativação dos alunos é Falta de retorno às nossas tentativas de contato, seguido por Conflito com horário escolar / período integral. Isso sugere que a comunicação e a compatibilidade de horários são áreas críticas que precisam de atenção.")

    # Título gráfico - Situações dos Alunos nas Turmas
    st.write("### Situações dos Alunos nas Turmas")

    # Analisando as situações dos alunos nas aulas
    student_situations = df['IdSituacaoAlunoTurma'].value_counts()

    # Plotar a distribuição das situações dos alunos nas aulas
    fig = plt.figure(figsize=(10, 5))
    student_situations.plot(kind='bar')
    plt.title('Situações dos Alunos nas Turmas')
    plt.xlabel('ID da Situação do Aluno na Turma')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=0)

    st.pyplot(fig)

    # Verificando se há códigos de situação específicos com os comentários, se disponíveis
    unique_situations_with_comments = df[[
        'IdSituacaoAlunoTurma', 'ComentarioInativacao']].dropna().drop_duplicates()

    unique_situations_with_comments.head()

    st.write("**A análise das situações dos alunos nas turmas revela o seguinte:**")

    st.write("**Distribuição das Situações:**")

    st.write("A maioria dos alunos está associada a um único código de situação, que é o 14. Esse código representa uma categoria comum de situação dos alunos em suas respectivas turmas.")

    st.write("**Comentários Associados:**")

    st.write("Para algumas situações, existem comentários adicionais que fornecem contexto. Por exemplo:")

    st.write("Situação 14 está associada a comentários sobre Retorno das aulas na escola para o presencial e Falta de condições financeiras para o transporte.")

    st.write("Situação 19 tem comentários como Alfa N - 1N e Vide ocorrência, indicando reavaliações ou referências a outras ocorrências.")

    st.write("Essas informações podem ser úteis para entender melhor as razões por trás das situações dos alunos nas turmas e ajudar a identificar áreas onde intervenções ou suporte adicional podem ser necessários.")

    # Comparando as situações dos alunos com dados demográficos: gênero e raça.
    situation_gender = df.groupby(
        ['IdSituacaoAlunoTurma', 'Sexo']).size().unstack().fillna(0)
    situation_race = df.groupby(
        ['IdSituacaoAlunoTurma', 'CorRaca']).size().unstack().fillna(0)

    # Título gráfico - Situações dos Alunos nas Turmas por Gênero
    st.write("### Situações dos Alunos nas Turmas por Gênero")

    # Plotar a comparação entre as situações dos alunos e o gênero
    fig, ax = plt.subplots(figsize=(12, 8))
    situation_gender.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Situações dos Alunos nas Turmas por Gênero')
    plt.xlabel('ID da Situação do Aluno na Turma')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=0)
    plt.legend(title='Gênero')

    st.pyplot(fig)

    # Título gráfico - Situações dos Alunos nas Turmas por Cor/Raça
    st.write("### Situações dos Alunos nas Turmas por Cor/Raça")

    # Plotar a comparação entre as situações dos alunos e a raça
    fig, ax = plt.subplots(figsize=(12, 8))
    situation_race.plot(kind='bar', stacked=True, ax=ax)
    plt.title('Situações dos Alunos nas Turmas por Cor/Raça')
    plt.xlabel('ID da Situação do Aluno na Turma')
    plt.ylabel('Número de Alunos')
    plt.xticks(rotation=0)
    plt.legend(title='Cor/Raça')

    st.pyplot(fig)

    st.write("**A análise das situações dos alunos nas turmas em relação aos dados demográficos de gênero e cor/raça revela o seguinte:**")

    st.write("**Situações por Gênero:**")

    st.write("Para a situação mais comum, código 14, há um equilíbrio na distribuição entre alunos do sexo masculino e feminino.")

    st.write("Para outras situações, como o código 19, a distribuição também parece relativamente equilibrada, indicando que as questões que afetam as situações dos alunos não são fortemente influenciadas pelo gênero.")

    st.write("**Situações por Cor/Raça:**")

    st.write("A maioria das situações, especialmente o código 14, está associada ao grupo racial predominante, código B.")

    st.write("Isso reflete a distribuição geral de raça/cor no conjunto de dados, sem grandes desvios em termos de situação acadêmica.")

# -----------------------------------------------------------------------------------

# tab2 - Conclusão
with tab2:
    st.write("""Com as análises, podemos concluir que a Passos Mágicos possui fatores importantes que contribuem para a desistência dos alunos. 
    A implementação de estratégias nas áreas de apoio financeiro, flexibilidade nos horários, suporte psicopedagógico, e envolvimento comunitário pode reduzir a taxa de evasão. Recomendamos que a Associação adote medidas para fortalecer o suporte oferecido aos alunos, garantindo maior retenção e sucesso acadêmico. O compromisso contínuo com a inovação e o apoio individualizado será essencial para transformar ainda mais a vida de crianças e jovens de baixa renda, assegurando-lhes melhores oportunidades de futuro.
    """)

# -----------------------------------------------------------------------------------

# tab3 - Sugestãoo
with tab3:
    st.write("""
Os principais motivos identificados para a inativação dos alunos foram:

**Mudou de bairro/cidade/distância:** Mudanças de residência que dificultam o acesso à instituição.

**Outras prioridades/trabalho:** Este é o motivo mais frequente, indicando que muitos estudantes estão priorizando o trabalho ou outras atividades sobre os estudos.

**Sem adaptação ao curso:** Alguns alunos não se ajustaram bem ao curso ou à instituição.

**Desistência por motivos pessoais:** Questões pessoais significativas que levaram alguns alunos a deixar o curso.

**Problemas financeiros:** Dificuldades econômicas que têm um impacto considerável na continuidade dos estudos.

Para reduzir a evasão e melhorar a retenção dos alunos, recomendamos as seguintes ações:

**Programas de Apoio Financeiro:**
   - Criação de bolsas de estudo e subsídios para alunos em situação de vulnerabilidade econômica.
   - Estabelecimento de um fundo de emergência para auxiliar estudantes que enfrentam crises financeiras temporárias.

**Flexibilidade nos Horários:**
   - Oferecer cursos noturnos e de fim de semana.
   - Expandir o acesso a aulas e materiais online (EAD).

**Suporte Psicopedagógico:**
   - Implementar um programa de mentoria e aconselhamento.
   - Disponibilizar acompanhamento psicológico e pedagógico.

**Envolvimento Familiar e Comunitário:**
   - Promover programas de envolvimento dos pais e atividades comunitárias.
   - Estabelecer parcerias com comunidades locais.

**Diversificação de Atividades e Currículo:**
   - Oferecer atividades extracurriculares atraentes.
   - Customizar o currículo para atender às necessidades individuais dos alunos.
""")
# -----------------------------------------------------------------------------------