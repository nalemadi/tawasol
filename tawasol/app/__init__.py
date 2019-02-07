from database_manager.MongoDB_Manager import *
from database_manager.SqliteManager import *
import redis
import yaml
import os

# Current Location
CURR_LOC = os.path.join(os.path.dirname(__file__), 'config')
# Configuration files
MONGO_DB_CONFIG = yaml.load(open(CURR_LOC+'/mongodb.yml'))
REDIS_CONFIG = yaml.load(open(CURR_LOC+'/redis.yml'))
twitter_keys = yaml.load(open(CURR_LOC+'/keys.yml'))

# get users from sqlite
sqlite_manager = SqliteManager()
users_dict = sqlite_manager.get_keywords_accounts_for_user()

#Connect to MongoDb
mongodb_connector = mongoDB_manager(MONGO_DB_CONFIG)
undefined_tweets_collection = '%s_%s' % ('undefined', MONGO_DB_CONFIG['tweets_collection'])
tweets_collections_list = []
tweets_collections_list.append(undefined_tweets_collection)
keywords = []
accounts = []
for key, value in users_dict.iteritems():
	key_broken = key.split('@')
	user_name = key_broken[0]
	user_tweets_collection = '%s_%s' % (user_name, MONGO_DB_CONFIG['tweets_collection'])
	tweets_collection = mongodb_connector.connect_to_collection(user_tweets_collection)
	tweets_collections_list.append(tweets_collection)

	user_keywords = value['keywords']
	user_accounts = value['accounts']
	if user_keywords:
		keywords += value['keywords']

	if user_accounts:
		accounts += value['accounts']

keywords = list(set([_.strip().lower() for _ in keywords if len(_.strip()) > 1]))
accounts = list(set([_.strip().lower() for _ in accounts if len(_.strip()) > 1]))

REDIS_DB = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])
REDIS_NAMESPACE = REDIS_CONFIG['host']
tweets_channel = '%s:%s' % (REDIS_NAMESPACE, REDIS_CONFIG['channels']['tweets'])