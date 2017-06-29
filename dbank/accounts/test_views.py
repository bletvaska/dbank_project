import pytest
from selenium.webdriver import Chrome


@pytest.fixture(scope='session')
def webdriver():
    driver = Chrome()
    yield driver
    driver.quit()


def test_when_homepage_is_open_then_h1_contains_hello_world(live_server, webdriver):
    webdriver.get(live_server.url + '/')
    h1 = webdriver.find_element_by_tag_name('h1')
    assert h1.text == 'Hello, world!'
