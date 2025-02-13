import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import os

def extraer_producto(url):
    # Configuración del navegador
    options = Options()
    options.headless = True  # Ejecutar en modo sin cabeza (sin interfaz gráfica)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Iniciar Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Esperar a que el contenido del producto esté disponible
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "main"))
        )
    except Exception as e:
        print("Error: No se pudo cargar el contenido del producto.")
        driver.quit()
        return []

    # Obtener el HTML de la página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Seleccionar el div específico
    especificaciones_div = soup.find("div", id="pdp-section-features")
    if not especificaciones_div:
        print("Error: No se encontró el div con id pdp-section-features")
        return []

    # Buscar las listas ul dentro del div especificaciones_div
    ul_list = especificaciones_div.find_all("ul")
    if not ul_list:
        print("Error: No se encontraron listas ul dentro del div especificaciones_div")
        return []

    # Extraer los elementos de las listas
    productos = []
    for ul in ul_list:
        lis = ul.find_all("li")
        for li in lis:
            productos.append(li.text.strip())
            if len(productos) >= 16:  # Limitar a 16 productos
                return productos
    return productos

def extraer_url_desde_csv(archivo_csv):
    try:
        df_categorias = pd.read_csv(archivo_csv)
        return df_categorias.to_dict('records')
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo_csv}")
        return []

def extraer_productos(archivo_categoria, archivo_productos):
    categorias = extraer_url_desde_csv(archivo_categoria)
    
    # Limitar a un máximo de 10 categorías seleccionadas aleatoriamente
    if len(categorias) > 10:
        categorias = random.sample(categorias, 10)
    
    todos_productos = []
    for categoria in categorias:
        nombre_categoria = categoria["nombre"]
        url_categoria = categoria["url"]
        print(f"Extrayendo productos de: {nombre_categoria}")
        productos = extraer_producto(url_categoria)
     
        if productos:
            # Agregar el nombre del producto como clave y sus caracteristicas
            producto_dict = {"Producto": nombre_categoria}
            for i, caracteristica in enumerate(productos):
                producto_dict[f"Característica_{i+1}"] = caracteristica
            todos_productos.append(producto_dict)
        
        # Limitar el total de productos a 10
        if len(todos_productos) >= 10:
            print("Límite de 10 productos alcanzado. Deteniendo la extracción.")
            break
    
    # Verificar si el archivo ya existe sumamos la busqueda actual, 10 10 cada ejecuccion
    if os.path.exists(archivo_productos):
        df_existente = pd.read_csv(archivo_productos)
        df_nuevos = pd.DataFrame(todos_productos)
        df_combinado = pd.concat([df_existente, df_nuevos], ignore_index=True)
    else:
        df_combinado = pd.DataFrame(todos_productos)
    
    # Guardar los productos en un archivo CSV
    df_combinado.to_csv(archivo_productos, index=False)
    print(f"Extracción completada y guardada en {archivo_productos}")

# Archivos CSV de los url de extraccion.py
archivo_categoria_componentes_pc = "../data/productosPortatil.csv"

# Archivos CSV para almacenar loa caracteristicas 
archivo_productos_componentes_pc = "../data/caracteristicas_productos_portatil.csv"

# Extraer caracteristicas portatiles
extraer_productos(archivo_categoria_componentes_pc, archivo_productos_componentes_pc)
