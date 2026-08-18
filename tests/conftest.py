import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    opciones = Options()
    opciones.add_argument("--start-maximized")

    servicio = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servicio, options=opciones)

    yield navegador

    navegador.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        navegador = item.funcargs.get("driver")
        if navegador is not None:
            carpeta = os.path.join(os.path.dirname(__file__), "capturas")
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

            nombre_archivo = os.path.join(carpeta, f"{item.name}.png")
            try:
                navegador.save_screenshot(nombre_archivo)
            except Exception:
                pass

            if hasattr(item.config, "_html") or "pytest_html" in item.config.pluginmanager.list_name_plugin():
                try:
                    from pytest_html import extras
                    extra = getattr(report, "extra", [])
                    extra.append(extras.image(nombre_archivo))
                    report.extra = extra
                except Exception:
                    pass