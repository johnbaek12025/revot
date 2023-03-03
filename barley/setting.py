import os
import json

CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config')

def get_database_info():
    fp = os.path.join(CONFIG_DIR, 'databases')
    with open(fp, 'r') as f:
        return json.load(f)


def get_debug_database_info():
    fp = os.path.join(CONFIG_DIR, 'databases-debug')
    with open(fp, 'r') as f:
        return json.load(f)
    
def get_secret_key():
    fp = os.path.join(CONFIG_DIR, 'secret_key')
    with open(fp, 'r') as f:
        return json.load(f)

def get_debug():
    fp = os.path.join(CONFIG_DIR, 'debug')
    if not os.path.exists(fp):
        return False
    with open(fp, 'r') as f:
        return json.load(f)
    
def get_allowed_hosts():
    fp = os.path.join(CONFIG_DIR, 'allowed_hosts')
    with open(fp, 'r') as f:
        return json.load(f)