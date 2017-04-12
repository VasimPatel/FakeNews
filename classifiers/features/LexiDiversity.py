import nltk

def get(article):
	return nltk.lexical_diversity(article['content'])
