import time
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:5000"

def login(driver):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "usuario").send_keys("admin")
    driver.find_element(By.ID, "contrasena").send_keys("admin123")
    driver.find_element(By.ID, "btn-login").click()
    time.sleep(1)


def crear_idea(driver, titulo):
    driver.find_element(By.ID, "titulo").send_keys(titulo)
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)


def test_buscar_idea_camino_feliz(driver):
    login(driver)
    crear_idea(driver, "Idea Buscable")

    driver.find_element(By.ID, "buscar").send_keys("Buscable")
    driver.find_element(By.ID, "btn-buscar").click()
    time.sleep(1)

    tabla = driver.find_element(By.ID, "tabla-ideas").text
    assert "Idea Buscable" in tabla


def test_buscar_idea_prueba_negativa(driver):
    login(driver)
    driver.find_element(By.ID, "buscar").send_keys("NoExisteXYZ123")
    driver.find_element(By.ID, "btn-buscar").click()
    time.sleep(1)

    tabla = driver.find_element(By.ID, "tabla-ideas").text
    assert "NoExisteXYZ123" not in tabla


def test_buscar_idea_prueba_limites(driver):
    login(driver)
    crear_idea(driver, "Idea Cualquiera")

    driver.find_element(By.ID, "buscar").click()
    driver.find_element(By.ID, "btn-buscar").click()
    time.sleep(1)

    tabla = driver.find_element(By.ID, "tabla-ideas").text
    assert "Idea Cualquiera" in tabla