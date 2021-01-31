import sqlite3
import subprocess
import signal
import os
import psutil

def start(args):
    conn = sqlite3.connect('sniper.db')
    c = conn.cursor()

    pid = None
    c.execute('SELECT pid FROM process')
    processes = c.fetchall()
    for process in processes:
        if psutil.pid_exists(process.pid):
            pid = process.pid
            break

    if len(processes) > 1:
        if pid == None:
            c.execute('DELETE FROM process')
        else:
            c.execute('DELETE FROM process WHERE pid != ?', (pid,))

    if pid != None:
        print('Sniper process is already running')
    else:
        proc = subprocess.Popen(['python', 'deamon.py'])
        pid = proc.pid
        c.execute('INSERT INTO process (pid) VALUES (?)', (pid,))

    c.close()
    conn.close()

def stop(args):
    conn = sqlite3.connect('sniper.db')
    c = conn.cursor()

    c.execute('SELECT pid FROM process')
    processes = c.fetchall()
    for process in processes:
        if psutil.pid_exists(process.pid):
            os.kill(int(process.pid), signal.SIGKILL)
    c.execute('DELETE FROM process')

    c.close()
    conn.close()

def create(args):
    return None

def delete(args):
    return None

def update(args):
    return None

def print_list(args):
    conn = sqlite3.connect('sniper.db')
    c = conn.cursor()

    c.execute('SELECT * FROM listings')
    listings = c.fetchall()
    for listing in listings:
        print('https://www.shopgoodwill.com/Item/' + str(listing.item_id))

    c.close()
    conn.close()