from scrapy.item import Item, Field

from likms.rules import filepath
from likms.utils import assembly_id_by_bill_id


class HtmlItem(Item):
    path = Field()
    body = Field()


class BillHtmlItem(HtmlItem):
    def __init__(self, bill_id, *args, **kwargs):
        super(BillHtmlItem, self).__init__(self, *args, **kwargs)

        assembly_id = assembly_id_by_bill_id(bill_id)
        self['path'] = filepath('bill-html',
                                assembly_id=assembly_id,
                                bill_id=bill_id)

