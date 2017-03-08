# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-08 12:27:22
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivinePC
# @Last modified time: 2017-03-08 12:44:52

from db_utils import commits_connection

@commits_connection
def add_source(conn, cur, name, author_ids = None):
	cur.execute("""INSERT INTO TABLE sources (name) VALUES (%s)""", (name))

	if not authors_ids is None:
		for author_id in author_ids:
			if get_author(conn, cur, author_id) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO TABLE source_authors (source_id, author_id) VALUES (%s, %s)""", (
					get_source_named(conn, cur, name)[0],
					author_id
				))

@commits_connection
def add_article(conn, cur, title, url, timestamp, content, source_id, author_ids = None, tag_ids = None):
	# Check to make sure the source is already in the database
	if get_source(conn, cur, source_id) is None:
		print("ERROR: No souce found within the database with [id:%d]" % source_id)
		raise EnvironmentError

	# Insert article into article table
	cur.execute("""INSERT INTO TABLE articles (title, url, created_at, content, source_id) VALUES (%s, %s, %s, %s, %s)""", (
		title,
		url,
		timestamp,
		content,
		source_id
	))

	# Check to make sure that the authors referenced are already in the database
	if not authors_ids is None:
		for author_id in author_ids:
			if get_author(conn, cur, author_id) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO TABLE article_authors (article_id, author_id) VALUES (%s, %s)""", (
					get_article_linked(conn, cur, url)[0],
					author_id
				))

	# Check to make sure that the tags references are already in the database
	if not tag_ids is None:
		for tag_id in tag_ids:
			if get_tag(conn, cur, tag_id) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO TABLE article_tags (article_id, tag_id) VALUES (%s, %s)""", (
					get_article_linked(conn, cur, url)[0],
					tag_id
				))

@commits_connection
def add_author(conn, cur, first_name, last_name, article_ids = None, source_ids = None):
	# Insert author into author table
	cur.execute("""INSERT INTO TABLE authors (first_name, last_name) VALUES (%s, %s)""", (first_name last_name))

	# Check to make sure that the articles referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if get_article(conn, cur, article_id) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO TABLE article_authors (article_id, author_id) VALUES (%s, %s)""", (
					article_id,
					get_author_named(conn, cur, first_name, last_name)[0]
				))

	# Check to make sure that the sources references are already in the database
	if not source_ids is None:
		for source_id in source_ids:
			if get_tag(conn, cur, tag_id) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO TABLE article_tags (article_id, tag_id) VALUES (%s, %s)""", (
					get_article_url(conn, cur, url)[0],
					get_author_named(conn, cur, first_name, last_name)[0]
				))

@commits_connection
def add_tag(conn, cur, name, article_ids = None):
	# Insert the Tag into the database
	cur.execute("""INSERT INTO TABLE tags (tag_name) VALUES (%s)""", (name))

	# Check to make sure that the authors referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if get_article(conn, cur, article_id) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO TABLE article_tags (article_id, tag_id) VALUES (%s, %s)""", (
					article_id,
					get_tag_named(conn, cur, name)[0]
				))
