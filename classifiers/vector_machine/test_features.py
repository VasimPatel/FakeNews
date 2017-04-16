from .features_set import Features
from Utils import connection_utils as glc
@glc.new_connection(primary = True, pass_to_function = False)
def main():
	test = Features()

	articles = glc.execute_db_query("""SELECT * FROM articles LIMIT 1""")
	for article in articles:
		print(test.get_features(article))