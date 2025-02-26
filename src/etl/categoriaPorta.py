import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL de la página de portátiles en PCComponentes
URL_PC_COMPONENTES = "https://www.pccomponentes.com/portatiles"

# 🔹 Configuración del navegador
options = Options()
options.headless = True  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--start-maximized")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
)

# 🔹 Iniciar Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(URL_PC_COMPONENTES)

# 🔄 Esperar a que el menú de categorías esté disponible
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "nav#menu-seo-links"))
    )
    time.sleep(3)  # Pequeña espera adicional
except Exception:
    print("❌ Error: No se pudo cargar el menú de categorías.")
    driver.quit()
    exit()

# 🔹 Obtener el HTML actualizado después de la carga
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()  # Cerrar Selenium

# 🔹 Buscar el menú de categorías dentro de la sección de portátiles
menu_categorias = soup.find("nav", {"id": "menu-seo-links"})

if not menu_categorias:
    print("❌ No se encontró el menú de categorías de portátiles.")
    exit()

# 🔍 Extraer categorías SOLO de portátiles
categorias_validas = []
for li in menu_categorias.find_all("li"):
    a_tag = li.find("a")
    if a_tag and "href" in a_tag.attrs:
        nombre_categoria = a_tag.get_text(strip=True)
        url_categoria = a_tag["href"]
        
        # 🔹 FILTRO ESTRICTO: Asegurar que SOLO sean portátiles
        if "/portatiles/" in url_categoria and "accesorios" not in url_categoria:
            categorias_validas.append({"nombre": nombre_categoria, "url": url_categoria})

# 🔹 Eliminar duplicados
categorias_finales = []
urls_vistas = set()

for cat in categorias_validas:
    if cat["url"] not in urls_vistas:
        categorias_finales.append(cat)
        urls_vistas.add(cat["url"])

# 🔹 Imprimir y guardar los resultados
if categorias_finales:
    print("\n✅ Categorías de portátiles extraídas correctamente:\n")
    for categoria in categorias_finales:
        print(f"➡️ {categoria['nombre']} → {categoria['url']}")
    
    # Guardar en CSV
    df = pd.DataFrame(categorias_finales)
    df.to_csv('../../data/categoriasPortatiles.csv', index=False, encoding='utf-8')
    print("\n✅ Archivo guardado: categoriasPortatiles.csv")
else:
    print("\n⚠️ No se encontraron categorías de portátiles.")
