from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import time
import urllib.parse

class WikipediaPage(BasePage):
    SEARCH_INPUT = (By.NAME, "search")
    ARTICLE_TITLE = (By.CSS_SELECTOR, "h1#firstHeading")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def search(self, query):
        # Codificar la consulta para la URL
        encoded_query = urllib.parse.quote(query)
        # Construir la URL directa al artículo
        article_url = f"https://es.wikipedia.org/wiki/{encoded_query}"
        
        # Intentar acceder directamente al artículo
        self.driver.get(article_url)
        
        # Esperar a que se cargue el artículo
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.ARTICLE_TITLE)
            )
        except:
            # Si no se encuentra el artículo, volver a la página principal y buscar
            self.driver.get("https://es.wikipedia.org")
            search_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            
            # Esperar a que se cargue el artículo
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.ARTICLE_TITLE)
            )

    def get_article_title(self):
        return self.find_element(*self.ARTICLE_TITLE).text 