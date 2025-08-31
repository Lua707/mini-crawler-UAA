# IMPORTAR LIBRERÍAS
import requests
import time
import csv
import os
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

# CONFIGURACIÓN INICIAL
console = Console()
VISITED = set()
# SEMILLAS MEJORADAS: Usamos URLs que sabemos que existen y son ricas en enlaces.
QUEUE = [
    # Semillas principales 
    "https://www.uaa.edu.py",
    "https://www.uaa.edu.py/carreras", 
    "https://www.uaa.edu.py/documentos",
    "https://www.uaa.edu.py/instalaciones",
    "https://www.uaa.edu.py/acreditaciones",
    # CEBO para forzar nuevos caminos
    "https://www.uaa.edu.py/facultades/ciencias-tecnologias/ingenieria-informatica",
    "https://www.uaa.edu.py/facultades/ciencias-tecnologias",
    "https://www.uaa.edu.py/facultades/ciencias-educacion-comunicacion",
    "https://www.uaa.edu.py/facultades/ciencias-salud/medicina",
    "https://www.uaa.edu.py/facultades/ciencias-salud",
    "https://www.uaa.edu.py/facultades/ciencias-economicas-empresariales/contaduria",
    "https://www.uaa.edu.py/la-universidad/historia",
    "https://www.uaa.edu.py/investigacion/proyectos",
    "https://www.uaa.edu.py/noticias/eventos"
]
MAX_PAGES = 50
DELAY = 1  # Segundos entre requests (cumple 1 req/segundo)
USER_AGENT = "mi-mini-crawler-educativo"  # Identificador ético

# FUNCIONES (F.) AUXILIARES

# F. 1: Verificar que el dominio es de la UAA
def allowed(url):
    return urlparse(url).netloc.endswith("uaa.edu.py")

# F. 2: Respetar robots.txt
def respect_robots(url, user_agent=USER_AGENT):
    """
    Verifica si según robots.txt está permitido crawlear la URL.
    Returns True si está permitido, False si está prohibido.
    """
    try:
        # Obtener la base del dominio para construir la URL de robots.txt
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        robots_url = f"{base_url}/robots.txt"
        
        # Crear el parser y leer robots.txt
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()  # Lee y parsea el archivo robots.txt
        
        # Consultar si user-agent puede acceder a la URL
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        # Si hay cualquier error (ej: no existe robots.txt), se asume que está permitido por defecto
        print(f"Advertencia robots.txt para {url}: {e}. Se procede por defecto.")
        return True

# PROGRAMA PRINCIPAL 

# Asegurarse de que 'data' existe
os.makedirs("data", exist_ok=True)

# Abrir (o crear) el archivo CSV para escribir los logs
with open("data/log_mejora.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["#", "url", "status", "elapsed_s", "n_links"])  # Escribir los encabezados

    # Crear tabla para la consola con Rich
    table = Table(title="Mini Crawler - Recorriendo la UAA", show_lines=True)
    table.add_column("#")
    table.add_column("URL", width=60)
    table.add_column("Code")
    table.add_column("t (s)")
    table.add_column("Links")

    count = 0
    # Mientras haya URLs en la cola y no se haya alcanzado el máximo:
    while QUEUE and count < MAX_PAGES:
        url = QUEUE.pop()  # saca el ÚLTIMO elemento (LIFO -> DFS)

        # VERIFICACIÓN COMPLETA: ¿Ya se ha visitado? ¿Es de la UAA? ¿Robots.txt lo permite?
        if url in VISITED or not allowed(url) or not respect_robots(url):
            continue  # Si no pasa alguna, saltar a la siguiente URL

        try:
            # 1. Hacer la petición HTTP 
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, timeout=5, headers=headers)
            status_code = response.status_code
            elapsed_time = round(response.elapsed.total_seconds(), 2)

            # 2. Parsear el HTML para encontrar links (VERSIÓN MEJORADA)
            soup = BeautifulSoup(response.text, "html.parser")
            links_found = []

            # Lista de extensiones de archivo que queremos IGNORAR
            extensiones_no_deseadas = ('.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.zip', '.ppt', '.pptx')

            for link_tag in soup.find_all('a', href=True):
                raw_url = link_tag['href']
                # Construir URL absoluta
                full_url = urljoin(url, raw_url)

                # Filtro: verificar que sea interesante
                # 1. URL HTTP/HTTPS (no "mailto:", "tel:", "javascript:")
                if not full_url.startswith('http'):
                    continue
                # 2. Mismo dominio 
                if not allowed(full_url):
                    continue
                # 3. No sea ancla (ej: "uaa.edu.py/#noticias")
                if '#' in full_url:
                    full_url = full_url.split('#')[0]  # Quitar todo después del #

                # 4. MEJORA: Filtrar por extensiones no deseadas 
                if full_url.lower().endswith(extensiones_no_deseadas):
                    continue # Si es un archivo, saltar y no agregar

                # Si pasa: agrega la URL a la lista
                if full_url not in links_found:  # Evita duplicados en la misma página
                    links_found.append(full_url)

            # 3. Agregar los nuevos links encontrados a la COLA (QUEUE)
            QUEUE.extend(links_found[:15])  # Limite a 15 links para no saturar

        except Exception as e:
            # Si algo sale mal (timeout, error de conexión, etc.)
            status_code = "ERROR"
            elapsed_time = 0
            links_found = []
            print(f"Error con {url}: {e}")

        # Marcar la URL como visitada y aumentar el contador
        VISITED.add(url)
        count += 1

        # 4. Escribir la fila en el CSV
        writer.writerow([count, url, status_code, elapsed_time, len(links_found)])

        # 5. Agregar la fila a la tabla de Rich para mostrar en consola
        table.add_row(str(count), url[:60], str(status_code), str(elapsed_time), str(len(links_found)))
        console.clear()
        console.print(table)

        # Esperar un tiempo para no saturar el servidor (cumple el delay de 1s)
        time.sleep(DELAY)

print("\n✅ ¡Crawleo completado! Revisa data/log_mejora.csv para los resultados.")