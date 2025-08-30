import requests
import time
import csv
import os
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from urllib.parse import urljoin, urlparse

# Configuración inicial
console = Console()
VISITED = set()
QUEUE = ["https://www.uaa.edu.py"]  # 🔁 SEMILLA CAMBIADA A UAA
MAX_PAGES = 50
DELAY = 1  # Segundos de espera entre requests

# Asegurarse de que la carpeta 'data' existe antes de abrir el archivo
os.makedirs("data", exist_ok=True)

# Función para verificar si un link es de la UAA
def allowed(url):
    return urlparse(url).netloc.endswith("uaa.edu.py")

# Abrir (o crear) el archivo CSV para escribir los logs
with open("data/log.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["#", "url", "status", "elapsed_s", "n_links"])  # Escribir los encabezados

    # Crear una tabla bonita para la consola con Rich
    table = Table(title="Mini Crawler - Recorriendo la UAA", show_lines=True)
    table.add_column("#")
    table.add_column("URL", width=60)
    table.add_column("Code")
    table.add_column("t (s)")
    table.add_column("Links")

    count = 0
    # Mientras haya URLs en la cola y no hayamos alcanzado el máximo...
    while QUEUE and count < MAX_PAGES:
        url = QUEUE.pop(0)  # Tomar la primera URL de la cola

        # Saltar si ya la visitamos o no es de la UAA
        if url in VISITED or not allowed(url):
            continue

        try:
            # 1. Hacer la petición HTTP
            response = requests.get(url, timeout=5)
            status_code = response.status_code
            elapsed_time = round(response.elapsed.total_seconds(), 2)

            # 2. Parsear el HTML para encontrar links
            soup = BeautifulSoup(response.text, "html.parser")
            links_found = []
            for link_tag in soup.find_all('a', href=True):
                full_url = urljoin(url, link_tag['href'])
                links_found.append(full_url)

            # 3. Agregar los nuevos links encontrados a la COLA (QUEUE)
            # (Pero solo los 10 primeros para no saturar)
            QUEUE.extend(links_found[:10])

        except Exception as e:
            # Si algo sale mal (timeout, error de conexión, etc.)
            status_code = "ERROR"
            elapsed_time = 0
            links_found = []
            print(f"Error con {url}: {e}")

        # Marcar la URL como visitada
        VISITED.add(url)
        count += 1

        # 4. Escribir la fila en el CSV
        writer.writerow([count, url, status_code, elapsed_time, len(links_found)])

        # 5. Agregar la fila a la tabla de Rich para mostrarla en consola
        table.add_row(str(count), url[:60], str(status_code), str(elapsed_time), str(len(links_found)))
        console.clear()
        console.print(table)

        # Esperar un tiempo para no saturar el servidor
        time.sleep(DELAY)

print("\n✅ ¡Crawleo completado! Revisa data/log.csv para los resultados.")