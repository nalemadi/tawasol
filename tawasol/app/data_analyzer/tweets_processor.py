from tweets_analyzer import TweetsAnalyzer
from multiprocessing import Process

import json

import logging
logging.getLogger().setLevel(logging.INFO)


class TweetProcessor(Process):

	def __init__(self, redis_db, tweets_channel, tweets_collection_list, users_dict):
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
					"""
					if 'retweeted_status' in processed_tweet.keys():
						if 'extended_tweet' in processed_tweet['retweeted_status'].keys():
							print 'INFO: collection: ', collections, 'process tweet:', processed_tweet['retweeted_status']['extended_tweet']['full_text'].encode('utf-8')
					else:
						print 'INFO: collection: ', collections, 'process tweet:', processed_tweet['text'].encode('utf-8')
					"""
					print 'tweets_collection_list', self.tweets_collection_list
					print 'INFO: collection: ', collections, 'process tweet:', processed_tweet['text'].encode('utf-8')
					if len(collections) > 0:
						for collection in collections:
							for tweet_collection in self.tweets_collection_list:
								if collection == tweet_collection.name:
									tweet_collection.insert_one(processed_tweet)
									print 'INFO: a tweet inserted into:', collection, ". ", processed_tweet['text'].encode('utf-8')
					else:
						self.undefined_tweets_collection.insert_one(processed_tweet)
						print 'INFO: a tweet inserted into Undefined collection:', processed_tweet['text'].encode('utf-8')
			except Exception as e:
				logging.info('TweetProcessor: tweets processor error: %s' % e)
				pass
