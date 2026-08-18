import time
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:5000"

def test_login_camino_feliz(driver):
    """Camino feliz: login con usuario y contraseña correctos"""
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "usuario").send_keys("admin")
    driver.find_element(By.ID, "contrasena").send_keys("admin123")
    driver.find_element(By.ID, "btn-login").click()
    time.sleep(1)

    assert "dashboard" in driver.current_url

def test_login_prueba_negativa(driver):
    """Prueba negativa: login con contraseña incorrecta"""
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "usuario").send_keys("admin")
    driver.find_element(By.ID, "contrasena").send_keys("contrasena_mala")
    driver.find_element(By.ID, "btn-login").click()
    time.sleep(1)

    mensaje = driver.find_element(By.ID, "mensaje-error").text
    assert "incorrectos" in mensaje

def test_login_prueba_limites(driver):
    """Prueba de limites: login dejando los campos vacios"""
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "btn-login").click()
    time.sleep(1)

    mensaje = driver.find_element(By.ID, "mensaje-error").text
    assert "llenar" in mensaje