# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-04 23:27:36
# @Last modified by:   DivinePC
# @Last modified time: 2017-03-06 19:14:20

import Utils.settings as settings
settings.init()

# Import required modules
import os
import Utils.db_utils as db_utils

@db_utils.commits_connection
def setup_sources(conn, cur):
	cur.execute("""CREATE TABLE sources (
		source_id serial UNIQUE PRIMARY KEY,
		name varchar(255) UNIQUE NOT NULL
	)""")

@db_utils.commits_connection
def setup_articles(conn, cur):
	cur.execute("""CREATE TABLE articles (
		article_id serial UNIQUE PRIMARY KEY,
		title varchar(255) NOT NULL,
		url varchar(255) NOT NULL,
		created_at TIMESTAMP WITH TIME ZONE NOT NULL,
		content text NOT NULL,
		source_id integer NOT NULL REFERENCES sources on DELETE RESTRICT
	)""")

@db_utils.commits_connection
def setup_authors(conn, cur):
	cur.execute("""CREATE TABLE authors (
		author_id serial UNIQUE PRIMARY KEY,
		first_name varchar(50) NOT NULL,
		last_name varchar(50) NOT NULL
	)""")

@db_utils.commits_connection
def setup_linking_tables(conn, cur):
	cur.execute("""CREATE TABLE article_authors (
		atricle_id integer NOT NULL PRIMARY KEY REFERENCES articles ON DELETE CASCADE,
		author_id integer NOT NULL REFERENCES authors ON DELETE CASCADE
	)""")
	cur.execute("""CREATE TABLE source_authors (
		source_id integer NOT NULL PRIMARY KEY REFERENCES sources ON DELETE CASCADE,
		author_id integer NOT NULL REFERENCES authors ON DELETE CASCADE
	)""")

@db_utils.new_connection(host = os.environ.get("DBHOST"), dbname = os.environ.get("DBNAME"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"))
def main(conn, cur):
	setup_sources(conn, cur)
	setup_articles(conn, cur)
	setup_authors(conn, cur)
	setup_linking_tables(conn, cur)

if __name__ == "__main__":
	main()
