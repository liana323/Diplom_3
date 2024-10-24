from selenium.webdriver.common.by import By

class LoginPageLocators:
    FORGOT_PASSWORD_LINK = (By.LINK_TEXT, "Восстановить пароль")
    EMAIL_INPUT = (By.NAME, "name")
    RECOVER_BUTTON = (By.XPATH, '//button[text()="Восстановить"]')
    PASSWORD_INPUT = (By.XPATH, '//input[@type="password"]')
    SHOW_PASSWORD_ICON = (By.CLASS_NAME, "input__icon")
    LOGIN_BUTTON = (By.XPATH, '//button[text()="Войти"]')

class AccountPageLocators:
    ACCOUNT_BUTTON = (By.XPATH, '//a[@href="/account"]')
    ORDER_HISTORY = (By.LINK_TEXT, "История заказов")
    LOGOUT_BUTTON = (By.XPATH, '//button[text()="Выйти"]')
    ORDER_HISTORY_LINK = (By.LINK_TEXT, "История заказов")

class MainPageLocators:
    CONSTRUCTOR_LINK = (By.LINK_TEXT, "Конструктор")
    ORDER_FEED_LINK = (By.XPATH, '//p[text()="Лента Заказов"]')
    INGREDIENT = (By.CLASS_NAME, "ingredient_class")  # Пример класса
    MODAL_CLOSE_BUTTON = (By.CLASS_NAME, "modal_close_icon")

class OrderHistoryLocators:
    ORDER_ITEM = (By.CLASS_NAME, "OrderHistory_listItem__2x95r")
    ORDER_NUMBER = (By.CLASS_NAME, "text_type_digits-default")

class FeedPageLocators:
    FEED_LINK = (By.XPATH, '//a[@href="/feed"]')
    ORDER_NUMBER_IN_FEED = lambda order_number: (By.XPATH, f'//p[text()="{order_number}"]')
    CONSTRUCTOR_TAB = (By.CLASS_NAME, 'tab_tab__1SPyG')
    INGREDIENT_ITEM = (By.CLASS_NAME, 'BurgerIngredient_ingredient__1TVf6')
    DROP_ZONE = (By.CLASS_NAME, 'App_componentContainer__2JC2W')
    CREATE_ORDER_BUTTON = (By.XPATH, '//button[text()="Оформить заказ"]')
    ORDER_NUMBER = (By.CLASS_NAME, 'order_number')
    MODAL_TITLE = (By.CLASS_NAME, 'Modal_modal__title__2L34m')
    CLOSE_BUTTON = (By.CLASS_NAME, 'Modal_modal__close__3D_2Z')  # Селектор для крестика
