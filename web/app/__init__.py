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

# Redis Configuration
REDIS_DB = redis.Redis(host=APP_CONFIG_TYP['redis']['host'], port=APP_CONFIG_TYP['redis']['port'])
REDIS_NAMESPACE = APP_CONFIG_TYP['redis']['host']