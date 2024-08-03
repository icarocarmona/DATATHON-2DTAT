# Importações
import streamlit as st

# Title da página
st.set_page_config(
    page_title="Passos Mágicos | DataThon - Grupo 26",
    page_icon="🪄",
    initial_sidebar_state="expanded",
)

# Sobre a PM
st.header('🪄 Sobre a Passos Mágicos', divider='rainbow')

# Criando as abas
tab1, tab2, tab3 = st.tabs(["Como funciona a Passos Mágicos", "O que fazem", "Objetivo"])

# tab1 - Como funciona a Passos Mágicos
with tab1:
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
        st.write("Nosso objetivo é impactar a vida de jovens e crianças, oferecendo meios para que alcancem melhores oportunidades.")

        st.write("Nosso ideal é um Brasil onde todas as crianças e jovens tenham oportunidades iguais para realizarem seus sonhos e se tornem protagonistas de suas próprias histórias.")