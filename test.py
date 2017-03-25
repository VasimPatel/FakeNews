import Utils.settings as settings
settings.init()

from os import path
from wordcloud import WordCloud, STOPWORDS

import Utils.connection_utils as glc

stopwords = set(STOPWORDS)


@glc.new_connection(primary = True, pass_to_function = False)
def concatContent():
	articles = glc.execute_db_query("SELECT content FROM articles WHERE created_at BETWEEN '2016-11-01 00:00:00' AND '2016-11-30 23:59:59'")
	text = ""
	for article in articles :
		contents = article["content"]
		text = text + contents
	return text

text = concatContent()
# Generate a word cloud image
wordcloud = WordCloud().generate(text)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# lower max_font_size
wordcloud = WordCloud(max_font_size=40, stopwords = stopwords).generate(text)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# The pil way (if you don't have matplotlib)
# image = wordcloud.to_image()
# image.show()