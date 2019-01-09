from tweets_analyzer import TweetsAnalyzer
from multiprocessing import Process

import json

import logging
logging.getLogger().setLevel(logging.INFO)


class TweetProcessor(Process):

	def __init__(self, redis_db, tweets_channel, tweets_collection_list, users_dict):
		super(TweetProcessor, self).__init__()

		self.tweets_collection_list = tweets_collection_list
		self.users_dict = users_dict

		# redis channel
		self.redis_db = redis_db
		self.tweets_channel = tweets_channel

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
					print 'INFO: collection: ', collections, 'process tweet:' , processed_tweet
					for collection in collections:
						for tweet_collection in self.tweets_collection_list:
							if collection == tweet_collection.name:
								tweet_collection.insert_one(processed_tweet)
								print 'INFO: tweet: ',processed_tweet, 'inserted into:', collection
			except Exception as e:
				logging.info('TweetProcessor: tweets processor error: %s' % e)
				pass
