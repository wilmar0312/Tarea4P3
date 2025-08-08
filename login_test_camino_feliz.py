from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

# Configuración del driver de Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Ruta al archivo login.html en tu computadora
BASE_URL = "file:///C:\\Users\\wilma\\Desktop\\prueba\\login.html"
  # CAMBIAR

# Carpeta para capturas
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

# Iniciar prueba (Camino Feliz)
driver.get(BASE_URL)

# Llenar campos (usa credenciales que tu login acepte)
driver.find_element(By.ID, "username").send_keys("admin")
driver.find_element(By.ID, "password").send_keys("")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# Esperar a que redireccione
time.sleep(1)

# Validar resultado
if "crud.html" in driver.current_url:
    resultado = "✅ Camino feliz login: PASÓ"
else:
    resultado = "❌ Camino feliz login: FALLÓ"

# Guardar captura y reporte
driver.save_screenshot("screenshots/login_camino_feliz.png")
with open("reporte_login.txt", "w", encoding="utf-8") as f:
    f.write(resultado + "\n")

print(resultado)

driver.quit()
