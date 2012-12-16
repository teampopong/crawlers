#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re, urllib2 
import get

settings = {
                "base_url": "http://www.google.com/search?hl=en&q=",
                "xpath":'//body//div[@id="resultStats"]'
           }

def as_list(querylist=['박근혜','안철수','문재인']):
    l = []
    for q in querylist:
        l.append(google(q))
    return l

def as_matrix(querylist=['박근혜','안철수','문재인']):
    print 'retrieving document numbers from google...'
    l = len(querylist)
    m = [[0]*l for x in range(l)]

    for i in range(l):
        for j in range(i, l):
            if i==j:
                q = querylist[i] 
            else:
                q = ' '.join([querylist[i], querylist[j]])
            m[i][j] = google(q)
    return m

def google(query):
    url = settings['base_url'] + urllib2.quote(query.encode('utf-8'))
    f = get.htmltree(url)
    p = get.webpage(f)
    x = get.text(p, settings['xpath'])[0]
    n = re.findall(r'[0-9]+', x)
    return int(''.join(n))

if __name__ == '__main__':
    QUERYLIST   = ['박은정','강철','윤주희']
    print(as_matrix(QUERYLIST))
