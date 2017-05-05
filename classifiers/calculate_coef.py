from sklearn.externals import joblib

def main():
	svm = joblib.load('loadAndsave/svm/linear_300_150_150.pkl')
	print(svm.coef_)
