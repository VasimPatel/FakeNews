# @Author: DivineEnder
# @Date:   2017-03-29 14:47:11
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-29 15:13:55 

import Utils.settings as settings
settings.init()

import math
from nltk import word_tokenize
from wordcloud import STOPWORDS
import Utils.connection_utils as glc

def tokenize_article(article):
	stopwords = set(STOPWORDS).add("said")
	tokens = word_tokenize(article["content"])
	for stop_word in stopwords:
		tokens.remove(stop_word)

	return tokens

def build_class_dict(articles):
	total_words = 0

	class_dict = {}
	for article in articles:
		tokens = tokenize_article(article)
		for token in tokens:
			if token in class_dict.keys():
				class_dict[token] = class_dict[token] + 1
			else:
				class_dict[token] = 1
		total_words = total_words + len(tokens)

	for key, value in class_dict:
		class_dict[key] = -1 * math.log(float(class_dict[key]) / float(total_words))

	return class_dict

def classify_article(dictionaries, article):
	article_tokens = bay.tokenize_article(article)

	sums = {}

	for each_token in tokens:
		for each_dictionary in dictionaries.keys():
			sums[each_dictionary] = sums[each_dictionary] + each_dictionary[each_token]

	return min(sums, key=sums.get)