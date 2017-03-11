# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-08 12:27:22
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-10 01:34:11

from Utils.db_utils import commits_connection
import Utils.get_fakenews_db as db

@commits_connection
def add_source(conn, cur, name, author_ids = None):
	cur.execute("""INSERT INTO sources (name) VALUES (%s)""", (name,))

	inserted_source_id = db.get_source_named(conn, cur, name)[0]

	if not author_ids is None:
		for author_id in author_ids:
			if db.get_author(conn, cur, author_id) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO source_authors (source_id, author_id) VALUES (%s, %s)""", (inserted_source_id, author_id))

	return inserted_source_id

@commits_connection
def add_article(conn, cur, title, url, timestamp, content, source_id, author_ids = None, tag_ids = None):
	# Check to make sure the source is already in the database
	if db.get_source(conn, cur, source_id) is None:
		print("ERROR: No souce found within the database with [id:%d]" % source_id)
		raise EnvironmentError

	# Insert article into article table
	cur.execute("""INSERT INTO articles (title, url, created_at, content, source_id) VALUES (%s, %s, %s, %s, %s)""", (
		title,
		url,
		timestamp,
		content,
		source_id
	))

	conn.commit()

	insterted_article_id = db.get_article_linked(conn, cur, url)[0]

	# Check to make sure that the authors referenced are already in the database
	if not author_ids is None:
		for author_id in author_ids:
			# print("Checking author id: %s" % author_id)
			if db.get_author(conn, cur, author_id) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)""", (
					insterted_article_id,
					author_id
				))
				cur.execute("""INSERT INTO source_authors (author_id, source_id) VALUES (%s, %s)""", (
					author_id,
					source_id
				))

	# Check to make sure that the tags references are already in the database
	if not tag_ids is None:
		for tag_id in tag_ids:
			if db.get_tag(conn, cur, tag_id) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)""", (
					insterted_article_id,
					tag_id
				))

	return insterted_article_id

@commits_connection
def add_author(conn, cur, first_name, last_name, article_ids = None, source_ids = None):
	# Insert author into author table
	cur.execute("""INSERT INTO authors (first_name, last_name) VALUES (%s, %s)""", (first_name, last_name))

	inserted_author_id = db.get_author_named(conn, cur, first_name, last_name)

	# Check to make sure that the articles referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(conn, cur, article_id) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)""", (
					article_id,
					inserted_author_id
				))

	# Check to make sure that the sources references are already in the database
	if not source_ids is None:
		for source_id in source_ids:
			if db.get_source(conn, cur, source_id) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO  (author_id, source_id) VALUES (%s, %s)""", (
					inserted_author_id,
					source_id
				))

	return inserted_author_id

@commits_connection
def add_tag(conn, cur, name, article_ids = None):
	# Insert the Tag into the database
	cur.execute("""INSERT INTO tags (tag_name) VALUES (%s)""", (name,))

	inserted_tag_id = db.get_tag_named(conn, cur, name)[0]

	# Check to make sure that the authors referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(conn, cur, article_id) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				cur.execute("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)""", (
					article_id,
					inserted_tag_id
				))

	return inserted_tag_id
