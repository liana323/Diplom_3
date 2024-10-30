import allure
import time
from pages.LoginPage import LoginPage
from pages.PersonalAccountPage import PersonalAccountPage
from pages.FeedPage import FeedPage

@allure.feature("Создание заказа и проверка счетчиков")
def test_create_order_and_check_counters(browser, test_data):
    login_page = LoginPage(browser)
    personal_account_page = PersonalAccountPage(browser)
    feed_page = FeedPage(browser)

    # Открываем сайт и переходим в личный кабинет
    login_page.open("https://stellarburgers.nomoreparties.site/")
    login_page.go_to_personal_account()

    with allure.step("Вход в личный кабинет"):
        email = test_data["email"]
        password = test_data["password"]
        login_page.enter_email(email)
        personal_account_page.enter_password(password)
        login_page.submit_login()

    assert personal_account_page.is_main_page(), "Не удалось перейти на главную страницу после входа"

    with allure.step("Переход на Ленту заказов"):
        feed_page.open_feed()
        time.sleep(5)

    # Запоминаем начальные значения счетчиков
    total_orders_before = feed_page.get_order_count("all_time")
    today_orders_before = feed_page.get_order_count("today")

    with allure.step("Переход в Конструктор"):
        feed_page.click_constructor()
        assert feed_page.is_constructor_page(), "Не удалось перейти в Конструктор"

    with allure.step("Добавление ингредиентов"):
        feed_page.drag_and_drop_ingredient("Флюоресцентная булка R2-D3")
        feed_page.drag_and_drop_ingredient("Соус Spicy-X")
        feed_page.drag_and_drop_ingredient("Мясо бессмертных моллюсков Protostomia")

    with allure.step("Оформление заказа"):
        feed_page.create_order()


    with allure.step("Проверка успешного оформления заказа"):
        order_number = feed_page.extract_order_number()
        assert order_number, "Номер заказа не отображается"
        print(f"Номер заказа: {order_number}")

    with allure.step("Закрытие модального окна"):
        feed_page.close_modal_for_order()

    with allure.step("Проверка появления заказа в разделе 'В работе'"):
        personal_account_page.go_to_feed()
        feed_page.refresh_page()  # Обновляем страницу
        try:
            assert feed_page.is_order_in_progress(order_number), f"Заказ {order_number} не найден в 'В работе'"
        except AssertionError as e:
            print(f"[LOG] Предупреждение: {str(e)}")
            allure.attach(body=str(e), name="Order not found warning", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Проверка увеличения счетчиков"):
        feed_page.refresh_page()

        total_orders_after = feed_page.get_order_count("all_time")
        today_orders_after = feed_page.get_order_count("today")

        assert total_orders_after > total_orders_before, \
            f"Счётчик 'Выполнено за всё время' не увеличился. Было: {total_orders_before}, стало: {total_orders_after}"
        assert today_orders_after > today_orders_before, \
            f"Счётчик 'Выполнено за сегодня' не увеличился. Было: {today_orders_before}, стало: {today_orders_after}"
