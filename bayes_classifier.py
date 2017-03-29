# @Author: DivineEnder
# @Date:   2017-03-29 14:19:15
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-29 15:22:47

import Utils.settings as settings
settings.init()

from nltk import word_tokenize
import Utils.connection_utils as glc

glc.new_connection(primary = True, pass_to_function = False)
def main():
	pol_articles = glc.execute_db_query("""SELECT content FROM articles WHERE source_id = 1 LIMIT 1000""")




if __name__ == "__main__":
	main()
