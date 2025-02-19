import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    return pd.read_csv("../data/productos_componentes_pc.csv")

df = load_data()

st.title("🔍 Buscar un Componente")

busqueda = st.text_input("Ingrese el nombre del componente")

if busqueda:
 resultados = df[df["nombre"].str.contains(busqueda, case=False, na=False)]
 st.dataframe(resultados)
