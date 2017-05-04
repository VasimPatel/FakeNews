from sklearn.externals import joblib

def important(words, val):
	if val > 0:
		return sorted(words,key=lambda l: (l[1]))[:val]
		#return sorted(words,key=lambda l: (l[1]))[:10000]
	else:
		return sorted(words,key=lambda l: (l[1]))[len(words)+val:]
		#return sorted(words,key=lambda l: (l[1]))[:10000]


def main():
	dictionary = joblib.load('loadAndsave/bayes_dict/large_test_10000_5000_5000.pkl')

	real_dict = dictionary['real']
	fake_dict = dictionary['fake']

	results = []

	for each_word, fake_val in fake_dict.items():
		if real_dict.get(each_word) is not None:
			real_val = real_dict[each_word]
			fake_val = fake_val

			rel_val = fake_val - real_val

			results.append([each_word, rel_val])
		else:
			pass


	
	# top 25 for fake
	important_fake = important(results, 50)

	# top 25 real
	important_real = important(results, -50)

	print("{0:22}{1}".format("Fake", "Real"))
	print("-----------------------------------")
	i = 1
	for fake_word, real_word in zip(important_fake, important_real):
		print("{0:20} {1}".format(fake_word[0], real_word[0]))
		i+=1

	r = []
	# for e, v in fake_dict.items():
	# 	r.append([e,v])
	# r = sorted(r,key=lambda l: (l[1]))[:100]
	# for each in r:
	# 	print(each[0])








