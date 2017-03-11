# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-04 23:27:36
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-10 17:36:24

import Utils.settings as settings
settings.init()

# Import required modules
import os
import Utils.db_utils as db_utils

@glc_database_command
def setup_sources(glc):
	return ("""CREATE TABLE sources (
		source_id serial UNIQUE PRIMARY KEY,
		name varchar(255) UNIQUE NOT NULL
	)""", None)

@glc_database_command
def setup_articles(glc):
	return ("""CREATE TABLE articles (
		article_id serial UNIQUE PRIMARY KEY,
		title varchar(255) NOT NULL,
		url varchar(255) NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE NOT NULL,
		content text NOT NULL,
		source_id integer NOT NULL REFERENCES sources on DELETE RESTRICT
	)""", None)

@glc_database_command
def setup_authors(glc):
	return ("""CREATE TABLE authors (
		author_id serial UNIQUE PRIMARY KEY,
		first_name varchar(50) NOT NULL,
		last_name varchar(50) NOT NULL
	)""", None)

def setup_linking_tables():
	@glc_database_command
	def setup_article_authors_link():
		return ("""CREATE TABLE article_authors (
			article_id integer NOT NULL REFERENCES articles ON DELETE CASCADE,
			author_id integer NOT NULL REFERENCES authors ON DELETE CASCADE
		)""", None)

	@glc_database_command
	def setup_source_authors_link():
		return ("""CREATE TABLE source_authors (
			source_id integer NOT NULL REFERENCES sources ON DELETE CASCADE,
			author_id integer NOT NULL REFERENCES authors ON DELETE CASCADE
		)""", None)

	@glc_database_command
	def setup_article_tags_link():
		return ("""CREATE TABLE article_tags (
			article_id integer NOT NULL REFERENCES articles ON DELETE CASCADE,
			tag_id integer NOT NULL REFERENCES tags ON DELETE CASCADE
		)""")

@glc_database_command
def setup_tags():
	return ("""CREATE TABLE tags (
		tag_id serial UNIQUE PRIMARY KEY,
		tag_name varchar(255) UNIQUE
	)""", None)


def setup_indexes():
	@glc_database_command
	def setup_tag_name_index():
		return ("""CREATE INDEX tag_name_skey ON tags (tag_name)""", None)

	@glc_database_command
	def setup_source_name_index():
		return ("""CREATE INDEX source_name_skey ON sources (name)""", None)

	@glc_database_command
	def setup_tag_name_index():
		return ("""CREATE INDEX tag_name_skey ON tags (tag_name)""", None)

@db_utils.new_connection(host = os.environ.get("DBHOST"), dbname = os.environ.get("DBNAME"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"), global_conn = True)
def main(glc):
	setup_sources()
	setup_articles()
	setup_authors()
	setup_tags()
	setup_linking_tables()
	setup_indexes()

if __name__ == "__main__":
	main()
