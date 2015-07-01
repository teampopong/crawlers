#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import os
import re
import urllib

from lxml import html
import requests


basedir = './data'   # change me
jsondir = '%s/meetings/national/meta' % basedir
pdfdir = '%s/meeting-docs/national' % basedir
baseurl = 'http://likms.assembly.go.kr/record'

getnum = lambda s: re.search(r'\d+', s).group(0)
joinall = lambda l: ' '.join(i.strip() for i in l).strip()


def checkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_filename(data, filetype):
    if filetype=='json':
        directory = jsondir
    elif filetype=='pdf':
        directory = pdfdir
    a, s, m = data['assembly_id'], data['session_id'], data['meeting_id']
    c, d = data['committee'], data['date']
    checkdir('%s/%s/%s' % (directory, a, d))
    filename = '%s/%s/%s/%s-%s-%s-%s.%s'\
            % (directory, a, d, a, s, m, c, filetype)
    return filename


def try_except(success, failure=lambda: ''):
    try:
        return success()
    except IndexError:
        return failure()


def parse_summary(response):
    root = html.document_fromstring(response.text)
    issues = [{
            'link_id': try_except(lambda: i.xpath('.//a/@onclick')[0].split("'")[1]),
            'title': joinall(i.xpath('.//text()')),
        } for i in root.xpath('//div[@class="popup_box"]/ul/li')]

    participants = [{
            'link_id': try_except(lambda: i.xpath('./a/@onclick')[0].split("'")[1]),
            'party': i.xpath('.//span/strong/text()')[0],
            'name': i.xpath('.//span/text()')[0],
        } for i in root.xpath('//div[@class="popup_box02"]/ul/li')]
    return issues, participants


def parse_row(row):

    def to_url(string):
        fname, params = re.search('javascript:(\w+)\((.+)\)', string).groups()
        params = [p.strip("'") for p in params.split(',')]

        if fname=='fn_fileDown':
            # params: [conferNum, fileId, imsiYn]
            # r = requests.post('%s/mhs-10-040-0040.do' % baseurl, data={'conferNum': params[0], 'fileId': params[1]})
            return '%s/new/getFileDown.jsp?CONFER_NUM=%s' % (baseurl, params[0])

        elif fname=='fn_popup_vod':
            # params: [vodCommCode, daeNum, sesNum, degreeNum]
            params[-1] = int(params[-1])
            return 'http://w3.assembly.go.kr/jsp/vod/vod.do?'\
                   'cmd=vod&mc=%s&ct1=%s&ct2=%s&ct3=%02d' % tuple(params)

        elif fname=='fn_summPopup':
            # params: [conferNum]
            r = requests.post('%s/mhs-10-030.do' % baseurl, data={'conferNum': params[0]})
            return parse_summary(r)

        else:
            print 'Unknown function %s' % fname


    def parse_links(item):
        anchors = item.xpath('.//a')
        return { a.xpath('./img/@alt')[0]: to_url(a.xpath('./@onclick')[0]) for a in anchors }

    def parse_items(items):
        links = parse_links(items[6])
        issue_links, participants = links.get(u'요약정보보기')
        return {
            'assembly_id': getnum(items[1].xpath('.//a/text()')[0]),            # 대
            'session_id': getnum(items[2].xpath('.//a/text()')[0]),             # 회기
            'meeting_id': getnum(items[3].xpath('.//a/text()')[0]),             # 차
            'committee': joinall(items[4].xpath('.//a/text()')),                # 회의구분
            'date': items[5].xpath('.//a/text()')[0].strip().replace('.', '-'), # 회의일
            'pdf': links.get(u'pdf회의록다운'),                                 # 회의록
            'vod': links.get(u'영상회의록보기'),
            'participants': participants,
            'issue_links': issue_links,
            'issues': [i['title'] for i in issues],  # TODO: deprecate me
            'issues_url': '',                        # TODO: deprecate me
        }

    items = row.xpath('.//td')
    return parse_items(items)


def save_json(data):
    filename = get_filename(data, 'json')
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def save_pdf(data):
    filename = get_filename(data, 'pdf')
    urllib.urlretrieve(data['pdf'], filename)


if __name__=='__main__':
    NITEMS = 100 # number of items to retrieve

    r = requests.post('%s/mhs-30-011.do' % baseurl, data={'countPage': NITEMS, 'pageNo': 1})
    root = html.document_fromstring(r.text)
    rows = root.xpath('//tbody[@id="ajaxResult"]//tr')

    for row in rows:
        data = parse_row(row)
        save_json(data)
        save_pdf(data)
