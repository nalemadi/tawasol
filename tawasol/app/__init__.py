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
users_dict = sqlite_manager.get_hashtags_accounts_for_user()

#Connect to MongoDb
db_connector = mongoDB_manager(MONGO_DB_CONFIG)
tweets_collections_list = []
hashtags = []
accounts = []
for key, value in users_dict.iteritems():
	user_tweets_collection = '%s_%s' % (key, MONGO_DB_CONFIG['tweets_collection'])
	tweets_collection = db_connector.connect_to_collection(user_tweets_collection)
	tweets_collections_list.append(tweets_collection)

	user_hashtags = value['hashtags']
	user_accounts = value['accounts']
	if user_hashtags:
		hashtags += value['hashtags']

	if user_accounts:
		accounts += value['accounts']

REDIS_DB = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])
REDIS_NAMESPACE = REDIS_CONFIG['host']
tweets_channel = '%s:%s' % (REDIS_NAMESPACE, REDIS_CONFIG['channels']['tweets'])