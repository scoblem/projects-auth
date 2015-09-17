import json

SECRET_KEY = 'm9rd8iau9b1-o8v=e3h0p&qcjn$t(*+e!b8(df0-4fu#1s(xz3'

def get_auth():
    try:
        with open('database.json', 'r') as f:
            in_data = json.load(f)
    except (IOError, ValueError):
        in_data = {}
    return in_data

# overwrite json file with current state of 'database'.
def save_auth(out_data):
    with open('database.json', 'w') as f:
        json.dump(out_data, f)
