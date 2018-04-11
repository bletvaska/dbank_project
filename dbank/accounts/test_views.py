import pytest
from django.urls import resolve
from selenium.webdriver import Chrome

from .views import AccountListView


@pytest.fixture(scope='session')
def webdriver():
    driver = Chrome()
    yield driver
    driver.quit()


def test_when_homepage_is_open_then_h1_contains_hello_world(live_server, webdriver):
    webdriver.get(live_server.url + '/')
    h1 = webdriver.find_element_by_tag_name('h1')
    assert h1.text == 'Hello, world!'


def test_if_accounts_url_is_resolved_as_account_list_view():
    view = resolve('/accounts')
    assert view.func == AccountListView