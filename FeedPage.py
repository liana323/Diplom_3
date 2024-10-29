from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from BasePage import BasePage
from locators import *
from selenium.webdriver.support.ui import WebDriverWait


class FeedPage(BasePage):
    """Класс для работы с Лентой заказов и ингредиентами."""
    def open_feed(self):
        """Переходит на страницу Ленты заказов."""
        feed_link = self.wait.until(
            EC.element_to_be_clickable(FeedPageLocators.FEED_LINK)
        )
        feed_link.click()

    def is_feed_page(self):
        """Проверяет, что мы находимся на странице Ленты заказов."""
        return "feed" in self.browser.current_url

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
            self.browser.execute_script("arguments[0].scrollIntoView(true);", modal)
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
            close_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, '(//button[contains(@class, "Modal_modal__close__TnseK")])[2]')),
                message="Кнопка закрытия не появилась в отведённое время."
            )
            print("Кнопка закрытия найдена.")

            # Скроллим к кнопке и кликаем на неё
            self.browser.execute_script("arguments[0].scrollIntoView(true);", close_button)
            WebDriverWait(self.browser, 2).until(lambda driver: True)

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
        return "https://stellarburgers.nomoreparties.site/" in self.browser.current_url

    def wait_and_scroll_to_element(self, locator, timeout=10):
        """Ожидает, пока элемент станет видимым, и скроллит до него."""
        element = WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
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

        ActionChains(self.browser).drag_and_drop(ingredient, drop_zone).perform()

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
        WebDriverWait(self.browser, timeout).until(
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

            WebDriverWait(self.browser, 2).until(lambda driver: True)
            # Находим кнопку закрытия
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".Modal_modal__close__TnseK")),
                message="Кнопка закрытия не появилась или не кликабельна."
            )
            print("Кнопка закрытия найдена и готова к клику.")

            # Скроллим к кнопке, чтобы она попала в зону видимости
            self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", close_button)
            WebDriverWait(self.browser, 2).until(lambda driver: True)

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
        WebDriverWait(self.browser, 10).until(lambda driver: True)
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
            WebDriverWait(self.browser, 10).until(lambda driver: True) # Ждём перед следующей проверкой

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
        order_list = self.browser.find_element(By.CLASS_NAME, "OrderHistory_profileList__374GU")

        # Цикл для прокрутки и поиска заказа
        attempts = 0
        max_attempts = 3  # Ограничиваем количество попыток
        while attempts < max_attempts:
            try:
                print(f"[LOG] Попытка {attempts + 1} поиска заказа {search_order_number}...")

                # Проверяем, появился ли заказ с нужным номером
                element = self.browser.find_element(By.XPATH, f'//p[text()="{search_order_number}"]')
                print(f"[LOG] Заказ с номером {search_order_number} найден в истории!")
                return True  # Если нашли заказ, выходим из функции
            except:
                # Если не нашли, продолжаем скроллить
                print(f"[LOG] Заказ с номером {search_order_number} не найден, прокручиваем дальше...")
                self.browser.execute_script("arguments[0].scrollTop += 300;", order_list)

                # Ждем немного, чтобы дать странице обновиться
                WebDriverWait(self.browser, 2).until(lambda driver: True)
                attempts += 1

        # Если цикл завершился, а заказ не найден
        raise AssertionError(
            f"[LOG] Заказ с номером {search_order_number} не найден в истории после {max_attempts} попыток.")




    def is_order_in_progress(self, order_number):
        """Проверяет, что заказ отображается в разделе 'В работе'."""
        orders = self.browser.find_elements(
            By.CSS_SELECTOR, "li.text.text_type_digits-default.mb-2"
        )
        return any(order.text == order_number for order in orders)

    def refresh_page(self):
        """Обновляет текущую страницу."""
        self.browser.refresh()

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