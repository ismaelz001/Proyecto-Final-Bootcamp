import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import funciones.funciones_graficas as funciones_graficas

# Cargar datos (esto luego se cambiará a la base de datos)

st.title("📊 Dashboard de Componentes")

# # Filtros
# categoria = st.sidebar.selectbox("Seleccionar categoría", df["categoria"].unique())

# # Filtrar datos
# df_filtrado = df[df["categoria"] == categoria]

# # Mostrar tabla
# st.dataframe(df_filtrado)

# # Gráfico de precios
# fig, ax = plt.subplots()
# sns.histplot(df_filtrado["precio"], bins=20, ax=ax)
# st.pyplot(fig)


select_box_comp_port = st.selectbox(label = "Componentes o Portatiles",
             options = ("Componentes", "Portatiles"))

fig_hist = funciones_graficas.grafico_hist(select_box_comp_port)
st.plotly_chart(fig_hist)

fig_scatter1 = funciones_graficas.fig_category(select_box_comp_port)
st.plotly_chart(fig_scatter1)

fig_scatter1 = funciones_graficas.fig_rating(select_box_comp_port)
st.plotly_chart(fig_scatter1)

fig_hist2 = funciones_graficas.fig_hist2(select_box_comp_port)
st.plotly_chart(fig_hist2)

fig_scatter2 = funciones_graficas.fig_scatter(select_box_comp_port)
st.plotly_chart(fig_scatter2)

fig_hist_desc = funciones_graficas.fig_hist_desc(select_box_comp_port)
st.plotly_chart(fig_hist_desc)