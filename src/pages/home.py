import streamlit as st

def home():
    st.title("Bienvenido al Análisis de Mercado de Componentes")
    st.write("📢 Esta aplicación analiza tendencias de precios y demanda en PC Componentes.")
    # 📌 Cargar estilos desde styles.css
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()  # Llamamos a la función para aplicar los estilos

    # st.image("src/assets/", use_column_width=True)

if __name__ == "__main__":
    home()
