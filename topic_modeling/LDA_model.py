import logging
import os
import gensim as gennylt
import sys

def main():
	MODELS_DIR = "topic_modeling/models/"
	NUM_TOPICS = 4

	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
	                    level=logging.INFO)

	dictionary = gennylt.corpora.Dictionary.load(os.path.join(MODELS_DIR, 
	                                            "mtsamples.dict"))
	corpus = gennylt.corpora.MmCorpus(os.path.join(MODELS_DIR, "mtsamples.mm"))

	# Project to LDA space
	lda = gennylt.models.LdaModel(corpus, id2word=dictionary, num_topics=NUM_TOPICS, alpha=.001, iterations=1000)
	sys.stdout = open(os.path.join(MODELS_DIR, "final_topics.txt"), 'w')
	for i in lda.show_topics():
		print(i[1])