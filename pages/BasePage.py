from selenium.webdriver.support.ui import WebDriverWait
import allure

class BasePage:
    BASE_URL = "https://stellarburgers.nomoreparties.site"
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    @allure.step("Открываем URL: {url}")
    def open(self, url):
        self.browser.get(url)

    @allure.step("Открываем базовый URL")
    def open_base_url(self):
        """Открывает базовый URL."""
        self.browser.get(self.BASE_URL)
