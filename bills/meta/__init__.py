import csv
import html

def get_npages(assembly_id):
    return html.get_npages(assembly_id)

def get_html(assembly_id, npages):
    html.getlist(assembly_id, npages)

def html2csv(assembly_id, npages):
    csv.parselist(assembly_id, npages)
