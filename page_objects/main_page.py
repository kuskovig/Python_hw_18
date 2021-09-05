from .base_page import BasePage
from .alerts import Alerts
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random


class MainPage(BasePage):
    """
    block with locators
    """
    MAIN_PAGE_CART_BUTTON = (By.CSS_SELECTOR, "#cart button")
    MAIN_PAGE_HEADER_CART_LINK = (By.CSS_SELECTOR, "#top-links li:nth-child(4)")
    MAIN_PAGE_CURRENCY_SELECTOR = (By.CSS_SELECTOR, "#form-currency")
    MAIN_PAGE_SLIDESHOW = (By.CSS_SELECTOR, "#slideshow0.swiper-container")
    RECOMMENDED_WISHLIST_BUTTONS = (By.CSS_SELECTOR, ".product-layout button:nth-child(2)")
    WISHLIST_ATTEMPT_ALERT = (By.CSS_SELECTOR, ".alert")
    WISHLIST_ATTEMPT_ALERT_CLOSE = (By.CSS_SELECTOR, ".alert button")
    SEARCH_BAR_SEARCH_BUTTON = (By.CSS_SELECTOR, "span.input-group-btn button")
    
    def wish_random_recommended_item(self, timeout=2):
        random_recommended = random.randint(0, 3)
        try:
            random_item_wish = WebDriverWait(self.browser, timeout) \
                .until(EC.presence_of_all_elements_located(MainPage.RECOMMENDED_WISHLIST_BUTTONS))[random_recommended]
            random_item_wish.click()
        except TimeoutException:
            raise AssertionError(f"Couldn't fined element in {timeout} seconds")

    def close_wishlist_alert(self):
        self.wait_for_element_and_click(*Alerts.SUCCESS_ALERT_CLOSE)

    def closed_alert_should_disappear(self):
        self.wait_for_element_to_disappear(*Alerts.SUCCESS_ALERT)

    def should_be_cart_button(self):
        assert self.is_element_present(*MainPage.MAIN_PAGE_CART_BUTTON), "Cart button wasn't found"

    def should_be_search_button(self):
        assert self.is_element_present(*MainPage.SEARCH_BAR_SEARCH_BUTTON), "Search button wasn't found"
