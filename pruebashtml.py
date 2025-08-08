import os
from datetime import datetime

# Carpeta donde están los reportes y screenshots
REPORTES_DIR = "."
CAPTURAS_DIR = "screenshots"

# Lista de pruebas (nombres de archivo base)
pruebas = [
    "reporte_login.txt",
    "reporte_prueba_login_crear.txt",
    "reporte_prueba_editar.txt",
    "reporte_prueba_eliminar.txt",
    "reporte_prueba_limite_tarea_vacia.txt",
   
]

html_header = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Reporte de Pruebas Automatizadas</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; background: #f9f9f9;}
    .passed { color: green; font-weight: bold; }
    .failed { color: red; font-weight: bold; }
    .screenshot { max-width: 400px; margin-top: 10px; border: 1px solid #ccc; }
    .test-block { background: white; padding: 15px; margin-bottom: 25px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
  </style>
</head>
<body>
  <h1>Reporte de Pruebas Automatizadas</h1>
"""

html_footer = """
</body>
</html>
"""

def encontrar_captura(base_name):
    # Buscar archivo en screenshots que comience con base_name sin extension txt y termine .png
    base = base_name.replace("reporte_", "").replace(".txt", "")
    for f in os.listdir(CAPTURAS_DIR):
        if f.startswith(base) and f.endswith(".png"):
            return os.path.join(CAPTURAS_DIR, f)
    return None

with open("reporte_completo.html", "w", encoding="utf-8") as html_file:
    html_file.write(html_header)

    for reporte in pruebas:
        ruta_txt = os.path.join(REPORTES_DIR, reporte)
        if not os.path.isfile(ruta_txt):
            continue
        with open(ruta_txt, "r", encoding="utf-8") as f:
            contenido = f.read().strip()

        captura = encontrar_captura(reporte)
        status_class = "passed" if "PASÓ" in contenido else "failed"

        html_file.write(f'<div class="test-block">\n')
        html_file.write(f'<h2>{reporte.replace("reporte_", "").replace(".txt", "").replace("_", " ").title()}</h2>\n')
        html_file.write(f'<p class="{status_class}">{contenido}</p>\n')
        if captura:
            html_file.write(f'<img src="{captura}" alt="Screenshot" class="screenshot">\n')
        else:
            html_file.write("<p><em>No hay captura disponible</em></p>\n")
        html_file.write(f'<p>Fecha generación: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>\n')
        html_file.write('</div>\n\n')

    html_file.write(html_footer)

print("Reporte HTML generado: reporte_completo.html")
