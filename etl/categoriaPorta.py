import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
import random

# URL de PCComponentes
url = "https://www.pccomponentes.com/portatiles"

def extraer_categorias_primer_nivel(url):
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

    # Esperar a que el menú de categorías esté disponible
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "aside nav ul li"))
        )
    except Exception as e:
        print("Error: No se pudo cargar el menú de categorías.")
        driver.quit()
        return []

    # Obtener el HTML de la página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    categorias = []

    nav= soup.find("nav",id="menu-seo-links")
    if not nav:
        print("No se encontró el aside en la página.")
        return categorias
    
    # Buscar todos los elementos li dentro del aside
    lis = nav.find_all("li")
    
    print(f"Cantidad de elementos 'li' encontrados: {len(lis)}")

    for li in lis:
        a_tag = li.find("a")
        if a_tag:
            categoria_nombre = a_tag.get_text(strip=True)
            categoria_url = a_tag["href"]
            categorias.append({"nombre": categoria_nombre, "url": categoria_url})

    
    
    return categorias







# Llamar a la función y obtener las categorías de primer nivel
categorias = extraer_categorias_primer_nivel(url)

    # Limitar a un máximo de 10 categorías seleccionadas aleatoriamente
if len(categorias) > 10:
    categorias = random.sample(categorias, 10)
    






# Imprimir las categorías extraídas
for categoria in categorias:
    print(f"Nombre: {categoria['nombre']}, URL: {categoria['url']}")

# Convertir a DataFrame y mostrar
df = pd.DataFrame(categorias)
print(df)

archivoCategoria = df.to_csv('../data/categoriasPortatiles.csv')