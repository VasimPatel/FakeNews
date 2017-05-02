from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models, similarities
import gensim
MODEL_DIR = "topic_modeling/models/"
def lda(articles, num_t=10, name = "test", load=True):
	if load != True:
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
		    
		    i = convert(i['content'])
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
		ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_t, id2word = dictionary, alpha=2, passes=20)

		#save dictionary corpus and ldamodel to be used later
		dictionary.save(MODEL_DIR + name + "_dictionary.dict")

		corpora.MmCorpus.serialize(MODEL_DIR + name + '_corpus.mm', corpus)

		ldamodel.save(MODEL_DIR + name + "_lda.lda")

		#load saved docs for consistency and return
		dictionary = corpora.Dictionary.load(MODEL_DIR + name + "_dictionary.dict")

		lda = models.LdaModel.load(MODEL_DIR + name + "_lda.lda")

		corpus = corpora.MmCorpus(MODEL_DIR + name + "_corpus.mm")
	else:
		lda = models.LdaModel.load(MODEL_DIR + name + "_lda.lda")
		corpus = corpora.MmCorpus(MODEL_DIR + name + "_corpus.mm")
		dictionary = corpora.Dictionary.load(MODEL_DIR + name + "_dictionary.dict")

	return lda, dictionary, corpus




def get_topic_distr(article, lda, dictionary, corpus):

	article_content = convert(article['content'])
	
	#convert article text to bow
	vec_bow = dictionary.doc2bow(article_content.split())

	#calculate topic distribution for article
	topic_distr = lda.get_document_topics(vec_bow, minimum_probability=0)
	
	return topic_distr




def get_max_distr(topic_distr):
	return max(topic_distr, key = lambda t: t[1])



def cluster_articles(articles, lda, dictionary, corpus):
	#initialize hash table for article clusters
	article_table = {}

	for article in articles:

		#get topic distribution for an article
		topic_dis = get_topic_distr(article, lda, dictionary, corpus)

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
	vec_bow = dictionary.doc2bow(convert(article['content']).split())

	#convert query to lda space for similarity comparison
	vec_lda = lda[vec_bow]

	return vec_lda




def compare_article(article_lda, lda, dictionary, corpus, name="test"):

	#convert all documents in corpus to lda space for similarity comparisons
	index = similarities.MatrixSimilarity(lda[corpus])

	#save for consistency
	index.save(MODEL_DIR + name + "_index.index")

	#load for consistency
	index = similarities.MatrixSimilarity.load(MODEL_DIR + name + "_index.index")

	# computes cosine similarity between article and all other articles
	sims = index[article_lda]

	#sort similar articles in decreasing order
	sims = sorted(enumerate(sims), key=lambda item: -item[1])

	return sims



def get_topic_words(lda, nmost):
	topic_words = []
	for words in lda.show_topics(num_words=nmost):
		topic_words.append(words)

	return topic_words

def convert(article):
	return article.encode('ascii', errors='ignore').decode('utf-8').replace("\ ", '')

