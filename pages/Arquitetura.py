import streamlit as st

# Title da página
st.set_page_config(
    page_title="Passos Mágicos | DataThon - Grupo 26",
    page_icon="🪄",
    initial_sidebar_state="expanded",
    layout= 'wide'
)

# Páginas
cols = st.columns(6, gap="large")
with cols[0]:
    st.image("https://passosmagicos.org.br/wp-content/uploads/2020/10/Passos-magicos-icon-cor.png")
with cols[1]:
    if st.button("Home"):
        st.switch_page("Home.py")
with cols[2]:
    if st.button("Passos Mágicos"):
        st.switch_page("pages/A Ong Passos Mágicos.py")
with cols[3]:
    if st.button("Análises"):
        st.switch_page("pages/Análises.py")
with cols[4]:
    if st.button("Arquitetura"):
        st.switch_page("pages/Arquitetura.py")
with cols[5]:
    if st.button("Modelo"):
        st.switch_page("pages/Modelo.py")

# Título Análises
st.header(':gear: Arquitetura do Projeto', divider='rainbow')

st.image("imagens/Arquitetura.png", caption="Arquitetura do projeto")
st.markdown("""
> Neste projeto, decidimos utilizar um banco de dados para facilitar a modelagem e limpeza dos dados, além de trabalhar em equipe de forma mais ágil e colaborativa.

### Repositório
A organização do projeto está estruturada da seguinte forma:

- imagens: Contém as imagens utilizadas no projeto;
- notebooks: Todo o processo exploratório e desenvolvimento dos modelos estão documentados aqui;
- pages: Páginas do Streamlit;
- sql: Todas as consultas e criação de novas tabelas/views estão aqui.

### Ferramentas, Frameworks e Bibliotecas

#### Arquivos
Recebemos todos os arquivos do Passos Mágicos em formato CSV através do Google Drive. Decidimos não hospedar os dados neste repositório.

#### Neon
Como precisávamos de uma ferramenta gratuita para hospedar um banco de dados, encontramos o Neon, que fornece gratuitamente uma versão de PostgreSQL que atende às necessidades do nosso projeto.

#### Streamlit
Esta ferramenta foi escolhida para entregar toda a análise visual.

### Scikit-Learn
Utilizamos o Scikit-Learn para a criação do modelo de Regressão Logística.
""")
