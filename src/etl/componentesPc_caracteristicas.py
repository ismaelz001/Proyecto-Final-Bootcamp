import pandas as pd
import re
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 🔹 Configuración del navegador Selenium
def iniciar_driver():
    options = Options()
    options.headless = True  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🔹 Función para limpiar valores y extraer solo números
def limpiar_valor(valor):
    match = re.search(r"([\d,.]+)\s?([\w%°]*)", valor)
    if match:
        numero = match.group(1).replace(",", ".")
        unidad = match.group(2).strip()
        return float(numero) if numero.replace(".", "").isdigit() else numero
    return None

# 🔹 Función para extraer características numéricas
def extraer_caracteristicas_numericas(url):
    driver = iniciar_driver()
    driver.get(url)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "main")))
    except:
        print(f"⚠️ No se pudo cargar {url}")
        driver.quit()
        return {}

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    especificaciones_div = soup.find("div", id="pdp-section-features")
    if not especificaciones_div:
        print(f"⚠️ No se encontró la sección de especificaciones en {url}")
        return {}

    h2_especificaciones = especificaciones_div.find("h2", string=re.compile("Especificaciones", re.IGNORECASE))
    if not h2_especificaciones:
        print(f"⚠️ No se encontró el título de especificaciones en {url}")
        return {}

    ul_list = h2_especificaciones.find_next_siblings("ul")

    caracteristicas = {}
    for ul in ul_list:
        for li in ul.find_all("li", recursive=False):  
            strong = li.find("strong")
            if strong:
                clave = strong.text.strip().lower().replace(" ", "_")
                valor = li.text.replace(strong.text, "").strip()

                # 🔍 Si hay otra UL dentro, extraer los valores de sus LI internos
                sub_ul = li.find("ul")
                if sub_ul:
                    valores = [limpiar_valor(sub_li.text.strip()) for sub_li in sub_ul.find_all("li")]
                    valores = [str(v) for v in valores if v is not None]  
                    if valores:
                        caracteristicas[clave] = ", ".join(valores)
                else:
                    valor_limpio = limpiar_valor(valor)
                    if valor_limpio is not None:
                        caracteristicas[clave] = valor_limpio

    return caracteristicas

# 🔹 Función para extraer URLs desde CSV
def extraer_urls_csv(archivo_csv, limite=5):
    try:
        df = pd.read_csv(archivo_csv)
        return df.head(limite).to_dict("records")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo_csv}")
        return []

# 🔹 Función principal para recorrer productos y guardar cada uno en un CSV separado
def extraer_caracteristicas(archivo_productos, carpeta_salida):
    productos = extraer_urls_csv(archivo_productos)

    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    for producto in productos:
        nombre_producto = producto["nombre"]
        url_producto = producto["url"]
        print(f"🔍 Extrayendo características de: {nombre_producto}")

        caracteristicas = extraer_caracteristicas_numericas(url_producto)

        if caracteristicas:
            # 📌 Asegurar que "producto" y "url" sean las primeras columnas
            datos_ordenados = {"producto": nombre_producto, "url": url_producto}
            datos_ordenados.update(caracteristicas)  # Añadir las especificaciones después
            
            df = pd.DataFrame([datos_ordenados])

            # 🔥 Crear un CSV para cada producto
            nombre_archivo = f"{carpeta_salida}/caracteristicas_{nombre_producto.replace(' ', '_')}.csv"
            df.to_csv(nombre_archivo, index=False)
            print(f"✅ Características guardadas en {nombre_archivo}")
        else:
            print(f"⚠️ No se encontraron características para {nombre_producto}")

        time.sleep(1)  

# 📌 Archivos CSV de entrada y salida
archivo_productos = "../../data/productos_componentes_pc_limpio.csv"
carpeta_salida = "../../data/caracteristicas_por_producto"

# 🔥 Ejecutar extracción
extraer_caracteristicas(archivo_productos, carpeta_salida)

