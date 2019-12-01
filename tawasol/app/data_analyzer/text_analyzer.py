from labMTsimple.storyLab import emotionFileReader, re, emotion, stopper, emotionV, subprocess
import os
from ..utils.consts import BLACK_LISTED_WORDS
import shlex
import logging
import random

labMT_eng, labMTvector_eng, labMTwordList_eng = emotionFileReader(stopval=0.0, lang='english', returnVector=True)
labMT_ar, labMTvector_ar, labMTwordList_ar = emotionFileReader(stopval=0.0, lang='arabic', returnVector=True)


class TextAnalyzer():

	def clean_text(self, text):
		"""
		Clean text from new lines, and lower the text
		:param text: str
		:return: cleaned string
		"""
		return text.encode('ascii', 'ignore').encode('utf8').replace('\n', ' ').replace('\r', '').lower()

	def get_hashtags_dist(self, text):
		"""
		get list of hashtags from a tweet text
		Deprecated: as for now
		:param text: str
		:return: list of hashtags
		"""
		hashtag_pattern = re.compile(r'#(\w*):?', re.IGNORECASE)
		hashtags = [x.lower() for x in re.findall(hashtag_pattern,text)]
		hashtags = [hashtag for hashtag in hashtags if hashtag not in BLACK_LISTED_WORDS]
		return hashtags

	def get_mentioned_users(self, text):
		"""
		extract mentioned usernames
		Deprecated: not used as for now.
		:param text: str
		:return: list of mentioned users
		"""
		mention_pattern = re.compile(r'@(\w*):?', re.IGNORECASE)
		mentions = [x.lower() for x in re.findall(mention_pattern, text)]
		return mentions

	def get_words_dist(self,text):
		"""
		get list of words from text
		:param text: str
		:return: list of words
		"""
		words_pattern = re.compile(r'([\w*]+)', re.IGNORECASE)
		words = [x.lower() for x in re.findall(words_pattern, text)]
		return words

	def get_emotion(self, text, lang):
		"""
		calculate the emotion of text using LabMT
		:param text: str
		:param lang: str
		:return: a score between 0 and 9.
		"""
		if lang == 'ar':
			valence, fvec = emotion(text, labMT_ar, shift=True, happsList=labMTvector_ar)
			stoppedVec = stopper(fvec, labMTvector_ar, labMTwordList_ar, stopVal=1.0)
			valence = emotionV(stoppedVec,labMTvector_ar)
			if valence == -1:
				return 0
			else:
				return valence
		elif lang == 'en':
			valence, fvec = emotion(text, labMT_eng, shift=True, happsList=labMTvector_eng)
			stoppedVec = stopper(fvec, labMTvector_eng, labMTwordList_eng, stopVal=1.0)
			valence = emotionV(stoppedVec, labMTvector_eng)

			if valence == -1:
				return 0
			else:
				return valence
		else:
			return 0

	def get_sentiment_sentistrength(self, text, lang):
		"""
		calculate the sentiment
		:param text:
		:param lang:
		:return:
		"""
		text = text.encode('utf8')
		# get location of the server
		server_location = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'utils'))
		p = subprocess.Popen(shlex.split("java -jar {}/SentiStrength.jar stdin sentidata {}/SentStrength_Data/ trinary".format(server_location, server_location)), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout_text, stderr_text = p.communicate(text.replace(" ", "+"))
		if lang == 'en':
			try:
				result = int(float(stdout_text.rstrip().split(' ')[-1]))
				return result
			except Exception as e:
				logging.info('Exception: get_sentiment_sentistrength')
				return 0
		else:
			score = random.randrange(-1, 2)
			return score

		# if lang == 'en':
		# 	text = text.encode('utf8')
		# 	#get location of the server
		# 	server_location = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'utils'))
		# 	p = subprocess.Popen(shlex.split("java -jar {}/SentiStrength.jar stdin sentidata {}/SentStrength_Data/ trinary".format(server_location, server_location)), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# 	stdout_text, stderr_text = p.communicate(text.replace(" ", "+"))
		#
		# 	try:
		# 		result = int(float(stdout_text.rstrip().split(' ')[-1]))
		# 		return result
		# 	except Exception, e:
		# 		return 0
		# else:
		# 	return 0