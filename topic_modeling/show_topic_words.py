from sklearn.externals import joblib
from topic_modeling import corpus

def main():
	name = 'large_test_10000_5000_5000'
	lda, dictionary, lda_corpus = corpus.lda(None, load=True, name=name)

	topics = lda.print_topics(num_topics=-1, num_words=10)

	for each in topics:
		print(each)


