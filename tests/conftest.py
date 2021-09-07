import socket
import pytest
import logging

from selenium import webdriver

logging.basicConfig(level=logging.INFO, filename="logs/selenium.log", filemode="w")
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
                     default="local")
    parser.addoption("--bversion",
                     action="store",
                     default="92.0")
    parser.addoption("--vnc",
                     action="store_true",
                     default=False)
    parser.addoption("--video",
                     action="store_true",
                     default=False)
    parser.addoption("--logs",
                     action="store_true",
                     default=False)


@pytest.fixture
def browser(request):
    test_name = request.node.name

    def teardown():
        browser_logger.info("==============> CLOSING DRIVER")
        driver.quit()

    driver = None
    browser_choice = request.config.getoption("--browser")
    executor_choice = request.config.getoption("--executor")
    browser_version = request.config.getoption("--bversion")
    vnc = request.config.getoption("--vnc")
    video = request.config.getoption("--video")
    logs = request.config.getoption("--logs")

    if executor_choice == "local":

        if browser_choice == "chrome":
            driver = webdriver.Chrome()
        elif browser_choice == "firefox":
            driver = webdriver.Firefox()
        elif browser_choice == "opera":
            driver = webdriver.Opera()
        elif browser_choice == "edge":
            driver = webdriver.Edge()
    else:
        executor_url = f"http://{executor_choice}:4444/wd/hub"
        caps = {
            "browserName": browser_choice,
            "browserVersion": browser_version,
            "name": test_name,
            "selenoid:options": {
                "enableVNC": vnc,
                "enableVideo": video,
                "enableLog": logs
            }
        }
        driver = webdriver.Remote(
            command_executor=executor_url,
            desired_capabilities=caps)

    request.addfinalizer(teardown)
    driver.set_window_size(1960, 1080)
    browser_logger.info(f"==============> Starting {test_name}")
    return driver


@pytest.fixture
def url(request):
    return request.config.getoption("--url")
