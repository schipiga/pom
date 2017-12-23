import mock
import pytest
from hamcrest import *

from pom.base import Page

@pytest.fixture
def page():
    page = Page(mock.MagicMock())
    page.url = "https://yandex.ru"
    return page

def test_page_has_app(page):
    assert_that(page.app, not_none())

def test_page_has_webdriver(page):
    assert_that(page.webdriver, not_none())

def test_page_has_webelement(page):
    assert_that(page.webelement, not_none())

def test_page_refreshes(page):
    page.refresh()
    page.webdriver.refresh.assert_called_once()

def test_page_opens(page):
    page.open()
    page.app.open.assert_called_with("https://yandex.ru")

def test_page_forwards(page):
    page.forward()
    page.webdriver.forward.assert_called_once()

def test_page_backs(page):
    page.back()
    page.webdriver.back.assert_called_once()
