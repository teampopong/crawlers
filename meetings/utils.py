#! /usr/bin/python2.7
# -*- coding: utf-8 -*-


from datetime import datetime
import os
import re
import urllib


def convid(assembly_id):
    if assembly_id==5.5: assembly_id = 66
    if assembly_id==10.5: assembly_id = 77
    return assembly_id

def chkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def curterm(date=None):
    """
    Term of the National Assembly (or assembly id) for a given date.
    If date is not explicitly given, returns the term of the current date.
    """

    if not date: date = today()
    if not isinstance(date, datetime):
        raise Exception('Invalid datatype for date')

    if (date.year - 2000)%4==0 and date.month < 6:
        term = (date.year - 2000)/4 + 15
    else:
        term = (date.year - 2000)/4 + 16
    return term

def download_doc(doc_id, filepath='./tmp.pdf'):
    if os.path.exists(filepath):
        print 'Exists %s' % filepath
        return

    filedir, filename = filepath.rsplit('/', 1)
    chkdir(filedir)

    url = 'http://likms.assembly.go.kr/record/new/getFileDown.jsp?CONFER_NUM=%s'\
            % doc_id
    print url
    urllib.urlretrieve(url, filepath)
    print 'Downloaded %s' % filepath

def get_js_functions(root, f):
    def parse_js_function_contents(f):
        stripped = [re.search(r'document\.(.+?)\.value', t).group(1)\
                    for t in f[1].split(';') if '=' in t]
        target = stripped[0].split('.')[0]
        attrs = [t.split('.')[1] for t in stripped]
        return {'function': f[0], 'target': target, 'attrs': attrs}

    js_snippet = root.xpath('.//script')[0].xpath('./text()')[0]
    js_snippet = re.sub(r'\s+', ' ', str(js_snippet))

    re_functions = r'function\s*(.+?)\(.+?\)\s*\{(.*?)\}'
    function_matches = re.findall(re_functions, js_snippet)
    return [parse_js_function_contents(f) for f in function_matches]

def match_name_codes(js_calls, filter='mainsearch', type='committees'):
    n = {}
    if type=='committees':
        js_calls = [c for c in js_calls if c[0]==filter]
        for i, call in enumerate(js_calls):
            n['COMM_NAME%s' % i] = call[1][0]
            n['COMM_CODE%s' % i] = call[1][1]
    if type=='sessions':
        js_calls = [c for c in js_calls if c[0]==filter]
        for i, call in enumerate(js_calls):
            n['SES_NUM%s' % i] = call[1][2]
    return n

def parse_js_call(s):
    function, attrs = re.match(r'javascript:(.+?)\((.*)\)', s).groups()
    attrs = [a.strip("'") for a in attrs.split(',')]
    return function, attrs

def today():
    return datetime.today()

def urlencode(d, encoding='euc-kr'):
    return urllib.urlencode({p:v.encode(encoding) for p, v in d.items()})
