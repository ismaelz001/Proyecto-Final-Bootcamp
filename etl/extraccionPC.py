import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import uuid
from datetime import datetime
import os

# Configuración del navegador
options = Options()
options.headless = True  # Ejecución en segundo plano
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

def extraer_productos(url_categoria, categoria_nombre):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    productos = []
    try:
        driver.get(url_categoria)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "main")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        main = soup.find("main")
        if main is None:
            raise Exception("No se encontró el elemento 'main'")
        
        # Buscar todos los productos dentro del 'main'
        for product in main.find_all("a", href=True):
            try:
                nombre = product.get("data-product-name", "Desconocido")
                
                if nombre == "Desconocido":
                    continue 
                #saltamos iteracion Desconocido
                
                url = product["href"]
                precio_element = product.find("span", {"data-e2e": "price-card"})
                precio = precio_element.get_text(strip=True) if precio_element else "N/A"
                precio_tachado_element = product.find("span", {"data-e2e": "crossedPrice"})
                precio_tachado = precio_tachado_element.get_text(strip=True) if precio_tachado_element else "N/A"
                rating_element = product.find("span", class_="sc-gIqMXP dDKMBL")
                rating = rating_element.get_text(strip=True) if rating_element else "N/A"
                opiniones_element = product.find("span", class_="sc-gIqMXP Gmlkk")
                opiniones = opiniones_element.get_text(strip=True) if opiniones_element else "N/A"
                
                productos.append({
                    "id": str(uuid.uuid4()),  
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "nombre": nombre,
                    "url": url,
                    "precio": precio,
                    "precio_tachado": precio_tachado,
                    "rating": rating,
                    "opiniones": opiniones,
                    "categoria": categoria_nombre
                })
                
            except Exception as e:
                print(f"Error procesando un producto: {e}")
    except Exception as e:
        print(f"Error en la categoría {categoria_nombre}: {e}")
    finally:
        driver.quit()
    return productos


def actualizar_productos(nuevos_productos, archivo_csv):
    # Si el archivo CSV ya existe, cargarlo
    if os.path.exists(archivo_csv):
        df_existente = pd.read_csv(archivo_csv)
    else:
        df_existente = pd.DataFrame(columns=["id", "timestamp", "nombre", "url", "precio", "precio_tachado", "rating", "opiniones", "categoria"])
    
    # Convertir los nuevos productos a DataFrame
    df_nuevos = pd.DataFrame(nuevos_productos)
    
    # Combinar los DataFrames existente y nuevo
    df_combinado = pd.concat([df_existente, df_nuevos], ignore_index=True)
    
    # Eliminar duplicados basados en la URL del producto
    df_combinado.drop_duplicates(subset=["url"], keep="last", inplace=True)
    
    # Guardar el DataFrame actualizado en el archivo CSV
    df_combinado.to_csv(archivo_csv, index=False)
    print(f"Archivo {archivo_csv} actualizado con {len(df_nuevos)} nuevos productos.")

def extraer_categorias_desde_csv(archivo_csv):
    try:
        df_categorias = pd.read_csv(archivo_csv)
        return df_categorias.to_dict('records')
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_csv}")
        return []

def extraer_productos_para_categorias(archivo_categoria, archivo_productos):
    categorias = extraer_categorias_desde_csv(archivo_categoria)
    todos_productos = []
    for categoria in categorias:
        nombre_categoria = categoria["nombre"]
        url_categoria = categoria["url"]
        print(f"Extrayendo productos de: {nombre_categoria}")
        productos = extraer_productos(url_categoria, nombre_categoria)
        todos_productos.extend(productos)
    actualizar_productos(todos_productos, archivo_productos)
    print(f"Extracción completada y guardada en {archivo_productos}")

# Archivos CSV de categorías
archivo_categoria_componentes_pc = "../data/categoriasPC.csv"

# Archivos CSV para almacenar los productos
archivo_productos_componentes_pc = "../data/productos_componentes_pc.csv"

# Extraer productos para categorías de Componentes de PC
extraer_productos_para_categorias(archivo_categoria_componentes_pc, archivo_productos_componentes_pc)
