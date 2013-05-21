#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import urllib

from settings import DIR
import utils

def get_pdf(assembly_id, start=1, end=10):
    indir = '%s/%s' % (DIR['data'], assembly_id)
    outdir = '%s/%s' % (DIR['pdf'], assembly_id)
    utils.check_dir(outdir)

    for json in os.listdir(indir)[start:end]:
        urls = utils.read_json('%s/%s' % (indir, json))\
                ['status_dict']['접수']['의안접수정보'][0]['문서'][0][1]

        for url in urls:
            if url.endswith('type=0'):
                fname = json.replace('.json', '.hwp')
            else:
                fname = json.replace('.json', '.pdf')
            path = '%s/%s' % (outdir, fname)
            urllib.urlretrieve(url, path)
            print 'Downloaded %s' % path
