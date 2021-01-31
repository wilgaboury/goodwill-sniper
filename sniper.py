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

# run user specified function
FUNCTION_MAP[args.command](args)