#! /usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import json
import os

from lxml import html
import psycopg2

from settings import APIKEY, DATADIR, DB_INFO


DATAKEYS = 'title originallink description pubdate'.split()
SEARCHAPI = 'http://openapi.naver.com/search?key=%s&target=news&start=%s&display=100&sort=date&query=%s'

def init_db(password):
    addr = ' '.join(["%s='%s'" % (a, b) for a, b in DB_INFO.items() if b])
    conn = psycopg2.connect(addr)
    return conn.cursor()

def get_n_days_before(n_days):
    return (date.today() - timedelta(n_days)).isoformat()

def get_bills_since(date, cursor=None):
    if not cursor:
        cursor = init_db()
    cursor.execute("""select id from bill where proposed_date >= '%s'""" % date)
    return [b[0] for b in cursor.fetchall()]

def get_new_articles(billnum, page_start=1):
    query = '의안 %s' % billnum
    url = SEARCHAPI % (APIKEY, page_start, query)
    root = html.parse(url)
    total = int(root.xpath('//total/text()')[0])
    if total!=0:
        items = root.xpath('//item')
        return [{ key: item.xpath('./%s/text()' % key)[0] for key in DATAKEYS }\
                for item in items]
    else:
        return None

def read_write_json(new_articles, filename):
    articles = []
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            articles = json.load(f)
        links = [a['originallink'] for a in articles]
        new_articles = [a for a in new_articles if a['originallink'] not in links]
    if len(new_articles)!=0:
        with open(filename, 'w') as f:
            json.dump(new_articles, f, indent=2, ensure_ascii=False)
        print('%s added to %s articles in %s' % (len(new_articles), len(articles), filename))


date = get_n_days_before(365)
billnums = get_bills_since(date)
for billnum in billnums:
    new_articles = get_new_articles(billnum)
    if new_articles:
        read_write_json(new_articles, '%s/%s.json' % (DATADIR, billnum))
