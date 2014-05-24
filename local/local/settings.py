# Scrapy settings for local project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

import os.path

BOT_NAME = 'local'

SPIDER_MODULES = ['local.spiders']
NEWSPIDER_MODULE = 'local.spiders'

DOWNLOAD_TIMEOUT = 10
DOWNLOAD_DELAY = 0.5

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.132 Safari/537.36'
COOKIES_ENABLED = False

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# User settings (higher priority)
try:
    from likms.settings_local import *
except ImportError as e:
    pass

