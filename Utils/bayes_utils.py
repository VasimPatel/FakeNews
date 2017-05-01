# @Author: DivineEnder
# @Date:   2017-03-29 14:47:11
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-16 14:27:49

import Utils.settings as settings
settings.init()

import os
import math
import datetime
import pickle
from psycopg2.extras import execute_values
from unidecode import unidecode
from nltk import word_tokenize
from wordcloud import STOPWORDS
from copy import deepcopy

import Utils.common_utils as utils
import Utils.connection_utils as glc

def tokenize_article(article):
	# Build list of stopwords to remove
	stopwords = set(STOPWORDS)
	# Tokenize the article using nltk
	tokens = word_tokenize(convert(article["content"]))
	# Remove all stop words from tokens
	for stop_word in stopwords:
		tokens = [token for token in tokens if not token.lower() == stop_word.lower()]

	# Return article tokens
	return tokens


# @glc.new_connection(primary = True, pass_to_function = True)
# def build_token_table(connection, cursor):
# 	glc.execute_db_command("""PREPARE token_insert AS INSERT INTO tokens (token) VALUES ($1) ON CONFLICT DO NOTHING""")
#
# 	tokens = []
# 	if os.path.isfile("tokens_backup"):
# 		print("Loading token list from backup...")
# 		with open("tokens_backup", "rb") as token_backup:
# 			tokens = pickle.load(token_backup)
# 	else:
# 		articles = glc.execute_db_query("""SELECT content FROM articles""")
#
# 		print("Building token list from articles...")
# 		# Store last display time
# 		lpd_time = datetime.datetime.now()
# 		# Tokenize all articles
# 		for i in range(0, len(articles)):
# 			# Tokenize article and add tokens to list
# 			tokens.extend(tokenize_article(articles[i]))
# 			# Remove duplicates from token list
# 			tokens = list(set(tokens))
# 			# Display only updates after at least 1 second has passed
# 			if (datetime.datetime.now() - lpd_time) > datetime.timedelta(seconds = 1):
# 				# Display progress bar
# 				utils.progress_bar(50, i+1, len(articles))
# 				# Update the last progress display time
# 				lpd_time = datetime.datetime.now()
# 		print()
#
# 		with open("tokens_backup", "wb") as token_backup:
# 			pickle.dump(tokens, token_backup)
#
# 	tokens = [(token,) for token in tokens]
# 	print("Writing %d tokens to database..." % len(tokens))
# 	cursor.executemany("""EXECUTE token_insert (%s)""", tokens)
#
# def build_nltk_training_list(articles):
# 	training_list = []
#
# 	all_words = []
# 	for article in articles:
# 		article_dict = {}
#
# 		tokens = tokenize_article(article)
# 		for token in tokens:
# 			article_dict[token] = True
#
# 		for word in all_words:
# 			if not word in article_dict.keys():
# 				article_dict[word] = False
#
# 		all_words.extend(tokens)
# 		all_words = list(set(all_words))
#
# 		training_list.append(article_dict)
#
# 	return training_list

def build_source_dict(articles, starting_dict):
	# Keep track of all the words that the source used
	all_source_words = []

	source_dict = deepcopy(starting_dict)
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

def build_class_dict(articles, sources, tokens, classifyFromTokens):
	class_dict = {}

	if classifyFromTokens == 0:

		real_dict = {}
		fake_dict = {}

		for token in tokens:
			real_dict[token["token"]] = 1 + token["realCount"]
			fake_dict[token["token"]] = 1 + token["fakeCount"]

		class_dict[0] = {"classifier": fake_dict}
		class_dict[1] = {"classifier": real_dict}

	else:
		starting_dict = {}

		for token in tokens:
			starting_dict[token["token"]] = 1

		for source in sources:

			articles_from_source = []
			for article in articles:
				if article["source_id"] == source["source_id"]:
					articles_from_source.append(article)
					articles.remove(article)

			source_dict, source_words = build_source_dict(articles_from_source, starting_dict)
			class_dict[source["source_id"]] = { "words": source_words, "classifier": source_dict }

	return class_dict

def classify_article(dictionaries, article, tokenNames):
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

		if token in tokenNames:
			# Add to the overall article score based on how often the token appears in the sources
			for source_id in dictionaries.keys():
				sums[source_id] = sums[source_id] + dictionaries[source_id]["classifier"][token]

	# Return the source with the minimum sum of words. The article is classified as coming from this source.
	return min(sums, key=sums.get), sums



def build_source(articles):
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

def classify(dictionaries, article):
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
			# Add to the overall article score based on how often the token appears in the sources
			for source_id in dictionaries.keys():
				if dictionaries[source_id].get(token) != None:
					sums[source_id] = sums[source_id] + dictionaries[source_id][token]
				else:
					sums[source_id] = sums[source_id] + 13


	# Return the source with the minimum sum of words. The article is classified as coming from this source.
	return min(sums, key=sums.get), sums

def convert(article):
	return article.encode('ascii', errors='ignore').decode('utf-8').replace("\ ", '')