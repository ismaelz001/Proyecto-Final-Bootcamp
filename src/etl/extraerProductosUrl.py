import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import uuid
from datetime import datetime
import os
import random
import time

# 🛠️ Configuración del navegador Selenium
options = Options()
options.headless = True  # Para ejecución en segundo plano
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# 📂 Ruta del archivo con URLs (características de portátiles)
archivo_caracteristicas = "../../data/características_portatiles_.csv"
archivo_destino = "../../data/productos_portatiles.csv"

# 🔍 Leer el CSV y extraer URLs sin duplicados
def obtener_urls_desde_caracteristicas(archivo_csv):
    df = pd.read_csv(archivo_csv)
    
    # Asegurar que la columna 'url' existe y eliminar duplicados
    if 'url' in df.columns:
        urls = df['url'].dropna().unique().tolist()
        print(f"✅ Se han encontrado {len(urls)} URLs únicas para procesar.")
        return urls
    else:
        print("❌ Error: No se encontró la columna 'url' en el archivo.")
        return []

# 📥 Función para extraer detalles de un producto desde su URL
def extraer_detalles_producto(url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    producto = {}

    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # 📌 Extraer información
        nombre = soup.find("h1")  
        nombre = nombre.get_text(strip=True) if nombre else "Desconocido"

        precio = soup.find("span", {"id": "pdp-price-current-integer"})
        precio = precio.get_text(strip=True) if precio else 0

        precio_tachado = soup.find("span", {"id": "pdp-price-discount"})
        precio_tachado = precio_tachado.get_text(strip=True) if precio_tachado else 0

        rating = soup.find("span", class_="sc-gIqMXP dDKMBL")
        rating = rating.get_text(strip=True) if rating else 0

        opiniones = soup.find("span", class_="sc-gIqMXP Gmlkk")
        opiniones = opiniones.get_text(strip=True) if opiniones else 0

        # 📝 Guardar en diccionario
        producto = {
            "id": str(uuid.uuid4()),  
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nombre": nombre,
            "url": url,
            "precio": precio,
            "precio_tachado": precio_tachado,
            "rating": rating,
            "opiniones": opiniones
        }

    except Exception as e:
        print(f"⚠️ Error procesando {url}: {e}")
    
    finally:
        driver.quit()

    return producto

# 🔄 Función para actualizar CSV con nuevos productos
def actualizar_csv(nuevos_productos, archivo_csv):
    if os.path.exists(archivo_csv):
        df_existente = pd.read_csv(archivo_csv)
    else:
        df_existente = pd.DataFrame(columns=["id", "timestamp", "nombre", "url", "precio", "precio_tachado", "rating", "opiniones"])

    df_nuevos = pd.DataFrame(nuevos_productos)
    df_combinado = pd.concat([df_existente, df_nuevos], ignore_index=True)

    # 🔹 Eliminar duplicados por URL
    df_combinado.drop_duplicates(subset=["url"], keep="last", inplace=True)

    df_combinado.to_csv(archivo_csv, index=False)
    print(f"✅ Archivo {archivo_csv} actualizado con {len(df_nuevos)} nuevos productos.")

# 🏁 Función principal para procesar las URLs
def extraer_productos(archivo_caracteristicas, archivo_destino, limite=None):
    urls = obtener_urls_desde_caracteristicas(archivo_caracteristicas)
    if limite:
        urls = urls[:limite]  # Limitar la cantidad de URLs para pruebas
    
    print(f"🔍 Procesando {len(urls)} productos...")

    productos = []
    for i, url in enumerate(urls):
        print(f"➡️ Procesando {i+1}/{len(urls)}: {url}")
        producto = extraer_detalles_producto(url)
        if producto:
            productos.append(producto)

        # 🕒 Esperar un poco para evitar bloqueos
        time.sleep(random.uniform(2, 5))

    actualizar_csv(productos, archivo_destino)
    print(f"🎉 Extracción completada y guardada en {archivo_destino}")

# 🔥 EJECUCIÓN: PRIMERO PRUEBA CON 5 PRODUCTOS ANTES DE EJECUTAR TODOS
extraer_productos(archivo_caracteristicas, archivo_destino, limite=None)
