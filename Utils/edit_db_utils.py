# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-08 12:27:22
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-09 22:53:11

from unidecode import unidecode

import Utils.connection_utils as glc
import Utils.get_db_utils as db

def add_source(name, author_ids = None, connection = None, cursor = None, VERBOSE = False):
	# Check to see whether source is already in the table
	source = db.get_source_named(name, cursor = cursor)
	source_id = None

	# Insert source into table if not already there
	if source is None:
		glc.execute_db_values_command("""INSERT INTO sources (name) VALUES (%s)""", (name,), connection = connection, cursor = cursor)
		source_id = db.get_source_named(name, cursor = cursor)['source_id']

		# VERBOSE printing
		if VERBOSE:
			print("Added source %s to database" % name)
	else:
		source_id = source["source_id"]

		# Print if VERBOSE messaging turned on
		if VERBOSE:
			print("Source %s is already stored in the database" % name)

	# Link sources to given authors
	if not author_ids is None:
		# Insert proper links
		for author_id in author_ids:
			if db.get_author(author_id, cursor = cursor) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				if db.get_source_author_link(source_id, author_id, cursor = cursor) is None:
					glc.execute_db_values_command("""INSERT INTO source_authors (source_id, author_id) VALUES (%s, %s)""", (source_id, author_id))

					# VERBOSE printing
					if VERBOSE:
						print("Linked [source_id:%d] to [author_id:%d]" % (source_id, author_id))
				elif VERBOSE:
					print("[source_id:%d] already linked to [author_id:%d]" % (source_id, author_id))

	return source_id

