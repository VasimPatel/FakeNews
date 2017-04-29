from textblob import TextBlob

def get(article):
	blob = TextBlob(article['content'])

	avg = 0
	index = 0

	for sentence in blob.sentences:
		avg += sentence.sentiment.polarity
		index +=1

	avg = avg/index

	return avg
