# @Author: DivineEnder
# @Date:   2017-03-29 14:47:11
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-04 14:41:25

import Utils.settings as settings
settings.init()

import math
from nltk import word_tokenize
from wordcloud import STOPWORDS
import Utils.connection_utils as glc

def tokenize_article(article):
	# Build list of stopwords to remove
	stopwords = set(STOPWORDS)
	stopwords.add("said")
	# Tokenize the article using nltk
	tokens = word_tokenize(article["content"])
	# Remove all stop words from tokens
	for stop_word in stopwords:
		tokens = [token.lower() for token in tokens if not token.lower() == stop_word.lower()]

	# Return article tokens
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

def classify_article(dictionaries, article, overfit = False):
	'''
	Process:
		INPUT: set of dictionaries associated with a unique source, a test article
		OUTPUT: The source associated with the test article

	uncomment next line when testing with test_classify_article.py
	tokens = article.split(" ")
	'''

	# Comment next line when testing with test_classify_article.py
	article_tokens = tokenize_article(article)
	# Initialize keys (source name) and values = 0 for each source-associated score dictionary
	sums = dict.fromkeys(dictionaries.keys(), 0)

	# Compute the actual scores of each sum for the test article by iterating across the tokens
	for token in article_tokens:
		# Create a dictionary of source ids to booleans for whether the current token is in each source
		token_in_sources = dict.fromkeys(dictionaries.keys(), True)
		# Create a field within the dictionary to determine whether the given token is in all sources
		token_in_sources["all"] = True
		# Populate the dictionary with the correct booleans for each source
		for source_id in dictionaries.keys():
			if dictionaries[source_id]["classifier"].get(token) is None:
				token_in_sources["all"] = False
				token_in_sources[source_id] = False

		# Add to the overall article score based on whether the token in is the sources
		for source_id in dictionaries.keys():
			# If the token is in all sources then simply add the corresponding token value for each source
			if token_in_sources["all"]:
				sums[source_id] = sums[source_id] + dictionaries[source_id]["classifier"][token]
			# If the token is not in all sources then add 1 to the sources which it is not in (picking the minimum makes it less like to pick sources with words that don't appear in corpus)
			elif not token_in_sources[source_id] and overfit:
				sums[source_id] = sums[source_id] + 1

	# Teturn the source with the minimum sum of words. The article is classified as coming from this source.
	return min(sums, key=sums.get), sums
