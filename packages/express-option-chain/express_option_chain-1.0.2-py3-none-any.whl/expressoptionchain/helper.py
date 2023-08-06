import json
import os


def read_from_file(filename):
    try:
        with open(filename, 'r') as f:
            content = f.read()
            return content
    except:
        return None


def get_time_in_str(dt):
    if not dt:
        return dt
    return dt.strftime("%d-%m-%Y %H:%M:%S")


def get_secrets():
    return {'access_token': read_from_file(f'{os.environ["HOME"]}/.kite/access_token'),
            'api_key': read_from_file(f'{os.environ["HOME"]}/.kite/api_key'),
            'api_secret': read_from_file(f'{os.environ["HOME"]}/.kite/api_secret')
            }


def get_hash_value(r, hash_name, key):
    val = r.hget(hash_name, key)
    if val:
        return json.loads(val)
    return val
