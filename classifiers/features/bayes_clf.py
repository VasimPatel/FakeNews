import Utils.bayes_utils as bayes

def get(article, source_dict):
	c = bayes.classify(source_dict, article)[0]
	if c == 'real':
		return 0
	else:
		return 1