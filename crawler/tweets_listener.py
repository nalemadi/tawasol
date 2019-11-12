from tweepy.streaming import StreamListener
import json
import datetime
import time
import logging


class TweetsListener(StreamListener):

    def __init__(self, redis_db, tweets_channel):
        super(StreamListener, self).__init__()

        self.redis_db = redis_db
        self.tweets_channel = tweets_channel

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            if tweet['text']:
                self.redis_db.rpush(self.tweets_channel, json.dumps(tweet))
        except Exception, e:
            pass

    def on_error(self, status):
        logging.warn('Error in twitter listener, status: %s' % status)
        if status == 420:
            logging.info('Rate Limit!! ... sleep from 15 minutes, %s' % datetime.datetime.now())
            time.sleep(900)  # 15 minutes
        #pass
