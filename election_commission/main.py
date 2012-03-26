#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import json

from crawlers import Crawler19

Settings = {
    'START': 19,
    'END': 19
}

def crawl(target, output):
    crawler = None
    if 1 <= target <= 16:
        pass # TODO: not implemented yet
    elif 17 <= target <= 18:
        pass # TODO: not implemented yet
    elif 19 <= target <= 19:
        crawler = Crawler19()
    else:
        raise Exception('invalid parameter')

    print 'crawling %dth...' % (target,)
    cand_list = crawler.crawl()

    with open(output, 'w') as f:
        json.dump(cand_list, f, indent=2)

def main():
    for n in xrange(Settings['START'], Settings['END']+1):
        filename = 'cand-%d.json' % (n,)
        crawl(target=n, output=filename)

if __name__ == '__main__':
    main()
