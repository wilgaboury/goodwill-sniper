import sqlite3
import json
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from apscheduler.schedulers.background import BackgroundScheduler

conn = sqlite3.connect('sniper.db')
c = conn.cursor()

listings = c.execute("select * from listings")

config = json.loads(open('config.json', 'r').read())