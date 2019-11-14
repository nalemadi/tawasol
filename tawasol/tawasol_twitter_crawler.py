import os
from app.utils.consts import qcri_proxies
from app import MONGO_DB_CONFIG, REDIS_CONFIG, twitter_keys, tweets_collections_dict, \
	keywords, accounts, REDIS_DB, tweets_channel, users_dict, results_channels, keywords_dict, accounts_dict
from app.tweets_collector.tweets_collector import tweets_collector
from app.data_analyzer.tweets_processor import TweetProcessor
from multiprocessing import Process
import json


# print MONGO_DB_CONFIG
# print REDIS_CONFIG
# print twitter_keys
###############
print 'total hashtags: ', len(keywords)
twitter_keywords = ','.join(keywords)
#print twitter_keywords

print 'total accounts', accounts
###############
print tweets_collections_dict

# print json.dumps(users_dict, ensure_ascii=False).encode('utf8')
# print tweets_channel
# print REDIS_DB
print 'key_dict', keywords_dict
print 'acc_dict', accounts_dict

proxy_index = -4
proxies_list = qcri_proxies
os.environ['http_proxy']="[REDACTED_PROXYADD]"+proxies_list[proxy_index]+":[REDACTED_VALUE]"

tweet_processor = TweetProcessor(REDIS_DB, tweets_channel, results_channels, tweets_collections_dict, users_dict, keywords_dict, accounts_dict)
tweet_processor.start()

twitter_collector_thr = Process(target=tweets_collector, args=(twitter_keys, keywords, accounts, REDIS_DB, tweets_channel,))
twitter_collector_thr.start()
