#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import json
import os
import re
import requests
import urllib

import get


baseurl = 'http://likms.assembly.go.kr/record'
datadir = '/home/e9t/data/popong/meeting-docs/national'
divname = {1: u'본회의', 2: u'상임위원회'}


def chkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_listurl(assembly_id, divid):
    if divid==1: # 본회의, DAE_NUM = {1-19, 66, 77}
        if assembly_id==5.5:
            return '%s/content/con_search167.jsp?div=%s&DAE_NUM=66&COMM_CODE=ZA'\
                    '&i=1' % (baseurl, divid)
        elif assembly_id==10.5:
            return '%s/content/con_search7.jsp?div=%s&DAE_NUM=77&COMM_CODE=ZA'\
                    '&i=1' % (baseurl, divid)
        else:
            return '%s/content/con_search2.jsp?div=%s&DAE_NUM=%s'\
                                             % (baseurl, divid, assembly_id)
    elif divid==2: # 상임위원회, DAE_NUM = {3-19, 66, 77}
        '%s/content/con_search1.jsp?div=2&DAE_NUM=77'
    else:
        raise('No divid')

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
            sessionurl = '%s?%s' % (sessionurl_base, encode_session_params(k, v))

            anchors = get_anchors(sessionurl)
            sittings = [get_sitting_info(a) for a in anchors\
                            if re.match(r'javascript:mainsearch5', a[0])]
            docids.append({ 'session_name': v, 'sittings': sittings })
    return docids


def get_docs(attrs):
    docurl_base = '%s/new/getFileDown.jsp?CONFER_NUM=' % baseurl
    filedir = u'%s/%s/%s'\
            % (datadir, attrs.get('assembly_id'), attrs.get('date'))
    chkdir(filedir)
    filename = u'%s-%s-%s-%s.pdf'\
            % (attrs.get('assembly_id'), attrs.get('session_id'),\
            # TODO: 상임위별로 divname 이름 다르게
            attrs.get('sitting_id'), divname[divid])
    print filename
    urllib.urlretrieve('%s%s' % (docurl_base, attrs.get('docid')),\
            '%s/%s' % (filedir, filename))


if __name__=='__main__':
    #FIXME: duplicate entries for 10.5th assembly 본회의

    divid = 1
    assembly_id = 19

    listurl = get_listurl(assembly_id, divid)
    sessionurl_base = get_sessionurl_base(assembly_id)
    docids = get_docids(listurl, sessionurl_base)
    idfile = 'meetingdoc_ids_%.1f.json' % assembly_id
    with open(idfile, 'w') as f:
        json.dump(docids, f)

    sessions = docids
    for session in sessions:
        session_id = session.get('session_name').split(u'회')[0]
        for sitting in session.get('sittings'):
            docid = sitting.get('docid')
            tmp = re.match(r'(.*?)\((.*?)\)', sitting.get('sitting_name'))
            sitting_id = tmp.group(1).replace(u'제', '').replace(u'차', '').strip()
            date = re.sub(ur'(년|월|일)', '-', tmp.group(2)).strip('\s-')

            attrs = { 'assembly_id': assembly_id, 'session_id': session_id,\
                      'date': date, 'sitting_id': sitting_id, 'docid': docid }
            get_docs(attrs)
            print attrs
