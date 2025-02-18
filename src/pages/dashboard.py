import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar datos (esto luego se cambiará a la base de datos)
@st.cache_data
def load_data():
    return pd.read_csv("Proyecto-Final-Bootcamp/data/productos_componentes_pc.csv")

df = load_data()

st.title("📊 Dashboard de Componentes")

# Filtros
categoria = st.sidebar.selectbox("Seleccionar categoría", df["categoria"].unique())

# Filtrar datos
df_filtrado = df[df["categoria"] == categoria]

# Mostrar tabla
st.dataframe(df_filtrado)

# Gráfico de precios
fig, ax = plt.subplots()
sns.histplot(df_filtrado["precio"], bins=20, ax=ax)
st.pyplot(fig)
