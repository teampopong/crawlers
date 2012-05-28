#!/usr/bin/env python

import json
from pymongo import Connection


DB_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'database': 'popongdb',
    'collection': 'candidates'
    }


def connect_db(host, port, database, collection):
    conn = Connection(host, port)
    db = conn[database]
    col = db[collection]
    return (conn, col)


def main():
    conn, col = connect_db(**DB_SETTINGS)

    with open('candidates.json', 'r') as f:
        data = json.load(f, encoding='utf-8')

    for record in data:
        col.save(record)

    conn.close()


if __name__ == '__main__':
    main()
