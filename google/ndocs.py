#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import re, sys, csv, time, codecs, urllib2
import get

settings = {
                "base_url": "http://www.google.com/search?hl=en&q=",
                "xpath":'//body//div[@id="resultStats"]'
           }

def as_matrix(querylist):
    l = len(querylist)
    m = [[0]*l for x in range(l)]

    for i in range(l):
        for j in range(i, l):
            if i==j:
                q = querylist[i]
                run = '\t(%d)\t: %s' % (i,querylist[i])
            else:
                q = ' '.join([querylist[i], querylist[j]])
                run = '\t(%d,%d)\t: %s,%s' % (i, j, querylist[i], querylist[j])
            sys.stdout.write(run)

            try:
                m[i][j] = google(q)
                stat = 1
            except:
                stat = 0
                pass
            print (' - ' + str(stat))
    return m

def as_list(querylist):
    l = []
    for q in querylist:
        l.append(google(q))
    return l

def google(query):
    url = settings['base_url'] + urllib2.quote(query.encode('utf-8'))
    f = get.htmltree(url)
    p = get.webpage(f)
    x = get.text(p, settings['xpath'])[0]
    n = re.findall(r'[0-9]+', x)
    return int(''.join(n))

def write_csv(attrs, m):
    filename = './ndocs-%s.csv' % (time.strftime('%Y%m%d%H%M'))
    attrs = [a.encode('utf-8') for a in attrs]
    with open(filename, 'wb') as f:
        #f.write(codecs.BOM_UTF8)
        w = csv.writer(f)
        w.writerow(attrs)
        for i in m:
            w.writerow(i)

if __name__ == '__main__':
    QUERYLIST   = ['박근혜','문재인','이정희']
    print 'retrieving document numbers from google...'
    m = as_matrix(QUERYLIST)
    print 'write to file...'
    write_csv(QUERYLIST, m)
    print 'done'
