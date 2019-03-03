from threading import Thread
import time
import logging
import json
from datetime import datetime
from ..data_analyzer.tweets_analyzer import TweetsAnalyzer
from ..data_querier.time_querier import TimeQuerier
from ..config.dashboard_config import TIME_GRANULARITY, TIME_COVERED


class TawasolAnalyzer(Thread):

	def __init__(self, tweets_collection, users, redis_db, results_channels, interval=TIME_GRANULARITY):
		Thread.__init__(self)
		self.tweets_collection = tweets_collection
		self.users = users
		self.redis_db = redis_db
		self.results_channels = results_channels
		self.interval = interval

	def tawasol_analyzer(self, user_name):
		tweets_analyzer = TweetsAnalyzer()

		# user's tweets from mongodb
		user_collection = self.tweets_collection[user_name]

		time_querier = TimeQuerier(user_collection, user_name, TIME_COVERED)
		logging.info('running tweets query for %s' % user_name)
		tweets = time_querier.get_tweets_in_period()

		logging.info('Analyzing extracted Tweets for %s' % user_name)
		tw_analyzed_data, n_tweets = tweets_analyzer.get_analyzed_tweets(tweets)
		logging.info('Analyzed %s Tweets for %s' % (n_tweets, user_name))

		return {'twitter': tw_analyzed_data}

	def run(self):
		""" Method that runs forever """
		while True:
			for user_name in self.users:

				logging.info('*** Tawasol Analyzer for %s: %s\n**************' % (user_name, datetime.now()))
				data = self.tawasol_analyzer(user_name)

				# remove the previous one
				#self.redis_db.lpop(self.results_channels[user_name])

				# insert to redis Queue
				self.redis_db.rpush(self.results_channels[user_name], json.dumps(data))
				#self.redis_db.ltrim(self.results_channels[user_name], -100000, -1)
				logging.info('inserted tawasol_data for %s into redis channel: (%s)' % (user_name, self.results_channels[user_name]))

			logging.info("Sleeping for: %s" % self.interval)
			time.sleep(self.interval)


if __name__ == '__main__':
	tawasol_analyzer = TawasolAnalyzer()
	tawasol_analyzer.start()
