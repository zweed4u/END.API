#!/usr/bin/python3
import os
import requests
from selenium import webdriver


class Launches:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.session()
        self.base_url = 'https://launches-api.endclothing.com/api/'
        self.cookie_string = ''
        self.get_browser_cookies()
        self.headers = {
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Origin': 'https://launches.endclothing.com',
            'Allow': 'POST',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Encoding': 'gzip',
            'Content-Type': 'application/json',
            #'Date': 'Thu, 03 May 2018 21:46:25 GMT',
            'Server': 'nginx',
            'Vary': 'Accept-Encoding',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Access-Control-Allow-Credentials': 'true',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': self.cookie_string[:-1],
            'Host': 'launches-api.endclothing.com',
            'Origin': 'https://launches.endclothing.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
        }

    def get_browser_cookies(self):
        driver = webdriver.Chrome(f'{os.getcwd()}/chromedriver')
        driver.get('https://launches.endclothing.com/')
        driver.refresh()
        cookies = driver.get_cookies()
        for cookie in cookies:
            self.cookie_string += f'{cookie["name"]}={cookie["value"]}; '
        driver.close()

    def make_request(self, method, endpoint, params=None, data=None, json=None, json_content=True):
        if json_content is True:
            return self.session.request(method, f'{self.base_url}{endpoint}', params=params, data=data, json=json, headers=self.headers)
        else:
            return self.session.request(method, f'{self.base_url}{endpoint}', params=params, data=data, json=json, headers=headers)

    def login(self):
        data = {
            'login[email]': self.email,
            'login[password]': self.password
        }
        self.make_request('OPTIONS', 'account/login')
        return self.make_request('POST', 'account/login', data=data)

    def locate(self):
        return self.make_request('POST', 'account/locate')

    def get_all_countries(self):
        return self.make_request('GET', 'countries/all')

    def get_categories(self):
        return self.make_request('GET', 'categories')

    def get_account(self):
        return self.make_request('GET', 'account')

    def get_products(self):
        return self.make_request('GET', 'products/offset/0')

    def get_settings(self):
        return self.make_request('GET', 'settings')

    def get_product(self, product_path):
        # via get_products()['products'][]['urlKey']
        return self.make_request('GET', f'products/{product_path}')

    def get_stores(self):
        return self.make_request('GET', 'admin/store')

    def has_subscribed(self, product_id):
        data = {
            'productId': product_id  # retrieved from get_products()['products']
        }
        return self.make_request('POST', 'account/has-subscribed', data=data)

    def get_account_payment_methods(self, account_id):
        # account_id via get_account()['id']
        return self.make_request('GET', f'account/{account_id}/payment-methods')

    def get_token(self):
        data = {
            '{}': ''
        }
        return self.make_request('POST', 'gateway/token', data=data)

    def submit_entry(self, account_id, size_id, shipping_id, billing_id, payment_method_id, shipping_method_id, zipcode, street_address, website_id='2'):
        data = {
            'subscription[customer_id]': account_id,  # via get_account()['id']
            'subscription[product_size_id]': size_id,  # retrieved via get_product()['productSizes']
            'subscription[shipping_address_id]': shipping_id,  # via get_account()['addresses'] or get_account()['default_shipping']
            'subscription[shipping_address_type]': 'magento',
            'subscription[billing_address_id]': billing_id,  # via get_account()['addresses'] or get_account()['default_shipping']
            'subscription[billing_address_type]': 'magento',
            'subscription[payment_method_id]': payment_method_id,  # via get_account()['custom_attributes'] 
            'subscription[payment_method_type]': 'magento',
            'subscription[shipping_method_id]': shipping_method_id,  # via get_all_countries()[1]['availableShippingMethods']  1=US index - '7'
            'subscription[website_id]': website_id,
            'subscription[postcode]': zipcode,
            'subscription[street]': street_address
        }
        return self.make_request('POST', 'account/subscriptions', data=data)

    def cancel_entry(self, account_id, product_id):
        data = {
            'customerId': account_id,  # via get_account()['id']
            'productId': product_id  # retrieved from get_products()['products']
        }
        return self.make_request('POST', 'account/delete/subscriptions', data=data)


END = Launches('EMAIL_HERE', 'PASSWORD_HERE')
print(END.login().json())
