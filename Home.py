# Importações
import streamlit as st
import pandas as pd

# Title da página
st.set_page_config(
    page_title="DataThon - Grupo 26",
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

# Apresentação e integrantes
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