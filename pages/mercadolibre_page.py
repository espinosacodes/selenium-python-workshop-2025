from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage
import time

class MercadoLibrePage(BasePage):
    # Selectores más generales
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='text']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SEARCH_RESULTS = (By.CSS_SELECTOR, "h2, .ui-search-item__title")
    COOKIE_BANNER = (By.CSS_SELECTOR, "button, .cookie-consent-banner-opt-out__action")

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def search(self, query):
        # Esperar a que la página se cargue completamente
        time.sleep(5)
        
        # Manejar el banner de cookies si está presente
        try:
            cookie_buttons = self.driver.find_elements(*self.COOKIE_BANNER)
            for button in cookie_buttons:
                if "cookie" in button.text.lower() or "aceptar" in button.text.lower():
                    button.click()
                    time.sleep(2)
                    break
        except:
            pass

        # Intentar encontrar el campo de búsqueda
        try:
            search_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.SEARCH_INPUT)
            )
            search_input.clear()
            search_input.send_keys(query)
            
            # Intentar encontrar y hacer clic en el botón de búsqueda
            try:
                search_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable(self.SEARCH_BUTTON)
                )
                search_button.click()
            except:
                # Si no se encuentra el botón, usar Enter
                search_input.send_keys(Keys.RETURN)
            
            # Esperar a que aparezcan los resultados
            time.sleep(5)  # Espera adicional para que la página se cargue
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(self.SEARCH_RESULTS)
            )
        except Exception as e:
            print(f"Error durante la búsqueda: {str(e)}")
            raise

    def get_search_results(self):
        try:
            results = self.driver.find_elements(*self.SEARCH_RESULTS)
            return [result.text for result in results if result.text.strip()]
        except Exception as e:
            print(f"Error al obtener resultados: {str(e)}")
            return [] 