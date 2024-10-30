import allure
from pages.LoginPage import LoginPage
from pages.PersonalAccountPage import PersonalAccountPage
from pages.FeedPage import FeedPage

@allure.feature("Переходы: Конструктор и Лента заказов")
def test_constructor_and_feed(browser):
    login_page = LoginPage(browser)
    feed_page = FeedPage(browser)
    personal_account_page = PersonalAccountPage(browser)

    with allure.step("Открытие основной страницы"):
        login_page.open_base_url()
        assert personal_account_page.is_main_page(), "Не удалось открыть основную страницу"

    with allure.step("Переход в Конструктор"):
        feed_page.click_constructor()
        assert feed_page.is_constructor_page(), "Не удалось перейти в Конструктор"

    with allure.step("Переход на Ленту заказов"):
        feed_page.open_feed()
        assert feed_page.is_feed_page(), "Не удалось перейти на Ленту заказов"

    with allure.step("Клик по ингредиенту и проверка модального окна"):
        feed_page.click_ingredient()
        assert feed_page.is_modal_open(), "Модальное окно не открылось"

    with allure.step("Закрытие модального окна"):
        feed_page.close_modal()
        assert feed_page.is_modal_closed(), "Модальное окно не закрылось"
