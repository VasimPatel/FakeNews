import Utils.settings as settings
settings.init()

from nltk import word_tokenize
import Utils.connection_utils as glc
import Utils.bayes_utils as bay

glc.new_connection(primary = True, pass_to_function = False)
def main():
	pol_articles = glc.execute_db_query("""SELECT content FROM articles WHERE source_id = 1 LIMIT 1000""")
	d = bay.classify_articles(pol_articles[0:-1])
	c = bay.classify_article(d,pol_articles[-1]['content'])
	print(c)

if __name__ == "__main__":
	main()
