# Importações
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

# Sobre a PM
st.header('🪄 Sobre a Passos Mágicos', divider='rainbow')

# Criando as abas
tab1, tab2, tab3 = st.tabs(["Como funciona a Passos Mágicos", "O que fazem", "Objetivo"])

# tab1 - Como funciona a Passos Mágicos
with tab1:
    st.image("https://passosmagicos.org.br/wp-content/uploads/2020/10/Passos-magicos-icon-cor.png", use_column_width=True)

    st.write("A Associação Passos Mágicos possui uma trajetória de 30 anos, dedicando-se a transformar a vida de crianças e jovens de baixa renda, oferecendo-lhes melhores oportunidades de futuro.")

    st.write("Esta transformação, iniciada por Michelle Flues e Dimetri Ivanoff, começou em 1992 com atividades em orfanatos no município de Embu-Guaçu.")

    st.write("Em 2016, após muitos anos de trabalho, decidiram ampliar o programa para que mais jovens pudessem beneficiar-se dessa fórmula mágica de transformação, que abrange: educação de qualidade, apoio psicológico/psicopedagógico, expansão de sua visão de mundo e protagonismo. Dessa forma, passaram a atuar como um projeto social e educacional, estabelecendo a Associação Passos Mágicos.")

# tab2 - O que fazem
with tab2:
    st.write("A Passos Mágicos oferece um ensino de qualidade para crianças e jovens de Embu-Guaçu - SP. Contando e aplicando os métodos listados abaixo:")
    st.markdown("""
    - Aceleração do Conhecimento
    - Programas especiais
    - Eventos e ações sociais
    - Parceiros e apoiadores
    """)

# tab3 - Objetivo
with tab3:
        st.write("O objetivo da Passos Mágicos é impactar a vida de jovens e crianças, oferecendo meios para que alcancem melhores oportunidades.")

        st.write("O ideal da Passos Mágicos é um Brasil onde todas as crianças e jovens tenham oportunidades iguais para realizarem seus sonhos e se tornem protagonistas de suas próprias histórias.")