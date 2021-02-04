import argparse
import utils
import sqlite3
import sys
import subprocess
import psutil
from tzlocal import get_localzone
from dateutil.parser import parse

# init database
conn, c = utils.get_conn()
c.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND (name = 'listings' OR name = 'process')")
tables = c.fetchall()
if len(tables) != 2:
    print('initializing database')
    with open('init_database.sql', 'r') as init_script:
        sql = init_script.read()
    c.executescript(sql)
    conn.commit()
c.close()
conn.close()

# New better cli interface
class SniperCLI(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Command Line Sniper for the Goodwill Shopping Website',
            usage='''sniper.py <command> [<args>]

List of sniper commands:
    start   Initializes the sniping background process
    stop    Terminates the sniping background process
    restart Terminates then initialized the sniping background process
    status  Prints the status of the sniping background process
    create  Adds and schedules a specified item to be sniped
    delete  Stops a specified item from being sniped
    update  Used to update the max bid for a specified item
    list    Prints the list of items scheduled to be sniped
'''
        )
        parser.add_argument('command', help='name of command to be executed')

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def start(self):
        conn, c = utils.get_conn()

        c.execute('SELECT pid FROM process')
        pid_row = c.fetchone()

        if pid_row != None and psutil.pid_exists(pid_row['pid']):
            print('Sniper process is already running')
            return
        else:
            c.execute('DELETE FROM process')
            conn.commit()

            proc = subprocess.Popen(['python', 'deamon.py'], start_new_session=True)
            pid = proc.pid

            c.execute('INSERT INTO process(pid) VALUES(?)', (pid,))
            conn.commit()

            print('Sniper process succcessfully started with PID ' + str(pid))

        c.close()
        conn.close()

    def stop(self):
        conn, c = utils.get_conn()

        c.execute('SELECT * FROM process')
        pid_row = c.fetchone()
        if pid_row != None and psutil.pid_exists(pid_row['pid']):
            psutil.Process(pid_row['pid']).kill()
            print('Sniper process successfully terminated')
        else:
            print('Sniper process is not currently running')
        
        c.execute('DELETE FROM process')
        conn.commit()

        c.close()
        conn.close()

    def restart(self):
        self.stop()
        self.start()

    def status(self):
        conn, c = utils.get_conn()

        c.execute('SELECT pid FROM process')
        pid_row = c.fetchone()

        if pid_row != None and psutil.pid_exists(pid_row['pid']):
            print('Sniper process is running')
        else:
            print('Sniper process is *not* running')
        
        c.close()
        conn.close()

    def create(self):
        parser = argparse.ArgumentParser(description='Create new item to snipe')
        required = parser.add_argument_group('required named arguments')
        required.add_argument('-i', '--item', action='store', type=int, required=True)
        required.add_argument('-m', '--max', action='store', type=int, required=True)
        args = parser.parse_args(sys.argv[2:])

        item_data = utils.retreive_listing_information(args.item)

        conn, c = utils.get_conn()
        c.execute('INSERT INTO listings(item_id, max_bid, name, ending_dt) VALUES(?,?,?,?)', (args.item, args.max, item_data['name'], item_data['ending_dt']))
        conn.commit()

        print('Successfully added snipe for item #' + str(args.item))

        c.close()
        conn.close()


    def delete(self):
        parser = argparse.ArgumentParser(description='Delete an item from sniping list')
        required = parser.add_argument_group('required named arguments')
        required.add_argument('-i', '--item', nargs='+', action='store', type=int, required=True)
        args = parser.parse_args(sys.argv[2:])

        conn, c = utils.get_conn()
        for item in args.item:
            c.execute('DELETE FROM listings WHERE item_id=?', (item,))
        conn.commit()
        c.close()
        conn.close()

        try:
            utils.send_msg('update')
        except ConnectionRefusedError:
            pass

    def update(self):
        parser = argparse.ArgumentParser(description='Delete an item from sniping list')
        required = parser.add_argument_group('required named arguments')
        required.add_argument('-i', '--item', action='store', type=int, required=True)
        required.add_argument('-m', '--max', action='store', type=int, required=True)
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

        c.execute('SELECT * FROM listings ORDER BY ending_dt')
        listings = c.fetchall()
        for listing in listings:
            ending_dt = parse(listing['ending_dt'])
            print(str(listing['item_id']) + ' | ' + str(ending_dt) + ' | ' + str(listing['name']) + ' | Max Bid: ' + str(listing['max_bid']) + ' | URL: ' + 'https://www.shopgoodwill.com/Item/' + str(listing['item_id']))
        
        c.close()
        conn.close()

        try:
            utils.send_msg('update')
        except ConnectionRefusedError:
            pass

    def dump(self):
        utils.send_msg('dump')

SniperCLI()