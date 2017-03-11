# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-08 12:27:35
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-10 17:40:24

# from Utils.db_utils import commits_connection as cc
# from Utils.db_utils import uses_connection as uc
from Utils.db_utils import glc_database_query

# -----------
# | Sources |
# -----------
@glc_database_query
def get_all_sources():
	query_glc_database("""SELECT * FROM sources""", None)

@glc_database_query
def get_sources(ids):
	return ("""SELECT * FROM sources WHERE source_id = ANY(%s)""", (ids,))

def get_source(iden):
	return get_sources([iden])[0]

@glc_database_query
def get_sources_named(names):
	return ("""SELECT * FROM sources WHERE name = ANY(%s)""", (names,))

def get_source_named(name):
	return get_sources_named([name])[0]
# -----------
# | Sources |
# -----------

# -----------
# | Articles |
# -----------
@glc_database_query
def get_all_articles():
	return ("""SELECT * FROM articles""", None)

@glc_database_query
def get_articles(ids):
	return ("""SELECT * FROM articles WHERE article_id = ANY(%s)""", (ids,))

def get_article(iden):
	return get_articles([iden])[0]

@glc_database_query
def get_articles_linked(urls):
	return ("""SELECT * FROM articles WHERE url = ANY(%s)""", (urls,))

def get_article_linked(url):
	return get_articles_linked([url])[0]

@glc_database_query
def get_articles_entitled(title):
	return ("""SELECT * FROM articles WHERE title = %s""", (title,))
# ------------
# | Articles |
# ------------

# -----------
# | Authors |
# -----------
@glc_database_query
def get_all_authors():
	return ("""SELECT * FROM authors""", None)

@glc_database_query
def get_authors(ids):
	return ("""SELECT * FROM authors WHERE author_id = ANY(%s)""", (ids,))

def get_author(iden):
	return get_authors([iden])[0]

@glc_database_query
def get_author_named(first_name, last_name):
	return ("""SELECT * FROM authors WHERE first_name = %s AND last_name = %s""", (first_name, last_name))

@glc_database_query
def get_authors_first_named(first_name):
	return ("""SELECT * FROM authors WHERE first_name = %s""", (first_name,))

@glc_database_query
def get_authors_last_named(last_name):
	return ("""SELECT * FROM authors WHERE last_name = %s""", (last_name,))
# -----------
# | Authors |
# -----------

# --------
# | Tags |
# --------
@glc_database_query
def get_all_tags():
	return ("""SELECT * FROM tags""", None)

@glc_database_query
def get_tags(ids):
	return ("""SELECT * FROM tags WHERE tag_id = ANY(%s)""", (ids,))

def get_tag(iden):
	return get_tags([iden])[0]

@glc_database_query
def get_tags_named(tag_names):
	return ("""SELECT * FROM tags WHERE tag_name = ANY(%s)""", (tag_names,))

def get_tag_named(tag_name):
	return get_tags_named([tag_name])[0]
# --------
# | Tags |
# --------

# ---------
# | Links |
# ---------
@glc_database_query
def get_article_authors(article_id):
	return ("""SELECT author_id FROM article_authors WHERE article_id = %s""", article_id)


# ---------
# | Links |
# ---------
