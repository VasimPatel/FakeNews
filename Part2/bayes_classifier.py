# @Author: DivineEnder
# @Date:   2017-03-29 14:19:15
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-04 17:51:27

import Utils.settings as settings
settings.init()

import sys
import nltk
from random import random
from random import randint
import Utils.connection_utils as glc
import Utils.bayes_utils as bayes

@glc.new_connection(primary = True, pass_to_function = False)
def get_data(num_tests, classifyFromTokens, test_variance = 0, num_sources = None, num_articles = None):
	# Get specified number of sources from database (gets all if no number sources passed in)
	sources = None
	if num_sources is None:
		sources = glc.execute_db_query("SELECT source_id, name FROM sources")
	else:
		sources = glc.execute_db_query("SELECT source_id, name FROM sources LIMIT %s", (num_sources,))
	print("Sources query completed. Retrieved %d sources from database." % len(sources))

	# Build a dictionary of source_id keys which contain lists of articles from that source as their values
	source_article_dict = {}
	for source in sources:
		source_article_dict[source["source_id"]] = None
		if num_articles is None:
			source_article_dict[source["source_id"]] = glc.execute_db_query("SELECT article_id, source_id, content FROM articles WHERE source_id=%s", (source["source_id"],))
		else:
			source_article_dict[source["source_id"]] = glc.execute_db_query("SELECT article_id, source_id, content FROM articles WHERE source_id=%s LIMIT %s", (source["source_id"], num_articles))

		print("%s query completed! Retrived %d articles from database." % (source["name"], len(source_article_dict[source["source_id"]])))

	#Build a dictionary of all of the tokens in the database
	if classifyFromTokens == 0:
		tokens = glc.execute_db_query("SELECT token, realCount, fakeCount FROM tokens")
	else:
		tokens = glc.execute_db_query("SELECT token FROM tokens")

	print("Tokens query completed! Retrived %d tokens from database." % (len(tokens)))

	print("All queries completed, data fetched!")

	if classifyFromTokens == 0:
		training_articles = []
		test_articles = []
		for i in range(0, len(sources)):
			test_articles.extend(source_article_dict[sources[i]["source_id"]])

		source_id = [0, 1]
		name = ["fake", "real"]
		sources = {"source_id": source_id, "name": name}
	else:
		# Get the even distribution percent that would happen with this many sources (ex. 3 sources this would be .33)
		even_split_percent = float(1) / len(sources)
		# Get the range on the bounded percentage split (ex. .33 with a variance of 10% would have a range of .033)
		bound_range = even_split_percent * test_variance
		# Create a list of how each of the sources are going to be split
		source_splits = [even_split_percent] * len(sources)
		# Randomly split sources (leave out last one as it is calculated using the previous source distributions)
		for i in range(0, len(sources) - 1):
			# Minimum bound for number of tests can pick
			min_bound = int(num_tests * (even_split_percent - bound_range))
			# Maximum bound for number of tests can pick
			max_bound = int(num_tests * (even_split_percent + bound_range))

			# Pick a number inbetween these bounds
			source_splits[i] = randint(min_bound, max_bound)
			# Claculates the last distribution based on previous distributions and how much is left
			source_splits[-1] = num_tests - sum(source_splits[:-1])

			print("\nTest data contains: ")
			# Create training and test article lists using previously generated list splits
			training_articles = []
			test_articles = []
			for i in range(0, len(sources)):
				training_articles.extend(source_article_dict[sources[i]["source_id"]][source_splits[i]:])
				test_articles.extend(source_article_dict[sources[i]["source_id"]][:source_splits[i]])

				print("\t%d %s articles" % (source_splits[i], sources[i]["name"]))

	return sources, training_articles, test_articles, tokens

# NLTK STUFF
# NOTE:: This function DOES NOT WORK. Python runs out of memory before it can actually create the training list needed for NLTK (this was tested only pulling 20 articles total)
# def nltk_bayes():
# 	print("\n" + ("-" * 10) + "Querying data" + ("-" * 10))
# 	sources, training_articles, test_articles = get_data(100, test_variance = .30, num_articles = 1000)
# 	print("\n" + ("-" * 10) + ("-" * len("Querying data")) + ("-" * 10))
#
# 	print("Building training list.")
# 	nltk_training_list = bayes.build_nltk_training_list(training_articles)
# 	print("Building NLTK classifier from built training list.")
# 	classifier = nltk.NaiveBayesClassifier(nltk_training_list)
# 	print("Classifier has been built.")
# 	classifier.show_most_informative_features()

def main():

	#0 for using tokens table to classify against entire database, 1 for building a classifier from sources
	classifyFromTokens = 1
	realNews = [1, 2, 22236]

	# Get data from database for classification
	print("\n" + ("-" * 10) + "Querying data" + ("-" * 10))
	sources, training_articles, test_articles, tokens = get_data(500, classifyFromTokens, test_variance = .30, num_articles = 5000)
	print("\n" + ("-" * 10) + ("-" * len("Querying data")) + ("-" * 10))

	#Build the network for classification
	print("\n" + ("-" * 10) + "Building classifier" + ("-" * 10))
	class_dict = bayes.build_class_dict(training_articles, sources, tokens, classifyFromTokens)
	print("Classifier has been built successfully!")
	print("\n" + ("-" * 10) + ("-" * len("Building classifier")) + ("-" * 10))

	#Build a list of tokens from the dictionary
	tokenNames = [token["token"] for token in tokens]

	print("\n" + ("-"*10) + "Results" + ("-"*10))

	# Create a dictionary for storing statistics for the classification results
	source_stats = { "overall": { "total": 0, "correct": 0 } }
	for source in sources:
		source_stats[source["source_id"]] = { "total": 0, "correct": 0 }

	# Classify the articles and print stats
	for test_article in test_articles:

		if classifyFromTokens == 0:
			if test_article["source_id"] in realNews:
				test_source_id = 1
			else:
				test_source_id = 0
		else:
			test_source_id = test_article["source_id"]

		# Classify the article
		classified_id, sums = bayes.classify_article(class_dict, test_article, tokenNames)

		# Count number of correct (overall and by source)
		if int(test_source_id) == int(classified_id):
			source_stats["overall"]["correct"] = source_stats["overall"]["correct"] + 1
			source_stats[test_source_id]["correct"] = source_stats[test_source_id]["correct"] + 1

		# Increase overall total and source total
		source_stats[test_source_id]["total"] = source_stats[test_source_id]["total"] + 1
		source_stats["overall"]["total"] = source_stats["overall"]["total"] + 1

		# Write progress of classification to screen
		sys.stdout.write("Correctly Classified: " + str(source_stats["overall"]["correct"]) + "/" + str(source_stats["overall"]["total"]) + '\r')
		sys.stdout.flush()

	print("\nClassification of : ")
	# Print out source related statistics
	for source in sources:
		source_correct = source_stats[source["source_id"]]["correct"]
		source_total = source_stats[source["source_id"]]["total"]
		source_percent = source_correct / source_total
		print("\t%s had an accuracy was %.2f%% (%d/%d)" % (source["name"], round(source_percent * 100, 2), source_correct, source_total))

	print("\nOverall classification accuracy was %.2f%% (%d/%d)" % (round((source_stats["overall"]["correct"] / source_stats["overall"]["total"]) * 100, 2), source_stats["overall"]["correct"], source_stats["overall"]["total"]))

if __name__ == "__main__":
	main()
	# nltk_bayes()
