#coding=utf-8
#from nltk.tokenize import word_tokenize, sent_tokenize
#from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
#import string
import re


"""
def clean_text(text):
	# 1. remove urls
	text = re.sub(r"http\S+", "", text)
	# 2. tokenize and remove punctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	text = ' '.join([w for s in sent_tokenize(text) for w in word_tokenize(s) if w not in string.punctuation])
	# TODO: make sure we want to keep this one - 3. remove non ascii characters
	#text = ''.join([c for c in text if c in string.printable])
	return text
"""

"""
def clean_ar_text(text):
	text = re.sub(r"http\S+", "", text)
	tokenizer = RegexpTokenizer(r'\w+')
	text = [word for sent in sent_tokenize(text) for word in tokenizer.tokenize(sent) if not word.isdigit()]
	return ' '.join(text)
"""


def simple_clean_text(text):
	# 1. remove urls
	text = re.sub(r"http\S+", "", text)
	# 2. remove puctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	#text = re.sub(r'[^\w\s]','',text)
	text = re.sub(r'\w+','',text)
	text_broken = text.lower().strip().split(' ')
	#en_stops = set(stopwords.words('english'))
	#text = ' '.join(ch for ch in text_broken if ch not in en_stops)
	#text = text.lower()
	#txt_arr = text.split(' ')
	return text_broken

"""
if __name__ == '__main__':
	#print simple_clean_text('@SkyNews qatar_mowasalat I would? like to see that though. Maybe next time she scores a goal.')
	text = u'برنامج الحقيقة تقديم يوسف علاونة على قناة 24 سعودي الفضائية بعنوان "مرتزقة الاعلام القطري" وجمال ريان ابن سمسار الا… https://t.co/2DKYOMNPbQ'
	arr = simple_clean_text(text)
	print [x for x in arr]
	#unicode(x.decode("unicode_escape").encode("utf-8"))
"""

