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

	def construct_lda(self, load=False, num_t=10, name=None):
		if len(self.articles) == 0 and load == False:
			print("No articles have been pulled!")
			return 0
		else:
			self.lda, self.dictionary, self.corpus = corpus.lda(self.articles, load=load, num_t=num_t, name=name)

	def set_bayes_classes(self, source_dict=None, load = False, name=None):
		if load == True:
			self.real_fake_word_dict = joblib.load('loadAndsave/bayes_dict/' + name  + ".pkl")
		else:
			self.real_fake_word_dict = {'real': bayes.build_source(source_dict['real'])[0], 'fake': bayes.build_source(source_dict['fake'])[0]}
			joblib.dump(self.real_fake_word_dict, 'loadAndsave/bayes_dict/' + name + ".pkl")

	def get_features(self):
		#if self.lda != None:
			#self.Fobj.set_clusters(self.articles, self.lda, self.dictionary, self.corpus)
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

	def train_svm(self, test_size=.25, load=False, name=None):
		try:
			if load == True:
				self.svm.clf = joblib.load('loadAndsave/svm/' + name  + ".pkl")
				sys.stdout.write("Loaded SVM")
				self.svm.clf_fit = 1
				self.svm.clf_set = 1
			else:
				#self.svm.split_data(test_size)
				self.svm.set_clf()
				self.svm.fit_clf(name=name)
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


