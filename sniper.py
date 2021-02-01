import argparse
import utils
import sqlite3
import sys
import subprocess
import psutil

# init database
conn, c = utils.get_conn()
c.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND (name = 'listings' OR name = 'process')")
tables = c.fetchall()
if len(tables) != 2:
    print('initializing database')
    sql = open('init_database.sql', 'r').read()
    c.executescript(sql)
    conn.commit()
c.close()
conn.close()

# New better cli interface
class SniperCLI(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Sniper for Goodwill Website',
            usage='sniper.py <command> [<args>]'
        )
        parser.add_argument('command')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def start(self):
        conn, c = utils.get_conn()

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
            print('Sniper process succcessfully started with PID ' + str(pid))

        c.close()
        conn.close()

    def stop(self):
        try:
            utils.send_msg("close")
            print('Sniper process successfully closed')
        except ConnectionRefusedError:
            print('Sniper process has already been closed')

        conn, c = utils.get_conn()
        c.execute('DELETE FROM process')
        conn.commit()
        c.close()
        conn.close()

    def create(self):
        parser = argparse.ArgumentParser(description='Create new item to snipe')
        parser.add_argument('-i', '--item', action='store', type=int, required=True)
        parser.add_argument('-m', '--max', action='store', type=int, required=True)
        args = parser.parse_args(sys.argv[2:])

        item_data = utils.retreive_listing_information(args.item)

        conn, c = utils.get_conn()
        c.execute('INSERT INTO listings(item_id, max_bid, name, ending_dt) VALUES(?,?,?,?)', (args.item, args.max, item_data['name'], item_data['ending_dt']))
        conn.commit()
        c.close()
        conn.close()


    def delete(self):
        parser = argparse.ArgumentParser(description='Delete an item from sniping list')
        parser.add_argument('-i', '--item', action='store', type=int, required=True)
        args = parser.parse_args(sys.argv[2:])

        conn, c = utils.get_conn()
        c.execute('DELETE FROM listings WHERE item_id=?', (args.item))
        conn.commit()
        c.close()
        conn.close()

        try:
            utils.send_msg('update')
        except ConnectionRefusedError:
            pass

    def update(self):
        parser = argparse.ArgumentParser(description='Delete an item from sniping list')
        parser.add_argument('-i', '--item', action='store', type=int, required=True)
        parser.add_argument('-m', '--max', action='store', type=int, required=True)
        args = parser.parse_args(sys.argv[2:])

        conn, c = utils.get_conn()
        c.execute('UPDATE listings SET max_bid=? WHERE item_id=?', (args.max, args.item))
        conn.commit()
        c.close()
        conn.close()

        try:
            utils.send_msg('update')
        except ConnectionRefusedError:
            pass

    def list(self):
        conn, c = utils.get_conn()

        c.execute('SELECT * FROM listings')
        listings = c.fetchall()
        for listing in listings:
            print('https://www.shopgoodwill.com/Item/' + str(listing['item_id'] + 'Name: ' + str(listings['name']) + ', Max Bid: ' + str(listings['max_bid'])))

        c.close()
        conn.close()

        try:
            utils.send_msg('update')
        except ConnectionRefusedError:
            pass

SniperCLI()