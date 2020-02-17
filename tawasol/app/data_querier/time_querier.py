from pytz import timezone
from datetime import datetime, timedelta


class TimeQuerier:

	def __init__(self, tweets_collection, user_name, time_covered=None):
		self.tweets_collection = tweets_collection
		self.user_name = user_name
		self.time_covered = time_covered

	def get_tweets_in_period(self):
		"""
		:return: cursor of tweets
		"""
		# end_date = datetime.now(timezone('GMT'))
		end_date = datetime.now()
		start_date = end_date-timedelta(minutes=int(self.time_covered))
		cursor = self.tweets_collection.find({'created_at': {'$gte':start_date, '$lt':end_date}}, {'_id': False}) #For debuging.limit(10)
		cursor.batch_size(1000)
		return cursor

	def get_all_tweets(self):
		"""
		Return all tweets in the collection for a user.
		:return: cursor of all tweets
		"""
		cursor = self.tweets_collection.find({}, {'_id': False}).limit(100000)
		cursor.batch_size(1000)
		return cursor
