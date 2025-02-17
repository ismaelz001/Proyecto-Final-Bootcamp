from conn import conectar
import pandas as pd

def cargarDatos():
    con = conectar()
    if not con:
        print("❌ No se pudo conectar a la base de datos. Abortando...")
        return
    cursor = con.cursor()
    cursor.execute("USE PcComponentes")
    
    # Función para cargar datos desde un CSV a una tabla
    def cargarDatosDesdeCSV(ruta, tabla, columnas_csv, columnas_sql):
        df = pd.read_csv(ruta).fillna("")
        # Convertir todas las columnas a minúsculas
        df.columns = [col.lower() for col in df.columns]
        print(f"Columnas de '{ruta}': {df.columns.tolist()}")
        for _, row in df.iterrows():
            valores = [row[col] for col in columnas_csv]
            try:
                cursor.execute(f"INSERT IGNORE INTO {tabla} ({', '.join(columnas_sql)}) VALUES ({', '.join(['%s']*len(columnas_sql))})", valores)
                print(f"Datos insertados en {tabla}: {valores}")
            except Exception as e:
                print(f"❌ Error al insertar datos en {tabla}: {valores}, Error: {e}")

    # Cargar datos de categoriasPC
    cargarDatosDesdeCSV('../data/categoriasPC.csv', 'categoriaspc', ['nombre', 'url'], ['nombre', 'url'])

    # Cargar datos de categoriasPortatil
    cargarDatosDesdeCSV('../data/categoriasPortatiles.csv', 'categoriasportatil', ['nombre', 'url'], ['nombre', 'url'])

    # Verificar y obtener el mapeo de categorías
    def obtenerCategoriaId(nombre_categoria, tabla):
        cursor.execute(f"SELECT id FROM {tabla} WHERE nombre = %s", (nombre_categoria,))
        result = cursor.fetchone()
        return result[0] if result else None

    # Cargar datos de productosComponentes
    df_productosComponentes = pd.read_csv('../data/productos_componentes_pc.csv').fillna("")
    df_productosComponentes.columns = [col.lower() for col in df_productosComponentes.columns]
    for _, row in df_productosComponentes.iterrows():
        categoria_id = obtenerCategoriaId(row['categoria'], 'categoriaspc')
        if categoria_id:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO productoscomponentes (fecha, nombre, url, precio, precio_tachado, rating, opiniones, categoria_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (row['timestamp'], row['nombre'], row['url'], row['precio'], row['precio_tachado'], row['rating'], row['opiniones'], categoria_id))
                print(f"Datos insertados en productoscomponentes: {row['nombre']}")
            except Exception as e:
                print(f"❌ Error al insertar datos en productoscomponentes: {row['nombre']}, Error: {e}")
        else:
            print(f"⚠️ Advertencia: No se encontró la categoría '{row['categoria']}' en categoriaspc.")

    # Cargar datos de productosPortatil
    df_productosPortatil = pd.read_csv('../data/productosPortatil.csv').fillna("")
    df_productosPortatil.columns = [col.lower() for col in df_productosPortatil.columns]
    for _, row in df_productosPortatil.iterrows():
        categoria_id = obtenerCategoriaId(row['categoria'], 'categoriasportatil')
        if categoria_id:
            try:
                cursor.execute("""
                    INSERT IGNORE INTO productosportatil (fecha, nombre, url, precio, precio_tachado, rating, opiniones, categoria_id) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (row['timestamp'], row['nombre'], row['url'], row['precio'], row['precio_tachado'], row['rating'], row['opiniones'], categoria_id))
                print(f"Datos insertados en productosportatil: {row['nombre']}")
            except Exception as e:
                print(f"❌ Error al insertar datos en productosportatil: {row['nombre']}, Error: {e}")
        else:
            print(f"⚠️ Advertencia: No se encontró la categoría '{row['categoria']}' en categoriasportatil.")

    con.commit()
    print("✅ Datos cargados exitosamente en todas las tablas.")

    # Verificar los productos en la base de datos
    cursor.execute("SELECT nombre FROM productosportatil")
    productos_portatil = cursor.fetchall()
    print(f"Productos en productosportatil: {[nombre[0] for nombre in productos_portatil]}")

    cursor.execute("SELECT nombre FROM productoscomponentes")
    productos_componentes = cursor.fetchall()
    print(f"Productos en productoscomponentes: {[nombre[0] for nombre in productos_componentes]}")

    # Cargar datos de caracteristicasPortatiles
    df_caracteristicasPortatiles = pd.read_csv('../data/caracteristicas_productos_portatil.csv').fillna("")
    df_caracteristicasPortatiles.columns = [col.lower() for col in df_caracteristicasPortatiles.columns]
    print(f"Columnas de 'caracteristicas_productos_portatil.csv': {df_caracteristicasPortatiles.columns.tolist()}")
    for _, row in df_caracteristicasPortatiles.iterrows():
        cursor.execute("""
        SELECT id FROM productosportatil WHERE nombre = %s
        """, (row['producto'],))
        
        result = cursor.fetchone()
        
        if result:
            producto_id = result[0]
            try:
                cursor.execute("""
                    INSERT IGNORE INTO caracteristicasportatiles (
                        producto_id, caracteristica_1, caracteristica_2, caracteristica_3, caracteristica_4, 
                        caracteristica_5, caracteristica_6, caracteristica_7, caracteristica_8, 
                        caracteristica_9, caracteristica_10, caracteristica_11, caracteristica_12, 
                        caracteristica_13, caracteristica_14, caracteristica_15, caracteristica_16
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    producto_id, row['caracteristica_1'], row['caracteristica_2'], row['caracteristica_3'], 
                    row['caracteristica_4'], row['caracteristica_5'], row['caracteristica_6'], 
                    row['caracteristica_7'], row['caracteristica_8'], row['caracteristica_9'], 
                    row['caracteristica_10'], row['caracteristica_11'], row['caracteristica_12'], 
                    row['caracteristica_13'], row['caracteristica_14'], row['caracteristica_15'], 
                    row['caracteristica_16']
                ))
                print(f"Datos de características insertados para el producto {row['producto']}")
            except Exception as e:
                print(f"❌ Error al insertar características para el producto '{row['producto']}': {e}")
        else:
            print(f"⚠️ Advertencia: No se encontró el ID para el producto '{row['producto']}' en productosportatil.")
    
    # Cargar datos de caracteristicasComponentes
    df_caracteristicasComponentes = pd.read_csv('../data/caracteristicas_productos_componentes_pc.csv').fillna("")
    df_caracteristicasComponentes.columns = [col.lower() for col in df_caracteristicasComponentes.columns]
    print(f"Columnas de 'caracteristicas_productos_componentes_pc.csv': {df_caracteristicasComponentes.columns.tolist()}")
    for _, row in df_caracteristicasComponentes.iterrows():
        cursor.execute("""
        SELECT id FROM productoscomponentes WHERE nombre = %s
        """, (row['producto'],))
        
        result = cursor.fetchone()
        
        if result:
            producto_id = result[0]
            try:
                cursor.execute("""
                    INSERT IGNORE INTO caracteristicascomponentes (
                        producto_id, caracteristica_1, caracteristica_2, caracteristica_3, caracteristica_4, 
                        caracteristica_5, caracteristica_6, caracteristica_7, caracteristica_8, 
                        caracteristica_9, caracteristica_10, caracteristica_11, caracteristica_12, 
                        caracteristica_13, caracteristica_14, caracteristica_15, caracteristica_16
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    producto_id, row['caracteristica_1'], row['caracteristica_2'], row['caracteristica_3'], 
                    row['caracteristica_4'], row['caracteristica_5'], row['caracteristica_6'], 
                    row['caracteristica_7'], row['caracteristica_8'], row['caracteristica_9'], 
                    row['caracteristica_10'], row['caracteristica_11'], row['caracteristica_12'], 
                    row['caracteristica_13'], row['caracteristica_14'], row['caracteristica_15'], 
                    row['caracteristica_16']
                ))
                print(f"Datos de características insertados para el producto {row['producto']}")
            except Exception as e:
                print(f"❌ Error al insertar características para el producto '{row['producto']}': {e}")
        else:
            print(f"⚠️ Advertencia: No se encontró el ID para el producto '{row['producto']}' en productoscomponentes.")

    con.commit()
    print("✅ Datos cargados exitosamente en todas las tablas.")

    # Cerrar la conexión
    cursor.close()
    con.close()

# Ejecutar la función para cargar los datos
cargarDatos()