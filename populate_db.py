# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 13:49:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-22 00:25:00

import Utils.settings as settings
settings.init()

import os
import Utils.common_utils as utils
import Utils.connection_utils as glc
import Utils.edit_fakenews_db as edit
import Utils.get_fakenews_db as db

import json
import datetime
from unidecode import unidecode

# Read the data from the json file
def read_json_data(filename):
	with open(filename, "r") as file:
		data = json.load(file)
	return data

# Add the article to the database
def add_json_article_to_db(article, source_name):
	tag_ids = []
	for tag in article["tags"]:
		db_tag = db.get_tag_named(tag)
		if not db_tag:
			tag_ids.append(edit.add_tag(tag))
		else:
			tag_ids.append(db_tag['tag_id'])

	author_ids = []
	for author in article["author"].split("|"):
		names = author.split(" ")
		if len(names) == 2:
			db_author = db.get_author_named(names[0], names[1])
			if not db_author:
				author_ids.append(edit.add_author(names[0], names[1]))
			else:
				author_ids.append(db_author['author_id'])

	# TODO: Fix datetime stripping so that time zones are accounted for
	edit.add_article(article["title"],
		article["url"],
		datetime.datetime.strptime(article["date"][:-4], "%m/%d/%y %I:%M %p"),
		article["content"],
		db.get_source_named(source_name)['source_id'],
		author_ids,
		tag_ids
	)

# Add all the source data to the database (tracks and prints progress to console)
def add_source_data_to_db(source_data, source_name):
	# Add source to database
	edit.add_source(source_name)

	# Track total runtime
	total_runtime = 0
	# Set the last progress display time to the current time
	lpd_time = datetime.datetime.now()
	# Add articles to the database and display progress
	for i in range(0, len(source_data)):
		# This actually adds the article to the database (just passes it to another function to time how long it takes to execute)
		runtime = utils.time_it(add_json_article_to_db, source_data[i], source_name)
		# Total runtime of whole process
		total_runtime = total_runtime + runtime
		# Display only updates after at least 1 second has passed
		if (datetime.datetime.now() - lpd_time) > datetime.timedelta(seconds = 1):
			# Display progress bar
			utils.progress_bar(50, i+1, len(source_data), cur_runtime = total_runtime, last_runtime = runtime)
			# Update the last progress display time
			lpd_time = datetime.datetime.now()

	print("\nFinished adding %d articles from %s to the database." % (len(source_data), source_name))

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	add_source_data_to_db(read_json_data("politico_data.json"), "Politico")
	add_source_data_to_db(read_json_data("bb_data.json"), "BreitBart")

if __name__ == "__main__":
	main()
