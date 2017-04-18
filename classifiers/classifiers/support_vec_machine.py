from topic_modeling import corpus
from classifiers.vector_machine.svm import SVM
from classifiers.vector_machine import features_set as features
from Utils import connection_utils as glc
import random
class SupportVectorMachine:
	def __init__(self):
		self.lda = None
		self.dictionary = None
		self.corpus = None
		self.svm = SVM('linear')
		self.articles = []
		self.Fobj = features.Features()

	@glc.new_connection(primary = True, pass_to_function = False)
	def query_articles(self, query):
		#example query: "SELECT * FROM articles  WHERE created_at BETWEEN '2016-11-01 00:00:00' AND '2016-12-30 23:59:59' LIMIT 30"
		articles = glc.execute_db_query(query)
		for each_article in articles:
			#encode article text properly and clean
			self.articles.append(each_article)

	def construct_lda(self):
		if len(self.articles) == 0:
			print("No articles have been pulled!")
			return 0
		else:
			self.lda, self.dictionary, self.corpus = corpus.lda(self.articles)

	def get_features(self):
		if len(self.articles) == 0:
			print("No articles have been pulled or lda is not set!")
			return 0
		else:
			for each_article in self.articles:
				feature_set = self.Fobj.get_features(each_article, lda=self.lda, dictionary=self.dictionary, corpus = self.corpus)
				#target = each_article['classification']
				#head = []
				#for key,value in feature_set.items():
				#	head.append(value)

				target = random.randint(0,1)
				self.svm.add_data(feature_set, target)

	def train_svm(self, split):
		try:
			self.svm.split_data(random=split)
			self.svm.set_clf()
			self.svm.fit_clf()
		except Exception as e:
			print("Could not train svm: ")
			print("\tError: " + str(e))


	def run_svm(self):
		return self.svm.eval_clf()

	def predict_svm(self, article):
		#feature_set = self.Fobj.get_features(article, lda=self.lda, dictionary=self.dictionary, corpus=self.corpus)
		target = random.randint(0,1)
		feature_set = article
		result = self.svm.predict_article(feature_set)

		return result


def main():
	#instantiate machine
	machine = SupportVectorMachine()

	#add articles to machine
	query = "SELECT * FROM articles LIMIT 100"

	machine.query_articles(query)

	#machine.construct_lda()

	#get features for each article
	machine.get_features()

	#train svm
	machine.train_svm(4)

	#run svm
	result = machine.run_svm()

	print("\n\tClassifier Accuracy: " + str(result))

	#pred = [14, 2.0, 0.7098039215686274, 0.80799222695247019, 2.3343486625838541, 0.86400364373812371, 2.140210064453608, 0.22810606064047453, -0.32585958630164923, -0.21161127519319037, 0.0, -1.182755900009735]

	#print(machine.predict_svm(pred))

