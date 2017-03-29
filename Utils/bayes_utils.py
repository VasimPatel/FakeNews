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
	stopwords = set(STOPWORDS)
	stopwords.add("said")
	tokens = word_tokenize(article["content"])
	for stop_word in stopwords:
		while stop_word in tokens: tokens.remove(stop_word)

	return tokens

def build_source_dict(articles):
	total_words = 0

	source_dict = {}
	for article in articles:
		tokens = tokenize_article(article)
		for token in tokens:
			if token in source_dict.keys():
				source_dict[token] = source_dict[token] + 1
			else:
				source_dict[token] = 1
		total_words = total_words + len(tokens)

	for key, value in source_dict.items():
		source_dict[key] = -1 * (math.log(float(source_dict[key]) / float(total_words)))

	return source_dict

def build_class_dict(articles, sources):
	class_dict = {}

	for source in sources:
		articles_from_source = []

		for article in articles:
			if article["source_id"] == source["source_id"]:
				articles_from_source.append(article)
				articles.remove(article)
		class_dict[source["source_id"]] = build_source_dict(articles_from_source)


	return class_dict
