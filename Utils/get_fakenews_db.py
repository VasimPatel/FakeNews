# @Author: DivineEnder <DivinePC>
# @Date:   2017-03-08 12:27:35
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivinePC
# @Last modified time: 2017-03-08 12:44:24

from db_utils import commits_connection as cc
from db_utils import uses_connection as uc

# -----------
# | Sources |
# -----------
def get_sources(conn, cur, ids):
	cur.execute(cur.mogrify("""SELECT * FROM sources WHERE source_id IN %s""", (ids)))
	return cur.fetchall()

def get_source(conn, cur, id):
	return get_sources(conn, cur, [id])[0]

def get_sources_named(conn, cur, names):
	cur.execute(cur.mogrify("""SELECT * FROM sources WHERE name IN %s""", (names)))
	return cur.fetchall()

def get_source_named(conn, cur, name):
	return get_sources_named(conn, cur, [name])[0]
# -----------
# | Sources |
# -----------

# -----------
# | Articles |
# -----------
def get_articles(conn, cur, ids):
	cur.execute(cur.mogrify("""SELECT * FROM articles WHERE article_id IN %s""", ids))
	return cur.fetchall()

def get_article(conn, cur, id):
	return get_articles(conn, cur, [id])[0]

def get_articles_linked(conn, cur, urls):
	cur.execute(cur.mogrify("""SELECT * FROM articles WHERE url IN %s""", urls))
	return cur.fetchall()

def get_article_linked(conn, cur, url):
	return get_articles_linked(conn, cur, [url])

def get_articles_entitled(conn, cur, title):
	cur.execute(cur.mogrify("""SELECT * FROM articles WHERE title = %s""", (title)))
	return cur.fetchall()
# ------------
# | Articles |
# ------------

# -----------
# | Authors |
# -----------
def get_authors(conn, cur, ids):
	cur.execute(cur.mogrify("""SELECT * FROM authors WHERE author_id IN %s""", ids))
	return cur.fetchall()

def get_author(conn, cur, id):
	return get_authors(conn, cur, [id])[0]

def get_author_named(conn, cur, first_name, last_name):
	cur.execute(cur.mogrify("""SELECT * FROM authors WHERE first_name = %s AND last_name = %s""", (first_name, last_name)))
	return cur.fetchone()

def get_authors_first_named(conn, cur, first_name):
	cur.execute(cur.mogrify("""SELECT * FROM authors WHERE first_name = %s""", (first_name)))
	return cur.fetchall()

def get_authors_last_named(conn, cur, last_name):
	cur.execute(cur.mogrify("""SELECT * FROM authors WHERE last_name = %s""", (last_name)))
	return cur.fetchall()
# -----------
# | Authors |
# -----------

# --------
# | Tags |
# --------
def get_tags(conn, cur, ids):
	cur.execute(cur.mogrify("""SELECT * FROM tags WHERE tag_id IN %s""", ids))
	return cur.fetchall()

def get_tag(conn, cur, id):
	return get_tags(conn, cur, [ids])[0]

def get_tags_named(conn, cur, tag_names):
	cur.execute(cur.mogrify("""SELECT * FROM tags WHERE tag_name IN %s""", tag_names))
	return cur.fetchall()

def get_tag_named(conn, cur, tag_name):
	return get_tags_named(conn, cur, [tag_name])[0]
# --------
# | Tags |
# --------
