from database_manager.MongoDB_Manager import mongoDB_manager
from database_manager.SqliteManager import SqliteManager
from collections import defaultdict
import redis
import yaml
import os

# Current Location
CURR_LOC = os.path.join(os.path.dirname(__file__), 'config')
# Configuration files
MONGO_DB_CONFIG = yaml.load(open(CURR_LOC+'/mongodb.yml'), Loader=yaml.FullLoader)
REDIS_CONFIG = yaml.load(open(CURR_LOC+'/redis.yml'), Loader=yaml.FullLoader)
twitter_keys = yaml.load(open(CURR_LOC+'/keys.yml'), Loader=yaml.FullLoader)

# get users from sqlite
sqlite_manager = SqliteManager()
users_dict = sqlite_manager.tawasol_users

#Connect to MongoDb
mongodb_connector = mongoDB_manager(MONGO_DB_CONFIG)
undefined_tweets_collection_name = '%s_%s' % ('undefined', MONGO_DB_CONFIG['tweets_collection'])
undefined_tweets_collection = mongodb_connector.connect_to_collection(undefined_tweets_collection_name)
tweets_collections_dict = dict()
tweets_collections_dict['undefined'] = undefined_tweets_collection
keywords = []
accounts = []

# Redis Configuration
REDIS_DB = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])
REDIS_NAMESPACE = REDIS_CONFIG['host']
tweets_channel = '%s:%s' % (REDIS_NAMESPACE, REDIS_CONFIG['channels']['tweets'])
##
results_channels = {}
users = []
keywords_dict = defaultdict(set)
accounts_dict = defaultdict(set)
for key, value in users_dict.iteritems():
	key_broken = key.split('@')
	user_name = key_broken[0].lower()

	#users list
	users.append(user_name)

	#redis channels
	results_channels[user_name] = '%s:%s_%s' % (REDIS_NAMESPACE, REDIS_CONFIG['channels']['results'], user_name)

	# mongodb collections
	user_tweets_collection = '%s_%s' % (user_name, MONGO_DB_CONFIG['tweets_collection'])
	tweets_collection = mongodb_connector.connect_to_collection(user_tweets_collection)
	tweets_collections_dict[user_name] = tweets_collection

	user_keywords = value['keywords']
	user_accounts = value['accounts']
	if user_keywords:
		for uk in user_keywords:
			keywords_dict[uk].add(user_name)

		keywords += value['keywords']


	if user_accounts:
		for ac in user_accounts:
			accounts_dict[ac].add(user_name)
		accounts += value['accounts']

keywords = list(set([_.strip().lower() for _ in keywords if len(_.strip()) > 1]))
accounts = list(set([_.strip().lower() for _ in accounts if len(_.strip()) > 1]))
