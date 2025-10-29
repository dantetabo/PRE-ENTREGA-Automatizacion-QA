import pytest
from selenium.webdriver.common.by import By
from utils.helpers import wait_for_element, wait_for_visible
import time

# Test 1 - Login automatizado con espera explícita y validación de /inventory.html y título
def test_login_success(driver, base_url):
    driver.get(base_url)
    # inputs login
    username = wait_for_element(driver, By.ID, "user-name", timeout=10)
    password = wait_for_element(driver, By.ID, "password", timeout=10)
    login_btn = wait_for_element(driver, By.ID, "login-button", timeout=10)

    username.clear()
    username.send_keys("standard_user")
    password.clear()
    password.send_keys("secret_sauce")
    login_btn.click()

    # Validar redirect a /inventory.html
    wait_for_element(driver, By.CLASS_NAME, "inventory_list", timeout=10)
    assert "/inventory.html" in driver.current_url

    # Validar título de la página (Products o Swag Labs header)
    header = wait_for_visible(driver, By.CLASS_NAME, "title", timeout=10)
    assert header.text.strip() in ["Products", "Products/Swag Labs", "PRODUCTS"]

# Test 2 - Navegación y verificación del catálogo
def test_inventory_catalog(driver, base_url):
    # Aseguramos login previo (hacer login programáticamente)
    driver.get(base_url)
    wait_for_element(driver, By.ID, "user-name", 10).send_keys("standard_user")
    wait_for_element(driver, By.ID, "password", 10).send_keys("secret_sauce")
    wait_for_element(driver, By.ID, "login-button", 10).click()

    # Verificamos título
    header = wait_for_visible(driver, By.CLASS_NAME, "title", 10)
    assert header.text.strip() in ["Products", "Products/Swag Labs", "PRODUCTS"]

    # Comprobamos que existan productos visibles (al menos uno)
    products = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(products) >= 1

    # Listar nombre y precio del primer producto
    first = products[0]
    name = first.find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
    price = first.find_element(By.CLASS_NAME, "inventory_item_price").text.strip()
    # A modo de validación mínima
    assert name != ""
    assert price.startswith("$") or price != ""

    # Verificar presencia de elementos importantes (filtro/menu)
    assert driver.find_element(By.ID, "react-burger-menu-btn")
    assert driver.find_element(By.CLASS_NAME, "product_sort_container")

# Test 3 - Interacción con productos: agregar al carrito y verificar contador y carrito
def test_add_to_cart_and_check(driver, base_url):
    driver.get(base_url)
    wait_for_element(driver, By.ID, "user-name", 10).send_keys("standard_user")
    wait_for_element(driver, By.ID, "password", 10).send_keys("secret_sauce")
    wait_for_element(driver, By.ID, "login-button", 10).click()

    # Esperar inventario
    wait_for_element(driver, By.CLASS_NAME, "inventory_list", 10)

    # Agregar primer producto (botón 'Add to cart' dentro del primer item)
    add_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")
    assert len(add_buttons) >= 1
    add_buttons[0].click()

    # Verificar que el contador del carrito se incremente
    cart_badge = wait_for_visible(driver, By.CLASS_NAME, "shopping_cart_badge", 5)
    assert cart_badge.text.strip() == "1"

    # Navegar al carrito
    cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_link.click()

    # Verificar que el producto agregado aparezca en el carrito
    cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) >= 1
    # Verificar nombre coincide (opcionalmente)
    first_cart_name = cart_items[0].find_element(By.CLASS_NAME, "inventory_item_name").text.strip()
    assert first_cart_name != ""
