#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import meta
import specific
import pdf

assembly_s, assembly_e = 17, 17
bill_s, bill_e = 101, 120

for a in range(assembly_s, assembly_e+1):
    print '\n# Assembly %d' % a

    print '## Get meta data'
    npage = meta.get_npages(a)
    meta.get_html(a, npages)
    meta.html2csv(a, npages)

    print '## Get specific data'
    specific.get_html(a)
    specific.html2json(a, start=bill_s, end=bill_e)

    print ## Get pdfs
    pdf.get_pdf(a, start=bill_s, end=bill_e)
