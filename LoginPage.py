from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BasePage import BasePage
from locators import *
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage (BasePage):
    def go_to_forgot_password(self):
        """Переход на страницу восстановления пароля."""
        forgot_password_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Восстановить пароль"))
        )
        forgot_password_link.click()

    def enter_email(self, email):
        """Вводит email в поле."""
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        email_field.send_keys(email)

    def submit_recovery(self):
        """Кликает на кнопку 'Восстановить'."""
        recover_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Восстановить"]'))
        )
        recover_button.click()

    def enter_password(self, password):
        """Вводит пароль в поле."""
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//input[@name="Введите новый пароль"]'))
        )
        password_field.clear()
        password_field.send_keys(password)

    def toggle_password_visibility(self):
        """Прокручивает к иконке и кликает на неё."""
        show_icon = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "input__icon"))
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", show_icon)
        show_icon.click()

    def get_password_input_type(self):
        """Возвращает значение атрибута 'type' у поля пароля."""
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, '//input[@name="Введите новый пароль"]'))
        )
        return password_field.get_attribute("type")

    def get_password_container_class(self):
        """Возвращает класс контейнера поля пароля."""
        container = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "input"))
        )
        return container.get_attribute("class")

    def go_to_personal_account(self):
        account_button = self.wait.until(
            EC.element_to_be_clickable(AccountPageLocators.ACCOUNT_BUTTON)
        )
        account_button.click()

    def submit_login(self):
        login_button = self.wait.until(
            EC.element_to_be_clickable(LoginPageLocators.LOGIN_BUTTON)
        )
        login_button.click()

    def is_login_page(self):
        """Проверяет, находимся ли мы на странице логина."""
        return "login" in self.browser.current_url

