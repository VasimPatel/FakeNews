from topic_modeling import corpus
from classifiers.vector_machine.svm import SVM
from classifiers.vector_machine import features_set as features
from Utils import connection_utils as glc
import random
import sys
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.externals import joblib
import traceback
import Utils.bayes_utils as bayes

import json

class SupportVectorMachine:
	def __init__(self):
		self.lda = None
		self.dictionary = None
		self.corpus = None
		self.svm = SVM()
		self.articles = []
		self.Fobj = features.Features()
		self.features_collected = None
		self.real_fake_word_dict = None

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

	def set_bayes_classes(self, art_class, load = False):
		if load == True:
			self.real_fake_word_dict = joblib.load('word_dicts.pkl')
		else:
			self.real_fake_word_dict = {'real': bayes.build_source(art_class['real'])[0], 'fake': bayes.build_source(art_class['fake'])[0]}
			joblib.dump(self.real_fake_word_dict, 'word_dicts_1.pkl')





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
					feature_set = self.Fobj.get_features(each_article, lda=self.lda, dictionary=self.dictionary, corpus = self.corpus, class_dict = self.real_fake_word_dict)
					target = each_article['is_fake']
					if target == True:
						target = 1
					else:
						target = 0
					#target = random.randint(0,1)
					self.svm.add_data(feature_set, target)
				except Exception as e:
					sys.stdout.write("Training for this article failed. \r")
					print(e)
					pass
		self.features_collected = self.Fobj.get_features_collected()

	def train_svm(self, test_size=.25, load=False):
		try:
			if load == True:
				self.svm.clf = joblib.load('std.pkl')
				sys.stdout.write("Loaded SVM")
				self.svm.clf_fit = 1
				self.svm.clf_set = 1
			else:
				self.svm.split_data(test_size)
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
def query(query, variables = None):
	res = None
	if variables is None:
		res = glc.execute_db_query(query)
	else:
		res = glc.execute_db_query(query, variables)
	return res

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
	query_fake = "SELECT * FROM articles where is_fake=True order by random() LIMIT 500"
	query_real = "SELECT * From articles where is_fake=False order by random() limit 250"
	query_bp = "SELECT * From articles where is_fake is NULL order by random() limit 250"
	#query_na = "SELECT * From articles where source_id= order by random() limit 500"

	fake_a = query(query_fake)
	real_a = query(query_real)
	brei_po_a= query(query_bp)
	#na_a = query(query_na)

	articles = []
	articles_fake = fake_a
	articles_real = real_a + brei_po_a

	articles=articles_fake + articles_real

	source_dict = {'real': articles_real, 'fake': articles_fake}

	machine.set_bayes_classes(source_dict, load=True)
	#articles = articles + na_a

	random.shuffle(articles)
	sys.stdout.write("done queries...")
	sys.stdout.flush()

	machine.set_articles(articles)

	#construct our lda. comment out if you want
	machine.construct_lda(load=True,num_t=30)
	sys.stdout.write("done lda construction...\n")
	sys.stdout.flush()

	#get features for each article
	machine.get_features()
	sys.stdout.write("done feature collection...\n\n")
	sys.stdout.flush()

	#train svm
	machine.train_svm(test_size=.25, load=False)

	sys.stdout.write("done training...")
	sys.stdout.flush()

	#run svm
	#result = machine.run_svm()
	#sys.stdout.write("done running...")
	#sys.stdout.flush()

	#sys.stdout.write("\n\tClassifier Accuracy: " + str(result))
	#sys.stdout.flush()

	y_true, y_pred = machine.svm.y_test, machine.svm.clf.predict(machine.svm.X_test)
	sys.stdout.write(classification_report(y_true, y_pred))
	sys.stdout.flush()


	test_articles = []
	#article_ids = [322192, 321344, 320032, 318316, 322931, 314573, 335192, 333674, 334393, 318466, 315706, 323739, 321762, 319347, 319315, 335922, 320252, 319549, 323124, 336352, 338524, 342748, 349622, 343091, 346231, 342262, 338204, 344140, 341987, 348641, 222508, 171236, 33373, 183205, 307319, 288772, 225597, 253192, 260425, 69703]

	query_fake_t = "SELECT * FROM articles where is_fake=True order by random() LIMIT 100"
	query_real_t = "SELECT * From articles where is_fake=False order by random() limit 50"
	query_bp_t = "SELECT * From articles where is_fake is NULL order by random() limit 50"
	#db_q = "SELECT * FROM articles where article_id = any(%s)"
	#test_articles = query(db_q, (article_ids,))
	t_f = query(query_fake_t)
	t_r = query(query_real_t)
	t_bp = query(query_bp_t)
	test_articles = test_articles + t_f
	test_articles = test_articles + t_r
	test_articles = test_articles + t_bp
	total = 0
	correct=0
	total_f = 0
	total_r = 0
	correct_f = 0
	correct_r = 0
	sys.stdout.write("\ntesting against untrained data...\n")
	sys.stdout.flush()
	test_F = features.Features()
	i = 0
	t = len(test_articles)

	for each in test_articles:
		aid = each['article_id']
		ifk = each['is_fake']

		title = str(aid) + '_' + str(ifk) + '.txt'
		try:
			#test_F.set_clusters(machine.articles, machine.lda, machine.dictionary, machine.corpus)
			sys.stdout.write("getting features...")
			sys.stdout.flush()
			a_f = test_F.get_features(each, lda=machine.lda, dictionary=machine.dictionary, corpus=machine.corpus, class_dict= machine.real_fake_word_dict)
			sys.stdout.write("got features...")
			sys.stdout.flush()
			if each['is_fake'] == True:
				c = 1
			else:
				c = 0
			classif = machine.predict_svm([a_f])
			#print("\nclass: " + str(classif))
			#print("\nreal class: " + str(c))
			#print("\nlen article: " + str(len(each['content'])))
			#print('\nsource id: ' + str(each['source_id']))
			#print('\narticle id: ' + str(each['article_id']))
			# article_ids.append(each['article_id'])
			if classif == c:
				correct += 1
				if c == 1:
					correct_f += 1
				if c == 0:
					correct_r += 1
			else:
				try:
					json_str = json.dumps({'source_id': each['source_id'], 'article_id': each['article_id'], 'title': each['title'], 'content': each['content']})
					with open('incorrect/' + title, 'w') as f:
						json.dump(json_str, f)
						f.close()
				except Exception as e:
					print(e)
					pass

			if c == 1:
				total_f += 1
			if c == 0:
				total_r += 1

			if total_f != 0:
				f_acc = round(correct_f/total_f, 2)
			if total_f == 0:
				f_acc = 0
			if total_r != 0:
				r_acc = round(correct_r/total_r,2)
			if total_r == 0:
				r_acc = 0

			class_true.append(c)
			class_pred.append(classif)

			total += 1
			sys.stdout.write("Done...Test: " + str(total) + "/" + str(len(test_articles)) + ".....total accuracy: "  + str(round(correct/total,2)) + ", Fake accuracy: " + str(f_acc) + ", Real accuracy: " + str(r_acc)+ "\r")
			sys.stdout.flush()
		except Exception as e:
			print("Error!!: " + str(e))
			pass

	print("\n\tTotal Accuracy: " +  str(correct) + "/" + str(total) +": " + str(correct/total))
	print("\n\tFake Accuracy: " + str(correct_f) + "/" + str(total_f) + ": " + str(correct_f/total_f))
	print("\n\tReal Accuracy: " + str(correct_r) + "/" + str(total_r) + ": " + str(correct_r/total_r))
	# print(article_ids)

	#feature_names = machine.features_collected
	#print(machine.features_collected)
	#target_names = ['Fake', 'Real']
