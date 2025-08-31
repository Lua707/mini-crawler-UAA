import pandas as pd
import matplotlib.pyplot as plt
import os
os.makedirs('docs', exist_ok=True)

# 1) Leer los datos
df = pd.read_csv('data/log.csv')

# Por si vienen como texto, convertir a número
df['elapsed_s'] = pd.to_numeric(df['elapsed_s'], errors='coerce').fillna(0)
df['#'] = pd.to_numeric(df['#'], errors='coerce')

# 2) Barras: cuántas páginas dieron cada código (200, 404, 500...)
status_counts = df['status'].value_counts()
plt.figure(figsize=(8, 5))
status_counts.plot(kind='bar')
plt.title('Distribución de Códigos de Estado HTTP')
plt.xlabel('Código de Estado')
plt.ylabel('Número de Páginas')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('docs/grafica_status.png')
plt.close()

# 3) Línea: cuánto tardó cada página en responder
plt.figure(figsize=(10, 5))
plt.plot(df['#'], df['elapsed_s'], marker='o', linestyle='-')
plt.title('Tiempo de Respuesta por Página Visitada')
plt.xlabel('Número de Página (#)')
plt.ylabel('Tiempo de Respuesta (segundos)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig('docs/grafica_tiempos.png')
plt.close()

print("✅ Listo: se guardaron docs/grafica_status.png y docs/grafica_tiempos.png")
