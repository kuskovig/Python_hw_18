from page_objects.product_page import ProductPage


def test_there_is_reviews_tab(browser, url):
    page = ProductPage(browser, url)
    page.open(ProductPage.PRODUCT_RELATIVE_URL)
    page.should_be_reviews_tab()


def test_presence_of_add_review_button(browser, url):
    page = ProductPage(browser, url)
    page.open(ProductPage.PRODUCT_RELATIVE_URL)
    page.should_be_add_review_button()


def test_presence_of_alert_for_norating_review(browser, url):
    page = ProductPage(browser, url)
    page.open(ProductPage.PRODUCT_RELATIVE_URL)
    page.should_be_alert_for_nonrated_review()


def test_presence_of_add_to_cart_button(browser, url):
    page = ProductPage(browser, url)
    page.open(ProductPage.PRODUCT_RELATIVE_URL)
    page.should_be_add_to_cart_button()


def test_presence_of_added_to_cart_product_alert(browser, url):
    page = ProductPage(browser, url)
    page.open(ProductPage.PRODUCT_RELATIVE_URL)
    page.should_be_added_to_cart_alert()
