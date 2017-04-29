from Utils import connection_utils as glc
from .corpus import lda, classify_article, get_topic_distr, compare_article, get_max_distr, cluster_articles, get_topic_words
@glc.new_connection(primary = True, pass_to_function = False)
def query(query):
	return glc.execute_db_query(query)


def main():
	#collect articles to topic model
	query1 = "SELECT * FROM articles where is_fake=True LIMIT 30"
	query2="SELECT * FROM articles where is_fake is NULL LIMIT 30"
	articles = query(query1)
	articles2= query(query2)
	doc_set = []
	for each in articles[:-1]:
		#encode article text properly and clean
		doc_set.append(each)

	for each in articles2[:-1]:
		#encode article text properly and clean
		doc_set.append(each)
	#use latent dirichelet allocation to topic model
	model, dictionary, corpus = lda(doc_set)

	#-------------------------------------------------------------------------------
	#convert and classify article content to lda space
	vec_lda = classify_article(articles[-1], model, dictionary, corpus)

	#get sorted list of similar articles
	sims = compare_article(vec_lda, model, dictionary, corpus, name='test')

	print("Similar Articles: " + str(sims[0:10]))


	#-------------------------------------------------------------------------------
	#get topic distribution for an article
	topic_dis, article_id = get_topic_distr(articles[-1], model, dictionary, corpus)

	print("Topic Dist: " + str(topic_dis))
	#get most likely topic assigned to article
	max_distr = get_max_distr(topic_dis)
	print("Most Probable Topic: " + str(max_distr))
	#-------------------------------------------------------------------------------
	#test clustering articles
	clusters = cluster_articles(articles+articles2, model, dictionary, corpus)

	print(clusters)

	#-------------------------------------------------------------------------------
	for each in get_topic_words(model, nmost=10):
		print(each)

