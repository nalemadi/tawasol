#coding=utf-8
import re
import logging


def simple_clean_text(text):
	logging.info('=== simple_clean_text ===')
	# 1. remove urls
	text = re.sub(r"http\S+", "", text)
	# 2. remove puctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	#print '1:', text
	text = re.sub(r'[^\w\s]', '', text)
	#print '2:', text.strip()
	text_broken = text.lower().strip().split(' ')
	return text_broken


def simple_clean_text_ar(text):
	logging.info('=== simple_clean_text_ar ===')
	# 1. remove urls
	text = re.sub(r"http\S+", "", text)
	# 2. remove puctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	#text = re.sub(r'[^\w\s]','',text)
	#print '1:', text
	#[ ^\u0600 -\u06FF]+
	# r'\w+]'
	text = re.sub(r'[\u0600 -\u06FF]+', '', text)
	#print '2:', text.strip()
	text_broken = text.lower().strip().split(' ')
	#en_stops = set(stopwords.words('english'))
	#text = ' '.join(ch for ch in text_broken if ch not in en_stops)
	#text = text.lower()
	#txt_arr = text.split(' ')
	return text_broken
