from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import *
import allure

class BasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)

    @allure.step("Открываем URL: {url}")
    def open(self, url):
        self.browser.get(url)

