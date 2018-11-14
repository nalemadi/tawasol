from ..utils.text_operations import clean_text
from tweet import Tweet
from pytz import timezone
from collections import defaultdict
from datetime import datetime


class TweetsAnalyzer():
	def __init__(self):
		return None

	def process_tweet(self, tweet, users_dict):
		"""
		add extra information to tweet object
		:param tweet:
		:return: tweet object with extra info
		"""
		print tweet
		collections = []
		for key, value in users_dict.iteritems():
			#check hashtags
			hashtags = value['hashtags']
			for hashtag in hashtags:
				if hashtag in tweet['text']:
					collections.append(key+'_tweets')
			#check accounts
			accounts = value['accounts']
			for account in accounts:
				if account == tweet['user']['screen_name']:
					collections.append(key + '_tweets')

		tweet['created_at'] = self.to_datetime(tweet['created_at']).replace(tzinfo=timezone('GMT'))
		return tweet, collections

	def get_qatar_locations(self):
		return ['qatar','doha']

	def is_tweet_from_qatar(self, tweet):
		"""
		not used
		Check whether tweet is from Qatar or not
		:param tweet: tweet object
		:return: boolean
		"""
		if 'coordinates' not in tweet.keys() and 'user' not in tweet.keys():
			return False

		if tweet['coordinates'] is not None:
			lat = tweet['coordinates']['coordinates'][1]
			lng = tweet['coordinates']['coordinates'][0]

			# Qatar boundingBox 50.7048, 24.4708, 51.7371, 26.2057
			lat_max, lat_min, lng_max, lng_min = 26.2057, 24.4708, 51.7371, 50.7048

			if lat_min <= lat <= lat_max and lng_min <= lng <= lng_max:
				return True
			else:
				return False
		if tweet['user']['location'] is None:
			return False
		else:
			qatar_locations = self.get_qatar_locations()
			user_location = clean_text(tweet['user']['location'].lower())
			user_locations = user_location.split()
			for usr_location in user_locations:
				if usr_location in qatar_locations:
					return True
			return False
