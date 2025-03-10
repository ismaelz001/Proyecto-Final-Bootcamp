import streamlit as st
import funciones.funciones_graficas as funciones_graficas
import pandas as pd

# 📌 Función principal para mostrar la página del Dashboard
def show():
    """Muestra el Dashboard con gráficos interactivos y métricas clave."""

    # 📌 Cargar estilos desde styles.css
    load_css()

    # 📊 Título Principal con Imagen
    col1, col2 = st.columns([3, 1])  # 3/4 del espacio para el título, 1/4 para la imagen

    with col1:
        st.markdown('<p class="stTitle">📊 Dashboard de Portátiles</p>', unsafe_allow_html=True)

    # 📌 Imagen de portátiles en la cabecera
    top_image_path = "../imgs/porta.webp"
    with col2:
        st.image(top_image_path, width=120)

    # 🔹 Cargar datos de **portátiles**
    df = funciones_graficas.load_data("Portátiles")

    # 📊 **Resumen de Mercado (KPIs)**
    st.markdown("### 📊 Resumen de Mercado")
    col1, col2, col3 = st.columns(3)

    col1.metric("🔢 Total de Portátiles", len(df))
    col2.metric("💰 Precio Medio", f"€{df['precio'].mean():.2f}")
    col3.metric("🔻 Descuento Medio", f"{df['descuento_%'].mean():.1f}%")

    # 🔹 Primer bloque de gráficos
    tabs = st.tabs(["📊 Distribución de Precios", "⭐ Histograma de Rating", "💵 Relación Precio - Rating"])

    with tabs[0]:
        fig_hist = funciones_graficas.grafico_hist("Portátiles")
        st.plotly_chart(fig_hist, use_container_width=True)

    with tabs[1]:
        fig_hist2 = funciones_graficas.fig_hist2("Portátiles")
        st.plotly_chart(fig_hist2, use_container_width=True)

    with tabs[2]:
        fig_scatter1 = funciones_graficas.fig_category("Portátiles")
        st.plotly_chart(fig_scatter1, use_container_width=True)

    # 🔹 Segundo bloque de gráficos
    tabs2 = st.tabs(["📢 Opiniones vs. Rating", "📉 Descuento por Categoría", "📊 Gráfico 3D: Precio, Rating y Opiniones"])

    with tabs2[0]:
        fig_scatter2 = funciones_graficas.fig_rating("Portátiles")
        st.plotly_chart(fig_scatter2, use_container_width=True)

    with tabs2[1]:
        fig_hist_desc = funciones_graficas.fig_hist_desc("Portátiles")
        st.plotly_chart(fig_hist_desc, use_container_width=True)

    with tabs2[2]:
        fig_scatter3d = funciones_graficas.fig_scatter("Portátiles")
        st.plotly_chart(fig_scatter3d, use_container_width=True)

# 📌 Función para cargar estilos desde style.css
def load_css():
    """Carga los estilos CSS en la aplicación."""
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 📌 Permite ejecutar la función si el archivo se ejecuta directamente
if __name__ == "__main__":
    show()
