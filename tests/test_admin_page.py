from page_objects.admin_page import AdminPage
import random


def test_can_login_as_admin(browser, url):
    page = AdminPage(browser, url)
    page.open(AdminPage.RELATIVE_URL)
    page.login_as_admin()
    page.should_be_logout_button()


def test_cannot_login_with_incorrect_credentials(browser, url):
    page = AdminPage(browser, url)
    page.open(AdminPage.RELATIVE_URL)
    page.login_as_invalid_user()
    page.should_be_invalid_user_alert()


def test_can_add_new_product(browser, url):
    page = AdminPage(browser, url)
    page.open(AdminPage.RELATIVE_URL)
    page.login_as_admin()
    page.add_new_product(str(random.randint(123, 567)))
    page.check_added_product_confirmation_alert()


def test_can_delete_product(browser, url):
    page = AdminPage(browser, url)
    page.open(AdminPage.RELATIVE_URL)
    page.login_as_admin()
    page.add_and_delete_product(str(random.randint(123, 567)))


def test_there_is_password_recovery(browser, url):
    page = AdminPage(browser, url)
    page.open(AdminPage.RELATIVE_URL)
    page.should_be_password_recovery_link()
