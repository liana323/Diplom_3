from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BasePage import BasePage
from locators import *
from selenium.webdriver.support.ui import WebDriverWait

class PersonalAccountPage(BasePage):
    """Класс для работы с личным кабинетом."""
    def is_main_page(self):
        """Проверяет, находимся ли мы на главной странице."""
        return "https://stellarburgers.nomoreparties.site/" in self.browser.current_url

    def go_to_feed(self):
        """Переход на Ленту заказов."""
        # Ожидаем, пока элемент станет видимым и кликабельным
        feed_link = WebDriverWait(self.browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/feed"]'))
        )

        # Прокручиваем к элементу (если нужно)
        self.browser.execute_script("arguments[0].scrollIntoView(true);", feed_link)

        WebDriverWait(self.browser, 2).until(lambda driver: True)
        # Кликаем на элемент
        feed_link.click()

    def is_feed_page(self):
        """Проверяет, находимся ли мы на странице ленты заказов."""
        return "feed" in self.browser.current_url

    def go_to_personal_account(self):
        account_link = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/account"]'))
        )
        account_link.click()
        # Ожидаем, пока не перейдёт на страницу личного кабинета
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("/account/profile")
        )

    def is_personal_account_page(self):
        """Проверяет, что мы на странице Личного Кабинета."""
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/account/profile"]'))
        )
        return "account/profile" in self.browser.current_url

    def logout(self):
        """Нажимает на кнопку 'Выход'."""
        # Ожидаем появления и доступности кнопки выхода
        logout_button = WebDriverWait(self.browser, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Выход")]'))
        )

        # Прокручиваем к кнопке, чтобы убедиться, что она в зоне видимости
        self.browser.execute_script("arguments[0].scrollIntoView(true);", logout_button)

        # Ждем, пока кнопка станет видимой
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of(logout_button)
        )

        # Кликаем на кнопку выхода
        logout_button.click()

        # Убедимся, что мы вернулись на страницу логина
        WebDriverWait(self.browser, 10).until(
            EC.url_contains("login")
        )
    def enter_password(self, password):
        password_field = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.NAME, "Пароль"))
        )
        password_field.send_keys(password)


    def go_to_order_history(self):
        """Переходит в Историю заказов."""
        history_link = self.wait.until(
            EC.element_to_be_clickable(AccountPageLocators.ORDER_HISTORY_LINK)
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", history_link)
        history_link.click()
        # Извлекаем и логируем номер заказа
        order_item = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "OrderHistory_listItem__2x95r"))
        )
        order_number = order_item.find_element(By.CLASS_NAME, "text_type_digits-default").text
        print(f"[LOG] Найден номер заказа: {order_number}")
        return order_number

    def get_order_number(self):
        """Извлекает номер заказа из истории заказов."""
        try:
            order = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "OrderHistory_textBox__3lgbs"))
            )
            order_number = order.find_element(By.CLASS_NAME, "text_type_digits-default").text
            print(f"[LOG] Найден номер заказа: {order_number}")
            return order_number
        except TimeoutException:
            print("[LOG] Не удалось найти номер заказа.")
            return None

