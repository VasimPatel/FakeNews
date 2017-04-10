import logging 
import os
from os import path
import nltk
import gensim as gennylt
import Utils.settings as settings
settings.init()
import Utils.connection_utils as glc

def iter_docs(articles, stoplist):
	for article in articles:
		text = article['content']
		yield (x for x in 
				gennylt.utils.tokenize(text, lowercase=True, deacc=True, errors="ignore")
		if x not in stoplist)

class MyCorpus(object):
	@glc.new_connection(primary = True, pass_to_function = False)
	def __init__(self, query, stoplist):
		self.articles = glc.execute_db_query(query)
		self.stoplist = stoplist
		self.dictionary = gennylt.corpora.Dictionary(iter_docs(self.articles, self.stoplist))

	def __iter__(self):
		for tokens in iter_docs(self.articles, self.stoplist):
			yield self.dictionary.doc2bow(tokens)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
                    level=logging.INFO)

MODELS_DIR = "topic_modeling/models"
query = "SELECT content FROM articles  WHERE created_at BETWEEN '2015-10-01 00:00:00' AND '2016-12-30 23:59:59'"
# WHERE created_at BETWEEN '2016-10-01 00:00:00' AND '2016-12-30 23:59:59'
stoplist = set(nltk.corpus.stopwords.words("english"))
corpus = MyCorpus(query, stoplist)

corpus.dictionary.save(os.path.join(MODELS_DIR, "mtsamples.dict"))
gennylt.corpora.MmCorpus.serialize(os.path.join(MODELS_DIR, "mtsamples.mm"), 
                                  corpus)