from sklearn.externals import joblib
from topic_modeling import corpus
import sys

def main():
	out_file = open('topic_modeling/view_topics/large_test_10000_5000_5000.csv', 'w')
	name = 'large_test_10000_5000_5000'
	lda, dictionary, lda_corpus = corpus.lda(None, load=True, name=name)

	topics = lda.print_topics(num_topics=-1, num_words=10)
	
	for each_topic in topics:
		t_n = str(each_topic[0])

		sys.stdout.write("\nTopic {0:<5}".format(t_n+":"))
		out_file.write("\n{},".format(t_n))
		word_p_list = each_topic[1].split("+")
		for each in word_p_list:
			weight = each.split("*")[0]
			word = each.split("*")[1].replace('"', '')
			sys.stdout.write("{0}, {1:<13}".format(weight,word))
			out_file.write("{0}, {1},".format(weight,word))

