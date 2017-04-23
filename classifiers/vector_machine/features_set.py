# @Author: DivineEnder
# @Date:   2017-04-10 21:11:13
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 21:25:53

import importlib
from Utils import connection_utils as glc
from topic_modeling import corpus as tm
from topic_modeling.corpus import lda, classify_article, get_topic_distr, compare_article, get_max_distr, cluster_articles, compare_article
import random
class Features:
	def __init__(self):
		#######
		# To add feature: 
		# 1. create file in classifiers/features which collects the feature for an article object and returns
		# 2. add filename to self.feature_list
		# 3. you are good to go
		#######
		self.feature_list = ['ReadingLevel','LexiDiversity']
		self.num_topics = 0
		self.clusters = None

	def get_features(self, article, lda = None, dictionary = None, corpus = None):
		feature_vector = []
		num_topics = 0
		for feature in self.feature_list:
			feature_mod = importlib.import_module("classifiers.features." + feature)
			feature_vector.append(feature_mod.get(article))

		if lda != None:
			#----------------------------------------------------------------------------
			#collect topic distribution

			topic_distr = self.get_topicmod_features(article, lda, dictionary, corpus)
			i = 0
			for each_f in topic_distr:
				feature_vector.append(each_f[1])
				num_topics += 1
			self.num_topics = num_topics

			#----------------------------------------------------------------------------
			#collect similar articles

			#convert and classify article content to lda space
			vec_lda = classify_article(article, lda, dictionary, corpus)

			#get sorted list of similar articles
			sims = compare_article(vec_lda, lda, dictionary, corpus, name='test')

			for each in sims[:20]:
				feature_vector.append(each[0])
				feature_vector.append(each[1])


			#----------------------------------------------------------------------------
			#collect number of articles in most probable topic
			#get most likely topic assigned to article
			max_distr = get_max_distr(topic_distr)
			num_articles = len(self.clusters[max_distr[0]])
			feature_vector.append(num_articles)
			feature_vector.append(max_distr[1])
		
		return feature_vector

	def set_clusters(self, articles, lda, dictionary, corpus):
		self.clusters = cluster_articles(articles, lda, dictionary, corpus)

	def get_topicmod_features(self, article, lda, dictionary, corpus):
		#get topic distribution for an article
		topic_dis, article_id = get_topic_distr(article, lda, dictionary, corpus)

		return topic_dis

	def get_features_collected(self):
		f_c = self.feature_list
		for i in range(0,self.num_topics):
			f_c.append("Topic_" + str(i))
		
		return f_c

			

