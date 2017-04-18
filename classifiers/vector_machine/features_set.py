# @Author: DivineEnder
# @Date:   2017-04-10 21:11:13
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-10 21:25:53

import importlib
from Utils import connection_utils as glc
from topic_modeling import corpus as tm
from topic_modeling.corpus import lda, classify_article, get_topic_distr, compare_article, get_max_distr, cluster_articles
import random
class Features:
	def __init__(self):
		self.feature_list = ['ReadingLevel', 'Source', 'LexiDiversity']

	def get_features(self, article, lda = None, dictionary = None, corpus = None):
		feature_vector = []
		num_topics = 0
		for feature in self.feature_list:
			feature_mod = importlib.import_module("classifiers.features." + feature)
			feature_vector.append(feature_mod.get(article))

		if lda != None:
			topic_features = self.get_topicmod_features(article, lda, dictionary, corpus)
			for each_f in topic_features:
				feature_vector.append(each_f[1])
				num_topics += 1

		return feature_vector

	def get_topicmod_features(self, article, lda, dictionary, corpus):
		#get topic distribution for an article
		topic_dis, article_id = get_topic_distr(article, lda, dictionary, corpus)
		
		topic_features = []
		for each in topic_dis:
			topic = each[0]
			p = each[1] * random.randint(-10,10)

			topic_features.append([topic, p])

		return topic_features


			

