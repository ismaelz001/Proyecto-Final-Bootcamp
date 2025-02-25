import streamlit as st

# 📌 Configuración de la página
st.set_page_config(
    page_title="📊 Análisis de Mercado - PC Componentes",
    page_icon="🖥️",
    layout="wide"
)

# 📌 Aplicar estilos globales
# 📌 Cargar estilos desde styles.css
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()  # Llamamos a la función para aplicar los estilos


# 📊 Título Principal
st.markdown('<p class="stTitle">📊 Análisis de Mercado de PC Componentes</p>', unsafe_allow_html=True)
st.markdown('<p class="stSubtitle">Explora tendencias de precios y demanda en el sector tecnológico</p>', unsafe_allow_html=True)

# 📌 Mostrar las dos imágenes (PC y Portátil) centradas
col1, col2, col3 = st.columns([1, 2, 1])  # 📌 Centrar imágenes

with col1:
    st.image("../imgs/pc.webp", width=250)

with col3:
    st.image("../imgs/porta.webp", width=250)

# 📌 Subtítulo de navegación
st.markdown('<p class="stInstructions">⬅️ Seleccione opciones en la barra lateral izquierda</p>', unsafe_allow_html=True)
