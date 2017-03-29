# @Author: DivineEnder
# @Date:   2017-03-26 01:33:56
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2017-03-28 21:28:42

import Utils.settings as settings
settings.init()

from os import path
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

import Utils.connection_utils as glc

# Getting articles
@glc.new_connection(primary = True, pass_to_function = False)
def concatContent():
	# All articles in november
	articles = glc.execute_db_query("SELECT content FROM articles WHERE created_at BETWEEN '2016-11-01 00:00:00' AND '2016-11-30 23:59:59'")
	text = ""
	for article in articles :
		contents = article["content"]
		text = text + contents
	return text

def main():
	# Stop words
	stopwords = set(STOPWORDS)
	stopwords.add("said")

	# Get text
	text = concatContent()
	# Create image mask from logo
	img_mask = np.array(Image.open("data/wordcloud/logos/p_logo0.png"))
	# Setup word cloud
	wc = WordCloud(background_color="white", max_words=2000, mask=img_mask, stopwords=stopwords)
	# Generate a word cloud image
	wc.generate(text)
	# Write word cloud image to file
	wc.to_file("data/wordcloud/clouds/test.png")

	# Display image
	plt.imshow(wc, interpolation='bilinear')
	plt.axis("off")
	plt.figure()
	plt.imshow(img_mask, cmap=plt.cm.gray, interpolation='bilinear')
	plt.axis("off")
	plt.show()

if __name__ == "__main__":
	main()
