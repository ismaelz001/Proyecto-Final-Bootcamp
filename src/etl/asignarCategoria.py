import pandas as pd

# 📂 Cargar los archivos
productos_df = pd.read_csv("../../data/productos_portatiles.csv")
categorias_df = pd.read_csv("../../data/categoriasPortatiles.csv")

# 🔹 Diccionario de palabras clave mejorado
categoria_keywords = {
    1: ["gaming", "rtx", "gtx", "i7", "i9", "ryzen 7", "ryzen 9", "3060", "4050", "4060", "4070", "4080", "4090"],
    2: ["gaming avanzado", "rtx 4080", "rtx 4090", "ultra 7", "ultra 9", "i9", "intel core ultra"],
    3: ["trabajo", "estudio", "ofimática", "business", "empresarial"],
    4: ["celeron", "básico", "navegación", "ofimática"],
    5: ["ultraligero", "ultra", "thin", "light", "ligero"],
    6: ["edición", "diseño", "creator", "macbook", "adobe", "photoshop", "video", "arquitectura"],
    7: ["reacondicionado gaming", "segunda mano"],
    8: ["reacondicionado", "usado", "workstation", "profesional"],
    9: ["pccom"],
    10: ["alurin"]
}

# 🔍 Función mejorada para asignar categoría
def asignar_categoria(nombre_producto):
    nombre_producto = str(nombre_producto).lower()  # Convertir a minúsculas para mejor comparación
    
    for categoria_id, keywords in categoria_keywords.items():
        for keyword in keywords:
            if keyword in nombre_producto:
                return categoria_id
    
    return 4  # 🔹 Categoría 4 (Uso básico) por defecto si no encuentra coincidencias

# 🏷 Aplicar función
productos_df["categoria_id"] = productos_df["nombre"].apply(asignar_categoria)

# 📊 Ver cuántos productos aún tienen `categoria_id` en blanco
nulos = productos_df["categoria_id"].isnull().sum()
print(f"❌ Productos sin categoría asignada: {nulos}")

# 📂 Guardar el archivo actualizado
productos_df.to_csv("../../data/productos_portatiles_actualizado.csv", index=False)

print("✅ Archivo productos_portatiles_actualizado.csv generado con categorías asignadas correctamente.")