def add_article(title, url, timestamp, content, source_id, author_ids = None, tag_ids = None, connection = None, cursor = None, VERBOSE = False):
	# Check to make sure the source is already in the database
	if db.get_source(source_id, cursor = cursor) is None:
		print("ERROR: No souce found within the database with [id:%d]" % source_id)
		raise EnvironmentError

	# Check to see whether article is already in the table
	article = db.get_article_linked(url, cursor = cursor)
	article_id = None

	# Insert article into table if not already there
	if article is None:
		# Insert article into article table
		glc.execute_db_values_command("""INSERT INTO articles (title, url, created_at, content, source_id) VALUES (%s, %s, %s, %s, %s)""", (
			title,
			url,
			timestamp,
			content,
			source_id
		), connection = connection, cursor = cursor)
		article_id = db.get_article_linked(url, cursor = cursor)["article_id"]

		# VERBOSE printing
		if VERBOSE:
			print("Added article '%s' to database." % unidecode(title))
	else:
		# Update article to newest information
		glc.execute_db_values_command("""UPDATE articles SET title = %s,
		created_at = %s,
		content = %s,
		source_id = %s WHERE url = %s""", (
			title,
			timestamp,
			content,
			source_id,
			url
		), connection = connection, cursor = cursor)
		article_id = article["article_id"]

		# Print if VERBOSE messaging turned on
		if VERBOSE:
			print("Article '%s' is already stored in the database" % unidecode(title))

	# Check to make sure that the authors referenced are already in the database and link the article to its authors and source
	if not author_ids is None:
		for author_id in author_ids:
			if db.get_author(author_id, cursor = cursor) is None:
				print("ERROR: No author found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				if db.get_article_author_link(article_id, author_id, cursor = cursor) is None:
					# Insert links from articles to authors
					glc.execute_db_values_command("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)""", (
						article_id,
						author_id
					), connection = connection, cursor = cursor)

					# VERBOSE printing
					if VERBOSE:
						print("Linked [article_id:%d] to [author_id:%d]" % (article_id, author_id))
				elif VERBOSE:
					print("[article_id:%d] already linked to [author_id:%d]" % (article_id, author_id))

				if db.get_source_author_link(source_id, author_id, cursor = cursor) is None:
					# Insert links from sources to authors
					glc.execute_db_values_command("""INSERT INTO source_authors (author_id, source_id) VALUES (%s, %s)""", (
						author_id,
						source_id
					), connection = connection, cursor = cursor)

					# VERBOSE printing
					if VERBOSE:
						print("Linked article's [source_id:%d] to [author_id:%d]" % (source_id, author_id))
				elif VERBOSE:
					print("Article's [source_id:%d] already linked to [author_id:%d]" % (source_id, author_id))

	# Check to make sure that the tags references are already in the database
	if not tag_ids is None:
		for tag_id in tag_ids:
			if db.get_tag(tag_id, cursor = cursor) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				if db.get_article_tag_link(article_id, tag_id, cursor = cursor) is None:
					# Insert links from articles to tags
					glc.execute_db_values_command("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)""", (
						article_id,
						tag_id
					), connection = connection, cursor = cursor)

					# VERBOSE printing
					if VERBOSE:
						print("Linked [article_id:%d] to [tag_id:%d]" % (article_id, tag_id))
				elif VERBOSE:
					print("[article_id:%d] already linked to [tag_id:%d]" % (article_id, tag_id))

	return article_id

def add_author(first_name, last_name, article_ids = None, source_ids = None, connection = None, cursor = None, VERBOSE = False):
	# Check to see whether the author is already in the database
	author = db.get_author_named(first_name, last_name, cursor = cursor)
	author_id = None

	# Insert author into table if not already there
	if author is None:
		# Insert author into author table
		glc.execute_db_values_command("""INSERT INTO authors (first_name, last_name) VALUES (%s, %s)""", (first_name, last_name), connection = connection, cursor = cursor)
		author_id = db.get_author_named(first_name, last_name, cursor = cursor)["author_id"]

		# VERBOSE printing
		if VERBOSE:
			print("Added author '%s %s' to database." % (first_name, last_name))
	else:
		author_id = author["author_id"]

		# Print if VERBOSE messaging turned on
		if VERBOSE:
			print("Author %s %s is already stored in the database" % (first_name, last_name))

	# Check to make sure that the articles referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(conn, cur, article_id, cursor = cursor) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				if db.get_article_author_link(article_id, author_id, cursor = cursor) is None:
					# Insert links from articles to this author
					glc.execute_db_values_command("""INSERT INTO article_authors (article_id, author_id) VALUES (%s, %s)""", (
						article_id,
						author_id
					), connection = connection, cursor = cursor)

					# VERBOSE printing
					if VERBOSE:
						print("Linked [author_id:%d] to [article_id:%d]" % (author_id, article_id))
				elif VERBOSE:
					print("[author_id:%d] already linked to [article_id:%d]" % (author_id, article_id))

	# Check to make sure that the sources references are already in the database
	if not source_ids is None:
		for source_id in source_ids:
			if db.get_source(source_id, cursor = cursor) is None:
				print("ERROR: No tag found in database with [id:%d]" % source_id)
				raise EnvironmentError
			else:
				if db.get_source_author_link(source_id, author_id, cursor = cursor) is None:
					# Insert links from sources to this author
					glc.execute_db_values_command("""INSERT INTO  (author_id, source_id) VALUES (%s, %s)""", (
						author_id,
						source_id
					), connection = connection, cursor = cursor)

					# VERBOSE printing
					if VERBOSE:
						print("Linked [article_id:%d] to [source_id:%d]" % (author_id, source_id))
				elif VERBOSE:
					print("[article_id:%d] already linked to [source_id:%d]" % (author_id, source_id))

	return author_id

def add_tag(name, article_ids = None, connection = None, cursor = None, VERBOSE = False):
	# Check to see whether the tag is already in the database
	tag = db.get_tag_named(name, cursor = cursor)
	tag_id = None

	# Insert tag into table if not already there
	if tag is None:
		# Insert the Tag into the database
		glc.execute_db_values_command("""INSERT INTO tags (tag_name) VALUES (%s)""", (name,), connection = connection, cursor = cursor)
		tag_id = db.get_tag_named(name, cursor = cursor)["tag_id"]

		# VERBOSE printing
		if VERBOSE:
			print("Added tag %s to database" % name)
	else:
		tag_id = tag["tag_id"]

		# Print if VERBOSE messaging turned on
		if VERBOSE:
			print("Tag %s is already stored in the database" % name)

	# Check to make sure that the authors referenced are already in the database
	if not article_ids is None:
		for article_id in article_ids:
			if db.get_article(article_id, cursor = cursor) is None:
				print("ERROR: No article found in database with [id:%d]" % author_id)
				raise EnvironmentError
			else:
				if db.get_article_tag_link(article_id, tag_id, cursor = cursor) is None:
					# Insert links from articles to this tag
					glc.execute_db_values_command("""INSERT INTO article_tags (article_id, tag_id) VALUES (%s, %s)""", (
						article_id,
						tag_id
					), connection = connection, cursor = cursor)

					# VERBOSE printing
					if VERBOSE:
						print("Linked [tag_id:%d] to [article_id:%d]" % (tag_id, article_id))
				elif VERBOSE:
					print("[tag_id:%d] already linked to [article_id:%d]" % (tag_id, article_id))

	return tag_id
