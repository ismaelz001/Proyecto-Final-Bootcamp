import streamlit as st
import pandas as pd
import pickle

# 📌 Función principal para mostrar la página de búsqueda
def show():
    """Muestra la página de búsqueda y clasificación de portátiles."""

    # 📌 Cargar estilos desde styles.css
    load_css()

    # 🔹 Cargar datos de portátiles clustering
    @st.cache_data
    def cargar_datos():
        return pd.read_csv("../data/portatiles_clustering_final.csv")

    df = cargar_datos()

    # 🔹 Cargar el modelo de clasificación
    @st.cache_resource
    def cargar_modelo():
        with open("../modelo_clasificacion/modelo_clasificacion.pkl", "rb") as file:
            modelo = pickle.load(file)
        return modelo

    modelo = cargar_modelo()

    # 🔹 Función para predecir el cluster de un portátil
    def predecir_cluster(caracteristicas):
        prediccion = modelo.predict([caracteristicas])
        return prediccion[0]

    # 🔹 Explicación de cada cluster
    explicacion_clusters = {
        0: "📌 **Cluster 0 - Gama Baja/Media:** Portátiles más económicos, con rendimiento básico. Ideales para tareas de oficina, navegación web y estudios.",
        1: "📌 **Cluster 1 - Gama Media/Alta:** Portátiles equilibrados en precio y rendimiento. Buenos para trabajo profesional y gaming ligero.",
        2: "📌 **Cluster 2 - Gama Alta/Premium:** Portátiles potentes con hardware avanzado. Orientados a gaming, diseño gráfico y edición de video."
    }

    # 🎯 **Interfaz de búsqueda y predicción en Streamlit**
    st.title("🔍 Búsqueda de Portátiles y Clasificación")

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
    ]

    if not resultados.empty:
        st.write("✅ Portátiles encontrados:")
        st.dataframe(resultados[["producto_id", "precio", "Processor Cores", "Processor Speed", "RAM Gbs", "Storage Gbs", "marca"]])

        # Seleccionar un portátil específico por ID
        id_seleccionado = st.selectbox("📌 Selecciona un ID de portátil para hacer la predicción:", resultados["producto_id"].astype(str))

        if id_seleccionado:
            # Extraer características del portátil seleccionado
            portatil = resultados[resultados["producto_id"].astype(str) == id_seleccionado].iloc[0]
            caracteristicas = [
                portatil["precio"],
                portatil["opiniones"],
                portatil["rating"],
                portatil["Processor Cores"],
                portatil["Processor Speed"],
                portatil["RAM Gbs"],
                portatil["Storage Gbs"],
                portatil["marca_encoded"]
            ]

            # Realizar la predicción del cluster
            cluster_predicho = predecir_cluster(caracteristicas)

            # Explicar la predicción en base a los valores del portátil
            explicacion = f"""
            📌 **Portátil ID {id_seleccionado} - Características Principales:**  
            - 💰 **Precio:** {portatil["precio"]}€  
            - ⭐ **Valoración:** {portatil["rating"]}  
            - 💬 **Opiniones:** {portatil["opiniones"]}  
            - 🔢 **Núcleos del Procesador:** {portatil["Processor Cores"]}  
            - ⚡ **Velocidad del Procesador:** {portatil["Processor Speed"]} GHz  
            - 🖥️ **RAM:** {portatil["RAM Gbs"]} GB  
            - 💾 **Almacenamiento:** {portatil["Storage Gbs"]} GB  
            - 🏷️ **Marca:** {portatil["marca"]}  
            """

            # Mostrar la predicción y la explicación del cluster
            st.success(f"🖥️ El portátil con ID {id_seleccionado} ha sido clasificado en el CLUSTER: **{cluster_predicho}**")
            st.write(explicacion_clusters[cluster_predicho])  # Explicación del cluster
            st.markdown(explicacion)  # Explicación basada en características

    else:
        st.warning("❌ No se encontraron portátiles con esos filtros.")

# 📌 Función para cargar estilos desde style.css
def load_css():
    """Carga los estilos CSS en la aplicación."""
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 📌 Permite ejecutar la función si el archivo se ejecuta directamente
if __name__ == "__main__":
    show()
