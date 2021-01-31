import sqlite3
import json
import datetime
import time
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BackgroundScheduler

init_config = json.loads(open('config.json', 'r').read())

item_id = '114119260'

driver = Firefox()
driver.get('https://www.shopgoodwill.com/SignIn')

username_input = driver.find_element_by_id('Username')
username_input.send_keys(init_config['username'])
password_input = driver.find_element_by_id('Password')
password_input.send_keys(init_config['password'])
driver.find_element_by_id('login-submit').click()

driver.get('https://www.shopgoodwill.com/Item/' + str(item_id))
minimum_bid = float(driver.find_element_by_css_selector('.minimum-bid').get_attribute('innerHTML')[1:])
bid_amount = minimum_bid + init_config['added_to_bid']

driver.find_element_by_css_selector('.cc-btn.cc-dismiss').click()


bid_input = driver.find_element_by_id('bidAmount')
bid_input.send_keys('{:.2f}'.format(round(bid_amount, 2)))
driver.find_element_by_id('placeBid').click()
driver.find_element_by_id('place-bid-modal').click()