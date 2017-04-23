# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-08 12:27:22
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-22 15:36:37

from unidecode import unidecode

import Utils.connection_utils as glc
import Utils.get_db_utils as db

def add_source(name, base_url, author_ids = None, connection = None, cursor = None, VERBOSE = False):
	# Insert into database or update existing row on conflict
	source_id = glc.execute_db_values_command("""INSERT INTO sources (name, base_url) VALUES (%s, %s) ON CONFLICT (base_url)
		DO UPDATE SET name = EXCLUDED.name""",
		(name, base_url),
		returns = "source_id",
		connection = connection,
		cursor = cursor)["source_id"]

	if VERBOSE:
		print("Added source %s (id:%d) to database" % (name, source_id))

	# Link sources to given authors
	if not author_ids is None:
		# Insert proper links
		for author_id in author_ids:
			if db.get_author(author_id, cursor = cursor) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				glc.execute_db_values_command("""INSERT INTO source_authors (source_id, author_id) VALUES (%s, %s) ON CONFLICT DO NOTHING""", (source_id, author_id))

				# VERBOSE printing
				if VERBOSE:
					print("Linked [source_id:%d] to [author_id:%d]" % (source_id, author_id))

	return source_id

def add_article(title, publish_date, content, source_id, main_img_url = None, url = None, is_fake = None, fake_type = "NO_CLASS", author_ids = None, tag_ids = None, connection = None, cursor = None, VERBOSE = False):
	# Check to make sure the source is already in the database
	if db.get_source(source_id, cursor = cursor) is None:
		print("ERROR: No souce found within the database with [id:%d]" % source_id)
		raise EnvironmentError

	article_id = glc.execute_db_values_command("""INSERT INTO articles (title, url, publish_date, content, main_img_url, is_fake, fake_type, source_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
		ON CONFLICT (title, publish_date, source_id)
		DO UPDATE SET url = EXCLUDED.url,
			content = EXCLUDED.content,
			main_img_url = EXCLUDED.main_img_url,
			is_fake = EXCLUDED.is_fake,
			fake_type = EXCLUDED.fake_type""", (
		title,
		url,
		publish_date,
		content,
		main_img_url,
		is_fake,
		fake_type,
		source_id
	), returns = "article_id", connection = connection, cursor = cursor)["article_id"]

	# VERBOSE printing
	if VERBOSE:
		print("Added article '%s' to database." % unidecode(title))

	# Check to make sure that the authors referenced are already in the database and link the article to its authors and source
	if not author_ids is None:
		for author_id in author_ids:
			if db.get_author(author_id, cursor = cursor) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				# Try to insert or do nothing if already in database
				glc.execute_db_values_command("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)
					ON CONFLICT (article_id, author_id) DO NOTHING""", (
					article_id,
					author_id
				), connection = connection, cursor = cursor)
				# VERBOSE printing
				if VERBOSE:
					print("Linked [article_id:%d] to [author_id:%d]" % (article_id, author_id))

				# Insert links from sources to authors
				glc.execute_db_values_command("""INSERT INTO source_authors (author_id, source_id) VALUES (%s, %s)
					ON CONFLICT (author_id, source_id) DO NOTHING""", (
					author_id,
					source_id
				), connection = connection, cursor = cursor)
				# VERBOSE printing
				if VERBOSE:
					print("Linked article's [source_id:%d] to [author_id:%d]" % (source_id, author_id))

	# Check to make sure that the tags references are already in the database
	if not tag_ids is None:
		for tag_id in tag_ids:
			if db.get_tag(tag_id, cursor = cursor) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				# Insert links from articles to tags
				glc.execute_db_values_command("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)
					ON CONFLICT (article_id, tag_id) DO NOTHING""", (
					article_id,
					tag_id
				), connection = connection, cursor = cursor)

				# VERBOSE printing
				if VERBOSE:
					print("Linked [article_id:%d] to [tag_id:%d]" % (article_id, tag_id))

	return article_id

def add_author(first_name, last_name, middle_name = None, article_ids = None, source_ids = None, connection = None, cursor = None, VERBOSE = False):
	# Insert author into author table
	author_id = glc.execute_db_values_command("""INSERT INTO authors (first_name, last_name, middle_name) VALUES (%s, %s, %s)
		ON CONFLICT (first_name, last_name)
		DO UPDATE SET middle_name = EXCLUDED.middle_name""",
		(first_name, last_name, middle_name),
		returns = "author_id",
		connection = connection,
		cursor = cursor)["author_id"]

	# VERBOSE printing
	if VERBOSE:
		print("Added author '%s %s' to database." % (first_name, last_name))

	# Check to make sure that the articles referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(conn, cur, article_id, cursor = cursor) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				# Insert links from articles to this author
				glc.execute_db_values_command("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)
					ON CONFLICT (article_id, author_id) DO NOTHING""", (
					article_id,
					author_id
				), connection = connection, cursor = cursor)

				# VERBOSE printing
				if VERBOSE:
					print("Linked [author_id:%d] to [article_id:%d]" % (author_id, article_id))

	# Check to make sure that the sources references are already in the database
	if not source_ids is None:
		for source_id in source_ids:
			if db.get_source(source_id, cursor = cursor) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				# Insert links from sources to this author
				glc.execute_db_values_command("""INSERT INTO  (author_id, source_id) VALUES (%s, %s)
					ON CONFLICT (author_id, source_id) DO NOTHING""", (
					author_id,
					source_id
				), connection = connection, cursor = cursor)

				# VERBOSE printing
				if VERBOSE:
					print("Linked [article_id:%d] to [source_id:%d]" % (author_id, source_id))

	return author_id

def add_tag(name, article_ids = None, connection = None, cursor = None, VERBOSE = False):

	# Insert the Tag into the database
	tag_id = glc.execute_db_values_command("""INSERT INTO tags (tag_name) VALUES (%s)
		ON CONFLICT (tag_name) DO UPDATE SET tag_name = EXCLUDED.tag_name""", (name,), returns = "tag_id", connection = connection, cursor = cursor)["tag_id"]

	# Check to make sure that the authors referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(article_id, cursor = cursor) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				# Insert links from articles to this tag
				glc.execute_db_values_command("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)
					ON CONFLICT (article_id, tag_id) DO NOTHING""", (
					article_id,
					tag_id
				), connection = connection, cursor = cursor)

				# VERBOSE printing
				if VERBOSE:
					print("Linked [tag_id:%d] to [article_id:%d]" % (tag_id, article_id))

	return tag_id
