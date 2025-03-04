from conn import conectar
import pandas as pd

def cargarDatos():
    con = conectar()
    if not con:
        print("❌ No se pudo conectar a la base de datos. Abortando...")
        return

    cursor = con.cursor(buffered=True)
    cursor.execute("USE PcComponentes")

    # Cargar el CSV final con clusters
    df_clusters = pd.read_csv("../data/portatiles_clustering_final.csv")
    print(f"✅ CSV cargado con {len(df_clusters)} registros.")

    # Actualizar cada fila con su cluster
    for i, row in df_clusters.iterrows():
        cursor.execute("""
            UPDATE productosportatil
            SET cluster = %s
            WHERE id = %s
        """, (int(row["cluster"]), int(row["producto_id"])))
    
    # Guardar los cambios
    con.commit()
    print("✅ Clusters actualizados correctamente en la base de datos.")

    # Cerrar conexión
    cursor.close()
    con.close()
    print("🔒 Conexión cerrada.")


if __name__ == "__main__":
    print("🚀 Iniciando carga de clusters en la base de datos...")
    cargarDatos()
