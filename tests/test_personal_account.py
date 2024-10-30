import allure
from pages.LoginPage import LoginPage
from pages.PersonalAccountPage import PersonalAccountPage
from pages.FeedPage import FeedPage

@allure.feature("Личный кабинет")
def test_personal_account(browser, test_data):
    login_page = LoginPage(browser)
    personal_account_page = PersonalAccountPage(browser)

    # Открываем сайт и переходим в личный кабинет
    login_page.open_base_url()
    login_page.go_to_personal_account()

    with allure.step("Вход в личный кабинет"):
        email = test_data["email"]
        login_page.enter_email(email)
        password = test_data["password"]
        personal_account_page.enter_password(password)
        login_page.submit_login()

    # Проверяем переход на главную страницу после входа
    assert personal_account_page.is_main_page(), "Не удалось перейти на главную страницу после входа"

    # Переход на Ленту заказов
    with allure.step("Переход на Ленту заказов"):
        personal_account_page.go_to_feed()
        assert personal_account_page.is_feed_page(), "Не удалось перейти на Ленту заказов"

    # Возвращение в Личный кабинет и выход из аккаунта
    with allure.step("Переход в Личный кабинет и выход"):
        personal_account_page.go_to_personal_account()
        assert personal_account_page.is_personal_account_page(), "Не удалось перейти в Личный кабинет"

        personal_account_page.logout()
        assert login_page.is_login_page(), "Не удалось выйти из аккаунта"
