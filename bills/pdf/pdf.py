#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import urllib

from settings import DIR
import utils

def download(assembly_id, json, indir, outdir):
    try:
        url = utils.read_json('%s/%s' % (indir, json))\
            ['status_dict']['접수']['의안접수정보'][0]['문서'][0][1][1]
    except KeyError as e:
        try:
            url = utils.read_json('%s/%s' % (indir, json))\
                ['status_dict']['접수']['의안접수정보'][0]['의안원문'][0][1][1]
        except KeyError as e:
            print json
            print utils.read_json('%s/%s' % (indir, json))\
                ['status_dict']['접수']['의안접수정보'][0]
            url = None

    path = '%s/%s' % (outdir, json.replace('.json', '.pdf'))
    if not os.path.isfile(path) and url:
        urllib.urlretrieve(url, path)
        print 'Downloaded %s' % path

def get_pdf(assembly_id, range=(None, None), bill_ids=None):
    if bill_ids is not None and not bill_ids:
        return

    indir = '%s/%s' % (DIR['data'], assembly_id)
    outdir = '%s/%s' % (DIR['pdf'], assembly_id)
    utils.check_dir(outdir)

    failed = []
    jsons = os.listdir(indir)[range[0]:range[1]]

    for json in jsons:
        if bill_ids and json.split('.', 1)[0] not in bill_ids:
            continue

        try:
            download(assembly_id, json, indir, outdir)
        except (IndexError, TypeError) as e:
            print 'Failed downloading %s with %s' % (json, e)
            failed.append((json, e))
    print 'Failed files: ', failed
