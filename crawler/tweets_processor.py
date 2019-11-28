from tweets_annotator import TweetsAnnotator
from multiprocessing import Process
import json
import logging
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(filename='crawler.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class TweetProcessor(Process):

	def __init__(self, redis_db, tweets_channel, results_channels, tweets_collection_dict, users_dict):
		super(TweetProcessor, self).__init__()

		self.tweets_collection_dict = tweets_collection_dict
		self.undefined_tweets_collection = tweets_collection_dict['undefined']
		##
		self.users_dict = users_dict

		# redis channel
		self.redis_db = redis_db
		self.tweets_channel = tweets_channel
		self.results_channel = results_channels
		self.tweets_annotator = TweetsAnnotator()

	def run(self):
		while True:
			try:
				# if there is something in the queue, process it.
				if self.redis_db.llen(self.tweets_channel) > 0:
					tweet = self.redis_db.lpop(self.tweets_channel)
					#logging.info(json.dumps(tweet, ensure_ascii=False).encode('utf8'))

					raw_tweet = json.loads(tweet)
					proc_result = self.tweets_annotator.annotate_tweet(raw_tweet, self.users_dict)
					processed_tweet = proc_result[0]
					tawasol_users = proc_result[1]
					# TODO: Noora, we should make sure all tweets captured are relevant. No need to store extra tweets.
					for tawasol_user in tawasol_users:
						tweet_collection = self.tweets_collection_dict[tawasol_user.lower()]
						tweet_collection.insert_one(processed_tweet)
						logging.info('tweet is inserted into: %s . tweet: %s' % (tawasol_user, processed_tweet['text']))
			except Exception as e:
				print 'TweetProcessor: tweets processor error', e
				logging.info('TweetProcessor: tweets processor error: %s' % e)
				pass
