import streamlit as st

st.set_page_config(page_title="Arquitetura do Projeto", page_icon=":gear:")

st.title("Arquitetura do Projeto :gear:")
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
