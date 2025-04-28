from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from selenium.webdriver.common.by import By
import os

@given('the user is on the login page')
def step_given_user_on_login_page(context):
    # Limpiar cualquier configuración previa
    os.environ.pop('BROWSER', None)
    os.environ.pop('SELENIUM_BROWSER', None)
    
    # Configurar Firefox específicamente
    firefox_options = Options()
    firefox_options.binary_location = "/usr/bin/firefox-developer-edition"
    
    # Configurar preferencias específicas
    firefox_options.set_preference("browser.startup.homepage", "about:blank")
    firefox_options.set_preference("startup.homepage_welcome_url", "about:blank")
    firefox_options.set_preference("startup.homepage_welcome_url.additional", "about:blank")
    firefox_options.set_preference("browser.link.open_newwindow", 2)
    firefox_options.set_preference("browser.link.open_newwindow.restriction", 0)
    
    # Forzar el uso de Firefox
    service = Service(GeckoDriverManager().install())
    context.driver = webdriver.Firefox(service=service, options=firefox_options)
    
    # Verificar que estamos usando Firefox
    assert "firefox" in context.driver.capabilities['browserName'].lower(), "El navegador no es Firefox"
    
    context.login_page = LoginPage(context.driver)
    context.driver.get("https://www.saucedemo.com/v1/index.html")

@when('the user logs in with valid credentials')
def step_when_user_logs_in_valid(context):
    context.login_page.login("standard_user", "secret_sauce")

@when('the user logs in with invalid credentials')
def step_when_user_logs_in_invalid(context):
    context.login_page.login("invalid_user", "invalid_password")

@when('the user logs in with empty credentials')
def step_when_user_logs_in_empty(context):
    context.login_page.login("", "")

@then('the user should be redirected to the inventory page')
def step_then_inventory_page(context):
    inventory_page = InventoryPage(context.driver)
    assert inventory_page.is_inventory_page_displayed()

@then('an error message should be displayed')
def step_then_error_message(context):
    error_message = context.login_page.find_element((By.CSS_SELECTOR, '[data-test="error"]')).text
    assert "Epic sadface" in error_message

def after_scenario(context, scenario):
    context.driver.quit()
