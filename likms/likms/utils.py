def sel_to_str(sel):
    return ''.join(s.strip() for s in sel.extract())

def assembly_id_by_bill_id(bill_id):
    assembly_id = bill_id.lstrip('Z')[:2]
    return assembly_id

