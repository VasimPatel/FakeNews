
def get(article):
	return lexical_diversity(article['content'])

def lexical_diversity(data):
	content = "".join(c for c in data if c not in ('!','.',':',',')).split(" ")
	word_count = len(content)
	vocab_size = len(set(content))
	diversity_score = vocab_size / word_count
	return diversity_score