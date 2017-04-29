from .svm import SVM
from sklearn.datasets import load_iris
def main():
	iris = load_iris()
	head = iris.data
	target = iris.target
	print(type(head))
	print(target)

	machine = SVM('linear')
	machine.add_batch(head, target)
	machine.split_data(random=4)
	machine.set_clf()
	machine.fit_clf()

	machine.eval_clf()
