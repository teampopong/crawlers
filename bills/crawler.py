#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import gevent
from gevent import monkey; monkey.patch_all()
import utils
from settings import NUM_PAGES, MAX_PAGE, LIST_DIR, LIST_DATA, BASEURL

def get_files(page):
    url = BASEURL['list'] + 'PAGE=%d&PAGE_SIZE=%d' % (page*10+1, NUM_PAGES)
    fn = '%s/%s.html' % (LIST_DIR, str(page+1))
    utils.get_webpage(url, fn)
    print page+1

if __name__=='__main__':
    if not os.path.exists(LIST_DIR):
        os.makedirs(LIST_DIR)

    jobs = [gevent.spawn(get_files, page)\
            for page in range(MAX_PAGE/NUM_PAGES+1)]
    gevent.joinall(jobs)
