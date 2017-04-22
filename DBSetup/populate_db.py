# @Author: DivineEnder <DivineHP>
# @Date:   2017-03-08 13:49:12
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-04-22 15:41:30

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

def read_nytimes_data(folder):
	articles = []
	for (dirpath, dirnames, filenames) in os.walk(folder):
		for filename in filenames:
			with open(dirpath + "/" + filename) as data:
				for line in data:
					articles.append(json.loads(line.replace("\n", "")))

	return articles

# Read the data from the json file
def read_json_data_manual(filename):
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
		tag_id = edit.add_tag(tag, VERBOSE = VERBOSE)
		tag_ids.append(tag_id)
	tag_ids = list(set(tag_ids))

	author_ids = []
	for author in article["authors"]:
		names = author.split(" ")
		first_name = unidecode(names[0])
		last_name = unidecode(names[-1])
		middle_name = unidecode(str(names[1:-1]).strip("[]").replace(",", "").replace("'", ""))
		if not middle_name:
			middle_name = None

		author_id = edit.add_author(first_name, last_name, middle_name, VERBOSE = VERBOSE)
		author_ids.append(author_id)
	author_ids = list(set(author_ids))

	edit.add_article(title = article["title"],
		url = article["url"],
		publish_date = parser.parse(article["date"]),
		content = article["content"],
		source_id = db.get_source_named(source_name)['source_id'],
		is_fake = False,
		author_ids = author_ids,
		tag_ids = tag_ids,
		VERBOSE = VERBOSE
	)

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
def add_source_data_to_db(source_data, source_name, base_url):
	# Add source to database
	edit.add_source(source_name, base_url)
	# Progress bar loop display and add to database
	utils.loop_display_progress(source_data, add_json_article_to_db, source_name)

	print("\nFinished adding %d articles from %s to the database." % (len(source_data), source_name))

def add_csv_data_to_db(filename):
	articles = read_csv_data(filename)
	utils.loop_display_progress(articles, add_csv_article_to_db)

@glc.new_connection(primary = True, pass_to_function = False)
def main():
	# add_source_data_to_db(read_json_data("data/bb_data.json"), "BreitBart")
	# add_source_data_to_db(read_json_data("data/politico_data.json"), "Politico")
	add_source_data_to_db(read_nytimes_data("data/nytimes"), "New York Times", "nytimes.com")
	# add_csv_data_to_db("data/fake.csv")
	# bu.build_token_table()

if __name__ == "__main__":
	main()
