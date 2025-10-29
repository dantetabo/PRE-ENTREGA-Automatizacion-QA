import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os
import time

@pytest.fixture(scope="session")
def base_url():
    return "https://www.saucedemo.com/"

@pytest.fixture
def driver(request):
    # Configura Chrome WebDriver con webdriver-manager
    options = Options()
    # Comentar la siguiente línea si querés ver el navegador
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1366,768")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    yield driver

    # teardown
    try:
        driver.quit()
    except Exception:
        pass

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Hook para capturar screenshot al fallar
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get('driver', None)
        if driver:
            reports_dir = os.path.join(os.getcwd(), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            timestamp = int(time.time())
            name = f"screenshot_{item.name}_{timestamp}.png"
            path = os.path.join(reports_dir, name)
            try:
                driver.save_screenshot(path)
                # Agregar path al reporte (pytest-html puede recogerlo si se configura)
                if hasattr(rep, 'extra'):
                    rep.extra.append(path)
            except Exception:
                pass
