#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import urllib2

directory = 'html/'
base = 'http://www.rokps.or.kr/profile_result_ok.asp?num='
num = 2810
ext = '.html'

if not os.path.exists(directory):
    os.makedirs(directory)

for n in range(1, num+1):

    outp = directory + str(n) + ext

    url = base + str(n)
    r = urllib2.urlopen(url)
    with open(outp, 'w') as f:
        f.write(r.read())
    print '%s to %s' % (n, outp)
