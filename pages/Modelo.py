import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import joblib
from streamlit.components.v1 import html


st.set_page_config(page_title="Evasão de Alunos",
                   page_icon=":bar_chart:", layout="wide")

st.title("Previsão de Evasão de Alunos da Passos Mágicos :school:")

st.markdown("""
### Visualize e explore o modelo de previsão de evasão de alunos
Este aplicativo permite que você explore as métricas e previsões do modelo
que foi treinado para prever a evasão de alunos com base em várias características.
""")

tab1, tab2, tab3 = st.tabs(
    ["Previsão", "Contrução do Modelo 1", "Contrução do Modelo 2"])

with tab1:

    model = joblib.load('model.pkl')
    scaler = joblib.load('scaler.pkl')

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
