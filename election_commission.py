#!/usr/bin/python2.7
# -*- encoding=utf-8 -*-

import html5lib
from lxml import etree
import urllib2
from urlparse import urljoin
import json
import re

Settings = {
    'USER_AGENT': "Mozilla/5.0 (X11; U; Linux x86_64; fr; rv:1.9.1.5) "
            "Gecko/20091109 Ubuntu/9.10 (karmic) Firefox/3.5.5",
}

url_city_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_cityCodeBySgJson.json?electionId=0020120411&electionCode=2'
url_sgg_codes_json = 'http://info.nec.go.kr/bizcommon/selectbox/selectbox_getSggCityCodeJson.json?electionId=0020120411&electionCode=2&cityCode=%s'
url_cand_list_base = 'http://info.nec.go.kr/electioninfo/electionInfo_report.xhtml?electionId=0020120411&requestURI=%2Felectioninfo%2F0020120411%2Fpc%2Fpcri03_ex.jsp&topMenuId=PC&secondMenuId=PCRI03&menuId=&statementId=PCRI03_%232&electionCode=2'
url_image_base = 'http://info.nec.go.kr'

def get_json(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent", Settings['USER_AGENT'])
    f = urllib2.urlopen(request)
    txt = f.read()
    return json.loads(txt, encoding='UTF-8')

def get_xpath(url, xpath):
    htmlparser = html5lib.HTMLParser(\
            tree=html5lib.treebuilders.getTreeBuilder("lxml"),\
            namespaceHTMLElements=False)

    request = urllib2.Request(url)
    request.add_header("User-Agent", Settings['USER_AGENT'])
    f=urllib2.urlopen(request)

    page = htmlparser.parse(f)
    return page.xpath(xpath)

def city_codes():
    list_ = get_json(url_city_codes_json)['body']
    return map(lambda x: x['CODE'], list_)

def sgg_codes(city_code):
    list_ = get_json(url_sgg_codes_json % (city_code, ))['body']
    return map(lambda x: x['CODE'], list_)

attrs = ['district', 'party', 'image', 'name', 'sex', 'birth',
        'address', 'job', 'education', 'experience', 'regdate']

def stringify(node):
    parts = ([node.text] +
            [stringify(c) for c in node.getchildren()] +
            [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))

regex_split = re.compile('[/\(\)\s]')

def parse_member(member):
    for attr in attrs:
        if attr == 'image':
            rel_path = member['image'].find('./img').attrib['src']
            member['image'] = urljoin(url_image_base, rel_path)
            continue

        member[attr] = stringify(member[attr]).strip()

    member['name_kr'], member['name_cn'] = re.split(regex_split, member['name'])[:2]
    del member['name']

    member['birthyear'], member['birthmonth'], member['birthday'] =\
            re.split(regex_split, member['birth'])[:3]
    del member['birth']

    print member['district'], member['name_kr']

    return member

def parse_cand_page(url):
    import sys
    elems = get_xpath(url, '//td')
    members = (dict(zip(attrs, elems[i*11:(i+1)*11]))\
                for i in xrange(len(elems) / 11))

    members = [parse_member(member) for member in members]
    return members

def main():
    params = ({ 'city_code': city_code,\
                'sgg_code': sgg_code\
                }\
                for city_code in city_codes()\
                for sgg_code in sgg_codes(city_code))

    cand_list = []
    for param in params:
        url_options = '&cityCode=%(city_code)s&sggCityCode=%(sgg_code)s' % param
        req_url = url_cand_list_base + url_options
        dist_cand_list = parse_cand_page(req_url)
        cand_list.extend(dist_cand_list)

    with open('cand-0411.json', 'w') as f:
        json.dump(cand_list, f)

if __name__ == '__main__':
    main()
