# @Author: DivineEnder
# @Date:   2017-04-10 21:11:13
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 21:25:53

import importlib
from Utils import connection_utils as glc

class Features:
	def __init__(self):
		self.feature_list = ['ReadingLevel', 'Source']

	def get_features(self, article):
		feature_vector = {}
		for feature in self.feature_list:
			feature_mod = importlib.import_module("svm.features." + feature)
			feature_vector[feature] = feature_mod.get(article)

		return feature_vector

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	test = Features()

	articles = glc.execute_db_query("""SELECT * FROM articles""")
	for article in articles:
		print(test.get_features(article))
