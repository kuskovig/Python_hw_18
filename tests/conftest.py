import socket
import pytest
import logging

from selenium import webdriver

logging.basicConfig(level=logging.INFO, filename="logs/selenium.log")
browser_logger = logging.getLogger("BROWSER_LOGGER")


def get_local_opencart_address():
    return "http://" + socket.gethostbyname(socket.gethostname()) + ":8081"


def pytest_addoption(parser):
    parser.addoption("--browser",
                     action="store",
                     choices=["chrome", "firefox", "opera", "edge"],
                     default="chrome")
    parser.addoption("--url",
                     action="store",
                     default=get_local_opencart_address())
    parser.addoption("--executor",
                     action="store",
                     default="127.0.0.1")


@pytest.fixture
def browser(request):
    test_name = request.node.name

    def teardown():
        browser_logger.info("CLOSING DRIVER")
        driver.quit()

    driver = None
    browser_choice = request.config.getoption("--browser")
    # executor_choice = request.config.getoption("--executor")

    if browser_choice == "chrome":
        driver = webdriver.Chrome()
    elif browser_choice == "firefox":
        driver = webdriver.Firefox()
    elif browser_choice == "opera":
        driver = webdriver.Opera()
    elif browser_choice == "edge":
        driver = webdriver.Edge()

    request.addfinalizer(teardown)
    driver.set_window_size(1960, 1080)
    browser_logger.info(f"===> Starting {test_name}")
    return driver


@pytest.fixture
def url(request):
    return request.config.getoption("--url")
