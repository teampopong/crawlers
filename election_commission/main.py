#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import json

from crawlers import *
import gevent
from gevent import monkey
from utils import InvalidTargetError
from types import UnicodeType

Settings = {
    'START': 1,
    'END': 19,
    'FILETYPE': 'csv'
}

def print_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, encoding="UTF-8", indent=2)

def print_csv(filename, data):

    def transform(txt):
        txt = txt.replace(',', '|')
        if isinstance(txt, UnicodeType):
            txt = txt.encode('utf8')
        return txt

    attrs = ['district', 'cand_no', 'party', 'name', 'name_cn', 'sex',
             'birthyear', 'birthmonth', 'birthday', 'address', 'job',
             'education', 'experience']

    with open(filename, 'w') as f:
        for cand in data:
            values = (cand[attr] if attr in cand else '' for attr in attrs)
            values = (transform(value) for value in values)
            f.write(','.join(values))
            f.write('\n')

def crawl(target, printer, filename):
    crawler = None
    if 1 <= target <= 6:
        crawler = CandCrawlerUntil6(target)
    elif target <= 16:
        crawler = CandCrawlerUntil16(target)
    elif target == 17:
        crawler = CandCrawler17()
    elif target == 18:
        crawler = CandCrawler18()
    elif target == 19:
        crawler = CandCrawler19()
    else:
        raise InvalidTargetError(target)

    cand_list = crawler.crawl()
    printer(filename, cand_list)

def main():
    printer = print_json if Settings['FILETYPE'] == 'json' else print_csv

    jobs = []
    for n in xrange(Settings['START'], Settings['END']+1):
        filename = 'cand-%d.%s' % (n, Settings['FILETYPE'])
        job = gevent.spawn(crawl, target=n, filename=filename, printer=printer)
        jobs.append(job)
    gevent.joinall(jobs)

if __name__ == '__main__':
    monkey.patch_all()
    main()
