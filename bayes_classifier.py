# @Author: DivineEnder
# @Date:   2017-03-29 14:19:15
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-29 15:22:47

import Utils.settings as settings
settings.init()

from nltk import word_tokenize
import Utils.connection_utils as glc
import Utils.bayes_utils as bayes

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	articles = glc.execute_db_query("SELECT source_id, content FROM articles LIMIT 1000")
	sources = glc.execute_db_query("SELECT source_id FROM sources")
	# pol_articles = glc.execute_db_query("""SELECT content FROM articles WHERE source_id = 1 LIMIT 1000""")

	class_dict = bayes.build_class_dict(articles, sources)

	#print(class_dict[1].items())





if __name__ == "__main__":
	main()
