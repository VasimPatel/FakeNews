from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt

class SVM:
	def __init__(self, name='', description=''):
		self.name = name
		self.description = description
		self.clf = None
		self.data = []
		self.targets = []
		self.X_train = None
		self.X_test = None
		self.y_train = None
		self.y_test = None
		self.clf_set = 0
		self.clf_fit = 0

	def set_clf(self, kernel='linear'):
		self.clf = svm.SVC(kernel=kernel, C=1)
		self.clf_set = 1



	def fit_clf(self):
		if self.clf_set == 0:
			print("Support Vector Machine is not set")
			return

		self.clf.fit(self.X_train, self.y_train)
		self.clf_fit = 1

	def add_batch(self, head, target):
		self.data = head
		self.targets = target



	def add_data(self, head, target):
			self.data.append(head)
			self.targets.append(target)



	def split_data(self, size = 0.2, random = 0):
		if len(self.data) == 0 or len(self.targets) == 0:
			print("There is no data to split.")
			return

		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.data, self.targets, test_size = size, random_state = random)



	def eval_clf(self):
		if self.clf_fit == 0:
			print('Support Vector Machine is not fit')
			return

		y_pred = self.clf.predict(self.X_test)

		print("Classifier Accuracy: " + str(metrics.accuracy_score(self.y_test, y_pred)))



	def predict_article(self, article):
		if self.clf_fit == 0:
			print('Support Vector Machine is not fit')
			return

		return self.clf.predict(article)


