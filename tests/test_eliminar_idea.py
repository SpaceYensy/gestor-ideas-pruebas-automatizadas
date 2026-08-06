import time
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:5000"


def login(driver):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "usuario").send_keys("admin")
    driver.find_element(By.ID, "contrasena").send_keys("admin123")
    driver.find_element(By.ID, "btn-login").click()
    time.sleep(1)


def test_eliminar_idea_camino_feliz(driver):
    login(driver)
    driver.find_element(By.ID, "titulo").send_keys("Idea a Eliminar")
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    botones_eliminar = driver.find_elements(By.CLASS_NAME, "btn-eliminar")
    botones_eliminar[-1].click()
    time.sleep(1)
    driver.switch_to.alert.accept()
    time.sleep(1)

    tabla = driver.find_element(By.ID, "tabla-ideas").text
    assert "Idea a Eliminar" not in tabla


def test_eliminar_idea_prueba_negativa(driver):
    login(driver)
    driver.find_element(By.ID, "titulo").send_keys("Idea que no se elimina")
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    botones_eliminar = driver.find_elements(By.CLASS_NAME, "btn-eliminar")
    botones_eliminar[-1].click()
    time.sleep(1)
    driver.switch_to.alert.dismiss()
    time.sleep(1)

    tabla = driver.find_element(By.ID, "tabla-ideas").text
    assert "Idea que no se elimina" in tabla


def test_eliminar_idea_prueba_limites(driver):
    login(driver)
    driver.get(BASE_URL + "/eliminar/999999")
    time.sleep(1)

    assert "dashboard" in driver.current_url