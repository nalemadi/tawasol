#coding=utf-8
import re


def simple_clean_text(text):
	print '=== simple_clean_text ==='
	# 1. remove urls
	text = re.sub(r"http\S+", "", text)
	# 2. remove puctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	#print '1:', text
	text = re.sub(r'[^\w\s]', '', text)
	print '2:', text.strip()
	text_broken = text.lower().strip().split(' ')
	return text_broken

def simple_clean_text_ar(text):
	print '=== simple_clean_text_ar ==='
	# 1. remove urls
	text = re.sub(r"http\S+", "", text)
	# 2. remove puctuations: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
	#text = re.sub(r'[^\w\s]','',text)
	#print '1:', text
	#[ ^\u0600 -\u06FF]+
	# r'\w+]'
	text = re.sub(r'[\u0600 -\u06FF]+', '', text)
	print '2:', text.strip()
	text_broken = text.lower().strip().split(' ')
	#en_stops = set(stopwords.words('english'))
	#text = ' '.join(ch for ch in text_broken if ch not in en_stops)
	#text = text.lower()
	#txt_arr = text.split(' ')
	return text_broken

"""
if __name__ == '__main__':
	#print simple_clean_text_ar('@SkyNews qatar_mowasalat I would? like to see that though. Maybe next time she scores a goal.')
	#text = u'برنامج الحقيقة؟ تقديم\n يوسف $ علاونة على قناة'
	#text = u'برنامج الحقيقة تقديم يوسف علاونة على قناة 24 سعودي الفضائية بعنوان qatar_mowasalat I would "مرتزقة الاعلام القطري" وجمال ريان ابن سمسار الا… https://t.co/2DKYOMNPbQ'
	#text = '#qatar_metro test'
	list = [u'برنامج الحقيقة؟ تقديم\n يوسف $ علاونة على قناة', '@SkyNews qatar_mowasalat I would? like to see that though. Maybe next time she scores a goal.', u'برنامج الحقيقة تقديم يوسف علاونة على قناة 24 سعودي الفضائية بعنوان qatar_mowasalat I would "مرتزقة الاعلام القطري" وجمال ريان ابن سمسار الا… https://t.co/2DKYOMNPbQ', '#qatar_metro test']
	for text in list:
		print 'text:', text
		arr = simple_clean_text_ar(text)
		#arr1 = simple_clean_text(text)
		print 'arabic', [x for x in arr]
		#print 'english', [x for x in arr1]
		print '============================='

	#test_remove_punc('')
	#print [x for x in arr]
	#unicode(x.decode("unicode_escape").encode("utf-8"))
"""
