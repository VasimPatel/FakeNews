# @Author: DivineEnder
# @Date:   2017-04-04 18:56:31
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-16 15:53:57

import Utils.connection_utils as glc

def get_authors_with_num_sources(num_sources, cursor = None):
	return glc.execute_db_query("""WITH author_source_counts AS
		(SELECT author_id, COUNT(source_id) FROM source_authors GROUP BY author_id)
		SELECT author_id FROM author_source_counts WHERE count = %s""", (num_sources,))

def get_authors_with_min_num_sources(min_sources, cursor = None):
	return glc.execute_db_query("""WITH author_source_counts AS
		(SELECT author_id, COUNT(source_id) FROM source_authors GROUP BY author_id)
		SELECT author_id FROM author_source_counts WHERE count >= %s""", (num_sources,))

def get_avg_authors_per_article(cursor = None):
	return glc.execute_db_query("""WITH article_author_count AS
		(SELECT article_id, COUNT(author_id) FROM article_authors GROUP BY article_id)
		SELECT AVG(count) FROM article_author_count""")["avg"]
