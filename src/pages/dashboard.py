import streamlit as st
import funciones.funciones_graficas as funciones_graficas
import pandas as pd

# 📌 Cargar estilos desde styles.css
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()  # Llamamos a la función para aplicar los estilos


# 📊 Título Principal con Imagen
col1, col2 = st.columns([3, 1])  # 📌 3/4 del espacio para el título, 1/4 para la imagen

with col1:
    st.markdown('<p class="stTitle">📊 Dashboard de Componentes Electrónicos</p>', unsafe_allow_html=True)

# 📌 SELECCIÓN DE CATEGORÍA
st.markdown("### 📌 Selecciona qué tipo de productos analizar:")
select_box_comp_port = st.radio("Elige:", ("Componentes", "Portátiles"), horizontal=True)

# 📌 Definir la imagen según la selección
if select_box_comp_port == "Componentes":
    logo_path = "../imgs/pc.webp"
else:
    logo_path = "../imgs/porta.webp"

# 📌 Mostrar la imagen en la cabecera del Dashboard
with col2:
    st.image(logo_path, width=120)  # 📌 Imagen pequeña alineada a la derecha

# 🔹 Cargar datos para métricas
df = funciones_graficas.load_data(select_box_comp_port)

# 📊 **Resumen de Mercado (KPIs)**
st.markdown("### 📊 Resumen de Mercado")
col1, col2, col3 = st.columns(3)

col1.metric("🔢 Total de Productos", len(df))
col2.metric("💰 Precio Medio", f"€{df['precio'].mean():.2f}")
col3.metric("🔻 Descuento Medio", f"{df['descuento_%'].mean():.1f}%")

# 🔹 Primer bloque de gráficos en dos columnas
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🔹 Distribución de Precios")
    fig_hist = funciones_graficas.grafico_hist(select_box_comp_port)
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.markdown("#### 🔹 Histograma de Rating por Categoría")
    fig_hist2 = funciones_graficas.fig_hist2(select_box_comp_port)
    st.plotly_chart(fig_hist2, use_container_width=True)

# 🔹 Segundo bloque de gráficos en dos columnas
col3, col4 = st.columns(2)
with col3:
    st.markdown("#### 🔹 Relación Precio - Rating por Categoría")
    fig_scatter1 = funciones_graficas.fig_category(select_box_comp_port)
    st.plotly_chart(fig_scatter1, use_container_width=True)

with col4:
    st.markdown("#### 🔹 Relación Opiniones - Rating")
    fig_scatter2 = funciones_graficas.fig_rating(select_box_comp_port)
    st.plotly_chart(fig_scatter2, use_container_width=True)

# 🔹 Última fila con dos gráficos
st.markdown("### 🔥 Análisis de Descuentos y Popularidad")
col5, col6 = st.columns(2)
with col5:
    st.markdown("#### 🔹 Histograma de Descuento por Categoría")
    fig_hist_desc = funciones_graficas.fig_hist_desc(select_box_comp_port)
    st.plotly_chart(fig_hist_desc, use_container_width=True)

with col6:
    st.markdown("#### 🔹 Gráfico 3D: Precio, Rating y Opiniones")
    fig_scatter3d = funciones_graficas.fig_scatter(select_box_comp_port)
    st.plotly_chart(fig_scatter3d, use_container_width=True)
