# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-04 23:27:36
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-20 21:11:31

import Utils.settings as settings
settings.init()

# Import required modules
import os
import Utils.db_utils as db_utils
import Utils.connection_utils as glc

def setup_sources():
	glc.execute_db_command("""CREATE TABLE sources (
		source_id serial UNIQUE PRIMARY KEY,
		name varchar(255) UNIQUE NOT NULL
	)""")

def setup_articles():
	glc.execute_db_command("""CREATE TABLE articles (
		article_id serial UNIQUE PRIMARY KEY,
		title varchar(255) NOT NULL,
		url varchar(255) NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE NOT NULL,
		content text NOT NULL,
		source_id integer NOT NULL REFERENCES sources on DELETE RESTRICT
	)""")

def setup_authors():
	glc.execute_db_command("""CREATE TABLE authors (
		author_id serial UNIQUE PRIMARY KEY,
		first_name varchar(50) NOT NULL,
		last_name varchar(50) NOT NULL
	)""")

def setup_linking_tables():
	glc.execute_db_command("""CREATE TABLE article_authors (
			article_id integer NOT NULL REFERENCES articles ON DELETE CASCADE,
			author_id integer NOT NULL REFERENCES authors ON DELETE CASCADE
		)""", None)

	glc.execute_db_command("""CREATE TABLE source_authors (
			source_id integer NOT NULL REFERENCES sources ON DELETE CASCADE,
			author_id integer NOT NULL REFERENCES authors ON DELETE CASCADE
		)""", None)

	glc.execute_db_command("""CREATE TABLE article_tags (
			article_id integer NOT NULL REFERENCES articles ON DELETE CASCADE,
			tag_id integer NOT NULL REFERENCES tags ON DELETE CASCADE
		)""")

def setup_tags():
	glc.execute_db_command("""CREATE TABLE tags (
		tag_id serial UNIQUE PRIMARY KEY,
		tag_name varchar(255) UNIQUE
	)""")

def setup_indexes():
	glc.execute_db_command("""CREATE INDEX tag_name_skey ON tags (tag_name)""")
	glc.execute_db_command("""CREATE INDEX source_name_skey ON sources (name)""")
	glc.execute_db_command("""CREATE INDEX author_fname_skey ON authors (first_name)""")
	glc.execute_db_command("""CREATE INDEX author_lname_skey ON authors (last_name)""")
	glc.execute_db_command("""CREATE INDEX author_fullname_skey ON authors (first_name, last_name)""")
	glc.execute_db_command("""CREATE INDEX article_title_skey ON articles (title)""")
	glc.execute_db_command("""CREATE INDEX author_source_skey ON articles (source_id)""")
	glc.execute_db_command("""CREATE INDEX ar_au_article_skey ON article_authors (article_id)""")
	glc.execute_db_command("""CREATE INDEX ar_au_author_skey ON article_authors (author_id)""")
	glc.execute_db_command("""CREATE INDEX s_au_source_skey ON source_authors (source_id)""")
	glc.execute_db_command("""CREATE INDEX s_au_author_skey ON source_authors (author_id)""")
	glc.execute_db_command("""CREATE INDEX ar_t_article_skey ON article_tags (article_id)""")
	glc.execute_db_command("""CREATE INDEX ar_t_tag_skey ON article_tags (tag_id)""")

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	setup_sources()
	setup_articles()
	setup_authors()
	setup_tags()
	setup_linking_tables()
	setup_indexes()

if __name__ == "__main__":
	main()
