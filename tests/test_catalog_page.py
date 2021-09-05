from page_objects.catalog_page import CatalogPage
import pytest


def test_there_is_compare_page_link(browser, url):
    page = CatalogPage(browser, url)
    page.open(CatalogPage.LAPTOPS_CATALOG_RELATIVE_URL)
    page.there_is_compare_hyperlink()


def test_can_add_product_to_compare(browser, url):
    page = CatalogPage(browser, url)
    page.open(CatalogPage.LAPTOPS_CATALOG_RELATIVE_URL)
    page.add_single_random_product_to_compare()


def test_can_open_product_page_from_catalog(browser, url):
    page = CatalogPage(browser, url)
    page.open(CatalogPage.LAPTOPS_CATALOG_RELATIVE_URL)
    page.open_random_product_on_page()


@pytest.mark.parametrize('limit', ["25", "50", "75", "100"])
def test_can_change_input_limit(browser, url, limit):
    page = CatalogPage(browser, url)
    page.open(CatalogPage.LAPTOPS_CATALOG_RELATIVE_URL)
    page.select_input_limit(limit)
    page.check_current_input_limit()


@pytest.mark.parametrize("first_view, second_view", [("#grid-view", "#list-view")])
def test_can_change_view(browser, url, first_view, second_view):
    page = CatalogPage(browser, url)
    page.open(CatalogPage.LAPTOPS_CATALOG_RELATIVE_URL)
    page.switch_view(first_view)
    page.check_if_view_is_active(first_view)
    page.switch_view(second_view)
    page.check_if_view_is_active(second_view)
