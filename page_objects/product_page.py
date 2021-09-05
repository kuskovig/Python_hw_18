from .base_page import BasePage
from .alerts import Alerts
from selenium.webdriver.common.by import By


class ProductPage(BasePage):
    PRODUCT_RELATIVE_URL = "/iphone"
    REVIEWS_TAB_LINK = (By.CSS_SELECTOR, ".nav-tabs li:nth-child(2) a")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "#button-cart")
    ADD_REVIEW_BUTTON = (By.CSS_SELECTOR, "#button-review")

    def should_be_reviews_tab(self):
        self.is_element_present(*self.REVIEWS_TAB_LINK)

    def should_be_add_to_cart_button(self):
        self.is_element_present(*self.ADD_TO_CART_BUTTON)

    def should_be_add_review_button(self):
        self.wait_for_element_and_click(*self.REVIEWS_TAB_LINK)
        self.is_element_present(*self.ADD_REVIEW_BUTTON)

    def should_be_alert_for_nonrated_review(self):
        self.wait_for_element_and_click(*self.REVIEWS_TAB_LINK)
        self.wait_for_element_and_click(*self.ADD_REVIEW_BUTTON)
        self.wait_for_element(*Alerts.ERROR_ALERT)

    def should_be_added_to_cart_alert(self):
        self.wait_for_element_and_click(*self.ADD_TO_CART_BUTTON)
        self.wait_for_element(*Alerts.SUCCESS_ALERT)
