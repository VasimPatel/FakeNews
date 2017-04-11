import importlib
import Utils
class Features:
	def __init__(self):
		self.feature_list = ['ReadingLevel', 'Source']

	def get_features(self, article):
		feature_vector = {}
		for feature in self.feature_list:
			feature_mod = importlib.import_module("svm.features." + feature)
			self.feature_vector[feature] = feature_mod.get(article)

		return self.feature_vector

def main():
	test = Features("article")
	print(test.get_features())