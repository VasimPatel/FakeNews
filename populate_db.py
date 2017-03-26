# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 13:49:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-26 01:38:20

import Utils.settings as settings
settings.init()

import os
import Utils.common_utils as utils
import Utils.connection_utils as glc
import Utils.edit_fakenews_db as edit
import Utils.get_fakenews_db as db

import sys
import json
import datetime
import dateutil.parser as parser
from unidecode import unidecode

# Read the data from the json file
def read_json_data(filename):
	articles = []
	# Map string currently building
	article_dict_str = ""
	# Whether or not currently reading a map (to parse out list syntax)
	reading_map = False
	# Make sure map does not end in something that is a string
	ignore_map = False

	with open(filename, "r") as file:
		byte_data = file.read(9999999)
		while(byte_data):
			for i in range(0, len(byte_data)):
				char = byte_data[i]
				# Check for strings and don't check for map endings or startings within them
				if char == "\"" and (not byte_data[i - 1] == "\\" or byte_data[i - 2] == "\\"):
					ignore_map = not ignore_map
					article_dict_str = article_dict_str + char
				# Check for map starting
				elif char == "{" and not ignore_map:
					reading_map = True
					article_dict_str = "{"
				# Check for map ending
				elif char == "}" and reading_map and not ignore_map:
					reading_map = False
					article_dict_str = article_dict_str + "}"

					try:
						article = json.loads(article_dict_str)
						articles.append(article)
					except Exception as e:
						print("Problem with read. Map read was: ")
						print(unidecode(article_dict_str))
						print("\n")
						input()

						print("ERROR")
						print(e)
						input()
				# Otherwise if reading map just add the next character
				elif reading_map:
					article_dict_str = article_dict_str + char

			# Read next 9999999 bytes of data from file
			byte_data = file.read(9999999)

	# Return list of parsed articles
	return articles

# Add the article to the database
def add_json_article_to_db(article, source_name, VERBOSE = False):
	tag_ids = []
	for tag in article["tags"]:
		db_tag = db.get_tag_named(tag)
		if not db_tag:
			tag_ids.append(edit.add_tag(tag, VERBOSE = VERBOSE))
		else:
			tag_ids.append(db_tag['tag_id'])
	tag_ids = list(set(tag_ids))

	author_ids = []
	for author in article["author"].split("|"):
		names = author.split(" ")
		if len(names) == 2:
			db_author = db.get_author_named(names[0], names[1])
			if not db_author:
				author_ids.append(edit.add_author(names[0], names[1], VERBOSE = VERBOSE))
			else:
				author_ids.append(db_author['author_id'])

	edit.add_article(article["title"],
		article["url"],
		parser.parse(article["date"]),
		article["content"],
		db.get_source_named(source_name)['source_id'],
		author_ids,
		tag_ids,
		VERBOSE = VERBOSE
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
	add_source_data_to_db(read_json_data("data/politico_data.json"), "Politico")
	add_source_data_to_db(read_json_data("data/bb_data.json"), "BreitBart")

if __name__ == "__main__":
	main()
