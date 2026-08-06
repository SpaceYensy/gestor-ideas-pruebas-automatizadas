import time
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:5000"


def login(driver):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "usuario").send_keys("admin")
    driver.find_element(By.ID, "contrasena").send_keys("admin123")
    driver.find_element(By.ID, "btn-login").click()
    time.sleep(1)


def test_crear_idea_camino_feliz(driver):
    login(driver)
    driver.find_element(By.ID, "titulo").send_keys("Idea de prueba")
    driver.find_element(By.ID, "descripcion").send_keys("Descripcion de prueba")
    driver.find_element(By.ID, "categoria").send_keys("Trabajo")
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    tabla = driver.find_element(By.ID, "tabla-ideas").text
    assert "Idea de prueba" in tabla


def test_crear_idea_prueba_negativa(driver):
    login(driver)
    driver.find_element(By.ID, "descripcion").send_keys("Idea sin titulo")
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    mensaje = driver.find_element(By.ID, "mensaje-error").text
    assert "obligatorio" in mensaje


def test_crear_idea_prueba_limites(driver):
    login(driver)
    titulo_largo = "a" * 150
    driver.find_element(By.ID, "titulo").send_keys(titulo_largo)
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    mensaje = driver.find_element(By.ID, "mensaje-error").text
    assert "100 caracteres" in mensaje