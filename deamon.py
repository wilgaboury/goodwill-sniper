import sqlite3
import json
import datetime
import pause
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BackgroundScheduler

conn = sqlite3.connect('sniper.db')
c = conn.cursor()
init_config = json.loads(open('config.json', 'r').read())
scheduler = BackgroundScheduler()

def perform_snipe(item_id, listing_dt):
    try:
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

        pause.until(listing_dt - datetime.timedelta(seconds=init_config['added_to_bid']))

        driver.find_element_by_id('placeBid').click()
        driver.find_element_by_id('place-bid-modal').click()

    except Exception as e:
        print("Sniping item #" + str(item_id) + " failed")
        print(e)
    else:
        print("sniped item #" + str(item_id))

c.execute("select * from listings")
listings = c.fetchall()
for listing in listings:
    listing_dt = listings.ending_dt
    listing_dt = listing_dt - datetime.timedelta(minutes=1, seconds=init_config['bid_before_seconds'])
    scheduler.add_job(perform_snipe, 'date', runtime=listing_dt, args=[listing.item_id, listing.listing_dt])

scheduler.start()