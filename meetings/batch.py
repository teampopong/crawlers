#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import re
import requests
import urllib

import get
from utils import chkdir, convid, curterm, download_doc, match_name_codes,\
                  parse_js_call, urlencode


# change me
DATADIR = './data'

# don't change me
BASEURL = 'http://likms.assembly.go.kr/record'
ASSEMBLY_IDS = [5.5, 10.5] + range(1, curterm() + 1)
DIV_IDS = {1: u'본회의',
           2: u'상임위원회', 3: u'특별위원회', 4: u'예산결산특별위원회',
           5: u'국정감사', 6: u'국정조사', 7: u'전원위원회', 8: u'소위원회'}
DIV_LIST_SEARCH_NUM = {
    # div_id: {assembly_id: search_num}
    # http://likms.assembly.go.kr/record/content/con_index%s.jsp?div=%s
    # % (search_num, div_id)
    1: {'default': '2', 5.5: '167', 10.5: '7'}, # 1-19, 5.5, 10.5
    2: {'default': '1', 5.5: '166'}, # 3-19, 5.5, 10.5
    3: {'default': '1', 5.5: '166'}, # 3-19, 5.5, 10.5
    4: {'default': '2'}, # 5-19
    5: {'default': '1'}, # 3-19
    6: {'default': '1'}, # 4, 14-19
    7: {'default': '1'}, # 16, 17
    8: {'default': '_sub0'}, # 16-19
}


def get_list_url(assembly_id, div_id):
    dnum = DIV_LIST_SEARCH_NUM[div_id].get(assembly_id,\
           DIV_LIST_SEARCH_NUM[div_id].get('default'))
    return '%s/content/con_search%s.jsp?div=%s&DAE_NUM=%s'\
            % (BASEURL, dnum, div_id, convid(assembly_id))


def get_session_urls(assembly_id, div_id, listurl):
    def searchform(root, num=''):
        return root.xpath('.//form[@name="searchform%s"]/@action' % num)[0]

    root = get.webpage(get.htmltree(listurl))
    js_calls = [parse_js_call(j) for j in root.xpath('.//a/@href')]

    params = match_name_codes(js_calls, filter='mainsearch', type='committees')
    nsessions = len(params)/2
    params['i'] = str(nsessions)
    params['div'] = str(div_id)
    params['DAE_NUM'] = str(assembly_id)

    urls = []
    for i in range(nsessions):
        params['COMM_NAME'] = params['COMM_NAME%s' % i]
        params['COMM_CODE'] = params['COMM_CODE%s' % i]
        urls.append(\
            {'committee': params['COMM_NAME'],
             'url': '%s/content/%s?%s' %\
                    (BASEURL, searchform(root)[:-2], urlencode(params))})
    return urls


def add_session_info(assembly_id, div_id, sessions):
    def get_sitting_urls(assembly_id, div_id, sessionurl):
        root = get.webpage(get.htmltree(sessionurl))
        js_calls = [parse_js_call(j) for j in root.xpath('.//a/@href')]

        params = match_name_codes(js_calls, filter='mainsearch2', type='sessions')
        nsittings = len(params)
        params['j'] = str(nsittings)

        urls = []
        for i in range(nsittings):
            params['SES_NUM'] = params['SES_NUM%s' % i]
            url = '%s&%s' % (sessionurl, urlencode(params))
            # TODO: generalize me
            url = url.replace('con_search2', 'con_search3')
            urls.append({'session_name': params['SES_NUM'], 'url': url})
        return urls

    def get_doc_ids(assembly_id, div_id, sittingurl):
        root = get.webpage(get.htmltree(sittingurl))
        js_calls = [parse_js_call(j) for j in root.xpath('.//a/@href')]
        return [{'sitting_name': c[1][0], 'docid': c[1][1]}\
                    for c in js_calls if c[0]=='mainsearch4']

    def get_session_info():
        session_info = get_sitting_urls(assembly_id, div_id, session['url'])
        for sitting in session_info:
            sitting['sittings'] = get_doc_ids(assembly_id, div_id, sitting['url'])
            del sitting['url']
        return session_info

    for session in sessions:
        print session['committee']
        session['sessions'] = get_session_info()

    fn = 'meetingdoc_ids_%s_%s.json' % (DIV_IDS[div_id], assembly_id)
    with open(fn, 'w') as f:
        json.dump(sessions, f, indent=2)

    return sessions


def get_docs(assembly_id, div_id, sessions, committee_name):
    def get_docs_for_date(attrs):
        filename = u'%s-%s-%s-%s.pdf'\
                % (attrs.get('assembly_id'), attrs.get('session_id'),\
                attrs.get('sitting_id'), committee_name)
        filedir = u'%s/%s/%s'\
                % (DATADIR, attrs.get('assembly_id'), attrs.get('date'))
        filepath = u'%s/%s' % (filedir, filename)
        download_doc(attrs.get('doc_id'), filepath)

    for session in sessions:
        session_id = session.get('session_name').split(u'회')[0]
        for sitting in session.get('sittings'):
            tmp = re.match(r'(.*?)\((.*?)\)', sitting.get('sitting_name'))
            sitting_id = tmp.group(1).replace(u'제', '').replace(u'차', '').strip()
            date = re.sub(ur'(년|월|일)', '-', tmp.group(2)).strip('\s-')
            attrs = { 'assembly_id': assembly_id,\
                      'session_id': session_id,\
                      'sitting_id': sitting_id,\
                      'date': date,\
                      'doc_id': sitting.get('docid')}

            get_docs_for_date(attrs)


def main(assembly_id, div_id):

    listurl = get_list_url(assembly_id, div_id)
    sessions = get_session_urls(assembly_id, div_id, listurl)
    sessions = add_session_info(assembly_id, div_id, sessions)

    #with open('meetingdoc_ids_상임위원회_%s.json' % assembly_id, 'r') as f:
    #    sessions = json.load(f)

    for session in sessions:
        print session['committee']
        get_docs(assembly_id, div_id, session['sessions'], session['committee'])

if __name__=='__main__':
    #for assembly_id in ASSEMBLY_IDS:
    #for div_id in DIV_IDS:
    assembly_id = 19
    div_id = 2
    main(assembly_id, div_id)
