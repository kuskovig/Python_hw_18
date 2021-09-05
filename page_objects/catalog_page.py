from .base_page import BasePage
from selenium.webdriver.common.by import By
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select


class CatalogPage(BasePage):
    LAPTOPS_CATALOG_RELATIVE_URL = "/laptop-notebook"
    COMPARE_PRODUCT_BUTTONS = (By.CSS_SELECTOR, "button[data-original-title='Compare this Product']")  # all of them
    PRODUCT_IMAGES = (By.CSS_SELECTOR, ".product-layout img")  # all of them
    COMPARE_HYPERLINK = (By.CSS_SELECTOR, "#compare-total")
    SORTING_SELECTOR = (By.CSS_SELECTOR, "#input-sort")
    INPUT_LIMIT = (By.CSS_SELECTOR, "#input-limit")
    DESCRIPTION_TEXT_BLOCK = (By.CSS_SELECTOR, "#content p:nth-child(1)")
    PAGINATION_TEXT = (By.CSS_SELECTOR, ".text-right")

    def open_random_product_via_img(self):
        self.wait_for_element_and_click(*self.PRODUCT_IMAGES)

    def there_is_compare_hyperlink(self, amount=0, timeout=1):
        self.is_element_present(*self.COMPARE_HYPERLINK)
        try:
            WebDriverWait(self.browser, timeout) \
                .until(EC.text_to_be_present_in_element(self.COMPARE_HYPERLINK, f"Product Compare ({amount})"))
        except TimeoutException:
            self.logger.warning(f"Element wasn't found in {timeout} seconds")
            raise AssertionError("Compare hyperlink info haven't updated in 2 seconds")

    def return_random_item_from_many(self, _by, _locator):
        items = self.browser.find_elements(_by, _locator)
        return items[random.randint(0, len(items) - 1)]

    def add_single_random_product_to_compare(self):
        self.there_is_compare_hyperlink()
        self.return_random_item_from_many(*self.COMPARE_PRODUCT_BUTTONS).click()
        self.there_is_compare_hyperlink(1)

    def open_random_product_on_page(self):
        product = self.return_random_item_from_many(*self.PRODUCT_IMAGES)
        self.logger.info(f"Clicking '{product}' item")
        name = product.get_property("alt")
        product.click()
        self.logger.info(f"Asserting browser title is == '{name}'")
        assert self.browser.title == name

    def select_input_limit(self, limit):
        selector = Select(self.wait_for_element(*self.INPUT_LIMIT))
        self.logger.info(f"Choosing  '{limit}' selector")
        selector.select_by_value(self.browser.current_url + "?limit=" + limit)

    def check_current_input_limit(self):
        value_locator = f"{self.INPUT_LIMIT[1]} option[value='{self.browser.current_url}']"
        self.logger.info(f"Asserting current input limit ")
        assert self.wait_for_element(By.CSS_SELECTOR, value_locator).get_property("selected"),\
            "Element is not selected"
    
    def switch_view(self, view_id):
        self.logger.info(f"Switching view to {view_id}")
        self.wait_for_element_and_click(By.CSS_SELECTOR, view_id)
    
    def check_if_view_is_active(self, view_id):
        self.logger.info(f"Asserting {view_id} view is activated")
        assert "active" in self.wait_for_element(By.CSS_SELECTOR, view_id).get_property("classList"),\
            "Element is not selected"
