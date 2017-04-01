# @Author: DivineEnder
# @Date:   2017-03-29 14:19:15
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-29 15:22:47

import Utils.settings as settings
settings.init()

import sys
from nltk import word_tokenize
import Utils.connection_utils as glc
import Utils.bayes_utils as bayes

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	articles1 = glc.execute_db_query("SELECT source_id, content FROM articles WHERE source_id=1 LIMIT 500")
	articles2 = glc.execute_db_query("SELECT source_id, content FROM articles WHERE source_id=2 LIMIT 500")

	sources = glc.execute_db_query("SELECT source_id FROM sources")
	class_dict = bayes.build_class_dict(articles1[50:] + articles2[50:], sources)


	test_articles = articles1[:50] + articles2[:50]

	total_tests=0
	total_correct=0

	for test_article in test_articles:
		test_id = test_article["source_id"]
		classified_id, sums = bayes.classify_article(class_dict, test_article)

		if int(test_id) == int(classified_id):
			total_correct += 1

		total_tests += 1

		sys.stdout.write("Correctly classified: " + str(total_correct) + "/" + str(total_tests) + '\r')
		sys.stdout.flush()

	p_c = total_correct / total_tests
	print("\nPercent correct: " + ("%.2f" % round(p_c*100,2)) + "%")





if __name__ == "__main__":
	main()
