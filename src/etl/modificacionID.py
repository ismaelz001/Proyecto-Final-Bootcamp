import pandas as pd
import os

# Rutas de los archivos CSV originales
archivos = {
    "productos_portatil": "../../data/productosPortatil.csv",
    "productos_componentes_pc": "../../data/productos_componentes_pc.csv"
}

# Verificar que los archivos existen antes de procesarlos
for key, file_path in archivos.items():
    if not os.path.exists(file_path):
        print(f"⚠️ Archivo no encontrado: {file_path}")
        exit()

# Cargar los CSVs asegurando encoding correcto
df_productos_portatil = pd.read_csv(archivos["productos_portatil"], encoding="utf-8")
df_productos_componentes_pc = pd.read_csv(archivos["productos_componentes_pc"], encoding="utf-8")

# Renombrar la columna 'id' a 'producto_id' si aún no se llama así
if "id" in df_productos_portatil.columns:
    df_productos_portatil.rename(columns={"id": "producto_id"}, inplace=True)
if "id" in df_productos_componentes_pc.columns:
    df_productos_componentes_pc.rename(columns={"id": "producto_id"}, inplace=True)

# 🛠 Eliminar duplicados de columnas en df_productos_componentes_pc
df_productos_componentes_pc = df_productos_componentes_pc.loc[:, ~df_productos_componentes_pc.columns.duplicated()]

# Verificar que ambas columnas existen
print("Columnas en productos_portatil:", df_productos_portatil.columns)
print("Columnas en productos_componentes_pc:", df_productos_componentes_pc.columns)

# Asegurarnos de que 'producto_id' es una Series
df_productos_portatil["producto_id"] = df_productos_portatil["producto_id"].astype(str)
df_productos_componentes_pc["producto_id"] = df_productos_componentes_pc["producto_id"].astype(str)

# Crear mapeos de UUID a INT para cada archivo
uuid_to_int_portatil = {uuid: i+1 for i, uuid in enumerate(df_productos_portatil["producto_id"].unique())}
uuid_to_int_componentes_pc = {uuid: i+1 for i, uuid in enumerate(df_productos_componentes_pc["producto_id"].unique())}

# Reemplazar UUIDs por INTs en cada dataframe
df_productos_portatil["producto_id"] = df_productos_portatil["producto_id"].map(uuid_to_int_portatil).astype(int)
df_productos_componentes_pc["producto_id"] = df_productos_componentes_pc["producto_id"].map(uuid_to_int_componentes_pc).astype(int)

# Limpiar valores NaN en todas las columnas, reemplazándolos por una cadena vacía ""
df_productos_portatil.fillna("", inplace=True)
df_productos_componentes_pc.fillna("", inplace=True)

# Sobrescribir los archivos originales (Asegúrate de hacer un backup antes)
df_productos_portatil.to_csv(archivos["productos_portatil"], index=False, encoding="utf-8")
df_productos_componentes_pc.to_csv(archivos["productos_componentes_pc"], index=False, encoding="utf-8")

print("✅ Los archivos han sido modificados con éxito:")
print("- 'producto_id' está en formato INT.")
print("- Los valores NaN han sido eliminados.")
print("- Los archivos se han guardado correctamente.")
