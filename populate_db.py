# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 13:49:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineHP
# @Last modified time: 2017-03-10 14:46:54

import Utils.settings as settings
settings.init()

import os
import Utils.db_utils as db_utils
import Utils.edit_fakenews_db as edit
import Utils.get_fakenews_db as db

import json
import datetime
from unidecode import unidecode

def add_sources(conn, cur):
	edit.add_source(conn, cur, "Politico")
	edit.add_source(conn, cur, "BreitBart")

def read_json_data(filename):
	with open(filename, "r") as file:
		data = json.load(file)
	return data

@db_utils.new_connection(host = os.environ.get("DBHOST"), dbname = os.environ.get("DBNAME"), user = os.environ.get("DBUSER"), password = os.environ.get("DBPASS"))
def main(conn, cur):
	# add_sources(conn, cur)

	pol_data = read_json_data("politico_data.json")

	for article in pol_data:
		tag_ids = []
		for tag in article["tags"]:
			db_tag = db.get_tag_named(conn, cur, tag)
			if not db_tag:
				print("Adding [tag:'%s'] to database" % tag)
				tag_ids.append(edit.add_tag(conn, cur, tag))
			else:
				tag_ids.append(db_tag[0])

		author_ids = []
		for author in article["author"].split("|"):
			names = author.split(" ")
			db_author = db.get_author_named(conn, cur, names[0], names[1])
			if not db_author:
				print("Adding [author:'%s'] to database" % author)
				author_ids.append(edit.add_author(conn, cur, names[0], names[1]))
			else:
				author_ids.append(db_author[0])

		# TODO: Fix datetime stripping so that time zones are accounted for
		print("Adding [article:'%s'] to database" % article["title"])
		edit.add_article(conn, cur,
			article["title"],
			article["url"],
			datetime.datetime.strptime(article["date"][:-4], "%m/%d/%y %I:%M %p"),
			article["content"],
			db.get_source_named(conn, cur, "Politico")[0],
			author_ids,
			tag_ids
		)

if __name__ == "__main__":
	main()
