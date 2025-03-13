import streamlit as st
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt 

# 📌 Importar Comparador.py (Ahora está fuera de `pages/`)
from comparador import comparar_portatiles


# 📌 Cargar estilos desde style.css
def load_css():
    with open("../src/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# 📌 Cargar datos de productos con nombres
@st.cache_data
def cargar_datos_productos():
    return pd.read_csv("../data/productos_portatiles_actualizado.csv")

df_productos = cargar_datos_productos()

# 📌 Cargar datos de portátiles
@st.cache_data
def cargar_datos():
    return pd.read_csv("../data/portatiles_clustering_final.csv")

df = cargar_datos()

# 📌 Cargar modelo de clasificación
@st.cache_resource
def cargar_modelo():
    with open("../modelo_clasificacion/modelo_clasificacion.pkl", "rb") as file:
        modelo = pickle.load(file)
    return modelo

modelo = cargar_modelo()

# 📌 Explicaciones de cada gama (antes llamado "cluster")
explicacion_gamas = {
    0: "🟢 **Gama 0 - Básica**: Portátiles económicos con pocas opiniones. Ideales para navegación web, ofimática y estudios.",
    1: "🔵 **Gama 1 - Premium**: Portátiles de gama alta con excelentes valoraciones. Orientados a profesionales y multitarea.",
    2: "🔴 **Gama 2 - Gaming**: Portátiles potentes con precios elevados y componentes de alto rendimiento. Diseñados para gaming y tareas exigentes."
}

# 📌 Función para predecir la gama de un portátil
def predecir_gama(caracteristicas):
    prediccion = modelo.predict([caracteristicas])
    return prediccion[0]

# 📌 Función para buscar portátiles similares con Nombre y Marca
def recomendar_portatiles(portatil_id, df, df_productos):
    caracteristicas = ["precio", "Processor Cores", "Processor Speed", "RAM Gbs", "Storage Gbs"]

    # 📌 Convertir `producto_id` a string en ambos DataFrames
    df["producto_id"] = df["producto_id"].astype(str)
    df_productos["producto_id"] = df_productos["producto_id"].astype(str)

    # 📌 Verificar si el ID seleccionado existe en el DataFrame
    if str(portatil_id) not in df["producto_id"].values:
        st.error(f"⚠️ El producto ID {portatil_id} no existe en el dataset.")
        return pd.DataFrame()

    knn = NearestNeighbors(n_neighbors=6, algorithm="auto")
    knn.fit(df[caracteristicas])

    # 📌 Filtrar el portátil seleccionado
    portatil = df[df["producto_id"] == str(portatil_id)]
    
    if portatil.empty:
        st.error(f"⚠️ No se encontró el portátil con ID {portatil_id}.")
        return pd.DataFrame()

    # 📌 Extraer características necesarias
    portatil_features = portatil[caracteristicas]

    try:
        # 📌 Buscar vecinos más cercanos
        indices = knn.kneighbors(portatil_features, return_distance=False)[0]

        # 📌 Si no encuentra vecinos, devolver mensaje
        if len(indices) == 0:
            st.warning("⚠️ No se encontraron portátiles similares.")
            return pd.DataFrame()

        # 📌 Obtener recomendaciones basadas en los índices encontrados
        recomendaciones = df.iloc[indices].copy()

        # 📌 Asignar la marca directamente sin hacer `merge()`
        recomendaciones["marca"] = recomendaciones["producto_id"].map(df.set_index("producto_id")["marca"])

        # 📌 Asignar el nombre desde `productos_portatiles_actualizado.csv`
        recomendaciones["nombre"] = recomendaciones["producto_id"].map(df_productos.set_index("producto_id")["nombre"])

        return recomendaciones

    except ValueError as e:
        st.error(f"⚠️ Error en recomendación: {e}")
        return pd.DataFrame()

# 📌 Función para mostrar características detalladas de un portátil
def mostrar_caracteristicas(portatil):
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

# 📌 Función principal para mostrar la página en Streamlit
def show():
    """Muestra la página de búsqueda y clasificación de portátiles."""
    
    st.title("🔍 Búsqueda de Portátiles y Clasificación")
     
     
     # 📌 Inicializar `st.session_state` si no existen los valores
    if "selected_product_id" not in st.session_state:
        st.session_state.selected_product_id = None
    if "recommended_products" not in st.session_state:
        st.session_state.recommended_products = None
    if "df" not in st.session_state:
        st.session_state.df = None
        
        
    # 📌 Filtros para búsqueda
    marca = st.selectbox("📌 Selecciona la marca del portátil:", ["Todas"] + list(df["marca"].unique()))
    min_precio, max_precio = st.slider("💰 Rango de precio:", float(df["precio"].min()), float(df["precio"].max()), (float(df["precio"].min()), float(df["precio"].max())))
    min_cores, max_cores = st.slider("🔢 Rango de núcleos:", int(df["Processor Cores"].min()), int(df["Processor Cores"].max()), (int(df["Processor Cores"].min()), int(df["Processor Cores"].max())))
    min_speed, max_speed = st.slider("⚡ Rango de velocidad de procesador (GHz):", float(df["Processor Speed"].min()), float(df["Processor Speed"].max()), (float(df["Processor Speed"].min()), float(df["Processor Speed"].max())))

    # 📌 Aplicar filtros
    resultados = df[
        ((df["marca"] == marca) if marca != "Todas" else True) &
        (df["precio"].between(min_precio, max_precio)) &
        (df["Processor Cores"].between(min_cores, max_cores)) &
        (df["Processor Speed"].between(min_speed, max_speed))
    ].copy()  # Copiamos para evitar modificaciones inesperadas

    # 📌 Unir `nombre` desde `df_productos`
    resultados["nombre"] = resultados["producto_id"].map(df_productos.set_index("producto_id")["nombre"])

    if not resultados.empty:
        st.write("✅ Portátiles encontrados:")
        id_seleccionado = st.selectbox("📌 Selecciona un ID de portátil para ver detalles:", resultados["producto_id"].astype(str))

        if id_seleccionado:
            # Extraer características del portátil seleccionado
            portatil = resultados[resultados["producto_id"].astype(str) == id_seleccionado].iloc[0]
            mostrar_caracteristicas(portatil)

            # 📌 Predicción de gama para el portátil seleccionado
            gama_predicha = predecir_gama([
                portatil["precio"],
                portatil["opiniones"],
                portatil["rating"],
                portatil["Processor Cores"],
                portatil["Processor Speed"],
                portatil["RAM Gbs"],
                portatil["Storage Gbs"],
                portatil["marca_encoded"]
            ])

            # 📌 Mostrar la predicción y explicación de la gama
            st.success(f"🖥️ El portátil con ID {id_seleccionado} ha sido clasificado en la **GAMA {gama_predicha}**")
            st.write(explicacion_gamas[gama_predicha])  

            # 📌 Obtener recomendaciones y verificar si está vacío antes de aplicar filtros
            recomendaciones = recomendar_portatiles(int(id_seleccionado), df, df_productos)

            if not recomendaciones.empty:
                # 📌 Convertir `producto_id` en `recomendaciones` a `int` para asegurarnos de que la comparación funciona
                recomendaciones["producto_id"] = recomendaciones["producto_id"].astype(int)

                # 📌 Filtrar para que no aparezca el mismo ID seleccionado en los recomendados
                recomendaciones = recomendaciones[recomendaciones["producto_id"] != int(id_seleccionado)]

                st.write("🔍 **Portátiles similares recomendados:**")
                
                 # 📌 Ocultar el índice y hacer que `producto_id` sea la primera columna
                st.dataframe(recomendaciones.set_index("producto_id"))
                #st.dataframe(recomendaciones[["producto_id", "nombre", "marca", "precio", "Processor Cores", "Processor Speed"]])

                # 📌 Nueva selección con `st.radio()` para hacerla diferente del primer `selectbox`
                id_recomendado = st.radio(
                    "📌 Selecciona un portátil recomendado para ver sus características:",
                    recomendaciones["producto_id"].astype(str).tolist()
                )

                if id_recomendado:
                    # 📌 Extraer y mostrar características del portátil recomendado
                    portatil_recomendado = recomendaciones[recomendaciones["producto_id"].astype(str) == id_recomendado].iloc[0]
                    st.subheader("🔍 Detalles del Portátil Recomendado")
                    mostrar_caracteristicas(portatil_recomendado)

                    # 📌 Asegurar que `df` también tenga la columna 'nombre'
                    if "nombre" not in df.columns:
                        #st.warning("⚠️ La columna 'nombre' no está en `df`. Corrigiendo ahora...")
                        df["nombre"] = df["producto_id"].map(df_productos.set_index("producto_id")["nombre"])

                    # 📌 Guardamos en `st.session_state` para que `Comparador.py` lo use
                    st.session_state.selected_product_id = id_seleccionado
                    st.session_state.recommended_products = recomendaciones
                    st.session_state.df = df  # Guardamos el DataFrame con 'nombre' corregido

                    #st.write("✅ Columnas en `df` después de corrección:", df.columns.tolist())


            # 📌 Botón para ir al Comparador
            if st.button("🆚 Comparar Portátiles"):
                comparar_portatiles()  # 🔄 Llamar directamente a `Comparador.py`





            else:
                st.warning("⚠️ No se encontraron portátiles similares.")

    else:
        st.warning("❌ No se encontraron portátiles con esos filtros.")


if __name__ == "__main__":
    show()
