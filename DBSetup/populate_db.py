# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 13:49:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-19 20:54:36 

import Utils.settings as settings
settings.init()

import os
import Utils.bayes_utils as bu
import Utils.common_utils as utils
import Utils.connection_utils as glc
import Utils.edit_db_utils as edit
import Utils.get_db_utils as db

import sys
import csv
import json
import datetime
import dateutil.parser as parser
from unidecode import unidecode

def update_field_limit():
	maxInt = sys.maxsize
	decrement = True

	while decrement:
		try:
			csv.field_size_limit(maxInt)
			decrement = False
		except OverflowError:
			maxInt = int(maxInt/10)

def read_csv_data(filename):
	update_field_limit()
	articles = []

	with open(filename, encoding = "utf-8") as csvfile:
		reader = csv.DictReader(csvfile)
		articles = [row for row in reader]

	return articles

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
	if db.get_article_linked(article["url"]) is None:
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
	elif VERBOSE:
		print("Article '%s' is already in the database." % article["title"])

def add_csv_article_to_db(article, VERBOSE = False):
	source_id = edit.add_source(name = article["site_url"].split(".")[0], base_url = article["site_url"])

	author_names = article["author"].split(" ")
	author_first_name = unidecode(author_names[0])
	author_last_name = unidecode(author_names[-1])
	author_middle_name = unidecode(str(author_names[1:-1]).strip("[]").replace(",", "").replace("'", ""))
	author_id = edit.add_author(first_name = author_first_name,
		last_name = author_last_name,
		middle_name = author_middle_name)

	main_img_url = article["main_img_url"]
	if not main_img_url:
		main_img_url = None

	edit.add_article(title = article["title"],
		publish_date = parser.parse(article["published"]),
		content = article["text"],
		main_img_url = main_img_url,
		is_fake = True,
		fake_type = article["type"],
		author_ids = [author_id],
		source_id = source_id)

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

def add_csv_data_to_db(filename):
	articles = read_csv_data(filename)
	utils.loop_display_progress(articles, add_csv_article_to_db)

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	# add_source_data_to_db(read_json_data("data/bb_data.json"), "BreitBart")
	# add_source_data_to_db(read_json_data("data/politico_data.json"), "Politico")
	# glc.execute_db_command("""ALTER TABLE tokens ALTER COLUMN token TYPE text""")
	# bu.build_token_table()
	add_csv_data_to_db("data/fake.csv")

if __name__ == "__main__":
	main()
