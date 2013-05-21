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
        url = utils.read_json('%s/%s' % (indir, json))\
                ['status_dict']['접수']['의안접수정보'][0]['문서'][0][1][1]
        path = '%s/%s' % (outdir, json.replace('.json', '.pdf'))

        if not os.path.isfile(path):
            urllib.urlretrieve(url, path)
            print 'Downloaded %s' % path
