from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import gensim

def lda(articles, nameScheme = "test"):
	tokenizer = RegexpTokenizer(r'\w+')

	# create English stop words list
	en_stop = stopwords.words('english')

	# Create p_stemmer of class PorterStemmer
	p_stemmer = PorterStemmer()
	    

	# compile sample documents into a list
	doc_set = articles

	# list for tokenized documents in loop
	texts = []

	# loop through document list
	for i in doc_set:
	    
	    # clean and tokenize document string
	    raw = i.lower()
	    tokens = tokenizer.tokenize(raw)

	    # remove stop words from tokens
	    stopped_tokens = [i for i in tokens if not i in en_stop]
	    
	    # stem tokens
	    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
	    
	    # add tokens to list
	    texts.append(stemmed_tokens)

	# turn our tokenized documents into a id <-> term dictionary
	dictionary = corpora.Dictionary(texts)

	    
	# convert tokenized documents into a document-term matrix
	corpus = [dictionary.doc2bow(text) for text in texts]

	# generate LDA model
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=9, id2word = dictionary, alpha=2, passes=20)

	#save dictionary corpus and ldamodel to be used later
	dictionary.save(nameScheme + "_dictionary.dict")

	corpora.MmCorpus.serialize(nameScheme + '_corpus.mm', corpus)

	ldamodel.save(nameScheme + "_lda.lda")

	#load saved docs for consistency and return
	dictionary = corpora.Dictionary.load(nameScheme + "_dictionary.dict")

	lda = models.LdaModel.load(nameScheme + "_lda.lda")

	corpus = corpora.MmCorpus(nameScheme + "_corpus.mm")

	return lda, dictionary, corpus




def get_topic_distr(article, article_id, lda, dictionary, corpus):
	#convert article text to bow
	vec_bow = dictionary.doc2bow(article.split())

	#calculate topic distribution for article
	topic_distr = lda.get_document_topics(vec_bow)
	
	return topic_distr, article_id




def get_max_distr(topic_distr):
	return max(topic_distr, key = lambda t: t[1])



def cluster_articles(articles, lda, dictionary, corpus):
	#initialize hash table for article clusters
	article_table = {}

	for article in articles:
		content = convert(article['content'])
		article_id = article['article_id']

		#get topic distribution for an article
		topic_dis, article_id = get_topic_distr(content, article_id, lda, dictionary, corpus)

		#get most likely topic assigned to article
		max_distr = get_max_distr(topic_dis)

		topic = max_distr[0]

		if article_table.get(topic) != None:
			article_table[topic].append(article_id)
		else:
			article_table[topic] = [article_id]

	return article_table


def classify_article(article, lda, dictionary, corpus):
	#convert article text to bow
	vec_bow = dictionary.doc2bow(article.split())

	#convert query to lda space for similarity comparison
	vec_lda = lda[vec_bow]

	return vec_lda




def compare_article(article_lda, lda, dictionary, corpus):

	#convert all documents in corpus to lda space for similarity comparisons
	index = similarities.MatrixSimilarity(lda[corpus])

	#save for consistency
	index.save("test_index.index")

	#load for consistency
	index = similarities.MatrixSimilarity.load("test_index.index")

	# computes cosine similarity between article and all other articles
	sims = index[article_lda]

	#sort similar articles in decreasing order
	sims = sorted(enumerate(sims), key=lambda item: -item[1])

	return sims



def convert(article):
	return article.encode('ascii', errors='ignore').decode('utf-8').replace("\ ", '')

