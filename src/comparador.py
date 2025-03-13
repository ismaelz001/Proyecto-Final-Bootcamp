import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def comparar_portatiles():
    """Comparador de portátiles."""

    # 📌 Verificar que los datos existen antes de cargar la comparación
    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ No has seleccionado ningún portátil. Regresa a la búsqueda y selecciona uno.")
        return

    if "selected_product_id" not in st.session_state or st.session_state.selected_product_id is None:
        st.warning("⚠️ No has seleccionado ningún portátil para comparar.")
        return

    if "recommended_products" not in st.session_state or st.session_state.recommended_products is None:
        st.warning("⚠️ No hay portátiles recomendados para comparar.")
        return

    st.title("🆚 Comparador de Portátiles")

    # 📌 Obtener los datos de los portátiles seleccionados
    portatil = st.session_state.df[
        st.session_state.df["producto_id"].astype(str) == st.session_state.selected_product_id
    ].iloc[0]

    # 📌 Seleccionar el primer portátil recomendado si no hay selección previa
    if "selected_recommended_id" not in st.session_state:
        st.session_state.selected_recommended_id = st.session_state.recommended_products.iloc[0]["producto_id"]

    # 📌 Obtener el portátil recomendado
    portatil_recomendado = st.session_state.recommended_products[
        st.session_state.recommended_products["producto_id"].astype(str) == str(st.session_state.selected_recommended_id)
    ].iloc[0]

    st.subheader("🔍 Características del Portátil Seleccionado")
    mostrar_caracteristicas(portatil)

    st.subheader("🔍 Características del Portátil Recomendado")
    mostrar_caracteristicas(portatil_recomendado)

    # 📌 Comparación lado a lado
    st.subheader("📊 Comparador de Portátiles")

    def destacar_mejor(valor1, valor2):
        """Resalta el mejor valor en verde y el peor en rojo."""
        if valor1 > valor2:
            return f"🟢 **{valor1}**"
        elif valor2 > valor1:
            return f"🔴 **{valor1}**"
        else:
            return f"⚖️ {valor1}"

    comparacion = pd.DataFrame({
        "Característica": ["💰 Precio (€)", "⭐ Rating", "💬 Opiniones", "🔢 Núcleos", "⚡ Velocidad CPU (GHz)", "🖥️ RAM (GB)", "💾 Almacenamiento (GB)"],
        f"Portátil ID {portatil['producto_id']}": [
            destacar_mejor(portatil["precio"], portatil_recomendado["precio"]),
            destacar_mejor(portatil["rating"], portatil_recomendado["rating"]),
            destacar_mejor(portatil["opiniones"], portatil_recomendado["opiniones"]),
            destacar_mejor(portatil["Processor Cores"], portatil_recomendado["Processor Cores"]),
            destacar_mejor(portatil["Processor Speed"], portatil_recomendado["Processor Speed"]),
            destacar_mejor(portatil["RAM Gbs"], portatil_recomendado["RAM Gbs"]),
            destacar_mejor(portatil["Storage Gbs"], portatil_recomendado["Storage Gbs"])
        ],
        f"Portátil ID {portatil_recomendado['producto_id']}": [
            destacar_mejor(portatil_recomendado["precio"], portatil["precio"]),
            destacar_mejor(portatil_recomendado["rating"], portatil["rating"]),
            destacar_mejor(portatil_recomendado["opiniones"], portatil["opiniones"]),
            destacar_mejor(portatil_recomendado["Processor Cores"], portatil["Processor Cores"]),
            destacar_mejor(portatil_recomendado["Processor Speed"], portatil["Processor Speed"]),
            destacar_mejor(portatil_recomendado["RAM Gbs"], portatil["RAM Gbs"]),
            destacar_mejor(portatil_recomendado["Storage Gbs"], portatil["Storage Gbs"])
        ]
    })

    st.table(comparacion)
    
      # 📌 Generar gráfica comparativa
    graficar_comparacion(portatil, portatil_recomendado)

# 📌 Función para mostrar características detalladas de un portátil
def mostrar_caracteristicas(portatil):
    """Muestra detalles de un portátil de manera estructurada en Streamlit."""
    st.subheader("📌 Características del Portátil")
    st.write(f"**💻 Nombre:** {portatil['nombre']}")
    st.write(f"**🏷️ Marca:** {portatil['marca']}")
    st.write(f"**💰 Precio:** {portatil['precio']} €")
    st.write(f"**⭐ Valoración:** {portatil['rating']}")
    st.write(f"**💬 Opiniones:** {portatil['opiniones']}")
    st.write(f"**🔢 Núcleos del Procesador:** {portatil['Processor Cores']}")
    st.write(f"**⚡ Velocidad del Procesador:** {portatil['Processor Speed']} GHz")
    st.write(f"**🖥️ RAM:** {portatil['RAM Gbs']} GB")
    st.write(f"**💾 Almacenamiento:** {portatil['Storage Gbs']} GB")
    st.write("---")



def graficar_comparacion(portatil, portatil_recomendado):
    """Genera una gráfica comparativa de los portátiles seleccionados."""
    
    # 📌 Definir las características a comparar
    caracteristicas = ["Precio (€)", "Rating", "Opiniones", "Núcleos CPU", "Velocidad CPU (GHz)", "RAM (GB)", "Almacenamiento (GB)"]
    valores_portatil = [portatil["precio"], portatil["rating"], portatil["opiniones"], portatil["Processor Cores"],
                        portatil["Processor Speed"], portatil["RAM Gbs"], portatil["Storage Gbs"]]
    
    valores_recomendado = [portatil_recomendado["precio"], portatil_recomendado["rating"], portatil_recomendado["opiniones"],
                           portatil_recomendado["Processor Cores"], portatil_recomendado["Processor Speed"],
                           portatil_recomendado["RAM Gbs"], portatil_recomendado["Storage Gbs"]]
    
    # 📌 Definir la posición en el gráfico
    x = np.arange(len(caracteristicas))
    ancho_barra = 0.35

    # 📌 Crear la figura
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # 📌 Agregar las barras
    ax.bar(x - ancho_barra/2, valores_portatil, ancho_barra, label=f"Portátil {portatil['producto_id']}", alpha=0.7, color="blue")
    ax.bar(x + ancho_barra/2, valores_recomendado, ancho_barra, label=f"Portátil {portatil_recomendado['producto_id']}", alpha=0.7, color="orange")
    
    # 📌 Configurar el gráfico
    ax.set_xlabel("Características")
    ax.set_ylabel("Valores")
    ax.set_title("Comparación de Características entre Portátiles")
    ax.set_xticks(x)
    ax.set_xticklabels(caracteristicas, rotation=45)
    ax.legend()

    # 📌 Mostrar la gráfica en Streamlit
    st.pyplot(fig)

 