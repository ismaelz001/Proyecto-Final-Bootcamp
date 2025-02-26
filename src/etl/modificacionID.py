import pandas as pd
import os

# 🔹 Ruta del archivo CSV de portátiles
archivo_portatiles = "../../data/productosPortatil.csv"

# 🔍 Verificar que el archivo existe antes de procesarlo
if not os.path.exists(archivo_portatiles):
    print(f"⚠️ Archivo no encontrado: {archivo_portatiles}")
    exit()

# 📂 Cargar el CSV asegurando encoding correcto
df_productos_portatil = pd.read_csv(archivo_portatiles, encoding="utf-8")

# 🔄 Renombrar la columna 'id' a 'producto_id' si aún no se llama así
if "id" in df_productos_portatil.columns:
    df_productos_portatil.rename(columns={"id": "producto_id"}, inplace=True)

# 🛠 Eliminar posibles columnas duplicadas
df_productos_portatil = df_productos_portatil.loc[:, ~df_productos_portatil.columns.duplicated()]

# 📌 Verificar las columnas del dataset después de la limpieza
print("✅ Columnas en productos_portatil:", df_productos_portatil.columns)

# 🔢 Convertir 'producto_id' de UUID a INT para facilitar consultas en SQL
df_productos_portatil["producto_id"] = df_productos_portatil["producto_id"].astype(str)
uuid_to_int_portatil = {uuid: i+1 for i, uuid in enumerate(df_productos_portatil["producto_id"].unique())}
df_productos_portatil["producto_id"] = df_productos_portatil["producto_id"].map(uuid_to_int_portatil).astype(int)

# 🔄 Limpiar valores NaN en todas las columnas, reemplazándolos por una cadena vacía ""
df_productos_portatil.fillna("", inplace=True)

# 💾 Sobrescribir el archivo original (Asegúrate de hacer un backup antes)
df_productos_portatil.to_csv(archivo_portatiles, index=False, encoding="utf-8")

print("✅ Archivo de portátiles procesado con éxito:")
print("- 'producto_id' convertido a INT.")
print("- Los valores NaN han sido eliminados.")
print("- Archivo guardado correctamente.")
