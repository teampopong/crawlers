#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re

import utils

LIST_PAGE = 'list.html'
LIST_URL = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml?electionId=0020120411&requestURI=%2Felectioninfo%2F0020120411%2Fep%2Fepei01.jsp&topMenuId=EP&secondMenuId=EPEI01&menuId=&statementId=EPEI01_%232&electionCode=2&cityCode=0&proportionalRepresentationCode=0&x=17&y=11'
PLEDGE_BASEURL = 'http://party.nec.go.kr/people/popup/publicpledgepolicy/read.xhtml?candidateNo='
PLEDGE_DIR = 'html'
X = {
    'table'  : '//table[@id="table01"]//tr',
    'links'  : '//table[@id="table01"]//a/@href',
    'pledges': '//table[@id="table01"]//td[@align="left"]',
    'contents': '//table[@id="table01"]//div[@class="PledgeRepleEx"]/span'
}


def get_people(url, page):
    utils.get_webpage(url, page)

def find_people(filename, x_table, x_links):
    page = utils.read_webpage(filename)
    table = page.xpath(x_table)
    names = [list(row.itertext())[9].strip() for row in table]
    parties = [list(row.itertext())[5] for row in table]
    ids = [re.search(r'[0-9]+', s).group(0) for s in page.xpath(x_links)]
    return names, parties, ids

def write_people(names, parties, ids):
    people = zip(['name']+names[1:], ['party']+parties[1:], ['ids']+ids )
    with open(LIST_PAGE.replace('.html', '.csv'), 'w') as f:
        for p in people:
            f.write(','.join(p).encode('utf-8'))
            f.write('\n')

def get_pledges(basepath, baseurl, ids):
    if not os.path.exists(basepath):
        os.makedirs(basepath)

    tot = len(ids)
    for i, n in enumerate(ids):
        fn = '%s/%s.html' % (basepath, n)
        utils.get_webpage(baseurl + n, fn)
        #utils.get_webpage(baseurl + n, fn, decoding='euc-kr')
        print 'File written to %s (%s/%s)' % (fn, i, tot)

def find_pledges(filename, x_pledge, x_content):
    page = utils.read_webpage(filename)
    pledges = [list(row.itertext()) for row in page.xpath(x_pledge)]
    contents = [list(row.itertext()) for row in page.xpath(x_content)]
    return pledges, contents

if __name__=='__main__':
    get_people(LIST_URL, LIST_PAGE)
    names, parties, ids = find_people(LIST_PAGE, X['table'], X['links'])
    write_people(names, parties, ids)

    get_pledges(PLEDGE_DIR, PLEDGE_BASEURL, ids)

    # FIXME: Encoding problem
    filename = 'html/404154183.html'
    pledges, contents = find_pledges(filename, X['pledges'], X['contents'])
    print pledges, contents
    print len(pledges), len(contents)
