#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import urllib2

'''
원본 사이트는 [여기](http://likms.assembly.go.kr/bill/WebContents/Summary2.htm)인데
내용이 iframe 안에 있어서 실질적인 base url은 아래와 같음
'''

base = 'http://likms.assembly.go.kr/bill/WebContents/content'
ext = '.htm'
num = 4

for n in range(1, num+1):

    outp = str(n) + ext
    if n==1: n=''

    url = base + str(n) + ext
    r = urllib2.urlopen(url)
    with open(outp, 'w') as f:
        f.write(r.read())
