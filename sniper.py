import argparse
import utils

FUNCTION_MAP = {
    'start': utils.start,
    'stop': utils.stop,
    'create': None,
    'delete': None,
    'update': None
}

parser = argparse.ArgumentParser(description='Sniper for Goodwill Website')
parser.add_argument('command', choices=FUNCTION_MAP.keys())
args = parser.parse_args()

FUNCTION_MAP[args.command](args)