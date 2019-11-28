import os
from __init__ import APP_CONFIG_TYP, twitter_keys, tweets_collections_dict, keywords, accounts, REDIS_DB, tweets_channel, users_dict, results_channels
from tweets_collector import TweetsCollector
from tweets_processor import TweetProcessor
from multiprocessing import Process


twitter_keywords = ','.join(keywords)

os.environ['http_proxy'] = APP_CONFIG_TYP['proxy']['twitter_proxy']

tweet_processor = TweetProcessor(REDIS_DB, tweets_channel, results_channels, tweets_collections_dict, users_dict)
tweet_processor.start()

twitter_collector_thr = Process(target=TweetsCollector, args=(REDIS_DB, tweets_channel, twitter_keys, accounts, twitter_keywords,))
twitter_collector_thr.start()
