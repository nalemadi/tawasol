from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize import RegexpTokenizer
import string
import re


def clean_text(text):
	# 1. remove urls
	text = re.sub(r"http\S+", "", text)
	# 2. tokenize and remove punctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	text = ' '.join([w for s in sent_tokenize(text) for w in word_tokenize(s) if w not in string.punctuation])
	# TODO: make sure we want to keep this one - 3. remove non ascii characters
	#text = ''.join([c for c in text if c in string.printable])
	return text


def clean_ar_text(text):
	text = re.sub(r"http\S+", "", text)
	tokenizer = RegexpTokenizer(r'\w+')
	text = [word for sent in sent_tokenize(text) for word in tokenizer.tokenize(sent) if not word.isdigit()]
	return ' '.join(text)