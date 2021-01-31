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

def start(args):
    conn, c = get_conn()

    pid = None
    c.execute('SELECT pid FROM process')
    processes = c.fetchall()
    for process in processes:
        if psutil.pid_exists(process['pid']):
            pid = process['pid']
            break

    if len(processes) > 1:
        if pid == None:
            c.execute('DELETE FROM process')
        else:
            c.execute('DELETE FROM process WHERE pid != ?', (pid,))
        conn.commit()

    if pid != None:
        print('Sniper process is already running')
    else:
        proc = subprocess.Popen(['python', 'deamon.py'], start_new_session=True)
        pid = proc.pid
        c.execute('INSERT INTO process(pid) VALUES(?)', (pid,))
        conn.commit()
        print('Sniper process succcessfully started')

    c.close()
    conn.close()

def stop(args):
    try:
        send_msg("close")
        print('Sniper process successfully closed')
    except ConnectionRefusedError as e:
        print('Sniper process has already been closed')

    conn, c = get_conn()
    c.execute('DELETE FROM process')
    conn.commit()
    c.close()
    conn.close()

def create(args):
    return None

def delete(args):
    return None

def update(args):
    return None

def print_list(args):
    conn, c = get_conn()

    c.execute('SELECT * FROM listings')
    listings = c.fetchall()
    for listing in listings:
        print('https://www.shopgoodwill.com/Item/' + str(listing['item_id']))

    c.close()
    conn.close()