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
        CREATE TABLE IF NOT EXISTS categoriasPC (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) UNIQUE,
            url TEXT
        )
    """)
    print("✅ Tabla 'categoriasPC' creada o ya existente.")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categoriasPortatil (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) UNIQUE,
            url TEXT
        )
    """)
    print("✅ Tabla 'categoriasPortatil' creada o ya existente.")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productosComponentes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fecha DATETIME UNIQUE, 
            nombre VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            precio_tachado DECIMAL(10, 2),
            rating DECIMAL(3, 2),
            opiniones INT,
            categoria_id INT,
            FOREIGN KEY (categoria_id) REFERENCES categoriasPC(id)
        )
    """)
    print("✅ Tabla 'productosComponentes' creada o ya existente.")
    
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
            FOREIGN KEY (categoria_id) REFERENCES categoriasPortatil(id)
        )
    """)
    print("✅ Tabla 'productosPortatil' creada o ya existente.")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caracteristicasPortatiles (
            producto_id INT,
            FOREIGN KEY (producto_id) REFERENCES productosPortatil(id),
            caracteristica_1 VARCHAR(255) NOT NULL,
            caracteristica_2 VARCHAR(255) NOT NULL,
            caracteristica_3 VARCHAR(255) NOT NULL,
            caracteristica_4 VARCHAR(255) NOT NULL,
            caracteristica_5 VARCHAR(255) NOT NULL,
            caracteristica_6 VARCHAR(255) NOT NULL,
            caracteristica_7 VARCHAR(255) NOT NULL,
            caracteristica_8 VARCHAR(255) NOT NULL,
            caracteristica_9 VARCHAR(255) NOT NULL,
            caracteristica_10 VARCHAR(255) NOT NULL,
            caracteristica_11 VARCHAR(255) NOT NULL,
            caracteristica_12 VARCHAR(255) NOT NULL,
            caracteristica_13 VARCHAR(255) NOT NULL,
            caracteristica_14 VARCHAR(255) NOT NULL,
            caracteristica_15 VARCHAR(255) NOT NULL,
            caracteristica_16 VARCHAR(255) NOT NULL
        )
    """)
    print("✅ Tabla 'caracteristicasPortatiles' creada o ya existente.")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caracteristicasComponentes (
            producto_id INT,
            FOREIGN KEY (producto_id) REFERENCES productosComponentes(id),
            caracteristica_1 VARCHAR(255) NOT NULL,
            caracteristica_2 VARCHAR(255) NOT NULL,
            caracteristica_3 VARCHAR(255) NOT NULL,
            caracteristica_4 VARCHAR(255) NOT NULL,
            caracteristica_5 VARCHAR(255) NOT NULL,
            caracteristica_6 VARCHAR(255) NOT NULL,
            caracteristica_7 VARCHAR(255) NOT NULL,
            caracteristica_8 VARCHAR(255) NOT NULL,
            caracteristica_9 VARCHAR(255) NOT NULL,
            caracteristica_10 VARCHAR(255) NOT NULL,
            caracteristica_11 VARCHAR(255) NOT NULL,
            caracteristica_12 VARCHAR(255) NOT NULL,
            caracteristica_13 VARCHAR(255) NOT NULL,
            caracteristica_14 VARCHAR(255) NOT NULL,
            caracteristica_15 VARCHAR(255) NOT NULL,
            caracteristica_16 VARCHAR(255) NOT NULL
        )
    """)
    print("✅ Tabla 'caracteristicasComponentes' creada o ya existente.")

# Ejecutar la función para crear las tablas
crearTabla()
