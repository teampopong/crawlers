#!/usr/bin/env python

import argparse
import json
from pymongo import Connection


DB_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'database': 'popongdb',
    'collection': 'people'
    }


def connect_db(host, port, database, collection):
    conn = Connection(host, port)
    db = conn[database]
    col = db[collection]
    return (conn, col)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=['insert', 'update'])
    parser.add_argument('file', type=argparse.FileType('r'))
    return parser


def main(args):
    conn, col = connect_db(**DB_SETTINGS)

    data = json.load(args.file, encoding='utf-8')

    if args.type == 'insert':
        col.drop()
        for _id, record in enumerate(data):
            record['id'] = _id
            col.save(record)
        col.ensure_index('id')

    elif args.type == 'update':
        for record in data:
            pass # TODO:

    conn.close()


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)
