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
    driver.find_element(By.ID, "username").send_keys("admin")   
    driver.find_element(By.ID, "password").send_keys("1234")    
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)  # Esperar que redirija

    # Validar que esté en crud.html
    if "crud.html" not in driver.current_url:
        raise Exception("No se redirigió al CRUD después del login")

    # Paso 3: Crear una tarea para eliminar
    tarea = "Tarea a eliminar"
    task_input = driver.find_element(By.ID, "taskInput")
    task_input.send_keys(tarea)
    driver.find_element(By.CSS_SELECTOR, "#taskForm button[type='submit']").click()
    time.sleep(1)

    # Paso 4: Eliminar la primera tarea (botón 'Eliminar')
    eliminar_btn = driver.find_element(By.CSS_SELECTOR, "#taskList li:first-child button.btn-danger")
    eliminar_btn.click()
    time.sleep(1)

    # Paso 5: Validar que la tarea ya no aparece en la lista
    tareas = driver.find_elements(By.CSS_SELECTOR, "#taskList li span")
    textos = [t.text for t in tareas]

    if tarea not in textos:
        resultado = "✅ Prueba eliminar tarea: PASÓ"
    else:
        resultado = "❌ Prueba eliminar tarea: FALLÓ"

    # Captura con timestamp para evitar sobrescribir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"screenshots/prueba_eliminar_tarea_{timestamp}.png"
    driver.save_screenshot(screenshot_path)

    # Guardar reporte
    with open("reporte_prueba_eliminar.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print("❌ Error en prueba eliminar:", e)

finally:
    time.sleep(3)
    driver.quit()
