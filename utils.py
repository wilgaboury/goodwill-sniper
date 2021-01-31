import sqlite3
import subprocess
import signal
import os
import psutil
from multiprocessing.connection import Client
from multiprocessing.connection import Listener
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

def send_msg_with_data(msg, data):
    connection = Client(('localhost', 6000))
    connection.send((msg, data))
    connection.close()

def send_msg(msg):
    send_msg_with_data(msg, None)

def retreive_listing_information(item_id):
    driver = Firefox()
    driver.get('https://www.shopgoodwill.com/Item/' + str(item_id))
    name = driver.find_element_by_css_selector('.product-title').getAttribute('innerHTML')

    return {'name': name}
