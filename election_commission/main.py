#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import json

from crawlers import *
from utils import InvalidTargetError

Settings = {
    'START': 17,
    'END': 19
}

def crawl(target, output):
    crawler = None
    if 1 <= target <= 16:
        pass # TODO: not implemented yet
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

    with open(output, 'w') as f:
        json.dump(cand_list, f, indent=2)

def main():
    for n in xrange(Settings['START'], Settings['END']+1):
        filename = 'cand-%d.json' % (n,)
        crawl(target=n, output=filename)

if __name__ == '__main__':
    main()
