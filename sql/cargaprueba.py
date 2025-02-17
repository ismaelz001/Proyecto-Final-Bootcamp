from conn import conectar
import pandas as pd




con = conectar()
if not con:
    print("❌ No se pudo conectar a la base de datos. Abortando...")

    
cursor = con.cursor()
cursor.execute("USE PcComponentes")

# Verificar nombres en productosportatil
cursor.execute("SELECT nombre FROM productosportatil")
productos_portatil = cursor.fetchall()
print("Nombres en productosportatil:", [nombre[0] for nombre in productos_portatil])

# Verificar nombres en productoscomponentes
cursor.execute("SELECT nombre FROM productoscomponentes")
productos_componentes = cursor.fetchall()
print("Nombres en productoscomponentes:", [nombre[0] for nombre in productos_componentes])