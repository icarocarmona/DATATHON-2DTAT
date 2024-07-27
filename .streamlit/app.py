import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="DataThon - Grupo 26",
    page_icon="⛽",
    initial_sidebar_state="expanded",
)

st.header('🪄 DataThon - Passos Mágicos | Grupo 26', divider='rainbow')


st.write("DataThon Fase 5 - Passos mágicos")

st.write("### Integrantes:")

intro_home = pd.DataFrame({
    "Nome": ["Beatriz Vieira", "Icaro Carmona", "Priscila de França"],
    "linkedin": ["https://www.linkedin.com/in/beatrizrvieira/", "https://www.linkedin.com/in/icarocarmona/", "https://www.linkedin.com/in/pridefranca/"],
})
st.dataframe(intro_home,
    column_config={
        "Nome": "Nome",
        "linkedin": st.column_config.LinkColumn("Linkedin URL")
    },
    use_container_width=True,
    hide_index=True,
)