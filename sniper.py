import argparse
import utils
import sqlite3

FUNCTION_MAP = {
    'start': utils.start,
    'stop': utils.stop,
    'create': utils.create,
    'delete': utils.delete,
    'update': utils.update,
    'list': utils.print_list
}

parser = argparse.ArgumentParser(description='Sniper for Goodwill Website')
parser.add_argument('command', choices=FUNCTION_MAP.keys())
args = parser.parse_args()

#init database
conn = sqlite3.connect('sniper.db')
c = conn.cursor()
if len(c.execute("select * from sqlite_master where type = 'table'")) == 0:
    sql = open('init_database.sql', 'r').read()
    c.execute(sql)

FUNCTION_MAP[args.command](args)