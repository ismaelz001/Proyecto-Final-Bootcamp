import os
from conn import conectar
import pandas as pd

# Conexión a la base de datos
conn = conectar()

# Diccionario con consultas SQL avanzadas
queries = {
    "categorias_pc": "SELECT * FROM categoriasPC",
    "categorias_portatil": "SELECT * FROM categoriasPortatil",
    "productos_componentes": "SELECT * FROM productosComponentes",
    "productos_portatil": "SELECT * FROM productosPortatil",
    "caracteristicas_componentes": "SELECT * FROM caracteristicasComponentes",
    "caracteristicas_portatil": "SELECT * FROM caracteristicasPortatil",

    "top_10_productos_mas_caros": """
        SELECT nombre, precio, categoria_id 
        FROM productosComponentes 
        ORDER BY precio DESC 
        LIMIT 10;
    """,

    "total_productos_por_categoria": """
        SELECT c.nombre AS categoria, COUNT(p.id) AS total_productos
        FROM categoriasPC c
        LEFT JOIN productosComponentes p ON c.id = p.categoria_id
        GROUP BY c.nombre
        ORDER BY total_productos DESC;
    """,

    "precio_promedio_por_categoria": """
        SELECT c.nombre AS categoria, ROUND(AVG(p.precio), 2) AS precio_promedio
        FROM categoriasPC c
        JOIN productosComponentes p ON c.id = p.categoria_id
        GROUP BY c.nombre
        ORDER BY precio_promedio DESC;
    """,

    "producto_mejor_rating_por_categoria": """
        SELECT c.nombre AS categoria, p.nombre, p.rating
        FROM productosComponentes p
        JOIN categoriasPC c ON p.categoria_id = c.id
        WHERE p.rating = (SELECT MAX(p2.rating) 
                          FROM productosComponentes p2 
                          WHERE p2.categoria_id = p.categoria_id)
        ORDER BY c.nombre;
    """,

    "mayor_descuento_producto": """
        SELECT nombre, precio, precio_tachado, 
               ROUND(CASE 
                        WHEN precio_tachado > 0 THEN ((precio_tachado - precio) / precio_tachado) * 100
                        ELSE 0 
                    END, 2) AS descuento
        FROM productosComponentes
        WHERE precio_tachado IS NOT NULL AND precio_tachado > 0
        ORDER BY descuento DESC
        LIMIT 10;
    """
}

# Carpeta de salida
output_dir = "data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # Crea la carpeta si no existe

# Ejecutar consultas y exportar los resultados
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

# Cerrar conexión
conn.close()
