import os
from conn import conectar
import pandas as pd

# 🔹 Conexión a la base de datos
conn = conectar()

# 🔹 Diccionario con consultas SQL avanzadas (solo portátiles)
queries = {
    # 📌 Tablas principales de portátiles
    "categorias_portatil": "SELECT * FROM categoriasPortatil",
    "productos_portatil": "SELECT * FROM productosPortatil",
    
    # 📌 Consultas avanzadas sobre portátiles
    "top_10_portatiles_mas_caros": """
        SELECT nombre, precio, categoria_id 
        FROM productosPortatil 
        ORDER BY precio DESC 
        LIMIT 10;
    """,

    "total_portatiles_por_categoria": """
        SELECT c.nombre AS categoria, COUNT(p.id) AS total_productos
        FROM categoriasPortatil c
        LEFT JOIN productosPortatil p ON c.id = p.categoria_id
        GROUP BY c.nombre
        ORDER BY total_productos DESC;
    """,

    "precio_promedio_por_categoria_portatil": """
        SELECT c.nombre AS categoria, ROUND(AVG(p.precio), 2) AS precio_promedio
        FROM categoriasPortatil c
        JOIN productosPortatil p ON c.id = p.categoria_id
        GROUP BY c.nombre
        ORDER BY precio_promedio DESC;
    """,

    "portatil_mejor_rating_por_categoria": """
        SELECT c.nombre AS categoria, p.nombre, p.rating
        FROM productosPortatil p
        JOIN categoriasPortatil c ON p.categoria_id = c.id
        WHERE p.rating = (SELECT MAX(p2.rating) 
                          FROM productosPortatil p2 
                          WHERE p2.categoria_id = p.categoria_id)
        ORDER BY c.nombre;
    """,

    "mayor_descuento_portatil": """
        SELECT nombre, precio, precio_tachado, 
               ROUND(CASE 
                        WHEN precio_tachado > 0 THEN ((precio_tachado - precio) / precio_tachado) * 100
                        ELSE 0 
                    END, 2) AS descuento
        FROM productosPortatil
        WHERE precio_tachado IS NOT NULL AND precio_tachado > 0
        ORDER BY descuento DESC
        LIMIT 10;
    """
}

# 📂 Carpeta de salida
output_dir = "data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # Crea la carpeta si no existe

# 🔄 Ejecutar consultas y exportar los resultados
for nombre_consulta, query in queries.items():
    try:
        df = pd.read_sql_query(query, conn)
        file_path = os.path.join(output_dir, f"{nombre_consulta}.csv")

        if os.path.exists(file_path):
            print(f"♻️ Sobrescribiendo archivo existente: {file_path}")
        else:
            print(f"✅ Creando nuevo archivo: {file_path}")

        df.to_csv(file_path, index=False, encoding="utf-8")

    except Exception as e:
        print(f"❌ Error en la consulta '{nombre_consulta}': {e}")

# 🔒 Cerrar conexión
conn.close()
