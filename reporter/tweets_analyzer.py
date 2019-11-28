import logging
from consts import NBR_HAHSTAGS
from collections import defaultdict, Counter
from tweet import Tweet
from datetime import datetime
from consts import langs_dict, TIME_COVERED, TIME_GRANULARITY
from datetime import timedelta
from app.models.genderizer.genderizer_client import *

logging.getLogger().setLevel(logging.INFO)

# model to infer whether the user is male/female
genderizer = Genderizer(male_fname='./data/male.txt', female_fname='./data/female.txt')


class TweetsAnalyzer():

    def __init__(self):
        self.time_indexes = set()
        self.users_distribution = defaultdict(set)
        self.tweets_distribution = defaultdict(set)
        self.tweets_sentiment = defaultdict(lambda: defaultdict(int))
        self.tweets_happiness = defaultdict(set)
        self.language_distribution = defaultdict(int)
        self.hashtags = defaultdict(int)
        self.mentions = defaultdict(int)
        self.top_users = defaultdict(int)
        self.gender_distribution = {'female': 0, 'male': 0}
        self.users_profile = dict()
        self.user_cat = dict()
        self.accounts_creation = {'Week': 0, 'Month': 0, '3-Months': 0, '6-Months': 0, 'Year': 0, '+Year': 0}
        self.accounts_tweets_counter = {'Week': 0, 'Month': 0, '3-Months': 0, '6-Months': 0, 'Year': 0, '+Year': 0}
        self.account_age_cat = ['Week', 'Month', '3-Months', '6-Months', 'Year', '+Year']

    def generate_tweet_with_timeIndex(self, tweet, time_slots):
        is_string = isinstance(tweet['created_at'], basestring)
        if is_string:
            tweet_date = self.to_datetime(tweet['created_at'])
        else:
            tweet_date = tweet['created_at']
        time_index = self.get_time_index(tweet_date, time_slots)
        result_tweet = Tweet(tweet, time_index)
        return result_tweet

    def to_datetime(self, created_at):
        """
        convert string to date
        :param created_at: string
        :return: datetime
        """
        dt = datetime.strptime(created_at,'%a %b %d %H:%M:%S +0000 %Y')
        dt = dt.replace(second=0, microsecond=0)
        return dt

    def get_time_index(self, tweet_date, time_slots):
        """
        :param tweet_date:
        :param time_slots:
        :return:
        """
        for curr_time_slot, next_time_slot in zip(time_slots, time_slots[1:]):
            if curr_time_slot <= tweet_date < next_time_slot:
                return curr_time_slot.strftime('%Y-%m-%dT%H:%M')
        return None

    def get_language_dist(self, lang_list, limit=7):
        lst_lang_top = sorted(lang_list, key=lambda x:x[1], reverse=True)[:limit]
        others_lang_freq = sum([x[1] for x in sorted(lang_list, key=lambda x:x[1], reverse=True)[limit:]])
        return map(list, lst_lang_top) + [['other', others_lang_freq]]

    def get_tweets_summary_report(self):
        """
        get summary of all tweets statistics
        :return: dictionary for all tweets statistics
        """
        logging.info('Generating Tweets Report')
        result = dict()

        # Categories
        result['categories'] = sorted(self.time_indexes)

        # Tweets Sentiment
        result['positive'] = [self.tweets_sentiment[x].get('positive', 0) for x in self.time_indexes]
        result['negative'] = [self.tweets_sentiment[x].get('negative', 0) for x in self.time_indexes]
        result['neutral'] = [self.tweets_sentiment[x].get('neutral', 0) for x in self.time_indexes]

        # Nbr of tweets/users
        result['nbr_users'] = sum([len(list(self.users_distribution[x])) for x in self.time_indexes])
        result['nbr_tweets'] = sum([len(list(self.tweets_distribution[x])) for x in self.time_indexes])

        # Happiness Chart
        result['happiness'] = [self.get_emotion(' '.join(list(self.tweets_distribution[x])), lang='en') for x in self.time_indexes]
        #result['happiness'] = [self.tweets_happiness[x] for x in self.time_indexes]

        # Users Chart
        result['users'] = [len(list(self.users_distribution[x])) for x in self.time_indexes]

        # Hashtags Chart
        users_hashtags = [{'text': hashtag, 'weight': freq, 'link': {'href': '%s%s' % ('https://twitter.com/hashtag/', hashtag), 'target': '_blank'}} for hashtag, freq in self.hashtags.iteritems()]
        result['hashtags'] = sorted(users_hashtags, key=lambda x:x['weight'], reverse=True)[:NBR_HAHSTAGS]

        users_count = [{'text': username, 'weight': freq, 'link': {'href': '%s%s' % ('https://twitter.com/', username), 'target': '_blank', 'title': 'This user tweeted %s times' % (freq)}} for username, freq in self.top_users.iteritems()]
        result['top_users'] = sorted(users_count, key=lambda x: x['weight'], reverse=True)[:20]

        # Mentions tagCloud
        top_mentions = [{'text': mention, 'weight': freq, 'link': {'href': '%s%s' % ('https://twitter.com/', mention),'target': '_blank', 'title': 'This user is mentioned %s times' % (freq)}} for mention, freq in self.mentions.iteritems()]
        result['top_mentions'] = sorted(top_mentions, key=lambda x: x['weight'], reverse=True)[:20]

        result['account_age_cat'] = self.account_age_cat
        result['account_creation'] = [self.accounts_creation[y] for y in self.account_age_cat]
        result['accounts_tweets_counter'] = [self.accounts_tweets_counter[y] for y in self.account_age_cat]

        # Language
        lst_lang = [[langs_dict.get(k,k),v] for k,v in self.language_distribution.items()]
        result['language'] = self.get_language_dist(lst_lang)

        # Gender Distribution
        result['gender'] = [['Female', self.gender_distribution['female']], ['Male', self.gender_distribution['male']]]

        try:
            if self.tweets_distribution:
                result['tweets'] = [tweet for tweet in self.tweets_distribution[max(self.tweets_distribution)]] # [(-1)*NBR_TWEETS:]
            else:
                result['tweets'] = []

        except Exception as e:
            result['tweets'] = None
            # print 'error get_tweets_summary_report', e

        if result['tweets']:
            # [tweet.tweet_text, '-- @' + tweet.screen_name, tweet_date.strftime('%Y-%m-%dT%H:%M:%S'), str(tweet.tweet_coor)]
            tweets = result['tweets']
            tweets_arr = []
            for tweet in tweets:
                broken = tweet.split('-- ')
                tweet_text = broken[0]
                tweets_arr.append(tweet_text)
            ###
            counter_tweets = Counter(tweets_arr)
            tweets_count = [{'text': tweet_txt, 'weight': freq} for tweet_txt, freq in counter_tweets.iteritems()]
            result['top_tweets'] = sorted(tweets_count, key=lambda x:x['weight'], reverse=True)[:20]
            ###

        return result

    def populate_tweets(self, tweet):
        # time_index
        self.time_indexes.add(tweet.time_index)

        # Gender
        if tweet.gender is not None:
            self.gender_distribution[tweet.gender] += 1

        # Language
        self.language_distribution[tweet.lang] += 1

        # Sentiment
        self.calculate_sentiment_dist(tweet.time_index, tweet.sentiment_score)

        # User distribution
        self.users_distribution[tweet.time_index].add(tweet.screen_name)
        self.top_users[tweet.screen_name] +=1

        # Tweet distribution
        is_string = isinstance(tweet.created_at, basestring)
        if is_string:
            tweet_date = self.to_datetime(tweet.created_at)
        else:
            tweet_date = tweet.created_at
        self.tweets_distribution[tweet.time_index].add('\n'.join([tweet.tweet_text, '-- @' + tweet.screen_name, tweet_date.strftime('%Y-%m-%dT%H:%M:%S')]))

        self.tweets_happiness[tweet.time_index].add(tweet.emotion_score)
        # Used hashtags
        for hashtag in tweet.hashtags:
            self.hashtags[hashtag] += 1

        # user mentions
        for mention in tweet.mentions:
            self.mentions[mention] += 1

    def calculate_sentiment_dist(self, date_index, sentiment_score):
        """
        calculate sentiment distribution in date index
        :param date_index: date
        :param sentiment_score: int
        :return:
        """
        # tweet sentiment
        if self.tweets_sentiment.get(date_index, None) is None:
            self.tweets_sentiment[date_index] = {'negative': 0, 'positive': 0, 'neutral': 0 }

        if sentiment_score < 0:
            self.tweets_sentiment[date_index]['negative'] += 1
        elif sentiment_score > 0:
            self.tweets_sentiment[date_index]['positive'] += 1
        else:
            self.tweets_sentiment[date_index]['neutral'] += 1

    def get_account_creation_cat(self, creation_date_st):
        range = '+Year'
        creation_date = datetime.strptime(creation_date_st, '%a %b %d %H:%M:%S +0000 %Y').date()
        if self.week_ago <= creation_date:
            range = 'Week'
        elif self.month_age <= creation_date:
            range = 'Month'
        elif self.months_3_ago <= creation_date:
            range = '3-Months'
        elif self.months_6_ago <= creation_date:
            range = '6-Months'
        elif self.year_ago <= creation_date:
            range = 'Year'
        elif creation_date < self.year_ago:
            range = '+Year'
        else:
            print 'error in get_account_creation_range'
        return range

    def populate_account_creation_info(self, result_tweet):
        creation_date = result_tweet.user_info['account_creation']
        user_id = result_tweet.user_info['user_id']
        if user_id not in self.users_profile:
            self.users_profile[user_id] = {'creation_date': creation_date}
            cat = self.get_account_creation_cat(creation_date)
            self.user_cat[user_id] = cat
            self.accounts_creation[cat] += 1

        self.accounts_tweets_counter[self.user_cat[user_id]] += 1

    def get_all_timeslots(self):
        """
        prepare timeslots list
        :return: timeslots list
        """
        max_frames = TIME_COVERED
        start = datetime.utcnow()
        time_slots = [start - timedelta(minutes=x) for x in range(0, max_frames+1, TIME_GRANULARITY)]
        return sorted(time_slots)

    def get_analyzed_tweets(self, tweets):
        """
        :param tweets:
        :return:
        """
        time_slots = self.get_all_timeslots()
        self.get_accounts_creation_ranges()
        # This is iterating over PyMongoDB cursor.
        n = 0
        for tweet in tweets:
            # Assign a tweet to a time slot
            result_tweet = self.generate_tweet_with_timeIndex(tweet, time_slots)

            # get account creation info
            self.populate_account_creation_info(result_tweet)

            # Update all reports: e.g., gender distribution, user distribution, etc.
            self.populate_tweets(result_tweet)
            n += 1

        result = self.get_tweets_summary_report()
        return result, n
