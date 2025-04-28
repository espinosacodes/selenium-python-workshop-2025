from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from pages.mercadolibre_page import MercadoLibrePage
import os

@given('I am on the MercadoLibre home page')
def step_impl(context):
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
    
    context.mercadolibre_page = MercadoLibrePage(context.driver)
    context.driver.get("https://www.mercadolibre.com.co")

@when('I search for product "{query}" in MercadoLibre')
def step_impl(context, query):
    context.mercadolibre_page.search(query)

@then('I should see MercadoLibre search results containing "{text}"')
def step_impl(context, text):
    results = context.mercadolibre_page.get_search_results()
    assert any(text.lower() in result.lower() for result in results), f"No se encontraron resultados que contengan '{text}'"
    context.driver.quit() 