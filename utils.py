import sqlite3
import subprocess
import signal
import os
import psutil
from multiprocessing.connection import Client

def get_conn():
    conn = sqlite3.connect('sniper.db')
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

def send_msg(msg):
    connection = Client(('localhost', 6000))
    connection.send(msg)
    connection.close()