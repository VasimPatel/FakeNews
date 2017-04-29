from topic_modeling import corpus
from classifiers.vector_machine.svm import SVM
from classifiers.vector_machine import features_set as features
from Utils import connection_utils as glc
import random
import sys
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib
import traceback
class SupportVectorMachine:
	def __init__(self):
		self.lda = None
		self.dictionary = None
		self.corpus = None
		self.svm = SVM()
		self.articles = []
		self.Fobj = features.Features()
		self.features_collected = None

	def set_articles(self, articles):
		self.articles = articles

	@glc.new_connection(primary = True, pass_to_function = False)
	def query_articles(self, query):
		#example query: "SELECT * FROM articles  WHERE created_at BETWEEN '2016-11-01 00:00:00' AND '2016-12-30 23:59:59' LIMIT 30"
		articles = glc.execute_db_query(query)
		for each_article in articles:
			#encode article text properly and clean
			self.articles.append(each_article)

	def construct_lda(self, load=False, num_t=10):
		if len(self.articles) == 0:
			print("No articles have been pulled!")
			return 0
		else:
			self.lda, self.dictionary, self.corpus = corpus.lda(self.articles, load=load, num_t=num_t)

	def get_features(self):
		if self.lda != None:
			self.Fobj.set_clusters(self.articles, self.lda, self.dictionary, self.corpus)
		if len(self.articles) == 0:
			print("No articles have been pulled or lda is not set!")
			return 0
		else:
			i = 0
			for each_article in self.articles:
				progress = i / len(self.articles)
				i = i + 1
				sys.stdout.write("Feature Collection in Progress: {}%   \r".format(round(progress*100)) )
				sys.stdout.flush()
				try:
					feature_set = self.Fobj.get_features(each_article, lda=self.lda, dictionary=self.dictionary, corpus = self.corpus)
					target = each_article['is_fake']
					if target == True:
						target = 1
					else:
						target = 0
					#target = random.randint(0,1)
					self.svm.add_data(feature_set, target)
				except Exception as e:
					sys.stdout.write("Training for this article failed. \r")
					pass
		self.features_collected = self.Fobj.get_features_collected()

	def train_svm(self, split):
		try:
			self.svm.split_data(random=split)
			self.svm.set_clf()
			self.svm.fit_clf()
		except Exception as e:
			print("Could not train svm: ")
			print("\tError: " + str(e))
			traceback.print_exc()


	def run_svm(self):
		return self.svm.eval_clf()

	def predict_svm(self, article):
		feature_set = article
		result = self.svm.predict_article(feature_set)

		return result

@glc.new_connection(primary = True, pass_to_function = False)
def query(query):
	return glc.execute_db_query(query)

def preprocess_data(articles):
	for each_article in articles:
		#print(type(each_article['content']))
		if each_article == None:
			articles.remove(each_article)
			print("removed article because it was null!")
		elif len(str(each_article['content'])) == 1:
			articles.remove(each_article)
			print("removed article because it had no content! Class: " + str(each_article['is_fake']))
		elif len(str(each_article['source_id'])) == None:
			articles.remove(each_article)
			print("removed article because it had no source! Class: " + str(each_article['is_fake']))
		else:
			pass
	return articles

def main():
	class_true = []
	class_pred = []
	#instantiate machine
	machine = SupportVectorMachine()

	#add articles to machine
	query_fake = "SELECT * FROM articles where is_fake=True order by random() LIMIT 1000"
	query_real = "SELECT * From articles where source_id=22236 order by random() limit 1000"

	fake_a = query(query_fake)
	real_a = query(query_real)

	fake_a = random.sample(fake_a, 100)
	real_a = random.sample(real_a, 100)

	articles = []
	articles = articles + fake_a
	articles = articles + real_a

	random.shuffle(articles)

	sys.stdout.write("done queries...")
	sys.stdout.flush()

	machine.set_articles(articles[:700])

	#construct our lda. comment out if you want
	machine.construct_lda(load=True,num_t=45)
	sys.stdout.write("done lda construction...\n")
	sys.stdout.flush()

	#get features for each article
	machine.get_features()
	sys.stdout.write("done feature collection...\n\n")
	sys.stdout.flush()

	#train svm
	machine.train_svm(10)
	sys.stdout.write("done training...")
	sys.stdout.flush()

	#run svm
	#result = machine.run_svm()
	#sys.stdout.write("done running...")
	#sys.stdout.flush()

	#sys.stdout.write("\n\tClassifier Accuracy: " + str(result))
	#sys.stdout.flush()

	y_true, y_pred = machine.svm.y_test, machine.svm.clf.predict(machine.svm.X_test)
	print(classification_report(y_true, y_pred))

'''

	test_articles = articles[700:750]
	total = 0
	correct=0
	total_f = 0
	total_r = 0
	correct_f = 0
	correct_r = 0
	sys.stdout.write("\ntesting against untrained data...\n")
	sys.stdout.flush()
	test_F = features.Features()
	for each in test_articles:
		try:
			test_F.set_clusters(machine.articles, machine.lda, machine.dictionary, machine.corpus)
			sys.stdout.write("getting features...")
			sys.stdout.flush()
			a_f = test_F.get_features(each, lda=machine.lda, dictionary=machine.dictionary, corpus=machine.corpus)
			sys.stdout.write("got features...")
			sys.stdout.flush()
			if each['is_fake'] == True:
				c = 1
			else:
				c = 0
			classif = machine.predict_svm([a_f])
			if classif == c:
				correct += 1
				if c == 1:
					correct_f += 1
				if c == 0:
					correct_r += 1
			if c == 1:
				total_f += 1
			if c == 0:
				total_r += 1

			class_true.append(c)
			class_pred.append(classif)

			total += 1
			sys.stdout.write("Done...Test: " + str(total) + "/" + str(len(test_articles)) + "\n")
			sys.stdout.flush()
		except Exception as e:
			print("Error!!: " + str(e))
			pass

	print("\n\tTotal Accuracy: " +  str(correct) + "/" + str(total) +": " + str(correct/total))
	print("\n\tFake Accuracy: " + str(correct_f) + "/" + str(total_f) + ": " + str(correct_f/total_f))
	print("\n\tReal Accuracy: " + str(correct_r) + "/" + str(total_r) + ": " + str(correct_r/total_r))

	feature_names = machine.features_collected
	print(machine.features_collected)
	target_names = ['Fake', 'Real']

'''
