#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import html5lib
import json
import urllib2

baseurl = 'http://www.nec.go.kr/portal/bbs/list/B000037%d.do'\
        '?menuNo=%d&pageIndex=%d'
candtypes = {
    0: 'province_governor',
    1: 'education_governor',
    2: 'municipal_governor',
    3: 'province_member',
    4: 'municipal_member'
    }

def get_url(candtype, pageno):
    url = baseurl % (candtype + 2, candtype + 200576, pageno + 1)
    return url

def get_htmltree(url):
    r = urllib2.Request(url)
    r.add_header("User-Agent", "Mozilla/5.0")
    f = urllib2.urlopen(r)
    return f

def get_webpage(f):
    parser = html5lib.HTMLParser(\
        tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
        namespaceHTMLElements=False)
    root = parser.parse(f)
    return root

def get_link_type(link):
    url = link.xpath('./img/@src')[0]
    if url==u'/images/contents/btn_t_01.gif':
        linktype = 'homepage'
    elif url==u'/images/contents/btn_t_02.gif':
        linktype = 'twitter'
    elif url==u'/images/contents/btn_t_03.gif':
        linktype = 'facebook'
    else:
        linktype = 'unknown'
    return linktype

def get_links(candtype):
    pageno = 0
    cont = True
    people = []
    while cont:
        url = get_url(candtype, pageno)
        f = get_htmltree(url)
        root = get_webpage(f)
        elems = root.xpath('//form[@id="frm"]/div[@class="candidate_info2 btn"]')
        morepeople = [parse(elem) for elem in elems]
        if morepeople:
            people.extend(morepeople)
            pageno += 1
        else:
            cont = False
    return people

def parse(elem):
    person = {}
    person['name'] = elem.xpath('.//dt/span/a/text()')[0]
    person['district'] = elem.xpath('.//dd[@class="txt"]/text()')[0]
    links = elem.xpath('.//dd[@class="pr"]/a')
    person['links'] =\
            {get_link_type(link): link.xpath('./@href')[0] for link in links}
    return person

if __name__=='__main__':
    for candtype in range(5):
        people = get_links(candtype)
        ct = candtypes[candtype]
        with open('links_%s.json' % ct, 'w') as f:
            json.dump(people, f)
        print ct
