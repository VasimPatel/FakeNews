# @Author: DivineEnder
# @Date:   2017-04-19 19:59:49
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-19 20:35:33 


import Utils.connection_utils as glc

def remove_article_dups(connection = None, cursor = None):
	glc.execute_db_command("""DELETE FROM articles WHERE article_id IN (
		SELECT article_id FROM (
			SELECT article_id, ROW_NUMBER() OVER (
				PARTITION BY title, publish_date, source_id ORDER BY article_id
			) AS rnum FROM articles
		) t WHERE t.rnum > 1)
	)""")