def main(name_scheme, load_lda, load_bayes, load_svm, run_tests, num_articles, num_articles_test, lda_only, bayes_only):
	#instantiate machine
	machine = SupportVectorMachine()

	load_lda = int(load_lda)
	load_svm = int(load_svm)
	load_bayes = int(load_bayes)
	run_tests = int(run_tests)
	num_articles = int(num_articles)
	num_articles_test = int(num_articles_test)
	lda_only = int(lda_only)
	bayes_only = int(bayes_only)

	if load_svm is 0:
		#add articles to machine
		query_fake = "SELECT * FROM articles where is_fake=True order by random() LIMIT {}".format(round(num_articles/2)+num_articles_test)
		query_real = "SELECT * From articles where is_fake=False order by random() limit {}".format(round(num_articles/4)+num_articles_test/2)
		query_bp = "SELECT * From articles where is_fake is NULL order by random() limit {}".format(round(num_articles/4)+num_articles_test/2)

		sys.stdout.write(str(num_articles_test))
		sys.stdout.write("\n"+str(num_articles))
		#uncoment when not loading svm
		fake = query(query_fake)

		fake_a = fake[:-num_articles_test]
		test_fake_a = fake[round(num_articles/2):]


		real = query(query_real)

		real_a = real[:-round(num_articles_test/2)]
		test_real_a = real[round(num_articles/4):]


		brei= query(query_bp)

		brei_a = brei[:-round(num_articles_test/2)]
		test_brei_a = brei[round(num_articles/4):]
	

		articles = []
		#uncomment when not loading svm

		articles_fake = fake_a
		articles_real = real_a + brei_a


		#uncomment when not loading svm

		articles=articles_fake + articles_real
		test_articles = test_fake_a + test_real_a + test_brei_a

		sys.stdout.write("Length of training articles: " + str(len(articles)))
		sys.stdout.write("\nLength of testing articles: " + str(len(test_articles)))
		sys.stdout.flush()
		#shuffle articles for robustness
		random.shuffle(articles)
		#sys.stdout.write("done queries...\n")
		#sys.stdout.flush()

		#set articles for machine to get features of
		machine.set_articles(articles)


		#uncomment when not loading svm
		source_dict = {'real': articles_real, 'fake': articles_fake}


	if load_bayes is 1 and lda_only is not 1:
		#comment out when not loading
		machine.set_bayes_classes(load=True, name=name_scheme)

	if load_bayes is 0 and lda_only is not 1:
		#uncomment when not loading svm
		machine.set_bayes_classes(source_dict, load=False, name=name_scheme)

	sys.stdout.write("done bayes dictionary construction...\n")
	sys.stdout.flush()

	if load_lda is 1 and bayes_only is not 1:
		#comment out when not loading
		machine.construct_lda(load=True,num_t=30, name=name_scheme)

	if load_lda is 0 and bayes_only is not 1:
		#uncomment when not loading
		machine.construct_lda(load=False,num_t=30, name=name_scheme)

	sys.stdout.write("done lda construction...\n")
	sys.stdout.flush()


	if load_svm is 0:
		#get features for each article
		#uncomment when not loading svm
		if bayes_only is 1:
			machine.lda = None
		if lda_only is 1:
			machine.Fobj.feature_list = []

		machine.get_features()
		sys.stdout.write("done feature collection...\n\n")
		sys.stdout.flush()

		#uncomment when not loading svm
		machine.train_svm(test_size=0, load=False, name=name_scheme)

		sys.stdout.write("done training...")
		sys.stdout.flush()

	if load_svm is 1:
		#train svm 
		#comment when not loading
		machine.train_svm(load=True, name=name_scheme)

		query_fake = "SELECT * FROM articles where is_fake=True order by random() LIMIT {}".format(num_articles_test)
		query_real = "SELECT * From articles where is_fake=False order by random() limit {}".format(num_articles_test/2)
		query_bp = "SELECT * From articles where is_fake is NULL order by random() limit {}".format(num_articles_test/2)

		f_a = query(query_fake)
		r_a = query(query_real)
		b_a = query(query_bp)

		test_articles = f_a+r_a+b_a



	#if load_svm is 0:
	if load_svm is 5:
		#get prediction stats
		#uncomment when not loading svm
	
		y_true, y_pred = machine.svm.y_test, machine.svm.clf.predict(machine.svm.X_test)
		sys.stdout.write(classification_report(y_true, y_pred))
		sys.stdout.flush()


	if run_tests is 1:

		result_file = open('results/results_lot_' + str(lda_only) + str(bayes_only) + '.txt', 'a+')
		#test_articles = []
		#article_ids = [322192, 321344, 320032, 318316, 322931, 314573, 335192, 333674, 334393, 318466, 315706, 323739, 321762, 319347, 319315, 335922, 320252, 319549, 323124, 336352, 338524, 342748, 349622, 343091, 346231, 342262, 338204, 344140, 341987, 348641, 222508, 171236, 33373, 183205, 307319, 288772, 225597, 253192, 260425, 69703]

		#query_fake_t = "SELECT * FROM articles where is_fake=True order by random() LIMIT {}".format(num_articles_test)
		#query_real_t = "SELECT * From articles where is_fake=False order by random() limit {}".format(round(num_articles_test/2))
		#query_bp_t = "SELECT * From articles where is_fake is NULL order by random() limit {}".format(round(num_articles_test/2))
		#db_q = "SELECT * FROM articles where article_id = any(%s)"
		#test_articles = query(db_q, (article_ids,))
		#t_f = query(query_fake_t)
		#t_r = query(query_real_t)
		#t_bp = query(query_bp_t)
		#test_articles = test_articles + t_f
		#test_articles = test_articles + t_r
		#test_articles = test_articles + t_bp
		total = 0
		correct=0
		total_f = 0
		total_r = 0
		correct_f = 0
		correct_r = 0
		sys.stdout.write("\ntesting against untrained data...\n")
		sys.stdout.flush()
		test_F = features.Features()
		if lda_only is 1:
			test_F.feature_list = []

		i = 0
		t = len(test_articles)
		random.shuffle(test_articles)
		for each in test_articles:
			aid = each['article_id']
			ifk = each['is_fake']

			title = str(aid) + '_' + str(ifk) + '.txt'
			try:
				#test_F.set_clusters(machine.articles, machine.lda, machine.dictionary, machine.corpus)
				sys.stdout.write("getting features...")
				sys.stdout.flush()
				a_f = test_F.get_features(each, lda=machine.lda, dictionary=machine.dictionary, corpus=machine.corpus, class_dict= machine.real_fake_word_dict)
				#print("Features: ")
				#print(a_f)
				sys.stdout.write("got features...")
				sys.stdout.flush()
				if each['is_fake'] == True:
					c = 1
				else:
					c = 0
				#classif = a_f[0]
				classif = machine.predict_svm([a_f])
				if classif == c:
					correct += 1
					if c == 1:
						correct_f += 1
					if c == 0:
						correct_r += 1
				#else:
					#try:
						#json_str = json.dumps({'source_id': each['source_id'], 'article_id': each['article_id'], 'title': each['title'], 'content': each['content']})
						#with open('incorrect/' + title, 'w') as f:
						#	json.dump(json_str, f)
						#	f.close()
					#except Exception as e:
					#	print(e)
					#	pass

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

				total += 1
				sys.stdout.write("Done...Test: " + str(total) + "/" + str(len(test_articles)) + ".....total accuracy: "  + str(round(correct/total,2)) + ", Fake accuracy: " + str(f_acc) + ", Real accuracy: " + str(r_acc)+ "\r")
				sys.stdout.flush()
			except Exception as e:
				#print("Error!!: " + str(e))
				pass

		#sys.stdout.write("Done...Test: " + str(total) + "/" + str(len(test_articles)) + ".....total accuracy: "  + str(round(correct/total,2)) + ", Fake accuracy: " + str(f_acc) + ", Real accuracy: " + str(r_acc)+ "\r")
		sys.stdout.write(str(round(correct/total,2)) + ", " + str(f_acc) + ", " + str(r_acc)+ "\n")
		sys.stdout.flush()

		out_str = str(num_articles) + ',' + str(round(correct/total,2)) + "," + str(f_acc) + "," + str(r_acc)+ "\n"
		result_file.write(out_str)
		#print("\n\tTotal Accuracy: " +  str(correct) + "/" + str(total) +": " + str(correct/total))
		#print("\n\tFake Accuracy: " + str(correct_f) + "/" + str(total_f) + ": " + str(correct_f/total_f))
		#print("\n\tReal Accuracy: " + str(correct_r) + "/" + str(total_r) + ": " + str(correct_r/total_r))