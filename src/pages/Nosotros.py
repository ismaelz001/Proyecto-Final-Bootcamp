import streamlit as st
from PIL import Image
import os

# 📌 Función principal para mostrar la página
def show():
    """Muestra la página 'Nosotros' con información del equipo."""

    # 📌 Cargar estilos desde styles.css
    load_css()

    # 📌 Título Principal
    st.title("👥 Nosotros - Equipo del Proyecto")

    st.write("""
    Somos un equipo apasionado por la tecnología y el análisis de datos.  
    Aquí puedes conocer a los integrantes del proyecto y sus perfiles profesionales. 🚀
    """)

    st.write("---")

    # 📌 Información de los integrantes del equipo
    integrantes = [
        {
            "nombre": "Luis Vazquez",
            "imagen": "../src/pages/imagenes_foto/Imagen1.jpg",
            "linkedin": "https://www.linkedin.com/in/luis-vasquez-d/",
            "github": "https://github.com/luis4039"
        },
        {
            "nombre": "Naomi Burgués",
            "imagen": "../src/pages/imagenes_foto/fotoperfil.jpeg",
            "linkedin": "https://www.linkedin.com/in/naomi-burgues/",
            "github": "https://github.com/mariagomez"
        },
        {
            "nombre": "Mateo Morales Gomez",
            "imagen": "../src/pages/imagenes_foto/perfilM.jpg",
            "linkedin": "www.linkedin.com/in/mateo-morales-51a207355/",
            "github": "https://github.com/mateomg-dotcom"
        },
        {
            "nombre": "Ismael Rodríguez",
            "imagen": "../src/pages/imagenes_foto/fotoPro.jpeg",
            "linkedin": "https://www.linkedin.com/in/ismael-rodriguez-b6155165/",
            "github": "https://github.com/ismaelz001"
        }
    ]

    # 📌 Ruta Absoluta para evitar problemas de búsqueda
    imagen_default = os.path.abspath("imagenes_foto/avatar.webp")

    # 📌 Mostrar la información de cada integrante en columnas
    for integrante in integrantes:
        col1, col2 = st.columns([1, 3])

        with col1:
            imagen_path = integrante["imagen"]

            # 📌 Intentar cargar la imagen, si no existe usar la imagen por defecto
            try:
                if os.path.exists(imagen_path):
                    imagen = Image.open(imagen_path)
                else:
                    st.warning(f"⚠ La imagen '{imagen_path}' no existe. Usando imagen por defecto.")
                    imagen = Image.open(imagen_default)
            except FileNotFoundError:
                st.error(f"❌ No se pudo abrir la imagen '{imagen_path}'. Verifica la ruta.")
                imagen = Image.open(imagen_default)

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
