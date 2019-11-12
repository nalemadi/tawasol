import os
import json

from . import APP_CONFIG, twitter_keys, tweets_collections_dict, \
	keywords, accounts, REDIS_DB, tweets_channel, users_dict, results_channels
from tweets_collector import tweets_collector
from app.data_analyzer.tweets_processor import TweetProcessor
from multiprocessing import Process


twitter_keywords = ','.join(keywords)

proxy_index = -4
proxies_list = qcri_proxies
os.environ['http_proxy']=APP_CONFIG['PROXY']['twitter_proxy']

tweet_processor = TweetProcessor(REDIS_DB, tweets_channel, results_channels, tweets_collections_dict, users_dict)
tweet_processor.start()

twitter_collector_thr = Process(target=tweets_collector, args=(twitter_keys, keywords, accounts, REDIS_DB, tweets_channel,))
twitter_collector_thr.start()
