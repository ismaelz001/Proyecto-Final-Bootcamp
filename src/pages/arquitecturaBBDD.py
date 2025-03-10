import streamlit as st
from PIL import Image

# 📌 Función principal para mostrar la página de Arquitectura de la Base de Datos
def show():
    """Muestra la página con la arquitectura de la base de datos."""

    # 📌 Configuración de la página
    st.set_page_config(page_title="📊 Arquitectura de Base de Datos", layout="wide")

    # 📌 Cargar estilos desde styles.css
    load_css()

    # 📌 Título principal
    st.markdown("# 🗄️ Arquitectura de la Base de Datos")
    st.markdown(
        "En esta sección se presenta la estructura de la base de datos utilizada en el proyecto, "
        "incluyendo la descripción de cada tabla y el significado de cada una de sus columnas."
    )

    # 📌 Mostrar imagen del diagrama MER
    st.markdown("## 📌 Diagrama Entidad-Relación (MER)")
    image_path = "../src/pages/diagramaMER.png"  
    image = Image.open(image_path)
    st.image(image, caption="Modelo Entidad-Relación de la Base de Datos", use_column_width=True)

    # 📌 Descripción de las tablas
    st.markdown("## 📋 Descripción de las Tablas")

    st.markdown("### 🔹 Tabla `categorias_portatiles`")
    st.write(
        "Esta tabla almacena las diferentes categorías en las que se agrupan los portátiles. "
        "Cada categoría tiene un identificador único y un nombre."
    )
    st.code("""
    categoria_id (PK) - Identificador único de la categoría
    categoria_nombre - Nombre de la categoría
    url - URL de referencia a la categoría en la web
    """, language="sql")

    st.markdown("### 🔹 Tabla `productos_portatiles`")
    st.write(
        "Almacena la información detallada de cada portátil, incluyendo sus características principales, "
        "opiniones y precios. Se relaciona con la tabla `categorias_portatiles` y la tabla de características."
    )
    st.code("""
    producto_id (PK) - Identificador único del portátil
    timestamp - Fecha y hora de la extracción de datos
    nombre - Nombre del producto
    url - URL del producto en la web
    precio - Precio actual del portátil
    precio_tachado - Precio anterior (si tiene descuento)
    rating - Calificación promedio de los usuarios
    opiniones - Número de opiniones registradas
    categoria_id (FK) - Relación con la tabla de categorías
    descuento_porcentaje - Descuento aplicado en el precio
    marca - Marca del portátil
    cluster (FK) - Grupo al que pertenece el portátil según el análisis de clustering
    """, language="sql")

    st.markdown("### 🔹 Tabla `caracteristicas_portatiles`")
    st.write(
        "Contiene detalles técnicos de cada portátil, como procesador, RAM, almacenamiento y otros aspectos."
    )
    st.code("""
    producto_id (FK) - Identificador único del portátil (relación 1:1)
    Processor_Cores - Número de núcleos del procesador
    Processor_Speed - Velocidad del procesador en GHz
    RAM_Gbs - Cantidad de memoria RAM en GB
    Storage_Gbs - Capacidad de almacenamiento en GB
    Display_Inches - Tamaño de la pantalla en pulgadas
    GPU_Model - Modelo de tarjeta gráfica
    USB_Ports - Número de puertos USB
    Operating_System - Sistema operativo preinstalado
    Weight - Peso del portátil en kg
    Battery_mAh - Capacidad de la batería en mAh
    """, language="sql")

    st.markdown("## 🔎 Conclusión")
    st.write(
        "El modelo de base de datos implementado permite organizar eficientemente la información de los portátiles, "
        "facilitando el análisis y segmentación de productos en función de sus características y opiniones de los clientes."
    )

# 📌 Función para cargar estilos desde style.css
def load_css():
    """Carga los estilos CSS en la aplicación."""
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 📌 Permite ejecutar la función si el archivo se ejecuta directamente
if __name__ == "__main__":
    show()
