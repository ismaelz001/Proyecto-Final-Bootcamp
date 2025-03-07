from conn import conectar
import pandas as pd 

def crearTabla():
    con = conectar()
    if not con:
        print("❌ No se pudo conectar a la base de datos. Abortando...")
        return
    cursor = con.cursor()
    print("🛠️ Creando tablas en la base de datos...")

    cursor.execute("""
                   CREATE DATABASE IF NOT EXISTS PcComponentes
                   """)
    print("✅ Base de datos 'PcComponentes' creada o ya existente.")

    cursor.execute("""
                   USE PcComponentes
                   """)
    print("✅ Usando base de datos 'PcComponentes'.")
    
 
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoriasPortatil (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) UNIQUE,
            url TEXT
        )
    """)
    print("✅ Tabla 'categoriasPortatil' creada o ya existente.")
    
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productosPortatil (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATETIME UNIQUE, 
            nombre VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            precio_tachado DECIMAL(10, 2),
            rating DECIMAL(3, 2),
            opiniones INT,
            categoria_id INT,         
            descuento_porcentaje DECIMAL(5, 2),
            marca VARCHAR(255),                 
            FOREIGN KEY (categoria_id) REFERENCES categoriasPortatil(id)
        )
    """)
    print("✅ Tabla 'productosPortatil' creada o ya existente.")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS caracteristicasPortatiles (
        id INT AUTO_INCREMENT PRIMARY KEY,
        producto_id INT NOT NULL,
        processor_speed VARCHAR(50),
        processor_cores INT(11),
        ram_gbs INT(11),
        storage_gbs INT(11),
        display_inches DECIMAL(10,5),
        gpu_model VARCHAR(100),
        usb_ports INT(11),
        operating_system VARCHAR(100),
        weight DECIMAL(6,2),
        battery_mah INT(11),
        FOREIGN KEY (producto_id) REFERENCES productosPortatil(id)
    )
""")
print("✅ Tabla 'caracteristicasPortatiles' creada o ya existente.")

    
   

# Ejecutar la función para crear las tablas
crearTabla()
