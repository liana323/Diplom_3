from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import *
import time

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url):
        """Открывает указанный URL."""
        self.driver.get(url)

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
        self.driver.execute_script("arguments[0].scrollIntoView(true);", show_icon)
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
        return "login" in self.driver.current_url


class PersonalAccountPage:
    """Класс для работы с личным кабинетом."""
    def __init__(self, driver):
        self.wait = WebDriverWait(driver, 10)
        self.driver = driver

    def is_main_page(self):
        """Проверяет, находимся ли мы на главной странице."""
        return "https://stellarburgers.nomoreparties.site/" in self.driver.current_url

    def go_to_feed(self):
        """Переход на Ленту заказов."""
        # Ожидаем, пока элемент станет видимым и кликабельным
        feed_link = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/feed"]'))
        )

        # Прокручиваем к элементу (если нужно)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", feed_link)

        time.sleep(1)
        # Кликаем на элемент
        feed_link.click()

    def is_feed_page(self):
        """Проверяет, находимся ли мы на странице ленты заказов."""
        return "feed" in self.driver.current_url

    def go_to_personal_account(self):
        account_link = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/account"]'))
        )
        account_link.click()
        # Ожидаем, пока не перейдёт на страницу личного кабинета
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("/account/profile")
        )

    def is_personal_account_page(self):
        """Проверяет, что мы на странице Личного Кабинета."""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@href="/account/profile"]'))
        )
        return "account/profile" in self.driver.current_url

    def logout(self):
        """Нажимает на кнопку 'Выход'."""
        # Ожидаем появления и доступности кнопки выхода
        logout_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Выход")]'))
        )

        # Прокручиваем к кнопке, чтобы убедиться, что она в зоне видимости
        self.driver.execute_script("arguments[0].scrollIntoView(true);", logout_button)

        # Ждем, пока кнопка станет видимой
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of(logout_button)
        )

        # Кликаем на кнопку выхода
        logout_button.click()

        # Убедимся, что мы вернулись на страницу логина
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("login")
        )
    def enter_password(self, password):
        password_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "Пароль"))
        )
        password_field.send_keys(password)


    def go_to_order_history(self):
        """Переходит в Историю заказов."""
        history_link = self.wait.until(
            EC.element_to_be_clickable(AccountPageLocators.ORDER_HISTORY_LINK)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", history_link)
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


class FeedPage:
    """Класс для работы с Лентой заказов и ингредиентами."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open_feed(self):
        """Переходит на страницу Ленты заказов."""
        feed_link = self.wait.until(
            EC.element_to_be_clickable(FeedPageLocators.FEED_LINK)
        )
        feed_link.click()

    def is_feed_page(self):
        """Проверяет, что мы находимся на странице Ленты заказов."""
        return "feed" in self.driver.current_url

    def click_ingredient(self):
        """Кликает на ингредиент для открытия модального окна."""
        ingredient = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "OrderHistory_img__baKNk"))
        )
        ingredient.click()

    def is_modal_open(self):
        """Проверяет, что модальное окно открыто и видимо."""
        try:
            print("Проверяем наличие модального окна...")
            modal = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "Modal_orderBox__1xWdi"))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", modal)
            return modal.is_displayed()
        except Exception as e:
            print(f"Модальное окно не найдено: {e}")
            return False

    def close_modal(self):
        """Закрывает модальное окно кликом по крестику."""
        try:
            print("Проверяем наличие модального окна...")

            # Ждём появления контейнера модального окна
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Modal_modal__container__Wo2l_")),
                message="Модальное окно не открылось в отведённое время."
            )
            print("Контейнер модального окна найден.")

            # Ждём и находим кнопку закрытия
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, '(//button[contains(@class, "Modal_modal__close__TnseK")])[2]')),
                message="Кнопка закрытия не появилась в отведённое время."
            )
            print("Кнопка закрытия найдена.")

            # Скроллим к кнопке и кликаем на неё
            self.driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
            time.sleep(0.5)  # Короткая пауза для стабильности

            print("Кнопка видима и активна. Выполняем клик.")
            close_button.click()

            # Ждём, пока активный класс исчезнет, что указывает на закрытие окна
            self.wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4")),
                message="Модальное окно не закрылось в отведённое время."
            )
            print("Модальное окно успешно закрыто.")

        except Exception as e:
            print(f"Ошибка при закрытии модального окна: {str(e)}")
            raise AssertionError(f"Не удалось закрыть модальное окно: {str(e)}")

    def is_modal_closed(self):
        """Проверяет, что модальное окно закрыто."""
        try:
            # Проверяем, что класс для открытого окна исчез
            self.wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4"))
            )
            print("Модальное окно успешно закрыто.")
            return True
        except Exception as e:
            print(f"Модальное окно не закрылось: {str(e)}")
            return False
    def click_constructor(self):
        """Кликает на 'Конструктор'."""
        constructor_link = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[@href="/"]'))
        )
        constructor_link.click()

    def is_constructor_page(self):
        """Проверяет, что мы находимся на главной странице."""
        return "https://stellarburgers.nomoreparties.site/" in self.driver.current_url

    def wait_and_scroll_to_element(self, locator, timeout=10):
        """Ожидает, пока элемент станет видимым, и скроллит до него."""
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    def find_order_in_feed(self, order_number):
        """Ищет заказ в ленте заказов."""
        try:
            orders = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "OrderHistory_listItem__2x95r"))
            )
            for order in orders:
                if order_number in order.text:
                    print(f"[LOG] Заказ {order_number} найден в ленте.")
                    return True
            print(f"[LOG] Заказ {order_number} не найден в ленте.")
            return False
        except TimeoutException:
            print("[LOG] Заказы не были найдены вовремя.")
            return False

    def open_order_modal(self, order_element):
        """Открывает модальное окно с деталями заказа."""
        order_element.click()

    def drag_and_drop_ingredient(self, ingredient_name):
        """Перетаскивает ингредиент в зону сборки."""
        ingredient_locator = (By.XPATH, f"//p[contains(text(), '{ingredient_name}')]")
        ingredient = self.wait_and_scroll_to_element(ingredient_locator)
        drop_zone = self.wait_and_scroll_to_element(FeedPageLocators.DROP_ZONE)

        ActionChains(self.driver).drag_and_drop(ingredient, drop_zone).perform()

    def create_order(self):
        """Нажимает на кнопку оформления заказа."""
        create_order_button = self.wait_and_scroll_to_element(FeedPageLocators.CREATE_ORDER_BUTTON)
        create_order_button.click()

    def get_order_number(self):
        """Извлекает номер заказа из модального окна."""
        modal_title = self.wait_and_scroll_to_element(FeedPageLocators.MODAL_TITLE)
        return modal_title.text


    def wait_for_element_to_disappear(self, locator, timeout=10):
        """Ожидает, пока элемент исчезнет."""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element(locator)
        )


    def close_modal_for_order(self):
        """Закрывает модальное окно кликом по крестику, проверяя все состояния."""
        try:
            print("Проверяем наличие открытого модального окна...")

            # Ждём появления открытого модального окна
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Modal_modal_opened__3ISw4")),
                message="Открытое модальное окно не обнаружено."
            )
            print("Модальное окно найдено и открыто.")

            time.sleep(1)
            # Находим кнопку закрытия
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".Modal_modal__close__TnseK")),
                message="Кнопка закрытия не появилась или не кликабельна."
            )
            print("Кнопка закрытия найдена и готова к клику.")

            # Скроллим к кнопке, чтобы она попала в зону видимости
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", close_button)
            time.sleep(0.3)  # Короткая пауза для стабильности

            # Выполняем клик по кнопке закрытия
            close_button.click()
            print("Клик по кнопке закрытия выполнен.")

            # Ожидаем исчезновения открытого класса
            self.wait.until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Modal_modal_opened__3ISw4")),
                message="Модальное окно не закрылось."
            )
            print("Модальное окно успешно закрыто.")

        except Exception as e:
            print(f"Ошибка при закрытии модального окна: {str(e)}")
            raise AssertionError(f"Не удалось закрыть модальное окно: {str(e)}")

    def extract_order_number(self):
        """Извлекает номер заказа из открытого модального окна."""
        print("Проверяем наличие открытого модального окна...")
        time.sleep(10)
        # Ждем, пока появится модальное окно
        order_number_element = self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "Modal_modal_opened__3ISw4")),
            message="Модальное окно не появилось."
        )
        print("Модальное окно найдено и открыто.")

        # Ждём появления элемента с номером заказа

        order_number_element = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//h2[contains(@class, "Modal_modal__title__2L34m")]')
            ),
            message="Элемент с номером заказа не найден."
        )

        # Увеличиваем время ожидания для получения реального номера
        max_attempts = 30  # Количество попыток
        for attempt in range(max_attempts):
            order_number = order_number_element.text.strip()

            if order_number.isdigit():  # Проверяем, что это настоящий номер заказа
                print(f"Найден номер заказа: {order_number}")
                return order_number

            print(f"Попытка {attempt + 1}/{max_attempts}: Номер пока не сформирован, ждём 2 секунды...")
            time.sleep(10)  # Ждём перед следующей проверкой

        raise AssertionError("Настоящий номер заказа не был получен в отведённое время.")
        time.sleep(20)

    def check_order_in_history(self, order_number):
        """Переходит в личный кабинет и проверяет наличие заказа в истории."""

        # Убедимся, что искомый номер всегда формируется корректно
        search_order_number = f"#0{order_number.lstrip('#0')}"  # Очищаем лишние префиксы перед добавлением
        print(f"[LOG] Переходим в историю заказов для поиска заказа: {search_order_number}...")

        # Открываем раздел "История заказов"
        history_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//a[text()="История заказов"]')),
            message="Кнопка 'История заказов' не найдена или не кликабельна."
        )
        history_button.click()

        # Находим список заказов
        order_list = self.driver.find_element(By.CLASS_NAME, "OrderHistory_profileList__374GU")

        # Цикл для прокрутки и поиска заказа
        attempts = 0
        max_attempts = 3  # Ограничиваем количество попыток
        while attempts < max_attempts:
            try:
                print(f"[LOG] Попытка {attempts + 1} поиска заказа {search_order_number}...")

                # Проверяем, появился ли заказ с нужным номером
                element = self.driver.find_element(By.XPATH, f'//p[text()="{search_order_number}"]')
                print(f"[LOG] Заказ с номером {search_order_number} найден в истории!")
                return True  # Если нашли заказ, выходим из функции
            except:
                # Если не нашли, продолжаем скроллить
                print(f"[LOG] Заказ с номером {search_order_number} не найден, прокручиваем дальше...")
                self.driver.execute_script("arguments[0].scrollTop += 300;", order_list)

                # Ждем немного, чтобы дать странице обновиться
                time.sleep(1)
                attempts += 1

        # Если цикл завершился, а заказ не найден
        raise AssertionError(
            f"[LOG] Заказ с номером {search_order_number} не найден в истории после {max_attempts} попыток.")




    def is_order_in_progress(self, order_number):
        """Проверяет, что заказ отображается в разделе 'В работе'."""
        orders = self.driver.find_elements(
            By.CSS_SELECTOR, "li.text.text_type_digits-default.mb-2"
        )
        return any(order.text == order_number for order in orders)

    def refresh_page(self):
        """Обновляет текущую страницу."""
        self.driver.refresh()

    def get_order_count(self, counter_type):
        """Получает количество заказов из счётчиков."""
        if counter_type == "all_time":
            element = self.wait_and_scroll_to_element(
                (By.CSS_SELECTOR, "p.OrderFeed_number__2MbrQ.text_type_digits-large")
            )
            return int(element.text)

        elif counter_type == "today":
            element = self.wait_and_scroll_to_element(
                (By.CSS_SELECTOR, "p.OrderFeed_number__2MbrQ.text_type_digits-large:nth-of-type(2)")
            )
            return int(element.text)