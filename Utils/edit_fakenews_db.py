# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-08 12:27:22
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-20 20:51:03

import Utils.connection_utils as glc
import Utils.get_fakenews_db as db

def add_source(name, author_ids = None, connection = None, cursor = None):
	glc.execute_db_values_command("""INSERT INTO sources (name) VALUES (%s)""", (name,), connection = connection, cursor = cursor)

	print("Added source %s to database" % name)

	inserted_source_id = db.get_source_named(name, cursor = cursor)

	if not author_ids is None:
		for author_id in author_ids:
			if db.get_author(author_id, cursor = cursor) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				glc.execute_db_values_command("""INSERT INTO source_authors (source_id, author_id) VALUES (%s, %s)""", (inserted_source_id, author_id))

				print("Linked [source_id:%d] to [author_id:%d]" % (inserted_source_id, author_id))

	return inserted_source_id

def add_article(title, url, timestamp, content, source_id, author_ids = None, tag_ids = None, connection = None, cursor = None):
	# Check to make sure the source is already in the database
	if db.get_source(source_id, cursor = cursor) is None:
		print("ERROR: No souce found within the database with [id:%d]" % source_id)
		raise EnvironmentError

	# Insert article into article table
	glc.execute_db_values_command("""INSERT INTO articles (title, url, created_at, content, source_id) VALUES (%s, %s, %s, %s, %s)""", (
		title,
		url,
		timestamp,
		content,
		source_id
	), connection = connection, cursor = cursor)

	print("Added article %s to database." % title)

	insterted_article_id = db.get_article_linked(url, cursor = cursor)

	# Check to make sure that the authors referenced are already in the database
	if not author_ids is None:
		for author_id in author_ids:
			# print("Checking author id: %s" % author_id)
			if db.get_author(author_id, cursor = cursor) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				glc.execute_db_values_command("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)""", (
					insterted_article_id,
					author_id
				), connection = connection, cursor = cursor)
				glc.execute_db_values_command("""INSERT INTO source_authors (author_id, source_id) VALUES (%s, %s)""", (
					author_id,
					source_id
				), connection = connection, cursor = cursor)

				print("Linked [article_id:%d] to [author_id:%d]" % (insterted_article_id, author_id))
				print("Linked article's [source_id:%d] to [author_id:%d]" % (source_id, author_id))

	# Check to make sure that the tags references are already in the database
	if not tag_ids is None:
		for tag_id in tag_ids:
			if db.get_tag(tag_id, cursor = cursor) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				glc.execute_db_values_command("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)""", (
					insterted_article_id,
					tag_id
				), connection = connection, cursor = cursor)

				print("Linked [article_id:%d] to [tag_id:%d]" % (insterted_article_id, tag_id))

	return insterted_article_id

def add_author(first_name, last_name, article_ids = None, source_ids = None, connection = None, cursor = None):
	# Insert author into author table
	glc.execute_db_values_command("""INSERT INTO authors (first_name, last_name) VALUES (%s, %s)""", (first_name, last_name), connection = connection, cursor = cursor)

	print("Added author '%s %s' to database." % (first_name, last_name))

	inserted_author_id = db.get_author_named(first_name, last_name, cursor = cursor)

	# Check to make sure that the articles referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(conn, cur, article_id, cursor = cursor) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				glc.execute_db_values_command("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)""", (
					article_id,
					inserted_author_id
				), connection = connection, cursor = cursor)

				print("Linked [author_id:%d] to [article_id:%d]" % (inserted_author_id, article_id))

	# Check to make sure that the sources references are already in the database
	if not source_ids is None:
		for source_id in source_ids:
			if db.get_source(source_id, cursor = cursor) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				glc.execute_db_values_command("""INSERT INTO  (author_id, source_id) VALUES (%s, %s)""", (
					inserted_author_id,
					source_id
				), connection = connection, cursor = cursor)

				print("Linked [article_id:%d] to [source_id:%d]" % (inserted_author_id, source_id))

	return inserted_author_id

def add_tag(name, article_ids = None, connection = None, cursor = None):
	# Insert the Tag into the database
	glc.execute_db_values_command("""INSERT INTO tags (tag_name) VALUES (%s)""", (name,), connection = connection, cursor = cursor)

	print("Added tag %s to database" % name)

	inserted_tag_id = db.get_tag_named(name, cursor = cursor)

	# Check to make sure that the authors referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(article_id, cursor = cursor) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				glc.execute_db_values_command("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)""", (
					article_id,
					inserted_tag_id
				), connection = connection, cursor = cursor)

				print("Linked [tag_id:%d] to [article_id:%d]" % (inserted_tag_id, article_id))

	return inserted_tag_id
