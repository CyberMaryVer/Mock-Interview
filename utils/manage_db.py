# create csv, list csv, visualise csv from ./db/*.csv

import random
import csv
import uuid
import pandas as pd
from datetime import datetime


def create_keys(key_num, key_uses=10, rand_uses=True, key_file='./db/user_keys.csv'):
    with open(key_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "key", "uses", "last_used", "created_at"])

    # create 10 keys
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    key_template = lambda k: f"key-{k:06d}-{str(uuid.uuid4())[:8]}"
    uses = lambda k: random.randint(1, key_uses) if rand_uses else key_uses
    last_used = 0

    for i in range(key_num):
        with open(key_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(uuid.uuid4()),
                             key_template(i),
                             uses(i),
                             last_used,
                             created_at])


def get_key(key_file='./db/user_keys.csv'):
    # get key: check if key is valid, if yes, return key, else return None
    keys = pd.read_csv(key_file)
    valid_keys = keys.loc[keys['uses'] > 0, 'key'].values.tolist()
    return valid_keys


def get_key_info(key, key_file='./db/user_keys.csv'):
    # get key info: return key info
    keys = pd.read_csv(key_file)
    key_info = keys.loc[keys['key'] == key, :].to_dict('records')[0]
    return key_info


def update_key(key, key_file='./db/user_keys.csv'):
    # update key: decrease uses by 1, update last_used and updated_at
    keys = pd.read_csv(key_file)
    keys.loc[keys['key'] == key, 'uses'] -= 1
    keys.loc[keys['key'] == key, 'last_used'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keys.to_csv(key_file, index=False)
    return keys.loc[keys['key'] == key, 'uses'].values[0]


if __name__ == "__main__":
    create_keys(10, key_file='./../db/user_keys.csv')
    keys = get_key(key_file='./../db/user_keys.csv')
    print(keys)
    key_info = get_key_info(key=keys[4], key_file='./../db/user_keys.csv')
    print(key_info)
    uses = update_key(key=keys[4], key_file='./../db/user_keys.csv')
    print(uses)
