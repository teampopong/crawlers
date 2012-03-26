#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import json

from crawlers import *
from utils import InvalidTargetError
from types import UnicodeType

Settings = {
    'START': 1,
    'END': 19,
    'FILETYPE': 'csv'
}

def print_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(cand_list, f, indent=2)

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
    if 1 <= target <= 16:
        crawler = CrawlerUntil16()
    elif target == 17:
        crawler = Crawler17()
    elif target == 18:
        crawler = Crawler18()
    elif target == 19:
        crawler = Crawler19()
    else:
        raise InvalidTargetError(target)

    print 'crawling %d대...' % (target,)
    cand_list = crawler.crawl(target)

    printer(filename, cand_list)

def main():
    printer = print_json if Settings['FILETYPE'] == 'json' else print_csv

    for n in xrange(Settings['START'], Settings['END']+1):
        filename = 'cand-%d.%s' % (n, Settings['FILETYPE'])
        crawl(target=n, filename=filename, printer=printer)

if __name__ == '__main__':
    main()
