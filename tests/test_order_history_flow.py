import pytest
import allure
from pages import LoginPage, PersonalAccountPage, FeedPage


@allure.feature("История заказов")
def test_order_history_flow(browser, test_data):
    login_page = LoginPage(browser)
    personal_account_page = PersonalAccountPage(browser)
    feed_page = FeedPage(browser)

    # Открываем сайт и переходим в личный кабинет
    login_page.open("https://stellarburgers.nomoreparties.site/")
    login_page.go_to_personal_account()

    with allure.step("Вход в личный кабинет"):
        email = test_data["email"]
        login_page.enter_email(email)
        password = test_data["password"]
        personal_account_page.enter_password(password)
        login_page.submit_login()

    # Проверяем переход на главную страницу после входа
    assert personal_account_page.is_main_page(), "Не удалось перейти на главную страницу после входа"

    login_page.go_to_personal_account()

    with allure.step("Переход в конструктор"):
        feed_page.click_constructor()
        assert feed_page.is_constructor_page(), "Не удалось перейти в Конструктор"

    with allure.step("Добавление ингредиентов"):
        feed_page.drag_and_drop_ingredient("Флюоресцентная булка R2-D3")
        feed_page.drag_and_drop_ingredient("Соус Spicy-X")
        feed_page.drag_and_drop_ingredient("Мясо бессмертных моллюсков Protostomia")

    with allure.step("Оформление заказа"):
        feed_page.create_order()

    with allure.step("Проверка успешного оформления заказа"):
        order_number = feed_page.extract_order_number()  # Извлекаем номер заказа
        assert order_number, "Номер заказа не отображается"
        print(f"Номер заказа: {order_number}")

    with allure.step("Закрытие модального окна"):
        feed_page.close_modal_for_order()  # Закрываем модальное окно

    with allure.step("Переход в личный кабинет"):
        personal_account_page.go_to_personal_account()

    with allure.step("Переход в Историю заказов"):
        personal_account_page.go_to_order_history()  # Переход в раздел истории заказов

    with allure.step("Проверка наличия заказа в истории"):
        order_found = feed_page.check_order_in_history(order_number)
        assert order_found, f"Заказ с номером {order_number} не найден в истории."

    with allure.step("Переход на Ленту заказов"):
        personal_account_page.go_to_feed()
        order_found_in_feed = feed_page.find_order_in_feed(order_number)
        assert order_found_in_feed, f"Заказ {order_number} не найден в ленте заказов."




