from collections import defaultdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import os
import hashlib


class Genderizer:
	"""
	Source of male and female data sets:
	# Data from http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/female.txt
	# Data from http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/male.txt
	"""
	def __init__(self, male_fname=None, female_fname=None):
		self.server_location = os.path.abspath(os.path.join(os.path.dirname( __file__ )))
		self.male_fname = '{}/{}'.format(self.server_location,male_fname)
		self.female_fname = '{}/{}'.format(self.server_location,female_fname)
		self.data = defaultdict()
		self.classifier = None

	def _hash_str(self, text):
		"""
		Hash a text
		:param text:
		:return: number
		"""
		key = int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)
		return key

	def load_data(self):
		"""
		load training data
		:return:
		"""
		male_data = [_.strip('\n') for _ in open(self.male_fname,'r').readlines()]
		female_data = [_.strip('\n') for _ in open(self.female_fname,'r').readlines()]

		for m_name in male_data:
			m_name = m_name.lower()
			self.data[m_name] = 2

		for f_name in female_data:
			f_name = f_name.lower()
			self.data[f_name] = 1

	def get_context(self, name):
		"""
		Prepare features
		:param name: first name of male or female
		:return: json object that contains features
		"""
		return {'last_letter': self._hash_str(name[-1]), 'last_two_letters': self._hash_str(name[-2:]), 'last_three_letters': self._hash_str(name[-3:]), 'is_last_vowel': 1 if name[-1] in ['A','E','I','O','U','Y'] else -1, 'category': self.data[name]}

	def get_features(self, name):
		"""
		Prepared features for training
		:param name: first name of male or female
		:return: json object that contains features
		"""
		return {'last_letter': self._hash_str(name[-1]), 'last_two_letters': self._hash_str(name[-2:]),'last_three_letters': self._hash_str(name[-3:]), 'is_last_vowel': 1 if name[-1] in ['A','E','I','O','U','Y'] else -1}

	def dump_model(self, model_name ='model/model_pickle.p'):
		"""
		export model to model name
		:param model_path: path of the model
		:return:
		"""
		model_name = '{}/{}'.format(self.server_location, model_name)
		with open(model_name , 'wb') as f:
			pickle.dump(self.classifier, f)

	def load_model(self, model_name ='model/model_pickle.p'):
		model_name = '{}/{}'.format(self.server_location, model_name)
		self.classifier = pickle.load(open(model_name, 'rb'))

	def train_and_test(self, percent_to_train = 0.30):
		"""
		train and test the model
		:param percent_to_test:
		:return:
		"""
		x_features = ['last_letter', 'last_two_letters', 'last_three_letters', 'is_last_vowel']
		y_features = ['category']

		# load data
		self.load_data()

		# get features
		feature_list = [self.get_context(name) for name in self.data]
		df = pd.DataFrame(feature_list)

		x_train, x_test, y_train, y_test = train_test_split(df[x_features], df[y_features], test_size=percent_to_train, random_state=0)

		self.classifier = RandomForestClassifier()
		self.classifier.fit(x_train, y_train)
		print 'Accuracy RF ', self.classifier.score(x_test, y_test)

		self.classifier = GaussianNB()
		self.classifier.fit(x_train, y_train)
		print 'Accuracy RF ', self.classifier.score(x_test, y_test)

	def train(self):
		x_features = ['last_letter', 'last_two_letters', 'last_three_letters', 'is_last_vowel']
		y_features = ['category']

		# load data
		self.load_data()

		# get features
		features = [self.get_context(name) for name in self.data]
		df = pd.DataFrame(features)

		self.classifier = RandomForestClassifier()
		self.classifier.fit(df[x_features], df[y_features])

		self.dump_model()

	def infer_gender(self, name):
		"""
		classify name by using trained model
		:param name: first name of male or female
		:return: gender
		"""
		name = name.strip().lower()
		# gender = {2:'male', 1:'female'}
		gender = {1:'male', 2:'female'}
		self.load_model()
		x_features = ['last_letter', 'last_two_letters','last_three_letters', 'is_last_vowel']

		try:
			df = pd.DataFrame([self.get_features(name)])
			predicted = self.classifier.predict(df)
			return gender[predicted[0]]

		except Exception as e:
			pass
			return None

if __name__ == '__main__':
	# Data from http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/female.txt
	# Data from http://www.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/male.txt

	genderizer = Genderizer(male_fname='data/male.txt', female_fname='data/female.txt')
	genderizer.train_and_test()
	genderizer.train()