#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2
import gevent
from gevent import monkey; monkey.patch_all()


def get_files(directory, base, url_ext, file_ext):
    if not os.path.exists(directory):
        os.makedirs(directory)
    empty = []
    jobs = [gevent.spawn(_get_file, directory, base, url_ext, file_ext, num)\
            for num in range(859, NUM+1)]
    gevent.joinall(jobs)

def _get_file(directory, base, url_ext, file_ext, num):

    url = base + str(num) + url_ext
    outp = directory + str(num) + file_ext

    is_empty = False

    try:
        r = urllib2.urlopen(url)
        with open(outp, 'w') as f:
            f.write(r.read())
        print '%s to %s' % (num, outp)
    except urllib2.HTTPError, e:
        is_empty = True
        print '%s is empty' % num

    return is_empty

if __name__=='__main__':
    NUM = 2810
    base_url = 'http://www.rokps.or.kr'
    get_files('html/', '%s/profile_result_ok.asp?num=' % base_url, '', '.html')
    get_files('images/', '%s/images/user/' % base_url, '.jpg', '.jpg')

