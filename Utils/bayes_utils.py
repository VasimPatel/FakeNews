# @Author: DivineEnder
# @Date:   2017-03-29 14:47:11
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 17:53:00

import Utils.settings as settings
settings.init()

import math
import datetime
from psycopg2.extras import execute_values
from unidecode import unidecode
from nltk import word_tokenize
from wordcloud import STOPWORDS

import Utils.common_utils as utils
import Utils.connection_utils as glc

def tokenize_article(article):
	# Build list of stopwords to remove
	stopwords = set(STOPWORDS)
	# Tokenize the article using nltk
	tokens = word_tokenize(article["content"])
	# Remove all stop words from tokens
	for stop_word in stopwords:
		tokens = [token for token in tokens if not token.lower() == stop_word.lower()]

	# Return article tokens
	return tokens

def article_tokens_to_db(article):
	for token in tokenize_article(article):
		glc.execute_db_command("""INSERT INTO tokens (token) SELECT %s WHERE NOT EXISTS (SELECT token FROM tokens WHERE token = %s)""", (token, token))#ON CONFLICT ON CONSTRAINT tokens_token_key DO NOTHING""", (token,))

@glc.new_connection(primary = True, pass_to_function = True)
def build_token_table(connection, cursor):
	articles = glc.execute_db_query("""SELECT content FROM articles""")

	tokens = []

	print("Building token list from articles...")
	for i in range(0, len(articles)):
		tokens.extend(tokenize_article(articles[i]))
		tokens = list(set(tokens))
		utils.progress_bar(50, i+1, len(articles))
	print()

	print("Writing tokens to database...")
	tokens = [(token,) for token in tokens]
	execute_values(cursor, """INSERT INTO tokens (token) VALUES %s""", tokens)#ON CONFLICT DO NOTHING""", tokens)
	# 	glc.execute_db_values("""INSERT INTO tokens (token) SELECT %s WHERE NOT EXISTS (SELECT token FROM tokens WHERE token = %s)""", (token, token))
	# # Track total runtime
	# total_runtime = 0
	# # Set the last progress display time to the current time
	# lpd_time = datetime.datetime.now()
	# for i in range(0, len(articles)):
	# 	runtime = utils.time_it(tokenize_article, articles[i])
	# 	# Total runtime of whole process
	# 	total_runtime = total_runtime + runtime
	# 	# Display only updates after at least 1 second has passed
	# 	if (datetime.datetime.now() - lpd_time) > datetime.timedelta(seconds = 1):
	# 		# Display progress bar
	# 		utils.progress_bar(50, i+1, len(articles), cur_runtime = total_runtime, last_runtime = runtime)
	# 		# Update the last progress display time
	# 		lpd_time = datetime.datetime.now()

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

def classify_article(dictionaries, article, overfit = 0):
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
			elif not token_in_sources[source_id]:
				sums[source_id] = sums[source_id] + overfit

	# Teturn the source with the minimum sum of words. The article is classified as coming from this source.
	return min(sums, key=sums.get), sums
