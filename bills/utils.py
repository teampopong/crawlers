#! /usr/bin/python
# -*- coding: utf-8 -*-

import codecs
from datetime import date, datetime
from functools import wraps
import json

from lxml import html
from pymongo import MongoClient
import requests


ENCODING = 'utf8'


# decorators
def catch(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
        except Exception as e:
            print(e.__repr__())
            r = None
        return r
    return wrapper


# crawl
def get_root(url, data, method='GET'):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'http://likms.assembly.go.kr/bill/jsp/LatestReceiptBill.jsp'
    }
    if method=='GET':
        rqst = requests.get(url, params=data)
    else:
        rqst = requests.post(url, headers=headers, data=data)
    root = html.fromstring(rqst.text)
    return root


# db
def init_db(uri, dbname, collections=None):
    client = MongoClient(uri)
    db = client[dbname]
    if collections:
        for c in collections:
            if not db[c].find_one():
                db.create_collection(c)
                db[c].create_index({'id': 1})
                print('Created collection %s' % c)
    return db


# io
def write_json(data, filename):
    d = json.dumps(data, ensure_ascii=False, indent=2)
    with codecs.open(filename, 'w', encoding=ENCODING) as f:
        f.write(d)


# time
def now():
    return datetime.today().isoformat().split('.')[0]


def today():
    return date.today().isoformat()
