#!/usr/bin/python

import tempfile
import subprocess

def pdf2txt(pdffile, txtfile):
    if txtfile==None:
        txtfile = pdffile.replace('.pdf', '.txt')

    with open(pdffile, 'r') as f:
        pdfdata = f.read()

    inf = tempfile.NamedTemporaryFile()
    inf.write(pdfdata)
    inf.seek(0)

    if (len(pdfdata) > 0) :
        out, err = subprocess.Popen(\
            ["pdftotext", "-layout", inf.name, txtfile]).communicate()
        return True
    else :
        return False

if __name__ == '__main__':
    # Usage: python pdf2txt.py file.pdf file.txt
    import sys
    pdf2txt(sys.argv[1], sys.argv[2])
