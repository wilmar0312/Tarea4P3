from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

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

    # Paso 3: Crear tarea en crud.html
    tarea = "Tarea desde prueba Selenium con login"
    task_input = driver.find_element(By.ID, "taskInput")
    task_input.send_keys(tarea)
    driver.find_element(By.CSS_SELECTOR, "#taskForm button[type='submit']").click()
    time.sleep(1)

    # Paso 4: Verificar que la tarea aparece en la lista
    tareas = driver.find_elements(By.CSS_SELECTOR, "#taskList li span")
    textos = [t.text for t in tareas]

    if tarea in textos:
        resultado = "✅ Prueba login + crear tarea: PASÓ"
    else:
        resultado = "❌ Prueba login + crear tarea: FALLÓ"

    # Captura y reporte
    driver.save_screenshot("screenshots/prueba_login_crear_tarea.png")
    with open("reporte_prueba_login_crear.txt", "w", encoding="utf-8") as f:
        f.write(resultado + "\n")

    print(resultado)

except Exception as e:
    print("❌ Error en prueba:", e)

finally:
    time.sleep(3)
    driver.quit()
