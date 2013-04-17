BOT_NAME = 'Open'
BOT_VERSION = '1'

SPIDER_MODULES = ['popong.spiders']
NEWSPIDER_MODULE = 'popong.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

FEED_URI = 'items.json'
FEED_FORMAT = 'json'
