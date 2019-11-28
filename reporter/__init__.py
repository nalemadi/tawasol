from db_manager.mongodb_manager import MongodbManager
from db_manager.sqlite_manager import SqliteManager
import redis
import yaml
import os

# Current Location
CURR_LOC = os.path.join(os.path.dirname(__file__), 'config')
# Configuration files
APP_CONFIG = yaml.load(open(CURR_LOC+'/config.yml'), Loader=yaml.FullLoader)
APP_CONFIG_TYP = APP_CONFIG['dev']

DB_LOC = os.path.join(os.path.dirname(__file__), 'db_manager')
sqlite_db = APP_CONFIG_TYP['sqlite']['db_name']
tawasolsqlite = DB_LOC+'/'+sqlite_db
print '==== tawasol db === ', tawasolsqlite

# get users from sqlite
sqlite_manager = SqliteManager(tawasolsqlite)
users_dict = sqlite_manager.tawasol_users

#Connect to MongoDb
mongodb_connector = MongodbManager(APP_CONFIG_TYP['mongo'])
undefinedtweets_name = '%s_%s' % ('undefined', APP_CONFIG_TYP['mongo']['tweets_collection'])
undefined_tweets_collection = mongodb_connector.connect_to_collection(undefinedtweets_name)
tweets_collections_dict = dict()
tweets_collections_dict['undefined'] = undefined_tweets_collection

# Redis Configuration
REDIS_DB = redis.Redis(host=APP_CONFIG_TYP['redis']['host'], port=APP_CONFIG_TYP['redis']['port'])
REDIS_NAMESPACE = APP_CONFIG_TYP['redis']['host']
tweets_channel = '%s:%s' % (REDIS_NAMESPACE, APP_CONFIG_TYP['redis']['channels']['tweets'])
##
results_channels = dict()
users = []
for key, value in users_dict.iteritems():
    key_broken = key.split('@')
    user_name = key_broken[0].lower()

    #users list
    users.append(user_name)

    #redis channels
    results_channels[user_name] = '%s:%s_%s' % (REDIS_NAMESPACE, APP_CONFIG_TYP['redis']['channels']['results'], user_name)

    # mongodb collections
    user_tweets_collection = '%s_%s' % (user_name, APP_CONFIG_TYP['mongo']['tweets_collection'])
    tweets_collection = mongodb_connector.connect_to_collection(user_tweets_collection)
    tweets_collections_dict[user_name] = tweets_collection
