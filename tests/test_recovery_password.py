import allure
from pages.LoginPage import LoginPage
from pages.PersonalAccountPage import PersonalAccountPage
from pages.FeedPage import FeedPage

@allure.feature("Восстановление пароля")
def test_recovery_password(browser, test_data):
    login_page = LoginPage(browser)
    login_page.open("https://stellarburgers.nomoreparties.site/login")

    with allure.step("Переход на страницу восстановления пароля"):
        login_page.go_to_forgot_password()

    with allure.step("Ввод почты и клик на 'Восстановить'"):
        email = test_data["email"]
        password = test_data["password"]

        login_page.enter_email(email)
        login_page.submit_recovery()

    with allure.step("Ввод пароля для активации поля"):
        login_page.enter_password(password)

    with allure.step("Проверка начального состояния"):
        # Проверяем, что поле имеет атрибут type='password'
        input_type = login_page.get_password_input_type()
        assert input_type == "password", "Поле пароля не скрыто по умолчанию"

        # Проверяем, что контейнер поля содержит класс 'input_type_password'
        container_class = login_page.get_password_container_class()
        assert any(cls in container_class for cls in ["input_type_password", "input_size_default"]), \
            "Поле не имеет ожидаемые классы по умолчанию"

    with allure.step("Проверка изменения на 'text'"):
        login_page.toggle_password_visibility()

        # Проверяем, что поле теперь имеет атрибут type='text'
        input_type = login_page.get_password_input_type()
        assert input_type == "text", "Поле не стало видимым (type='text') после клика"

        # Проверяем, что контейнер изменил класс на 'input_type_text'
        container_class = login_page.get_password_container_class()
        assert any(cls in container_class for cls in ["input_type_text", "input_size_active"]), \
            "Поле не получило ожидаемые классы при показе пароля"
