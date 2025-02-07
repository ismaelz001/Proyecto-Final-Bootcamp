import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

import requests

# url pcomponentes
url = "https://www.pccomponentes.com/?s_kwcid=AL!14405!3!600262053045!b!!g!!pccomponentes&gad_source=1&gclid=CjwKCAiA2JG9BhAuEiwAH_zf3mOsa0N8DvFr3_3w81OaubnqOB42gHDeSowabmsdmtla-V2kmEnv9BoC7m4QAvD_BwE"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')



def extraer_categoriasPrimerNivel(url):
    
    # Extraer los productos de la página principal
    categorias = []


 # Verificar si la solicitud fue exitosa
    if response.status_code != 200:
        print(f"Error al acceder a la página: {response.status_code}")
        return []
    #primero necesitamos la primera categoria, despues la segunda
    #asi hasta llegar a los productos

    # Buscar el aside
    for aside in soup.find_all("aside", class_="sc-ceEKmU dcglbf"):
        # Buscar el nav dentro del aside
        for nav in aside.find_all("nav", class_="sc-czZcoD gNFhmR at-element-click-tracking at-element-marker"):
            # Buscar la lista ul dentro del nav
            for ul in nav.find_all("ul"):
                # Buscar los elementos li dentro de la lista ul
                for li in ul.find_all("li"):
                    categoria_nombre = li.get_text(strip=True)
                    categoria_url = li.find("a")["href"]
                    categorias.append({"nombre": categoria_nombre, "url": categoria_url})
    
    return categorias

# Llamar a la función y obtener las categorías de primer nivel
categorias_primer_nivel = extraer_categoriasPrimerNivel(url)

# Imprimir las categorías extraídas
for categoria in categorias_primer_nivel:
    print(f"Nombre: {categoria['nombre']}, URL: {categoria['url']}")