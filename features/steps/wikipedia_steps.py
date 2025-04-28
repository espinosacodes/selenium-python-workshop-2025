from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from pages.wikipedia_page import WikipediaPage
import os

@given('I am on the Wikipedia home page')
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
    
    context.wikipedia_page = WikipediaPage(context.driver)
    context.driver.get("https://es.wikipedia.org")

@when('I search for "{query}"')
def step_impl(context, query):
    context.wikipedia_page.search(query)

@then('I should see the article title "{expected_title}"')
def step_impl(context, expected_title):
    actual_title = context.wikipedia_page.get_article_title()
    assert actual_title == expected_title, f"Expected title: {expected_title}, but got: {actual_title}"
    context.driver.quit() 