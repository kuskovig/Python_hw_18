from .base_page import BasePage
from .alerts import Alerts
from selenium.webdriver.common.by import By
from test_data.get_product import product as newproduct
import allure


class AdminPage(BasePage):
    RELATIVE_URL = "/admin"
    ADMIN_USERNAME = "user"
    ADMIN_PASSWORD = "bitnami"
    INPUT_USERNAME = (By.CSS_SELECTOR, "#input-username")
    INPUT_PASSWORD = (By.CSS_SELECTOR, "#input-password")
    ADMINPAGE_PASSWORD_RECOVERY_LINK = (By.CSS_SELECTOR, ".help-block a")
    ADMINPAGE_LOGIN_BUTTON = (By.CSS_SELECTOR, "button")
    ADMINPAGE_CATALOG = (By.CSS_SELECTOR, "#menu-catalog")
    ADMINPAGE_LIST_OF_PRODUCTS = (By.CSS_SELECTOR, "#menu-catalog>ul>li:nth-child(2)")
    ADMINPAGE_SELECT_PRODUCT_CHECKBOX = (By.CSS_SELECTOR, "input[name='selected[]']")
    ADMINPAGE_ADD_NEW_PRODUCT_BUTTON = (By.CSS_SELECTOR, ".pull-right a")
    ADMINPAGE_DELETE_PRODUCT_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Delete']")
    ADMINPAGE_SAVE_PRODUCT_BUTTON = (By.CSS_SELECTOR, ".pull-right button[data-original-title='Save']")
    ADMINPAGE_PRODUCTS_FILTER_BY_NAME = (By.CSS_SELECTOR, "#input-name")
    ADMINPAGE_PRODUCTS_FILTER_BUTTON = (By.CSS_SELECTOR, "#button-filter")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, ".navbar-right>li:nth-child(2)")
    PRODUCT_CREATION_NAME = (By.CSS_SELECTOR, "#input-name1")
    PRODUCT_CREATION_DESCRIPTION = (By.CSS_SELECTOR, ".note-editable")
    PRODUCT_CREATION_META = (By.CSS_SELECTOR, "#input-meta-title1")
    PRODUCT_CREATION_DATA_TAB = (By.CSS_SELECTOR, ".nav-tabs>li:nth-child(2)")
    PRODUCT_CREATION_MODEL = (By.CSS_SELECTOR, "#input-model")
    PRODUCTLIST_TABLE_BODY = (By.CSS_SELECTOR, "tbody td")

    @allure.step("Enters data = 'data' into '_locator' element")
    def enter_data(self, _by, _locator, data):
        element = self.wait_for_element(_by, _locator)
        element.clear()
        self.logger.info(f"Sending data '{data}' in '{element}'")
        element.send_keys(data)

    def click_login(self):
        self.wait_for_element_and_click(*self.ADMINPAGE_LOGIN_BUTTON)

    def login_as_admin(self):
        self.enter_data(*self.INPUT_USERNAME, self.ADMIN_USERNAME)
        self.enter_data(*self.INPUT_PASSWORD, self.ADMIN_PASSWORD)
        self.click_login()

    def login_as_invalid_user(self):
        self.enter_data(*self.INPUT_USERNAME, 'qwe')
        self.enter_data(*self.INPUT_PASSWORD, 'zxc')
        self.click_login()

    def should_be_invalid_user_alert(self):
        self.logger.info(f"Checking presence of '{Alerts.ERROR_ALERT[1]}' element")
        self.is_element_present(*Alerts.ERROR_ALERT)

    def should_be_password_recovery_link(self):
        self.logger.info(f"Checking presence of '{self.ADMINPAGE_PASSWORD_RECOVERY_LINK[1]}' element")
        self.is_element_present(*self.ADMINPAGE_PASSWORD_RECOVERY_LINK)

    def should_be_logout_button(self):
        self.logger.info(f"Checking presence of '{self.LOGOUT_BUTTON[1]}' element")
        assert self.is_element_present(*self.LOGOUT_BUTTON), "Logout button wasn't found"

    def open_add_product_form(self):
        self.wait_for_element_and_click(*self.ADMINPAGE_CATALOG)
        self.wait_for_element_and_click(*self.ADMINPAGE_LIST_OF_PRODUCTS, 5)
        self.wait_for_element_and_click(*self.ADMINPAGE_ADD_NEW_PRODUCT_BUTTON)

    def fill_required_fields_in_product(self, prodname):
        self.enter_data(*self.PRODUCT_CREATION_NAME, prodname)
        self.enter_data(*self.PRODUCT_CREATION_DESCRIPTION, newproduct["Description"])
        self.enter_data(*self.PRODUCT_CREATION_META, newproduct["Meta"])
        self.wait_for_element_and_click(*self.PRODUCT_CREATION_DATA_TAB)
        self.enter_data(*self.PRODUCT_CREATION_MODEL, newproduct["Model"])

    def save_product(self):
        self.wait_for_element_and_click(*self.ADMINPAGE_SAVE_PRODUCT_BUTTON)

    def check_added_product_confirmation_alert(self):
        self.wait_for_element(*Alerts.SUCCESS_ALERT)

    def add_new_product(self, name):
        self.open_add_product_form()
        self.fill_required_fields_in_product(name)
        self.save_product()

    def delete_product(self, name):
        if not self.browser.title == "Products":
            self.wait_for_element_and_click(*self.ADMINPAGE_CATALOG)
            self.wait_for_element_and_click(*self.ADMINPAGE_LIST_OF_PRODUCTS)
        self.enter_data(*self.ADMINPAGE_PRODUCTS_FILTER_BY_NAME, name)
        self.wait_for_element_and_click(*self.ADMINPAGE_PRODUCTS_FILTER_BUTTON)
        self.wait_for_element_and_click(*self.ADMINPAGE_SELECT_PRODUCT_CHECKBOX)
        self.wait_for_element_and_click(*self.ADMINPAGE_DELETE_PRODUCT_BUTTON)
        alert = self.browser.switch_to.alert
        alert.accept()
        self.enter_data(*self.ADMINPAGE_PRODUCTS_FILTER_BY_NAME, name)
        self.wait_for_element_and_click(*self.ADMINPAGE_PRODUCTS_FILTER_BUTTON)
        assert self.wait_for_element(*self.PRODUCTLIST_TABLE_BODY).text == "No results!"

    def add_and_delete_product(self, name):
        """adds new product, then filters by name to find it, checks it and presses delete button"""
        self.add_new_product(name)
        self.delete_product(name)
