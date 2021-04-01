import os
import sys
from datetime import datetime

BOT_NAME = 'Raffle'

SPIDER_MODULES = ['Raffle.Raffle.spiders']
NEWSPIDER_MODULE = 'Raffle.Raffle.spiders'

USER_AGENT_LIST = "c:\\Projects\\Work11\\pythonrafflescrape\\Raffle\\Raffle\\useragents.txt"

ROBOTSTXT_OBEY = False
DOWNLOADER_MIDDLEWARES = {
	'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
	'random_useragent.RandomUserAgentMiddleware': 400,
}

CONCURRENT_REQUESTS=20
CONCURRENT_REQUESTS_PER_DOMAIN=20

DOWNLOAD_TIMEOUT=30
LOG_LEVEL = 'WARNING'

DOWNLOAD_DELAY=1
RANDOMIZE_DOWNLOAD_DELAY = True

RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 404, 408]

# Feed details
#FEED_FORMAT = 'json'
#FEED_URI = 'data/%s.json'%datetime.utcnow().strftime('%Y-%d-%mT%H-%M-%S') # WHERE to store the export file

REDIRECT_ENABLED = True
REFERER_ENABLED = False

COOKIES_ENABLED = False
COOKIES_DEBUG = False
PROXY_LIST = ['http://37.48.118.90:13042','http://83.149.70.159:13042']

if PROXY_LIST:
	DOWNLOADER_MIDDLEWARES['Raffle.Raffle.middlewares.RetryMiddleware'] = 200
	DOWNLOADER_MIDDLEWARES['Raffle.Raffle.middlewares.ProxyMiddleware'] = 100
