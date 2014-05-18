#!/usr/bin/python
#-*- coding: utf-8 -*-

from collections import OrderedDict
import json
import os
import re
import sys
from time import sleep
import urllib2
from urlparse import urljoin

from scrapy.selector import Selector

# settings
PAGE_ENC = 'utf-8'
HEADERS = ['name_kr','name_cn','name_en','birth','party','district','committee','when_elected','off_phone','homepage','email','aides','pr_secrs','sc_secrs','hobby','experience','photo','url']
DATADIR = '.'
DEBUG = False

# global dicts
urls = {}
ppl_urls = []
ppl_data = []

def load_urls():
    for line in open('urls', 'r'):
        if line[0] == '#':
            continue
        key, url = line.split()
        urls[key] = url

def get_page(url, htmldir):
    try:
        page_in_txt = urllib2.urlopen(url).read()
    except urllib2.URLError:
        print 'Connection time out. Retrying in 10 seconds... %s' % url
        sleep(10)
        get_page(url, htmldir)

    idx = url.find('memCode=')
    if idx != -1:
        filename = '%s/%s.html' % (htmldir, url[idx + len('memCode='):])
    else:
        filename = '%s/index.html' % htmldir

    with open(filename, 'w') as f:
        f.write(page_in_txt)
    return page_in_txt.decode(PAGE_ENC)

def get_xpath_data(data, _xpath, getall=False):
    xpath_selector_list = []

    hxs = Selector(text=data)
    for i in hxs.xpath(_xpath):
        xpath_selector_list.append(i.extract().encode("utf-8"))
    if getall:
        return [x.decode(PAGE_ENC) for x in xpath_selector_list]
    else:
        return xpath_selector_list[0].decode(PAGE_ENC)

def get_ppl_urls(htmldir):
    def unescape_html(doc):
        escape_table = {'&lt;': '<', '&gt;': '>', '&amp;': '&'}
        for old, new in escape_table.items():
            doc = doc.replace(old, new)
        return doc

    page = get_page(urls['people_list'], htmldir)

    full_member_list = []
    member_lists = get_xpath_data(page, ".//*/dd[@class='img']", getall=True)
    for member_list in member_lists:
        full_member_list.append(re.split('\(|\)', member_list)[1])

    for url in full_member_list:
        url = unescape_html(url)
        ppl_urls.append(urls['person']+ url)

def extract_profile(page):
    def parse_name_and_birth(name_and_birth):
        name_kr = get_xpath_data(profile, ".//*/h4/text()")
        name_cn, name_en, birth =\
                get_xpath_data(profile, ".//*/li[not(@class='photo')]/text()",\
                getall=True)
        name_cn = re.sub('[()\s]', '', name_cn)
        birth = birth.replace('.','-')
        return [name_kr, name_cn, name_en, birth]

    def get_detail(data):
        try:
            d = get_xpath_data(data, ".//text()")
        except IndexError:
            d = ''
        return re.sub('\s+', ' ', d).strip()

    # get name & birth
    profile = get_xpath_data(page, ".//*/div[@class='profile']")
    name_and_birth = parse_name_and_birth(page)

    # get experience
    experience = get_xpath_data(page, ".//*/dl[@class='per_history']/dd/text()",\
            getall=True)
    experience = '||'.join(e.strip() for e in experience)

    # get photo
    photo = urls['base']\
            + get_xpath_data(profile, ".//*/ul/li[@class='photo']/img/@src")

    # get others
    others_list = get_xpath_data(page, ".//*/dl[@class='pro_detail']/dd",\
            getall=True)
    others = [get_detail(o) for o in others_list]

    full_profile = list(name_and_birth + others)
    full_profile.append(experience)
    full_profile.append(photo)

    return [p.replace('"',"'") for p in full_profile]

def crawl_ppl_data(htmldir, debug=DEBUG):
    npeople = 15 if debug else len(ppl_urls)
    for i, url in enumerate(ppl_urls[:npeople]):
        page = get_page(url, htmldir)
        profile = extract_profile(page)
        ppl_data.append(profile + [url])
        if debug:
            print i, ppl_data[i][0]

def sort_ppl_data(ppl_data):
    ppl_data = sorted(ppl_data, key=lambda x: x[3])
    ppl_data = sorted(ppl_data, key=lambda x: x[0])

def write_csv():
    with open('assembly.csv', 'w') as f:
        f.write('%s\n' % ','.join(HEADERS))
        f.write('\n'.join(\
            '"%s"' % '","'.join(row) for row in ppl_data).encode('utf-8'))
    print 'Data succesfully written to csv'

def write_json():
    with open('assembly.json', 'w') as f:
        ppl_list =[]
        for person_data in ppl_data:
            person_dict = {}
            for key, value in zip(HEADERS, person_data):
                person_dict[key] = value
            ppl_list.append(person_dict)

        # order ppl_data by HEADERS
        ordered_json_list = [OrderedDict(sorted(item.iteritems(),
            key=lambda (k, v): HEADERS.index(k)))for item in ppl_list]

        f.write(json.dumps(ordered_json_list, indent=4))
    print 'Data succesfully written to json'

def main(argv, datadir=DATADIR):
    htmldir = '%s/html' % datadir
    if not os.path.exists(htmldir):
        os.makedirs(htmldir)

    load_urls()
    get_ppl_urls(htmldir)
    crawl_ppl_data(htmldir)
    sort_ppl_data(ppl_data)
    write_csv()
    write_json()

if __name__ == '__main__':
    main(sys.argv[1:])
