
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# url pcomponentes
url = "https://www.pccomponentes.com"

def extraer_categoriasPrimerNivel(url):
    # Configurar opciones del navegador
    options = Options()
    options.headless = True  # Ejecutar en modo headless (sin interfaz gráfica)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    # Iniciar el navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    # Obtener el contenido de la página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Extraer los productos de la página principal
    categorias = []

    # Buscar el aside
    asides = soup.find_all("aside", class_="sc-ceEKmU dcglbf")
    if not asides:
        print("No se encontraron elementos 'aside' con la clase especificada.")
        return []

    for aside in asides:
        print("Contenido del aside:", aside.prettify())  # Añadir mensaje de depuración para imprimir el contenido del aside
        # Buscar todos los elementos nav dentro del aside
        navs = aside.find_all("nav")
        if not navs:
            print("No se encontraron elementos 'nav' dentro del 'aside'.")
            continue

        for nav in navs:
            # Buscar la lista ul dentro del nav con la clase específica
            uls = nav.find_all("ul")
            if not uls:
                print("No se encontraron elementos 'ul' dentro del 'nav'.")
                continue

            for ul in uls:
                # Buscar los elementos li con id que comienza con 'second-level-'
                lis = ul.find_all("li", id=lambda x: x and x.startswith("second-level-"))
                if not lis:
                    print("No se encontraron elementos 'li' dentro del 'ul'.")
                    continue

                for li in lis:
                    categoria_nombre = li.get_text(strip=True)
                    a_tag = li.find("a")
                    categoria_url = a_tag["href"] if a_tag else "URL no disponible"
                    categorias.append({"nombre": categoria_nombre, "url": categoria_url})
    
    return categorias

# Llamar a la función y obtener las categorías de primer nivel
categorias_primer_nivel = extraer_categoriasPrimerNivel(url)

# Imprimir las categorías extraídas
for categoria in categorias_primer_nivel:
    print(f"Nombre: {categoria['nombre']}, URL: {categoria['url']}")

df1 = pd.DataFrame(categorias_primer_nivel)
print(df1)
