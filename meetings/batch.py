#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import re
import requests
import urllib

import get


baseurl = 'http://likms.assembly.go.kr/record'


def get_docs():
    docurl_base = '%s/new/getFileDown.jsp?CONFER_NUM=' % baseurl


def get_listurl(assembly_id):
    if assembly_id==5.5:
        return '%s/content/con_search167.jsp?div=1&DAE_NUM=66&COMM_CODE=ZA'\
                '&i=1' % baseurl
    elif assembly_id==10.5:
        return '%s/content/con_search7.jsp?div=1&DAE_NUM=77&COMM_CODE=ZA'\
                '&i=1' % baseurl
    else:
        return 'http://likms.assembly.go.kr/record/content/con_search2.jsp'\
                                         '?div=1&DAE_NUM=%s' % assembly_id

def get_sessionurl_base(assembly_id):
    if assembly_id==5.5:
        n = 767
    elif assembly_id==10.5:
        n = 8
    else:
        n = 3
    return '%s/content/con_search%d.jsp' % (baseurl, n)


def get_docids(listurl, sessionurl_base):
    def encode_session_params(k, v):
        if assembly_id==5.5:
            params['COMM_NAME'] = v
            params['COMM_CODE'] = 'ZA'
            params['CONF_DATE'] = v.strip(u'년')
        elif assembly_id==10.5:
            params['CONF_DATE'] = v
        else:
            params['SES_NUM'] = v
            params['SES_BIGO'] = 'null'
        return urllib.urlencode({p:v.encode('euc-kr') for p, v in params.items()})

    def get_sitting_info(anchor):
        print anchor
        items = anchor[0].split("'")
        return {'sitting_name': items[1].strip(), 'docid': items[3]}

    def get_anchors(sessionurl):
        root = get.webpage(get.htmltree(sessionurl))
        return filter(None, [i.xpath('./@href') for i in root.xpath('.//a')])

    root = get.webpage(get.htmltree(listurl))
    params = {i.xpath('./@name')[0]: i.xpath('./@value')[0]\
                    for i in root.xpath('.//input')}

    docids = []
    for k, v in params.items():
        if re.match(ur'(SES_NUM|CONF_DATE|COMM_NAME)[0-9]+', k):
            print k, v
            sessionurl = '%s?%s' % (sessionurl_base, encode_session_params(k, v))

            anchors = get_anchors(sessionurl)
            sittings = [get_sitting_info(a) for a in anchors\
                            if re.match(r'javascript:mainsearch[0-9]+', a[0])]
            docids.append({ 'session_name': v, 'sittings': sittings })
    return docids


#FIXME: broken for 1-19th assembly
for assembly_id in [5.5, 10.5]:
    print assembly_id
    listurl = get_listurl(assembly_id)

    sessionurl_base = get_sessionurl_base(assembly_id)
    docids = get_docids(listurl, sessionurl_base)
    with open('meetingdoc_ids_%.1f.json' % assembly_id, 'w') as f:
        json.dump(docids, f)
