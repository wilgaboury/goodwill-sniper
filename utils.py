import sqlite3
import subprocess
import signal
import os
import psutil
import re
import pytz
import socket
from tzlocal import get_localzone
from dateutil.parser import parse
from multiprocessing.connection import Client
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BackgroundScheduler

def get_conn():
    conn = sqlite3.connect('sniper.db')
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# def send_msg(msg):
#     connection = Client(('localhost', 6000))
#     connection.sendall(msg)
#     connection.close()

def send_msg(msg):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 6000))
    s.sendall(msg.encode())
    s.close()

def retreive_listing_information(item_id):
    driver = Firefox()
    driver.get('https://www.shopgoodwill.com/Item/' + str(item_id))

    driver.find_element_by_css_selector('.cc-btn.cc-dismiss').click()

    name = driver.find_element_by_css_selector('.product-title').get_attribute('innerHTML')
    ending_dt_raw = driver.find_element_by_css_selector('.product-data>li:last-child').get_attribute('innerHTML')
    driver.quit()

    pattern = re.compile("<b>.*<\\/b>(.*) Pacific Time")
    matcher = pattern.search(ending_dt_raw)
    ending_dt_str = matcher.group(1)
    ending_dt = parse(ending_dt_str)
    tz = pytz.timezone('US/Pacific')
    ending_dt = tz.localize(ending_dt)
    ending_dt = ending_dt.astimezone(get_localzone())
    ending_dt = ending_dt.replace(tzinfo=None)

    return {'name': name, 'ending_dt': ending_dt}
