# @Author: DivineEnder
# @Date:   2017-03-29 14:47:11
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-03 19:19:59

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

def build_nltk_training_list(articles):
	training_list = []

	all_words = []
	for article in articles:
		article_dict = {}

		tokens = tokenize_article(article)
		for token in tokens:
			article_dict[token] = True

		for word in all_words:
			if not word in article_dict.keys():
				article_dict[word] = False

		all_words.extend(tokens)
		all_words = list(set(all_words))

		training_list.append(article_dict)

	return training_list

def build_source_dict(articles):
	# Keep track of all the words that the source used
	all_source_words = []

	source_dict = {}
	for article in articles:
		tokens = tokenize_article(article)
		for token in tokens:
			if token in source_dict.keys():
				source_dict[token] = source_dict[token] + 1
			else:
				source_dict[token] = 1

		all_source_words.extend(tokens)

	# all_source_words = list(set(all_source_words))

	for key, value in source_dict.items():
		source_dict[key] = -1 * (math.log(float(source_dict[key]) / float(len(all_source_words))))

	return source_dict, list(set(all_source_words))

def build_class_dict(articles, sources):
	class_dict = {}

	for source in sources:

		articles_from_source = []
		for article in articles:
			if article["source_id"] == source["source_id"]:
				articles_from_source.append(article)
				articles.remove(article)

		source_dict, source_words = build_source_dict(articles_from_source)
		class_dict[source["source_id"]] = { "words": source_words, "classifier": source_dict }

	return class_dict

def classify_article(dictionaries, article):
	'''
	Process:
		INPUT: set of dictionaries associated with a unique source, a test article
		OUTPUT: The source associated with the test article

	uncomment next line when testing with test_classify_article.py
	tokens = article.split(" ")
	'''

	#comment next line when testing with test_classify_article.py
	article_tokens = tokenize_article(article)
	sums = {}

	#initialize keys (source name) and values = 0 for each source-associated dictionary
	for source_id in dictionaries.keys():
		sums[source_id] = 0

	#for each word in test article (which has been reduced to common stems)
	for token in article_tokens:
		#for each source collect the -log(count/words) associate with each word.
		for source_id, value in dictionaries.items():
			#if the word is in the sources dictionary
			if value["classifier"].get(token) != None:
				#add the value associated with the word in this source to the sum of words in this dictionary
				sums[source_id] = sums[source_id] + value["classifier"][token]

	#return the source with the minimum sum of words. The article is classified as coming from this source.
	return min(sums, key=sums.get), sums
