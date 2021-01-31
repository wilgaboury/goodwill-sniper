import sqlite3
import os.path
from os import path

def start(args):
    conn = sqlite3.connect('/path/to/db')
    c = conn.cursor()

    # init database
    if len(c.execute("select * from sqlite_master where type = 'table'")) == 0:
        sql = open('init_database.sql', 'r').read()
        c.execute(sql)

def stop(args):
    return None