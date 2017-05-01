from classifiers.classifiers.support_vec_machine import SupportVectorMachine as SVM 

from classifiers.vector_machine import features_set 

import sys


def main():
	file = open('classifiers/articles/may_day.txt', 'r')

	content = ''

	for line in file:
		content = content + ' ' + line

	article = {'content': content}

	machine = SVM()
	F = features_set.Features()

	machine.set_bayes_classes(load=True)

	machine.construct_lda(load=True)

	machine.train_svm(load = True)

	article_features = F.get_features(article, lda = machine.lda,
											dictionary=machine.dictionary,
											corpus=machine.corpus,
											class_dict=machine.real_fake_word_dict)
	
	pred = machine.predict_svm([article_features])

	if pred == 0:
		print("\n--------------------------------\nThis article is Real!")
	else:
		print('\n--------------------------------\nThis article is Fake!')


#if __name__ == "__main__":
#	main()
	#main(sys.argv[1:])


