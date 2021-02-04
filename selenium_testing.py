import sqlite3
import json
import datetime
import pause
import utils
import math
import socket
from dateutil.parser import parse
from multiprocessing.connection import Listener
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BackgroundScheduler

init_config = json.loads(open('config.json', 'r').read())

item_id = '114119260'
max_bid = 10

try:
    driver = Firefox()
    driver.get('https://www.shopgoodwill.com/SignIn')

    username_input = driver.find_element_by_id('Username')
    username_input.send_keys(init_config['username'])
    password_input = driver.find_element_by_id('Password')
    password_input.send_keys(init_config['password'])
    driver.find_element_by_id('login-submit').click()

    driver.get('https://www.shopgoodwill.com/Item/' + str(item_id))

    driver.find_element_by_css_selector('.cc-btn.cc-dismiss').click()

    minimum_bid = float(driver.find_element_by_css_selector('.minimum-bid').get_attribute('innerHTML')[1:])
    bid_amount = math.ceil(minimum_bid)

    while bid_amount <= max_bid:
        bid_input = driver.find_element_by_id('bidAmount')
        bid_input.send_keys('{:.2f}'.format(round(bid_amount, 2)))

        driver.find_element_by_id('placeBid').click()
        driver.find_element_by_id('place-bid-modal').click()

        if driver.find_element_by_id('bid-result').get_attribute('innerHTML').find('You have already been outbid.') >= 0:
            break
        else:
            driver.find_element_by_css_selector('.modal-footer button.btn.btn-default').click()
            bid_amount += 1

except Exception as e:
    print("Sniping item #" + str(item_id) + " failed")
    print(e)
else:
    print("sniped item #" + str(item_id))