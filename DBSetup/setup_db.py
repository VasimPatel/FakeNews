# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-04 23:27:36
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-19 20:53:43 

import Utils.settings as settings
settings.init()

# Import required modules
import os
import Utils.db_utils as db_utils
import Utils.connection_utils as glc

def setup_sources():
	glc.execute_db_command("""CREATE TABLE sources (
		source_id serial UNIQUE PRIMARY KEY,
		name varchar(255) UNIQUE NOT NULL,
		base_url varchar(512) UNIQUE
	)""")

def setup_articles():
	glc.execute_db_command("""CREATE TABLE articles (
		article_id serial UNIQUE PRIMARY KEY,
		title varchar(512) NOT NULL,
		url varchar(512),
		publish_date DATE NOT NULL,
		content text NOT NULL,
		main_img_url varchar(1024),
		source_id integer NOT NULL REFERENCES sources on DELETE RESTRICT,
		is_fake boolean,
		fake_type varchar(25) NOT NULL DEFAULT 'NO_CLASS'
	)""")

def setup_authors():
	glc.execute_db_command("""CREATE TABLE authors (
		author_id serial UNIQUE PRIMARY KEY,
		first_name varchar(50) NOT NULL,
		middle_name varchar(100),
		last_name varchar(50)
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

def setup_tokens():
	glc.execute_db_command("""CREATE TABLE tokens (
		token_id serial UNIQUE PRIMARY KEY,
		token text UNIQUE
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
	glc.execute_db_command("""CREATE UNIQUE INDEX ar_au_unique_skey ON article_authors (article_id, author_id)""")
	glc.execute_db_command("""CREATE UNIQUE INDEX s_au_unique_skey ON source_authors (source_id, author_id)""")
	glc.execute_db_command("""CREATE UNIQUE INDEX ar_t_unique_skey ON article_tags (article_id, tag_id)""")
	glc.execute_db_command("""CREATE INDEX token_skey ON tokens (token)""")

def setup_constraints():
	glc.execute_db_command("""ALTER TABLE articles ADD CONSTRAINT check_fake_types CHECK (fake_type IN ('bs', 'conspiracy', 'satire', 'hate', 'fake', 'state', 'junksci', 'bias', 'NO_CLASS'))""")
	glc.execute_db_command("""ALTER TABLE articles ADD CONSTRAINT unique_articles UNIQUE (title, publish_date, source_id)""")
	glc.execute_db_command("""ALTER TABLE authors ADD CONSTRAINT unique_authors UNIQUE (first_name, last_name)""")

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	setup_sources()
	setup_articles()
	setup_authors()
	setup_tags()
	setup_tokens()
	setup_linking_tables()
	setup_indexes()
	setup_constraints()

if __name__ == "__main__":
	main()
