# @Author: DivineEnder
# @Date:   2017-03-29 14:19:15
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-29 15:22:47

import Utils.settings as settings
settings.init()

import sys
from nltk import word_tokenize
from random import randint
import Utils.connection_utils as glc
import Utils.bayes_utils as bayes

@glc.new_connection(primary = True, pass_to_function = False)
def main():

	numTests = 1000
	minPercentBound = .35

	sources = glc.execute_db_query("SELECT source_id FROM sources")
	print("Sources query completed!")

	articles1 = glc.execute_db_query("SELECT article_id, source_id, content FROM articles WHERE source_id=1") #LIMIT 50000")
	print("Politico query completed!")

	articles2 = glc.execute_db_query("SELECT article_id, source_id, content FROM articles WHERE source_id=2") #LIMIT 50000")
	print("Breitbart query completed!")

	print("All queries completed, data fetched!")

	#Get a random number 1-100
	splitNum = randint(int(numTests * minPercentBound), numTests - int(numTests * minPercentBound))

	#Build the network for classification
	class_dict = bayes.build_class_dict(articles1[splitNum:] + articles2[(numTests -  splitNum):], sources)
	print("Classifier has been built successfully!")

	test_articles = articles1[:splitNum] + articles2[:(numTests - splitNum)]

	#Print number of articles from each source
	print("\nNumber of Articles")
	print("Politico = %d" % splitNum)
	print("Breitbart = %d" % (numTests - splitNum))


	print("\nResults")

	#Classify the articles
	total_tests=0
	total_correct=0
	polCorrect = 0

	for test_article in test_articles:
		test_id = test_article["source_id"]
		classified_id, sums = bayes.classify_article(class_dict, test_article)

		if int(test_id) == int(classified_id):
			if int(test_id) == 1:
				polCorrect = polCorrect + 1
			total_correct += 1


		total_tests += 1

		sys.stdout.write("Correctly Classified: " + str(total_correct) + "/" + str(total_tests) + '\r')
		sys.stdout.flush()

	p_c = total_correct / total_tests
	p_c_p = polCorrect / splitNum
	p_c_b = (total_correct - polCorrect) / (numTests - splitNum)

	print("\nPolitico Correctly Classified: %d/%d" %(polCorrect, splitNum))
	print("Breitbart Correctly Classified: %d/%d" %(total_correct - polCorrect, numTests - splitNum))

	print("\nPolitico Percent Correct: " + ("%.2f" % round(p_c_p*100,2)) + "%")
	print("Breitbart Percent Correct: " + ("%.2f" % round(p_c_b*100,2)) + "%")
	print("\nPercent Correct: " + ("%.2f" % round(p_c*100,2)) + "%")





if __name__ == "__main__":
	main()
