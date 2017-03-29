from nltk import word_tokenize
import Utils.connection_utils as glc
import Utils.bayes_utils as bay

def main():
	#example source dictionaries
	dict_1 = {"in":-.34, "hat": -.1, "eat": .05}
	dict_2 = {"the":-.34, "in": -.22, "said": .1}
	#set of sources with associated dictionary
	dictionaries = {"dict_1": dict_1, "dict_2": dict_2}
	#example test articles
	article_1 = "in eat eat"
	article_2 = "the in said"
	#classify article
	c = bay.classify_article(dictionaries, article_1)
	#print source that article was classified to
	print(c)

if __name__ == "__main__":
	main()
