import streamlit as st
import streamlit.components.v1 as components

# Título de la sección
st.title("Dashboard de Power BI")

# Código de inserción de Power BI (reemplaza con tu código)
powerbi_embed_code = """
<iframe title="Tu título de informe" width="1140" height="541.25" src="URL de tu informe" frameborder="0" allowFullScreen="true"></iframe>
"""

# Muestra el dashboard de Power BI en Streamlit
components.html(powerbi_embed_code, width=1140, height=541)
