import os
from app.utils.consts import qcri_proxies
from app import MONGO_DB_CONFIG, REDIS_CONFIG, twitter_keys, tweets_collections_list, \
	keywords, accounts, REDIS_DB, tweets_channel, users_dict
from app.tweets_collector.tweets_collector import tweets_collector
from app.data_analyzer.tweets_processor import TweetProcessor
from multiprocessing import Process
import json


print MONGO_DB_CONFIG
print REDIS_CONFIG
print twitter_keys
###############
print 'total hashtags: ', len(keywords)
twitter_keywords = ','.join(keywords)
#print twitter_keywords

print 'total accounts', accounts
###############
print tweets_collections_list

print json.dumps(users_dict, ensure_ascii=False).encode('utf8')
print tweets_channel
print REDIS_DB

proxy_index = 10
proxies_list = qcri_proxies
os.environ['http_proxy']="[REDACTED_PROXYADD]"+proxies_list[proxy_index]+":[REDACTED_VALUE]"

tweet_processor = TweetProcessor(REDIS_DB, tweets_channel, tweets_collections_list, users_dict)
tweet_processor.start()

twitter_collector_thr = Process(target=tweets_collector, args=(twitter_keys, keywords, accounts, REDIS_DB, tweets_channel,))
twitter_collector_thr.start()
