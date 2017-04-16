from Utils import connection_utils as glc
from .corpus import lda, classify_article, get_topic_distr, compare_article, get_max_distr, cluster_articles
@glc.new_connection(primary = True, pass_to_function = False)
def main():
	#collect articles to topic model
	query = "SELECT * FROM articles  WHERE created_at BETWEEN '2016-11-01 00:00:00' AND '2016-12-30 23:59:59' LIMIT 30"
	articles = glc.execute_db_query(query)
	doc_set = []
	for each in articles[:4]:
		#encode article text properly and clean
		doc_set.append(convert(each['content']))

	#use latent dirichelet allocation to topic model
	model, dictionary, corpus = lda(doc_set)

	#-------------------------------------------------------------------------------
	#convert and classify article content to lda space
	vec_lda = classify_article(convert(articles[4]['content']), model, dictionary, corpus)

	#get sorted list of similar articles
	sims = compare_article(vec_lda, model, dictionary, corpus)


	#-------------------------------------------------------------------------------
	#get topic distribution for an article
	topic_dis, article_id = get_topic_distr(convert(articles[3]['content']), articles[3]['article_id'], model, dictionary, corpus)

	#get most likely topic assigned to article
	max_distr = get_max_distr(topic_dis)

	#-------------------------------------------------------------------------------
	#test clustering articles
	clusters = cluster_articles(articles, model, dictionary, corpus)

	print(clusters)








def convert(article):
	return article.encode('ascii', errors='ignore').decode('utf-8').replace("\ ", '')
