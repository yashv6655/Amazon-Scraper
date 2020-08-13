import time
from selenium.webdriver.common.keys import Keys
from amazon_filters import (
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY
)
from driver_configs import (get_web_driver_options,
                            get_chrome_web_driver,
                            set_ignore_certificate_error,
                            set_browser_as_incognito)
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime


class GenerateProductReport:
    def __init__(self, file_name, filters, base_link, currency, data):
        self.data = data
        self.file_name = file_name
        self.filters = filters
        self.base_link = base_link
        self.currency = currency
        report = {
            'title': self.file_name,
            'date': self.get_now(),
            'best_item': self.get_best_item(),
            'currency': self.currency,
            'filters': self.filters,
            'base_link': self.base_link,
            'products': self.data
        }
        if self.data is None:
            return print("Could not create a report for the items.")

        print("Creating report...")
        with open(f'{DIRECTORY}/{file_name}.json', 'w') as f:
            json.dump(report, f)
        print("Done...")

    @staticmethod
    def get_now():
        now = datetime.now()
        return now.strftime("%m/%d/%Y %H:%M:%S")

    def get_best_item(self):
        try:
            return sorted(self.data, key=lambda k: k['price'])[0]
        except Exception as e:
            print(e)
            print("Error while sorting items.")
            return None


class AmazonAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency
        self.price_filter = f"&rh=p_36%3A{filters['min']}00-{filters['max']}00"

    def run(self):
        print("Starting Script...")
        print(f"Searching for {self.search_term} on {self.base_url}")
        links = self.get_products_links()
        if not links:
            print("Stopped script.")
            return
        print(f"Found {len(links)} links.")
        print("Getting info about products...")
        products = self.get_products_info(links)
        print(f"Got info for {len(products)} products...")
        self.driver.quit()
        # print(products)
        return products

    def get_products_links(self):
        self.driver.get(self.base_url)
        element = self.driver.find_element_by_xpath(
            '//*[@id="twotabsearchtextbox"]')
        element.send_keys(self.search_term)
        element.send_keys(Keys.ENTER)
        time.sleep(2)  # wait to load page
        self.driver.get(f'{self.driver.current_url}{self.price_filter}')
        print(f"Our url: {self.driver.current_url}")
        time.sleep(2)  # wait to load page
        result_list = self.driver.find_elements_by_class_name(
            's-result-list' or 'sg-col-inner')
        links = []
        try:
            results = result_list[0].find_elements_by_xpath(
                "//div/span/div/div/div[2]/div[2]/div/div[1]/div/div/div[1]/h2/a")
            links = [link.get_attribute('href') for link in results]
            return links
        except Exception as e:
            print("Didn't get any products...")
            print(e)
            return links

    def get_products_info(self, links):
        products = []
        for link in links:
            product = self.get_single_product_info(link)
            if product:
                products.append(product)
        return products

    def get_single_product_info(self, link):
        print(f"Evaluating: {link}")
        self.driver.get(link)
        time.sleep(2)
        title = self.get_title()
        seller = self.get_seller()
        price = self.get_price()
        if title and seller and price:
            product_info = {
                'url': link,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            return self.driver.find_element_by_id('productTitle').text
        except Exception as e:
            print(e)
            print(f"Can't get title of product - {self.driver.current_url}")
            return None

    def get_seller(self):
        try:
            return self.driver.find_element_by_id('bylineInfo').text
        except Exception as e:
            print(e)
            print(f"Can't get seller of product - {self.driver.current_url}")
            return None

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_id('priceblock_ourprice').text
            price = self.convert_price(price)
        except NoSuchElementException:
            try:
                availability = self.driver.find_element_by_id(
                    'availability').text
                if 'Available' in availability:
                    price = self.driver.find_element_by_class_name(
                        'olp-padding-right').text
                    price = price[price.find(self.currency):]
                    price = self.convert_price(price)
            except Exception as e:
                print(e)
                print(
                    f"Can't get price of a product - {self.driver.current_url}")
                return None
        except Exception as e:
            print(e)
            print(f"Can't get price of a product - {self.driver.current_url}")
            return None
        return price

    def convert_price(self, price):
        price = price.split(self.currency)[1]
        try:
            price = price.split("\n")[0] + "." + price.split("\n")[1]
        except:
            Exception()
        try:
            price = price.split(",")[0] + price.split(",")[1]
        except:
            Exception()
        return float(price)


if __name__ == "__main__":
    amazon = AmazonAPI(NAME, FILTERS, BASE_URL, CURRENCY)
    data = amazon.run()
    GenerateProductReport(NAME, FILTERS, BASE_URL, CURRENCY, data)
