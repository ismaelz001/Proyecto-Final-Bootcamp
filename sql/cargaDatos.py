from conn import conectar
import pandas as pd

def cargarDatos():
    con = conectar()
    if not con:
        print("❌ No se pudo conectar a la base de datos. Abortando...")
        return

    cursor = con.cursor(buffered=True)
    cursor.execute("USE PcComponentes")

    # 🔹 Cargar Categorías
    cargar_categorias(cursor)

    # 🔹 Cargar Productos
    cargar_productos(cursor)

    # 🔹 Cargar Características
    cargar_caracteristicas(cursor)

    con.commit()
    cursor.close()
    con.close()
    print("✅ Conexión cerrada.")

# 🔹 Cargar Categorías
def cargar_categorias(cursor):
    df = pd.read_csv("../data/categoriasPortatiles.csv")

    for _, row in df.iterrows():
        sql = """
        INSERT INTO categoriasportatil (id, nombre, url) 
        VALUES (%s, %s, %s) 
        ON DUPLICATE KEY UPDATE nombre = VALUES(nombre), url = VALUES(url);
        """
        cursor.execute(sql, (row["id"], row["nombre"], row["url"]))

    print("✅ Categorías cargadas correctamente.")

# 🔹 Cargar Productos
def cargar_productos(cursor):
    df = pd.read_csv("../data/productos_portatiles_actualizado.csv")

    for _, row in df.iterrows():
        sql = """
        INSERT INTO productosportatil (id, fecha, nombre, url, precio, precio_tachado, rating, opiniones, categoria_id) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
        nombre = VALUES(nombre), 
        url = VALUES(url),
        precio = VALUES(precio),
        precio_tachado = VALUES(precio_tachado),
        rating = VALUES(rating),
        opiniones = VALUES(opiniones),
        categoria_id = VALUES(categoria_id);
        """
        cursor.execute(sql, (
            row["producto_id"],
            row["timestamp"],
            row["nombre"],
            row["url"],
            float(row["precio"].replace("€", "").replace(",", ".")) if pd.notna(row["precio"]) else None,
            float(row["precio_tachado"].replace(".", "").replace("€", "").replace(",", ".")) if pd.notna(row["precio_tachado"]) and row["precio_tachado"] != "0" else None,

            float(row["rating"].split("/")[0].replace(",", ".")) if pd.notna(row["rating"]) else None,  # ✅ Convierte "4,7/5" → 4.7
            int(row["opiniones"].split()[0].replace(".", "")) if pd.notna(row["opiniones"]) else None,

            int(row["categoria_id"]) if pd.notna(row["categoria_id"]) else None
        ))

    print("✅ Productos cargados correctamente.")

def limpiar_numero(valor):
    """
    Limpia valores numéricos eliminando caracteres no numéricos y convirtiendo a int o float.
    """
    if pd.notna(valor):
        valor = str(valor).strip().replace(",", ".")  # Convertir comas a puntos y eliminar espacios
        valor = ''.join(filter(str.isdigit, valor))  # Dejar solo los dígitos

        return int(valor) if valor.isdigit() else None  # Convertir a int si es posible
    return None

def cargar_caracteristicas(cursor):
    df = pd.read_csv("../data/caracteristicas_portatiles_actualizado.csv")

    for _, row in df.iterrows():
        sql = """
        INSERT INTO caracteristicasportatiles (producto_id, processor_speed, processor_cores, ram_gbs, storage_gbs, display_inches, gpu_model, usb_ports, operating_system, weight, battery_mah) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        processor_speed = VALUES(processor_speed),
        processor_cores = VALUES(processor_cores),
        ram_gbs = VALUES(ram_gbs),
        storage_gbs = VALUES(storage_gbs),
        display_inches = VALUES(display_inches),
        gpu_model = VALUES(gpu_model),
        usb_ports = VALUES(usb_ports),
        operating_system = VALUES(operating_system),
        weight = VALUES(weight),
        battery_mah = VALUES(battery_mah);
        """
        cursor.execute(sql, (
            row["producto_id"],
            row["Processor Speed"] if pd.notna(row["Processor Speed"]) else None,
            limpiar_numero(row["Processor Cores"]),
            limpiar_numero(row["RAM Gbs"]),
            limpiar_numero(row["Storage Gbs"]),
            limpiar_numero(row["Display Inches"]),
            row["GPU Model"] if pd.notna(row["GPU Model"]) else None,
            limpiar_numero(row["USB Ports"]),
            row["Operating System"] if pd.notna(row["Operating System"]) else None,
            limpiar_numero(row["Weight"]),
            limpiar_numero(row["Battery mAh"])
        ))

    print("✅ Características cargadas correctamente.")


# 🔹 Ejecutar el script si es el archivo principal
if __name__ == "__main__":
    print("📌 Iniciando carga de datos a MySQL...")
    cargarDatos()
    print("🎉 Carga de datos completada.")
