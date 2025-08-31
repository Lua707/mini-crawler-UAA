# Mini Crawler - UAA

Este proyecto implementa un **crawler web ético y minimalista**, desarrollado como prototipo para **DataExplore**.  
Su objetivo es recorrer el sitio de la **Universidad Autónoma de Asunción (UAA)** para recolectar información de manera **automatizada, eficiente y respetuosa** con las normas del servidor.

El prototipo:
- Utiliza semillas de inicio (`https://www.uaa.edu.py` y otras URLs adicionales).
- Respeta estrictamente las reglas definidas en el archivo `robots.txt`.
- Se limita a un máximo de **50 solicitudes por ejecución**, con un **delay de 1 segundo** entre cada una.
- Filtra contenido no-HTML (ejemplo: PDFs, imágenes).
- En pruebas alcanzó **30 URLs únicas**, lo que permitió comprobar la complejidad de crawlear sitios reales con enlaces limitados.

## Requisitos
Instala las dependencias con:
```bash
pip install -r requirements.txt

## Uso
Ejecuta el crawler desde la raíz del proyecto con:
```bash
python src/mini_crawler.py

## Uso de Git (flujo básico)

Para mantener actualizado tu repositorio en GitHub:

1.Añadir cambios al área de preparación: 
```bash
git add .

2.Confirmar cambios con un mensaje descriptivo: 
```bash
git commit -m "Descripción breve de lo que hiciste"

3.Subir los cambios a GitHub (rama principal): 
```bash
git push origin main

4.Actualizar tu repositorio local con los cambios del remoto: 
```bash
git pull origin main

## Notas importantes

- Este crawler fue diseñado con fines educativos y de prototipado.

- No busca realizar scraping masivo ni sobrecargar servidores.

- Se puede ampliar a otros dominios de universidades paraguayas.

- Limitación observada: incluso con múltiples semillas, solo se rastrearon 30 URLs en el dominio objetivo. Esto aporta un aprendizaje valioso para la siguiente fase del proyecto.

## Futuras mejoras

- Ampliar el conjunto de semillas iniciales.

- Implementar un sistema de logs más detallado.

- Exportar resultados en formatos estructurados (CSV, JSON).

- Mejorar la estrategia de descubrimiento de enlaces para alcanzar más profundidad en la navegación.