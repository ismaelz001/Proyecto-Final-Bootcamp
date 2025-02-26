from conn import conectar
import pandas as pd

def cargarDatos():
    con = conectar()
    if not con:
        print("❌ No se pudo conectar a la base de datos. Abortando...")
        return

    cursor = con.cursor(buffered=True)
    cursor.execute("USE PcComponentes")

    # 🔹 Cargar Categorías de Portátiles (SIN MODIFICAR DATOS)
    def cargarCategorias(ruta, tabla):
        df = pd.read_csv(ruta, usecols=["nombre", "url"]).fillna("")
        print(f"📌 Cargando categorías desde {ruta}...")

        for _, row in df.iterrows():
            try:
                cursor.execute(
                    f"INSERT IGNORE INTO {tabla} (nombre, url) VALUES (%s, %s)",
                    (row["nombre"], row["url"])
                )
            except Exception as e:
                print(f"❌ Error al insertar en {tabla}: {row['nombre']}, Error: {e}")

    print("🔹 Cargando categorías de portátiles...")
    cargarCategorias("../data/categoriasPortatiles.csv", "categoriasportatil")

    # 🔎 Obtener `categoria_id`
    def obtenerCategoriaId(nombre_categoria, tabla):
        cursor.execute(f"SELECT id FROM {tabla} WHERE LOWER(nombre) = %s", (nombre_categoria.strip().lower(),))
        result = cursor.fetchone()
        cursor.fetchall()
        return result[0] if result else None

    # 📂 Cargar Productos Portátiles (SIN MODIFICAR DATOS)
    print("🔹 Cargando productos de portátiles...")
    df_productosPortatil = pd.read_csv("../data/productosPortatil-limpio.csv").fillna("")

    for _, row in df_productosPortatil.iterrows():
        categoria_id = obtenerCategoriaId(row["categoria"], "categoriasportatil")
        if categoria_id:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO productosportatil (fecha, nombre, url, precio, precio_tachado, rating, opiniones, categoria_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    row["timestamp"], row["nombre"], row["url"], 
                    row["precio"], 
                    row["precio_tachado"], 
                    row["rating"], 
                    row["opiniones"], 
                    categoria_id
                ))
            except Exception as e:
                print(f"❌ Error al insertar en productosportatil: {row['nombre']}, Error: {e}")

    con.commit()
    print("✅ Todos los datos de portátiles han sido cargados exitosamente.")
    cursor.close()
    con.close()

# Ejecutar la función
cargarDatos()
