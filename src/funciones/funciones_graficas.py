import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import os 

def load_data(select_box_comp_port):
    file_path = None
    if select_box_comp_port == "Portátiles":
        file_path = "../data/productosPortatil-limpio.csv"
    else:
        st.error("⚠️ Error: Solo se permite 'Portátiles'.")
        return None

    if not os.path.exists(file_path):
        st.error(f"⚠️ ERROR: No se encontró el archivo `{file_path}`")
        return None

    try:
        df = pd.read_csv(file_path)
        st.write("✅ Datos cargados correctamente:", df.head())

        if "precio_tachado" in df.columns and "precio" in df.columns:
            df["descuento_%"] = (((df["precio"] - df["precio_tachado"]) / df["precio"]) * 100) * -1
            df["descuento_%"] = df["descuento_%"].round(2).fillna(0)

        return df
    except Exception as e:
        st.error(f"⚠️ ERROR al cargar los datos: {e}")
        return None

def grafico_hist(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig_hist = px.histogram(df, x="precio", nbins=40)
    return fig_hist

def fig_category(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig = go.Figure()

    for categoria in df['categoria_id'].unique():
        df_filtrado = df[df['categoria_id'] == categoria]
        fig.add_trace(go.Scatter(
            x=df_filtrado['precio'],
            y=df_filtrado['rating'],
            mode='markers',
            name=str(categoria)  # Convertir a string
        ))

    fig.update_layout(
        title='Gráfico de Dispersión por Categoría: Precio - Rating',
        xaxis_title='Precio',
        yaxis_title='Rating',
        template='plotly_dark'
    )
    return fig

def fig_rating(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig = go.Figure()

    for categoria in df['categoria_id'].unique():
        df_filtrado = df[df['categoria_id'] == categoria]
        fig.add_trace(go.Scatter(
            x=df_filtrado['opiniones'],
            y=df_filtrado['rating'],
            mode='markers',
            name=str(categoria)  # Convertir a string
        ))

    fig.update_layout(
        title='Gráfico de Dispersión Opiniones - Rating',
        xaxis_title='Opiniones',
        yaxis_title='Rating',
        template='plotly_dark'
    )
    return fig


def fig_hist2(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig = px.histogram(df, x="rating", color="categoria_id", 
                       title="Histograma de Rating por Categoría", 
                       template="plotly_dark")
    return fig

def fig_scatter(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig = px.scatter_3d(df, x="precio", y="rating", z="opiniones", 
                        color="categoria_id")
    return fig

def fig_hist_desc(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig = px.histogram(df, x="descuento_%", color="categoria_id", 
                       title="Histograma de Descuento por Categoría", 
                       template="plotly_dark")
    return fig
