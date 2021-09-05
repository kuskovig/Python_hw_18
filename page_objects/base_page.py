import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    CURRENCY_PICKER = (By.CSS_SELECTOR, ".pull-left div>button")
    CURRENCY_CHOICE = '.pull-left li>button'
    CURRENCY_SYMBOL = (By.CSS_SELECTOR, ".pull-left strong")

    def __init__(self, browser, url):
        self.browser = browser
        self.url = url
        self.logger = logging.getLogger(type(self).__name__)

    def open(self, relative_url=""):
        self.logger.info(f"Opening {self.url}{relative_url} url")
        self.browser.get(self.url + relative_url)

    def is_element_present(self, _by, _locator):
        self.logger.info(f"Trying to find {_locator} element by {_by}")
        try:
            self.browser.find_element(_by, _locator)
        except NoSuchElementException:
            return False
        return True

    def wait_for_element(self, _by, _selector, timeout=2):
        self.logger.info(f"Waiting for {_selector} element by {_by} for {timeout} seconds")
        try:
            element = WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((_by, _selector)))
        except TimeoutException:
            self.logger.warning(f"Element wasn't found in {timeout} seconds")
            raise AssertionError(f"Couldn't find element for {timeout} seconds")
        return element
    '''
    In ActionChain we pass "element.wrapped_element" argument to ".move_to" method because of using EventFiringWebDriver
    If usual webdriver is used, then argument should be changed to "element"
    '''
    def wait_for_element_and_click(self, _by, _selector, timeout=2):
        element = self.wait_for_element(_by, _selector, timeout)
        self.logger.info(f"clicking '{element}' element")
        ActionChains(self.browser).pause(0.1).move_to_element(element).click().perform()

    def wait_for_element_to_disappear(self, _by, _selector, timeout=2):
        self.logger.info(f"Waiting for {_selector} element by {_by} for {timeout} seconds to disappear")
        try:
            WebDriverWait(self.browser, timeout).until_not(EC.presence_of_element_located((_by, _selector)))
        except TimeoutException:
            self.logger.warning(f"Element wasn't found in {timeout} seconds")
            raise AssertionError(f"Element didn't disappear in {timeout} seconds")

    def change_currency(self, currency):
        """
        possible currency values = EUR, USD, GBP
        """
        self.logger.info(f"Changing currency to {currency}")
        self.browser.find_element(*self.CURRENCY_PICKER).click()
        self.browser.find_element(By.CSS_SELECTOR, self.CURRENCY_CHOICE + f"[name='{currency}']").click()

    def currency_symbol_should_change_with_currency(self, currency, symbol):
        """
        changes currency to the user choice and checks if currency symbols changed
        """
        self.change_currency(currency)
        assert self.wait_for_element(*self.CURRENCY_SYMBOL).text == symbol, "Currency symbol haven't changed"
