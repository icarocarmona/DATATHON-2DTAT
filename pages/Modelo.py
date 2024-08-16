import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import joblib
from streamlit.components.v1 import html

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
st.header(':school: Previsão de Evasão de Alunos da Passos Mágicos', divider='rainbow')

st.markdown("""
### Visualize e explore o modelo de previsão de evasão de alunos
Este aplicativo permite que você explore as métricas e previsões do modelo
que foi treinado para prever a evasão de alunos com base em várias características.
""")

tab1, tab2, tab3 = st.tabs(
    ["Previsão", "Contrução do Modelo 1", "Contrução do Modelo 2"])

with tab1:

    model = joblib.load('./model.pkl')
    scaler = joblib.load('./scaler.pkl')

    def prever_evasao(idade, notafase, numerofase, diasmatriculado):
        novo_dado = pd.DataFrame({
            'idade': [idade],
            'notafase': [notafase],
            'numerofase': [numerofase],
            'diasmatriculado': [diasmatriculado]
        })
        novo_dado_scaled = scaler.transform(novo_dado)
        previsao = model.predict(novo_dado_scaled)
        probabilidade = model.predict_proba(novo_dado_scaled)
        return previsao[0], probabilidade

    st.title('Previsão de Evasão de Alunos')

    with st.form(key='form'):
        idade = st.number_input('Idade', min_value=0)
        notafase = st.number_input(
            'Nota da Fase', min_value=0.0, format="%.1f")
        numerofase = st.number_input('Número da Fase', min_value=0)
        diasmatriculado = st.number_input('Dias Matriculado', min_value=0)

        submit_button = st.form_submit_button('Prever')

        if submit_button:
            previsao, probabilidade = prever_evasao(
                idade, notafase, numerofase, diasmatriculado)

            if previsao == 1:
                st.write("O modelo prevê que o aluno ficará inativo.")
            else:
                st.write("O modelo prevê que o aluno não ficará inativo.")

            st.write(
                f"Probabilidade de não inativo: {probabilidade[0][0]:.2f}")
            st.write(f"Probabilidade de inativo: {probabilidade[0][1]:.2f}")


with tab2:
    # Ler o conteúdo do arquivo HTML
    with open('html/Construindo_modelo_1.html', 'r') as file:
        html_content = file.read()

    # Exibir o HTML no Streamlit
    st.markdown("""
    ### Notebook em formato HTML
    >Convertemos o notebook para facilitar a visualização.
    """)
    html(html_content, height=800, scrolling=True)

with tab3:

    # Ler o conteúdo do arquivo HTML
    with open('html/Construindo_modelo_2.html', 'r') as file:
        html_content = file.read()

    # Exibir o HTML no Streamlit
    st.markdown("""
    ### Notebook em formato HTML
    >Convertemos o notebook para facilitar a visualização.
    """)
    html(html_content, height=800, scrolling=True)
