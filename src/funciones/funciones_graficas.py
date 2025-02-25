import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import nbformat
import streamlit as st
import os 

def load_data(select_box_comp_port):
    file_path = None
    if select_box_comp_port == "Componentes":
        file_path =("../data/productos_componentes_pc_limpio.csv")
    elif select_box_comp_port == "Portátiles":
        file_path= ("../data/productosPortatil-limpio.csv")
    else:
        st.error("⚠️ Error: Selección no válida en el menú de productos.")
        
    
     # Verificar si el archivo existe
    if not os.path.exists(file_path):
        st.error(f"⚠️ ERROR: No se encontró el archivo `{file_path}`")
        return None

    try:
        df = pd.read_csv(file_path)
        st.write("✅ Datos cargados correctamente:", df.head())  # 🔍 Mostrar datos en Streamlit para depuración
          # ✅ Calcular descuento_% al cargar los datos
        if "precio_tachado" in df.columns and "precio" in df.columns:
            df["descuento_%"] = (((df["precio"] - df["precio_tachado"]) / df["precio"]) * 100) * -1
            df["descuento_%"] = df["descuento_%"].round(2)
            df["descuento_%"] = df["descuento_%"].fillna(0)
        
        
        
        
        return df
    except Exception as e:
        st.error(f"⚠️ ERROR al cargar los datos: {e}")
        return None
    
def grafico_hist(select_box_comp_port):

    df = load_data(select_box_comp_port)

    # df = df['timestamp'] = pd.to_datetime(df['timestamp'])

    fig_hist = px.histogram(data_frame = df, 
             x          = "precio",
             nbins      = 40)

    return fig_hist

def fig_category(select_box_comp_port):

    df = load_data(select_box_comp_port)

    fig = go.Figure()

    for categoria in df['categoria'].unique():
        df_filtrado = df[df['categoria'] == categoria]
        fig.add_trace(go.Scatter(
            x=df_filtrado['precio'],
            y=df_filtrado['rating'],
            mode='markers',
            name=categoria
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

    for categoria in df['categoria'].unique():
        df_filtrado = df[df['categoria'] == categoria]
        fig.add_trace(go.Scatter(
            x=df_filtrado['opiniones'],
            y=df_filtrado['rating'],
            mode='markers',
            name=categoria
        ))

    fig.update_layout(
        title='Gráfico de Dispersión por Categoría: Opiniones - Rating',
        xaxis_title='Opiniones',
        yaxis_title='Rating',
        template='plotly_dark'
    )

    return fig

def fig_hist2(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig = px.histogram(data_frame = df,
             x          = "rating",
             color      = "categoria",
             title      = "Histograma de Rating por Categoría",
             template   = "plotly_dark")
    return fig

def fig_scatter(select_box_comp_port):
    df = load_data(select_box_comp_port)
    fig = px.scatter_3d(data_frame = df,
              x          = "precio",
              y          = "rating",
              z          = "opiniones",
              color      = "categoria"
              )
    return fig

def fig_hist_desc(select_box_comp_port):
    df = load_data(select_box_comp_port)
  
  


    fig = px.histogram(data_frame = df,
                x          = "descuento_%",
                color      = "categoria",
                title      = "Histograma de Descuento por Categoría",
                template   = "plotly_dark")
    return fig