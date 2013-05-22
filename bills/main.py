#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

import meta
import specific
import pdf

assembly_s, assembly_e = 17, 19
bill_s, bill_e = None, None

for a in range(assembly_s, assembly_e+1):
    print '\n# Assembly %d' % a

    print '## Get meta data'
    npages = meta.get_npages(a)
    meta.get_html(a, npages)
    meta.html2csv(a, npages)

    print '## Get specific data'
    specific.get_html(a, range=(bill_s, bill_e))
    specific.html2json(a, range=(bill_s, bill_e))

    print '## Get pdfs'
    pdf.get_pdf(a, range=(bill_s, bill_e))
