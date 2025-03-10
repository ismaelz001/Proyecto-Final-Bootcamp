import streamlit as st
from streamlit_lottie import st_lottie
import requests

# 📌 Configuración de la página
st.set_page_config(
    page_title="📊 Análisis de Mercado - PC Componentes",
    page_icon="🖥️",
    layout="wide"
)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_file = "https://assets9.lottiefiles.com/packages/lf20_ggwq3ysg.json"

# 📌 Aplicar estilos globales
def load_css():
    with open("../src/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()  # Llamamos a la función para aplicar los estilos

# 📌 Página de Inicio
def show():
    """Muestra la página principal de la aplicación."""

    st.title("📊 Análisis de Mercado de PC Componentes")

    # 📌 Presentación
    with st.container():
        st.subheader("Explora tendencias de precios y demanda en el sector tecnológico")
        st.write(
            "Con esta app podrás analizar el mercado de componentes electrónicos de ordenadores y portátiles, tomando como fuente principal de datos la tienda en línea PC Componentes. "
            "El objetivo de esta herramienta es que permita tanto a usuarios generales como a clientes especializados explorar y comprender mejor este mercado, "
            "por lo tanto la aplicación se dividirá en dos secciones: una para usuarios generales y otra para clientes especializados."
        )

        st.write(
            """
            Nuestro objetivo principal es crear una herramienta útil y accesible para cualquier persona interesada en el mercado de PC Componentes.
            Seguramente te vamos a poder ayudar si:
            * Tienes un negocio y quieres mejorar tus procesos de trabajo para ahorrar tiempo y dinero.
            * Tienes trabajadores que emplean parte de su jornada a realizar tareas repetitivas sin valor añadido para tu negocio.
            * No tienes claras las métricas de tu negocio y quieres tomar decisiones basadas en datos.
            * Quieres mejorar la experiencia de tus clientes.
            * Usas herramientas de software antiguas o poco eficientes o procesos en los que usas papel y bolígrafo.
            """ 
        )

        st.subheader("Funcionalidades Generales de la Aplicación")
        st.write("""
        * La aplicación contará con herramientas de navegación como filtros, búsqueda y paginación para facilitar la exploración de los datos.
        * Se asegurará que los datos y visualizaciones estén siempre actualizados.
        """)
        st.write("---")

    # 📌 Mostrar imágenes (Se mantienen las rutas originales)
    col1, col2, col3 = st.columns([1, 1, 1])  # Reducimos separación de las imágenes
    with col1:
        st.image("../imgs/pc.webp", width=250)
    with col3:
        st.image("../imgs/porta.webp", width=250)

    # 📌 Secciones
    with st.container():
        st.write("---")
        st.header("Secciones de la aplicación")

        st.subheader("Vista para Usuarios")
        st.write("""
        Esta sección está diseñada para el público en general interesado en comprar componentes electrónicos.
        Ofrecerá funcionalidades como:
        * Una tabla detallada con las características de los productos.
        * Un panel de control interactivo con visualizaciones de datos relevantes (precios, descuentos, etc.).
        * Fichas individuales con información completa de cada producto.
        * Una herramienta para comparar productos y facilitar la toma de decisiones.
        """)

        st.subheader("Vista para Clientes")
        st.write("""
        Esta sección está dirigida a clientes más especializados, como empresas o profesionales del sector.
        Proporcionará:
        * Un panel de control en PowerBI con indicadores clave de rendimiento (KPIs) para un comercio electrónico tecnológico.
        * Un esquema visual de la estructura de la base de datos.
        """)

    # 📌 Contacto
    with st.container():
        st.write("---")
        st.header("📩 Ponte en contacto con nosotros!")
        st.write("##")
        contact_form = """
        <form action="https://formsubmit.co/" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Tu nombre" required>
            <input type="email" name="email" placeholder="Tu email" required>
            <button type="submit">Enviar</button>
        </form>
        """
        left_column, right_column = st.columns(2)
        with right_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with left_column:
            st_lottie(load_lottieurl(lottie_file), height=250)

# 📌 Ejecutar la función si el archivo no  se ejecuta directamente
if __name__ == "__main__":
    show()
