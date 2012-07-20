#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import argparse
import json
from pymongo import Connection


DB_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'database': 'popongdb',
    'collection': 'people'
    }


fields_key = ['name_kr', 'sex', 'birthyear', 'birthmonth', 'birthday']


def connect_db(host, port, database, collection):
    conn = Connection(host, port)
    db = conn[database]
    col = db[collection]
    return (conn, db, col)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('type', choices=['insert', 'update'])
    parser.add_argument('files', nargs='+', type=argparse.FileType('r'))
    return parser


def getkey(person, type=tuple):
    values = (person.get(field, None) for field in fields_key)
    if type == tuple:
        return tuple(values)
    elif type == dict:
        return dict(zip(fields_key, values))


def copy(_from, _to, fields=None):
    if not fields:
        fields = _from.keys()

    for field in fields:
        if field in _from and _from[field] not in ['', None]:
            _to[field] = _from[field]


def merge_person(old, new):
    if not old:
        old = {
              'assembly': {}
              }

    ### 국회 대수별 정보 업데이트 ###
    assembly_no = str(new['assembly_no'])

    # 없었던 정보면 초기화
    if assembly_no not in old['assembly']\
            or old['assembly'][assembly_no]['elected'] < new['elected']:
        old['assembly'][assembly_no] = new

    ### 최신 정보 ###
    if 'assembly_no' not in old or old['assembly_no'] < assembly_no:
        copy(new, old)

    return old


def insert(counters, col, person):
    next_id = counters.find_and_modify({ 'key': 'person_id' },
            update={ '$inc': { 'value': 1 }},
            new=True)
    person['id'] = int(next_id['value'])
    col.save(person)


def update(counters, col, record):
    key = getkey(record, dict)
    old = col.find_one(key)
    new = merge_person(old, record)
    if old:
        _id = old['id']
        col.update({ 'id': _id }, new, safe=True)
    else:
        # TODO: 코드 정리
        insert(counters, col, new)


def main(args):
    conn, db, col = connect_db(**DB_SETTINGS)
    counters = db['counters']

    if args.type == 'insert':
        col.drop()

    for file in args.files:
        print 'processing %s' % file.name
        data = json.load(file, encoding='utf-8')

        for record in data:
            if args.type == 'insert':
                insert(counters, col, record)
            elif args.type == 'update':
                update(counters, col, record)

    col.ensure_index('id')
    conn.close()


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)
