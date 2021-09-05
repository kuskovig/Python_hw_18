from .base_page import BasePage
from selenium.webdriver.common.by import By


class Alerts(BasePage):
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert")
    ERROR_ALERT = (By.CSS_SELECTOR, ".alert-danger")
    SUCCESS_ALERT_CLOSE = (By.CSS_SELECTOR, ".alert button")
