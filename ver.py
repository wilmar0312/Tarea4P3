from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime

BASE_LOGIN_URL = "http://localhost:8000/login.html"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

try:
    # Paso 1: Abrir login.html
    driver.get(BASE_LOGIN_URL)
    time.sleep(1)

    # Paso 2: Ingresar usuario y contraseña válidos
    driver.find_element(By.ID, "username").send_keys("admin")   # Cambia si tu user es otro
    driver.find_element(By.ID, "password").send_keys("1234")    # Cambia si tu pass es otro
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)  # Esperar que redirija

    # Validar que esté en crud.html
    if "crud.html" not in driver.current_url:
        raise Exception("No se redirigió al CRUD después del login")

    # Paso 3: Contar tareas actuales para comparar luego
    tareas_antes = driver.find_elements(By.CSS_SELECTOR, "#taskList li")
    cantidad_antes = len(tareas_antes)

    # Paso 4: Intentar agregar tarea vacía (cadena vacía)
    task_input = driver.find_element(By.ID, "taskInput")
    task_input.clear()
    task_input.send_keys("")  # vacío
    driver.find_element(By.CSS_SELECTOR, "#taskForm button[type='submit']").click()
    time.sleep(1)

    # Paso 5: Contar tareas después de intentar agregar
    tareas_despues = driver.find_elements(By.CSS_SELECTOR, "#taskList li")
    cantidad_despues = len(tareas_despues)

    # Validar que no se agregó tarea vacía (cantidad igual)
    if cantidad_despues == cantidad_antes:
        resultado = "✅ Prueba límite crear tarea vacía: PASÓ"
    else:
        resultado = "❌ Prueba límite crear tarea vacía: FALLÓ"

    # Captura con timestamp para evitar sobrescribir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/prueba_limite_tarea_vacia_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Guardar reporte
    with open("reporte_prueba_limite_tarea_vacia.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print("❌ Error en prueba límite tarea vacía:", e)

finally:
    time.sleep(3)
    driver.quit()
