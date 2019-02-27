from tweets_analyzer import TweetsAnalyzer
from multiprocessing import Process

import json

import logging
logging.getLogger().setLevel(logging.INFO)


class TweetProcessor(Process):

	def __init__(self, redis_db, tweets_channel, results_channels, tweets_collection_list, users_dict):
		super(TweetProcessor, self).__init__()

		self.tweets_collection_list = tweets_collection_list
		##
		undefined_tweets_collection = None
		for tweets_collection in tweets_collection_list:
			if tweets_collection.name == 'undefined_tweets':
				undefined_tweets_collection = tweets_collection
		self.undefined_tweets_collection = undefined_tweets_collection
		##
		self.users_dict = users_dict

		# redis channel
		self.redis_db = redis_db
		self.tweets_channel = tweets_channel
		self.results_channel = results_channels

		self.tweetsAnalyzer = TweetsAnalyzer()

	def run(self):
		while True:
			try:
				# if there is something in the queue, process it.
				if self.redis_db.llen(self.tweets_channel) > 0:
					tweet = self.redis_db.lpop(self.tweets_channel)
					#logging.info(json.dumps(tweet, ensure_ascii=False).encode('utf8'))

					_tweet = json.loads(tweet)
					processed_info = self.tweetsAnalyzer.process_tweet(_tweet, self.users_dict)
					processed_tweet = processed_info[0]
					collections = processed_info[1]
					if len(collections) > 0:
						for collection in collections:
							broken = collection.split('_')
							user_name = broken[0].lower()
							for tweet_collection in self.tweets_collection_list:
								if collection == tweet_collection.name:
									#self.redis_db.rpush(self.results_channel[user_name], json.dumps(processed_tweet))
									#self.redis_db.ltrim(self.results_channel[user_name], -1000, -1)
									##
									tweet_collection.insert_one(processed_tweet)
									logging.info('tweet is inserted into: %s - %s . tweet: %s' % (collection, user_name, processed_tweet['text']))
					else:
						self.undefined_tweets_collection.insert_one(processed_tweet)
						logging.info('tweet is inserted into Undefined collection: %s' % processed_tweet['text'])
			except Exception as e:
				logging.info('TweetProcessor: tweets processor error: %s' % e)
				pass
