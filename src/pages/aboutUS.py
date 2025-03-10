import streamlit as st
from PIL import Image
import os

# 📌 Función principal para mostrar la página
def show():
    """Muestra la página 'About Us' con información del equipo."""

    # 📌 Cargar estilos desde styles.css
    load_css()

    # 📌 Título Principal
    st.title("👥 About Us - Equipo del Proyecto")

    st.write("""
    Somos un equipo apasionado por la tecnología y el análisis de datos.  
    Aquí puedes conocer a los integrantes del proyecto y sus perfiles profesionales. 🚀
    """)

    st.write("---")

    # 📌 Información de los integrantes del equipo
    integrantes = [
        {
            "nombre": "Juan Pérez",
            "imagen": "imagenes_foto/avatar.webp",
            "linkedin": "https://www.linkedin.com/in/juanperez",
            "github": "https://github.com/juanperez"
        },
        {
            "nombre": "María Gómez",
            "imagen": "imagenes_foto/avatar.webp",
            "linkedin": "https://www.linkedin.com/in/mariagomez",
            "github": "https://github.com/mariagomez"
        },
        {
            "nombre": "Mateo Morales Gomez",
            "imagen": "imagenes_foto/avatar.webp",
            "linkedin": "www.linkedin.com/in/mateo-morales-51a207355",
            "github": "https://github.com/mateomg-dotcom"
        },
        {
            "nombre": "Ismael Rodríguez",
            "imagen": "imagenes_foto/avatar.webp",
            "linkedin": "https://www.linkedin.com/in/ismael-rodriguez-b6155165/",
            "github": "https://github.com/ismaelz001"
        }
    ]

    # 📌 Imagen por defecto si la imagen no existe o está vacía
    imagen_default = "../src/pages/imagenes_foto/avatar.webp"

    # 📌 Mostrar la información de cada integrante en columnas
    for integrante in integrantes:
        col1, col2 = st.columns([1, 3])

        with col1:
            # 📌 Verificar si la clave "imagen" existe y no está vacía
            if "imagen" in integrante and os.path.exists(integrante["imagen"]):
                imagen = Image.open(integrante["imagen"])
            else:
                imagen = Image.open(imagen_default)  # Usar imagen por defecto si no se encuentra

            st.image(imagen, width=150)  # Ajustar tamaño de la imagen

        with col2:
            st.subheader(integrante["nombre"])
            st.markdown(f"[LinkedIn]( {integrante['linkedin']} ) 🔗")
            st.markdown(f"[GitHub]( {integrante['github']} ) 🖥")

        st.write("---")  # Línea divisoria entre integrantes

    # 📌 Mensaje final
    st.write("Si deseas conocer más sobre nuestro trabajo, ¡síguenos en nuestras redes! 🚀")

# 📌 Función para cargar estilos desde style.css
def load_css():
    """Carga los estilos CSS en la aplicación."""
    with open("../src/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 📌 Permite ejecutar la función si el archivo se ejecuta directamente
if __name__ == "__main__":
    show()
