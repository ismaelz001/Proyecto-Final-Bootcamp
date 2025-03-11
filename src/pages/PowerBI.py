import streamlit as st
import streamlit.components.v1 as components

# 📌 Aplicar estilos globales
def load_css():
    with open("../src/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css() 

# 📌 Función principal para mostrar el Dashboard de Power BI
def show():
    """Muestra el Dashboard de Power BI incrustado en Streamlit."""

    # 📌 Título de la sección
    st.title("📊 Dashboard de Power BI")

    # 📌 Código de inserción de Power BI (Corregido)
    powerbi_embed_code = """
    <iframe title="pc componentes vFinal" width="800" height="600" 
    src="https://app.powerbi.com/view?r=eyJrIjoiYjcwNWQ5OTEtMTNkMy00ZjE3LWFhMDItNjlkNmRjOGI2OTQ1IiwidCI6IjVlNzNkZTM1LWU4MjUtNGVkNS1iZTIyLTg4NTYzNTI3MDkxZSIsImMiOjl9&pageName=4eb3f4309beaea8a173d" 
    frameborder="0" allowFullScreen="true"></iframe>
    """

    # 📌 Muestra el dashboard en Streamlit
    components.html(powerbi_embed_code, width=1140, height=800)

# 📌 Permite ejecutar la función si el archivo se ejecuta directamente
if __name__ == "__main__":
    show()
