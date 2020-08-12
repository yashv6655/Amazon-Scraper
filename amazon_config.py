from selenium import webdriver

DIRECTORY = 'reports'
NAME = 'PS4'  # Search bar input/query
CURRENCY = '$'
MIN_PRICE = '275'  # Minimum price
MAX_PRICE = '650'  # Maximum price
FILTERS = {
    'min': MIN_PRICE,
    'max': MAX_PRICE
}
BASE_URL = "http://www.amazon.com/"


def get_chrome_web_driver(options):
    return webdriver.Chrome("./chromedriver", chrome_options=options)


def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


def set_automation_as_head_less(options):
    options.add_argument('--headless')
