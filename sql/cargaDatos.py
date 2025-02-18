from conn import conectar
import pandas as pd
import re

def cargarDatos():
    con = conectar()
    if not con:
        print("❌ No se pudo conectar a la base de datos. Abortando...")
        return
    cursor = con.cursor(buffered=True)  # 🔹 Agregar `buffered=True` #
    #para evitar resultados no leídos
    cursor.execute("USE PcComponentes")

    # 🔹 Función para cargar categorías
    def cargarDatosDesdeCSV(ruta, tabla):
        df = pd.read_csv(ruta, usecols=["nombre", "url"]).fillna("")
        print(f"📌 Cargando categorías desde {ruta}...")

        for _, row in df.iterrows():
            try:
                cursor.execute(
                    f"INSERT IGNORE INTO {tabla} (nombre, url) VALUES (%s, %s)",
                    (row["nombre"].strip(), row["url"].strip())
                    #eliminamos espacios en blanco
                )
            except Exception as e:
                print(f"❌ Error al insertar en {tabla}: {row['nombre']}, Error: {e}")

    # 📂 Cargar Categorías
    print("🔹 Cargando categorías...")
    cargarDatosDesdeCSV("../data/categoriasPC.csv", "categoriaspc")
    cargarDatosDesdeCSV("../data/categoriasPortatiles.csv", "categoriasportatil")

    # 🔎 Obtener `categoria_id`
    def obtenerCategoriaId(nombre_categoria, tabla):
        cursor.execute(f"SELECT id FROM {tabla} WHERE LOWER(nombre) = %s", (nombre_categoria.strip().lower(),))
        result = cursor.fetchone()
        cursor.fetchall()  # Limpia cualquier resultado no leído
        return result[0] if result else None

    # 🔄 Función mejorada para convertir valores a float
    def convertir_a_float(valor):
        if pd.isna(valor) or valor == "" or valor is None:
            return None
        #arreglo de valores nulos 
        valor_limpio = re.sub(r"[^\d,.]", "", valor) #expersion regular 
        #mantenemos digitos puntos y comas elimanmos el resto 
        #me dio problemas el 1.299,99 para dejarlo en 1299.99 
        if "." in valor_limpio and "," in valor_limpio:
            valor_limpio = valor_limpio.replace(".", "").replace(",", ".")
        elif "," in valor_limpio:
            valor_limpio = valor_limpio.replace(",", ".")
        try:
            return float(valor_limpio)
        except ValueError:
            return None

    #  Función mejorada para convertir valores a int
    def convertir_a_int(valor):
        if pd.isna(valor) or valor == "" or valor is None:
            return None
        return int(re.sub(r"[^\d]", "", valor)) #igual dejamos digitos reemplazos coma por punto

    # 📂 Cargar Productos Componentes PC
    print("Cargando productos de componentes...")
    df_productosComponentes = pd.read_csv("../data/productos_componentes_pc.csv").fillna("")

    for _, row in df_productosComponentes.iterrows():
        categoria_id = obtenerCategoriaId(row["categoria"], "categoriaspc")
        if categoria_id:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO productoscomponentes (fecha, nombre, url, precio, precio_tachado, rating, opiniones, categoria_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row["timestamp"], row["nombre"], row["url"], 
                    convertir_a_float(row["precio"]), 
                    convertir_a_float(row["precio_tachado"]), 
                    convertir_a_float(row["rating"]), 
                    convertir_a_int(row["opiniones"]), 
                    categoria_id
                ))
            except Exception as e:
                print(f"❌ Error al insertar en productoscomponentes: {row['nombre']}, Error: {e}")

    # 📂 Cargar Productos Portátiles
    print("Cargando productos de portátiles...")
    df_productosPortatil = pd.read_csv("../data/productosPortatil.csv").fillna("")

    for _, row in df_productosPortatil.iterrows():
        categoria_id = obtenerCategoriaId(row["categoria"], "categoriasportatil")
        if categoria_id:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO productosportatil (fecha, nombre, url, precio, precio_tachado, rating, opiniones, categoria_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row["timestamp"], row["nombre"], row["url"], 
                    convertir_a_float(row["precio"]), 
                    convertir_a_float(row["precio_tachado"]), 
                    convertir_a_float(row["rating"]), 
                    convertir_a_int(row["opiniones"]), 
                    categoria_id
                ))
            except Exception as e:
                print(f"❌ Error al insertar en productosportatil: {row['nombre']}, Error: {e}")

    # Obtener `producto_id`
    def obtenerProductoId(nombre_producto, tabla):
        cursor.execute(f"SELECT id FROM {tabla} WHERE LOWER(nombre) = %s", (nombre_producto.strip().lower(),))
        result = cursor.fetchone()
        cursor.fetchall()  
        return result[0] if result else None

    #  Función para limpiar características
    def limpiarCaracteristica(valor):
        if pd.isna(valor) or valor == "" or valor is None:
            return None
        return re.sub(r"\s+", " ", valor).strip()[:255]  

    # 📂 Cargar Características de Portátiles
    print("Cargando características de portátiles...")
    df_caracteristicasPortatiles = pd.read_csv("../data/caracteristicas_productos_portatil.csv").fillna("")

    for _, row in df_caracteristicasPortatiles.iterrows():
        producto_id = obtenerProductoId(row["Producto"], "productosportatil")
        if producto_id:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO caracteristicasportatiles (producto_id, producto, caracteristica_1, caracteristica_2, caracteristica_3, caracteristica_4, 
                        caracteristica_5, caracteristica_6, caracteristica_7, caracteristica_8, 
                        caracteristica_9, caracteristica_10, caracteristica_11, caracteristica_12, 
                        caracteristica_13, caracteristica_14, caracteristica_15, caracteristica_16)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (producto_id, row["Producto"], *[limpiarCaracteristica(row.get(f"Característica_{i}", "")) for i in range(1, 17)]))
            except Exception as e:
                print(f"❌ Error al insertar características de {row['Producto']}: {e}")

    # 📂 Cargar Características de Componentes
    print("🔹 Cargando características de componentes...")
    df_caracteristicasComponentes = pd.read_csv("../data/caracteristicas_productos_componentes_pc.csv").fillna("")

    for _, row in df_caracteristicasComponentes.iterrows():
        producto_id = obtenerProductoId(row["Producto"], "productoscomponentes")
        if producto_id:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO caracteristicascomponentes (producto_id, producto, caracteristica_1, caracteristica_2, caracteristica_3, caracteristica_4, 
                        caracteristica_5, caracteristica_6, caracteristica_7, caracteristica_8, 
                        caracteristica_9, caracteristica_10, caracteristica_11, caracteristica_12, 
                        caracteristica_13, caracteristica_14, caracteristica_15, caracteristica_16)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (producto_id, row["Producto"], *[limpiarCaracteristica(row.get(f"Característica_{i}", "")) for i in range(1, 17)]))
            except Exception as e:
                print(f"❌ Error al insertar características de {row['Producto']}: {e}")

    con.commit()
    print("✅ Todos los datos han sido cargados exitosamente.")
    cursor.close()
    con.close()

# Ejecutar la función
cargarDatos()
