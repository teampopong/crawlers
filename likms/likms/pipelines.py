import os

from likms.items import HtmlItem


class HtmlPipeline(object):
    def process_item(self, item, spider):
        self.makedir(item['path'])

        if isinstance(item, HtmlItem):
            with open(item['path'], 'w') as f:
                f.write(item['body'])
        return item

    def makedir(self, path):
        dirpath = os.path.dirname(path)
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)


class FilterExistingBillPipeline(object):
    def process_item(self, item, spider):
        return item  # TODO

