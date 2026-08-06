import time
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:5000"


def login(driver):
    driver.get(BASE_URL + "/login")
    driver.find_element(By.ID, "usuario").send_keys("admin")
    driver.find_element(By.ID, "contrasena").send_keys("admin123")
    driver.find_element(By.ID, "btn-login").click()
    time.sleep(1)


def test_editar_idea_camino_feliz(driver):
    login(driver)
    driver.find_element(By.ID, "titulo").send_keys("Idea Original")
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    botones_editar = driver.find_elements(By.CLASS_NAME, "btn-editar")
    botones_editar[-1].click()
    time.sleep(1)

    campo_titulo = driver.find_element(By.ID, "titulo")
    campo_titulo.clear()
    campo_titulo.send_keys("Idea Editada")
    driver.find_element(By.ID, "btn-guardar").click()
    time.sleep(1)

    tabla = driver.find_element(By.ID, "tabla-ideas").text
    assert "Idea Editada" in tabla


def test_editar_idea_prueba_negativa(driver):
    login(driver)
    driver.find_element(By.ID, "titulo").send_keys("Idea Para Editar")
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    botones_editar = driver.find_elements(By.CLASS_NAME, "btn-editar")
    botones_editar[-1].click()
    time.sleep(1)

    campo_titulo = driver.find_element(By.ID, "titulo")
    campo_titulo.clear()
    driver.find_element(By.ID, "btn-guardar").click()
    time.sleep(1)

    mensaje = driver.find_element(By.ID, "mensaje-error").text
    assert "obligatorio" in mensaje


def test_editar_idea_prueba_limites(driver):
    login(driver)
    driver.find_element(By.ID, "titulo").send_keys("Idea Limite")
    driver.find_element(By.ID, "btn-agregar").click()
    time.sleep(1)

    botones_editar = driver.find_elements(By.CLASS_NAME, "btn-editar")
    botones_editar[-1].click()
    time.sleep(1)

    campo_titulo = driver.find_element(By.ID, "titulo")
    campo_titulo.clear()
    campo_titulo.send_keys("b" * 150)
    driver.find_element(By.ID, "btn-guardar").click()
    time.sleep(1)

    mensaje = driver.find_element(By.ID, "mensaje-error").text
    assert "100 caracteres" in mensaje