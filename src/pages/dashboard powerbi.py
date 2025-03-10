import streamlit as st
import streamlit.components.v1 as components

# 📌 Aplicar estilos globales
def load_css():
    with open("src/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
load_css()  # Llamamos a la función para aplicar los estilos

  
# Título de la sección
st.title("Dashboard de Power BI")

# Código de inserción de Power BI (reemplaza con tu código)
powerbi_embed_code = """
<iframe title="Tu título de informe" width="1140" height="541.25" src="URL de tu informe" frameborder="0" allowFullScreen="true"></iframe>
"""

# Muestra el dashboard de Power BI en Streamlit
components.html(powerbi_embed_code, width=1140, height=541)
