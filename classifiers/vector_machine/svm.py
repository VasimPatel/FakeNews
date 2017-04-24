from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import sys


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
		# Set the parameters by cross-validation
		tuned_parameters = [
  			{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
  			{'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
 			]
		self.clf = GridSearchCV(svm.SVC(C=1), tuned_parameters, cv=5)
		self.clf_set = 1



	def fit_clf(self):
		if self.clf_set == 0:
			print("Support Vector Machine is not set")
			return

		sys.stdout.write("fitting svm...")
		sys.stdout.flush()

		self.clf.fit(self.X_train, self.y_train)
		#print("Best SVM Params: " + self.clf.best_params_)
		self.clf_fit = 1


	def add_batch(self, head, target):
		self.data = head
		self.targets = target



	def add_data(self, head, target):
			self.data.append(head)
			self.targets.append(target)



	def split_data(self, size = 0.2, random = 0):
		self.data = preprocessing.scale(self.data)
		if len(self.data) == 0 or len(self.targets) == 0:
			print("There is no data to split.")
			return
		head = np.array(self.data)
		target = np.array(self.targets)
		self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(head, target, test_size = size, random_state = random)



	def eval_clf(self):
		if self.clf_fit == 0:
			print('Support Vector Machine is not fit')
			return

		y_pred = self.clf.predict(self.X_test)

		return metrics.accuracy_score(self.y_test, y_pred)



	def predict_article(self, head):
		if self.clf_fit == 0:
			print('Support Vector Machine is not fit')
			return

		result = self.clf.predict(head)

		return result[0]